#!/usr/bin/env python3
"""
Tests unitarios para métodos numéricos avanzados
Incluye pruebas de interpolación, eliminación gaussiana y análisis de errores

Autor: Equipo TPO Modelado y Simulación
Fecha: 2025
"""

import sys
import os
import pytest
import numpy as np
from typing import List

# Agregar el directorio principal al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from numerics.advanced import InterpolationMethods, AdvancedNumericalMethods, ErrorAnalysis


class TestInterpolationMethods:
    """Tests de métodos de interpolación."""

    @pytest.fixture
    def interp_methods(self):
        return InterpolationMethods()

    def test_lagrange_basic(self, interp_methods):
        """Test básico de interpolación de Lagrange."""
        x_points = [0, 1, 2, 3]
        y_points = [0, 1, 4, 9]  # y = x^2

        # Interpolar en x = 1.5
        result = interp_methods.lagrange_interpolation(x_points, y_points, 1.5)
        expected = 1.5**2  # 2.25

        assert abs(result - expected) < 1e-10, f"Resultado: {result}, esperado: {expected}"

    def test_lagrange_edge_points(self, interp_methods):
        """Test de interpolación en puntos de los datos."""
        x_points = [0, 1, 2, 3]
        y_points = [1, 2, 5, 10]  # y = x^2 + 1

        # Interpolar en puntos conocidos
        for i, x in enumerate(x_points):
            result = interp_methods.lagrange_interpolation(x_points, y_points, x)
            expected = y_points[i]
            assert abs(result - expected) < 1e-10, f"Error en punto conocido x={x}"

    def test_lagrange_polynomial_degree(self, interp_methods):
        """Test con polinomio de grado exacto."""
        # Polinomio de grado 2: x^2 + 2x + 1
        x_points = [-1, 0, 1]
        y_points = [2, 1, 4]  # (-1)^2 + 2*(-1) + 1 = 2, etc.

        # Interpolar en punto intermedio
        result = interp_methods.lagrange_interpolation(x_points, y_points, 0.5)
        expected = 0.5**2 + 2*0.5 + 1  # 2.75

        assert abs(result - expected) < 1e-10, f"Resultado: {result}, esperado: {expected}"

    def test_finite_differences_table(self, interp_methods):
        """Test de tabla de diferencias finitas."""
        x_points = np.array([0, 1, 2, 3])
        y_points = np.array([0, 1, 4, 9])  # x^2

        table = interp_methods.finite_differences_table(x_points, y_points)

        assert table.shape == (4, 4), f"Forma incorrecta: {table.shape}"
        assert np.allclose(table[:, 0], y_points), "Primera columna debe ser y_points"

        # Verificar diferencias primeras: [1, 3, 5]
        expected_first_diff = np.array([1, 3, 5])
        assert np.allclose(table[0:3, 1], expected_first_diff), "Diferencias primeras incorrectas"

    def test_central_finite_differences_derivative(self, interp_methods):
        """Test de derivadas usando diferencias finitas centrales."""
        def f(x):
            return x**3

        x = 2.0
        h = 1e-5

        # Primera derivada
        derivatives = interp_methods.central_finite_differences_derivative_table(f, x, [1], h)
        expected_first = 3*x**2  # 12
        assert abs(derivatives[1] - expected_first) < 1e-3, f"Primera derivada: {derivatives[1]}"

        # Segunda derivada
        derivatives = interp_methods.central_finite_differences_derivative_table(f, x, [2], h)
        expected_second = 6*x  # 12
        assert abs(derivatives[2] - expected_second) < 1e-2, f"Segunda derivada: {derivatives[2]}"


