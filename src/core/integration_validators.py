"""
Validadores específicos para integración numérica.

Implementa validaciones para intervalos, subdivisiones y restricciones
específicas de métodos de integración Newton-Cotes.
"""

import math
from typing import Union, Tuple
import logging

logger = logging.getLogger(__name__)


class IntegrationValidationError(Exception):
    """Excepción para errores de validación en integración"""
    pass


class IntegrationValidator:
    """Validador para parámetros de integración numérica"""
    
    @staticmethod
    def validate_interval(a: float, b: float) -> None:
        """
        Validar intervalo de integración [a, b]
        
        Args:
            a: Límite inferior
            b: Límite superior
            
        Raises:
            IntegrationValidationError: Si el intervalo no es válido
        """
        # Validar que sean números válidos
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise IntegrationValidationError("Los límites deben ser números")
        
        if math.isnan(a) or math.isnan(b):
            raise IntegrationValidationError("Los límites no pueden ser NaN")
        
        if math.isinf(a) or math.isinf(b):
            raise IntegrationValidationError("Los límites no pueden ser infinitos")
        
        # Validar orden
        if a >= b:
            raise IntegrationValidationError(
                f"El límite inferior ({a}) debe ser menor al superior ({b})"
            )
        
        # Advertir sobre intervalos muy grandes
        if abs(b - a) > 1e6:
            logger.warning(f"Intervalo muy grande: [{a}, {b}]. Esto puede afectar la precisión.")
    
    @staticmethod
    def validate_subdivisions(n: int, min_n: int = 1, max_n: int = 1_000_000) -> None:
        """
        Validar número de subdivisiones
        
        Args:
            n: Número de subdivisiones
            min_n: Mínimo número permitido
            max_n: Máximo número permitido
            
        Raises:
            IntegrationValidationError: Si n no es válido
        """
        if not isinstance(n, int):
            raise IntegrationValidationError("El número de subdivisiones debe ser entero")
        
        if n < min_n:
            raise IntegrationValidationError(
                f"El número de subdivisiones debe ser al menos {min_n}"
            )
        
        if n > max_n:
            raise IntegrationValidationError(
                f"El número de subdivisiones no puede exceder {max_n}"
            )
        
        # Advertir sobre valores muy grandes
        if n > 100_000:
            logger.warning(f"n={n} es muy grande. El cálculo puede ser lento.")
    
    @staticmethod
    def validate_simpson_13_n(n: int) -> None:
        """
        Validar que n sea par para Simpson 1/3
        
        Args:
            n: Número de subdivisiones
            
        Raises:
            IntegrationValidationError: Si n no es par
        """
        IntegrationValidator.validate_subdivisions(n)
        
        if n % 2 != 0:
            raise IntegrationValidationError(
                f"Simpson 1/3 requiere n par. Recibido: n={n}. "
                f"Sugerencia: use n={n+1} o n={n-1 if n > 1 else 2}"
            )
    
    @staticmethod
    def validate_simpson_38_n(n: int) -> None:
        """
        Validar que n sea múltiplo de 3 para Simpson 3/8
        
        Args:
            n: Número de subdivisiones
            
        Raises:
            IntegrationValidationError: Si n no es múltiplo de 3
        """
        IntegrationValidator.validate_subdivisions(n)
        
        if n % 3 != 0:
            # Sugerir valores cercanos múltiplos de 3
            suggestions = []
            for delta in [-2, -1, 1, 2]:
                candidate = n + delta
                if candidate > 0 and candidate % 3 == 0:
                    suggestions.append(str(candidate))
            
            suggestion_text = f" Sugerencias: {', '.join(suggestions[:3])}" if suggestions else ""
            
            raise IntegrationValidationError(
                f"Simpson 3/8 requiere n múltiplo de 3. Recibido: n={n}.{suggestion_text}"
            )
    
    @staticmethod
    def validate_function_string(func_str: str) -> None:
        """
        Validar string de función básico
        
        Args:
            func_str: String de la función
            
        Raises:
            IntegrationValidationError: Si el string no es válido
        """
        if not isinstance(func_str, str):
            raise IntegrationValidationError("La función debe ser un string")
        
        if not func_str.strip():
            raise IntegrationValidationError("La función no puede estar vacía")
        
        # Validaciones básicas de seguridad
        dangerous_keywords = ['import', 'exec', 'eval', '__', 'open', 'file']
        func_lower = func_str.lower()
        
        for keyword in dangerous_keywords:
            if keyword in func_lower:
                raise IntegrationValidationError(
                    f"Palabra clave no permitida en función: {keyword}"
                )
    
    @staticmethod
    def validate_method_name(method: str, available_methods: list) -> None:
        """
        Validar nombre de método de integración
        
        Args:
            method: Nombre del método
            available_methods: Lista de métodos disponibles
            
        Raises:
            IntegrationValidationError: Si el método no es válido
        """
        if not isinstance(method, str):
            raise IntegrationValidationError("El método debe ser un string")
        
        if method not in available_methods:
            raise IntegrationValidationError(
                f"Método '{method}' no disponible. "
                f"Métodos disponibles: {', '.join(available_methods)}"
            )
    
    @staticmethod
    def validate_integration_parameters(func_str: str, a: float, b: float, 
                                      method: str, n: int = None,
                                      available_methods: list = None) -> dict:
        """
        Validar todos los parámetros de integración de una vez
        
        Args:
            func_str: String de la función
            a: Límite inferior
            b: Límite superior  
            method: Método de integración
            n: Número de subdivisiones (opcional para métodos simples)
            available_methods: Lista de métodos disponibles
            
        Returns:
            Dict con información de validación
            
        Raises:
            IntegrationValidationError: Si algún parámetro no es válido
        """
        validation_info = {
            'function': func_str,
            'interval': [a, b],
            'method': method,
            'subdivisions': n,
            'warnings': [],
            'validations_passed': []
        }
        
        try:
            # Validar función
            IntegrationValidator.validate_function_string(func_str)
            validation_info['validations_passed'].append('function_string')
            
            # Validar intervalo
            IntegrationValidator.validate_interval(a, b)
            validation_info['validations_passed'].append('interval')
            
            # Validar método
            if available_methods:
                IntegrationValidator.validate_method_name(method, available_methods)
                validation_info['validations_passed'].append('method')
            
            # Validar subdivisiones según el método
            if n is not None:
                if 'simpson_13' in method:
                    IntegrationValidator.validate_simpson_13_n(n)
                    validation_info['validations_passed'].append('simpson_13_n')
                elif 'simpson_38' in method:
                    IntegrationValidator.validate_simpson_38_n(n)
                    validation_info['validations_passed'].append('simpson_38_n')
                else:
                    IntegrationValidator.validate_subdivisions(n)
                    validation_info['validations_passed'].append('subdivisions')
            
            # Validaciones adicionales según el método
            if 'composite' in method and n is None:
                raise IntegrationValidationError(
                    f"Método compuesto '{method}' requiere especificar n (subdivisiones)"
                )
            
            validation_info['is_valid'] = True
            validation_info['message'] = "Todos los parámetros son válidos"
            
        except IntegrationValidationError as e:
            validation_info['is_valid'] = False
            validation_info['message'] = str(e)
            raise
        
        return validation_info
    
    @staticmethod
    def get_method_requirements(method: str) -> dict:
        """
        Obtener requerimientos específicos de un método
        
        Args:
            method: Nombre del método
            
        Returns:
            Dict con requerimientos del método
        """
        requirements = {
            'requires_n': True,
            'n_constraint': None,
            'min_n': 1,
            'description': '',
            'formula': '',
            'order': ''
        }
        
        if 'simple' in method:
            requirements['requires_n'] = False
            requirements['description'] = 'Método simple (no requiere subdivisiones)'
        
        if 'simpson_13' in method:
            requirements['n_constraint'] = 'par'
            requirements['min_n'] = 2
            requirements['description'] = 'Requiere n par (número par de subdivisiones)'
            requirements['formula'] = 'I ≈ h/3 * [f(a) + 4*Σf(x_impar) + 2*Σf(x_par) + f(b)]'
            requirements['order'] = 'O(h⁴)'
        elif 'simpson_38' in method:
            requirements['n_constraint'] = 'múltiplo de 3'
            requirements['min_n'] = 3
            requirements['description'] = 'Requiere n múltiplo de 3'
            requirements['formula'] = 'I ≈ 3h/8 * [f(a) + 3*Σf(...) + f(b)]'
            requirements['order'] = 'O(h⁴)'
        elif 'trapezoid' in method:
            requirements['formula'] = 'I ≈ h/2 * [f(a) + 2*Σf(xi) + f(b)]'
            requirements['order'] = 'O(h²)'
        elif 'rectangle' in method:
            requirements['formula'] = 'I ≈ h * Σf(xi)'
            requirements['order'] = 'O(h²)'
        
        return requirements


