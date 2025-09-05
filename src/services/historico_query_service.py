#!/usr/bin/env python3
"""
Servicio unificado de consultas para el histórico de PQRS
Combina funcionalidades básicas y avanzadas en un solo servicio
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import re
import pandas as pd
from src.repositories.pqrs_repository import PQRSRepository
from src.models.pqrs_model import PQRSHistorico
from src.utils.logger import logger

class HistoricoQueryService:
    """Servicio unificado de consultas del histórico de PQRS con funcionalidades avanzadas"""
    
    def __init__(self, pqrs_repository: PQRSRepository):
        """Inicializa el servicio de consultas históricas unificado"""
        self.pqrs_repository = pqrs_repository
        # logger.info("Servicio unificado de consultas históricas inicializado")
    
    def consultar_por_radicado(self, numero_radicado: str) -> Dict[str, Any]:
        """Consulta información de una PQRS por número de radicado con información enriquecida"""
        try:
            historico = self.pqrs_repository.get_historico_by_radicado(numero_radicado)
            
            if historico:
                # Crear respuesta enriquecida con información útil
                info_util = {
                    "numero_radicado": historico.numero_radicado,
                    "solicitante": historico.nombre or historico.nombre_completo or "No especificado",
                    "asunto": historico.texto_pqrs or "No disponible",
                    "clasificacion": historico.clasificacion or "No clasificado",
                    "estado_actual": historico.estado_pqrs or "Sin estado",
                    "fecha_radicacion": str(historico.fecha_radicacion) if historico.fecha_radicacion else "No disponible",
                    "unidad_responsable": historico.unidad or "Secretaría de Infraestructura Física",
                    "barrio_sector": historico.barrio or "No especificado",
                    "tipo_solicitud": historico.tipo_solicitud or "No especificado",
                    "observaciones": historico.observacion or "Sin observaciones",
                    "seguimiento": historico.seguimiento or "Sin seguimiento registrado",
                    "telefono_contacto": historico.celular or "No disponible",
                    "correo_contacto": historico.correo or "No disponible"
                }
                
                return {
                    "success": True,
                    "tipo_consulta": "por_radicado",
                    "datos": info_util,
                    "datos_completos": historico.to_dict(),
                    "mensaje": f"PQRS encontrada - Solicitante: {info_util['solicitante']} | Estado: {info_util['estado_actual']}"
                }
            else:
                return {
                    "success": False,
                    "tipo_consulta": "por_radicado",
                    "datos": None,
                    "mensaje": f"No se encontró ninguna PQRS con el radicado {numero_radicado}. Verifica que el número sea correcto."
                }
                
        except Exception as e:
            logger.error(f"Error al consultar por radicado {numero_radicado}: {e}")
            return {
                "success": False,
                "tipo_consulta": "por_radicado",
                "error": str(e),
                "mensaje": "Error en la consulta del radicado. Intenta de nuevo o contacta soporte."
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
    
    def consulta_avanzada(self, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """
        Consulta avanzada con múltiples filtros personalizables
        
        Args:
            filtros: Diccionario con filtros como:
                - texto: str - Búsqueda en texto
                - radicado: str - Número de radicado específico
                - nombre: str - Nombre del solicitante
                - fecha_inicio: str - Fecha de inicio (YYYY-MM-DD)
                - fecha_fin: str - Fecha de fin (YYYY-MM-DD)
                - clasificacion: str - Tipo de clasificación
                - estado: str - Estado de la PQRS
                - unidad: str - Unidad responsable
                - barrio: str - Barrio o sector
                - limit: int - Límite de resultados
                - ordenar_por: str - Campo para ordenar
                - orden: str - 'asc' o 'desc'
        """
        try:
            df = self.pqrs_repository._load_historico()
            resultado = df.copy()
            
            # Aplicar filtros secuencialmente
            if 'texto' in filtros and filtros['texto']:
                resultado = self._filtrar_por_texto(resultado, filtros['texto'])
            
            if 'radicado' in filtros and filtros['radicado']:
                resultado = self._filtrar_por_radicado(resultado, filtros['radicado'])
            
            if 'nombre' in filtros and filtros['nombre']:
                resultado = self._filtrar_por_nombre(resultado, filtros['nombre'])
            
            if 'fecha_inicio' in filtros and filtros['fecha_inicio']:
                resultado = self._filtrar_por_fecha(resultado, filtros['fecha_inicio'], filtros.get('fecha_fin'))
            
            if 'clasificacion' in filtros and filtros['clasificacion']:
                resultado = self._filtrar_por_clasificacion(resultado, filtros['clasificacion'])
            
            if 'estado' in filtros and filtros['estado']:
                resultado = self._filtrar_por_estado(resultado, filtros['estado'])
            
            if 'unidad' in filtros and filtros['unidad']:
                resultado = self._filtrar_por_unidad(resultado, filtros['unidad'])
            
            if 'barrio' in filtros and filtros['barrio']:
                resultado = self._filtrar_por_barrio(resultado, filtros['barrio'])
            
            # Ordenar resultados
            if 'ordenar_por' in filtros and filtros['ordenar_por']:
                resultado = self._ordenar_resultados(resultado, filtros['ordenar_por'], filtros.get('orden', 'asc'))
            
            # Limitar resultados
            limit = filtros.get('limit', 100)
            if limit > 0:
                resultado = resultado.head(limit)
            
            # Convertir a objetos PQRSHistorico
            registros = [PQRSHistorico.from_dict(row.to_dict()) for _, row in resultado.iterrows()]
            
            return {
                "success": True,
                "total_resultados": len(registros),
                "filtros_aplicados": filtros,
                "datos": [reg.to_dict() for reg in registros],
                "resumen": self._generar_resumen_filtrado(resultado)
            }
            
        except Exception as e:
            logger.error(f"Error en consulta avanzada: {e}")
            return {
                "success": False,
                "error": str(e),
                "mensaje": "Error al procesar consulta avanzada"
            }
    
    def obtener_sugerencias_busqueda(self, texto: str) -> List[str]:
        """Obtiene sugerencias de búsqueda basadas en el texto ingresado"""
        try:
            df = self.pqrs_repository._load_historico()
            
            # Buscar en múltiples columnas
            columnas_busqueda = ['texto', 'nombre', 'clasificacion', 'unidad', 'barrio']
            sugerencias = set()
            
            for columna in columnas_busqueda:
                if columna in df.columns:
                    # Filtrar valores que contengan el texto
                    valores = df[columna].dropna().astype(str)
                    coincidencias = valores[valores.str.contains(texto, case=False, na=False)]
                    
                    # Agregar hasta 5 sugerencias por columna
                    sugerencias.update(coincidencias.head(5).tolist())
            
            # Convertir a lista y limitar resultados
            sugerencias_lista = list(sugerencias)[:20]
            logger.info(f"Sugerencias generadas para '{texto}': {len(sugerencias_lista)}")
            
            return sugerencias_lista
            
        except Exception as e:
            logger.error(f"Error generando sugerencias para '{texto}': {e}")
            return []
    
    def consultar_estadisticas(self) -> Dict[str, Any]:
        """Consulta estadísticas generales del histórico"""
        try:
            df = self.pqrs_repository._load_historico()
            
            estadisticas = {
                "total_pqrs": len(df),
                "por_clasificacion": df['clasificacion'].value_counts().to_dict(),
                "por_estado": df['estado'].value_counts().to_dict(),
                "por_unidad": df['unidad'].value_counts().head(10).to_dict(),
                "por_barrio": df['barrio'].value_counts().head(10).to_dict(),
                "fecha_mas_antigua": df['fecha_radicacion'].min() if 'fecha_radicacion' in df.columns else None,
                "fecha_mas_reciente": df['fecha_radicacion'].max() if 'fecha_radicacion' in df.columns else None
            }
            
            return {
                "success": True,
                "tipo_consulta": "estadisticas",
                "datos": estadisticas,
                "mensaje": "Estadísticas generadas exitosamente"
            }
            
        except Exception as e:
            logger.error(f"Error consultando estadísticas: {e}")
            return {
                "success": False,
                "tipo_consulta": "estadisticas",
                "error": str(e),
                "mensaje": "Error al generar estadísticas"
            }
    
    def obtener_ayuda_consultas(self) -> Dict[str, Any]:
        """Proporciona ayuda sobre cómo usar el servicio"""
        ayuda = {
            "consulta_basica": {
                "descripcion": "Consulta simple por texto, nombre o radicado",
                "ejemplo": "Buscar PQRS relacionadas con 'reparación'"
            },
            "consulta_avanzada": {
                "descripcion": "Consulta con múltiples filtros y opciones de ordenamiento",
                "filtros_disponibles": [
                    "texto", "radicado", "nombre", "fecha_inicio", "fecha_fin",
                    "clasificacion", "estado", "unidad", "barrio", "limit",
                    "ordenar_por", "orden"
                ]
            },
            "estadisticas": {
                "descripcion": "Obtener estadísticas generales del histórico"
            }
        }
        
        return {
            "success": True,
            "tipo_consulta": "ayuda",
            "datos": ayuda,
            "mensaje": "Información de ayuda disponible"
        }
    
    def consulta_inteligente(self, consulta: str) -> Dict[str, Any]:
        """Consulta inteligente que determina automáticamente el tipo de búsqueda"""
        try:
            consulta_lower = consulta.lower().strip()
            
            # Detectar tipo de consulta
            if consulta_lower in ['estadisticas', 'estadísticas', 'stats', 'resumen']:
                return self.consultar_estadisticas()
            elif consulta_lower in ['ayuda', 'help', 'como usar', 'instrucciones']:
                return self.obtener_ayuda_consultas()
            elif consulta_lower.isdigit() or consulta_lower.replace('-', '').isdigit():
                # Probablemente es un radicado
                return self.consultar_por_radicado(consulta_lower)
            elif len(consulta_lower) <= 50:
                # Probablemente es un nombre
                return self.buscar_por_nombre(consulta_lower)
            else:
                # Probablemente es una descripción o texto
                return self.buscar_por_texto(consulta_lower)
                
        except Exception as e:
            logger.error(f"Error en consulta inteligente: {e}")
            return {
                "success": False,
                "error": str(e),
                "mensaje": "Error al procesar consulta inteligente"
            }
    
    # Métodos privados para filtros avanzados
    def _filtrar_por_texto(self, df, texto: str):
        """Filtra por texto en múltiples columnas"""
        texto_lower = texto.lower()
        mascara = df.astype(str).apply(lambda x: x.str.contains(texto_lower, case=False, na=False)).any(axis=1)
        return df[mascara]
    
    def _filtrar_por_radicado(self, df, radicado: str):
        """Filtra por número de radicado"""
        return df[df['radicado'].astype(str).str.contains(radicado, case=False, na=False)]
    
    def _filtrar_por_nombre(self, df, nombre: str):
        """Filtra por nombre del solicitante"""
        return df[df['nombre'].astype(str).str.contains(nombre, case=False, na=False)]
    
    def _filtrar_por_fecha(self, df, fecha_inicio: str, fecha_fin: str = None):
        """Filtra por rango de fechas"""
        try:
            fecha_inicio = pd.to_datetime(fecha_inicio)
            if fecha_fin:
                fecha_fin = pd.to_datetime(fecha_fin)
                return df[(df['fecha_radicacion'] >= fecha_inicio) & (df['fecha_radicacion'] <= fecha_fin)]
            else:
                return df[df['fecha_radicacion'] >= fecha_inicio]
        except:
            return df
    
    def _filtrar_por_clasificacion(self, df, clasificacion: str):
        """Filtra por clasificación de PQRS"""
        return df[df['clasificacion'].astype(str).str.contains(clasificacion, case=False, na=False)]
    
    def _filtrar_por_estado(self, df, estado: str):
        """Filtra por estado de la PQRS"""
        return df[df['estado'].astype(str).str.contains(estado, case=False, na=False)]
    
    def _filtrar_por_unidad(self, df, unidad: str):
        """Filtra por unidad responsable"""
        return df[df['unidad'].astype(str).str.contains(unidad, case=False, na=False)]
    
    def _filtrar_por_barrio(self, df, barrio: str):
        """Filtra por barrio o sector"""
        return df[df['barrio'].astype(str).str.contains(barrio, case=False, na=False)]
    
    def _ordenar_resultados(self, df, campo: str, orden: str = 'asc'):
        """Ordena los resultados por un campo específico"""
        try:
            if campo in df.columns:
                if orden.lower() == 'desc':
                    return df.sort_values(by=campo, ascending=False)
                else:
                    return df.sort_values(by=campo, ascending=True)
            return df
        except:
            return df
    
    def _generar_resumen_filtrado(self, df) -> Dict[str, Any]:
        """Genera un resumen de los resultados filtrados"""
        try:
            return {
                "total_filtrado": len(df),
                "clasificaciones": df['clasificacion'].value_counts().head(5).to_dict(),
                "estados": df['estado'].value_counts().head(5).to_dict(),
                "unidades": df['unidad'].value_counts().head(5).to_dict()
            }
        except:
            return {"total_filtrado": len(df)}
