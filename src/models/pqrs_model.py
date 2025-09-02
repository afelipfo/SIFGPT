from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum

class PQRSClase(Enum):
    """Enumeración de clases de PQRS"""
    PETICION = "Petición"
    QUEJA = "Queja"
    RECLAMO = "Reclamo"
    SUGERENCIA = "Sugerencia"
    DENUNCIA = "Denuncia"

class PQRSEstado(Enum):
    """Enumeración de estados de PQRS"""
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En proceso"
    EN_REVISION = "En revisión"
    RESUELTA = "Resuelta"
    CANCELADA = "Cancelada"

@dataclass
class PQRSData:
    """Modelo de datos para PQRS"""
    nombre: str
    telefono: str
    cedula: str
    clase: str
    explicacion: str
    radicado: str
    entidad_responde: str
    es_faq: str
    barrio: str = ""
    tipo_solicitud: str = ""
    tema_principal: str = ""
    
    def __post_init__(self):
        """Validación post-inicialización"""
        if not self.nombre.strip():
            self.nombre = ""
        if not self.telefono.strip():
            self.telefono = ""
        if not self.cedula.strip():
            self.cedula = ""
        if not self.clase.strip():
            self.clase = ""
        if not self.explicacion.strip():
            self.explicacion = ""
        if not self.radicado.strip():
            self.radicado = ""
        if not self.entidad_responde.strip():
            self.entidad_responde = ""
        if self.es_faq not in ["Sí", "No"]:
            self.es_faq = "No"
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            "nombre": self.nombre,
            "telefono": self.telefono,
            "cedula": self.cedula,
            "clase": self.clase,
            "explicacion": self.explicacion,
            "radicado": self.radicado,
            "entidad_responde": self.entidad_responde,
            "es_faq": self.es_faq,
            "barrio": self.barrio,
            "tipo_solicitud": self.tipo_solicitud,
            "tema_principal": self.tema_principal
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PQRSData':
        """Crea una instancia desde un diccionario"""
        return cls(**data)

