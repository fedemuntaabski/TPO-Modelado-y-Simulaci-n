"""
Tests unitarios para los métodos de búsqueda de raíces.

Verifica el correcto funcionamiento de los algoritmos numéricos
siguiendo buenas prácticas de testing.
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.core.root_finding import RootFinder, create_function_from_string


class TestRootFinding(unittest.TestCase):
    """Tests para métodos de búsqueda de raíces"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.finder = RootFinder(tolerance=1e-6, max_iterations=100)
        
        # Funciones de prueba con raíces conocidas
        self.linear_func = lambda x: 2*x - 4  # Raíz: x = 2
        self.quadratic_func = lambda x: x**2 - 4  # Raíces: x = ±2
        self.cubic_func = lambda x: x**3 - x**2 - 2*x  # Raíces: x = 0, -1, 2
    
    def test_bisection_linear(self):
        """Test bisección con función lineal"""
        result = self.finder.bisection_method(self.linear_func, 0, 3)
        
        self.assertTrue(result.converged)
        self.assertAlmostEqual(result.root, 2.0, places=5)
        self.assertLess(abs(result.function_value), 1e-6)
    
    def test_bisection_quadratic(self):
        """Test bisección con función cuadrática"""
        result = self.finder.bisection_method(self.quadratic_func, 1, 3)
        
        self.assertTrue(result.converged)
        self.assertAlmostEqual(result.root, 2.0, places=5)
        self.assertLess(abs(result.function_value), 1e-6)
    
    def test_bisection_no_sign_change(self):
        """Test bisección sin cambio de signo debe fallar"""
        with self.assertRaises(ValueError):
            self.finder.bisection_method(self.quadratic_func, 0, 1)
    
    def test_newton_raphson_quadratic(self):
        """Test Newton-Raphson con función cuadrática"""
        result = self.finder.newton_raphson_method(self.quadratic_func, None, 1.5)
        
        self.assertTrue(result.converged)
        self.assertAlmostEqual(result.root, 2.0, places=5)
        self.assertLess(abs(result.function_value), 1e-6)
    
    def test_fixed_point_simple(self):
        """Test punto fijo con función simple"""
        # Para f(x) = x**2 - x - 2, usar g(x) = sqrt(x + 2)
        g = lambda x: np.sqrt(x + 2) if x >= -2 else 0
        
        result = self.finder.fixed_point_method(g, 1.5)
        
        self.assertTrue(result.converged)
        self.assertAlmostEqual(result.root, 2.0, places=3)  # Menos precisión para punto fijo
    
    def test_create_function_from_string(self):
        """Test creación de función desde string"""
        f = create_function_from_string("x**2 - 4")
        
        self.assertAlmostEqual(f(2), 0, places=10)
        self.assertAlmostEqual(f(-2), 0, places=10)
        self.assertAlmostEqual(f(0), -4, places=10)
    
    def test_iteration_data_storage(self):
        """Test que se almacenan correctamente los datos de iteración"""
        result = self.finder.bisection_method(self.linear_func, 0, 3)
        
        self.assertIsNotNone(result.iteration_data)
        self.assertGreater(len(result.iteration_data), 0)
        
        # Verificar estructura de datos
        first_iteration = result.iteration_data[0]
        required_keys = ['iteration', 'a', 'b', 'c', 'f_c', 'error']
        for key in required_keys:
            self.assertIn(key, first_iteration)


class TestRootFindingAdvanced(unittest.TestCase):
    """Tests avanzados para casos edge y rendimiento"""
    
    def setUp(self):
        self.finder = RootFinder(tolerance=1e-8, max_iterations=200)
    
    def test_polynomial_multiple_roots(self):
        """Test con polinomio de múltiples raíces"""
        # (x-1)(x-2)(x-3) = x³ - 6x² + 11x - 6
        poly = lambda x: x**3 - 6*x**2 + 11*x - 6
        
        # Encontrar cada raíz
        root1 = self.finder.bisection_method(poly, 0.5, 1.5)
        root2 = self.finder.bisection_method(poly, 1.5, 2.5)
        root3 = self.finder.bisection_method(poly, 2.5, 3.5)
        
        self.assertAlmostEqual(root1.root, 1.0, places=6)
        self.assertAlmostEqual(root2.root, 2.0, places=6)
        self.assertAlmostEqual(root3.root, 3.0, places=6)
    
    def test_transcendental_function(self):
        """Test con función trascendental"""
        # f(x) = e^x - 2, raíz en ln(2) ≈ 0.693
        transcendental = lambda x: np.exp(x) - 2
        
        result = self.finder.newton_raphson_method(transcendental, None, 0.5)
        expected_root = np.log(2)
        
        self.assertTrue(result.converged)
        self.assertAlmostEqual(result.root, expected_root, places=6)
    
    def test_tolerance_precision(self):
        """Test que la tolerancia se respeta"""
        strict_finder = RootFinder(tolerance=1e-10, max_iterations=1000)
        
        result = strict_finder.bisection_method(lambda x: x**2 - 2, 1, 2)
        
        self.assertLess(result.error, 1e-10)
        self.assertLess(abs(result.function_value), 1e-10)
    
    def test_max_iterations_limit(self):
        """Test que se respeta el límite de iteraciones"""
        limited_finder = RootFinder(tolerance=1e-15, max_iterations=5)
        
        result = limited_finder.bisection_method(lambda x: x**2 - 2, 1, 2)
        
        self.assertFalse(result.converged)
        self.assertEqual(result.iterations, 5)


if __name__ == "__main__":
    # Configurar nivel de verbosidad
    unittest.main(verbosity=2)
