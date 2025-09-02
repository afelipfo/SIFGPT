#!/usr/bin/env python3
"""
Script de pruebas básicas para SIFGPT
Verifica la funcionalidad básica del sistema
"""

import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.append('src/')

def test_config():
    """Prueba la configuración básica"""
    print("🔧 Probando configuración...")
    
    try:
        from config.config import config
        
        # Verificar que la configuración se cargue
        assert config is not None, "Configuración no se cargó"
        print("✅ Configuración cargada correctamente")
        
        # Verificar variables básicas
        assert hasattr(config, 'APP_NAME'), "APP_NAME no encontrado"
        assert config.APP_NAME == "SIFGPT - Sistema de PQRS", f"APP_NAME incorrecto: {config.APP_NAME}"
        print("✅ APP_NAME configurado correctamente")
        
        # Verificar directorios
        assert hasattr(config, 'INPUT_DIR'), "INPUT_DIR no encontrado"
        assert Path(config.INPUT_DIR).exists(), f"Directorio {config.INPUT_DIR} no existe"
        print("✅ Directorio de entrada verificado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
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
        logger.info("Test de logger desde test_basic.py")
        print("✅ Logging funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en logger: {e}")
        return False

def test_models():
    """Prueba los modelos básicos"""
    print("\n📊 Probando modelos...")
    
    try:
        from models.pqrs_model import PQRSData, AudioTranscription
        
        # Probar PQRSData
        pqrs = PQRSData(
            nombre="Test User",
            telefono="3001234567",
            cedula="12345678",
            clase="Petición",
            explicacion="Test description",
            radicado="TEST001",
            entidad_responde="Test Entity",
            es_faq=False
        )
        
        assert pqrs.nombre == "Test User", "Nombre incorrecto"
        assert pqrs.radicado == "TEST001", "Radicado incorrecto"
        print("✅ PQRSData funcionando correctamente")
        
        # Probar AudioTranscription
        audio = AudioTranscription(
            audio_file="test.wav",
            transcription="Test transcription",
            confidence=0.95
        )
        
        assert audio.transcription == "Test transcription", "Transcripción incorrecta"
        print("✅ AudioTranscription funcionando correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False

def test_repository():
    """Prueba el repositorio básico"""
    print("\n💾 Probando repositorio...")
    
    try:
        from repositories.pqrs_repository import PQRSRepository
        
        repo = PQRSRepository()
        assert repo is not None, "Repositorio no se creó"
        print("✅ Repositorio creado correctamente")
        
        # Probar carga de datos
        try:
            data = repo.load_historico_data()
            if data is not None:
                print(f"✅ Datos cargados: {len(data)} registros")
            else:
                print("⚠️  No se pudieron cargar datos")
        except Exception as e:
            print(f"⚠️  Carga de datos: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en repositorio: {e}")
        return False

def test_services():
    """Prueba los servicios básicos"""
    print("\n⚙️ Probando servicios...")
    
    try:
        from services.pqrs_orchestrator_service import PQRSOrchestratorService
        
        # Probar creación del servicio
        orchestrator = PQRSOrchestratorService("test_key")
        assert orchestrator is not None, "Orquestador no se creó"
        print("✅ Orquestador creado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en servicios: {e}")
        return False

def test_controllers():
    """Prueba los controladores básicos"""
    print("\n🎮 Probando controladores...")
    
    try:
        from controllers.pqrs_controller import pqrs_bp
        
        # Verificar que sea un Blueprint
        assert hasattr(pqrs_bp, 'name'), "No es un Blueprint válido"
        assert pqrs_bp.name == 'pqrs', f"Nombre incorrecto: {pqrs_bp.name}"
        print("✅ Blueprint pqrs creado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en controladores: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 SIFGPT - Pruebas Básicas del Sistema")
    print("=" * 50)
    
    tests = [
        ("Configuración", test_config),
        ("Logger", test_logger),
        ("Modelos", test_models),
        ("Repositorio", test_repository),
        ("Servicios", test_services),
        ("Controladores", test_controllers)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS BÁSICAS")
    print("=" * 50)
    print(f"✅ Pasaron: {passed}")
    print(f"❌ Fallaron: {total - passed}")
    print(f"🎯 Total: {total}")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas básicas pasaron!")
        return True
    else:
        print(f"\n⚠️  {total - passed} pruebas fallaron")
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
