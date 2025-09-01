import logging
import sys
from pathlib import Path
from src.config.config import config

class Logger:
    """Sistema de logging centralizado para TUNRAG"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        """Inicializa el logger con configuración estándar"""
        self.logger = logging.getLogger('TUNRAG')
        self.logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        # Evitar duplicación de handlers
        if not self.logger.handlers:
            # Handler para consola
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(config.LOG_FORMAT)
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
            # Handler para archivo
            log_dir = Path(__file__).parent.parent.parent / 'logs'
            log_dir.mkdir(exist_ok=True)
            file_handler = logging.FileHandler(log_dir / 'tunrag.log', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(config.LOG_FORMAT)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message):
        """Log de nivel INFO"""
        self.logger.info(message)
    
    def debug(self, message):
        """Log de nivel DEBUG"""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log de nivel WARNING"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log de nivel ERROR"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log de nivel CRITICAL"""
        self.logger.critical(message)
    
    def exception(self, message):
        """Log de excepción con traceback"""
        self.logger.exception(message)

# Instancia global del logger
logger = Logger()
