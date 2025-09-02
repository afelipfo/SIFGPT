"""
Controladores del sistema TUNRAG
"""

from .historico_controller import historico_bp
from .pqrs_controller import pqrs_bp

__all__ = [
    'historico_bp',
    'pqrs_bp'
]
