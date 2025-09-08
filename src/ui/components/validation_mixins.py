"""
Mixins avanzados para validación en tiempo real y funcionalidades reutilizables.

Este módulo extiende los mixins existentes con validación en tiempo real,
feedback visual y validadores especializados.
"""

import customtkinter as ctk
import re
from typing import Dict, Any, Optional, Callable, List
from enum import Enum

from .constants import VALIDATION, ALLOWED_FUNCTIONS, ALLOWED_CHARS, ValidationErrorCodes
from .error_handler import handle_validation_error


class ValidationState(Enum):
    """Estados posibles de validación"""
    VALID = "valid"
    INVALID = "invalid"
    EMPTY = "empty"
    PENDING = "pending"


class RealTimeValidationMixin:
    """
    Mixin para validación en tiempo real de entradas de usuario.
    Proporciona feedback visual inmediato y validación automática.
    """

    def __init__(self):
        self._validation_states = {}
        self._validation_callbacks = {}
        self._field_validators = {}

    def setup_realtime_validation(self, entries: Dict[str, ctk.CTkEntry],
                                 validators: Dict[str, Callable[[str], tuple[bool, str]]]) -> None:
        """
        Configura validación en tiempo real para múltiples campos.

        Args:
            entries: Diccionario de campos de entrada
            validators: Diccionario de funciones validadoras por campo
        """
        self._field_validators = validators

        for field_name, entry in entries.items():
            if field_name in validators:
                # Estado inicial
                self._validation_states[field_name] = ValidationState.EMPTY

                # Configurar callback de validación
                entry.bind("<KeyRelease>", lambda e, fn=field_name: self._validate_field_realtime(fn))
                entry.bind("<FocusOut>", lambda e, fn=field_name: self._validate_field_realtime(fn))

                # Configurar colores iniciales
                self._update_field_appearance(entry, ValidationState.EMPTY)

    def _validate_field_realtime(self, field_name: str) -> None:
        """
        Valida un campo en tiempo real y actualiza su apariencia.
        """
        if field_name not in self._field_validators:
            return

        entry = getattr(self, 'entries', {}).get(field_name)
        if not entry:
            return

        value = entry.get().strip()
        validator = self._field_validators[field_name]

        # Ejecutar validación
        is_valid, error_message = validator(value)

        # Determinar estado
        if not value:
            state = ValidationState.EMPTY
        elif is_valid:
            state = ValidationState.VALID
        else:
            state = ValidationState.INVALID

        # Actualizar estado y apariencia
        self._validation_states[field_name] = state
        self._update_field_appearance(entry, state)

        # Mostrar/ocultar mensaje de error
        self._update_validation_feedback(field_name, error_message if not is_valid and value else "")

    def _update_field_appearance(self, entry: ctk.CTkEntry, state: ValidationState) -> None:
        """
        Actualiza la apariencia visual del campo según su estado de validación.
        """
        if state == ValidationState.VALID:
            entry.configure(border_color="#28a745", border_width=2)  # Verde
        elif state == ValidationState.INVALID:
            entry.configure(border_color="#dc3545", border_width=2)  # Rojo
        elif state == ValidationState.EMPTY:
            entry.configure(border_color="#6c757d", border_width=1)  # Gris
        else:  # PENDING
            entry.configure(border_color="#ffc107", border_width=1)  # Amarillo

    def _update_validation_feedback(self, field_name: str, message: str) -> None:
        """
        Actualiza el feedback de validación para un campo.
        """
        # Buscar label de feedback existente o crear uno
        feedback_label_name = f"{field_name}_feedback"
        feedback_label = getattr(self, feedback_label_name, None)

        if message and not feedback_label:
            # Crear label de feedback si no existe
            parent_frame = self.content_frame  # Asumiendo que está disponible
            feedback_label = ctk.CTkLabel(
                parent_frame,
                text=message,
                text_color="#dc3545",
                font=ctk.CTkFont(size=10)
            )
            setattr(self, feedback_label_name, feedback_label)
            # Aquí se necesitaría lógica para posicionar el label correctamente

        if feedback_label:
            if message:
                feedback_label.configure(text=message)
                feedback_label.pack()  # O grid, dependiendo del layout
            else:
                feedback_label.pack_forget()

    def is_form_valid(self) -> tuple[bool, Dict[str, str]]:
        """
        Verifica si todo el formulario es válido.

        Returns:
            Tupla (is_valid, error_messages_dict)
        """
        errors = {}
        all_valid = True

        for field_name, state in self._validation_states.items():
            if state == ValidationState.INVALID:
                all_valid = False
                entry = getattr(self, 'entries', {}).get(field_name)
                if entry:
                    validator = self._field_validators.get(field_name)
                    if validator:
                        is_valid, error_msg = validator(entry.get().strip())
                        if not is_valid:
                            errors[field_name] = error_msg
            elif state == ValidationState.EMPTY:
                # Campos requeridos no pueden estar vacíos
                all_valid = False
                errors[field_name] = "Este campo es requerido"

        return all_valid, errors

    def get_validated_values(self) -> Dict[str, Any]:
        """
        Obtiene los valores validados del formulario.

        Returns:
            Diccionario con valores convertidos apropiadamente
        """
        values = {}

        for field_name, entry in getattr(self, 'entries', {}).items():
            value_str = entry.get().strip()
            if value_str:
                # Intentar conversión automática
                try:
                    if '.' in value_str or 'e' in value_str.lower():
                        values[field_name] = float(value_str)
                    else:
                        values[field_name] = int(value_str)
                except ValueError:
                    values[field_name] = value_str

        return values


    def setup_validation_for_tab(self, entries: Dict[str, ctk.CTkEntry],
                                validation_config: Dict[str, Dict[str, Any]]) -> None:
        """
        Configura validación para una pestaña completa.

        Args:
            entries: Diccionario de campos de entrada
            validation_config: Configuración de validación por campo
        """
        # Guardar referencia a los entries
        self.entries = entries

        # Crear validadores basados en la configuración
        validators = {}
        for field_name, config in validation_config.items():
            validator_type = config.get("type", "text")
            params = config.get("params", {})

            if validator_type == "function":
                validators[field_name] = self._create_function_validator()
            elif validator_type == "numeric":
                validators[field_name] = self._create_numeric_validator(params)
            elif validator_type == "integer":
                validators[field_name] = self._create_integer_validator(params)
            elif validator_type == "tolerance":
                validators[field_name] = self._create_tolerance_validator()
            else:
                validators[field_name] = self._create_text_validator()

        # Configurar validación en tiempo real
        self.setup_realtime_validation(entries, validators)

    def _create_function_validator(self) -> Callable[[str], tuple[bool, str]]:
        """Crea validador para funciones matemáticas."""
        return lambda value: self.validate_function(value)

    def _create_numeric_validator(self, params: Dict[str, Any]) -> Callable[[str], tuple[bool, str]]:
        """Crea validador para números con parámetros."""
        min_val = params.get("min_val")
        max_val = params.get("max_val")
        return lambda value: self.validate_numeric(value, min_val, max_val)

    def _create_integer_validator(self, params: Dict[str, Any]) -> Callable[[str], tuple[bool, str]]:
        """Crea validador para enteros con parámetros."""
        min_val = params.get("min_val")
        max_val = params.get("max_val")
        return lambda value: self.validate_integer(value, min_val, max_val)

    def _create_tolerance_validator(self) -> Callable[[str], tuple[bool, str]]:
        """Crea validador para tolerancias."""
        return lambda value: self.validate_tolerance(value)

    def _create_text_validator(self) -> Callable[[str], tuple[bool, str]]:
        """Crea validador básico para texto."""
        return lambda value: (bool(value.strip()), "El campo no puede estar vacío" if not value.strip() else "")

    def validate_range(self, start_value: str, end_value: str,
                      start_label: str = "límite inferior",
                      end_label: str = "límite superior") -> tuple[bool, str]:
        """
        Valida que el rango sea correcto (inicio < fin).

        Args:
            start_value: Valor del límite inferior
            end_value: Valor del límite superior
            start_label: Etiqueta para el límite inferior
            end_label: Etiqueta para el límite superior

        Returns:
            Tupla (is_valid, error_message)
        """
        try:
            start = float(start_value)
            end = float(end_value)

            if start >= end:
                return False, f"El {start_label} debe ser menor que el {end_label}"

            return True, ""
        except ValueError:
            return False, "Los valores del rango deben ser números válidos"


