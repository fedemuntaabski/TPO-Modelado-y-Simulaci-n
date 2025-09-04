"""
Tests para utilidades y parsers
Pruebas unitarias para funciones de utilidad y parsing
"""

import unittest
import numpy as np
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.function_parser import FunctionParser
from utils.validators import InputValidator


class TestFunctionParser(unittest.TestCase):
    """Tests para el parser de funciones"""

    def setUp(self):
        """Configurar parser para tests"""
        self.parser = FunctionParser()

    def test_parse_simple_function(self):
        """Test parsing de función simple"""
        expr = "x**2 + 2*x + 1"
        func = self.parser.parse_function(expr)

        # Testear en algunos puntos
        self.assertAlmostEqual(func(0), 1)
        self.assertAlmostEqual(func(1), 4)
        self.assertAlmostEqual(func(2), 9)

    def test_parse_trigonometric_function(self):
        """Test parsing de función trigonométrica"""
        expr = "sin(x) + cos(x)"
        func = self.parser.parse_function(expr)

        # Testear en x = π/4
        x = np.pi/4
        result = func(x)
        expected = np.sin(x) + np.cos(x)
        self.assertAlmostEqual(result, expected, places=5)

    def test_parse_complex_function(self):
        """Test parsing de función compleja"""
        expr = "exp(-x**2) * sin(2*x)"
        func = self.parser.parse_function(expr)

        x = 1.0
        result = func(x)
        expected = np.exp(-x**2) * np.sin(2*x)
        self.assertAlmostEqual(result, expected, places=5)

    def test_invalid_function(self):
        """Test manejo de funciones inválidas"""
        expr = "x**2 + invalid_function(x)"
        # El parser debería manejar esto sin excepciones
        try:
            func = self.parser.parse_function(expr)
            # Si llega aquí, verificar que se puede llamar
            result = func(1.0)
        except Exception:
            # Es aceptable que falle
            pass


class TestValidators(unittest.TestCase):
    """Tests para validadores"""

    def setUp(self):
        """Configurar validador para tests"""
        self.validator = InputValidator()

    def test_validate_numeric_input(self):
        """Test validación de entrada numérica"""
        # Valores válidos
        valid, msg, val = InputValidator.validate_positive_float("123")
        self.assertTrue(valid)
        self.assertEqual(val, 123.0)

        valid, msg, val = InputValidator.validate_positive_float("123.45")
        self.assertTrue(valid)
        self.assertAlmostEqual(val, 123.45)

        # Valores inválidos
        valid, msg, val = InputValidator.validate_positive_float("abc")
        self.assertFalse(valid)

        valid, msg, val = InputValidator.validate_positive_float("")
        self.assertFalse(valid)

    def test_validate_interval(self):
        """Test validación de intervalos"""
        # Intervalos válidos
        valid, msg, a, b = InputValidator.validate_interval(-1, 1)
        self.assertTrue(valid)

        valid, msg, a, b = InputValidator.validate_interval(0, 10)
        self.assertTrue(valid)

        # Intervalos inválidos
        valid, msg, a, b = InputValidator.validate_interval(1, -1)
        self.assertFalse(valid)  # a > b

        valid, msg, a, b = InputValidator.validate_interval(0, 0)
        self.assertFalse(valid)  # a == b

    def test_validate_tolerance(self):
        """Test validación de tolerancia"""
        # Tolerancias válidas
        valid, msg, val = InputValidator.validate_positive_float("1e-6", 1e-10, 1)
        self.assertTrue(valid)

        valid, msg, val = InputValidator.validate_positive_float("0.001", 1e-10, 1)
        self.assertTrue(valid)

        # Tolerancias inválidas
        valid, msg, val = InputValidator.validate_positive_float("0", 1e-10, 1)
        self.assertFalse(valid)  # cero

        valid, msg, val = InputValidator.validate_positive_float("-1e-6", 1e-10, 1)
        self.assertFalse(valid)  # negativa

    def test_validate_function_syntax(self):
        """Test validación de sintaxis de funciones"""
        # Funciones válidas (simples)
        valid, msg = InputValidator.validate_function("x")
        self.assertTrue(valid)

        valid, msg = InputValidator.validate_function("x+1")
        self.assertTrue(valid)

        # Funciones inválidas
        valid, msg = InputValidator.validate_function("")
        self.assertFalse(valid)

        valid, msg = InputValidator.validate_function("x++")
        self.assertFalse(valid)


class TestIntegrationTests(unittest.TestCase):
    """Tests de integración entre módulos"""

    def test_parser_validator_integration(self):
        """Test integración entre parser y validador"""
        parser = FunctionParser()
        validator = InputValidator()

        expressions = [
            "x",
            "x+1",
            "x*2",
            "x/2"
        ]

        for expr in expressions:
            # Validar sintaxis
            valid, msg = InputValidator.validate_function(expr)
            if valid:  # Solo probar parsing si la validación pasa
                # Parsear función
                func = parser.parse_function(expr)

                # Verificar que se puede evaluar
                result = func(1.0)
                self.assertIsInstance(result, (int, float, np.floating))

    def test_numerical_methods_integration(self):
        """Test integración entre métodos numéricos"""
        from core.numerical_integration import NumericalIntegration
        from utils.function_parser import FunctionParser

        parser = FunctionParser()

        # Función a integrar: ∫ sin(x) dx de 0 a π = 2
        expr = "sin(x)"
        func = parser.parse_function(expr)

        a, b = 0, np.pi
        n = 1000

        # Usar diferentes métodos
        trap_result = NumericalIntegration.trapezoid(func, a, b, n)
        simp_result = NumericalIntegration.simpson_13(func, a, b, n)

        # Ambos deberían estar cerca de 2
        self.assertAlmostEqual(trap_result, 2.0, places=3)
        self.assertAlmostEqual(simp_result, 2.0, places=4)


if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.INFO)

    # Ejecutar tests
    unittest.main(verbosity=2)
