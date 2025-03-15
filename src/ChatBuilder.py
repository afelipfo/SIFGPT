import gradio as gr
import os
from PQRS import PQRSProcessor

class ChatActions:

    def __init__(self, audio_path: str, transcript_api_key: str):

        self.audio_path = audio_path
        self.transcript_api_key = transcript_api_key

        self.pqrs_proc = PQRSProcessor(base_url=None, openai_api_key=self.transcript_api_key, whisper_model='whisper-1')

        
    def chat_response(self, history, user_message):
        if user_message:

            bot_message = self.pqrs_proc.model_answer(user_message)            
            history.append((user_message, bot_message))
            # Simulating bot response generation logic
        return history, gr.update(value="", interactive=True)
    
    # Function to process audio input and save it to a folder
    def audio_response(self, history, audio):
        if audio:
            # Define the directory to save audio files
            
            os.makedirs(self.audio_path, exist_ok=True)
    
            # Save the audio file
            audio_path = os.path.join(self.audio_path, os.path.basename(audio))
            os.rename(audio, audio_path)

        self.pqrs_proc.get_audio_files(folder_path=self.audio_path)
        self.pqrs_proc.transcribe_audio_openai(self.pqrs_proc.audio_files[0])

        return history, gr.update(value=self.pqrs_proc.transcription, interactive=True)