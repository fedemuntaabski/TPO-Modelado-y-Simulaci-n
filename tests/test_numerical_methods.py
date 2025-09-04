#!/usr/bin/env python3
"""
Tests unitarios para métodos numéricos principales
Incluye pruebas de integración, EDO, raíces y parsing matemático

Autor: Equipo TPO Modelado y Simulación
Fecha: 2025
"""

import sys
import os
import pytest
import numpy as np
from typing import Callable

# Agregar el directorio principal al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from numerics.methods import NumericalMethods, MathParser


class TestNumericalMethodsRoots:
    """Tests de métodos para encontrar raíces."""

    @pytest.fixture
    def methods(self):
        return NumericalMethods()

    def test_bisection_basic(self, methods):
        """Test básico del método de bisección."""
        def f(x):
            return x**2 - 4  # Raíz en x = 2

        root, iterations, history = methods.bisection(f, 0, 5, tolerance=1e-6)

        assert abs(root - 2.0) < 1e-5, f"Raíz incorrecta: {root}"
        assert iterations > 0, "Debe haber iteraciones"
        assert len(history) == iterations, "Historial inconsistente"

    def test_bisection_edge_cases(self, methods):
        """Test de casos edge para bisección."""
        def f(x):
            return x - 3  # Raíz en x = 3

        # Caso donde a y b están muy cerca de la raíz
        root, iterations, history = methods.bisection(f, 2.9, 3.1, tolerance=1e-10)

        assert abs(root - 3.0) < 1e-9, f"Raíz incorrecta: {root}"
        assert iterations < 50, "Demasiadas iteraciones para caso simple"

    def test_newton_raphson_basic(self, methods):
        """Test básico de Newton-Raphson."""
        def f(x):
            return x**2 - 4

        def df(x):
            return 2*x

        root, iterations, history = methods.newton_raphson(f, df, 1.0, tolerance=1e-8)

        assert abs(root - 2.0) < 1e-7, f"Raíz incorrecta: {root}"
        assert iterations > 0, "Debe haber iteraciones"

    def test_newton_raphson_convergence(self, methods):
        """Test de convergencia de Newton-Raphson."""
        def f(x):
            return x**3 - 8  # Raíz en x = 2

        def df(x):
            return 3*x**2

        root, iterations, history = methods.newton_raphson(f, df, 1.5, tolerance=1e-10)

        assert abs(root - 2.0) < 1e-9, f"Raíz incorrecta: {root}"
        assert iterations < 10, "Debe converger rápidamente"

    def test_fixed_point_basic(self, methods):
        """Test básico de punto fijo."""
        def g(x):
            return (x + 4/x) / 2  # Para encontrar raíz de x^2 - 4 = 0

        root, iterations, history = methods.fixed_point(g, 1.5, tolerance=1e-6)

        assert abs(root - 2.0) < 1e-5, f"Raíz incorrecta: {root}"
        assert iterations > 0, "Debe haber iteraciones"


class TestNumericalMethodsIntegration:
    """Tests de métodos de integración numérica."""

    @pytest.fixture
    def methods(self):
        return NumericalMethods()

    def test_trapezoidal_basic(self, methods):
        """Test básico de integración trapezoidal."""
        def f(x):
            return x**2

        result = methods.trapezoidal_integration(f, 0, 2, 1000)
        expected = 8/3  # ∫x^2 dx de 0 a 2 = 8/3

        assert abs(result - expected) < 0.01, f"Resultado: {result}, esperado: {expected}"

    def test_trapezoidal_polynomial(self, methods):
        """Test de integración trapezoidal con polinomio de alto grado."""
        def f(x):
            return x**4 + 3*x**3 - 2*x + 1

        result = methods.trapezoidal_integration(f, -1, 1, 10000)
        expected = 2 + 2/5  # ∫(x^4 + 3x^3 - 2x + 1) dx de -1 a 1 = 2 + 2/5 = 12/5

        assert abs(result - expected) < 0.001, f"Resultado: {result}, esperado: {expected}"

    def test_simpson_basic(self, methods):
        """Test básico de integración de Simpson."""
        def f(x):
            return np.sin(x)

        result = methods.simpson_integration(f, 0, np.pi, 1000)
        expected = 2.0  # ∫sin(x) dx de 0 a π = 2

        assert abs(result - expected) < 0.001, f"Resultado: {result}, esperado: {expected}"

    def test_simpson_precision(self, methods):
        """Test de precisión de Simpson."""
        def f(x):
            return 1/(1 + x**2)  # Función suave

        result = methods.simpson_integration(f, 0, 1, 10000)
        expected = np.arctan(1) - np.arctan(0)  # ∫1/(1+x^2) dx = arctan(x)

        assert abs(result - expected) < 1e-6, f"Resultado: {result}, esperado: {expected}"