@dataclass
class PQRSHistorico:
    """Modelo de datos para PQRS histórico"""
    numero_radicado: str
    nombre: str = ""
    fecha_radicacion: str = ""
    texto_pqrs: str = ""
    clasificacion: str = ""
    estado_pqrs: str = ""
    
    # Campos adicionales del Excel
    mes: Optional[str] = None
    consecutivo_mes: Optional[str] = None
    control_radicado: Optional[str] = None
    rad_respuesta: Optional[str] = None
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    nombre_completo: Optional[str] = None
    fecha_entrada_sif: Optional[str] = None
    fecha_respuesta: Optional[str] = None
    fecha_ingreso: Optional[str] = None
    fecha_ingreso_bandeja: Optional[str] = None
    datos_iniciales: Optional[str] = None
    seguimiento: Optional[str] = None
    observacion: Optional[str] = None
    tipo_solicitud: Optional[str] = None
    tema: Optional[str] = None
    semaforo_dias: Optional[str] = None
    oportunidad: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    correo: Optional[str] = None
    celular: Optional[str] = None
    direccion: Optional[str] = None
    barrio: Optional[str] = None
    unidad: Optional[str] = None
    areas_intervencion: Optional[str] = None
    enlace: Optional[str] = None
    lider: Optional[str] = None
    
    def __post_init__(self):
        """Validación post-inicialización"""
        if not self.numero_radicado.strip():
            raise ValueError("Número de radicado es requerido")
        
        # Asegurar que los campos principales tengan valores por defecto
        if not self.nombre.strip():
            # Intentar construir nombre desde campos individuales
            if self.primer_nombre or self.primer_apellido:
                self.nombre = f"{self.primer_nombre or ''} {self.primer_apellido or ''}".strip()
            elif self.nombre_completo:
                self.nombre = self.nombre_completo
            else:
                self.nombre = ""
        
        if not self.fecha_radicacion.strip():
            self.fecha_radicacion = ""
        if not self.texto_pqrs.strip():
            self.texto_pqrs = ""
        if not self.clasificacion.strip():
            self.clasificacion = ""
        if not self.estado_pqrs.strip():
            self.estado_pqrs = ""
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            "numero_radicado": self.numero_radicado,
            "nombre": self.nombre,
            "fecha_radicacion": self.fecha_radicacion,
            "texto_pqrs": self.texto_pqrs,
            "clasificacion": self.clasificacion,
            "estado_pqrs": self.estado_pqrs,
            "mes": self.mes,
            "consecutivo_mes": self.consecutivo_mes,
            "control_radicado": self.control_radicado,
            "rad_respuesta": self.rad_respuesta,
            "primer_nombre": self.primer_nombre,
            "segundo_nombre": self.segundo_nombre,
            "primer_apellido": self.primer_apellido,
            "segundo_apellido": self.segundo_apellido,
            "nombre_completo": self.nombre_completo,
            "fecha_entrada_sif": self.fecha_entrada_sif,
            "fecha_respuesta": self.fecha_respuesta,
            "fecha_ingreso": self.fecha_ingreso,
            "fecha_ingreso_bandeja": self.fecha_ingreso_bandeja,
            "datos_iniciales": self.datos_iniciales,
            "seguimiento": self.seguimiento,
            "observacion": self.observacion,
            "tipo_solicitud": self.tipo_solicitud,
            "tema": self.tema,
            "semaforo_dias": self.semaforo_dias,
            "oportunidad": self.oportunidad,
            "tipo_documento": self.tipo_documento,
            "numero_documento": self.numero_documento,
            "correo": self.correo,
            "celular": self.celular,
            "direccion": self.direccion,
            "barrio": self.barrio,
            "unidad": self.unidad,
            "areas_intervencion": self.areas_intervencion,
            "enlace": self.enlace,
            "lider": self.lider
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PQRSHistorico':
        """Crea una instancia desde un diccionario"""
        # Mapeo de campos del Excel a campos del modelo
        field_mapping = {
            'numero_radicado': 'numero_radicado',
            'MES': 'mes',
            'CONSECUTIVO MES': 'consecutivo_mes',
            'CONTROL DE RADICADO': 'control_radicado',
            'RAD. RESPUESTA': 'rad_respuesta',
            'PRIMERNOMBRE': 'primer_nombre',
            'SEGUNDONOMBRE': 'segundo_nombre',
            'PRIMERAPELLIDO': 'primer_apellido',
            'SEGUNDOAPELLIDO': 'segundo_apellido',
            'SOLICITANTE': 'nombre_completo',
            'ASUNTO DE LA PETICIÓN': 'texto_pqrs',
            'ESTADO': 'estado_pqrs',
            'CLASE DE SOLICITUD': 'clasificacion',
            'FECHA RADICACIÓN': 'fecha_radicacion',
            'FECHA ENTRADA A SIF': 'fecha_entrada_sif',
            'FECHA RADICADO RESPUESTA': 'fecha_respuesta',
            'FECHA DE INGRESO': 'fecha_ingreso',
            'FECHA DE INGRESO A LA BANDEJA': 'fecha_ingreso_bandeja',
            'DATOS INICIALES PQRSD': 'datos_iniciales',
            'SEGUIMIENTO DE LA PQRSD': 'seguimiento',
            'OBSERVACIÓN': 'observacion',
            'TIPO DE SOLICITUD': 'tipo_solicitud',
            'TEMA': 'tema',
            'SEMAFORO DIAS': 'semaforo_dias',
            'OPORTUNIDAD': 'oportunidad',
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
        
        # Mapear campos del Excel a campos del modelo
        mapped_data = {}
        for excel_field, model_field in field_mapping.items():
            if excel_field in data:
                mapped_data[model_field] = data[excel_field]
        
        # Asegurar que numero_radicado esté presente
        if 'numero_radicado' not in mapped_data:
            # Intentar obtener desde diferentes campos posibles
            for field in ['numero_radicado', 'DOCUMENTO-CarguedeinformaciónalaplicativoPQRSDdelSIF', 'RAD. RESPUESTA']:
                if field in data and data[field]:
                    mapped_data['numero_radicado'] = str(data[field])
                    break
        
        # Filtrar solo los campos que existen en el modelo
        valid_fields = {}
        for k, v in mapped_data.items():
            if k in cls.__dataclass_fields__:
                valid_fields[k] = v
        
        return cls(**valid_fields)

@dataclass
class AudioTranscription:
    """Modelo de datos para transcripción de audio"""
    audio_file: str
    transcription: str
    timestamp: datetime = None
    language: str = "es"
    
    def __post_init__(self):
        """Validación post-inicialización"""
        if not self.audio_file.strip():
            raise ValueError("Archivo de audio es requerido")
        if not self.transcription.strip():
            self.transcription = ""
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if not self.language.strip():
            self.language = "es"
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            "audio_file": self.audio_file,
            "transcription": self.transcription,
            "timestamp": self.timestamp.isoformat(),
            "language": self.language
        }
