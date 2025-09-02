#!/usr/bin/env python3
"""
Script de pruebas completo para las funcionalidades avanzadas de TUNRAG
"""

import requests
import json
import time
from datetime import datetime
import sys

# Configuración
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api/advanced-historico"

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime mensaje de error"""
    print(f"❌ {message}")

def print_info(message):
    """Imprime mensaje informativo"""
    print(f"ℹ️  {message}")

def test_health_check():
    """Prueba el endpoint de salud"""
    print_header("VERIFICACIÓN DE SALUD DEL SISTEMA")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Sistema saludable - Versión: {data.get('version', 'N/A')}")
            return True
        else:
            print_error(f"Error en health check: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False

def test_dashboard_endpoint():
    """Prueba el endpoint del dashboard"""
    print_header("PRUEBA DEL ENDPOINT DASHBOARD")
    
    try:
        response = requests.get(f"{API_BASE}/dashboard")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                dashboard = data['dashboard']
                print_success("Dashboard cargado correctamente")
                print_info(f"Total PQRS: {dashboard['metricas']['total_pqrs']}")
                print_info(f"Pendientes: {dashboard['metricas']['pqrs_pendientes']}")
                print_info(f"Resueltas: {dashboard['metricas']['pqrs_resueltas']}")
                print_info(f"Este mes: {dashboard['metricas']['pqrs_este_mes']}")
                return True
            else:
                print_error(f"Error en dashboard: {data.get('error', 'Desconocido')}")
                return False
        else:
            print_error(f"Error HTTP: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False

def test_filtros_disponibles():
    """Prueba el endpoint de filtros disponibles"""
    print_header("PRUEBA DE FILTROS DISPONIBLES")
    
    try:
        response = requests.get(f"{API_BASE}/filtros-disponibles")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                filtros = data['filtros_disponibles']
                print_success("Filtros cargados correctamente")
                print_info(f"Total registros: {data['total_registros']}")
                print_info(f"Clasificaciones: {len(filtros['clasificaciones'])}")
                print_info(f"Estados: {len(filtros['estados'])}")
                print_info(f"Unidades: {len(filtros['unidades'])}")
                print_info(f"Barrios: {len(filtros['barrios'])}")
                return True
            else:
                print_error(f"Error en filtros: {data.get('error', 'Desconocido')}")
                return False
        else:
            print_error(f"Error HTTP: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False

def test_consulta_avanzada():
    """Prueba la consulta avanzada"""
    print_header("PRUEBA DE CONSULTA AVANZADA")
    
    # Prueba 1: Búsqueda por texto
    print_info("Prueba 1: Búsqueda por texto 'reparacion'")
    filtros_texto = {
        "texto": "reparacion",
        "limit": 10,
        "ordenar_por": "fecha_radicacion",
        "orden": "desc"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/consulta-avanzada",
            json=filtros_texto,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Consulta por texto exitosa - {data['total_resultados']} resultados")
                if data['datos']:
                    primer_resultado = data['datos'][0]
                    print_info(f"Primer resultado: {primer_resultado.get('numero_radicado', 'N/A')}")
                return True
            else:
                print_error(f"Error en consulta: {data.get('error', 'Desconocido')}")
                return False
        else:
            print_error(f"Error HTTP: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False

def test_sugerencias():
    """Prueba el sistema de sugerencias"""
    print_header("PRUEBA DEL SISTEMA DE SUGERENCIAS")
    
    try:
        response = requests.post(
            f"{API_BASE}/sugerencias",
            json={"texto": "repar"},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Sugerencias generadas - {data['total_sugerencias']} encontradas")
                for sugerencia in data['sugerencias'][:3]:  # Mostrar solo las primeras 3
                    print_info(f"  • {sugerencia}")
                return True
            else:
                print_error(f"Error en sugerencias: {data.get('error', 'Desconocido')}")
                return False
        else:
            print_error(f"Error HTTP: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False

def test_estadisticas_avanzadas():
    """Prueba las estadísticas avanzadas"""
    print_header("PRUEBA DE ESTADÍSTICAS AVANZADAS")
    
    try:
        response = requests.get(f"{API_BASE}/estadisticas-avanzadas")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                stats = data['estadisticas_avanzadas']
                print_success("Estadísticas cargadas correctamente")
                print_info(f"Total registros: {data['total_registros']}")
                print_info(f"Estadísticas por año: {len(stats['por_año'])} años")
                print_info(f"Estadísticas por mes: {len(stats['por_mes'])} meses")
                print_info(f"Top barrios: {len(stats['top_barrios'])} barrios")
                print_info(f"Top unidades: {len(stats['top_unidades'])} unidades")
                return True
            else:
                print_error(f"Error en estadísticas: {data.get('error', 'Desconocido')}")
                return False
        else:
            print_error(f"Error HTTP: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False

def test_exportacion():
    """Prueba el sistema de exportación"""
    print_header("PRUEBA DEL SISTEMA DE EXPORTACIÓN")
    
    # Prueba exportación JSON
    print_info("Prueba 1: Exportación a JSON")
    filtros_export = {
        "texto": "reparacion",
        "limit": 5
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/exportar",
            json={
                "filtros": filtros_export,
                "formato": "json"
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Exportación JSON exitosa - {data['total_registros']} registros")
                return True
            else:
                print_error(f"Error en exportación JSON: {data.get('error', 'Desconocido')}")
                return False
        else:
            print_error(f"Error HTTP en exportación: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión en exportación: {e}")
        return False

def test_consulta_compleja():
    """Prueba una consulta compleja con múltiples filtros"""
    print_header("PRUEBA DE CONSULTA COMPLEJA")
    
    filtros_complejos = {
        "texto": "reparacion",
        "fecha_inicio": "2024-01-01",
        "fecha_fin": "2024-12-31",
        "limit": 20,
        "ordenar_por": "nombre",
        "orden": "asc"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/consulta-avanzada",
            json=filtros_complejos,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Consulta compleja exitosa - {data['total_resultados']} resultados")
                print_info(f"Filtros aplicados: {len(data['filtros_aplicados'])} filtros")
                if data.get('resumen'):
                    resumen = data['resumen']
                    print_info(f"Resumen: {resumen['total_registros']} registros")
                return True
            else:
                print_error(f"Error en consulta compleja: {data.get('error', 'Desconocido')}")
                return False
        else:
            print_error(f"Error HTTP: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False

def test_web_interface():
    """Prueba la interfaz web"""
    print_header("PRUEBA DE INTERFAZ WEB")
    
    try:
        # Probar acceso al dashboard avanzado
        response = requests.get(f"{BASE_URL}/advanced-dashboard")
        if response.status_code == 200:
            print_success("Dashboard web accesible correctamente")
            print_info("URL: http://localhost:5000/advanced-dashboard")
            return True
        else:
            print_error(f"Error accediendo al dashboard: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión al dashboard: {e}")
        return False

def test_performance():
    """Prueba de rendimiento básica"""
    print_header("PRUEBA DE RENDIMIENTO")
    
    # Medir tiempo de respuesta del dashboard
    start_time = time.time()
    try:
        response = requests.get(f"{API_BASE}/dashboard")
        end_time = time.time()
        
        if response.status_code == 200:
            tiempo_respuesta = (end_time - start_time) * 1000  # Convertir a milisegundos
            print_success(f"Dashboard responde en {tiempo_respuesta:.2f}ms")
            
            if tiempo_respuesta < 1000:
                print_info("✅ Rendimiento EXCELENTE (< 1 segundo)")
            elif tiempo_respuesta < 3000:
                print_info("✅ Rendimiento BUENO (< 3 segundos)")
            else:
                print_info("⚠️  Rendimiento LENTO (> 3 segundos)")
            
            return True
        else:
            print_error(f"Error en prueba de rendimiento: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error en prueba de rendimiento: {e}")
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print_header("🚀 INICIANDO PRUEBAS COMPLETAS DE FUNCIONALIDADES AVANZADAS")
    print_info(f"URL Base: {BASE_URL}")
    print_info(f"API Base: {API_BASE}")
    print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Verificación de Salud", test_health_check),
        ("Dashboard Endpoint", test_dashboard_endpoint),
        ("Filtros Disponibles", test_filtros_disponibles),
        ("Consulta Avanzada", test_consulta_avanzada),
        ("Sistema de Sugerencias", test_sugerencias),
        ("Estadísticas Avanzadas", test_estadisticas_avanzadas),
        ("Sistema de Exportación", test_exportacion),
        ("Consulta Compleja", test_consulta_compleja),
        ("Interfaz Web", test_web_interface),
        ("Rendimiento", test_performance)
    ]
    
    resultados = []
    
    for nombre_test, funcion_test in tests:
        print(f"\n🔄 Ejecutando: {nombre_test}")
        try:
            resultado = funcion_test()
            resultados.append((nombre_test, resultado))
            if resultado:
                print_success(f"✅ {nombre_test} - EXITOSO")
            else:
                print_error(f"❌ {nombre_test} - FALLÓ")
        except Exception as e:
            print_error(f"❌ {nombre_test} - ERROR: {e}")
            resultados.append((nombre_test, False))
    
    # Resumen final
    print_header("📊 RESUMEN DE PRUEBAS")
    
    exitos = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    print_info(f"Total de pruebas: {total}")
    print_info(f"Exitosas: {exitos}")
    print_info(f"Fallidas: {total - exitos}")
    print_info(f"Porcentaje de éxito: {(exitos/total)*100:.1f}%")
    
    print("\n📋 DETALLE DE RESULTADOS:")
    for nombre_test, resultado in resultados:
        status = "✅ EXITOSO" if resultado else "❌ FALLÓ"
        print(f"  {status} - {nombre_test}")
    
    if exitos == total:
        print_success("\n🎉 ¡TODAS LAS PRUEBAS EXITOSAS! El sistema está funcionando perfectamente.")
    else:
        print_error(f"\n⚠️  {total - exitos} prueba(s) fallaron. Revisar logs para más detalles.")
    
    return exitos == total

def main():
    """Función principal"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
