#!/usr/bin/env python3
"""
Controlador unificado para el histórico de PQRS
Combina funcionalidades básicas y avanzadas en un solo controlador
"""

from flask import Blueprint, request, jsonify
from src.services.historico_query_service import HistoricoQueryService
from src.repositories.pqrs_repository import PQRSRepository
from src.utils.logger import logger
import json
import pandas as pd
from datetime import datetime

# Crear blueprint para consultas históricas unificado
historico_bp = Blueprint('historico', __name__)

# Inicializar servicios
pqrs_repository = PQRSRepository()
historico_service = HistoricoQueryService(pqrs_repository)

@historico_bp.route('/consulta', methods=['POST'])
def consultar_historico():
    """Endpoint para consultas históricas unificado"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Datos no proporcionados",
                "mensaje": "Se requiere un JSON con la consulta"
            }), 400
        
        consulta = data.get('consulta', '')
        tipo_consulta = data.get('tipo_consulta', 'inteligente')
        
        if not consulta and tipo_consulta not in ['estadisticas', 'ayuda']:
            return jsonify({
                "success": False,
                "error": "Consulta requerida",
                "mensaje": "Se debe proporcionar una consulta o seleccionar un tipo válido"
            }), 400
        
        # Realizar consulta
        if tipo_consulta == 'estadisticas':
            resultado = historico_service.consultar_estadisticas()
        elif tipo_consulta == 'ayuda':
            resultado = historico_service.obtener_ayuda_consultas()
        else:
            resultado = historico_service.consulta_inteligente(consulta)
        
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error en endpoint de consulta histórica: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@historico_bp.route('/radicado/<numero_radicado>', methods=['GET'])
def consultar_por_radicado(numero_radicado):
    """Endpoint para consultar PQRS por número de radicado"""
    try:
        resultado = historico_service.consultar_por_radicado(numero_radicado)
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error al consultar por radicado {numero_radicado}: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@historico_bp.route('/buscar/texto', methods=['POST'])
def buscar_por_texto():
    """Endpoint para búsqueda por texto"""
    try:
        data = request.get_json()
        
        if not data or 'texto' not in data:
            return jsonify({
                "success": False,
                "error": "Texto de búsqueda requerido",
                "mensaje": "Se debe proporcionar el campo 'texto'"
            }), 400
        
        texto = data['texto']
        resultado = historico_service.buscar_por_texto(texto)
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error en búsqueda por texto: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@historico_bp.route('/buscar/nombre', methods=['POST'])
def buscar_por_nombre():
    """Endpoint para búsqueda por nombre"""
    try:
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({
                "success": False,
                "error": "Nombre requerido",
                "mensaje": "Se debe proporcionar el campo 'nombre'"
            }), 400
        
        nombre = data['nombre']
        resultado = historico_service.buscar_por_nombre(nombre)
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error en búsqueda por nombre: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@historico_bp.route('/consulta-avanzada', methods=['POST'])
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
        resultado = historico_service.consulta_avanzada(filtros)
        
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error en consulta avanzada: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@historico_bp.route('/sugerencias', methods=['POST'])
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
        
        sugerencias = historico_service.obtener_sugerencias_busqueda(texto)
        
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

@historico_bp.route('/filtros-disponibles', methods=['GET'])
def obtener_filtros_disponibles():
    """Endpoint para obtener información sobre filtros disponibles"""
    try:
        filtros_info = {
            "filtros_texto": {
                "texto": "Búsqueda en texto de la PQRS",
                "nombre": "Nombre del solicitante",
                "radicado": "Número de radicado"
            },
            "filtros_fecha": {
                "fecha_inicio": "Fecha de inicio (YYYY-MM-DD)",
                "fecha_fin": "Fecha de fin (YYYY-MM-DD)"
            },
            "filtros_clasificacion": {
                "clasificacion": "Tipo de PQRS (Petición, Queja, Reclamo, Sugerencia, Denuncia)",
                "estado": "Estado actual de la PQRS"
            },
            "filtros_ubicacion": {
                "unidad": "Unidad responsable de la PQRS",
                "barrio": "Barrio o sector de la PQRS"
            },
            "filtros_resultado": {
                "limit": "Límite de resultados (número)",
                "ordenar_por": "Campo para ordenar resultados",
                "orden": "Orden de resultados ('asc' o 'desc')"
            }
        }
        
        return jsonify({
            "success": True,
            "filtros_disponibles": filtros_info,
            "mensaje": "Información de filtros disponibles"
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo filtros disponibles: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@historico_bp.route('/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """Endpoint para obtener estadísticas del histórico"""
    try:
        resultado = historico_service.consultar_estadisticas()
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@historico_bp.route('/ayuda', methods=['GET'])
def obtener_ayuda():
    """Endpoint para obtener ayuda sobre el uso del servicio"""
    try:
        resultado = historico_service.obtener_ayuda_consultas()
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error obteniendo ayuda: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@historico_bp.route('/resumen', methods=['GET'])
def obtener_resumen():
    """Endpoint para obtener un resumen rápido del histórico"""
    try:
        # Obtener estadísticas básicas
        stats = historico_service.consultar_estadisticas()
        
        if stats['success']:
            datos = stats['datos']
            resumen = {
                "total_pqrs": datos.get('total_pqrs', 0),
                "clasificaciones_principales": datos.get('por_clasificacion', {}),
                "estados_principales": datos.get('por_estado', {}),
                "unidades_principales": datos.get('por_unidad', {}),
                "fecha_ultima_actualizacion": datetime.now().isoformat()
            }
            
            return jsonify({
                "success": True,
                "resumen": resumen,
                "mensaje": "Resumen del histórico generado exitosamente"
            })
        else:
            return jsonify(stats)
            
    except Exception as e:
        logger.error(f"Error obteniendo resumen: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500
