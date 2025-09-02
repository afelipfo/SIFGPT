#!/usr/bin/env python3
"""
Script de pruebas básicas para TUNRAG
Verifica que las funcionalidades principales estén funcionando.
"""

import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.append('src/')

def test_imports():
    """Prueba las importaciones básicas"""
    print("🔍 Probando importaciones...")
    
    try:
        from src.config.config import config
        print("✅ Configuración importada")
        
        from src.utils.logger import logger
        print("✅ Logger importado")
        
        from src.models.pqrs_model import PQRSData, AudioTranscription
        print("✅ Modelos importados")
        
        from src.services.audio_service import AudioService
        print("✅ Servicios importados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_configuration():
    """Prueba la configuración del sistema"""
    print("\n🔍 Probando configuración...")
    
    try:
        from src.config.config import config
        
        # Verificar configuración básica
        assert config.APP_NAME == "TUNRAG - Sistema de PQRS"
        assert config.BASE_DIR.exists()
        assert config.INPUT_DIR.exists()
        
        print("✅ Configuración básica válida")
        
        # Verificar archivos de prompts
        for prompt_name, prompt_path in config.PROMPT_FILES.items():
            if prompt_path.exists():
                print(f"✅ Prompt '{prompt_name}' encontrado")
            else:
                print(f"⚠️  Prompt '{prompt_name}' no encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_models():
    """Prueba los modelos de datos"""
    print("\n🔍 Probando modelos...")
    
    try:
        from src.models.pqrs_model import PQRSData, AudioTranscription
        from datetime import datetime
        
        # Probar PQRSData
        pqrs = PQRSData(
            nombre="Juan Pérez",
            telefono="3001234567",
            cedula="12345678",
            clase="Petición",
            explicacion="Solicito información",
            radicado="2024-001",
            entidad_responde="Secretaría de Infraestructura Física",
            es_faq="No"
        )
        
        assert pqrs.nombre == "Juan Pérez"
        assert pqrs.clase == "Petición"
        print("✅ Modelo PQRSData funcionando")
        
        # Probar AudioTranscription
        audio = AudioTranscription(
            audio_file="test.wav",
            transcription="Texto de prueba"
        )
        
        assert audio.audio_file == "test.wav"
        assert audio.transcription == "Texto de prueba"
        assert audio.timestamp is not None
        print("✅ Modelo AudioTranscription funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False

def test_logger():
    """Prueba el sistema de logging"""
    print("\n🔍 Probando logger...")
    
    try:
        from src.utils.logger import logger
        
        # Probar diferentes niveles de log
        logger.debug("Mensaje de debug")
        logger.info("Mensaje de info")
        logger.warning("Mensaje de warning")
        logger.error("Mensaje de error")
        
        print("✅ Logger funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en logger: {e}")
        return False

def test_repositories():
    """Prueba los repositorios"""
    print("\n🔍 Probando repositorios...")
    
    try:
        from src.repositories.pqrs_repository import PQRSRepository, PromptRepository
        
        # Probar repositorio de prompts
        prompt_repo = PromptRepository()
        
        # Intentar obtener un prompt
        try:
            sys_prompt = prompt_repo.get_prompt('sys_prompt')
            print("✅ Repositorio de prompts funcionando")
        except Exception as e:
            print(f"⚠️  Repositorio de prompts: {e}")
        
        # Probar repositorio de PQRS
        pqrs_repo = PQRSRepository()
        
        # Intentar cargar datos históricos
        try:
            historico = pqrs_repo.get_all_historico()
            print(f"✅ Repositorio de PQRS funcionando - {len(historico)} registros")
        except Exception as e:
            print(f"⚠️  Repositorio de PQRS: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en repositorios: {e}")
        return False

def test_services():
    """Prueba los servicios básicos"""
    print("\n🔍 Probando servicios...")
    
    try:
        from src.services.pqrs_classifier_service import PQRSClassifierService
        from src.services.response_generator_service import ResponseGeneratorService
        
        print("✅ Servicios importados correctamente")
        
        # Nota: No podemos probar los servicios completos sin API key
        # pero podemos verificar que se importen correctamente
        
        return True
        
    except Exception as e:
        print(f"❌ Error en servicios: {e}")
        return False

def test_file_structure():
    """Prueba la estructura de archivos"""
    print("\n🔍 Probando estructura de archivos...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'src/__init__.py',
        'src/config/__init__.py',
        'src/controllers/__init__.py',
        'src/models/__init__.py',
        'src/repositories/__init__.py',
        'src/services/__init__.py',
        'src/utils/__init__.py',
        'templates/index.html',
        'static/js/script.js',
        'static/css/styles.css'
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Archivos faltantes: {len(missing_files)}")
        return False
    
    print("✅ Estructura de archivos completa")
    return True

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🧪 TUNRAG - Pruebas Básicas del Sistema")
    print("=" * 60)
    
    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_configuration),
        ("Modelos", test_models),
        ("Logger", test_logger),
        ("Repositorios", test_repositories),
        ("Servicios", test_services),
        ("Estructura de archivos", test_file_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en prueba '{test_name}': {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Resultado: {success_count}/{total_count} pruebas pasaron")
    
    if success_count == total_count:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
    else:
        print(f"\n⚠️  {total_count - success_count} pruebas fallaron.")
        print("   Revisa los errores anteriores y corrige los problemas.")
    
    return success_count == total_count

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
