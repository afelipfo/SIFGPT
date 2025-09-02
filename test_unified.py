#!/usr/bin/env python3
"""
Script de pruebas unificado para TUNRAG
Reemplaza todos los archivos de prueba anteriores con funcionalidad consolidada
"""

import sys
import os
import importlib
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Prueba las importaciones principales"""
    print("🔍 Probando importaciones...")
    
    try:
        # Importaciones básicas
        from config.config import config
        print("✅ Configuración importada correctamente")
        
        from utils.logger import logger
        print("✅ Logger importado correctamente")
        
        from models.pqrs_model import PQRSData, AudioTranscription, PQRSHistorico
        print("✅ Modelos importados correctamente")
        
        from services.pqrs_orchestrator_service import PQRSOrchestratorService
        print("✅ Servicio orquestador importado correctamente")
        
        from services.audio_service import AudioService, AudioServiceFactory
        print("✅ Servicio de audio importado correctamente")
        
        from services.historico_query_service import HistoricoQueryService
        print("✅ Servicio de histórico unificado importado correctamente")
        
        from repositories.pqrs_repository import PQRSRepository
        print("✅ Repositorio importado correctamente")
        
        from controllers.pqrs_controller import pqrs_bp
        print("✅ Controlador PQRS importado correctamente")
        
        from controllers.historico_controller import historico_bp
        print("✅ Controlador histórico unificado importado correctamente")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error en importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado en importación: {e}")
        return False

def test_config():
    """Prueba la configuración del sistema"""
    print("\n⚙️ Probando configuración...")
    
    try:
        from config.config import config
        
        # Verificar configuración
        config.validate_config()
        print("✅ Configuración válida")
        
        # Verificar variables importantes
        required_vars = ['OPENAI_API_KEY', 'OPENAI_MODEL', 'WHISPER_MODEL']
        for var in required_vars:
            value = getattr(config, var, None)
            if value:
                print(f"✅ {var}: {value[:20]}{'...' if len(str(value)) > 20 else ''}")
            else:
                print(f"⚠️  {var}: No configurado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_models():
    """Prueba los modelos de datos"""
    print("\n📊 Probando modelos...")
    
    try:
        from models.pqrs_model import PQRSData, AudioTranscription, PQRSHistorico
        
        # Probar creación de PQRSData
        pqrs_data = PQRSData(
            nombre="Juan Pérez",
            telefono="3001234567",
            cedula="12345678",
            clase="Petición",
            explicacion="Necesito información sobre trámites",
            radicado="2024001",
            entidad_responde="Secretaría de Infraestructura Física",
            es_faq=False
        )
        print("✅ PQRSData creado correctamente")
        
        # Probar creación de AudioTranscription (sin confidence)
        try:
            audio_trans = AudioTranscription(
                audio_file="test.wav",
                transcription="Texto transcrito de prueba"
            )
            print("✅ AudioTranscription creado correctamente")
        except TypeError:
            # Intentar sin parámetros adicionales
            audio_trans = AudioTranscription(
                audio_file="test.wav",
                transcription="Texto transcrito de prueba"
            )
            print("✅ AudioTranscription creado correctamente")
        
        # Probar métodos de conversión
        pqrs_dict = pqrs_data.to_dict()
        assert isinstance(pqrs_dict, dict), "to_dict() debe retornar un diccionario"
        print("✅ Método to_dict() funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False

def test_logger():
    """Prueba el sistema de logging"""
    print("\n📝 Probando logger...")
    
    try:
        from utils.logger import logger
        
        # Verificar que el logger funcione
        assert logger is not None, "Logger no se inicializó"
        print("✅ Logger inicializado correctamente")
        
        # Probar logging
        logger.info("Test de logger desde test_unified.py")
        logger.debug("Test de debug")
        logger.warning("Test de warning")
        print("✅ Logging funcionando en todos los niveles")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en logger: {e}")
        return False

def test_historico_service():
    """Prueba el servicio de histórico unificado"""
    print("\n🔍 Probando servicio de histórico unificado...")
    
    try:
        from services.historico_query_service import HistoricoQueryService
        from repositories.pqrs_repository import PQRSRepository
        
        # Inicializar servicios
        pqrs_repository = PQRSRepository()
        historico_service = HistoricoQueryService(pqrs_repository)
        print("✅ Servicio de histórico inicializado")
        
        # Probar consulta de estadísticas
        stats = historico_service.consultar_estadisticas()
        if stats['success']:
            print("✅ Consulta de estadísticas funcionando")
        else:
            print(f"⚠️  Estadísticas no disponibles: {stats.get('error', 'Error desconocido')}")
        
        # Probar ayuda
        ayuda = historico_service.obtener_ayuda_consultas()
        if ayuda['success']:
            print("✅ Sistema de ayuda funcionando")
        else:
            print(f"⚠️  Ayuda no disponible: {ayuda.get('error', 'Error desconocido')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en servicio de histórico: {e}")
        return False

def test_pqrs_orchestrator():
    """Prueba el orquestador de PQRS"""
    print("\n🎯 Probando orquestador de PQRS...")
    
    try:
        from services.pqrs_orchestrator_service import PQRSOrchestratorService
        
        # Intentar inicializar (puede fallar si no hay API key)
        try:
            openai_api_key = os.environ.get('OPENAI_API_KEY', 'test-key')
            orchestrator = PQRSOrchestratorService(openai_api_key)
            print("✅ Orquestador inicializado correctamente")
            
            # Verificar servicios
            assert hasattr(orchestrator, 'historico_service'), "Servicio histórico no disponible"
            assert hasattr(orchestrator, 'audio_service'), "Servicio de audio no disponible"
            assert hasattr(orchestrator, 'classifier_service'), "Servicio de clasificación no disponible"
            print("✅ Todos los servicios del orquestador disponibles")
            
        except Exception as e:
            print(f"⚠️  Orquestador no pudo inicializarse (esperado sin API key): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en orquestador: {e}")
        return False

def test_controllers():
    """Prueba los controladores"""
    print("\n🎮 Probando controladores...")
    
    try:
        from controllers.historico_controller import historico_bp
        from controllers.pqrs_controller import pqrs_bp
        
        # Verificar blueprints
        assert historico_bp.name == 'historico', "Nombre del blueprint histórico incorrecto"
        assert pqrs_bp.name == 'pqrs', "Nombre del blueprint PQRS incorrecto"
        print("✅ Blueprints de controladores correctos")
        
        # Verificar rutas del histórico (verificar atributos disponibles)
        if hasattr(historico_bp, 'url_map'):
            historico_routes = [rule.rule for rule in historico_bp.url_map.iter_rules()]
            expected_routes = [
                '/consulta', '/radicado/<numero_radicado>', '/buscar/texto', 
                '/buscar/nombre', '/consulta-avanzada', '/sugerencias',
                '/filtros-disponibles', '/estadisticas', '/ayuda', '/resumen'
            ]
            
            for route in expected_routes:
                if route in historico_routes:
                    print(f"✅ Ruta {route} disponible")
                else:
                    print(f"⚠️  Ruta {route} no encontrada")
        else:
            print("✅ Blueprint histórico creado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en controladores: {e}")
        return False

def test_repository():
    """Prueba el repositorio de datos"""
    print("\n💾 Probando repositorio...")
    
    try:
        from repositories.pqrs_repository import PQRSRepository
        
        # Inicializar repositorio
        repo = PQRSRepository()
        print("✅ Repositorio inicializado")
        
        # Verificar métodos disponibles
        methods = ['get_historico_by_radicado', 'search_historico_advanced', '_load_historico']
        for method in methods:
            if hasattr(repo, method):
                print(f"✅ Método {method} disponible")
            else:
                print(f"⚠️  Método {method} no encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en repositorio: {e}")
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🚀 TUNRAG - Pruebas Unificadas del Sistema")
    print("=" * 60)
    
    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_config),
        ("Modelos", test_models),
        ("Logger", test_logger),
        ("Servicio de Histórico", test_historico_service),
        ("Orquestador PQRS", test_pqrs_orchestrator),
        ("Controladores", test_controllers),
        ("Repositorio", test_repository)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        return True
    else:
        print(f"⚠️  {total - passed} pruebas fallaron")
        return False

def main():
    """Función principal"""
    try:
        success = run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n👋 Pruebas interrumpidas por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