class TestNumericalMethodsODE:
    """Tests de métodos para ecuaciones diferenciales ordinarias."""

    @pytest.fixture
    def methods(self):
        return NumericalMethods()

    def test_euler_basic(self, methods):
        """Test básico del método de Euler."""
        def f(x, y):
            return -y  # dy/dx = -y, solución: y = e^(-x)

        x_vals, y_vals = methods.euler_ode(f, 0, 1, 1, 100)

        assert len(x_vals) == len(y_vals), "Arrays deben tener misma longitud"
        assert abs(y_vals[-1] - np.exp(-1)) < 0.1, f"Solución final incorrecta: {y_vals[-1]}"

    def test_euler_stiff(self, methods):
        """Test de Euler con ecuación stiff."""
        def f(x, y):
            return -100*y  # Ecuación stiff

        x_vals, y_vals = methods.euler_ode(f, 0, 1, 0.01, 1000)

        # Para ecuación stiff, Euler puede ser inestable, pero debe dar algún resultado
        assert len(x_vals) == len(y_vals), "Arrays deben tener misma longitud"
        assert not np.any(np.isnan(y_vals)), "No debe haber NaN en la solución"

    def test_runge_kutta_basic(self, methods):
        """Test básico de Runge-Kutta."""
        def f(x, y):
            return y  # dy/dx = y, solución: y = e^x

        x_vals, y_vals = methods.runge_kutta_4(f, (0, 1), 1, 100)

        assert len(x_vals) == len(y_vals), "Arrays deben tener misma longitud"
        assert abs(y_vals[-1] - np.exp(1)) < 0.001, f"Solución final incorrecta: {y_vals[-1]}"

    def test_runge_kutta_precision(self, methods):
        """Test de precisión de Runge-Kutta."""
        def f(x, y):
            return -y**2  # Ecuación no lineal

        x_vals, y_vals = methods.runge_kutta_4(f, (0, 1), 1, 1000)

        # Solución exacta: y = 1/(x + 1)
        expected_final = 1/(1 + 1)

        assert abs(y_vals[-1] - expected_final) < 0.001, f"Solución final incorrecta: {y_vals[-1]}"


class TestMathParser:
    """Tests del parser matemático."""

    @pytest.fixture
    def parser(self):
        return MathParser()

    def test_basic_arithmetic(self, parser):
        """Test de operaciones aritméticas básicas."""
        test_cases = [
            ("2 + 3", 5),
            ("10 - 4", 6),
            ("3 * 4", 12),
            ("15 / 3", 5),
            ("2 ^ 3", 8),
            ("(2 + 3) * 4", 20),
        ]

        for expr, expected in test_cases:
            result = parser.evaluate_expression(expr)
            assert abs(result - expected) < 1e-10, f"Error en '{expr}': {result} != {expected}"

    def test_mathematical_functions(self, parser):
        """Test de funciones matemáticas."""
        test_cases = [
            ("sin(0)", 0),
            ("cos(0)", 1),
            ("tan(pi/4)", 1),
            ("log(1)", 0),
            ("log10(10)", 1),
            ("exp(0)", 1),
            ("sqrt(4)", 2),
            ("abs(-5)", 5),
        ]

        for expr, expected in test_cases:
            result = parser.evaluate_expression(expr)
            assert abs(result - expected) < 1e-10, f"Error en '{expr}': {result} != {expected}"

    def test_constants(self, parser):
        """Test de constantes matemáticas."""
        test_cases = [
            ("pi", np.pi),
            ("e", np.e),
            ("2*pi", 2*np.pi),
            ("e^2", np.e**2),
        ]

        for expr, expected in test_cases:
            result = parser.evaluate_expression(expr)
            assert abs(result - expected) < 1e-10, f"Error en '{expr}': {result} != {expected}"

    def test_function_parsing(self, parser):
        """Test de parsing de funciones."""
        # Función: x^2 + 2*x + 1
        func = parser.parse_function("x^2 + 2*x + 1")

        test_points = [0, 1, 2, -1]
        for x in test_points:
            result = func(x)
            expected = x**2 + 2*x + 1
            assert abs(result - expected) < 1e-10, f"Error en punto x={x}: {result} != {expected}"

    def test_ode_function_parsing(self, parser):
        """Test de parsing de funciones para EDO."""
        # Función: t + y
        ode_func = parser.parse_ode_function("t + y")

        result = ode_func(1, 2)  # t=1, y=2
        expected = 1 + 2  # 3

        assert abs(result - expected) < 1e-10, f"Error en función ODE: {result} != {expected}"