def test_integration_validator():
    """Función de prueba para el validador"""
    validator = IntegrationValidator()
    
    print("=== Pruebas del Validador de Integración ===")
    
    # Pruebas de intervalo
    test_intervals = [
        (0, 1, True),
        (1, 0, False),  # Orden incorrecto
        (float('nan'), 1, False),  # NaN
        (0, float('inf'), False),  # Infinito
    ]
    
    print("\n--- Pruebas de Intervalos ---")
    for a, b, should_pass in test_intervals:
        try:
            validator.validate_interval(a, b)
            result = "✓ VÁLIDO"
            if not should_pass:
                result += " (INESPERADO)"
        except Exception as e:
            result = f"✗ ERROR: {e}"
            if should_pass:
                result += " (INESPERADO)"
        
        print(f"[{a}, {b}] -> {result}")
    
    # Pruebas de Simpson
    print("\n--- Pruebas Simpson 1/3 (n par) ---")
    for n in [2, 4, 6, 1, 3, 5]:
        try:
            validator.validate_simpson_13_n(n)
            print(f"n={n} -> ✓ VÁLIDO")
        except Exception as e:
            print(f"n={n} -> ✗ ERROR: {e}")
    
    print("\n--- Pruebas Simpson 3/8 (n múltiplo de 3) ---")
    for n in [3, 6, 9, 1, 2, 4, 5]:
        try:
            validator.validate_simpson_38_n(n)
            print(f"n={n} -> ✓ VÁLIDO")
        except Exception as e:
            print(f"n={n} -> ✗ ERROR: {e}")


if __name__ == "__main__":
    test_integration_validator()
