#!/usr/bin/env python3
"""
Servicio avanzado de consultas para el histórico de PQRS
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import re
from src.repositories.pqrs_repository import PQRSRepository
from src.models.pqrs_model import PQRSHistorico
from src.utils.logger import logger
import pandas as pd

class AdvancedQueryService:
    """Servicio avanzado de consultas con filtros personalizables"""
    
    def __init__(self, pqrs_repository: PQRSRepository):
        """Inicializa el servicio de consultas avanzadas"""
        self.pqrs_repository = pqrs_repository
        logger.info("Servicio de consultas avanzadas inicializado")
    
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
    
    def _filtrar_por_texto(self, df, texto: str):
        """Filtra por texto en múltiples columnas"""
        texto_lower = texto.lower()
        mascara = (
            df['texto_pqrs'].astype(str).str.contains(texto_lower, case=False, na=False) |
            df['datos_iniciales'].astype(str).str.contains(texto_lower, case=False, na=False) |
            df['seguimiento'].astype(str).str.contains(texto_lower, case=False, na=False) |
            df['observacion'].astype(str).str.contains(texto_lower, case=False, na=False)
        )
        return df[mascara]
    
    def _filtrar_por_radicado(self, df, radicado: str):
        """Filtra por número de radicado"""
        return df[df['numero_radicado'] == radicado]
    
    def _filtrar_por_nombre(self, df, nombre: str):
        """Filtra por nombre del solicitante"""
        nombre_lower = nombre.lower()
        mascara = (
            df['nombre'].astype(str).str.contains(nombre_lower, case=False, na=False) |
            df['primer_nombre'].astype(str).str.contains(nombre_lower, case=False, na=False) |
            df['primer_apellido'].astype(str).str.contains(nombre_lower, case=False, na=False) |
            df['nombre_completo'].astype(str).str.contains(nombre_lower, case=False, na=False)
        )
        return df[mascara]
    
    def _filtrar_por_fecha(self, df, fecha_inicio: str, fecha_fin: str = None):
        """Filtra por rango de fechas"""
        try:
            if fecha_fin is None:
                fecha_fin = fecha_inicio
            
            df_fechas = df.copy()
            df_fechas['fecha_radicacion'] = pd.to_datetime(df_fechas['fecha_radicacion'], errors='coerce')
            
            fecha_inicio_dt = pd.to_datetime(fecha_inicio)
            fecha_fin_dt = pd.to_datetime(fecha_fin)
            
            mascara = (
                (df_fechas['fecha_radicacion'] >= fecha_inicio_dt) & 
                (df_fechas['fecha_radicacion'] <= fecha_fin_dt)
            )
            return df_fechas[mascara]
        except Exception as e:
            logger.warning(f"Error al filtrar por fecha: {e}")
            return df
    
    def _filtrar_por_clasificacion(self, df, clasificacion: str):
        """Filtra por clasificación"""
        return df[df['clasificacion'].astype(str).str.contains(clasificacion, case=False, na=False)]
    
    def _filtrar_por_estado(self, df, estado: str):
        """Filtra por estado"""
        return df[df['estado_pqrs'].astype(str).str.contains(estado, case=False, na=False)]
    
    def _filtrar_por_unidad(self, df, unidad: str):
        """Filtra por unidad"""
        return df[df['unidad'].astype(str).str.contains(unidad, case=False, na=False)]
    
    def _filtrar_por_barrio(self, df, barrio: str):
        """Filtra por barrio"""
        return df[df['barrio'].astype(str).str.contains(barrio, case=False, na=False)]
    
    def _ordenar_resultados(self, df, campo: str, orden: str = 'asc'):
        """Ordena los resultados por campo específico"""
        try:
            if campo in df.columns:
                if orden.lower() == 'desc':
                    return df.sort_values(by=campo, ascending=False)
                else:
                    return df.sort_values(by=campo, ascending=True)
            return df
        except Exception as e:
            logger.warning(f"Error al ordenar por {campo}: {e}")
            return df
    
    def _generar_resumen_filtrado(self, df) -> Dict[str, Any]:
        """Genera resumen de los resultados filtrados"""
        try:
            resumen = {
                'total_registros': len(df),
                'por_clasificacion': df['clasificacion'].value_counts().to_dict() if 'clasificacion' in df.columns else {},
                'por_estado': df['estado_pqrs'].value_counts().to_dict() if 'estado_pqrs' in df.columns else {},
                'por_unidad': df['unidad'].value_counts().to_dict() if 'unidad' in df.columns else {},
                'por_barrio': df['barrio'].value_counts().to_dict() if 'barrio' in df.columns else {}
            }
            
            # Fechas extremas
            if 'fecha_radicacion' in df.columns:
                try:
                    df_fechas = df.copy()
                    df_fechas['fecha_radicacion'] = pd.to_datetime(df_fechas['fecha_radicacion'], errors='coerce')
                    resumen['fecha_mas_antigua'] = df_fechas['fecha_radicacion'].min().strftime('%Y-%m-%d') if not df_fechas['fecha_radicacion'].isna().all() else None
                    resumen['fecha_mas_reciente'] = df_fechas['fecha_radicacion'].max().strftime('%Y-%m-%d') if not df_fechas['fecha_radicacion'].isna().all() else None
                except:
                    resumen['fecha_mas_antigua'] = None
                    resumen['fecha_mas_reciente'] = None
            
            return resumen
            
        except Exception as e:
            logger.error(f"Error al generar resumen filtrado: {e}")
            return {'total_registros': len(df)}
    
    def obtener_sugerencias_busqueda(self, texto: str) -> List[str]:
        """Genera sugerencias de búsqueda basadas en el texto"""
        try:
            df = self.pqrs_repository._load_historico()
            sugerencias = []
            
            # Buscar en clasificaciones
            if 'clasificacion' in df.columns:
                clasificaciones = df['clasificacion'].dropna().unique()
                for clas in clasificaciones:
                    if texto.lower() in str(clas).lower():
                        sugerencias.append(f"Clasificación: {clas}")
            
            # Buscar en estados
            if 'estado_pqrs' in df.columns:
                estados = df['estado_pqrs'].dropna().unique()
                for estado in estados:
                    if texto.lower() in str(estado).lower():
                        sugerencias.append(f"Estado: {estado}")
            
            # Buscar en unidades
            if 'unidad' in df.columns:
                unidades = df['unidad'].dropna().unique()
                for unidad in unidades:
                    if texto.lower() in str(unidad).lower():
                        sugerencias.append(f"Unidad: {unidad}")
            
            return sugerencias[:10]  # Máximo 10 sugerencias
            
        except Exception as e:
            logger.error(f"Error al generar sugerencias: {e}")
            return []
