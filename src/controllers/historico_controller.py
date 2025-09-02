from flask import Blueprint, request, jsonify
from src.services.historico_query_service import HistoricoQueryService
from src.repositories.pqrs_repository import PQRSRepository
from src.utils.logger import logger

# Crear blueprint para consultas históricas
historico_bp = Blueprint('historico', __name__)

# Inicializar servicios
pqrs_repository = PQRSRepository()
historico_service = HistoricoQueryService(pqrs_repository)

@historico_bp.route('/consulta', methods=['POST'])
def consultar_historico():
    """Endpoint para consultas históricas"""
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

@historico_bp.route('/fechas', methods=['POST'])
def consultar_por_fechas():
    """Endpoint para consulta por rango de fechas"""
    try:
        data = request.get_json()
        
        if not data or 'fecha_inicio' not in data or 'fecha_fin' not in data:
            return jsonify({
                "success": False,
                "error": "Fechas requeridas",
                "mensaje": "Se deben proporcionar 'fecha_inicio' y 'fecha_fin'"
            }), 400
        
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        resultado = historico_service.consultar_por_fechas(fecha_inicio, fecha_fin)
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error en consulta por fechas: {e}")
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
        logger.error(f"Error al obtener estadísticas: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@historico_bp.route('/ayuda', methods=['GET'])
def obtener_ayuda():
    """Endpoint para obtener ayuda sobre consultas disponibles"""
    try:
        resultado = historico_service.obtener_ayuda_consultas()
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error al obtener ayuda: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500

@historico_bp.route('/resumen', methods=['GET'])
def obtener_resumen():
    """Endpoint para obtener resumen del histórico"""
    try:
        resultado = historico_service.consultar_estadisticas()
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error al obtener resumen: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "mensaje": "Error interno del servidor"
        }), 500
