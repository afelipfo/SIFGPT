"""
TUNRAG PQRS - Clase de compatibilidad para migración
====================================================

Esta clase mantiene la interfaz original para compatibilidad con código existente,
pero internamente usa la nueva arquitectura refactorizada.

IMPORTANTE: Esta clase está marcada como DEPRECATED. 
Usar la nueva arquitectura directamente es la opción recomendada.
"""

import warnings
from typing import Optional, List
from src.services.pqrs_orchestrator_service import PQRSOrchestratorService
from src.utils.logger import logger

class PQRSProcessor:
    """
    Clase de compatibilidad para migración gradual.
    
    DEPRECATED: Usar PQRSOrchestratorService directamente.
    """
    
    def __init__(self, 
                 openai_api_key: str, 
                 hotwords: str = "", 
                 whisper_model: str = 'large-v3', 
                 openai_model: str = 'gpt-4o', 
                 base_url: Optional[str] = None):
        """
        Inicializa el procesador de PQRS (compatibilidad)
        
        Args:
            openai_api_key: Clave API de OpenAI
            hotwords: Palabras clave (no usado en nueva arquitectura)
            whisper_model: Modelo de Whisper a usar
            openai_model: Modelo de OpenAI a usar
            base_url: URL base de OpenAI (opcional)
        """
        warnings.warn(
            "PQRSProcessor está DEPRECATED. Usar PQRSOrchestratorService directamente.",
            DeprecationWarning,
            stacklevel=2
        )
        
        try:
            # Inicializar el nuevo orquestador
            self.orchestrator = PQRSOrchestratorService(openai_api_key, base_url)
            
            # Mantener atributos para compatibilidad
            self.openai_client = self.orchestrator.openai_client
            self.hotwords = hotwords  # No usado en nueva arquitectura
            self.openai_model = openai_model
            self.whisper_model = whisper_model
            
            # Atributos de compatibilidad
            self.transcription = ""
            self.audio_files = []
            
            logger.info("PQRSProcessor (compatibilidad) inicializado exitosamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar PQRSProcessor: {e}")
            raise
    
    def get_audio_files(self, folder_path: str) -> List[str]:
        """Obtiene archivos de audio (compatibilidad)"""
        try:
            self.audio_files = self.orchestrator.get_audio_files(folder_path)
            return self.audio_files
        except Exception as e:
            logger.error(f"Error al obtener archivos de audio: {e}")
            return []
    
    def transcribe_audio(self, file_path: str) -> str:
        """Transcribe audio usando Faster Whisper (compatibilidad)"""
        try:
            # Cambiar a estrategia Faster Whisper
            self.orchestrator.change_audio_strategy("faster_whisper", model=self.whisper_model)
            
            # Transcribir archivo
            with open(file_path, 'rb') as audio_file:
                transcription = self.orchestrator.transcribe_audio_only(audio_file)
            
            self.transcription = transcription
            logger.info(f"Audio transcrito: {len(transcription)} caracteres")
            return transcription
            
        except Exception as e:
            logger.error(f"Error en transcripción de audio: {e}")
            raise
    
    def transcribe_audio_openai(self, audio_file) -> str:
        """Transcribe audio usando OpenAI Whisper (compatibilidad)"""
        try:
            # Cambiar a estrategia OpenAI
            self.orchestrator.change_audio_strategy("openai", model=self.whisper_model)
            
            # Transcribir archivo
            transcription = self.orchestrator.transcribe_audio_only(audio_file)
            
            self.transcription = transcription
            logger.info(f"Audio transcrito con OpenAI: {len(transcription)} caracteres")
            return transcription
            
        except Exception as e:
            logger.error(f"Error en transcripción OpenAI: {e}")
            raise
    
    def model_answer(self, transcription: str, test: bool = False) -> str:
        """Genera respuesta del modelo (compatibilidad)"""
        try:
            if test:
                result = self.orchestrator.process_text_pqrs(transcription, test=True)
                return result["response"]
            else:
                result = self.orchestrator.process_text_pqrs(transcription, test=False)
                return result["response"]
                
        except Exception as e:
            logger.error(f"Error al generar respuesta del modelo: {e}")
            raise
    
    def process_audios(self, folder_path: str, user_prompt: str, system_prompt: str) -> List[dict]:
        """Procesa múltiples archivos de audio (compatibilidad)"""
        try:
            results = []
            audio_files = self.get_audio_files(folder_path)
            
            for audio_file in audio_files:
                try:
                    # Transcribir audio
                    transcription = self.transcribe_audio(audio_file)
                    
                    # Procesar PQRS
                    result = self.orchestrator.process_text_pqrs(transcription)
                    
                    results.append({
                        "audio_file": audio_file,
                        "transcription": transcription,
                        "pqrs_data": result.get("pqrs_data", {}),
                        "response": result.get("response", "")
                    })
                    
                except Exception as e:
                    logger.error(f"Error procesando archivo {audio_file}: {e}")
                    results.append({
                        "audio_file": audio_file,
                        "transcription": "",
                        "error": str(e)
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error en procesamiento de audios: {e}")
            return []
    
    @staticmethod
    def save_to_json(data: dict, output_file: str):
        """Guarda datos en JSON (compatibilidad)"""
        try:
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Datos guardados en {output_file}")
        except Exception as e:
            logger.error(f"Error al guardar JSON: {e}")
            raise
    
    def get_prompts(self):
        """Obtiene prompts (compatibilidad - no usado en nueva arquitectura)"""
        warnings.warn(
            "get_prompts() está DEPRECATED. Los prompts se manejan automáticamente en la nueva arquitectura.",
            DeprecationWarning,
            stacklevel=2
        )
        # Los prompts se manejan automáticamente en PromptRepository
        pass

# Alias para compatibilidad
PQRS = PQRSProcessor 