class TestNumericalMethodsEdgeCases:
    """Tests de casos edge y manejo de errores."""

    @pytest.fixture
    def methods(self):
        return NumericalMethods()

    def test_bisection_no_root(self, methods):
        """Test de bisección cuando no hay raíz en el intervalo."""
        def f(x):
            return x**2 + 1  # Nunca cruza el eje x

        with pytest.raises(ValueError):
            methods.bisection(f, -1, 1, tolerance=1e-6)

    def test_integration_singularities(self, methods):
        """Test de integración con singularidades."""
        def f(x):
            return 1/np.sqrt(x)  # Singularidad en x=0

        # Debe manejar la singularidad o dar un resultado razonable
        result = methods.simpson_integration(f, 0.001, 1, 1000)
        assert np.isfinite(result), "Resultado debe ser finito"

    def test_ode_stiff_equation(self, methods):
        """Test con ecuación diferencial stiff."""
        def f(x, y):
            return -1000*y  # Muy stiff

        x_vals, y_vals = methods.runge_kutta_4(f, (0, 0.01), 1, 1000)

        # RK4 debe manejar mejor las ecuaciones stiff que Euler
        assert len(x_vals) == len(y_vals), "Arrays deben tener misma longitud"
        assert not np.any(np.isnan(y_vals)), "No debe haber NaN"

    def test_parser_invalid_syntax(self):
        """Test del parser con sintaxis inválida."""
        parser = MathParser()

        invalid_expressions = [
            "2++3",
            "sin(",
            "1/0",
            "undefined_function(1)",
        ]

        for expr in invalid_expressions:
            with pytest.raises((ValueError, SyntaxError, NameError)):
                parser.evaluate_expression(expr)


class TestNumericalMethodsPerformance:
    """Tests de rendimiento."""

    @pytest.fixture
    def methods(self):
        return NumericalMethods()

    def test_integration_performance(self, methods):
        """Test de rendimiento de integración."""
        import time

        def complex_function(x):
            return np.sin(x) * np.exp(-x) * np.cos(2*x)

        start_time = time.time()
        result = methods.simpson_integration(complex_function, 0, 10, 10000)
        end_time = time.time()

        execution_time = end_time - start_time

        assert execution_time < 5.0, f"Integración muy lenta: {execution_time}s"
        assert np.isfinite(result), "Resultado debe ser finito"

    def test_ode_performance(self, methods):
        """Test de rendimiento de resolución de EDO."""
        import time

        def f(x, y):
            return np.sin(x) * y + np.cos(x)

        start_time = time.time()
        x_vals, y_vals = methods.runge_kutta_4(f, (0, 10), 1, 10000)
        end_time = time.time()

        execution_time = end_time - start_time

        assert execution_time < 10.0, f"EDO muy lenta: {execution_time}s"
        assert len(x_vals) == len(y_vals), "Arrays inconsistentes"


if __name__ == "__main__":
    # Ejecutar tests
    try:
        import pytest
        pytest.main([__file__, "-v", "--tb=short"])
    except ImportError:
        print("⚠️ pytest no encontrado, ejecutando tests manualmente...")

        test_classes = [
            TestNumericalMethodsRoots,
            TestNumericalMethodsIntegration,
            TestNumericalMethodsODE,
            TestMathParser,
            TestNumericalMethodsEdgeCases,
            TestNumericalMethodsPerformance
        ]

        total_tests = 0
        passed_tests = 0

        for test_class in test_classes:
            print(f"\n🧪 Ejecutando {test_class.__name__}...")

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

        print(f"\n📊 RESULTADOS MÉTODOS NUMÉRICOS: {passed_tests}/{total_tests} tests pasaron")

        if passed_tests == total_tests:
            print("🎉 ¡Todos los tests de métodos numéricos pasaron exitosamente!")
        else:
            print(f"⚠️ {total_tests - passed_tests} tests fallaron")
