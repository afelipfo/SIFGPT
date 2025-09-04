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
        """Genera una respuesta apropiada para la PQRS usando IA"""
        try:
            fecha = datetime.now().strftime("%d/%m/%Y")
            
            # Generar respuesta conversacional usando IA (mantener compatibilidad)
            fake_context = {
                'messages': [{'role': 'user', 'content': transcription}],
                'classification_history': [],
                'current_topic': pqrs_data.tema_principal
            }
            return self.generate_conversational_response(pqrs_data, transcription, fake_context)
                
        except Exception as e:
            logger.error(f"Error al generar respuesta: {e}")
            # Fallback a respuesta básica
            nombre = pqrs_data.nombre or "Ciudadano/a"
            return f"Estimado/a {nombre}, hemos recibido tu solicitud y será procesada. Gracias por contactarnos."
    
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
    
    def generate_conversational_response(self, pqrs_data: PQRSData, current_message: str, conversation_context: Dict[str, Any]) -> str:
        """Genera una respuesta conversacional inteligente con contexto completo"""
        try:
            # Cargar prompt conversacional avanzado
            try:
                with open('input/prompts/sys_prompt_conversacional.txt', 'r', encoding='utf-8') as f:
                    conversational_prompt = f.read()
            except:
                conversational_prompt = self._get_fallback_conversational_prompt()
            
            # Construir historial de conversación
            conversation_history = self._build_conversation_history(conversation_context)
            
            # Crear contexto específico para el mensaje actual
            context_info = f"""
CONTEXTO DE LA CONVERSACIÓN:
{conversation_history}

INFORMACIÓN ACTUAL:
- Clasificación: {pqrs_data.clase or 'Conversación'}
- Tema principal: {pqrs_data.tema_principal or 'General'}
- Barrio: {pqrs_data.barrio or 'No especificado'}

MENSAJE ACTUAL DEL CIUDADANO: "{current_message}"

INSTRUCCIÓN: Responde manteniendo la coherencia con toda la conversación anterior. Si el ciudadano se refiere a algo mencionado antes, haz referencia específica a ello."""

            # Crear mensajes para OpenAI
            messages = [
                {"role": "system", "content": conversational_prompt},
                {"role": "user", "content": context_info}
            ]
            
            # Realizar llamada a OpenAI con parámetros optimizados
            response = self.openai_client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.9,  # Más creatividad para conversaciones naturales
                max_tokens=250,   # Respuestas concisas pero completas
                presence_penalty=0.6,
                frequency_penalty=0.4
            )
            
            response_content = response.choices[0].message.content.strip()
            logger.info("Respuesta conversacional inteligente generada exitosamente")
            return response_content
            
        except Exception as e:
            logger.error(f"Error al generar respuesta conversacional: {e}")
            # Fallback a respuesta contextual básica
            return self._generate_basic_contextual_response(current_message, conversation_context)

    def _build_conversation_history(self, context: Dict[str, Any]) -> str:
        """Construye un resumen del historial de conversación"""
        messages = context.get('messages', [])
        if not messages or len(messages) <= 1:
            return "Esta es la primera interacción del ciudadano."
        
        # Tomar últimos 6 mensajes para mantener contexto sin sobrecargar
        recent_messages = messages[-6:]
        history_lines = []
        
        for msg in recent_messages:
            role = "Ciudadano" if msg['role'] == 'user' else "SIF-GPT"
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            history_lines.append(f"{role}: {content}")
        
        return "\n".join(history_lines)

    def _get_fallback_conversational_prompt(self) -> str:
        """Prompt de respaldo si no se puede cargar el archivo"""
        return """Eres SIF-GPT, asistente inteligente de la Alcaldía de Medellín. Mantén el contexto de toda la conversación, haz referencias específicas a mensajes anteriores cuando sea relevante, y responde de manera natural y útil. Sé conciso pero completo."""

    def _generate_basic_contextual_response(self, current_message: str, context: Dict[str, Any]) -> str:
        """Genera respuesta básica con contexto"""
        if len(context.get('messages', [])) <= 1:
            return "¡Hola! Soy SIF-GPT, tu asistente para temas de infraestructura física. ¿En qué puedo ayudarte hoy?"
        
        return "Entiendo tu consulta. Permíteme revisar la información que me proporcionaste anteriormente para darte una respuesta más precisa. ¿Podrías darme un momento?"

    def _generate_new_pqrs_response(self, pqrs_data: PQRSData, fecha: str) -> str:
        """Genera respuesta para nueva PQRS"""
        try:
            # Obtener plantilla para nueva PQRS
            plantilla = self.prompt_repository.get_plantilla('plantilla')
            sys_prompt_solucion = self.prompt_repository.get_prompt('sys_prompt_solucion')
            faqs = self.prompt_repository.get_prompt('faqs')
            
            # Crear respuesta directa para nueva PQRS (sin usar plantilla compleja)
            nombre = pqrs_data.nombre or "Ciudadano/a"
            clase = pqrs_data.clase or "solicitud"
            entidad = pqrs_data.entidad_responde or "Secretaría de Infraestructura Física"
            
            formatted_plantilla = f"""Estimado/a {nombre}, recibimos tu {clase} el día {fecha}.

Tu solicitud ha sido clasificada como: {pqrs_data.tipo_solicitud or clase}
Unidad responsable: {entidad}
Tema principal: {pqrs_data.tema_principal or "Infraestructura física"}

Tu solicitud está siendo procesada y será atendida según los tiempos establecidos por la normatividad vigente.

Te mantendremos informado sobre el avance de tu caso.

Atentamente,
Secretaría de Infraestructura Física - Alcaldía de Medellín"""
            
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
            
            # Crear respuesta directa para consulta de estado
            nombre = pqrs_data.nombre or historico.nombre or "Ciudadano/a"
            
            formatted_plantilla = f"""Estimado/a {nombre}, consultamos el estado de tu solicitud:

Radicado: {historico.numero_radicado}
Estado actual: {historico.estado_pqrs or "En proceso"}
Unidad responsable: {historico.unidad or "Secretaría de Infraestructura Física"}
Fecha de radicación: {historico.fecha_radicacion or "No disponible"}
Barrio/Sector: {historico.barrio or "No especificado"}

Asunto: {historico.texto_pqrs[:200] + '...' if len(historico.texto_pqrs or '') > 200 else historico.texto_pqrs or 'No disponible'}

Si necesitas más información, puedes contactarnos.

Atentamente,
Secretaría de Infraestructura Física - Alcaldía de Medellín"""
            
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
