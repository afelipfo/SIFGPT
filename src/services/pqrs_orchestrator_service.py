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
    
    def process_text_pqrs_with_context(self, text: str, conversation_context: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa una PQRS desde texto con contexto conversacional"""
        try:
            logger.info("Iniciando procesamiento de PQRS desde texto con contexto")
            
            # Paso 1: Detectar si hay consulta por radicado específico
            radicado_detectado = self._extract_radicado_from_text(text)
            if radicado_detectado:
                logger.info(f"Radicado detectado: {radicado_detectado}")
                return self._process_radicado_query(radicado_detectado, text, conversation_context)
            
            # Paso 2: Analizar si necesita clasificación completa o es conversación
            requires_classification = self._requires_full_classification(text, conversation_context)
            
            if requires_classification:
                # Clasificación completa para nuevas solicitudes
                pqrs_data = self.classifier_service.classify_pqrs(text)
                logger.info(f"PQRS clasificada como: {pqrs_data.clase}")
                
                # Actualizar contexto con información de clasificación
                conversation_context['current_topic'] = pqrs_data.tema_principal
                conversation_context['classification_history'].append({
                    'clase': pqrs_data.clase,
                    'tipo': pqrs_data.tipo_solicitud,
                    'tema': pqrs_data.tema_principal
                })
            else:
                # Usar clasificación del contexto existente
                pqrs_data = self._create_contextual_pqrs_data(text, conversation_context)
                logger.info("Usando contexto conversacional existente")
            
            # Paso 3: Generar respuesta conversacional inteligente
            response = self.response_service.generate_conversational_response(
                pqrs_data, text, conversation_context
            )
            
            # Paso 4: Preparar resultado
            result = {
                "success": True,
                "response": response,
                "pqrs_data": pqrs_data.to_dict() if hasattr(pqrs_data, 'to_dict') else {},
                "context_updated": True
            }
            
            logger.info("Procesamiento de PQRS desde texto con contexto completado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"Error en procesamiento de PQRS con contexto: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "Lo sentimos, ha ocurrido un error. ¿Podrías repetir tu consulta?",
                "context_updated": False
            }

    def _requires_full_classification(self, text: str, context: Dict[str, Any]) -> bool:
        """Determina si el mensaje requiere clasificación completa o es conversación"""
        # Mensajes cortos o de confirmación no requieren clasificación
        if len(text.strip()) < 10 or text.lower().strip() in ['ok', 'sí', 'si', 'no', 'gracias', 'perfecto']:
            return False
        
        # Si no hay contexto previo, requiere clasificación
        if not context.get('messages') or len(context['messages']) <= 1:
            return True
        
        # Si menciona nuevos temas, requiere clasificación
        new_topic_keywords = ['nuevo', 'otra', 'también', 'además', 'diferente']
        if any(keyword in text.lower() for keyword in new_topic_keywords):
            return True
        
        return False

    def _extract_radicado_from_text(self, text: str) -> str:
        """Extrae número de radicado del texto usando expresiones regulares"""
        import re
        
        # Patrones para detectar radicados
        patterns = [
            r'radicado[:\s]*(\d{12})',  # "radicado: 202510293114" o "radicado 202510293114"
            r'radicado[:\s]*(\d{4}\d{8})',  # Variación de 12 dígitos
            r'número[:\s]*(\d{12})',  # "número: 202510293114"
            r'(\d{12})',  # Simplemente 12 dígitos seguidos
            r'rad[:\s]*(\d{12})',  # "rad: 202510293114"
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1)
        
        return None

    def _process_radicado_query(self, radicado: str, original_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa una consulta específica por radicado"""
        try:
            logger.info(f"Procesando consulta por radicado: {radicado}")
            
            # Consultar en el histórico
            resultado = self.historico_service.consultar_por_radicado(radicado)
            
            # Actualizar contexto con el radicado consultado
            context['current_radicado'] = radicado
            context['last_query_type'] = 'radicado'
            
            if resultado['success']:
                datos = resultado['datos']
                
                # Generar respuesta conversacional con los datos encontrados
                response = self._format_radicado_response(datos, original_text)
                
                return {
                    "success": True,
                    "response": response,
                    "query_type": "radicado",
                    "radicado": radicado,
                    "data_found": True,
                    "context_updated": True
                }
            else:
                # Radicado no encontrado - respuesta conversacional
                response = f"No encontré información sobre el radicado {radicado}. ¿Podrías verificar que el número esté correcto? A veces hay errores de digitación. Si el número es correcto, es posible que la solicitud sea muy reciente y aún no esté en nuestro sistema."
                
                return {
                    "success": True,
                    "response": response,
                    "query_type": "radicado",
                    "radicado": radicado,
                    "data_found": False,
                    "context_updated": True
                }
                
        except Exception as e:
            logger.error(f"Error procesando consulta de radicado {radicado}: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": f"Tuve un problema consultando el radicado {radicado}. ¿Podrías intentar de nuevo?",
                "context_updated": False
            }

    def _format_radicado_response(self, datos: Dict[str, Any], original_text: str) -> str:
        """Formatea una respuesta conversacional con los datos del radicado"""
        nombre = datos.get('solicitante', 'Ciudadano/a')
        estado = datos.get('estado_actual', 'Sin estado')
        fecha = datos.get('fecha_radicacion', 'No disponible')
        unidad = datos.get('unidad_responsable', 'Secretaría de Infraestructura Física')
        asunto = datos.get('asunto', 'Solicitud registrada')
        
        # Respuesta conversacional profesional y amigable
        response = f"¡Hemos recibido tu solicitud el día {fecha}! 📋\n\n"
        response += f"📝 Tu mensaje: \"{asunto}\"\n\n"
        response += f"📊 Estado: {estado}\n"
        response += f"🏢 Unidad responsable: {unidad}\n\n"
        
        if estado.lower() in ['recibida', 'en proceso', 'pendiente']:
            response += "Tu solicitud está siendo procesada según los tiempos establecidos por la normatividad vigente. ¡Gracias por contactarnos! 😊"
        elif estado.lower() in ['resuelta', 'resuelto', 'finalizada']:
            response += "¡Excelente! Tu solicitud ya fue resuelta. Si tienes dudas adicionales, no dudes en preguntarme."
        else:
            response += "Te mantendremos informado sobre cualquier actualización en tu caso."
            
        return response

    def _create_contextual_pqrs_data(self, text: str, context: Dict[str, Any]) -> PQRSData:
        """Crea datos de PQRS basados en el contexto conversacional"""
        # Usar información del contexto previo
        last_classification = context['classification_history'][-1] if context['classification_history'] else {}
        
        return PQRSData(
            nombre=context.get('user_info', {}).get('nombre', 'Ciudadano/a'),
            telefono=context.get('user_info', {}).get('telefono', ''),
            cedula=context.get('user_info', {}).get('cedula', ''),
            clase=last_classification.get('clase', 'CONVERSACION'),
            explicacion=text,
            radicado=context.get('current_radicado', ''),
            entidad_responde="Secretaría de Infraestructura Física",
            es_faq="No",
            barrio=context.get('user_info', {}).get('barrio', ''),
            tipo_solicitud=last_classification.get('tipo', 'Seguimiento'),
            tema_principal=context.get('current_topic', 'Conversación')
        )

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
            
            # Paso 1: Clasificar PQRS con fallback
            try:
                pqrs_data = self.classifier_service.classify_pqrs(text)
                logger.info(f"PQRS clasificada como: {pqrs_data.clase}")
            except Exception as e:
                logger.warning(f"Error en clasificación, usando fallback: {e}")
                # Crear clasificación básica de fallback
                from src.models.pqrs_model import PQRSData
                pqrs_data = PQRSData(
                    nombre="",
                    telefono="",
                    cedula="",
                    clase="SOLICITUD-INTERÉS PARTICULAR",
                    explicacion="Clasificación automática",
                    radicado="",
                    entidad_responde="Secretaría de Infraestructura Física",
                    es_faq="No",
                    barrio="",
                    tipo_solicitud="SOLICITUD-INTERÉS PARTICULAR",
                    tema_principal="Infraestructura física"
                )
            
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
    
    def get_audio_files(self, audio_path: str) -> list:
        """Obtiene lista de archivos de audio del directorio especificado"""
        try:
            import os
            from pathlib import Path
            
            audio_dir = Path(audio_path)
            if not audio_dir.exists():
                logger.warning(f"Directorio de audio no existe: {audio_path}")
                return []
            
            audio_files = []
            for ext in config.AUDIO_EXTENSIONS:
                audio_files.extend(audio_dir.glob(ext))
            
            logger.info(f"Encontrados {len(audio_files)} archivos de audio en {audio_path}")
            return audio_files
            
        except Exception as e:
            logger.error(f"Error al obtener archivos de audio: {e}")
            return []
    
    def transcribe_audio_only(self, audio_file_path: str) -> str:
        """Transcribe solo el audio sin procesar PQRS"""
        try:
            logger.info(f"Iniciando transcripción de audio: {audio_file_path}")
            
            # Crear un objeto similar a FileStorage para compatibilidad
            class MockFileStorage:
                def __init__(self, file_path):
                    self.file_path = file_path
                    self.filename = os.path.basename(file_path)
                
                def read(self):
                    with open(self.file_path, 'rb') as f:
                        return f.read()
            
            mock_audio_file = MockFileStorage(audio_file_path)
            transcription = self.audio_service.transcribe_audio(mock_audio_file)
            
            logger.info(f"Audio transcrito exitosamente: {len(transcription)} caracteres")
            return transcription
            
        except Exception as e:
            logger.error(f"Error al transcribir audio: {e}")
            return ""
    
    def consultar_historico_inteligente(self, consulta: str) -> Dict[str, Any]:
        """Consulta inteligente del histórico usando IA"""
        try:
            logger.info(f"Iniciando consulta inteligente: {consulta}")
            
            # Usar el servicio de histórico para la consulta
            resultado = self.historico_service.consulta_inteligente(consulta)
            
            logger.info("Consulta inteligente completada exitosamente")
            return resultado
            
        except Exception as e:
            logger.error(f"Error en consulta inteligente: {e}")
            return {
                "success": False,
                "error": str(e),
                "mensaje": "Error al realizar consulta inteligente"
            }
