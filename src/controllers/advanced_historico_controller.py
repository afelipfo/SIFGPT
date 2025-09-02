#!/usr/bin/env python3
"""
Controlador avanzado para el histórico de PQRS
"""

from flask import Blueprint, request, jsonify
from src.services.advanced_query_service import AdvancedQueryService
from src.repositories.pqrs_repository import PQRSRepository
from src.utils.logger import logger
import json
import pandas as pd
from datetime import datetime

advanced_historico_bp = Blueprint('advanced_historico', __name__)

# Inicializar servicios
pqrs_repository = PQRSRepository()
advanced_query_service = AdvancedQueryService(pqrs_repository)

@advanced_historico_bp.route('/consulta-avanzada', methods=['POST'])
def consulta_avanzada():
    """Endpoint para consultas avanzadas con múltiples filtros"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Datos JSON requeridos",
                "mensaje": "Debe enviar un JSON con los filtros de búsqueda"
            }), 400
        
        # Validar filtros básicos
        filtros_validos = {
            'texto', 'radicado', 'nombre', 'fecha_inicio', 'fecha_fin',
            'clasificacion', 'estado', 'unidad', 'barrio', 'limit',
            'ordenar_por', 'orden'
        }
        
        filtros = {k: v for k, v in data.items() if k in filtros_validos and v}
        
        if not filtros:
            return jsonify({
                "success": False,
                "error": "Filtros requeridos",
                "mensaje": "Debe especificar al menos un filtro de búsqueda"
            }), 400
        
        # Ejecutar consulta avanzada
        resultado = advanced_query_service.consulta_avanzada(filtros)
        
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error en consulta avanzada: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@advanced_historico_bp.route('/sugerencias', methods=['POST'])
def obtener_sugerencias():
    """Endpoint para obtener sugerencias de búsqueda"""
    try:
        data = request.get_json()
        if not data or 'texto' not in data:
            return jsonify({
                "success": False,
                "error": "Texto requerido",
                "mensaje": "Debe enviar un JSON con el campo 'texto'"
            }), 400
        
        texto = data['texto']
        if len(texto) < 2:
            return jsonify({
                "success": False,
                "error": "Texto muy corto",
                "mensaje": "El texto debe tener al menos 2 caracteres"
            }), 400
        
        sugerencias = advanced_query_service.obtener_sugerencias_busqueda(texto)
        
        return jsonify({
            "success": True,
            "texto_busqueda": texto,
            "sugerencias": sugerencias,
            "total_sugerencias": len(sugerencias)
        })
        
    except Exception as e:
        logger.error(f"Error al obtener sugerencias: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@advanced_historico_bp.route('/filtros-disponibles', methods=['GET'])
def obtener_filtros_disponibles():
    """Endpoint para obtener información sobre filtros disponibles"""
    try:
        df = pqrs_repository._load_historico()
        
        filtros_info = {
            "clasificaciones": df['clasificacion'].dropna().unique().tolist() if 'clasificacion' in df.columns else [],
            "estados": df['estado_pqrs'].dropna().unique().tolist() if 'estado_pqrs' in df.columns else [],
            "unidades": df['unidad'].dropna().unique().tolist() if 'unidad' in df.columns else [],
            "barrios": df['barrio'].dropna().unique().tolist() if 'barrio' in df.columns else [],
            "campos_ordenamiento": [
                'numero_radicado', 'fecha_radicacion', 'nombre', 'clasificacion', 
                'estado_pqrs', 'unidad', 'barrio'
            ]
        }
        
        return jsonify({
            "success": True,
            "filtros_disponibles": filtros_info,
            "total_registros": len(df)
        })
        
    except Exception as e:
        logger.error(f"Error al obtener filtros disponibles: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@advanced_historico_bp.route('/estadisticas-avanzadas', methods=['GET'])
def estadisticas_avanzadas():
    """Endpoint para estadísticas avanzadas del histórico"""
    try:
        df = pqrs_repository._load_historico()
        
        # Estadísticas por período
        if 'fecha_radicacion' in df.columns:
            try:
                df_fechas = df.copy()
                df_fechas['fecha_radicacion'] = pd.to_datetime(df_fechas['fecha_radicacion'], errors='coerce')
                df_fechas['año'] = df_fechas['fecha_radicacion'].dt.year
                df_fechas['mes'] = df_fechas['fecha_radicacion'].dt.month
                
                estadisticas_por_año = df_fechas['año'].value_counts().to_dict()
                estadisticas_por_mes = df_fechas['mes'].value_counts().to_dict()
            except:
                estadisticas_por_año = {}
                estadisticas_por_mes = {}
        else:
            estadisticas_por_año = {}
            estadisticas_por_mes = {}
        
        # Estadísticas por área geográfica
        if 'barrio' in df.columns:
            top_barrios = df['barrio'].value_counts().head(20).to_dict()
        else:
            top_barrios = {}
        
        # Estadísticas por unidad
        if 'unidad' in df.columns:
            top_unidades = df['unidad'].value_counts().head(20).to_dict()
        else:
            top_unidades = {}
        
        # Tendencias temporales
        tendencias = {
            "por_año": estadisticas_por_año,
            "por_mes": estadisticas_por_mes,
            "top_barrios": top_barrios,
            "top_unidades": top_unidades
        }
        
        return jsonify({
            "success": True,
            "estadisticas_avanzadas": tendencias,
            "total_registros": len(df),
            "resumen": {
                "total_clasificaciones": len(df['clasificacion'].dropna().unique()) if 'clasificacion' in df.columns else 0,
                "total_estados": len(df['estado_pqrs'].dropna().unique()) if 'estado_pqrs' in df.columns else 0,
                "total_unidades": len(df['unidad'].dropna().unique()) if 'unidad' in df.columns else 0,
                "total_barrios": len(df['barrio'].dropna().unique()) if 'barrio' in df.columns else 0
            }
        })
        
    except Exception as e:
        logger.error(f"Error en estadísticas avanzadas: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@advanced_historico_bp.route('/exportar', methods=['POST'])
def exportar_resultados():
    """Endpoint para exportar resultados de consultas"""
    try:
        data = request.get_json()
        if not data or 'filtros' not in data:
            return jsonify({
                "success": False,
                "error": "Filtros requeridos",
                "mensaje": "Debe enviar un JSON con los filtros de exportación"
            }), 400
        
        filtros = data['filtros']
        formato = data.get('formato', 'json')  # json, csv, excel
        
        # Ejecutar consulta con los filtros
        resultado = advanced_query_service.consulta_avanzada(filtros)
        
        if not resultado['success']:
            return jsonify(resultado), 400
        
        # Preparar datos para exportación
        datos_exportar = resultado['datos']
        
        if formato == 'csv':
            # Convertir a CSV
            import csv
            import io
            
            output = io.StringIO()
            if datos_exportar:
                writer = csv.DictWriter(output, fieldnames=datos_exportar[0].keys())
                writer.writeheader()
                writer.writerows(datos_exportar)
            
            return output.getvalue(), 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': 'attachment; filename=historico_pqrs.csv'
            }
        
        elif formato == 'excel':
            # Convertir a Excel
            import pandas as pd
            import io
            
            df = pd.DataFrame(datos_exportar)
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Historico_PQRS', index=False)
            
            output.seek(0)
            
            return output.getvalue(), 200, {
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'Content-Disposition': 'attachment; filename=historico_pqrs.xlsx'
            }
        
        else:
            # Formato JSON por defecto
            return jsonify({
                "success": True,
                "formato": "json",
                "total_registros": len(datos_exportar),
                "datos": datos_exportar
            })
        
    except Exception as e:
        logger.error(f"Error en exportación: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@advanced_historico_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Endpoint para obtener datos del dashboard"""
    try:
        df = pqrs_repository._load_historico()
        
        # Métricas del dashboard
        metricas = {
            "total_pqrs": len(df),
            "pqrs_pendientes": len(df[df['estado_pqrs'].astype(str).str.contains('PENDIENTE', case=False, na=False)]) if 'estado_pqrs' in df.columns else 0,
            "pqrs_resueltas": len(df[df['estado_pqrs'].astype(str).str.contains('RESUELTA', case=False, na=False)]) if 'estado_pqrs' in df.columns else 0,
            "pqrs_este_mes": 0,
            "pqrs_este_año": 0
        }
        
        # Calcular PQRS del mes y año actual
        if 'fecha_radicacion' in df.columns:
            try:
                df_fechas = df.copy()
                df_fechas['fecha_radicacion'] = pd.to_datetime(df_fechas['fecha_radicacion'], errors='coerce')
                
                ahora = datetime.now()
                inicio_mes = ahora.replace(day=1)
                inicio_año = ahora.replace(month=1, day=1)
                
                pqrs_mes = df_fechas[
                    (df_fechas['fecha_radicacion'] >= inicio_mes) & 
                    (df_fechas['fecha_radicacion'] <= ahora)
                ]
                
                pqrs_año = df_fechas[
                    (df_fechas['fecha_radicacion'] >= inicio_año) & 
                    (df_fechas['fecha_radicacion'] <= ahora)
                ]
                
                metricas["pqrs_este_mes"] = len(pqrs_mes)
                metricas["pqrs_este_año"] = len(pqrs_año)
                
            except Exception as e:
                logger.warning(f"Error al calcular métricas temporales: {e}")
        
        return jsonify({
            "success": True,
            "dashboard": {
                "metricas": metricas,
                "ultima_actualizacion": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Error en dashboard: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500