class AdvancedValidationMixin:
    """
    Mixin con validadores especializados para diferentes tipos de entrada.
    """

    @staticmethod
    def validate_numeric(value: str, min_val: Optional[float] = None,
                        max_val: Optional[float] = None,
                        allow_zero: bool = True) -> tuple[bool, str]:
        """
        Valida entrada numérica con rangos opcionales.
        """
        if not value.strip():
            return False, "El campo no puede estar vacío"

        try:
            num_value = float(value)

            if not allow_zero and abs(num_value) < 1e-15:
                return False, "El valor no puede ser cero"

            if min_val is not None and num_value < min_val:
                return False, f"El valor debe ser mayor o igual a {min_val}"

            if max_val is not None and num_value > max_val:
                return False, f"El valor debe ser menor o igual a {max_val}"

            return True, ""

        except ValueError:
            return False, "Debe ser un número válido"

    @staticmethod
    def validate_integer(value: str, min_val: Optional[int] = None,
                        max_val: Optional[int] = None) -> tuple[bool, str]:
        """
        Valida entrada entera.
        """
        if not value.strip():
            return False, "El campo no puede estar vacío"

        try:
            int_value = int(float(value))  # Permite notación científica

            if min_val is not None and int_value < min_val:
                return False, f"El valor debe ser mayor o igual a {min_val}"

            if max_val is not None and int_value > max_val:
                return False, f"El valor debe ser menor o igual a {max_val}"

            return True, ""

        except ValueError:
            return False, "Debe ser un número entero válido"

    @staticmethod
    def validate_function(value: str) -> tuple[bool, str]:
        """
        Valida expresión matemática.
        """
        if not value.strip():
            return False, "La función no puede estar vacía"

        # Verificar caracteres permitidos
        for char in value:
            if char not in ALLOWED_CHARS:
                return False, f"Carácter no permitido: '{char}'"

        # Verificar sintaxis básica
        try:
            # Reemplazos comunes
            test_expr = value.replace('^', '**').replace('sen', 'sin')

            # Verificar paréntesis balanceados
            if test_expr.count('(') != test_expr.count(')'):
                return False, "Los paréntesis no están balanceados"

            # Verificar que no haya operadores consecutivos
            if re.search(r'[+\-*/]{2,}', test_expr.replace('**', '')):
                return False, "Operadores consecutivos no permitidos"

            return True, ""

        except Exception:
            return False, "Expresión matemática inválida"

    @staticmethod
    def validate_range(lower: str, upper: str) -> tuple[bool, str]:
        """
        Valida que un rango sea válido (lower < upper).
        """
        lower_valid, lower_msg = AdvancedValidationMixin.validate_numeric(lower)
        if not lower_valid:
            return False, f"Límite inferior: {lower_msg}"

        upper_valid, upper_msg = AdvancedValidationMixin.validate_numeric(upper)
        if not upper_valid:
            return False, f"Límite superior: {upper_msg}"

        lower_val = float(lower)
        upper_val = float(upper)

        if lower_val >= upper_val:
            return False, "El límite inferior debe ser menor al superior"

        return True, ""

    @staticmethod
    def validate_positive_number(value: str) -> tuple[bool, str]:
        """
        Valida número positivo.
        """
        return AdvancedValidationMixin.validate_numeric(value, min_val=0, allow_zero=False)

    @staticmethod
    def validate_tolerance(value: str) -> tuple[bool, str]:
        """
        Valida tolerancia numérica.
        """
        return AdvancedValidationMixin.validate_numeric(
            value,
            min_val=VALIDATION.MIN_TOLERANCE,
            max_val=VALIDATION.MAX_TOLERANCE,
            allow_zero=False
        )