🔍 SCRIPT DE PRUEBAS AVANZADAS - TUNRAG PQRS SYSTEM

Uso:
  python test_advanced_features.py          # Ejecutar todas las pruebas
  python test_advanced_features.py --help   # Mostrar esta ayuda

Descripción:
  Este script prueba todas las funcionalidades avanzadas del sistema:
  - Sistema de consultas avanzadas
  - Dashboard web interactivo
  - API REST completa
  - Sistema de exportación
  - Métricas y estadísticas
  - Rendimiento del sistema

Requisitos:
  - La aplicación debe estar ejecutándose en http://localhost:5000
  - Todas las dependencias instaladas
  - Archivo historico2.xlsx disponible

Ejemplos:
  # Ejecutar todas las pruebas
  python test_advanced_features.py
  
  # Ver ayuda
  python test_advanced_features.py --help
        """)
        return
    
    try:
        # Verificar que la aplicación esté corriendo
        print_info("Verificando conexión con la aplicación...")
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print_error("❌ La aplicación no está ejecutándose en http://localhost:5000")
            print_info("💡 Ejecuta 'python app.py' antes de correr las pruebas")
            return False
    except requests.exceptions.ConnectionError:
        print_error("❌ No se puede conectar a http://localhost:5000")
        print_info("💡 Asegúrate de que la aplicación esté ejecutándose")
        return False
    except Exception as e:
        print_error(f"❌ Error de conexión: {e}")
        return False
    
    # Ejecutar todas las pruebas
    return run_all_tests()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
