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
            "es_faq": self.es_faq
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PQRSData':
        """Crea una instancia desde un diccionario"""
        return cls(**data)

@dataclass
class PQRSHistorico:
    """Modelo de datos para PQRS histórico"""
    numero_radicado: str
    nombre: str
    fecha_radicacion: str
    texto_pqrs: str
    clasificacion: str
    estado_pqrs: str
    
    def __post_init__(self):
        """Validación post-inicialización"""
        if not self.numero_radicado.strip():
            raise ValueError("Número de radicado es requerido")
        if not self.nombre.strip():
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
            "estado_pqrs": self.estado_pqrs
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PQRSHistorico':
        """Crea una instancia desde un diccionario"""
        return cls(**data)

@dataclass
class AudioTranscription:
    """Modelo de datos para transcripción de audio"""
    audio_file: str
    transcription: str
    timestamp: datetime
    language: str = "es"
    
    def __post_init__(self):
        """Validación post-inicialización"""
        if not self.audio_file.strip():
            raise ValueError("Archivo de audio es requerido")
        if not self.transcription.strip():
            self.transcription = ""
        if not self.timestamp:
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
