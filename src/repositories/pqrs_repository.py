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
        self.historico_excel_path = config.HISTORICO_EXCEL
        self._historico_df = None
        self._historico_source = None
    
    def _load_historico(self) -> pd.DataFrame:
        """Carga el archivo histórico en memoria desde Excel"""
        if self._historico_df is None:
            try:
                # Cargar archivo Excel
                if self.historico_excel_path.exists():
                    self._historico_df = pd.read_excel(self.historico_excel_path)
                    self._historico_source = 'excel'
                    logger.info(f"Archivo histórico Excel cargado: {len(self._historico_df)} registros")
                else:
                    logger.error("No se encontró archivo histórico Excel")
                    raise FileNotFoundError("No se encontró archivo histórico Excel")
                
                # Normalizar nombres de columnas
                self._normalize_columns()
                
            except Exception as e:
                logger.error(f"Error al cargar archivo histórico: {e}")
                raise
        return self._historico_df
    
    def _normalize_columns(self):
        """Normaliza los nombres de columnas para compatibilidad"""
        if self._historico_df is not None:
            # Mapeo de columnas específicas del archivo Excel histórico2.xlsx
            column_mapping = {
                # Mapeo para número de radicado - COLUMNA CORREGIDA
                'DOCUMENTO-CarguedeinformaciónalaplicativoPQRSDdelSIF': 'numero_radicado',
                'CONTROL DE RADICADO': 'control_radicado',  # Cambiado para evitar conflicto
                'RAD. RESPUESTA': 'rad_respuesta',  # Cambiado para evitar conflicto
                
                # Mapeo para nombre (combinar campos de nombre)
                'PRIMERNOMBRE': 'primer_nombre',
                'SEGUNDONOMBRE': 'segundo_nombre',
                'PRIMERAPELLIDO': 'primer_apellido',
                'SEGUNDOAPELLIDO': 'segundo_apellido',
                'SOLICITANTE': 'nombre_completo',
                
                # Mapeo para fechas
                'FECHA RADICACIÓN': 'fecha_radicacion',
                'FECHA ENTRADA A SIF': 'fecha_entrada_sif',
                'FECHA RADICADO RESPUESTA': 'fecha_respuesta',
                'FECHA DE INGRESO': 'fecha_ingreso',
                'FECHA DE INGRESO A LA BANDEJA': 'fecha_ingreso_bandeja',
                
                # Mapeo para texto de PQRS
                'ASUNTO DE LA PETICIÓN': 'texto_pqrs',
                'DATOS INICIALES PQRSD': 'datos_iniciales',
                'SEGUIMIENTO DE LA PQRSD': 'seguimiento',
                'OBSERVACIÓN': 'observacion',
                
                # Mapeo para clasificación
                'CLASE DE SOLICITUD': 'clasificacion',
                'TIPO DE SOLICITUD': 'tipo_solicitud',
                'TEMA': 'tema',
                
                # Mapeo para estado
                'ESTADO': 'estado_pqrs',
                'SEMAFORO DIAS': 'semaforo_dias',
                'OPORTUNIDAD': 'oportunidad',
                
                # Mapeo para información adicional
                'TIPO DOCUMENTO': 'tipo_documento',
                'NÚMERO DOCUMENTO': 'numero_documento',
                'CORREO1': 'correo',
                'CELULAR 1': 'celular',
                'DIRECCIÓN DEL PETICIONARIO': 'direccion',
                'BARRIO, VEREDA O SECTOR': 'barrio',
                'UNIDAD': 'unidad',
                'AREAS DE INTERVENCIÓN': 'areas_intervencion',
                'ENLACE': 'enlace',
                'LÍDER': 'lider'
            }
            
            # Renombrar columnas si es necesario
            for old_name, new_name in column_mapping.items():
                if old_name in self._historico_df.columns and new_name not in self._historico_df.columns:
                    self._historico_df = self._historico_df.rename(columns={old_name: new_name})
                    logger.info(f"Columna renombrada: {old_name} -> {new_name}")
            
            # Crear columna nombre combinada si no existe
            if 'nombre_completo' not in self._historico_df.columns:
                if all(col in self._historico_df.columns for col in ['primer_nombre', 'primer_apellido']):
                    self._historico_df['nombre_completo'] = (
                        self._historico_df['primer_nombre'].fillna('') + ' ' + 
                        self._historico_df['primer_apellido'].fillna('')
                    ).str.strip()
                    logger.info("Columna nombre_completo creada combinando campos de nombre")
            
            # Verificar columnas requeridas mínimas
            required_columns = ['numero_radicado', 'texto_pqrs', 'estado_pqrs']
            available_columns = list(self._historico_df.columns)
            
            # Verificar qué columnas requeridas están disponibles
            missing_columns = [col for col in required_columns if col not in available_columns]
            if missing_columns:
                logger.warning(f"Columnas requeridas faltantes: {missing_columns}")
                logger.info(f"Columnas disponibles: {available_columns}")
                
                # Crear columnas faltantes con valores por defecto si es posible
                if 'texto_pqrs' not in available_columns and 'asunto_peticion' in available_columns:
                    self._historico_df['texto_pqrs'] = self._historico_df['asunto_peticion']
                    logger.info("Columna texto_pqrs creada desde asunto_peticion")
                
                if 'estado_pqrs' not in available_columns and 'estado' in available_columns:
                    self._historico_df['estado_pqrs'] = self._historico_df['estado']
                    logger.info("Columna estado_pqrs creada desde estado")
            else:
                logger.info("Todas las columnas requeridas están disponibles")
    

    
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
    
    def search_historico_advanced(self, search_term: str, search_type: str = 'texto') -> List[PQRSHistorico]:
        """Búsqueda avanzada en el histórico por diferentes criterios"""
        try:
            df = self._load_historico()
            
            if search_type == 'texto':
                # Búsqueda en texto de PQRS
                if 'texto_pqrs' in df.columns:
                    try:
                        # Convertir a string y manejar valores nulos
                        df_texto = df['texto_pqrs'].astype(str).fillna('')
                        result = df[df_texto.str.contains(search_term, case=False, na=False)]
                    except Exception as e:
                        logger.error(f"Error en búsqueda por texto: {e}")
                        # Fallback: búsqueda simple
                        result = df[df['texto_pqrs'].astype(str).str.contains(search_term, case=False, na=False)]
                else:
                    logger.warning("Columna 'texto_pqrs' no disponible para búsqueda")
                    return []
            elif search_type == 'nombre':
                # Búsqueda por nombre
                if 'nombre' in df.columns:
                    # Convertir a string y manejar valores nulos
                    df_nombre = df['nombre'].astype(str).fillna('')
                    result = df[df_nombre.str.contains(search_term, case=False, na=False)]
                else:
                    logger.warning("Columna 'nombre' no disponible para búsqueda")
                    return []
            elif search_type == 'clasificacion':
                # Búsqueda por clasificación
                if 'clasificacion' in df.columns:
                    result = df[df['clasificacion'].str.contains(search_term, case=False, na=False)]
                else:
                    logger.warning("Columna 'clasificacion' no disponible para búsqueda")
                    return []
            elif search_type == 'estado':
                # Búsqueda por estado
                if 'estado_pqrs' in df.columns:
                    result = df[df['estado_pqrs'].str.contains(search_term, case=False, na=False)]
                else:
                    logger.warning("Columna 'estado_pqrs' no disponible para búsqueda")
                    return []
            else:
                logger.error(f"Tipo de búsqueda no válido: {search_type}")
                return []
            
            return [PQRSHistorico.from_dict(row.to_dict()) for _, row in result.iterrows()]
            
        except Exception as e:
            logger.error(f"Error en búsqueda avanzada de histórico: {e}")
            return []
    
    def get_historico_by_date_range(self, start_date: str, end_date: str) -> List[PQRSHistorico]:
        """Obtiene registros históricos en un rango de fechas"""
        try:
            df = self._load_historico()
            if 'fecha_radicacion' not in df.columns:
                logger.error("Columna 'fecha_radicacion' no encontrada en el archivo histórico")
                return []
            
            # Convertir fechas a datetime si es posible
            try:
                df['fecha_radicacion'] = pd.to_datetime(df['fecha_radicacion'], errors='coerce')
                start_dt = pd.to_datetime(start_date)
                end_dt = pd.to_datetime(end_date)
                
                result = df[(df['fecha_radicacion'] >= start_dt) & (df['fecha_radicacion'] <= end_dt)]
                return [PQRSHistorico.from_dict(row.to_dict()) for _, row in result.iterrows()]
                
            except Exception as e:
                logger.warning(f"No se pudo procesar fechas: {e}")
                return []
                
        except Exception as e:
            logger.error(f"Error al obtener histórico por rango de fechas: {e}")
            return []
    
    def get_historico_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen del histórico con estadísticas detalladas"""
        try:
            df = self._load_historico()
            
            summary = {
                'total_registros': len(df),
                'fuente_datos': self._historico_source,
                'columnas_disponibles': list(df.columns),
                'ultima_actualizacion': None
            }
            
            # Estadísticas por clasificación
            if 'clasificacion' in df.columns:
                summary['por_clasificacion'] = df['clasificacion'].value_counts().to_dict()
            
            # Estadísticas por estado
            if 'estado_pqrs' in df.columns:
                summary['por_estado'] = df['estado_pqrs'].value_counts().to_dict()
            
            # Fecha más reciente
            if 'fecha_radicacion' in df.columns:
                try:
                    df['fecha_radicacion'] = pd.to_datetime(df['fecha_radicacion'], errors='coerce')
                    summary['ultima_actualizacion'] = df['fecha_radicacion'].max().strftime('%Y-%m-%d') if not df['fecha_radicacion'].isna().all() else None
                except:
                    summary['ultima_actualizacion'] = None
            
            return summary
            
        except Exception as e:
            logger.error(f"Error al obtener resumen del histórico: {e}")
            return {}
    
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
