import json
from typing import Dict, Any, Optional
from openai import OpenAI
from src.utils.logger import logger
from src.config.config import config
from src.models.pqrs_model import PQRSData
from src.repositories.pqrs_repository import PromptRepository

class PQRSClassifierService:
    """Servicio especializado en clasificación de PQRS"""
    
    def __init__(self, openai_client: OpenAI, prompt_repository: PromptRepository):
        """Inicializa el servicio de clasificación"""
        self.openai_client = openai_client
        self.prompt_repository = prompt_repository
        self.model = config.OPENAI_MODEL
        logger.info("Servicio de clasificación de PQRS inicializado")
    
    def classify_pqrs(self, transcription: str) -> PQRSData:
        """Clasifica una PQRS basada en la transcripción"""
        try:
            # Construir el prompt de clasificación
            system_prompt = self._build_classification_prompt()
            
            # Crear mensajes para OpenAI
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Inicio PQRS:\n{transcription}\nFin PQRS.\nNo des explicaciones adicionales, sólo responde con el JSON."}
            ]
            
            # Realizar llamada a OpenAI
            response = self.openai_client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            # Procesar respuesta
            response_content = response.choices[0].message.content
            logger.debug(f"Respuesta de clasificación recibida: {response_content}")
            
            # Parsear JSON y crear modelo de datos
            pqrs_data = self._parse_classification_response(response_content)
            
            logger.info(f"PQRS clasificada exitosamente: {pqrs_data.clase}")
            return pqrs_data
            
        except Exception as e:
            logger.error(f"Error en clasificación de PQRS: {e}")
            raise
    
    def _build_classification_prompt(self) -> str:
        """Construye el prompt de clasificación"""
        try:
            # Obtener todos los prompts necesarios
            estructura = self.prompt_repository.get_prompt('estructura_json')
            categorias = self.prompt_repository.get_prompt('categorias')
            sys_prompt = self.prompt_repository.get_prompt('sys_prompt')
            faqs = self.prompt_repository.get_prompt('faqs')
            entidades = self.prompt_repository.get_prompt('entidades')
            
            # Formatear el prompt principal
            formatted_prompt = sys_prompt.format(
                estructura=estructura,
                categorias=categorias,
                faqs=faqs,
                entidades=entidades
            )
            
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"Error al construir prompt de clasificación: {e}")
            raise
    
    def _parse_classification_response(self, response_content: str) -> PQRSData:
        """Parsea la respuesta de clasificación y crea el modelo de datos"""
        try:
            # Limpiar la respuesta si es necesario
            cleaned_response = response_content.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            
            # Parsear JSON
            json_data = json.loads(cleaned_response)
            
            # Asegurar que todos los campos requeridos estén presentes con valores por defecto
            default_values = {
                'nombre': "",
                'telefono': "",
                'cedula': "",
                'clase': "SOLICITUD-INTERÉS PARTICULAR",
                'explicacion': "",
                'radicado': "",
                'entidad_responde': "Secretaría de Infraestructura Física",
                'es_faq': "No",
                'barrio': "",
                'tipo_solicitud': "",
                'tema_principal': ""
            }
            
            # Completar campos faltantes con valores por defecto
            for field, default_value in default_values.items():
                if field not in json_data or json_data[field] is None:
                    json_data[field] = default_value
            
            # Crear y retornar modelo de datos usando from_dict
            return PQRSData.from_dict(json_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON de clasificación: {e}")
            # Retornar modelo con valores por defecto en caso de error
            return PQRSData(
                nombre="",
                telefono="",
                cedula="",
                clase="SOLICITUD-INTERÉS PARTICULAR",
                explicacion="Error en clasificación automática",
                radicado="",
                entidad_responde="Secretaría de Infraestructura Física",
                es_faq="No",
                barrio="",
                tipo_solicitud="SOLICITUD-INTERÉS PARTICULAR",
                tema_principal="Infraestructura física"
            )
        except Exception as e:
            logger.error(f"Error inesperado al procesar clasificación: {e}")
            # Retornar modelo con valores por defecto
            return PQRSData(
                nombre="",
                telefono="",
                cedula="",
                clase="SOLICITUD-INTERÉS PARTICULAR",
                explicacion="Error en procesamiento",
                radicado="",
                entidad_responde="Secretaría de Infraestructura Física",
                es_faq="No",
                barrio="",
                tipo_solicitud="SOLICITUD-INTERÉS PARTICULAR",
                tema_principal="Infraestructura física"
            )
            raise ValueError(f"Respuesta de clasificación no es un JSON válido: {e}")
        except Exception as e:
            logger.error(f"Error al procesar respuesta de clasificación: {e}")
            raise
    
    def validate_classification(self, pqrs_data: PQRSData) -> bool:
        """Valida que la clasificación sea correcta"""
        try:
            # Validaciones básicas
            if not pqrs_data.clase:
                logger.warning("Clase de PQRS no especificada")
                return False
            
            if not pqrs_data.entidad_responde:
                logger.warning("Entidad que responde no especificada")
                return False
            
            if pqrs_data.es_faq not in ["Sí", "No"]:
                logger.warning("Campo es_faq debe ser 'Sí' o 'No'")
                return False
            
            logger.debug("Clasificación validada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en validación de clasificación: {e}")
            return False
    
    def get_classification_summary(self, pqrs_data: PQRSData) -> Dict[str, Any]:
        """Obtiene un resumen de la clasificación"""
        return {
            "clase": pqrs_data.clase,
            "entidad_responde": pqrs_data.entidad_responde,
            "es_faq": pqrs_data.es_faq,
            "tiene_radicado": bool(pqrs_data.radicado),
            "tiene_nombre": bool(pqrs_data.nombre)
        }
    
    def _create_default_pqrs_data(self, transcription: str) -> PQRSData:
        """Crea datos de PQRS por defecto en caso de error"""
        try:
            # Intentar extraer información básica del texto
            text_lower = transcription.lower()
            
            # Determinar clase por palabras clave
            clase = "Petición"  # Por defecto
            if any(word in text_lower for word in ["queja", "me quejo", "inconformidad"]):
                clase = "Queja"
            elif any(word in text_lower for word in ["reclamo", "reclamo por"]):
                clase = "Reclamo"
            elif any(word in text_lower for word in ["sugerencia", "sugiero", "recomiendo"]):
                clase = "Sugerencia"
            elif any(word in text_lower for word in ["denuncia", "denuncio"]):
                clase = "Denuncia"
            
            # Determinar si es FAQ
            es_faq = "No"
            if any(word in text_lower for word in ["cómo", "cuándo", "dónde", "qué", "cuál", "información", "proceso"]):
                es_faq = "Sí"
            
            # Crear datos por defecto
            default_data = {
                "nombre": "",
                "telefono": "",
                "cedula": "",
                "clase": clase,
                "explicacion": f"Clasificación automática basada en: {transcription[:100]}...",
                "radicado": "",
                "entidad_responde": "Secretaría de Infraestructura Física - Alcaldía de Medellín",
                "es_faq": es_faq
            }
            
            logger.info(f"Datos por defecto creados para PQRS: {clase}")
            return PQRSData.from_dict(default_data)
            
        except Exception as e:
            logger.error(f"Error al crear datos por defecto: {e}")
            # Retornar datos mínimos en caso de error crítico
            return PQRSData(
                nombre="",
                telefono="",
                cedula="",
                clase="Petición",
                explicacion="Error en clasificación automática",
                radicado="",
                entidad_responde="Secretaría de Infraestructura Física - Alcaldía de Medellín",
                es_faq="No"
            )
