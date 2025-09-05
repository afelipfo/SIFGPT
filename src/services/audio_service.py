from abc import ABC, abstractmethod
from typing import Optional, List
from pathlib import Path
import os
from openai import OpenAI
from faster_whisper import WhisperModel
from src.utils.logger import logger
from src.config.config import config
from src.models.pqrs_model import AudioTranscription

class TranscriptionStrategy(ABC):
    """Estrategia abstracta para transcripción de audio"""
    
    @abstractmethod
    def transcribe(self, audio_file) -> str:
        """Transcribe un archivo de audio"""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Retorna los formatos de audio soportados"""
        pass

class OpenAIWhisperStrategy(TranscriptionStrategy):
    """Estrategia de transcripción usando OpenAI Whisper"""
    
    def __init__(self, api_key: str, model: str = 'whisper-1'):
        """Inicializa la estrategia OpenAI Whisper"""
        self.client = OpenAI(api_key=api_key)
        self.model = model
        # Reducir logging
        pass  # logger.info(f"Estrategia OpenAI Whisper inicializada con modelo: {model}")
    
    def transcribe(self, audio_file) -> str:
        """Transcribe usando OpenAI Whisper"""
        try:
            logger.info("Iniciando transcripción con OpenAI Whisper")
            
            # Convertir FileStorage de Flask a bytes para OpenAI
            if hasattr(audio_file, 'read'):
                # Si es un FileStorage de Flask, leer los bytes
                logger.info(f"Procesando FileStorage - filename: {getattr(audio_file, 'filename', 'unknown')}")
                
                # Resetear posición del archivo por si ya fue leído
                if hasattr(audio_file, 'seek'):
                    audio_file.seek(0)
                
                audio_bytes = audio_file.read()
                logger.info(f"Audio leído: {len(audio_bytes)} bytes")
                
                if len(audio_bytes) == 0:
                    raise ValueError("El archivo de audio está vacío")
                
                # Crear un objeto BytesIO para OpenAI
                from io import BytesIO
                audio_io = BytesIO(audio_bytes)
                
                # OpenAI necesita el nombre del archivo para determinar el formato
                if hasattr(audio_file, 'filename') and audio_file.filename:
                    audio_io.name = audio_file.filename
                else:
                    # Asumir formato WAV por defecto si no hay nombre
                    audio_io.name = 'recording.wav'
                
                logger.info(f"Preparando para transcripción con nombre: {audio_io.name}")
            else:
                audio_io = audio_file
                logger.info("Usando archivo directo para transcripción")
            
            # Realizar transcripción
            transcription = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_io,
                language='es',
                response_format="text"
            )
            
            if not transcription or not transcription.strip():
                raise ValueError("La transcripción resultó vacía")
            
            logger.info(f"Transcripción OpenAI Whisper completada exitosamente: {len(transcription)} caracteres")
            return transcription.strip()
            
        except Exception as e:
            logger.error(f"Error en transcripción OpenAI Whisper: {str(e)}", exc_info=True)
            raise
    
    def get_supported_formats(self) -> List[str]:
        """Formatos soportados por OpenAI Whisper"""
        return ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm", "ogg", "flac", "aac"]

class FasterWhisperStrategy(TranscriptionStrategy):
    """Estrategia de transcripción usando Faster Whisper (local)"""
    
    def __init__(self, model: str = 'large-v3', compute_type: str = "int8"):
        """Inicializa la estrategia Faster Whisper"""
        self.model = WhisperModel(model, compute_type=compute_type)
        logger.info(f"Estrategia Faster Whisper inicializada con modelo: {model}")
    
    def transcribe(self, audio_file) -> str:
        """Transcribe usando Faster Whisper"""
        try:
            if hasattr(audio_file, 'name'):
                file_path = audio_file.name
            else:
                file_path = str(audio_file)
            
            segments, info = self.model.transcribe(
                file_path, 
                beam_size=2, 
                language="es"
            )
            
            transcription = " ".join([segment.text for segment in segments])
            logger.info("Transcripción Faster Whisper completada exitosamente")
            return transcription
        except Exception as e:
            logger.error(f"Error en transcripción Faster Whisper: {e}")
            raise
    
    def get_supported_formats(self) -> List[str]:
        """Formatos soportados por Faster Whisper"""
        return ["wav", "mp3", "flac", "ogg", "m4a", "aac"]

class AudioService:
    """Servicio principal para manejo de audio"""
    
    def __init__(self, strategy: TranscriptionStrategy):
        """Inicializa el servicio de audio con una estrategia"""
        self.strategy = strategy
        self.audio_extensions = config.AUDIO_EXTENSIONS
        # logger.info("Servicio de audio inicializado")
    
    def get_audio_files(self, folder_path: str) -> List[str]:
        """Obtiene lista de archivos de audio en un directorio"""
        try:
            from glob import glob
            audio_files = []
            for ext in self.audio_extensions:
                audio_files.extend(glob(os.path.join(folder_path, ext)))
            
            logger.info(f"Encontrados {len(audio_files)} archivos de audio en {folder_path}")
            return audio_files
        except Exception as e:
            logger.error(f"Error al obtener archivos de audio: {e}")
            return []
    
    def transcribe_audio(self, audio_file) -> AudioTranscription:
        """Transcribe un archivo de audio"""
        try:
            logger.info("Iniciando transcripción de audio")
            
            # Obtener nombre del archivo
            if hasattr(audio_file, 'filename'):
                filename = audio_file.filename
            elif hasattr(audio_file, 'name'):
                filename = os.path.basename(audio_file.name)
            else:
                filename = "recording.wav"  # Nombre por defecto
            
            logger.info(f"Procesando archivo: {filename}")
            
            # Validar formato antes de transcribir (pero no fallar si no es válido)
            if not self.validate_audio_format(filename):
                logger.warning(f"Formato posiblemente no soportado, pero continuando: {filename}")
            
            # Realizar transcripción
            logger.info("Iniciando proceso de transcripción...")
            transcription_text = self.strategy.transcribe(audio_file)
            
            # Validar que la transcripción no esté vacía
            if not transcription_text or not transcription_text.strip():
                raise ValueError("La transcripción resultó vacía - el audio podría no contener habla reconocible")
            
            # Crear objeto de transcripción
            audio_transcription = AudioTranscription(
                audio_file=filename,
                transcription=transcription_text.strip()
            )
            
            logger.info(f"Transcripción completada exitosamente para: {filename} - {len(transcription_text)} caracteres")
            logger.info(f"Texto transcrito: {transcription_text[:100]}...")  # Primeros 100 caracteres para debug
            
            return audio_transcription
            
        except Exception as e:
            logger.error(f"Error en transcripción de audio: {str(e)}", exc_info=True)
            raise
    
    def validate_audio_format(self, filename: str) -> bool:
        """Valida si el formato de audio es soportado"""
        if not filename:
            logger.warning("Nombre de archivo vacío, asumiendo formato válido")
            return True  # Permitir archivos sin nombre específico (como recording.wav)
        
        extension = Path(filename).suffix.lower().lstrip('.')
        if not extension:
            logger.warning("Sin extensión, asumiendo formato válido")
            return True  # Permitir archivos sin extensión específica
        
        supported_formats = self.strategy.get_supported_formats()
        is_valid = extension in supported_formats
        
        if not is_valid:
            logger.warning(f"Formato de audio no soportado: {extension}. Formatos soportados: {supported_formats}")
        else:
            logger.info(f"Formato de audio válido: {extension}")
        
        return is_valid
    
    def change_strategy(self, strategy: TranscriptionStrategy):
        """Cambia la estrategia de transcripción"""
        self.strategy = strategy
        logger.info("Estrategia de transcripción cambiada")
    
    def get_supported_formats(self) -> List[str]:
        """Obtiene formatos soportados por la estrategia actual"""
        return self.strategy.get_supported_formats()

class AudioServiceFactory:
    """Factory para crear servicios de audio"""
    
    @staticmethod
    def create_openai_service(api_key: str, model: str = 'whisper-1') -> AudioService:
        """Crea un servicio de audio con estrategia OpenAI"""
        strategy = OpenAIWhisperStrategy(api_key, model)
        return AudioService(strategy)
    
    @staticmethod
    def create_faster_whisper_service(model: str = 'large-v3', compute_type: str = "int8") -> AudioService:
        """Crea un servicio de audio con estrategia Faster Whisper"""
        strategy = FasterWhisperStrategy(model, compute_type)
        return AudioService(strategy)
