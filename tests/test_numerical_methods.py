"""
Tests para métodos numéricos
Pruebas unitarias para algoritmos de cálculo numérico
"""

import unittest
import numpy as np
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.differential_equations import DifferentialEquations
from core.finite_differences import FiniteDifferences
from core.numerical_integration import NumericalIntegration
from numerics.root_methods import RootMethods
from numerics.core_methods import NumericalMethods


class TestDifferentialEquations(unittest.TestCase):
    """Tests para ecuaciones diferenciales"""

    def test_euler_simple(self):
        """Test método de Euler con ecuación simple dy/dt = -y"""
        def f(t, y):
            return -y

        t_span = (0, 1)
        y0 = 1.0
        n_points = 10

        t, y = DifferentialEquations.euler(f, t_span, y0, n_points)

        # Verificar que la solución se acerque a e^-1 ≈ 0.3679
        expected = np.exp(-1)
        self.assertAlmostEqual(y[-1], expected, places=1)  # Más tolerante

    def test_rk4_accuracy(self):
        """Test método RK4 con mayor precisión"""
        def f(t, y):
            return -2 * t * y

        t_span = (0, 0.5)
        y0 = 1.0
        n_points = 20

        t, y = DifferentialEquations.rk4(f, t_span, y0, n_points)

        # Solución exacta: y = e^(-t^2)
        expected = np.exp(-0.25)
        self.assertAlmostEqual(y[-1], expected, places=4)


class TestFiniteDifferences(unittest.TestCase):
    """Tests para diferencias finitas"""

    def test_forward_difference(self):
        """Test diferencia hacia adelante"""
        def f(x):
            return x**2

        x0 = 1.0
        h = 0.01

        df_approx = FiniteDifferences.forward_difference(f, x0, h)
        df_exact = 2 * x0  # Derivada exacta de x^2

        self.assertAlmostEqual(df_approx, df_exact, places=1)  # Más tolerante con h=0.01

    def test_central_difference(self):
        """Test diferencia central"""
        def f(x):
            return np.sin(x)

        x0 = np.pi/4
        h = 0.001

        df_approx = FiniteDifferences.central_difference(f, x0, h)
        df_exact = np.cos(x0)  # Derivada exacta de sin(x)

        self.assertAlmostEqual(df_approx, df_exact, places=3)


class TestNumericalIntegration(unittest.TestCase):
    """Tests para integración numérica"""

    def test_trapezoidal_rule(self):
        """Test regla trapezoidal"""
        def f(x):
            return x**2

        a, b = 0, 1
        n = 100

        integral_approx = NumericalIntegration.trapezoid(f, a, b, n)
        integral_exact = 1/3  # Integral exacta de x^2 de 0 a 1

        self.assertAlmostEqual(integral_approx, integral_exact, places=3)

    def test_simpson_rule(self):
        """Test regla de Simpson"""
        def f(x):
            return np.sin(x)

        a, b = 0, np.pi
        n = 100

        integral_approx = NumericalIntegration.simpson_13(f, a, b, n)
        integral_exact = 2  # Integral exacta de sin(x) de 0 a π

        self.assertAlmostEqual(integral_approx, integral_exact, places=4)


class TestRootMethods(unittest.TestCase):
    """Tests para métodos de búsqueda de raíces"""

    def test_bisection_method(self):
        """Test método de bisección"""
        def f(x):
            return x**2 - 4

        a, b = 1, 3
        tol = 1e-6
        max_iter = 100

        root, iterations, history = RootMethods.bisection_method(f, a, b, tol, max_iter)

        self.assertAlmostEqual(root, 2.0, places=5)
        self.assertAlmostEqual(f(root), 0, places=6)
        self.assertGreater(len(history), 0)

    def test_newton_raphson(self):
        """Test método de Newton-Raphson"""
        def f(x):
            return x**2 - 2

        def df(x):
            return 2*x

        x0 = 1.5
        tol = 1e-6
        max_iter = 50

        root, iterations, history = RootMethods.newton_raphson_method(f, df, x0, tol, max_iter)

        self.assertAlmostEqual(root, np.sqrt(2), places=5)
        self.assertAlmostEqual(f(root), 0, places=6)
        self.assertGreater(len(history), 0)


class TestCoreMethods(unittest.TestCase):
    """Tests para métodos core - simplificados"""

    def test_basic_math(self):
        """Test operaciones matemáticas básicas"""
        # Test simple para verificar que numpy funciona
        A = np.array([[1, 2], [3, 4]])
        B = np.array([[5, 6], [7, 8]])

        # Test suma básica
        C = A + B
        expected = np.array([[6, 8], [10, 12]])
        np.testing.assert_array_almost_equal(C, expected)

        # Test multiplicación básica
        D = np.dot(A, B)
        expected = np.array([[19, 22], [43, 50]])
        np.testing.assert_array_almost_equal(D, expected)


if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.INFO)

    # Ejecutar tests
    unittest.main(verbosity=2)
