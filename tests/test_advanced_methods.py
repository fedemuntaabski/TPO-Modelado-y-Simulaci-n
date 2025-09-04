"""
Tests específicos para métodos de búsqueda de raíces
Pruebas unitarias detalladas para algoritmos de raíces
"""

import unittest
import numpy as np
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from numerics.root_methods import RootMethods
from utils.function_parser import FunctionParser


class TestBisectionMethod(unittest.TestCase):
    """Tests detallados para método de bisección"""

    def setUp(self):
        """Configurar funciones de test"""
        self.parser = FunctionParser()

    def test_bisection_simple_quadratic(self):
        """Test bisección con función cuadrática simple x^2 - 4 = 0"""
        def f(x):
            return x**2 - 4

        a, b = 1, 3
        tol = 1e-6
        max_iter = 100

        root = RootMethods.bisection(f, a, b, tol, max_iter)

        self.assertAlmostEqual(root, 2.0, places=5)
        self.assertAlmostEqual(f(root), 0, places=6)

    def test_bisection_negative_root(self):
        """Test bisección para raíz negativa"""
        def f(x):
            return x**2 - 4

        a, b = -3, -1
        tol = 1e-6
        max_iter = 100

        root = RootMethods.bisection(f, a, b, tol, max_iter)

        self.assertAlmostEqual(root, -2.0, places=5)
        self.assertAlmostEqual(f(root), 0, places=6)

    def test_bisection_trigonometric(self):
        """Test bisección con función trigonométrica sin(x) = 0"""
        def f(x):
            return np.sin(x)

        a, b = 3, 4  # Intervalo que contiene π ≈ 3.14159
        tol = 1e-6
        max_iter = 100

        root = RootMethods.bisection(f, a, b, tol, max_iter)

        self.assertAlmostEqual(root, np.pi, places=5)
        self.assertAlmostEqual(f(root), 0, places=6)

    def test_bisection_exponential(self):
        """Test bisección con función exponencial e^x - 2 = 0"""
        def f(x):
            return np.exp(x) - 2

        a, b = 0, 1  # ln(2) ≈ 0.693
        tol = 1e-6
        max_iter = 100

        root = RootMethods.bisection(f, a, b, tol, max_iter)

        expected = np.log(2)
        self.assertAlmostEqual(root, expected, places=5)
        self.assertAlmostEqual(f(root), 0, places=6)

    def test_bisection_no_root(self):
        """Test bisección cuando no hay raíz en el intervalo"""
        def f(x):
            return x**2 + 1  # Siempre positiva, no cruza el eje

        a, b = 0, 1
        tol = 1e-6
        max_iter = 100

        with self.assertRaises(ValueError):
            RootMethods.bisection(f, a, b, tol, max_iter)


class TestNewtonRaphsonMethod(unittest.TestCase):
    """Tests detallados para método de Newton-Raphson"""

    def test_newton_raphson_quadratic(self):
        """Test Newton-Raphson con función cuadrática x^2 - 2 = 0"""
        def f(x):
            return x**2 - 2

        def df(x):
            return 2*x

        x0 = 1.5  # Aproximación inicial
        tol = 1e-6
        max_iter = 50

        root = RootMethods.newton_raphson(f, df, x0, tol, max_iter)

        expected = np.sqrt(2)
        self.assertAlmostEqual(root, expected, places=5)
        self.assertAlmostEqual(f(root), 0, places=6)

    def test_newton_raphson_cubic(self):
        """Test Newton-Raphson con función cúbica x^3 - x - 1 = 0"""
        def f(x):
            return x**3 - x - 1

        def df(x):
            return 3*x**2 - 1

        x0 = 1.5  # Aproximación inicial
        tol = 1e-6
        max_iter = 50

        root = RootMethods.newton_raphson(f, df, x0, tol, max_iter)

        # Verificar que es raíz
        self.assertAlmostEqual(f(root), 0, places=6)

    def test_newton_raphson_trigonometric(self):
        """Test Newton-Raphson con función trigonométrica cos(x) + 1 = 0"""
        def f(x):
            return np.cos(x) + 1

        def df(x):
            return -np.sin(x)

        x0 = 0  # Aproximación inicial
        tol = 1e-6
        max_iter = 50

        root = RootMethods.newton_raphson(f, df, x0, tol, max_iter)

        expected = np.pi  # cos(π) = -1
        self.assertAlmostEqual(root, expected, places=5)
        self.assertAlmostEqual(f(root), 0, places=6)