class TestAdvancedNumericalMethods:
    """Tests de métodos numéricos avanzados."""

    @pytest.fixture
    def advanced_methods(self):
        return AdvancedNumericalMethods()

    def test_gaussian_elimination_basic(self, advanced_methods):
        """Test básico de eliminación gaussiana."""
        # Sistema: 2x + y = 3, x + y = 2
        # Solución: x = 1, y = 1
        A = [[2, 1], [1, 1]]
        b = [3, 2]

        solution = advanced_methods.gaussian_elimination(A, b)

        assert abs(solution[0] - 1.0) < 1e-10, f"x incorrecta: {solution[0]}"
        assert abs(solution[1] - 1.0) < 1e-10, f"y incorrecta: {solution[1]}"

    def test_gaussian_elimination_larger_system(self, advanced_methods):
        """Test con sistema más grande."""
        # Sistema 3x3
        A = [[1, 2, 3], [4, 5, 6], [7, 8, 10]]
        b = [6, 15, 22]  # Solución: x = 1, y = 1, z = 1

        solution = advanced_methods.gaussian_elimination(A, b)

        assert abs(solution[0] - 1.0) < 1e-10, f"x incorrecta: {solution[0]}"
        assert abs(solution[1] - 1.0) < 1e-10, f"y incorrecta: {solution[1]}"
        assert abs(solution[2] - 1.0) < 1e-10, f"z incorrecta: {solution[2]}"

    def test_gaussian_elimination_singular_matrix(self, advanced_methods):
        """Test con matriz singular."""
        # Matriz singular (filas dependientes)
        A = [[1, 2], [2, 4]]
        b = [3, 6]

        with pytest.raises(ValueError):
            advanced_methods.gaussian_elimination(A, b)

    def test_aitken_acceleration(self, advanced_methods):
        """Test de aceleración de Aitken."""
        # Secuencia convergente lentamente
        sequence = [1.0, 0.5, 0.75, 0.625, 0.6875, 0.65625]

        accelerated = advanced_methods.aitken_acceleration(sequence)

        # La secuencia converge a 2/3 ≈ 0.666...
        expected_limit = 2/3

        # El último valor acelerado debe estar más cerca del límite
        assert abs(accelerated[-1] - expected_limit) < abs(sequence[-1] - expected_limit), \
               "Aitken debe acelerar la convergencia"


class TestErrorAnalysis:
    """Tests de análisis de errores."""

    @pytest.fixture
    def error_analysis(self):
        return ErrorAnalysis()

    def test_error_estimation_basic(self, error_analysis):
        """Test básico de estimación de error."""
        # Método de bisección con error conocido
        def f(x):
            return x**2 - 2

        # Error estimado para bisección
        error_estimate = error_analysis.estimate_bisection_error(1.4, 1.5)
        expected_error = (1.5 - 1.4) / 2  # 0.05

        assert abs(error_estimate - expected_error) < 1e-10, \
               f"Error estimado: {error_estimate}, esperado: {expected_error}"

    def test_convergence_rate_analysis(self, error_analysis):
        """Test de análisis de tasa de convergencia."""
        # Secuencia de errores convergiendo cuadráticamente
        errors = [1.0, 0.25, 0.0625, 0.015625]  # Errores cuadráticos

        rate = error_analysis.analyze_convergence_rate(errors)

        assert abs(rate - 2.0) < 0.1, f"Tasa de convergencia: {rate}, esperada: 2.0"

    def test_numerical_stability_check(self, error_analysis):
        """Test de verificación de estabilidad numérica."""
        # Función bien condicionada
        def well_conditioned_f(x):
            return x + 1

        # Función mal condicionada
        def ill_conditioned_f(x):
            return x**20

        x = 1.0001

        stability_well = error_analysis.check_numerical_stability(well_conditioned_f, x)
        stability_ill = error_analysis.check_numerical_stability(ill_conditioned_f, x)

        assert stability_well > stability_ill, "Función bien condicionada debe ser más estable"


class TestInterpolationEdgeCases:
    """Tests de casos edge para interpolación."""

    @pytest.fixture
    def interp_methods(self):
        return InterpolationMethods()

    def test_lagrange_single_point(self, interp_methods):
        """Test con un solo punto."""
        x_points = [1.0]
        y_points = [2.0]

        result = interp_methods.lagrange_interpolation(x_points, y_points, 1.0)
        expected = 2.0

        assert abs(result - expected) < 1e-10, "Debe retornar el valor del punto único"

    def test_lagrange_duplicate_points(self, interp_methods):
        """Test con puntos duplicados."""
        x_points = [1.0, 1.0, 2.0]
        y_points = [2.0, 2.0, 3.0]

        # Debe manejar puntos duplicados o dar error apropiado
        try:
            result = interp_methods.lagrange_interpolation(x_points, y_points, 1.5)
            assert np.isfinite(result), "Resultado debe ser finito"
        except (ValueError, ZeroDivisionError):
            pass  # Es aceptable que falle con puntos duplicados

    def test_finite_differences_irregular_spacing(self, interp_methods):
        """Test con espaciado irregular de puntos."""
        x_points = np.array([0, 0.5, 1.5, 3.0])
        y_points = np.array([0, 0.25, 2.25, 9.0])  # x^2

        table = interp_methods.finite_differences_table(x_points, y_points)

        assert table.shape == (4, 4), "Tabla debe tener forma correcta"
        assert np.allclose(table[:, 0], y_points), "Primera columna debe ser y_points"


