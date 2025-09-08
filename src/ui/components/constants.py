"""
Constantes centralizadas para la aplicación del simulador matemático.

Este módulo contiene todas las constantes y configuraciones por defecto
usadas en la aplicación, siguiendo el principio DRY.
"""

from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum


class ValidationErrorCodes(Enum):
    """Códigos de error para validación"""
    EMPTY_FIELD = "EMPTY_FIELD"
    INVALID_NUMBER = "INVALID_NUMBER"
    INVALID_FUNCTION = "INVALID_FUNCTION"
    INVALID_RANGE = "INVALID_RANGE"
    DIVISION_BY_ZERO = "DIVISION_BY_ZERO"
    CONVERGENCE_FAILED = "CONVERGENCE_FAILED"


class ErrorSeverity(Enum):
    """Niveles de severidad para errores"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationConstants:
    """Constantes para validación de entrada"""
    MAX_ITERATIONS: int = 1000
    MIN_ITERATIONS: int = 1
    DEFAULT_TOLERANCE: float = 1e-6
    MIN_TOLERANCE: float = 1e-15
    MAX_TOLERANCE: float = 1e-1
    DEFAULT_STEP_SIZE: float = 0.1
    MIN_STEP_SIZE: float = 1e-10
    MAX_STEP_SIZE: float = 1.0
    MAX_SUBDIVISIONS: int = 10000
    MIN_SUBDIVISIONS: int = 2
    MAX_VALUE: float = 1e10  # Valor máximo absoluto para límites
    MIN_VALUE: float = -1e10  # Valor mínimo absoluto para límites
    MAX_INTERVAL: float = 1e6  # Intervalo máximo entre a y b
    MIN_INTERVAL: float = 1e-6  # Intervalo mínimo entre a y b


@dataclass
class UIConstants:
    """Constantes para la interfaz de usuario"""
    WINDOW_WIDTH: int = 1400
    WINDOW_HEIGHT: int = 900
    MIN_WINDOW_WIDTH: int = 1200
    MIN_WINDOW_HEIGHT: int = 800
    DEFAULT_FONT_SIZE: int = 12
    TITLE_FONT_SIZE: int = 20
    BUTTON_HEIGHT: int = 35
    ENTRY_HEIGHT: int = 30
    TEXTBOX_HEIGHT: int = 200
    SCROLLABLE_FRAME_HEIGHT: int = 600


@dataclass
class PlotConstants:
    """Constantes para gráficos"""
    FIGURE_WIDTH: int = 10
    FIGURE_HEIGHT: int = 6
    DPI: int = 100
    LINE_WIDTH: float = 2.0
    MARKER_SIZE: float = 6.0
    GRID_ALPHA: float = 0.3
    LEGEND_FONTSIZE: int = 10


@dataclass
class ColorConstants:
    """Constantes de colores para la interfaz"""
    PRIMARY: str = "#1f538d"
    SECONDARY: str = "#2b2b2b"
    SUCCESS: str = "#28a745"
    WARNING: str = "#ffc107"
    ERROR: str = "#dc3545"
    INFO: str = "#17a2b8"
    TEXT_LIGHT: str = "#ffffff"
    TEXT_DARK: str = "#000000"


# Instancias de constantes
VALIDATION = ValidationConstants()
UI = UIConstants()
PLOT = PlotConstants()
COLORS = ColorConstants()

# Mensajes de error amigables
ERROR_MESSAGES = {
    ValidationErrorCodes.EMPTY_FIELD: "Este campo no puede estar vacío. Por favor ingrese un valor.",
    ValidationErrorCodes.INVALID_NUMBER: "El valor ingresado no es un número válido. Use solo dígitos y puntos decimales.",
    ValidationErrorCodes.INVALID_FUNCTION: "La función contiene errores de sintaxis. Verifique los operadores y paréntesis.",
    ValidationErrorCodes.INVALID_RANGE: "El rango especificado no es válido. Verifique que el límite inferior sea menor al superior.",
    ValidationErrorCodes.DIVISION_BY_ZERO: "Se detectó una división por cero. Verifique los parámetros del cálculo.",
    ValidationErrorCodes.CONVERGENCE_FAILED: "El método no convergió en el número máximo de iteraciones. Intente con diferentes parámetros.",
}

# Mensajes de éxito
SUCCESS_MESSAGES = {
    "CALCULATION_SUCCESS": "Cálculo completado exitosamente.",
    "VALIDATION_SUCCESS": "Todos los parámetros son válidos.",
    "PLOT_SUCCESS": "Gráfico generado correctamente.",
}

# Configuraciones por defecto para diferentes métodos
DEFAULT_CONFIGS = {
    "root_finding": {
        "tolerance": VALIDATION.DEFAULT_TOLERANCE,
        "max_iterations": VALIDATION.MAX_ITERATIONS,
        "method": "bisection"
    },
    "integration": {
        "tolerance": VALIDATION.DEFAULT_TOLERANCE,
        "subdivisions": 10,
        "method": "trapezoid"
    },
    "ode_solver": {
        "tolerance": VALIDATION.DEFAULT_TOLERANCE,
        "step_size": VALIDATION.DEFAULT_STEP_SIZE,
        "max_iterations": VALIDATION.MAX_ITERATIONS,
        "method": "euler"
    },
    "finite_differences": {
        "step_size": VALIDATION.DEFAULT_STEP_SIZE,
        "method": "central"
    }
}

# Funciones matemáticas permitidas
ALLOWED_FUNCTIONS = {
    # Funciones trigonométricas
    "sin": "np.sin", "cos": "np.cos", "tan": "np.tan",
    "asin": "np.arcsin", "acos": "np.arccos", "atan": "np.arctan",
    "sinh": "np.sinh", "cosh": "np.cosh", "tanh": "np.tanh",

    # Funciones exponenciales y logarítmicas
    "exp": "np.exp", "log": "np.log", "log10": "np.log10",
    "sqrt": "np.sqrt", "pow": "np.power",

    # Otras funciones
    "abs": "abs", "pi": "np.pi", "e": "np.e",
}

# Caracteres permitidos en expresiones
ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.,()[]{}+-*/^=<>!&| ")

# Configuración de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S"
}
