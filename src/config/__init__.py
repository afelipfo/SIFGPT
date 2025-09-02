"""
Paquete de configuración del sistema SIFGPT

Este módulo contiene la configuración centralizada del sistema,
incluyendo variables de entorno, configuraciones de base de datos,
y parámetros del sistema.
"""

from .config import config, Config

__all__ = ['config', 'Config']
