"""
Tests para módulos de utilitarios
"""

import sys
import os
import pytest
import numpy as np
import math

# Agregar el directorio principal al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.function_parser import FunctionParser
from utils.validators import InputValidator


class TestFunctionParser:
    """Tests para FunctionParser"""

    def test_normalize_expression_basic(self):
        """Test de normalización básica de expresiones"""
        # Test operadores
        assert FunctionParser.normalize_expression("x^2") == "x**2"
        assert FunctionParser.normalize_expression("x + y") == "x + y"

        # Test funciones trigonométricas
        assert "np.sin" in FunctionParser.normalize_expression("sin(x)")
        assert "np.cos" in FunctionParser.normalize_expression("cos(x)")

        # Test constantes
        assert "np.pi" in FunctionParser.normalize_expression("pi")
        assert "np.e" in FunctionParser.normalize_expression("e")

    def test_normalize_expression_complex(self):
        """Test de normalización de expresiones complejas"""
        expr = "sin(x)^2 + cos(x)^2"
        normalized = FunctionParser.normalize_expression(expr)

        assert "np.sin" in normalized
        assert "np.cos" in normalized
        assert "**2" in normalized

    def test_parse_function_basic(self):
        """Test básico de parseo de funciones"""
        func = FunctionParser.parse_function("x + 1")

        # Test evaluación
        assert func(0) == 1
        assert func(1) == 2
        assert func(-1) == 0

    def test_parse_function_trigonometric(self):
        """Test de funciones trigonométricas"""
        func = FunctionParser.parse_function("sin(x)")

        # Test valores conocidos
        assert abs(func(0) - 0) < 1e-10
        assert abs(func(np.pi/2) - 1) < 1e-10

    def test_parse_function_polynomial(self):
        """Test de funciones polinomiales"""
        func = FunctionParser.parse_function("x^2 + 2*x + 1")

        # (x+1)^2 = x^2 + 2x + 1
        assert abs(func(0) - 1) < 1e-10
        assert abs(func(1) - 4) < 1e-10
        assert abs(func(2) - 9) < 1e-10

    def test_parse_function_error_handling(self):
        """Test de manejo de errores en parseo"""
        func = FunctionParser.parse_function("x + 1")

        # Función válida debe funcionar
        assert func(5) == 6

        # Test con expresión que causa error en evaluación
        func_div = FunctionParser.parse_function("1/x")
        with pytest.raises(ValueError):
            func_div(0)  # División por cero


class TestInputValidator:
    """Tests para InputValidator"""

    def test_validate_function_valid(self):
        """Test de validación de funciones válidas"""
        valid_functions = [
            "x",
            "x + 1",
            "x^2",
            "sin(x)",
            "cos(x) + sin(x)",
            "x^2 + 2*x + 1",
            "(x + 1)^2",
            "exp(x)",
            "ln(x + 1)"
        ]

        for func_str in valid_functions:
            is_valid, error_msg = InputValidator.validate_function(func_str)
            assert is_valid, f"Función válida rechazada: {func_str}, error: {error_msg}"

    def test_validate_function_invalid(self):
        """Test de validación de funciones inválidas"""
        invalid_functions = [
            "",  # Vacío
            "   ",  # Solo espacios
            "x +",  # Termina con operador
            "*x",  # Empieza con operador
            "x + + y",  # Operadores consecutivos
            "(x + 1",  # Paréntesis no balanceados
            "x + @",  # Carácter inválido
        ]

        for func_str in invalid_functions:
            is_valid, error_msg = InputValidator.validate_function(func_str)
            assert not is_valid, f"Función inválida aceptada: {func_str}"

    def test_validate_interval_valid(self):
        """Test de validación de intervalos válidos"""
        test_cases = [
            ("0", "1", 0.0, 1.0),
            ("-1", "1", -1.0, 1.0),
            ("1.5", "2.5", 1.5, 2.5),
        ]

        for a_str, b_str, expected_a, expected_b in test_cases:
            is_valid, error_msg, a_val, b_val = InputValidator.validate_interval(a_str, b_str)
            assert is_valid, f"Intervalo válido rechazado: [{a_str}, {b_str}], error: {error_msg}"
            assert abs(a_val - expected_a) < 1e-10
            assert abs(b_val - expected_b) < 1e-10

    def test_validate_interval_invalid(self):
        """Test de validación de intervalos inválidos"""
        invalid_cases = [
            ("1", "0"),  # a >= b
            ("abc", "1"),  # No numérico
            ("1", "def"),  # No numérico
            ("inf", "1"),  # Infinito
            ("1", "-inf"),  # Infinito negativo
        ]

        for a_str, b_str in invalid_cases:
            is_valid, error_msg, _, _ = InputValidator.validate_interval(a_str, b_str)
            assert not is_valid, f"Intervalo inválido aceptado: [{a_str}, {b_str}]"

    def test_validate_positive_integer_valid(self):
        """Test de validación de enteros positivos válidos"""
        test_cases = [
            ("1", 1),
            ("100", 100),
            (50, 50),  # Entero directo
        ]

        for input_val, expected in test_cases:
            is_valid, error_msg, val = InputValidator.validate_positive_integer(input_val)
            assert is_valid, f"Entero positivo válido rechazado: {input_val}, error: {error_msg}"
            assert val == expected

    def test_validate_positive_integer_invalid(self):
        """Test de validación de enteros positivos inválidos"""
        invalid_cases = [
            "-1",      # Negativo
            "1.5",     # Decimal
            "abc",     # No numérico
            "",        # Vacío
        ]

        for input_val in invalid_cases:
            is_valid, error_msg, _ = InputValidator.validate_positive_integer(input_val)
            assert not is_valid, f"Entero positivo inválido aceptado: {input_val}"


