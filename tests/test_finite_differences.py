"""
Tests para diferencias finitas
Pruebas unitarias para métodos de diferenciación numérica
"""

import unittest
import numpy as np
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.finite_differences import FiniteDifferences


class TestFiniteDifferences(unittest.TestCase):
    """Tests para diferencias finitas"""

    def setUp(self):
        """Configurar funciones de test"""
        self.fd = FiniteDifferences()

    def test_forward_difference_linear(self):
        """Test diferencia hacia adelante con función lineal"""
        def f(x):
            return 2*x + 1

        x0 = 1.0
        h = 0.01

        df_approx = FiniteDifferences.forward_difference(f, x0, h)
        df_exact = 2.0  # Derivada exacta de 2x + 1

        self.assertAlmostEqual(df_approx, df_exact, places=2)

    def test_backward_difference_linear(self):
        """Test diferencia hacia atrás con función lineal"""
        def f(x):
            return 3*x - 2

        x0 = 2.0
        h = 0.01

        df_approx = FiniteDifferences.backward_difference(f, x0, h)
        df_exact = 3.0  # Derivada exacta de 3x - 2

        self.assertAlmostEqual(df_approx, df_exact, places=2)

    def test_central_difference_quadratic(self):
        """Test diferencia central con función cuadrática"""
        def f(x):
            return x**2

        x0 = 1.0
        h = 0.001

        df_approx = FiniteDifferences.central_difference(f, x0, h)
        df_exact = 2*x0  # Derivada exacta de x^2

        self.assertAlmostEqual(df_approx, df_exact, places=3)

    def test_second_derivative(self):
        """Test segunda derivada"""
        def f(x):
            return x**3

        x0 = 1.0
        h = 0.001

        d2f_approx = FiniteDifferences.second_derivative(f, x0, h)
        d2f_exact = 6*x0  # Segunda derivada de x^3 es 6x

        self.assertAlmostEqual(d2f_approx, d2f_exact, places=2)

    def test_trigonometric_derivative(self):
        """Test derivada de función trigonométrica"""
        def f(x):
            return np.sin(x)

        x0 = np.pi/4
        h = 0.001

        df_approx = FiniteDifferences.central_difference(f, x0, h)
        df_exact = np.cos(x0)  # Derivada de sin(x) es cos(x)

        self.assertAlmostEqual(df_approx, df_exact, places=3)

    def test_exponential_derivative(self):
        """Test derivada de función exponencial"""
        def f(x):
            return np.exp(x)

        x0 = 0.0
        h = 0.001

        df_approx = FiniteDifferences.central_difference(f, x0, h)
        df_exact = np.exp(x0)  # Derivada de e^x es e^x

        self.assertAlmostEqual(df_approx, df_exact, places=3)


class TestFiniteDifferencesAccuracy(unittest.TestCase):
    """Tests para precisión de diferencias finitas"""

    def test_convergence_with_h(self):
        """Test convergencia al disminuir h"""
        def f(x):
            return x**4

        x0 = 1.0
        df_exact = 4*x0**3  # Derivada exacta: 4x^3

        h_values = [0.1, 0.01, 0.001, 0.0001]
        errors = []

        for h in h_values:
            df_approx = FiniteDifferences.central_difference(f, x0, h)
            error = abs(df_approx - df_exact)
            errors.append(error)

        # Verificar que el error disminuye al reducir h
        for i in range(len(errors) - 1):
            self.assertLess(errors[i+1], errors[i],
                          f"Error no disminuye con h más pequeño: h={h_values[i+1]}")

    def test_optimal_h_value(self):
        """Test encontrar valor óptimo de h"""
        def f(x):
            return np.sin(x)

        x0 = 1.0
        df_exact = np.cos(x0)

        # Probar diferentes valores de h
        h_values = [0.1, 0.01, 0.001, 0.0001, 1e-5]
        min_error = float('inf')
        optimal_h = None

        for h in h_values:
            df_approx = FiniteDifferences.central_difference(f, x0, h)
            error = abs(df_approx - df_exact)

            if error < min_error:
                min_error = error
                optimal_h = h

        # Verificar que se encontró un h óptimo
        self.assertIsNotNone(optimal_h)
        self.assertLess(min_error, 0.01)  # Error debería ser pequeño


class TestFiniteDifferencesEdgeCases(unittest.TestCase):
    """Tests para casos límite en diferencias finitas"""

    def test_very_small_h(self):
        """Test con h muy pequeño (posible underflow)"""
        def f(x):
            return x**2

        x0 = 1.0
        h = 1e-15  # Muy pequeño

        # Debería manejar el caso sin errores numéricos graves
        try:
            df_approx = FiniteDifferences.central_difference(f, x0, h)
            # No verificar precisión, solo que no crashee
            self.assertIsInstance(df_approx, (int, float))
        except OverflowError:
            # Es aceptable que falle con h demasiado pequeño
            pass

    def test_large_function_values(self):
        """Test con función que toma valores grandes"""
        def f(x):
            return 1e10 * x**2

        x0 = 1.0
        h = 0.001

        df_approx = FiniteDifferences.central_difference(f, x0, h)
        df_exact = 2e10 * x0  # Derivada exacta

        # Verificar que maneja valores grandes correctamente
        self.assertAlmostEqual(df_approx / df_exact, 1.0, places=2)

    def test_function_with_noise(self):
        """Test con función que tiene ruido numérico"""
        np.random.seed(42)  # Para reproducibilidad

        def f(x):
            return x**2 + 0.001 * np.random.normal()

        x0 = 1.0
        h = 0.01

        # Calcular derivada varias veces para ver estabilidad
        derivatives = []
        for _ in range(10):
            df = FiniteDifferences.central_difference(f, x0, h)
            derivatives.append(df)

        # Verificar que las derivadas son razonablemente consistentes
        mean_derivative = np.mean(derivatives)
        std_derivative = np.std(derivatives)

        # La desviación estándar debería ser pequeña comparada con el valor medio
        self.assertLess(std_derivative / abs(mean_derivative), 0.1)


class TestFiniteDifferencesIntegration(unittest.TestCase):
    """Tests de integración para diferencias finitas"""

    def test_compare_with_analytical(self):
        """Test comparación con derivadas analíticas"""
        functions_and_derivatives = [
            (lambda x: x**2, lambda x: 2*x),
            (lambda x: x**3, lambda x: 3*x**2),
            (lambda x: np.sin(x), lambda x: np.cos(x)),
            (lambda x: np.exp(x), lambda x: np.exp(x)),
            (lambda x: np.log(x + 1), lambda x: 1/(x + 1)),
        ]

        x0 = 1.0
        h = 0.001

        for f, df_exact in functions_and_derivatives:
            with self.subTest(function=str(f)):
                df_approx = FiniteDifferences.central_difference(f, x0, h)
                df_expected = df_exact(x0)

                self.assertAlmostEqual(df_approx, df_expected, places=2,
                                     msg=f"Derivada incorrecta para función")

    def test_higher_order_derivatives(self):
        """Test derivadas de orden superior"""
        def f(x):
            return x**4

        x0 = 2.0
        h = 0.001

        # Primera derivada
        df = FiniteDifferences.central_difference(f, x0, h)
        df_exact = 4*x0**3
        self.assertAlmostEqual(df, df_exact, places=2)

        # Segunda derivada
        d2f = FiniteDifferences.second_derivative(f, x0, h)
        d2f_exact = 12*x0**2
        self.assertAlmostEqual(d2f, d2f_exact, places=1)


if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.INFO)

    # Ejecutar tests
    unittest.main(verbosity=2)
