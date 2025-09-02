#!/usr/bin/env python3
"""
Aplicación principal de SIF-GPT - Sistema de PQRS
"""

from flask import Flask, render_template, request, jsonify
from src.services.pqrs_orchestrator_service import PQRSOrchestratorService
from src.services.audio_service import AudioServiceFactory
from src.controllers.historico_controller import historico_bp
from src.controllers.pqrs_controller import pqrs_bp
from src.utils.logger import logger
import os

app = Flask(__name__)

# Configuración
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = os.environ.get('SECRET_KEY', 'sif-gpt-secret-key-2024')

# Registrar blueprints
app.register_blueprint(historico_bp, url_prefix='/api/historico')
app.register_blueprint(pqrs_bp, url_prefix='/api/pqrs')

# Inicializar servicios con API key por defecto para pruebas
try:
    openai_api_key = os.environ.get('OPENAI_API_KEY', 'test-key-for-development')
    pqrs_orchestrator = PQRSOrchestratorService(openai_api_key)
    # Crear AudioService usando la factory
    audio_service = AudioServiceFactory.create_openai_service(openai_api_key)
    logger.info("Servicios inicializados correctamente")
except Exception as e:
    logger.warning(f"No se pudo inicializar servicios: {e}")
    pqrs_orchestrator = None
    audio_service = None

@app.route('/')
def index():
    """Página principal unificada"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Verificación de salud de la aplicación"""
    return jsonify({
        "status": "healthy",
        "service": "SIF-GPT PQRS System",
        "version": "2.0.0",
        "features": {
            "historico": "✅ Disponible (Unificado)",
            "pqrs_orchestrator": "✅ Disponible" if pqrs_orchestrator else "❌ No disponible",
            "audio_service": "✅ Disponible" if audio_service else "❌ No disponible"
        }
    })

@app.route('/test/historico')
def test_historico():
    """Endpoint de prueba para el servicio histórico unificado"""
    try:
        if not pqrs_orchestrator:
            return jsonify({
                "success": False,
                "error": "Servicio de orquestación no disponible"
            }), 503
        
        # Probar consulta por radicado
        radicado_test = "202510292021"
        resultado_radicado = pqrs_orchestrator.historico_service.consultar_por_radicado(radicado_test)
        
        # Probar consulta por texto
        texto_test = "reparacion"
        resultado_texto = pqrs_orchestrator.historico_service.buscar_por_texto(texto_test)
        
        # Probar estadísticas
        estadisticas = pqrs_orchestrator.historico_service.consultar_estadisticas()
        
        # Probar consulta avanzada
        filtros_test = {
            "texto": "reparacion",
            "limit": 10,
            "ordenar_por": "fecha_radicacion",
            "orden": "desc"
        }
        resultado_avanzado = pqrs_orchestrator.historico_service.consulta_avanzada(filtros_test)
        
        # Probar sugerencias
        sugerencias = pqrs_orchestrator.historico_service.obtener_sugerencias_busqueda("repar")
        
        return jsonify({
            "success": True,
            "test_radicado": {
                "radicado": radicado_test,
                "resultado": resultado_radicado
            },
            "test_texto": {
                "texto": texto_test,
                "resultado": resultado_texto
            },
            "estadisticas": estadisticas,
            "test_avanzado": resultado_avanzado,
            "sugerencias": sugerencias
        })
        
    except Exception as e:
        logger.error(f"Error en test histórico: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/debug/excel')
def debug_excel():
    """Endpoint de debug para verificar datos del Excel"""
    try:
        import pandas as pd
        
        # Cargar Excel directamente
        df = pd.read_excel('input/historico/historico2.xlsx')
        
        # Buscar registros específicos
        test_radicados = ['202510292228', '202510291196', '202510293082']
        resultados = {}
        
        for radicado in test_radicados:
            # Búsqueda en columna original
            original_search = df[df['DOCUMENTO-CarguedeinformaciónalaplicativoPQRSDdelSIF'].astype(str) == radicado]
            
            if len(original_search) > 0:
                row = original_search.iloc[0]
                resultados[radicado] = {
                    "encontrado": True,
                    "estado": row['ESTADO'],
                    "asunto": str(row['ASUNTO DE LA PETICIÓN'])[:100],
                    "solicitante": row['SOLICITANTE'],
                    "unidad": row['UNIDAD'],
                    "primer_nombre": row['PRIMERNOMBRE'],
                    "primer_apellido": row['PRIMERAPELLIDO']
                }
            else:
                resultados[radicado] = {"encontrado": False}
        
        return jsonify({
            "success": True,
            "total_registros": len(df),
            "resultados_debug": resultados
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/test/advanced-historico')
def test_advanced_historico():
    """Endpoint de prueba para funcionalidades avanzadas del histórico unificado"""
    try:
        if not pqrs_orchestrator:
            return jsonify({
                "success": False,
                "error": "Servicio de orquestación no disponible"
            }), 503
        
        # Probar consulta avanzada
        filtros_test = {
            "texto": "reparacion",
            "limit": 10,
            "ordenar_por": "fecha_radicacion",
            "orden": "desc"
        }
        
        resultado_avanzado = pqrs_orchestrator.historico_service.consulta_avanzada(filtros_test)
        
        # Probar sugerencias
        sugerencias = pqrs_orchestrator.historico_service.obtener_sugerencias_busqueda("repar")
        
        # Probar filtros disponibles
        from src.controllers.historico_controller import historico_bp
        with app.test_client() as client:
            response = client.get('/api/historico/filtros-disponibles')
            filtros_disponibles = response.get_json()
        
        return jsonify({
            "success": True,
            "consulta_avanzada": resultado_avanzado,
            "sugerencias": sugerencias,
            "filtros_disponibles": filtros_disponibles
        })
        
    except Exception as e:
        logger.error(f"Error en test avanzado: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    logger.info("🚀 Iniciando aplicación SIF-GPT unificada...")
    logger.info("📱 Frontend unificado disponible en: http://localhost:5000")
    logger.info("🔌 API disponible en: http://localhost:5000/api")
    logger.info("🧪 Tests disponibles en: http://localhost:5000/test")
    app.run(debug=True, host='0.0.0.0', port=5000)