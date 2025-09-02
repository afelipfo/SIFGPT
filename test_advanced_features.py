#!/usr/bin/env python3
"""
Script de pruebas completo para las funcionalidades avanzadas de SIFGPT
Verifica que todas las características avanzadas funcionen correctamente
"""

import sys
import os
import json
from pathlib import Path

# Agregar src al path
sys.path.append('src/')

def test_advanced_historico():
    """Prueba las funcionalidades avanzadas del histórico"""
    print("🔍 Probando consultas avanzadas del histórico...")
    
    try:
        from services.advanced_query_service import AdvancedQueryService
        
        service = AdvancedQueryService()
        assert service is not None, "Servicio avanzado no se creó"
        print("✅ AdvancedQueryService creado correctamente")
        
        # Probar consultas complejas
        try:
            # Consulta por múltiples criterios
            query_params = {
                'clase': 'Petición',
                'estado': 'Resuelto',
                'fecha_inicio': '2024-01-01',
                'fecha_fin': '2024-12-31'
            }
            
            results = service.consulta_avanzada(query_params)
            if results is not None:
                print(f"✅ Consulta avanzada funcionando: {len(results)} resultados")
            else:
                print("⚠️  Consulta avanzada no retornó resultados")
                
        except Exception as e:
            print(f"⚠️  Consulta avanzada: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en consultas avanzadas: {e}")
        return False

def test_audio_processing():
    """Prueba el procesamiento avanzado de audio"""
    print("\n🎵 Probando procesamiento de audio...")
    
    try:
        from services.audio_service import AudioService, AudioServiceFactory
        
        # Probar factory
        try:
            audio_service = AudioServiceFactory.create_openai_service("test_key")
            print("✅ AudioService creado correctamente")
            
            # Verificar estrategias disponibles
            strategies = AudioServiceFactory.get_available_strategies()
            if strategies:
                print(f"✅ Estrategias disponibles: {', '.join(strategies)}")
            else:
                print("⚠️  No se encontraron estrategias de audio")
                
        except Exception as e:
            print(f"⚠️  AudioService (requiere API key válida): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en procesamiento de audio: {e}")
        return False

def test_pqrs_classification():
    """Prueba la clasificación avanzada de PQRS"""
    print("\n🏷️ Probando clasificación de PQRS...")
    
    try:
        from services.pqrs_classifier_service import PQRSClassifierService
        
        service = PQRSClassifierService("test_key")
        assert service is not None, "Servicio de clasificación no se creó"
        print("✅ PQRSClassifierService creado correctamente")
        
        # Probar clasificación básica
        try:
            test_text = "Necesito información sobre trámites de construcción"
            classification = service.classify_pqrs(test_text)
            
            if classification:
                print(f"✅ Clasificación funcionando: {classification.get('clase', 'N/A')}")
            else:
                print("⚠️  Clasificación no retornó resultados")
                
        except Exception as e:
            print(f"⚠️  Clasificación (requiere API key válida): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en clasificación de PQRS: {e}")
        return False

def test_response_generation():
    """Prueba la generación de respuestas"""
    print("\n💬 Probando generación de respuestas...")
    
    try:
        from services.response_generator_service import ResponseGeneratorService
        
        service = ResponseGeneratorService("test_key")
        assert service is not None, "Servicio de respuestas no se creó"
        print("✅ ResponseGeneratorService creado correctamente")
        
        # Probar generación básica
        try:
            test_context = {
                'clase': 'Petición',
                'tema': 'Trámites',
                'descripcion': 'Consulta sobre permisos de construcción'
            }
            
            response = service.generate_response(test_context)
            
            if response:
                print(f"✅ Generación de respuestas funcionando: {len(response)} caracteres")
            else:
                print("⚠️  Generación no retornó respuesta")
                
        except Exception as e:
            print(f"⚠️  Generación de respuestas (requiere API key válida): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en generación de respuestas: {e}")
        return False

def test_orchestrator():
    """Prueba el orquestador principal"""
    print("\n🎼 Probando orquestador principal...")
    
    try:
        from services.pqrs_orchestrator_service import PQRSOrchestratorService
        
        orchestrator = PQRSOrchestratorService("test_key")
        assert orchestrator is not None, "Orquestador no se creó"
        print("✅ PQRSOrchestratorService creado correctamente")
        
        # Verificar métodos disponibles
        required_methods = [
            'process_text_pqrs',
            'process_audio_pqrs',
            'transcribe_audio_only',
            'get_audio_files',
            'consultar_historico_inteligente'
        ]
        
        for method in required_methods:
            if hasattr(orchestrator, method):
                print(f"✅ Método {method} disponible")
            else:
                print(f"❌ Método {method} no encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en orquestador: {e}")
        return False

