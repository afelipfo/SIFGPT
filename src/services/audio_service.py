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
        logger.info(f"Estrategia OpenAI Whisper inicializada con modelo: {model}")
    
    def transcribe(self, audio_file) -> str:
        """Transcribe usando OpenAI Whisper"""
        try:
            # Convertir FileStorage de Flask a bytes para OpenAI
            if hasattr(audio_file, 'read'):
                # Si es un FileStorage de Flask, leer los bytes
                audio_bytes = audio_file.read()
                # Crear un objeto BytesIO para OpenAI
                from io import BytesIO
                audio_io = BytesIO(audio_bytes)
                audio_io.name = audio_file.filename  # OpenAI necesita el nombre del archivo
            else:
                audio_io = audio_file
            
            transcription = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_io,
                language='es',
                response_format="text"
            )
            logger.info("Transcripción OpenAI Whisper completada exitosamente")
            return transcription
        except Exception as e:
            logger.error(f"Error en transcripción OpenAI Whisper: {e}")
            raise
    
    def get_supported_formats(self) -> List[str]:
        """Formatos soportados por OpenAI Whisper"""
        return ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]

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
        logger.info("Servicio de audio inicializado")
    
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
            # Obtener nombre del archivo
            if hasattr(audio_file, 'name'):
                filename = os.path.basename(audio_file.name)
            else:
                filename = str(audio_file)
            
            # Realizar transcripción
            transcription_text = self.strategy.transcribe(audio_file)
            
            # Crear objeto de transcripción
            audio_transcription = AudioTranscription(
                audio_file=filename,
                transcription=transcription_text
            )
            
            logger.info(f"Transcripción completada para: {filename}")
            return audio_transcription
            
        except Exception as e:
            logger.error(f"Error en transcripción de audio: {e}")
            raise
    
    def validate_audio_format(self, filename: str) -> bool:
        """Valida si el formato de audio es soportado"""
        extension = Path(filename).suffix.lower().lstrip('.')
        supported_formats = self.strategy.get_supported_formats()
        is_valid = extension in supported_formats
        
        if not is_valid:
            logger.warning(f"Formato de audio no soportado: {extension}")
        
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
