from typing import List, Dict, Any, Optional
from src.repositories.pqrs_repository import PQRSRepository
from src.models.pqrs_model import PQRSHistorico
from src.utils.logger import logger

class HistoricoQueryService:
    """Servicio especializado en consultas del histórico de PQRS"""
    
    def __init__(self, pqrs_repository: PQRSRepository):
        """Inicializa el servicio de consultas históricas"""
        self.pqrs_repository = pqrs_repository
        logger.info("Servicio de consultas históricas inicializado")
    
    def consultar_por_radicado(self, numero_radicado: str) -> Dict[str, Any]:
        """Consulta información de una PQRS por número de radicado"""
        try:
            historico = self.pqrs_repository.get_historico_by_radicado(numero_radicado)
            
            if historico:
                return {
                    "success": True,
                    "tipo_consulta": "por_radicado",
                    "datos": historico.to_dict(),
                    "mensaje": f"Se encontró la PQRS con radicado {numero_radicado}"
                }
            else:
                return {
                    "success": False,
                    "tipo_consulta": "por_radicado",
                    "datos": None,
                    "mensaje": f"No se encontró ninguna PQRS con el radicado {numero_radicado}"
                }
                
        except Exception as e:
            logger.error(f"Error al consultar por radicado {numero_radicado}: {e}")
            return {
                "success": False,
                "tipo_consulta": "por_radicado",
                "error": str(e),
                "mensaje": "Error al realizar la consulta"
            }
    
    def buscar_por_texto(self, texto_busqueda: str) -> Dict[str, Any]:
        """Busca PQRS en el histórico por texto de búsqueda"""
        try:
            resultados = self.pqrs_repository.search_historico_advanced(texto_busqueda, 'texto')
            
            if resultados:
                return {
                    "success": True,
                    "tipo_consulta": "busqueda_texto",
                    "total_resultados": len(resultados),
                    "datos": [h.to_dict() for h in resultados],
                    "mensaje": f"Se encontraron {len(resultados)} PQRS que coinciden con la búsqueda"
                }
            else:
                return {
                    "success": False,
                    "tipo_consulta": "busqueda_texto",
                    "total_resultados": 0,
                    "datos": [],
                    "mensaje": f"No se encontraron PQRS que coincidan con: '{texto_busqueda}'"
                }
                
        except Exception as e:
            logger.error(f"Error al buscar por texto '{texto_busqueda}': {e}")
            return {
                "success": False,
                "tipo_consulta": "busqueda_texto",
                "error": str(e),
                "mensaje": "Error al realizar la búsqueda"
            }
    
    def buscar_por_nombre(self, nombre: str) -> Dict[str, Any]:
        """Busca PQRS en el histórico por nombre del solicitante"""
        try:
            resultados = self.pqrs_repository.search_historico_advanced(nombre, 'nombre')
            
            if resultados:
                return {
                    "success": True,
                    "tipo_consulta": "busqueda_nombre",
                    "total_resultados": len(resultados),
                    "datos": [h.to_dict() for h in resultados],
                    "mensaje": f"Se encontraron {len(resultados)} PQRS para el nombre '{nombre}'"
                }
            else:
                return {
                    "success": False,
                    "tipo_consulta": "busqueda_nombre",
                    "total_resultados": 0,
                    "datos": [],
                    "mensaje": f"No se encontraron PQRS para el nombre '{nombre}'"
                }
                
        except Exception as e:
            logger.error(f"Error al buscar por nombre '{nombre}': {e}")
            return {
                "success": False,
                "tipo_consulta": "busqueda_nombre",
                "error": str(e),
                "mensaje": "Error al realizar la búsqueda"
            }
    
    def consultar_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales del histórico"""
        try:
            summary = self.pqrs_repository.get_historico_summary()
            stats = self.pqrs_repository.get_estadisticas()
            
            # Combinar información
            resultado = {
                "success": True,
                "tipo_consulta": "estadisticas",
                "resumen": summary,
                "estadisticas": stats,
                "mensaje": "Estadísticas del histórico obtenidas exitosamente"
            }
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {e}")
            return {
                "success": False,
                "tipo_consulta": "estadisticas",
                "error": str(e),
                "mensaje": "Error al obtener estadísticas"
            }
    
    def consultar_por_fechas(self, fecha_inicio: str, fecha_fin: str) -> Dict[str, Any]:
        """Consulta PQRS en un rango de fechas"""
        try:
            resultados = self.pqrs_repository.get_historico_by_date_range(fecha_inicio, fecha_fin)
            
            if resultados:
                return {
                    "success": True,
                    "tipo_consulta": "por_fechas",
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin,
                    "total_resultados": len(resultados),
                    "datos": [h.to_dict() for h in resultados],
                    "mensaje": f"Se encontraron {len(resultados)} PQRS entre {fecha_inicio} y {fecha_fin}"
                }
            else:
                return {
                    "success": False,
                    "tipo_consulta": "por_fechas",
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin,
                    "total_resultados": 0,
                    "datos": [],
                    "mensaje": f"No se encontraron PQRS entre {fecha_inicio} y {fecha_fin}"
                }
                
        except Exception as e:
            logger.error(f"Error al consultar por fechas {fecha_inicio}-{fecha_fin}: {e}")
            return {
                "success": False,
                "tipo_consulta": "por_fechas",
                "error": str(e),
                "mensaje": "Error al realizar la consulta por fechas"
            }
    
    def consulta_inteligente(self, consulta_usuario: str) -> Dict[str, Any]:
        """Realiza una consulta inteligente basada en el texto del usuario"""
        try:
            consulta_lower = consulta_usuario.lower()
            
            # Detectar tipo de consulta
            if any(palabra in consulta_lower for palabra in ['radicado', 'número', 'numero', 'código', 'codigo']):
                # Buscar número de radicado
                import re
                numeros = re.findall(r'\d+', consulta_usuario)
                if numeros:
                    return self.consultar_por_radicado(numeros[0])
                else:
                    return {
                        "success": False,
                        "tipo_consulta": "inteligente",
                        "mensaje": "Por favor, proporciona el número de radicado que deseas consultar"
                    }
            
            elif any(palabra in consulta_lower for palabra in ['estadísticas', 'estadisticas', 'resumen', 'total', 'cantidad']):
                return self.consultar_estadisticas()
            
            elif any(palabra in consulta_lower for palabra in ['fecha', 'periodo', 'desde', 'hasta']):
                # Intentar extraer fechas
                import re
                fechas = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', consulta_usuario)
                if len(fechas) >= 2:
                    return self.consultar_por_fechas(fechas[0], fechas[1])
                else:
                    return {
                        "success": False,
                        "tipo_consulta": "inteligente",
                        "mensaje": "Por favor, especifica el rango de fechas (formato: DD/MM/YYYY)"
                    }
            
            else:
                # Búsqueda por texto general
                return self.buscar_por_texto(consulta_usuario)
                
        except Exception as e:
            logger.error(f"Error en consulta inteligente: {e}")
            return {
                "success": False,
                "tipo_consulta": "inteligente",
                "error": str(e),
                "mensaje": "Error al procesar la consulta inteligente"
            }
    
    def obtener_ayuda_consultas(self) -> Dict[str, Any]:
        """Proporciona ayuda sobre los tipos de consultas disponibles"""
        return {
            "success": True,
            "tipo_consulta": "ayuda",
            "consultas_disponibles": {
                "por_radicado": "Consulta una PQRS específica por número de radicado",
                "por_texto": "Busca PQRS que contengan ciertas palabras en su descripción",
                "por_nombre": "Busca PQRS por nombre del solicitante",
                "por_fechas": "Consulta PQRS en un rango de fechas específico",
                "estadisticas": "Obtiene estadísticas generales del histórico",
                "inteligente": "Análisis automático del tipo de consulta basado en el texto"
            },
            "ejemplos": {
                "por_radicado": "Consulta el radicado 2024-001",
                "por_texto": "Busca PQRS sobre educación",
                "por_nombre": "Busca PQRS de Juan Pérez",
                "por_fechas": "PQRS entre 01/01/2024 y 31/12/2024",
                "estadisticas": "Muestra estadísticas del histórico"
            },
            "mensaje": "Estas son las consultas disponibles en el sistema histórico"
        }
