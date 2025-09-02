from typing import Optional, Dict, Any
from openai import OpenAI
from src.utils.logger import logger
from src.config.config import config
from src.models.pqrs_model import PQRSData, AudioTranscription
from src.services.audio_service import AudioService, AudioServiceFactory
from src.services.pqrs_classifier_service import PQRSClassifierService
from src.services.response_generator_service import ResponseGeneratorService
from src.services.historico_query_service import HistoricoQueryService
from src.repositories.pqrs_repository import PQRSRepository, PromptRepository

class PQRSOrchestratorService:
    """Servicio orquestador principal para el procesamiento de PQRS"""
    
    def __init__(self, openai_api_key: str, base_url: Optional[str] = None):
        """Inicializa el orquestador de PQRS"""
        try:
            # Validar configuración
            config.validate_config()
            
            # Inicializar cliente OpenAI
            self.openai_client = OpenAI(
                base_url=base_url or config.OPENAI_BASE_URL,
                api_key=openai_api_key
            )
            
            # Inicializar repositorios
            self.pqrs_repository = PQRSRepository()
            self.prompt_repository = PromptRepository()
            
            # Inicializar servicios
            self.audio_service = AudioServiceFactory.create_openai_service(
                openai_api_key, 
                config.WHISPER_MODEL
            )
            self.classifier_service = PQRSClassifierService(
                self.openai_client, 
                self.prompt_repository
            )
            self.response_service = ResponseGeneratorService(
                self.openai_client, 
                self.prompt_repository, 
                self.pqrs_repository
            )
            self.historico_service = HistoricoQueryService(self.pqrs_repository)
            
            logger.info("Orquestador de PQRS inicializado exitosamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar orquestador de PQRS: {e}")
            raise
    
    def process_audio_pqrs(self, audio_file) -> Dict[str, Any]:
        """Procesa una PQRS desde un archivo de audio"""
        try:
            logger.info("Iniciando procesamiento de PQRS desde audio")
            
            # Paso 1: Transcribir audio
            audio_transcription = self.audio_service.transcribe_audio(audio_file)
            logger.info(f"Audio transcrito: {len(audio_transcription.transcription)} caracteres")
            
            # Paso 2: Clasificar PQRS
            pqrs_data = self.classifier_service.classify_pqrs(audio_transcription.transcription)
            logger.info(f"PQRS clasificada como: {pqrs_data.clase}")
            
            # Paso 3: Generar respuesta
            response = self.response_service.generate_response(pqrs_data, audio_transcription.transcription)
            logger.info("Respuesta generada exitosamente")
            
            # Paso 4: Preparar resultado
            result = {
                "success": True,
                "transcription": audio_transcription.transcription,
                "pqrs_data": pqrs_data.to_dict(),
                "response": response,
                "audio_file": audio_transcription.audio_file,
                "timestamp": audio_transcription.timestamp.isoformat()
            }
            
            logger.info("Procesamiento de PQRS desde audio completado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"Error en procesamiento de PQRS desde audio: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcription": "",
                "pqrs_data": {},
                "response": "Lo sentimos, ha ocurrido un error en el procesamiento de tu solicitud.",
                "audio_file": "",
                "timestamp": ""
            }
    
    def process_text_pqrs(self, text: str, test: bool = False) -> Dict[str, Any]:
        """Procesa una PQRS desde texto"""
        try:
            logger.info("Iniciando procesamiento de PQRS desde texto")
            
            if test:
                response = self.response_service.generate_test_response()
                result = {
                    "success": True,
                    "transcription": text,
                    "pqrs_data": {},
                    "response": response,
                    "test_mode": True
                }
                logger.info("Modo de prueba completado")
                return result
            
            # Paso 1: Clasificar PQRS
            pqrs_data = self.classifier_service.classify_pqrs(text)
            logger.info(f"PQRS clasificada como: {pqrs_data.clase}")
            
            # Paso 2: Generar respuesta
            response = self.response_service.generate_response(pqrs_data, text)
            logger.info("Respuesta generada exitosamente")
            
            # Paso 3: Preparar resultado
            result = {
                "success": True,
                "transcription": text,
                "pqrs_data": pqrs_data.to_dict(),
                "response": response,
                "test_mode": False
            }
            
            logger.info("Procesamiento de PQRS desde texto completado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"Error en procesamiento de PQRS desde texto: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcription": text,
                "pqrs_data": {},
                "response": "Lo sentimos, ha ocurrido un error en el procesamiento de tu solicitud.",
                "test_mode": False
            }
    
    def get_audio_files(self, folder_path: str) -> list:
        """Obtiene lista de archivos de audio en un directorio"""
        return self.audio_service.get_audio_files(folder_path)
    
    def transcribe_audio_only(self, audio_file) -> str:
        """Solo transcribe audio sin procesar PQRS"""
        try:
            audio_transcription = self.audio_service.transcribe_audio(audio_file)
            return audio_transcription.transcription
        except Exception as e:
            logger.error(f"Error en transcripción de audio: {e}")
            raise
    
    def change_audio_strategy(self, strategy_type: str, **kwargs):
        """Cambia la estrategia de transcripción de audio"""
        try:
            if strategy_type == "openai":
                new_strategy = AudioServiceFactory.create_openai_service(
                    kwargs.get('api_key', config.OPENAI_API_KEY),
                    kwargs.get('model', config.WHISPER_MODEL)
                )
            elif strategy_type == "faster_whisper":
                new_strategy = AudioServiceFactory.create_faster_whisper_service(
                    kwargs.get('model', 'large-v3'),
                    kwargs.get('compute_type', 'int8')
                )
            else:
                raise ValueError(f"Estrategia de audio no soportada: {strategy_type}")
            
            self.audio_service = new_strategy
            logger.info(f"Estrategia de audio cambiada a: {strategy_type}")
            
        except Exception as e:
            logger.error(f"Error al cambiar estrategia de audio: {e}")
            raise
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el estado del sistema"""
        try:
            status = {
                "audio_service": {
                    "strategy": type(self.audio_service.strategy).__name__,
                    "supported_formats": self.audio_service.get_supported_formats()
                },
                "classifier_service": {
                    "model": config.OPENAI_MODEL,
                    "status": "active"
                },
                "response_service": {
                    "status": "active"
                },
                "repositories": {
                    "pqrs_cache_size": len(self.pqrs_repository._historico_df) if self.pqrs_repository._historico_df is not None else 0,
                    "prompts_cache_size": len(self.prompt_repository._prompts_cache),
                    "plantillas_cache_size": len(self.prompt_repository._plantillas_cache)
                }
            }
            return status
        except Exception as e:
            logger.error(f"Error al obtener estado del sistema: {e}")
            return {"error": str(e)}
    
    def refresh_all_caches(self):
        """Refresca todas las cachés del sistema"""
        try:
            self.pqrs_repository.refresh_cache()
            self.prompt_repository.refresh_cache()
            logger.info("Todas las cachés han sido refrescadas")
        except Exception as e:
            logger.error(f"Error al refrescar cachés: {e}")
            raise
    
    def validate_system(self) -> bool:
        """Valida que el sistema esté funcionando correctamente"""
        try:
            # Validar configuración
            config.validate_config()
            
            # Validar servicios
            if not self.openai_client:
                logger.error("Cliente OpenAI no inicializado")
                return False
            
            # Validar repositorios
            test_historico = self.pqrs_repository.get_all_historico()
            if not test_historico:
                logger.warning("No se pudieron cargar datos históricos")
            
            # Validar prompts
            test_prompt = self.prompt_repository.get_prompt('sys_prompt')
            if not test_prompt:
                logger.error("No se pudo cargar prompt del sistema")
                return False
            
            logger.info("Validación del sistema completada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en validación del sistema: {e}")
            return False
    
    def consultar_historico(self, consulta: str, tipo_consulta: str = 'inteligente') -> Dict[str, Any]:
        """Realiza consultas al histórico de PQRS"""
        try:
            logger.info(f"Iniciando consulta histórica de tipo: {tipo_consulta}")
            
            if tipo_consulta == 'por_radicado':
                resultado = self.historico_service.consultar_por_radicado(consulta)
            elif tipo_consulta == 'por_texto':
                resultado = self.historico_service.buscar_por_texto(consulta)
            elif tipo_consulta == 'por_nombre':
                resultado = self.historico_service.buscar_por_nombre(consulta)
            elif tipo_consulta == 'estadisticas':
                resultado = self.historico_service.consultar_estadisticas()
            elif tipo_consulta == 'ayuda':
                resultado = self.historico_service.obtener_ayuda_consultas()
            else:
                # Consulta inteligente por defecto
                resultado = self.historico_service.consulta_inteligente(consulta)
            
            logger.info(f"Consulta histórica completada: {resultado.get('tipo_consulta', 'desconocido')}")
            return resultado
            
        except Exception as e:
            logger.error(f"Error en consulta histórica: {e}")
            return {
                "success": False,
                "error": str(e),
                "mensaje": "Error al realizar la consulta histórica"
            }
    
    def obtener_resumen_historico(self) -> Dict[str, Any]:
        """Obtiene un resumen general del histórico"""
        try:
            logger.info("Obteniendo resumen del histórico")
            resultado = self.historico_service.consultar_estadisticas()
            logger.info("Resumen del histórico obtenido exitosamente")
            return resultado
            
        except Exception as e:
            logger.error(f"Error al obtener resumen del histórico: {e}")
            return {
                "success": False,
                "error": str(e),
                "mensaje": "Error al obtener resumen del histórico"
            }