class InputValidationMixin(RealTimeValidationMixin, AdvancedValidationMixin):
    """
    Mixin combinado que incluye validación en tiempo real y validadores avanzados.
    """

    def __init__(self):
        """Inicializar el mixin combinado."""
        RealTimeValidationMixin.__init__(self)
        # AdvancedValidationMixin no tiene __init__

    def setup_validation_for_tab(self, entries: Dict[str, ctk.CTkEntry],
                                validation_config: Dict[str, Dict]) -> None:
        """
        Configura validación completa para una pestaña.

        Args:
            entries: Campos de entrada
            validation_config: Configuración de validación por campo
        """
        # Crear validadores basados en configuración
        validators = {}
        for field_name, config in validation_config.items():
            validator_type = config.get('type', 'text')
            validator_params = config.get('params', {})

            if validator_type == 'numeric':
                validators[field_name] = lambda v, p=validator_params: self.validate_numeric(v, **p)
            elif validator_type == 'integer':
                validators[field_name] = lambda v, p=validator_params: self.validate_integer(v, **p)
            elif validator_type == 'function':
                validators[field_name] = self.validate_function
            elif validator_type == 'positive':
                validators[field_name] = self.validate_positive_number
            elif validator_type == 'tolerance':
                validators[field_name] = self.validate_tolerance
            else:
                validators[field_name] = lambda v: (bool(v.strip()), "Campo requerido" if not v.strip() else "")

        # Configurar validación en tiempo real
        self.setup_realtime_validation(entries, validators)

    def validate_range(self, start_value: str, end_value: str,
                      start_label: str = "límite inferior",
                      end_label: str = "límite superior") -> tuple[bool, str]:
        """
        Valida que el rango sea correcto (inicio < fin).

        Args:
            start_value: Valor del límite inferior
            end_value: Valor del límite superior
            start_label: Etiqueta para el límite inferior
            end_label: Etiqueta para el límite superior

        Returns:
            Tupla (is_valid, error_message)
        """
        try:
            start = float(start_value)
            end = float(end_value)

            if start >= end:
                return False, f"El {start_label} debe ser menor que el {end_label}"

            return True, ""
        except ValueError:
            return False, "Los valores del rango deben ser números válidos"