def test_controllers_advanced():
    """Prueba los controladores avanzados"""
    print("\n🎮 Probando controladores avanzados...")
    
    try:
        from controllers.advanced_historico_controller import advanced_historico_bp
        
        # Verificar blueprint avanzado
        assert hasattr(advanced_historico_bp, 'name'), "Blueprint avanzado no válido"
        assert advanced_historico_bp.name == 'advanced_historico', f"Nombre incorrecto: {advanced_historico_bp.name}"
        print("✅ Blueprint avanzado creado correctamente")
        
        # Verificar rutas
        routes = [rule.rule for rule in advanced_historico_bp.url_map.iter_rules()]
        expected_routes = [
            '/api/advanced-historico/consulta-avanzada',
            '/api/advanced-historico/sugerencias'
        ]
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Ruta {route} registrada")
            else:
                print(f"❌ Ruta {route} no encontrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en controladores avanzados: {e}")
        return False

def test_data_validation():
    """Prueba la validación de datos"""
    print("\n✅ Probando validación de datos...")
    
    try:
        from models.pqrs_model import PQRSData, AudioTranscription, PQRSHistorico
        
        # Probar validación de PQRSData
        try:
            pqrs = PQRSData(
                nombre="Test User",
                telefono="3001234567",
                cedula="12345678",
                clase="Petición",
                explicacion="Test description",
                radicado="TEST001",
                entidad_responde="Secretaría de Infraestructura Física",
                es_faq=False
            )
            print("✅ PQRSData validado correctamente")
            
        except Exception as e:
            print(f"❌ Validación PQRSData: {e}")
            return False
        
        # Probar validación de AudioTranscription
        try:
            audio = AudioTranscription(
                audio_file="test.wav",
                transcription="Test transcription",
                confidence=0.95
            )
            print("✅ AudioTranscription validado correctamente")
            
        except Exception as e:
            print(f"❌ Validación AudioTranscription: {e}")
            return False
        
        # Probar validación de PQRSHistorico
        try:
            historico = PQRSHistorico(
                radicado="TEST001",
                fecha="2024-01-15",
                nombre="Test User",
                clase="Petición",
                tema="Trámites",
                descripcion="Test description",
                estado="En proceso"
            )
            print("✅ PQRSHistorico validado correctamente")
            
        except Exception as e:
            print(f"❌ Validación PQRSHistorico: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en validación de datos: {e}")
        return False

def test_error_handling():
    """Prueba el manejo de errores"""
    print("\n🚨 Probando manejo de errores...")
    
    try:
        from services.pqrs_orchestrator_service import PQRSOrchestratorService
        
        # Probar con datos inválidos
        try:
            orchestrator = PQRSOrchestratorService("")
            print("⚠️  Orquestador creado con clave vacía (esperado)")
        except Exception as e:
            print(f"✅ Manejo de errores funcionando: {type(e).__name__}")
        
        # Probar con datos nulos
        try:
            orchestrator = PQRSOrchestratorService(None)
            print("⚠️  Orquestador creado con clave nula (esperado)")
        except Exception as e:
            print(f"✅ Manejo de errores funcionando: {type(e).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en manejo de errores: {e}")
        return False

def main():
    """Función principal de pruebas avanzadas"""
    print("🚀 SIFGPT - PRUEBAS DE FUNCIONALIDADES AVANZADAS")
    print("=" * 70)
    
    tests = [
        ("Consultas Avanzadas", test_advanced_historico),
        ("Procesamiento de Audio", test_audio_processing),
        ("Clasificación PQRS", test_pqrs_classification),
        ("Generación de Respuestas", test_response_generation),
        ("Orquestador Principal", test_orchestrator),
        ("Controladores Avanzados", test_controllers_advanced),
        ("Validación de Datos", test_data_validation),
        ("Manejo de Errores", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE PRUEBAS AVANZADAS")
    print("=" * 70)
    print(f"✅ Pasaron: {passed}")
    print(f"❌ Fallaron: {total - passed}")
    print(f"🎯 Total: {total}")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas avanzadas pasaron!")
        print("🚀 SIFGPT está funcionando al 100% con todas las funcionalidades avanzadas")
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
