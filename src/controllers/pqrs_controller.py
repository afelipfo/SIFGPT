from flask import request, jsonify
from typing import Dict, Any
from src.services.pqrs_orchestrator_service import PQRSOrchestratorService
from src.utils.logger import logger
from src.config.config import config

class PQRSController:
    """Controlador para endpoints de PQRS"""
    
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
        """Endpoint para solo transcribir audio"""
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
            
            # Solo transcribir
            transcription = self.orchestrator.transcribe_audio_only(audio_file)
            
            return jsonify({
                "transcript": transcription,
                "success": True
            })
                
        except Exception as e:
            logger.error(f"Error en endpoint transcribe_audio_only: {e}")
            return jsonify({
                "success": False,
                "error": "Error interno del servidor"
            }), 500
    
    def get_system_status(self) -> Dict[str, Any]:
        """Endpoint para obtener estado del sistema"""
        try:
            status = self.orchestrator.get_system_status()
            return jsonify(status)
                
        except Exception as e:
            logger.error(f"Error en endpoint get_system_status: {e}")
            return jsonify({
                "success": False,
                "error": "Error interno del servidor"
            }), 500
    
    def refresh_caches(self) -> Dict[str, Any]:
        """Endpoint para refrescar cachés"""
        try:
            self.orchestrator.refresh_all_caches()
            return jsonify({
                "success": True,
                "message": "Cachés refrescadas exitosamente"
            })
                
        except Exception as e:
            logger.error(f"Error en endpoint refresh_caches: {e}")
            return jsonify({
                "success": False,
                "error": "Error interno del servidor"
            }), 500
    
    def validate_system(self) -> Dict[str, Any]:
        """Endpoint para validar el sistema"""
        try:
            is_valid = self.orchestrator.validate_system()
            return jsonify({
                "success": True,
                "system_valid": is_valid,
                "message": "Sistema válido" if is_valid else "Sistema inválido"
            })
                
        except Exception as e:
            logger.error(f"Error en endpoint validate_system: {e}")
            return jsonify({
                "success": False,
                "error": "Error interno del servidor"
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
                "service": "TUNRAG PQRS",
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
                "service": "TUNRAG PQRS",
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