class TestUtilsIntegration:
    """Tests de integración entre módulos de utils"""

    def test_parser_validator_integration(self):
        """Test de integración entre parser y validador"""
        # Función válida
        func_str = "sin(x) + cos(x)"

        # Validar primero
        is_valid, error_msg = InputValidator.validate_function(func_str)
        assert is_valid, f"Función debería ser válida: {error_msg}"

        # Parsear después
        func = FunctionParser.parse_function(func_str)

        # Verificar que funciona
        result = func(np.pi/4)
        expected = np.sin(np.pi/4) + np.cos(np.pi/4)
        assert abs(result - expected) < 1e-10

    def test_complete_workflow(self):
        """Test del flujo completo: validar -> parsear -> evaluar"""
        # Datos de entrada
        func_str = "x^2 + 2*x + 1"
        a_str, b_str = "0", "2"

        # 1. Validar función
        is_valid_func, error_func = InputValidator.validate_function(func_str)
        assert is_valid_func, f"Error en función: {error_func}"

        # 2. Validar intervalo
        is_valid_int, error_int, a_val, b_val = InputValidator.validate_interval(a_str, b_str)
        assert is_valid_int, f"Error en intervalo: {error_int}"

        # 3. Parsear función
        func = FunctionParser.parse_function(func_str)

        # 4. Evaluar en puntos del intervalo
        test_points = np.linspace(a_val, b_val, 5)
        for x in test_points:
            result = func(x)
            expected = x**2 + 2*x + 1
            assert abs(result - expected) < 1e-10, f"Error en evaluación en x={x}"


class TestUtilsEdgeCases:
    """Tests de casos edge"""

    def test_parser_edge_cases(self):
        """Test de casos edge del parser"""
        # Funciones que podrían causar problemas
        edge_functions = [
            "x",           # Variable simple
            "1",           # Constante
            "x + 0",       # Con cero
            "x * 1",       # Con uno
            "x^0",         # Potencia cero
            "0^x",         # Base cero
        ]

        for func_str in edge_functions:
            # Validar
            is_valid, error = InputValidator.validate_function(func_str)
            if is_valid:
                # Parsear y evaluar
                func = FunctionParser.parse_function(func_str)
                result = func(1.0)  # Evaluar en x=1
                assert np.isfinite(result), f"Resultado no finito para {func_str}: {result}"

    def test_validator_edge_cases(self):
        """Test de casos edge del validador"""
        # Intervalos edge
        edge_intervals = [
            ("0", "0.000001"),     # Intervalo muy pequeño
            ("-1000", "1000"),     # Intervalo grande
            ("1e-10", "1e-9"),     # Números pequeños
            ("1e10", "1e11"),      # Números grandes
        ]

        for a_str, b_str in edge_intervals:
            is_valid, error, a_val, b_val = InputValidator.validate_interval(a_str, b_str)
            assert is_valid, f"Intervalo edge rechazado: [{a_str}, {b_str}], error: {error}"
            assert a_val < b_val, f"Orden incorrecto en intervalo edge: {a_val} >= {b_val}"


if __name__ == "__main__":
    # Ejecutar tests manualmente si no se usa pytest
    import sys

    test_classes = [
        TestFunctionParser,
        TestInputValidator,
        TestUtilsIntegration,
        TestUtilsEdgeCases
    ]

    total_tests = 0
    passed_tests = 0

    print("🧪 Ejecutando tests de utilitarios...")

    for test_class in test_classes:
        print(f"\n📋 {test_class.__name__}:")

        instance = test_class()
        methods = [method for method in dir(instance) if method.startswith('test_')]

        for method_name in methods:
            total_tests += 1
            try:
                method = getattr(instance, method_name)
                method()
                print(f"  ✅ {method_name}")
                passed_tests += 1
            except Exception as e:
                print(f"  ❌ {method_name}: {e}")

    print("\n📊 RESULTADOS UTILITARIOS:")
    print(f"  Tests totales: {total_tests}")
    print(f"  Tests exitosos: {passed_tests}")
    print(".1f")
    if passed_tests == total_tests:
        print("🎉 ¡Todos los tests de utilitarios pasaron!")
        sys.exit(0)
    else:
        print(f"⚠️ {total_tests - passed_tests} tests fallaron")
        sys.exit(1)
