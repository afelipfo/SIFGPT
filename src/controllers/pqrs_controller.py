from flask import Blueprint, request, jsonify
from typing import Dict, Any
from src.services.pqrs_orchestrator_service import PQRSOrchestratorService
from src.utils.logger import logger
from src.config.config import config

# Crear blueprint para PQRS
pqrs_bp = Blueprint('pqrs', __name__)

# Inicializar servicios
try:
    openai_api_key = config.OPENAI_API_KEY or 'test-key-for-development'
    pqrs_orchestrator = PQRSOrchestratorService(openai_api_key)
    logger.info("Controlador de PQRS inicializado exitosamente")
except Exception as e:
    logger.error(f"Error al inicializar controlador de PQRS: {e}")
    pqrs_orchestrator = None

@pqrs_bp.route('/process-text', methods=['POST'])
def process_text():
    """Endpoint para procesar PQRS desde texto"""
    if not pqrs_orchestrator:
        return jsonify({
            "success": False,
            "error": "Servicio de PQRS no disponible"
        }), 503
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "Mensaje no proporcionado"
            }), 400
        
        message = data['message']
        if not message or not message.strip():
            return jsonify({
                "success": False,
                "error": "Mensaje vacío"
            }), 400
        
        # Procesar PQRS
        result = pqrs_orchestrator.process_text_pqrs(message.strip())
        
        if result["success"]:
            return jsonify({
                "success": True,
                "response": result["response"]
            })
        else:
            return jsonify({
                "success": False,
                "error": result.get("error", "Error desconocido")
            }), 500
            
    except Exception as e:
        logger.error(f"Error en endpoint process_text: {e}")
        return jsonify({
            "success": False,
            "error": "Error interno del servidor"
        }), 500

@pqrs_bp.route('/process-audio', methods=['POST'])
def process_audio():
    """Endpoint para procesar PQRS desde audio"""
    if not pqrs_orchestrator:
        return jsonify({
            "success": False,
            "error": "Servicio de PQRS no disponible"
        }), 503
    
    try:
        # Verificar que se haya enviado un archivo de audio
        if 'audio' not in request.files:
            logger.error("No se proporcionó archivo de audio en la request")
            return jsonify({
                "success": False,
                "error": "No se proporcionó archivo de audio"
            }), 400
        
        audio_file = request.files['audio']
        if not audio_file.filename:
            logger.error("Archivo de audio inválido - filename vacío")
            return jsonify({
                "success": False,
                "error": "Archivo de audio inválido"
            }), 400
        
        logger.info(f"Procesando archivo de audio: {audio_file.filename}, tipo: {audio_file.content_type}")
        
        # Obtener session_id si está disponible
        session_id = request.form.get('session_id', 'default_session')
        logger.info(f"Session ID: {session_id}")
        
        # Procesar PQRS desde audio
        result = pqrs_orchestrator.process_audio_pqrs(audio_file, session_id)
        
        if result["success"]:
            logger.info("Audio procesado exitosamente")
            return jsonify({
                "success": True,
                "transcript": result["transcription"],
                "pqrs_data": result["pqrs_data"],
                "response": result["response"]
            })
        else:
            logger.error(f"Error en procesamiento de audio: {result.get('error', 'Error desconocido')}")
            return jsonify({
                "success": False,
                "error": result.get("error", "Error desconocido en el procesamiento")
            }), 500
            
    except Exception as e:
        logger.error(f"Error en endpoint process_audio: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"Error interno del servidor al procesar el audio: {str(e)}"
        }), 500

@pqrs_bp.route('/transcribe-audio', methods=['POST'])
def transcribe_audio_only():
    """Endpoint para transcribir solo audio (sin procesar PQRS)"""
    if not pqrs_orchestrator:
        return jsonify({
            "success": False,
            "error": "Servicio de PQRS no disponible"
        }), 503
    
    try:
        if 'audio' not in request.files:
            return jsonify({
                "success": False,
                "error": "No se proporcionó archivo de audio"
            }), 400
        
        audio_file = request.files['audio']
        if not audio_file.filename:
            return jsonify({
                "success": False,
                "error": "Archivo de audio inválido"
            }), 400
        
        # Transcribir solo el audio
        transcription = pqrs_orchestrator.audio_service.transcribe_audio(audio_file)
        
        if transcription:
            return jsonify({
                "success": True,
                "transcription": transcription
            })
        else:
            return jsonify({
                "success": False,
                "error": "No se pudo transcribir el audio"
            }), 400
            
    except Exception as e:
        logger.error(f"Error en endpoint transcribe_audio: {e}")
        return jsonify({
            "success": False,
            "error": "Error interno del servidor al transcribir audio"
        }), 500

@pqrs_bp.route('/status', methods=['GET'])
def get_status():
    """Endpoint para obtener estado del sistema"""
    if not pqrs_orchestrator:
        return jsonify({
            "success": False,
            "error": "Servicio de PQRS no disponible"
        }), 503
    
    try:
        status = pqrs_orchestrator.get_system_status()
        return jsonify({
            "success": True,
            "status": status
        })
    except Exception as e:
        logger.error(f"Error en endpoint get_status: {e}")
        return jsonify({
            "success": False,
            "error": "Error interno del servidor"
        }), 500