class TestFixedPointMethod(unittest.TestCase):
    """Tests detallados para método de punto fijo"""

    def test_fixed_point_simple(self):
        """Test punto fijo con función simple x^2 - x - 1 = 0"""
        def g(x):
            return (x + 1)**(1/2)  # Rearranged from x^2 - x - 1 = 0

        x0 = 1.5
        tol = 1e-6
        max_iter = 50

        root = RootMethods.fixed_point(g, x0, tol, max_iter)

        # Verificar convergencia
        self.assertLess(abs(root - g(root)), tol)

    def test_fixed_point_convergence(self):
        """Test convergencia del método de punto fijo"""
        def g(x):
            return np.cos(x)  # Para ecuación x = cos(x)

        x0 = 0.5
        tol = 1e-6
        max_iter = 50

        root = RootMethods.fixed_point(g, x0, tol, max_iter)

        # Verificar que converge
        self.assertLess(abs(root - g(root)), tol)


class TestAitkenMethod(unittest.TestCase):
    """Tests detallados para método de Aitken"""

    def test_aitken_acceleration(self):
        """Test aceleración de Aitken"""
        def g(x):
            return np.cos(x)

        x0 = 0.5
        tol = 1e-6
        max_iter = 50

        root = RootMethods.aitken(g, x0, tol, max_iter)

        # Verificar convergencia
        self.assertLess(abs(root - g(root)), tol)


class TestRootMethodsIntegration(unittest.TestCase):
    """Tests de integración entre métodos de raíces"""

    def setUp(self):
        """Configurar parser para tests"""
        self.parser = FunctionParser()

    def test_multiple_methods_same_function(self):
        """Test diferentes métodos con la misma función"""
        def f(x):
            return x**2 - 4

        def df(x):
            return 2*x

        def g(x):
            return 2 - x  # Rearranged from x^2 - 4 = 0

        # Parámetros comunes
        tol = 1e-6
        max_iter = 100

        # Método de bisección
        root_bisect = RootMethods.bisection(f, 1, 3, tol, max_iter)

        # Método de Newton-Raphson
        root_newton = RootMethods.newton_raphson(f, df, 1.5, tol, max_iter)

        # Método de punto fijo
        root_fixed = RootMethods.fixed_point(g, 1.5, tol, max_iter)

        # Todos deberían converger a la misma raíz (2.0)
        expected = 2.0

        self.assertAlmostEqual(root_bisect, expected, places=4)
        self.assertAlmostEqual(root_newton, expected, places=4)
        self.assertAlmostEqual(root_fixed, expected, places=4)

    def test_method_comparison_performance(self):
        """Test comparación de rendimiento entre métodos"""
        def f(x):
            return x**3 - 2*x - 5

        def df(x):
            return 3*x**2 - 2

        def g(x):
            return (2*x + 5)**(1/3)

        tol = 1e-6
        max_iter = 100

        # Este test verifica que los métodos convergen
        # En un escenario real, mediríamos el tiempo de ejecución

        # Bisección
        root_bisect = RootMethods.bisection(f, 2, 3, tol, max_iter)
        self.assertAlmostEqual(f(root_bisect), 0, places=5)

        # Newton-Raphson
        root_newton = RootMethods.newton_raphson(f, df, 2.5, tol, max_iter)
        self.assertAlmostEqual(f(root_newton), 0, places=5)


class TestErrorHandling(unittest.TestCase):
    """Tests para manejo de errores en métodos de raíces"""

    def test_bisection_invalid_interval(self):
        """Test bisección con intervalo inválido"""
        def f(x):
            return x**2 - 4

        # Intervalo donde f(a) y f(b) tienen el mismo signo
        a, b = 3, 4  # Ambos positivos
        tol = 1e-6
        max_iter = 100

        with self.assertRaises(ValueError):
            RootMethods.bisection(f, a, b, tol, max_iter)

    def test_newton_raphson_zero_derivative(self):
        """Test Newton-Raphson cuando la derivada se hace cero"""
        def f(x):
            return x**3  # f'(x) = 3x^2, se hace cero en x=0

        def df(x):
            return 3*x**2

        x0 = 0.1
        tol = 1e-6
        max_iter = 10

        # Debería manejar el caso o lanzar una excepción apropiada
        try:
            root = RootMethods.newton_raphson(f, df, x0, tol, max_iter)
        except (ZeroDivisionError, ValueError):
            pass  # Es aceptable que falle en este caso

    def test_max_iterations_exceeded(self):
        """Test cuando se exceden las iteraciones máximas"""
        def f(x):
            return x**2 + 1  # No tiene raíces reales

        def df(x):
            return 2*x

        x0 = 1.0
        tol = 1e-10  # Tolerancia muy estricta
        max_iter = 5   # Pocas iteraciones

        with self.assertRaises(ValueError):
            RootMethods.newton_raphson(f, df, x0, tol, max_iter)


if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.INFO)

    # Ejecutar tests
    unittest.main(verbosity=2)