class TestAdvancedMethodsPerformance:
    """Tests de rendimiento para métodos avanzados."""

    @pytest.fixture
    def advanced_methods(self):
        return AdvancedNumericalMethods()

    def test_gaussian_elimination_performance(self, advanced_methods):
        """Test de rendimiento de eliminación gaussiana."""
        import time

        # Sistema 10x10
        n = 10
        A = np.random.rand(n, n) + np.eye(n)  # Matriz bien condicionada
        b = np.random.rand(n)

        start_time = time.time()
        solution = advanced_methods.gaussian_elimination(A.tolist(), b.tolist())
        end_time = time.time()

        execution_time = end_time - start_time

        assert execution_time < 1.0, f"Gaussiana muy lenta: {execution_time}s"
        assert len(solution) == n, "Solución debe tener dimensión correcta"

    def test_interpolation_performance(self):
        """Test de rendimiento de interpolación."""
        import time
        from numerics.advanced import InterpolationMethods

        interp_methods = InterpolationMethods()

        # Muchos puntos
        x_points = list(range(100))
        y_points = [x**2 for x in x_points]

        start_time = time.time()
        result = interp_methods.lagrange_interpolation(x_points, y_points, 50.5)
        end_time = time.time()

        execution_time = end_time - start_time

        assert execution_time < 2.0, f"Interpolación muy lenta: {execution_time}s"
        assert np.isfinite(result), "Resultado debe ser finito"


class TestIntegrationWithCoreModules:
    """Tests de integración con módulos principales."""

    def test_interpolation_with_finite_differences(self):
        """Test de integración entre interpolación y diferencias finitas."""
        from core.finite_differences import FiniteDifferences
        from numerics.advanced import InterpolationMethods

        # Crear datos
        x_points = np.array([0, 1, 2, 3])
        y_points = np.array([0, 1, 4, 9])  # x^2

        # Usar tabla de diferencias finitas para interpolación
        fd_table = FiniteDifferences.finite_differences_table(x_points, y_points)
        interp_result = FiniteDifferences.interpolate_with_differences(x_points, y_points, 1.5)

        # Comparar con interpolación de Lagrange
        interp_methods = InterpolationMethods()
        lagrange_result = interp_methods.lagrange_interpolation(x_points.tolist(), y_points.tolist(), 1.5)

        expected = 1.5**2  # 2.25

        assert abs(interp_result - expected) < 1e-3, f"FD interpolation: {interp_result}"
        assert abs(lagrange_result - expected) < 1e-10, f"Lagrange interpolation: {lagrange_result}"

        # Los resultados deben ser similares
        assert abs(interp_result - lagrange_result) < 0.1, "Métodos deben dar resultados similares"


if __name__ == "__main__":
    # Ejecutar tests
    try:
        import pytest
        pytest.main([__file__, "-v", "--tb=short"])
    except ImportError:
        print("⚠️ pytest no encontrado, ejecutando tests manualmente...")

        test_classes = [
            TestInterpolationMethods,
            TestAdvancedNumericalMethods,
            TestErrorAnalysis,
            TestInterpolationEdgeCases,
            TestAdvancedMethodsPerformance,
            TestIntegrationWithCoreModules
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

        print(f"\n📊 RESULTADOS MÉTODOS AVANZADOS: {passed_tests}/{total_tests} tests pasaron")

        if passed_tests == total_tests:
            print("🎉 ¡Todos los tests de métodos avanzados pasaron exitosamente!")
        else:
            print(f"⚠️ {total_tests - passed_tests} tests fallaron")
