from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.append('src/')

from src.config.config import config
from src.utils.logger import logger
from src.services.pqrs_orchestrator_service import PQRSOrchestratorService
from src.controllers.pqrs_controller import PQRSController, HealthController

# Cargar variables de entorno
load_dotenv()

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    CORS(app)
    
    # Configuración de la aplicación
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DEBUG'] = config.DEBUG
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Validar configuración
    try:
        config.validate_config()
        logger.info("Configuración validada exitosamente")
    except Exception as e:
        logger.error(f"Error en configuración: {e}")
        raise
    
    # Inicializar servicios
    try:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY no está configurada")
        
        orchestrator_service = PQRSOrchestratorService(openai_api_key)
        logger.info("Servicios inicializados exitosamente")
        
    except Exception as e:
        logger.error(f"Error al inicializar servicios: {e}")
        raise
    
    # Inicializar controladores
    pqrs_controller = PQRSController(orchestrator_service)
    health_controller = HealthController(orchestrator_service)
    
    # Configurar rutas
    @app.route('/')
    def home():
        """Página principal"""
        return render_template('index.html')
    
    @app.route('/get_response', methods=['POST'])
    def get_response():
        """Endpoint para obtener respuesta a texto"""
        return pqrs_controller.get_response()
    
    @app.route('/process_audio', methods=['POST'])
    def process_audio():
        """Endpoint para procesar audio completo"""
        return pqrs_controller.process_audio()
    
    @app.route('/transcribe_audio', methods=['POST'])
    def transcribe_audio():
        """Endpoint para solo transcribir audio"""
        return pqrs_controller.transcribe_audio_only()
    
    @app.route('/system/status', methods=['GET'])
    def system_status():
        """Endpoint para obtener estado del sistema"""
        return pqrs_controller.get_system_status()
    
    @app.route('/system/refresh', methods=['POST'])
    def refresh_caches():
        """Endpoint para refrescar cachés"""
        return pqrs_controller.refresh_caches()
    
    @app.route('/system/validate', methods=['GET'])
    def validate_system():
        """Endpoint para validar el sistema"""
        return pqrs_controller.validate_system()
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint básico de salud"""
        return health_controller.health_check()
    
    @app.route('/health/detailed', methods=['GET'])
    def detailed_health_check():
        """Endpoint detallado de salud"""
        return health_controller.detailed_health_check()
    
    # Manejador de errores global
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Maneja excepciones no capturadas"""
        logger.error(f"Excepción no capturada: {e}")
        return jsonify({
            "success": False,
            "error": "Error interno del servidor",
            "message": str(e) if config.DEBUG else "Ha ocurrido un error inesperado"
        }), 500
    
    # Manejador de errores 404
    @app.errorhandler(404)
    def not_found(e):
        """Maneja rutas no encontradas"""
        logger.warning(f"Ruta no encontrada: {request.path}")
        return jsonify({
            "success": False,
            "error": "Ruta no encontrada",
            "path": request.path
        }), 404
    
    # Manejador de errores 405
    @app.errorhandler(405)
    def method_not_allowed(e):
        """Maneja métodos HTTP no permitidos"""
        logger.warning(f"Método no permitido: {request.method} en {request.path}")
        return jsonify({
            "success": False,
            "error": "Método no permitido",
            "method": request.method,
            "path": request.path
        }), 405
    
    # Manejador de errores 413 (Payload Too Large)
    @app.errorhandler(413)
    def payload_too_large(e):
        """Maneja archivos demasiado grandes"""
        logger.warning(f"Archivo demasiado grande enviado")
        return jsonify({
            "success": False,
            "error": "Archivo demasiado grande",
            "message": "El archivo excede el tamaño máximo permitido (16MB)"
        }), 413
    
    logger.info("Aplicación Flask configurada exitosamente")
    return app

# Crear aplicación
app = create_app()

if __name__ == '__main__':
    try:
        logger.info("Iniciando aplicación TUNRAG...")
        app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
        logger.info("Aplicación iniciada exitosamente en puerto 5000")
    except Exception as e:
        logger.error(f"Error al iniciar aplicación: {e}")
        sys.exit(1)