import gradio as gr
import os
from src.services.pqrs_orchestrator_service import PQRSOrchestratorService
from src.utils.logger import logger

class ChatBuilder:
    """Clase principal para construir interfaces de chat con Gradio"""
    
    def __init__(self, audio_path: str, transcript_api_key: str):
        """Inicializa el constructor de chat"""
        self.audio_path = audio_path
        self.transcript_api_key = transcript_api_key
        self.chat_actions = ChatActions(audio_path, transcript_api_key)
        logger.info("ChatBuilder inicializado exitosamente")
    
    def build_interface(self):
        """Construye la interfaz de Gradio"""
        try:
                with gr.Blocks(title="SIFGPT - Sistema de PQRS") as interface:
        gr.Markdown("# 🤖 SIFGPT - Sistema de PQRS Inteligente"
                gr.Markdown("Sistema automatizado para procesamiento de PQRS usando IA")
                
                with gr.Row():
                    with gr.Column():
                        chatbot = gr.Chatbot(label="Chat")
                        msg = gr.Textbox(label="Mensaje", placeholder="Escribe tu consulta...")
                        send_btn = gr.Button("Enviar", variant="primary")
                    
                    with gr.Column():
                        audio_input = gr.Audio(label="Audio", type="filepath")
                        audio_btn = gr.Button("Procesar Audio", variant="secondary")
                        status = gr.Textbox(label="Estado del Sistema", interactive=False)
                
                # Eventos
                send_btn.click(
                    self.chat_actions.chat_response,
                    inputs=[chatbot, msg],
                    outputs=[chatbot, msg]
                )
                
                audio_btn.click(
                    self.chat_actions.audio_response,
                    inputs=[chatbot, audio_input],
                    outputs=[chatbot, audio_input]
                )
                
                # Estado del sistema
                interface.load(
                    self.chat_actions.get_system_status,
                    outputs=status
                )
            
            logger.info("Interfaz de Gradio construida exitosamente")
            return interface
            
        except Exception as e:
            logger.error(f"Error construyendo interfaz: {e}")
            raise

class ChatActions:
    """Clase para manejar acciones del chat usando la nueva arquitectura"""

    def __init__(self, audio_path: str, transcript_api_key: str):
        """Inicializa las acciones del chat"""
        self.audio_path = audio_path
        self.transcript_api_key = transcript_api_key
        
        try:
            # Inicializar el orquestador de PQRS
            self.pqrs_orchestrator = PQRSOrchestratorService(transcript_api_key)
            logger.info("ChatActions inicializado exitosamente")
        except Exception as e:
            logger.error(f"Error al inicializar ChatActions: {e}")
            raise
        
    def chat_response(self, history, user_message):
        """Genera respuesta del chat"""
        if user_message:
            try:
                # Procesar PQRS desde texto
                result = self.pqrs_orchestrator.process_text_pqrs(user_message)
                
                if result["success"]:
                    bot_message = result["response"]
                else:
                    bot_message = "Lo sentimos, ha ocurrido un error en el procesamiento de tu solicitud."
                    logger.error(f"Error en chat_response: {result.get('error')}")
                
                history.append((user_message, bot_message))
                logger.info("Respuesta del chat generada exitosamente")
                
            except Exception as e:
                logger.error(f"Error en chat_response: {e}")
                bot_message = "Lo sentimos, ha ocurrido un error inesperado."
                history.append((user_message, bot_message))
        
        return history, gr.update(value="", interactive=True)
    
    def audio_response(self, history, audio):
        """Procesa respuesta de audio"""
        if audio:
            try:
                # Crear directorio si no existe
                os.makedirs(self.audio_path, exist_ok=True)
                
                # Guardar archivo de audio
                audio_path = os.path.join(self.audio_path, os.path.basename(audio))
                os.rename(audio, audio_path)
                
                # Obtener archivos de audio
                audio_files = self.pqrs_orchestrator.get_audio_files(self.audio_path)
                
                if audio_files:
                    # Transcribir solo el audio (sin procesar PQRS completo)
                    transcription = self.pqrs_orchestrator.transcribe_audio_only(audio_files[0])
                    logger.info("Audio transcrito exitosamente")
                else:
                    transcription = "No se encontraron archivos de audio"
                    logger.warning("No se encontraron archivos de audio")
                
            except Exception as e:
                logger.error(f"Error en audio_response: {e}")
                transcription = "Error al procesar el audio"
        
        return history, gr.update(value=transcription, interactive=True)
    
    def get_system_status(self):
        """Obtiene el estado del sistema"""
        try:
            return self.pqrs_orchestrator.get_system_status()
        except Exception as e:
            logger.error(f"Error al obtener estado del sistema: {e}")
            return {"error": str(e)}
    
    def validate_system(self):
        """Valida el sistema"""
        try:
            return self.pqrs_orchestrator.validate_system()
        except Exception as e:
            logger.error(f"Error al validar sistema: {e}")
            return False