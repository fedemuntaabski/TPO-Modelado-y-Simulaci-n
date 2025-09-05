"""
Unit tests for utils/validators.py
"""

import pytest
from utils.validators import InputValidator


class TestInputValidator:
    """Test cases for InputValidator class"""

    def test_validate_function_valid(self):
        """Test valid function expressions"""
        valid_expressions = [
            "x^2 + 1",
            "sin(x)",
            "x + y",
            "2*x - 3",
            "(x + 1)/(x - 1)"
        ]
        for expr in valid_expressions:
            is_valid, msg = InputValidator.validate_function(expr)
            assert is_valid, f"Expression '{expr}' should be valid: {msg}"

    def test_validate_function_invalid(self):
        """Test invalid function expressions"""
        invalid_expressions = [
            ("", "La expresión no puede estar vacía"),
            ("x +", "La expresión no puede terminar con un operador"),
            ("*x", "La expresión no puede empezar con ese operador"),
            ("x(", "Los paréntesis no están balanceados"),
            ("x@2", "La expresión contiene caracteres no válidos")
        ]
        for expr, expected_msg in invalid_expressions:
            is_valid, msg = InputValidator.validate_function(expr)
            assert not is_valid, f"Expression '{expr}' should be invalid"
            assert expected_msg in msg

    def test_validate_positive_integer_valid(self):
        """Test positive integer validation"""
        assert InputValidator.validate_positive_integer("5") == (True, "", 5)
        assert InputValidator.validate_positive_integer(10) == (True, "", 10)

    def test_validate_positive_integer_invalid(self):
        """Test invalid positive integer validation"""
        assert InputValidator.validate_positive_integer("-3") == (False, "Debe ser un número positivo", 0)
        assert InputValidator.validate_positive_integer("abc") == (False, "Debe ser un número entero", 0)
        assert InputValidator.validate_positive_integer("0") == (False, "Debe ser un número positivo", 0)
