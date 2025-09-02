import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
load_dotenv(override=True)

class Config:
    """Configuración centralizada del proyecto TUNRAG"""
    
    # Configuración de la aplicación
    APP_NAME = "SIFGPT - Sistema de PQRS"
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Configuración de OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
    WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'whisper-1')
    
    # Configuración de directorios
    BASE_DIR = Path(__file__).parent.parent.parent
    INPUT_DIR = BASE_DIR / 'input'
    AUDIO_DIR = INPUT_DIR / 'audios'
    HISTORICO_DIR = INPUT_DIR / 'historico'
    PROMPTS_DIR = INPUT_DIR / 'prompts'
    PLANTILLAS_DIR = INPUT_DIR / 'plantillas_solucion'
    
    # Configuración de archivos
    HISTORICO_EXCEL = HISTORICO_DIR / 'historico2.xlsx'
    
    # Configuración de prompts
    PROMPT_FILES = {
        'estructura_json': PROMPTS_DIR / 'estructura_json.txt',
        'categorias': PROMPTS_DIR / 'categorias.txt',
        'sys_prompt': PROMPTS_DIR / 'sys_prompt.txt',
        'sys_prompt_solucion': PROMPTS_DIR / 'sys_prompt_solucion.txt',
        'sys_prompt_faqs': PROMPTS_DIR / 'sys_prompt_faqs.txt',
        'faqs': PROMPTS_DIR / 'faqs.txt',
        'respuestas_faqs': PROMPTS_DIR / 'respuestas_faqs.txt',
        'entidades': PROMPTS_DIR / 'entidades.txt'
    }
    
    # Configuración de plantillas (unificada)
    PLANTILLA_FILES = {
        'plantilla': PLANTILLAS_DIR / 'plantilla.txt'
    }
    
    # Configuración de audio
    AUDIO_EXTENSIONS = ["*.aac", "*.wav", "*.opus", "*.ogg", "*.mp3", "*.mp4", "*.mpeg", "*.m4a", "*.flac"]
    
    # Configuración de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def validate_config(cls):
        """Valida que la configuración sea correcta"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está configurada")
        
        # Validar que existan los directorios necesarios
        required_dirs = [cls.INPUT_DIR, cls.AUDIO_DIR, cls.HISTORICO_DIR, cls.PROMPTS_DIR, cls.PLANTILLAS_DIR]
        for directory in required_dirs:
            if not directory.exists():
                raise ValueError(f"Directorio requerido no existe: {directory}")
        
        # Validar que existan los archivos de prompts
        for prompt_name, prompt_path in cls.PROMPT_FILES.items():
            if not prompt_path.exists():
                raise ValueError(f"Archivo de prompt requerido no existe: {prompt_path}")
        
        # Validar que existan los archivos de plantillas
        for plantilla_name, plantilla_path in cls.PLANTILLA_FILES.items():
            if not plantilla_path.exists():
                raise ValueError(f"Archivo de plantilla requerido no existe: {plantilla_path}")
        
        return True

# Instancia global de configuración
config = Config()
