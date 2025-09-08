"""
Components - Componentes reutilizables de la interfaz
"""

from .base_tab import BaseTab
from .mixins import InputValidationMixin, ResultDisplayMixin, PlottingMixin
from .constants import (
    VALIDATION, UI, PLOT, COLORS,
    ERROR_MESSAGES, SUCCESS_MESSAGES,
    DEFAULT_CONFIGS, ALLOWED_FUNCTIONS,
    ValidationErrorCodes, ErrorSeverity
)
from .error_handler import ErrorHandler, error_handler, handle_error, handle_validation_error, handle_success
from .validation_mixins import RealTimeValidationMixin, AdvancedValidationMixin

__all__ = [
    # Clases base
    'BaseTab',

    # Mixins existentes
    'InputValidationMixin',
    'ResultDisplayMixin',
    'PlottingMixin',

    # Nuevos mixins
    'RealTimeValidationMixin',
    'AdvancedValidationMixin',

    # Constantes
    'VALIDATION',
    'UI',
    'PLOT',
    'COLORS',
    'ERROR_MESSAGES',
    'SUCCESS_MESSAGES',
    'DEFAULT_CONFIGS',
    'ALLOWED_FUNCTIONS',

    # Enums
    'ValidationErrorCodes',
    'ErrorSeverity',

    # Gestor de errores
    'ErrorHandler',
    'error_handler',
    'handle_error',
    'handle_validation_error',
    'handle_success'
]
