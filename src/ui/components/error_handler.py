"""
Gestor centralizado de errores para la interfaz de usuario.

Este módulo proporciona un sistema unificado para manejar errores,
mostrar mensajes amigables al usuario y gestionar recuperación de errores.
"""

import customtkinter as ctk
import logging
from typing import Optional, Callable, Any
from enum import Enum

from .constants import ERROR_MESSAGES, SUCCESS_MESSAGES, ErrorSeverity, ValidationErrorCodes, COLORS

logger = logging.getLogger(__name__)


class ErrorHandler:
    """
    Gestor centralizado de errores y mensajes de usuario.
    Implementa el patrón Singleton para consistencia global.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._error_callbacks = []
            self._success_callbacks = []

    def register_error_callback(self, callback: Callable[[str, ErrorSeverity], None]):
        """Registra un callback para manejar errores"""
        self._error_callbacks.append(callback)

    def register_success_callback(self, callback: Callable[[str], None]):
        """Registra un callback para manejar mensajes de éxito"""
        self._success_callbacks.append(callback)

    def handle_error(self, error: Exception, context: str = "",
                    severity: ErrorSeverity = ErrorSeverity.ERROR,
                    show_dialog: bool = True) -> None:
        """
        Maneja errores de manera centralizada.

        Args:
            error: La excepción que ocurrió
            context: Contexto donde ocurrió el error
            severity: Severidad del error
            show_dialog: Si mostrar diálogo al usuario
        """
        # Log del error técnico
        logger.error(f"Error en {context}: {str(error)}", exc_info=True)

        # Convertir a mensaje amigable
        user_message = self._convert_to_user_message(error, context)

        # Notificar callbacks
        for callback in self._error_callbacks:
            try:
                callback(user_message, severity)
            except Exception as e:
                logger.error(f"Error en callback: {e}")

        # Mostrar diálogo si es necesario
        if show_dialog:
            self._show_error_dialog(user_message, severity)

    def handle_validation_error(self, error_code: ValidationErrorCodes,
                               field_name: str = "", show_dialog: bool = True) -> str:
        """
        Maneja errores de validación específicos.

        Args:
            error_code: Código del error de validación
            field_name: Nombre del campo que falló
            show_dialog: Si mostrar diálogo

        Returns:
            Mensaje de error para el usuario
        """
        user_message = ERROR_MESSAGES.get(error_code, "Error de validación desconocido")

        if field_name:
            user_message = f"Campo '{field_name}': {user_message}"

        if show_dialog:
            self._show_error_dialog(user_message, ErrorSeverity.WARNING)

        return user_message

    def handle_success(self, message_key: str, custom_message: str = "",
                      show_dialog: bool = False) -> None:
        """
        Maneja mensajes de éxito.

        Args:
            message_key: Clave del mensaje predefinido
            custom_message: Mensaje personalizado (opcional)
            show_dialog: Si mostrar diálogo de éxito
        """
        message = custom_message or SUCCESS_MESSAGES.get(message_key, "Operación exitosa")

        # Notificar callbacks
        for callback in self._success_callbacks:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error en callback de éxito: {e}")

        if show_dialog:
            self._show_success_dialog(message)

    def _convert_to_user_message(self, error: Exception, context: str) -> str:
        """
        Convierte excepciones técnicas en mensajes amigables para el usuario.
        """
        error_str = str(error).lower()

        # Mapeo de errores técnicos a mensajes amigables
        error_mappings = {
            "division by zero": "Se intentó dividir por cero. Verifique los parámetros.",
            "math domain error": "Error matemático: verifique que la función esté definida en el dominio.",
            "invalid syntax": "La expresión matemática contiene errores de sintaxis.",
            "nameerror": "Variable o función no reconocida en la expresión.",
            "overflow": "Los valores son demasiado grandes para calcularse con precisión.",
            "underflow": "Los valores son demasiado pequeños para calcularse con precisión.",
            "convergence": "El método no pudo converger con los parámetros dados.",
            "max iterations": "Se alcanzó el número máximo de iteraciones sin convergencia.",
        }

        for technical_term, user_message in error_mappings.items():
            if technical_term in error_str:
                return user_message

        # Mensaje genérico si no hay mapeo específico
        context_msg = f" en {context}" if context else ""
        return f"Ocurrió un error{context_msg}. Por favor verifique los parámetros e intente nuevamente."

    def _show_error_dialog(self, message: str, severity: ErrorSeverity) -> None:
        """
        Muestra un diálogo de error con el mensaje apropiado.
        """
        # Crear ventana de error
        error_window = ctk.CTkToplevel()
        error_window.title(self._get_severity_title(severity))
        error_window.geometry("500x200")
        error_window.grab_set()

        # Configurar colores según severidad
        color = self._get_severity_color(severity)

        # Mensaje de error
        error_label = ctk.CTkLabel(
            error_window,
            text=message,
            wraplength=450,
            font=ctk.CTkFont(size=12),
            text_color=color
        )
        error_label.pack(pady=20, padx=20)

        # Botón de cerrar
        close_btn = ctk.CTkButton(
            error_window,
            text="Entendido",
            command=error_window.destroy,
            fg_color=color
        )
        close_btn.pack(pady=10)

    def _show_success_dialog(self, message: str) -> None:
        """
        Muestra un diálogo de éxito.
        """
        success_window = ctk.CTkToplevel()
        success_window.title("Éxito")
        success_window.geometry("400x150")
        success_window.grab_set()

        success_label = ctk.CTkLabel(
            success_window,
            text=message,
            wraplength=350,
            font=ctk.CTkFont(size=12),
            text_color=COLORS.SUCCESS
        )
        success_label.pack(pady=20, padx=20)

        close_btn = ctk.CTkButton(
            success_window,
            text="OK",
            command=success_window.destroy,
            fg_color=COLORS.SUCCESS
        )
        close_btn.pack(pady=10)

    def _get_severity_title(self, severity: ErrorSeverity) -> str:
        """Obtiene el título apropiado según la severidad"""
        titles = {
            ErrorSeverity.INFO: "Información",
            ErrorSeverity.WARNING: "Advertencia",
            ErrorSeverity.ERROR: "Error",
            ErrorSeverity.CRITICAL: "Error Crítico"
        }
        return titles.get(severity, "Mensaje")

    def _get_severity_color(self, severity: ErrorSeverity) -> str:
        """Obtiene el color apropiado según la severidad"""
        colors = {
            ErrorSeverity.INFO: COLORS.INFO,
            ErrorSeverity.WARNING: COLORS.WARNING,
            ErrorSeverity.ERROR: COLORS.ERROR,
            ErrorSeverity.CRITICAL: COLORS.ERROR
        }
        return colors.get(severity, COLORS.ERROR)


# Instancia global del gestor de errores
error_handler = ErrorHandler()


def handle_error(error: Exception, context: str = "",
                severity: ErrorSeverity = ErrorSeverity.ERROR,
                show_dialog: bool = True) -> None:
    """
    Función de conveniencia para manejar errores globalmente.
    """
    error_handler.handle_error(error, context, severity, show_dialog)


def handle_validation_error(error_code: ValidationErrorCodes,
                           field_name: str = "", show_dialog: bool = True) -> str:
    """
    Función de conveniencia para manejar errores de validación.
    """
    return error_handler.handle_validation_error(error_code, field_name, show_dialog)


def handle_success(message_key: str, custom_message: str = "",
                  show_dialog: bool = False) -> None:
    """
    Función de conveniencia para manejar mensajes de éxito.
    """
    error_handler.handle_success(message_key, custom_message, show_dialog)
