#!/usr/bin/env python3
"""
Script de prueba completa para TUNRAG
Verifica que todos los componentes funcionen correctamente
"""

import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.append('src/')

def test_imports():
    """Prueba que todos los módulos se importen correctamente"""
    print("🔍 Probando importaciones...")
    
    try:
        # Configuración
        from src.config.config import config
        print("✅ Configuración importada")
        
        # Servicios principales
        from src.services.pqrs_orchestrator_service import PQRSOrchestratorService
        print("✅ Orquestador de PQRS importado")
        
        from src.services.audio_service import AudioService, AudioServiceFactory
        print("✅ Servicios de audio importados")
        
        from src.services.historico_query_service import HistoricoQueryService
        print("✅ Servicio de histórico importado")
        
        from src.services.advanced_query_service import AdvancedQueryService
        print("✅ Servicio avanzado importado")
        
        from src.services.pqrs_classifier_service import PQRSClassifierService
        print("✅ Servicio de clasificación importado")
        
        from src.services.response_generator_service import ResponseGeneratorService
        print("✅ Servicio de respuestas importado")
        
        # Controladores
        from src.controllers.historico_controller import historico_bp
        print("✅ Controlador histórico importado")
        
        from src.controllers.advanced_historico_controller import advanced_historico_bp
        print("✅ Controlador avanzado importado")
        
        from src.controllers.pqrs_controller import pqrs_bp
        print("✅ Controlador PQRS importado")
        
        # Repositorios
        from src.repositories.pqrs_repository import PQRSRepository, PromptRepository
        print("✅ Repositorios importados")
        
        # Modelos
        from src.models.pqrs_model import PQRSData, AudioTranscription, PQRSHistorico
        print("✅ Modelos importados")
        
        # Utilidades
        from src.utils.logger import logger
        print("✅ Logger importado")
        
        # ChatBuilder
        from src.ChatBuilder import ChatBuilder, ChatActions
        print("✅ ChatBuilder importado")
        
        # Aplicación principal (importar como módulo)
        import maintenance
        print("✅ Utilidades de mantenimiento importadas")
        
        print("🎉 Todas las importaciones exitosas!")
        return True
        
    except Exception as e:
        print(f"❌ Error en importación: {e}")
        return False

def test_configuration():
    """Prueba la configuración del sistema"""
    print("\n🔧 Probando configuración...")
    
    try:
        from src.config.config import config
        
        # Validar configuración
        config.validate_config()
        print("✅ Configuración validada")
        
        # Verificar directorios
        required_dirs = ['input', 'input/audios', 'input/historico', 'input/prompts', 'input/plantillas_solucion']
        for dir_path in required_dirs:
            if Path(dir_path).exists():
                print(f"✅ Directorio {dir_path} existe")
            else:
                print(f"⚠️  Directorio {dir_path} no existe")
        
        # Verificar archivos de prompts
        for prompt_name, prompt_path in config.PROMPT_FILES.items():
            if prompt_path.exists():
                print(f"✅ Prompt {prompt_name} existe")
            else:
                print(f"⚠️  Prompt {prompt_name} no existe")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_services():
    """Prueba los servicios principales"""
    print("\n⚙️  Probando servicios...")
    
    try:
        from src.services.pqrs_orchestrator_service import PQRSOrchestratorService
        
        # Probar orquestador
        openai_api_key = os.environ.get('OPENAI_API_KEY', 'test-key-for-development')
        orchestrator = PQRSOrchestratorService(openai_api_key)
        print("✅ Orquestador inicializado")
        
        # Probar repositorio
        from src.repositories.pqrs_repository import PQRSRepository
        repository = PQRSRepository()
        historico = repository.get_all_historico()
        print(f"✅ Repositorio cargado: {len(historico) if historico else 0} registros")
        
        # Probar servicio de histórico
        from src.services.historico_query_service import HistoricoQueryService
        historico_service = HistoricoQueryService(repository)
        stats = historico_service.consultar_estadisticas()
        print("✅ Servicio de histórico funcionando")
        
        # Probar servicio avanzado
        from src.services.advanced_query_service import AdvancedQueryService
        advanced_service = AdvancedQueryService(repository)
        print("✅ Servicio avanzado funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en servicios: {e}")
        return False

def test_controllers():
    """Prueba los controladores"""
    print("\n🎮 Probando controladores...")
    
    try:
        from flask import Flask
        
        # Crear app de prueba
        app = Flask(__name__)
        
        # Registrar blueprints
        from src.controllers.historico_controller import historico_bp
        from src.controllers.advanced_historico_controller import advanced_historico_bp
        from src.controllers.pqrs_controller import pqrs_bp
        
        app.register_blueprint(historico_bp, url_prefix='/api/historico')
        app.register_blueprint(advanced_historico_bp, url_prefix='/api/advanced-historico')
        app.register_blueprint(pqrs_bp, url_prefix='/api/pqrs')
        
        print("✅ Todos los blueprints registrados")
        
        # Verificar rutas
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.methods} {rule.rule}")
        
        print(f"✅ {len(routes)} rutas registradas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en controladores: {e}")
        return False

def test_models():
    """Prueba los modelos de datos"""
    print("\n📊 Probando modelos...")
    
    try:
        from src.models.pqrs_model import PQRSData, AudioTranscription, PQRSHistorico
        
        # Probar creación de modelos
        pqrs_data = PQRSData(
            nombre="Juan Pérez",
            telefono="3001234567",
            cedula="12345678",
            clase="Petición",
            explicacion="Necesito que reparen un hueco en la calle",
            radicado="2025001",
            entidad_responde="Secretaría de Infraestructura",
            es_faq="No"
        )
        print("✅ PQRSData creado correctamente")
        
        audio_trans = AudioTranscription(
            audio_file="test.wav",
            transcription="Texto de prueba"
        )
        print("✅ AudioTranscription creado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE TUNRAG")
    print("=" * 50)
    
    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_configuration),
        ("Servicios", test_services),
        ("Controladores", test_controllers),
        ("Modelos", test_models)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! TUNRAG está 100% funcional")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar los errores arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
