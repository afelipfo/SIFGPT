from datetime import datetime
from typing import Dict, Any, Optional
from openai import OpenAI
from src.utils.logger import logger
from src.config.config import config
from src.models.pqrs_model import PQRSData, PQRSHistorico
from src.repositories.pqrs_repository import PromptRepository, PQRSRepository

class ResponseGeneratorService:
    """Servicio especializado en generación de respuestas para PQRS"""
    
    def __init__(self, openai_client: OpenAI, prompt_repository: PromptRepository, pqrs_repository: PQRSRepository):
        """Inicializa el servicio de generación de respuestas"""
        self.openai_client = openai_client
        self.prompt_repository = prompt_repository
        self.pqrs_repository = pqrs_repository
        self.model = config.OPENAI_MODEL
        logger.info("Servicio de generación de respuestas inicializado")
    
    def generate_response(self, pqrs_data: PQRSData, transcription: str) -> str:
        """Genera una respuesta apropiada para la PQRS"""
        try:
            if pqrs_data.es_faq == "Sí":
                return self._generate_faq_response(pqrs_data, transcription)
            else:
                return self._generate_standard_response(pqrs_data)
                
        except Exception as e:
            logger.error(f"Error al generar respuesta: {e}")
            raise
    
    def _generate_faq_response(self, pqrs_data: PQRSData, transcription: str) -> str:
        """Genera respuesta para preguntas frecuentes"""
        try:
            # Obtener prompt para FAQs
            sys_prompt_faqs = self.prompt_repository.get_prompt('sys_prompt_faqs')
            respuestas_faqs = self.prompt_repository.get_prompt('respuestas_faqs')
            
            # Formatear prompt
            formatted_prompt = sys_prompt_faqs.format(faqs=respuestas_faqs)
            
            # Crear mensajes para OpenAI
            messages = [
                {'role': 'system', 'content': formatted_prompt},
                {'role': 'user', 'content': f"Inicio PQRS:\n{transcription}\nFin PQRS.\nResponde con la respuesta a la pregunta frecuente."}
            ]
            
            # Realizar llamada a OpenAI
            response = self.openai_client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
            )
            
            response_content = response.choices[0].message.content
            logger.info("Respuesta FAQ generada exitosamente")
            return response_content
            
        except Exception as e:
            logger.error(f"Error al generar respuesta FAQ: {e}")
            raise
    
    def _generate_standard_response(self, pqrs_data: PQRSData) -> str:
        """Genera respuesta estándar para PQRS no-FAQ"""
        try:
            fecha = datetime.strftime(datetime.today(), format="%m/%d/%Y")
            
            if pqrs_data.radicado:
                return self._generate_historical_response(pqrs_data, fecha)
            else:
                return self._generate_new_pqrs_response(pqrs_data, fecha)
                
        except Exception as e:
            logger.error(f"Error al generar respuesta estándar: {e}")
            raise
    
    def _generate_new_pqrs_response(self, pqrs_data: PQRSData, fecha: str) -> str:
        """Genera respuesta para nueva PQRS"""
        try:
            # Obtener plantilla para nueva PQRS
            plantilla = self.prompt_repository.get_plantilla('plantilla')
            sys_prompt_solucion = self.prompt_repository.get_prompt('sys_prompt_solucion')
            faqs = self.prompt_repository.get_prompt('faqs')
            
            # Formatear plantilla para nueva PQRS
            formatted_plantilla = plantilla.format(
                nombre=pqrs_data.nombre or "Ciudadano/a",
                fecha=fecha,
                clase=pqrs_data.clase,
                tipo_solicitud=pqrs_data.tipo_solicitud or pqrs_data.clase,
                entidad=pqrs_data.entidad_responde,
                tema_principal=pqrs_data.tema_principal or "Infraestructura física"
            )
            
            # Formatear prompt de solución
            formatted_sys_prompt = sys_prompt_solucion.format(faqs=faqs)
            
            # Crear mensajes para OpenAI
            messages = [
                {"role": "system", "content": formatted_sys_prompt},
                {"role": "user", "content": formatted_plantilla}
            ]
            
            # Realizar llamada a OpenAI
            response = self.openai_client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
            )
            
            response_content = response.choices[0].message.content
            logger.info("Respuesta para nueva PQRS generada exitosamente")
            return response_content
            
        except Exception as e:
            logger.error(f"Error al generar respuesta para nueva PQRS: {e}")
            raise
    
    def _generate_historical_response(self, pqrs_data: PQRSData, fecha: str) -> str:
        """Genera respuesta para PQRS con radicado existente"""
        try:
            # Buscar en histórico
            historico = self.pqrs_repository.get_historico_by_radicado(pqrs_data.radicado)
            if not historico:
                logger.warning(f"No se encontró histórico para radicado: {pqrs_data.radicado}")
                return self._generate_new_pqrs_response(pqrs_data, fecha)
            
            # Obtener plantilla para PQRS histórica
            plantilla_hist = self.prompt_repository.get_plantilla('plantilla')
            sys_prompt_solucion = self.prompt_repository.get_prompt('sys_prompt_solucion')
            faqs = self.prompt_repository.get_prompt('faqs')
            
            # Formatear plantilla para consulta de estado
            formatted_plantilla = plantilla_hist.format(
                nombre=pqrs_data.nombre or historico.nombre or "Ciudadano/a",
                fecha=fecha,
                radicado=historico.numero_radicado,
                estado=historico.estado_pqrs or "En proceso",
                unidad=historico.unidad or "Secretaría de Infraestructura Física",
                fecha_radicacion=historico.fecha_radicacion or "No disponible",
                barrio=historico.barrio or "No especificado",
                informacion_adicional=f"Asunto: {historico.texto_pqrs[:200] + '...' if len(historico.texto_pqrs or '') > 200 else historico.texto_pqrs or 'No disponible'}"
            )
            
            # Formatear prompt de solución
            formatted_sys_prompt = sys_prompt_solucion.format(faqs=faqs)
            
            # Crear mensajes para OpenAI
            messages = [
                {"role": "system", "content": formatted_sys_prompt},
                {"role": "user", "content": formatted_plantilla}
            ]
            
            # Realizar llamada a OpenAI
            response = self.openai_client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
            )
            
            response_content = response.choices[0].message.content
            logger.info("Respuesta para PQRS histórica generada exitosamente")
            return response_content
            
        except Exception as e:
            logger.error(f"Error al generar respuesta para PQRS histórica: {e}")
            raise
    
    def generate_test_response(self) -> str:
        """Genera respuesta de prueba"""
        test_response = """Gracias por ponerte en contacto con nosotros. Nos complace informarte que tu petición ha sido enviada al área encargada en la Secretaría de Educación y está siendo procesada en el sistema. A continuación, te proporcionamos una plantilla de solución de peticiones que puedes utilizar para seguir el estado de tu solicitud y obtener la información necesaria:

---

**Referencia de la Petición:** [Número de Radicado]

**Fecha de Recepción:** 08/15/2024

**Área Encargada:** Secretaría de Educación

**Estado Actual:** En proceso

**Próximos Pasos:** 

1. **Revisión Inicial:** El equipo revisará tu petición para asegurarse de que toda la información necesaria ha sido proporcionada.
2. **Asignación:** Tu petición será asignada a un funcionario específico que se encargará de darle seguimiento.
3. **Respuesta:** Recibirás una respuesta oficial por parte de la Secretaría de Educación dentro del plazo estipulado por la normativa vigente.

**Contacto Adicional:** Si tienes alguna pregunta adicional o necesitas más información, puedes ponerte en contacto con nosotros a través del correo electrónico [correo@medellin.gov.co] o llamando al [número de contacto].

Agradecemos tu paciencia y comprensión mientras trabajamos para resolver tu petición."""
        
        logger.info("Respuesta de prueba generada")
        return test_response
    
    def validate_response(self, response: str) -> bool:
        """Valida que la respuesta sea apropiada"""
        try:
            if not response or len(response.strip()) < 50:
                logger.warning("Respuesta demasiado corta")
                return False
            
            # Validaciones adicionales pueden ser agregadas aquí
            logger.debug("Respuesta validada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en validación de respuesta: {e}")
            return False
