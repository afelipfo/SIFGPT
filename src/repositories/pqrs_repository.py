import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict, Any
from src.models.pqrs_model import PQRSHistorico, PQRSData
from src.utils.logger import logger
from src.config.config import config

class PQRSRepository:
    """Repositorio para acceso a datos de PQRS"""
    
    def __init__(self):
        """Inicializa el repositorio"""
        self.historico_path = config.HISTORICO_CSV
        self.tabla_path = config.TABLA_CSV
        self._historico_df = None
        self._tabla_df = None
    
    def _load_historico(self) -> pd.DataFrame:
        """Carga el archivo histórico en memoria"""
        if self._historico_df is None:
            try:
                self._historico_df = pd.read_csv(self.historico_path, sep=";")
                logger.info(f"Archivo histórico cargado: {len(self._historico_df)} registros")
            except Exception as e:
                logger.error(f"Error al cargar archivo histórico: {e}")
                raise
        return self._historico_df
    
    def _load_tabla(self) -> pd.DataFrame:
        """Carga el archivo tabla en memoria"""
        if self._tabla_df is None:
            try:
                self._tabla_df = pd.read_csv(self.tabla_path, sep=";")
                logger.info(f"Archivo tabla cargado: {len(self._tabla_df)} registros")
            except Exception as e:
                logger.error(f"Error al cargar archivo tabla: {e}")
                raise
        return self._tabla_df
    
    def get_historico_by_radicado(self, numero_radicado: str) -> Optional[PQRSHistorico]:
        """Obtiene un registro histórico por número de radicado"""
        try:
            df = self._load_historico()
            if 'numero_radicado' not in df.columns:
                logger.error("Columna 'numero_radicado' no encontrada en el archivo histórico")
                return None
            
            result = df[df['numero_radicado'] == numero_radicado]
            if result.empty:
                logger.warning(f"No se encontró registro con radicado: {numero_radicado}")
                return None
            
            row = result.iloc[0]
            return PQRSHistorico.from_dict(row.to_dict())
            
        except Exception as e:
            logger.error(f"Error al buscar por radicado {numero_radicado}: {e}")
            return None
    
    def get_all_historico(self) -> List[PQRSHistorico]:
        """Obtiene todos los registros históricos"""
        try:
            df = self._load_historico()
            return [PQRSHistorico.from_dict(row.to_dict()) for _, row in df.iterrows()]
        except Exception as e:
            logger.error(f"Error al obtener todo el histórico: {e}")
            return []
    
    def search_historico(self, search_term: str, column: str = 'texto_pqrs') -> List[PQRSHistorico]:
        """Busca en el histórico por término de búsqueda"""
        try:
            df = self._load_historico()
            if column not in df.columns:
                logger.error(f"Columna '{column}' no encontrada en el archivo histórico")
                return []
            
            result = df[df[column].str.contains(search_term, case=False, na=False)]
            return [PQRSHistorico.from_dict(row.to_dict()) for _, row in result.iterrows()]
            
        except Exception as e:
            logger.error(f"Error en búsqueda de histórico: {e}")
            return []
    
    def get_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas del histórico"""
        try:
            df = self._load_historico()
            stats = {
                'total_registros': len(df),
                'por_clasificacion': df['clasificacion'].value_counts().to_dict() if 'clasificacion' in df.columns else {},
                'por_estado': df['estado_pqrs'].value_counts().to_dict() if 'estado_pqrs' in df.columns else {},
                'ultima_actualizacion': df['fecha_radicacion'].max() if 'fecha_radicacion' in df.columns else None
            }
            return stats
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {e}")
            return {}
    
    def refresh_cache(self):
        """Refresca la caché de datos"""
        self._historico_df = None
        self._tabla_df = None
        logger.info("Caché de datos refrescada")

class PromptRepository:
    """Repositorio para gestión de prompts y plantillas"""
    
    def __init__(self):
        """Inicializa el repositorio de prompts"""
        self.prompt_files = config.PROMPT_FILES
        self.plantilla_files = config.PLANTILLA_FILES
        self._prompts_cache = {}
        self._plantillas_cache = {}
    
    def get_prompt(self, prompt_name: str) -> str:
        """Obtiene un prompt específico"""
        if prompt_name not in self.prompt_files:
            raise ValueError(f"Prompt '{prompt_name}' no encontrado")
        
        if prompt_name not in self._prompts_cache:
            try:
                with open(self.prompt_files[prompt_name], 'r', encoding='utf-8') as f:
                    self._prompts_cache[prompt_name] = f.read()
                logger.debug(f"Prompt '{prompt_name}' cargado en caché")
            except Exception as e:
                logger.error(f"Error al cargar prompt '{prompt_name}': {e}")
                raise
        
        return self._prompts_cache[prompt_name]
    
    def get_plantilla(self, plantilla_name: str) -> str:
        """Obtiene una plantilla específica"""
        if plantilla_name not in self.plantilla_files:
            raise ValueError(f"Plantilla '{plantilla_name}' no encontrada")
        
        if plantilla_name not in self._plantillas_cache:
            try:
                with open(self.plantilla_files[plantilla_name], 'r', encoding='utf-8') as f:
                    self._plantillas_cache[plantilla_name] = f.read()
                logger.debug(f"Plantilla '{plantilla_name}' cargada en caché")
            except Exception as e:
                logger.error(f"Error al cargar plantilla '{plantilla_name}': {e}")
                raise
        
        return self._plantillas_cache[plantilla_name]
    
    def format_prompt(self, prompt_name: str, **kwargs) -> str:
        """Formatea un prompt con parámetros"""
        prompt = self.get_prompt(prompt_name)
        try:
            return prompt.format(**kwargs)
        except KeyError as e:
            logger.error(f"Error al formatear prompt '{prompt_name}': parámetro faltante {e}")
            raise
    
    def format_plantilla(self, plantilla_name: str, **kwargs) -> str:
        """Formatea una plantilla con parámetros"""
        plantilla = self.get_plantilla(plantilla_name)
        try:
            return plantilla.format(**kwargs)
        except KeyError as e:
            logger.error(f"Error al formatear plantilla '{plantilla_name}': parámetro faltante {e}")
            raise
    
    def refresh_cache(self):
        """Refresca la caché de prompts y plantillas"""
        self._prompts_cache.clear()
        self._plantillas_cache.clear()
        logger.info("Caché de prompts y plantillas refrescada")
