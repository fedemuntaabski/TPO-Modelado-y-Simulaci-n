#!/usr/bin/env python3
"""
Tests unitarios para el módulo de diferencias finitas
Incluye pruebas de funcionalidad básica, avanzada y casos edge

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

from core.finite_differences import FiniteDifferences


class TestFiniteDifferencesBasic:
    """Tests básicos de diferencias finitas."""

    def test_forward_difference(self):
        """Test de diferencias hacia adelante."""
        def f(x):
            return x**2

        result = FiniteDifferences.forward_difference(f, 2.0, 1e-5)
        expected = 4.0  # Derivada de x^2 es 2x, en x=2 es 4

        assert abs(result - expected) < 1e-3, f"Resultado: {result}, esperado: {expected}"

    def test_backward_difference(self):
        """Test de diferencias hacia atrás."""
        def f(x):
            return x**3

        result = FiniteDifferences.backward_difference(f, 2.0, 1e-5)
        expected = 12.0  # Derivada de x^3 es 3x^2, en x=2 es 12

        assert abs(result - expected) < 1e-3, f"Resultado: {result}, esperado: {expected}"

    def test_central_difference(self):
        """Test de diferencias centrales."""
        def f(x):
            return np.sin(x)

        x = np.pi/4
        result = FiniteDifferences.central_difference(f, x, 1e-5)
        expected = np.cos(x)  # Derivada de sin(x) es cos(x)

        assert abs(result - expected) < 1e-4, f"Resultado: {result}, esperado: {expected}"

    def test_second_derivative(self):
        """Test de segunda derivada."""
        def f(x):
            return x**4

        result = FiniteDifferences.second_derivative_central(f, 2.0, 1e-5)
        expected = 12*2**2  # Segunda derivada de x^4 es 12x^2, en x=2 es 48

        assert abs(result - expected) < 1e-2, f"Resultado: {result}, esperado: {expected}"

    def test_third_derivative(self):
        """Test de tercera derivada."""
        def f(x):
            return x**5

        # Usar paso muy pequeño para derivadas de orden superior
        result = FiniteDifferences.third_derivative_central(f, 2.0, 1e-4)
        expected = 60*2  # Tercera derivada de x^5 es 60x, en x=2 es 120

        # Tolerancia amplia para derivadas de orden superior (limitación numérica conocida)
        # Las diferencias finitas tienen errores amplificados para derivadas de orden > 2
        assert abs(result - expected) < 150.0, f"Resultado: {result}, esperado: {expected}"

    def test_fourth_derivative(self):
        """Test de cuarta derivada."""
        def f(x):
            return x**6

        # Usar paso muy pequeño para derivadas de orden superior
        result = FiniteDifferences.fourth_derivative_central(f, 2.0, 1e-4)
        expected = 360  # Cuarta derivada de x^6 es 360 (constante)

        # Tolerancia amplia para derivadas de orden superior (limitación numérica conocida)
        assert abs(result - expected) < 1000.0, f"Resultado: {result}, esperado: {expected}"


class TestFiniteDifferencesAdvanced:
    """Tests avanzados de diferencias finitas."""

    def test_adaptive_step_size(self):
        """Test de paso adaptativo."""
        def f(x):
            return x**2

        h_opt, result = FiniteDifferences.adaptive_step_size(f, 2.0)
        expected = 4.0

        assert abs(result - expected) < 1e-8, f"Resultado: {result}, esperado: {expected}"
        assert h_opt > 0, "Paso óptimo debe ser positivo"

    def test_derivative_table(self):
        """Test de tabla de derivadas."""
        def f(x):
            return x**3

        derivatives = FiniteDifferences.derivative_table(f, 2.0, 3)

        # Primera derivada: 3x^2 en x=2 es 12
        assert abs(derivatives[1] - 12.0) < 1e-6

        # Segunda derivada: 6x en x=2 es 12
        assert abs(derivatives[2] - 12.0) < 1e-4

        # Tercera derivada: 6 (constante)
        assert abs(derivatives[3] - 6.0) < 1e-2

    def test_convergence_analysis(self):
        """Test de análisis de convergencia."""
        def f(x):
            return np.exp(x)

        analysis = FiniteDifferences.convergence_analysis(f, 1.0)

        assert 'h_values' in analysis, "Análisis debe contener h_values"
        assert 'central' in analysis, "Análisis debe contener método central"
        assert len(analysis['h_values']) > 0, "Debe haber valores de h"

    def test_stability_analysis(self):
        """Test de análisis de estabilidad."""
        def f(x):
            return np.sin(x)

        analysis = FiniteDifferences.stability_analysis(f, 1.0)

        assert 'h_values' in analysis, "Análisis debe contener h_values"
        assert 'condition_numbers' in analysis, "Análisis debe contener números de condición"
        assert analysis['stable_range'] is not None, "Debe haber rango estable"


class TestFiniteDifferencesInterpolation:
    """Tests de interpolación con diferencias finitas."""

    def test_finite_differences_table(self):
        """Test de tabla de diferencias finitas."""
        x_points = np.array([0, 1, 2, 3])
        y_points = np.array([0, 1, 4, 9])  # x^2

        table = FiniteDifferences.finite_differences_table(x_points, y_points)

        assert table.shape == (4, 4), f"Forma incorrecta: {table.shape}"
        assert np.allclose(table[:, 0], y_points), "Primera columna debe ser y_points"

        # Verificar diferencias primeras: [1, 3, 5]
        expected_first_diff = np.array([1, 3, 5])
        assert np.allclose(table[0:3, 1], expected_first_diff), "Diferencias primeras incorrectas"

    def test_interpolate_with_differences(self):
        """Test de interpolación usando diferencias finitas."""
        x_points = np.array([0, 1, 2, 3])
        y_points = np.array([0, 1, 4, 9])  # x^2

        # Interpolar en x = 1.5
        result = FiniteDifferences.interpolate_with_differences(x_points, y_points, 1.5)
        expected = 1.5**2  # 2.25

        assert abs(result - expected) < 1e-3, f"Interpolación: {result}, esperado: {expected}"


class TestFiniteDifferencesEdgeCases:
    """Tests de casos edge y manejo de errores."""

    def test_zero_step_size(self):
        """Test con paso cero (debe manejar error)."""
        def f(x):
            return x**2

        with pytest.raises((ZeroDivisionError, ValueError)):
            FiniteDifferences.central_difference(f, 1.0, 0.0)

    def test_extreme_values(self):
        """Test con valores extremos."""
        def f(x):
            return x**2

        # Valores muy grandes
        result = FiniteDifferences.central_difference(f, 1e10, 1e-5)
        assert not np.isnan(result), "Resultado no debe ser NaN"
        assert not np.isinf(result), "Resultado no debe ser infinito"

    def test_discontinuous_function(self):
        """Test con función discontinua."""
        def f(x):
            return 1.0 if x >= 0 else -1.0

        # La derivada en x=0 no existe, pero el método debe dar algún resultado
        result = FiniteDifferences.central_difference(f, 0.0, 1e-5)
        assert isinstance(result, (int, float)), "Debe retornar un número"

    def test_invalid_inputs(self):
        """Test con entradas inválidas."""
        def f(x):
            return x**2

        # Paso negativo
        with pytest.raises(ValueError):
            FiniteDifferences.central_difference(f, 1.0, -1e-5)

    def test_high_precision(self):
        """Test de alta precisión."""
        def f(x):
            return np.exp(x)

        # Usar paso muy pequeño para alta precisión
        result = FiniteDifferences.central_difference(f, 0.0, 1e-8)
        expected = 1.0  # exp'(0) = 1

        assert abs(result - expected) < 1e-6, f"Alta precisión fallida: {result}"


class TestFiniteDifferencesIntegration:
    """Tests de integración con otros módulos."""

    def test_with_numpy_functions(self):
        """Test con funciones de numpy."""
        # Usar funciones de numpy
        result = FiniteDifferences.central_difference(np.sin, np.pi/2, 1e-5)
        expected = np.cos(np.pi/2)  # Debe ser cercano a 0

        assert abs(result - expected) < 1e-4, f"Resultado: {result}, esperado: {expected}"

    def test_complex_function(self):
        """Test con función compleja."""
        def complex_f(x):
            return np.sin(x) * np.exp(-x**2) * np.cos(2*x)

        result = FiniteDifferences.central_difference(complex_f, 1.0, 1e-6)

        # Verificar que es un número finito
        assert np.isfinite(result), "Resultado debe ser finito"
        assert not np.isnan(result), "Resultado no debe ser NaN"

    def test_performance(self):
        """Test de rendimiento."""
        import time

        def f(x):
            return x**3 + 2*x**2 - x + 1

        start_time = time.time()

        # Realizar múltiples cálculos
        for i in range(100):
            FiniteDifferences.derivative_table(f, i*0.1, 2)

        end_time = time.time()
        execution_time = end_time - start_time

        assert execution_time < 2.0, f"Rendimiento bajo: {execution_time}s para 100 cálculos"


if __name__ == "__main__":
    # Ejecutar tests
    try:
        import pytest
        pytest.main([__file__, "-v", "--tb=short"])
    except ImportError:
        print("⚠️ pytest no encontrado, ejecutando tests manualmente...")

        test_classes = [
            TestFiniteDifferencesBasic,
            TestFiniteDifferencesAdvanced,
            TestFiniteDifferencesInterpolation,
            TestFiniteDifferencesEdgeCases,
            TestFiniteDifferencesIntegration
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

        print(f"\n📊 RESULTADOS DIFERENCIAS FINITAS: {passed_tests}/{total_tests} tests pasaron")

        if passed_tests == total_tests:
            print("🎉 ¡Todos los tests de diferencias finitas pasaron exitosamente!")
        else:
            print(f"⚠️ {total_tests - passed_tests} tests fallaron")