# Mantener la clase original para compatibilidad
class PQRSController:
    """Controlador para endpoints de PQRS (mantenido para compatibilidad)"""
    
    def __init__(self, orchestrator_service: PQRSOrchestratorService):
        """Inicializa el controlador"""
        self.orchestrator = orchestrator_service
        logger.info("Controlador de PQRS inicializado")
    
    def get_response(self) -> Dict[str, Any]:
        """Endpoint para obtener respuesta a texto"""
        try:
            # Obtener datos de la request
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({
                    "success": False,
                    "error": "Mensaje no proporcionado"
                }), 400
            
            message = data['message']
            if not message or not message.strip():
                return jsonify({
                    "success": False,
                    "error": "Mensaje vacío"
                }), 400
            
            # Procesar PQRS
            result = self.orchestrator.process_text_pqrs(message.strip())
            
            if result["success"]:
                return jsonify({
                    "response": result["response"]
                })
            else:
                return jsonify({
                    "success": False,
                    "error": result.get("error", "Error desconocido")
                }), 500
                
        except Exception as e:
            logger.error(f"Error en endpoint get_response: {e}")
            return jsonify({
                "success": False,
                "error": "Error interno del servidor"
            }), 500
    
    def process_audio(self) -> Dict[str, Any]:
        """Endpoint para procesar audio"""
        try:
            # Verificar que se haya enviado un archivo de audio
            if 'audio' not in request.files:
                return jsonify({
                    "success": False,
                    "error": "No se proporcionó archivo de audio"
                }), 400
            
            audio_file = request.files['audio']
            if not audio_file.filename:
                return jsonify({
                    "success": False,
                    "error": "Archivo de audio inválido"
                }), 400
            
            # Validar formato de audio
            if not self.orchestrator.audio_service.validate_audio_format(audio_file.filename):
                return jsonify({
                    "success": False,
                    "error": f"Formato de audio no soportado. Formatos válidos: {', '.join(self.orchestrator.audio_service.get_supported_formats())}"
                }), 400
            
            # Procesar PQRS desde audio
            result = self.orchestrator.process_audio_pqrs(audio_file)
            
            if result["success"]:
                return jsonify({
                    "success": True,
                    "transcript": result["transcription"],
                    "pqrs_data": result["pqrs_data"],
                    "response": result["response"]
                })
            else:
                return jsonify({
                    "success": False,
                    "error": result.get("error", "Error desconocido en el procesamiento")
                }), 500
                
        except Exception as e:
            logger.error(f"Error en endpoint process_audio: {e}")
            return jsonify({
                "success": False,
                "error": "Error interno del servidor al procesar el audio"
            }), 500
    
    def transcribe_audio_only(self) -> Dict[str, Any]:
        """Endpoint para transcribir solo audio"""
        try:
            if 'audio' not in request.files:
                return jsonify({
                    "success": False,
                    "error": "No se proporcionó archivo de audio"
                }), 400
            
            audio_file = request.files['audio']
            if not audio_file.filename:
                return jsonify({
                    "success": False,
                    "error": "Archivo de audio inválido"
                }), 400
            
            # Transcribir solo el audio
            transcription = self.orchestrator.audio_service.transcribe_audio(audio_file)
            
            if transcription:
                return jsonify({
                    "success": True,
                    "transcription": transcription
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "No se pudo transcribir el audio"
                }), 400
                
        except Exception as e:
            logger.error(f"Error en endpoint transcribe_audio_only: {e}")
            return jsonify({
                "success": False,
                "error": "Error interno del servidor al transcribir audio"
            }), 500

class HealthController:
    """Controlador para endpoints de salud del sistema"""
    
    def __init__(self, orchestrator_service: PQRSOrchestratorService):
        """Inicializa el controlador de salud"""
        self.orchestrator = orchestrator_service
        logger.info("Controlador de salud inicializado")
    
    def health_check(self) -> Dict[str, Any]:
        """Endpoint básico de salud"""
        try:
            return jsonify({
                "status": "healthy",
                "service": "SIFGPT PQRS",
                "version": "1.0.0"
            })
        except Exception as e:
            logger.error(f"Error en health_check: {e}")
            return jsonify({
                "status": "unhealthy",
                "error": str(e)
            }), 500
    
    def detailed_health_check(self) -> Dict[str, Any]:
        """Endpoint detallado de salud del sistema"""
        try:
            # Verificar estado del sistema
            system_status = self.orchestrator.get_system_status()
            system_valid = self.orchestrator.validate_system()
            
            health_status = {
                "status": "healthy" if system_valid else "unhealthy",
                "service": "SIFGPT PQRS",
                "version": "1.0.0",
                "system_status": system_status,
                "system_valid": system_valid,
                "timestamp": "2024-01-09T14:00:00Z"
            }
            
            return jsonify(health_status)
            
        except Exception as e:
            logger.error(f"Error en detailed_health_check: {e}")
            return jsonify({
                "status": "unhealthy",
                "error": str(e)
            }), 500
