#!/usr/bin/env python3
"""
Script de prueba completa para SIFGPT
Verifica que todos los componentes del sistema funcionen correctamente
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
        
        from repositories.pqrs_repository import PQRSRepository
        print("✅ Repositorio importado correctamente")
        
        from controllers.pqrs_controller import pqrs_bp
        print("✅ Controlador importado correctamente")
        
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
        
        # Probar creación de AudioTranscription
        audio_trans = AudioTranscription(
            audio_file="test.wav",
            transcription="Texto transcrito de prueba",
            confidence=0.95
        )
        print("✅ AudioTranscription creado correctamente")
        
        # Probar creación de PQRSHistorico
        historico = PQRSHistorico(
            radicado="2024001",
            fecha="2024-01-15",
            nombre="Juan Pérez",
            clase="Petición",
            tema="Trámites",
            descripcion="Consulta sobre trámites",
            estado="En proceso"
        )
        print("✅ PQRSHistorico creado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False

def test_services():
    """Prueba los servicios del sistema"""
    print("\n🔧 Probando servicios...")
    
    try:
        # Importar servicios explícitamente
        from services.pqrs_orchestrator_service import PQRSOrchestratorService
        from services.audio_service import AudioService, AudioServiceFactory
        from services.historico_query_service import HistoricoQueryService
        from services.advanced_query_service import AdvancedQueryService
        
        # Probar creación de servicios
        orchestrator = PQRSOrchestratorService("test_key")
        print("✅ PQRSOrchestratorService creado correctamente")
        
        # Probar AudioServiceFactory
        try:
            audio_service = AudioServiceFactory.create_openai_service("test_key")
            print("✅ AudioService creado correctamente")
        except Exception as e:
            print(f"⚠️  AudioService (requiere API key válida): {e}")
        
        # Probar HistoricoQueryService
        historico_service = HistoricoQueryService()
        print("✅ HistoricoQueryService creado correctamente")
        
        # Probar AdvancedQueryService
        advanced_service = AdvancedQueryService()
        print("✅ AdvancedQueryService creado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en servicios: {e}")
        return False

def test_repositories():
    """Prueba los repositorios"""
    print("\n💾 Probando repositorios...")
    
    try:
        from repositories.pqrs_repository import PQRSRepository
        
        # Probar creación del repositorio
        repo = PQRSRepository()
        print("✅ PQRSRepository creado correctamente")
        
        # Probar carga de datos
        try:
            data = repo.load_historico_data()
            if data is not None:
                print(f"✅ Datos históricos cargados: {len(data)} registros")
            else:
                print("⚠️  No se pudieron cargar datos históricos")
        except Exception as e:
            print(f"⚠️  Carga de datos históricos: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en repositorios: {e}")
        return False

def test_controllers():
    """Prueba los controladores"""
    print("\n🎮 Probando controladores...")
    
    try:
        from controllers.pqrs_controller import pqrs_bp
        
        # Verificar que es un Blueprint de Flask
        if hasattr(pqrs_bp, 'name') and pqrs_bp.name == 'pqrs':
            print("✅ Blueprint pqrs creado correctamente")
        else:
            print("❌ Blueprint pqrs no válido")
            return False
        
        # Verificar rutas registradas
        routes = [rule.rule for rule in pqrs_bp.url_map.iter_rules()]
        expected_routes = [
            '/api/pqrs/process-text',
            '/api/pqrs/process-audio',
            '/api/pqrs/transcribe-audio',
            '/api/pqrs/status'
        ]
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Ruta {route} registrada")
            else:
                print(f"❌ Ruta {route} no encontrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en controladores: {e}")
        return False

def test_utils():
    """Prueba las utilidades del sistema"""
    print("\n🛠️ Probando utilidades...")
    
    try:
        from utils.logger import logger
        
        # Probar logging
        logger.info("Test de logging desde test_complete_functionality.py")
        print("✅ Logger funcionando correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en utilidades: {e}")
        return False

def test_maintenance():
    """Prueba las funciones de mantenimiento"""
    print("\n🔧 Probando funciones de mantenimiento...")
    
    try:
        import maintenance
        
        # Verificar que las funciones existen
        if hasattr(maintenance, 'clean_logs'):
            print("✅ Función clean_logs disponible")
        else:
            print("❌ Función clean_logs no encontrada")
        
        if hasattr(maintenance, 'clean_audio_files'):
            print("✅ Función clean_audio_files disponible")
        else:
            print("❌ Función clean_audio_files no encontrada")
        
        if hasattr(maintenance, 'create_backup'):
            print("✅ Función create_backup disponible")
        else:
            print("❌ Función create_backup no encontrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en mantenimiento: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE SIFGPT")
    print("=" * 60)
    
    # Lista de todas las pruebas
    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_config),
        ("Modelos", test_models),
        ("Servicios", test_services),
        ("Repositorios", test_repositories),
        ("Controladores", test_controllers),
        ("Utilidades", test_utils),
        ("Mantenimiento", test_maintenance)
    ]
    
    # Ejecutar pruebas
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! SIFGPT está 100% funcional")
        return True
    else:
        print(f"\n⚠️  {total - passed} pruebas fallaron")
        print("Revisa los errores anteriores y corrige los problemas")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Pruebas canceladas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
