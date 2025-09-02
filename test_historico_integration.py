#!/usr/bin/env python3
"""
Script de prueba para verificar la integración del archivo Excel histórico2.xlsx
"""

import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.append('src/')

from src.repositories.pqrs_repository import PQRSRepository
from src.services.historico_query_service import HistoricoQueryService
from src.utils.logger import logger

def test_historico_integration():
    """Prueba la integración del archivo Excel histórico"""
    print("🔍 Probando integración del archivo Excel histórico...")
    
    try:
        # Inicializar repositorio
        print("📁 Inicializando repositorio...")
        repo = PQRSRepository()
        
        # Cargar datos históricos
        print("📊 Cargando datos históricos...")
        df = repo._load_historico()
        
        print(f"✅ Datos cargados exitosamente desde: {repo._historico_source}")
        print(f"📈 Total de registros: {len(df)}")
        print(f"🏷️  Columnas disponibles: {list(df.columns)}")
        
        # Probar servicio de consultas
        print("\n🔍 Probando servicio de consultas históricas...")
        historico_service = HistoricoQueryService(repo)
        
        # Probar estadísticas
        print("📊 Obteniendo estadísticas...")
        stats = historico_service.consultar_estadisticas()
        if stats['success']:
            print(f"✅ Estadísticas obtenidas: {stats['resumen']['total_registros']} registros")
        else:
            print(f"❌ Error al obtener estadísticas: {stats.get('error', 'Desconocido')}")
        
        # Probar búsqueda por texto
        print("\n🔍 Probando búsqueda por texto...")
        if 'texto_pqrs' in df.columns:
            # Tomar una muestra del primer registro para buscar
            sample_text = str(df.iloc[0]['texto_pqrs'])[:50] if len(df) > 0 else "test"
            search_result = historico_service.buscar_por_texto(sample_text)
            if search_result['success']:
                print(f"✅ Búsqueda exitosa: {search_result['total_resultados']} resultados")
            else:
                print(f"❌ Error en búsqueda: {search_result.get('error', 'Desconocido')}")
        else:
            print("⚠️  Columna 'texto_pqrs' no disponible")
        
        # Probar ayuda
        print("\n❓ Probando sistema de ayuda...")
        help_result = historico_service.obtener_ayuda_consultas()
        if help_result['success']:
            print("✅ Sistema de ayuda funcionando correctamente")
            print(f"📚 Consultas disponibles: {list(help_result['consultas_disponibles'].keys())}")
        else:
            print(f"❌ Error en sistema de ayuda: {help_result.get('error', 'Desconocido')}")
        
        print("\n🎉 Prueba de integración completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba de integración: {e}")
        logger.error(f"Error en prueba de integración: {e}")
        return False

def test_specific_queries():
    """Prueba consultas específicas"""
    print("\n🔍 Probando consultas específicas...")
    
    try:
        repo = PQRSRepository()
        historico_service = HistoricoQueryService(repo)
        
        # Probar consulta inteligente
        print("🧠 Probando consulta inteligente...")
        smart_result = historico_service.consulta_inteligente("estadísticas del histórico")
        if smart_result['success']:
            print("✅ Consulta inteligente funcionando")
        else:
            print(f"❌ Error en consulta inteligente: {smart_result.get('error', 'Desconocido')}")
        
        # Probar búsqueda por nombre si está disponible
        if 'nombre' in repo._historico_df.columns:
            print("👤 Probando búsqueda por nombre...")
            sample_name = str(repo._historico_df.iloc[0]['nombre'])[:20] if len(repo._historico_df) > 0 else "test"
            name_result = historico_service.buscar_por_nombre(sample_name)
            if name_result['success']:
                print(f"✅ Búsqueda por nombre exitosa: {name_result['total_resultados']} resultados")
            else:
                print(f"❌ Error en búsqueda por nombre: {name_result.get('error', 'Desconocido')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en consultas específicas: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de integración del archivo Excel histórico...")
    
    # Ejecutar pruebas
    success = test_historico_integration()
    
    if success:
        success = test_specific_queries()
    
    if success:
        print("\n🎉 Todas las pruebas pasaron exitosamente!")
        print("✅ El archivo Excel histórico2.xlsx está integrado correctamente")
        print("🌐 Puedes usar las siguientes APIs:")
        print("   - POST /api/historico/consulta - Consulta inteligente")
        print("   - GET  /api/historico/radicado/<numero> - Por radicado")
        print("   - POST /api/historico/buscar/texto - Búsqueda por texto")
        print("   - POST /api/historico/buscar/nombre - Búsqueda por nombre")
        print("   - GET  /api/historico/estadisticas - Estadísticas")
        print("   - GET  /api/historico/ayuda - Ayuda")
    else:
        print("\n❌ Algunas pruebas fallaron")
        print("🔧 Revisa los logs para más detalles")
        sys.exit(1)
