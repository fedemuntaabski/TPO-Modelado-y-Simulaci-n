"""
Tests unitarios para los métodos de integración numérica.

Verifica la precisión y corrección de los algoritmos de integración.
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.core.integration import NumericalIntegrator


class TestIntegration(unittest.TestCase):
    """Tests para métodos de integración numérica"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.integrator = NumericalIntegrator(use_scipy=False)  # Sin scipy para tests aislados
        
        # Funciones de prueba con integrales conocidas
        self.constant_func = lambda x: 1  # ∫1 dx = x
        self.linear_func = lambda x: x    # ∫x dx = x²/2
        self.quadratic_func = lambda x: x**2  # ∫x² dx = x³/3
        self.sine_func = lambda x: np.sin(x)  # ∫sin(x) dx = -cos(x)
    
    def test_trapezoid_constant(self):
        """Test trapecio con función constante"""
        result = self.integrator.trapezoid_rule(self.constant_func, 0, 2, 10)
        
        expected = 2.0  # ∫₀² 1 dx = 2
        self.assertAlmostEqual(result.value, expected, places=6)
        self.assertEqual(result.method, "Regla del Trapecio")
        self.assertEqual(result.subdivisions, 10)
    
    def test_trapezoid_linear(self):
        """Test trapecio con función lineal"""
        result = self.integrator.trapezoid_rule(self.linear_func, 0, 2, 20)
        
        expected = 2.0  # ∫₀² x dx = x²/2 |₀² = 2
        self.assertAlmostEqual(result.value, expected, places=4)
    
    def test_simpson_13_quadratic(self):
        """Test Simpson 1/3 con función cuadrática (debe ser exacto)"""
        result = self.integrator.simpson_13_rule(self.quadratic_func, 0, 3, 6)
        
        expected = 9.0  # ∫₀³ x² dx = x³/3 |₀³ = 9
        self.assertAlmostEqual(result.value, expected, places=8)
    
    def test_simpson_13_adjusts_n(self):
        """Test que Simpson 1/3 ajusta n a par"""
        result = self.integrator.simpson_13_rule(self.linear_func, 0, 1, 5)  # n impar
        
        # Debe ajustar a n=6
        self.assertEqual(result.subdivisions, 6)
    
    def test_simpson_38_cubic_exact(self):
        """Test Simpson 3/8 con función cúbica"""
        cubic_func = lambda x: x**3
        result = self.integrator.simpson_38_rule(cubic_func, 0, 2, 6)
        
        expected = 4.0  # ∫₀² x³ dx = x⁴/4 |₀² = 4
        self.assertAlmostEqual(result.value, expected, places=6)
    
    def test_simpson_38_adjusts_n(self):
        """Test que Simpson 3/8 ajusta n a múltiplo de 3"""
        result = self.integrator.simpson_38_rule(self.linear_func, 0, 1, 7)  # No múltiplo de 3
        
        # Debe ajustar a n=9
        self.assertEqual(result.subdivisions, 9)
    
    def test_convergence_with_refinement(self):
        """Test convergencia al refinar la malla"""
        # Usar función suave
        smooth_func = lambda x: np.exp(-x**2)
        
        # Diferentes niveles de refinamiento
        n_values = [10, 20, 40]
        errors = []
        
        for n in n_values:
            result = self.integrator.simpson_13_rule(smooth_func, 0, 1, n)
            # Como no tenemos valor exacto, usamos alta precisión como referencia
            reference = self.integrator.simpson_13_rule(smooth_func, 0, 1, 1000)
            error = abs(result.value - reference.value)
            errors.append(error)
        
        # Los errores deben decrecer
        self.assertGreater(errors[0], errors[1])
        self.assertGreater(errors[1], errors[2])
    
    def test_computation_data_storage(self):
        """Test que se almacenan los datos de computación"""
        result = self.integrator.trapezoid_rule(self.linear_func, 0, 1, 4)
        
        self.assertIsNotNone(result.computation_data)
        self.assertIn('x_values', result.computation_data)
        self.assertIn('y_values', result.computation_data)
        self.assertIn('formula', result.computation_data)
    
    def test_step_size_calculation(self):
        """Test cálculo correcto del tamaño de paso"""
        result = self.integrator.trapezoid_rule(self.constant_func, 0, 5, 10)
        
        expected_h = 0.5  # (5-0)/10 = 0.5
        self.assertAlmostEqual(result.step_size, expected_h, places=10)


class TestIntegrationAdvanced(unittest.TestCase):
    """Tests avanzados para casos especiales"""
    
    def setUp(self):
        self.integrator = NumericalIntegrator(use_scipy=False)
    
    def test_oscillatory_function(self):
        """Test con función oscilatoria"""
        # ∫₀^π sin(x) dx = 2
        result = self.integrator.simpson_13_rule(self.sine_func, 0, np.pi, 100)
        
        expected = 2.0
        self.assertAlmostEqual(result.value, expected, places=4)
    
    def test_negative_interval(self):
        """Test con intervalo que incluye valores negativos"""
        result = self.integrator.trapezoid_rule(lambda x: x**2, -2, 2, 20)
        
        expected = 16.0/3  # ∫₋₂² x² dx = 16/3
        self.assertAlmostEqual(result.value, expected, places=3)
    
    def test_zero_width_interval(self):
        """Test con intervalo de ancho cero"""
        result = self.integrator.trapezoid_rule(self.linear_func, 1, 1, 10)
        
        self.assertAlmostEqual(result.value, 0.0, places=10)
        self.assertEqual(result.step_size, 0.0)
    
    def test_single_subdivision(self):
        """Test con una sola subdivisión"""
        result = self.integrator.trapezoid_rule(self.linear_func, 0, 2, 1)
        
        # Con n=1, trapecio da (f(0) + f(2))/2 * 2 = (0 + 2)/2 * 2 = 2
        self.assertAlmostEqual(result.value, 2.0, places=10)
        self.assertEqual(result.subdivisions, 1)
    
    def test_adaptive_simpson_basic(self):
        """Test básico de Simpson adaptativo"""
        result = self.integrator.adaptive_simpson(self.quadratic_func, 0, 1, tolerance=1e-6)
        
        expected = 1.0/3  # ∫₀¹ x² dx = 1/3
        self.assertAlmostEqual(result.value, expected, places=5)
        self.assertEqual(result.method, "Simpson Adaptativo")
    
    def test_method_comparison_consistency(self):
        """Test que los métodos dan resultados consistentes"""
        # Para una función suave, Simpson debe ser más preciso que trapecio
        func = lambda x: x**4
        a, b = 0, 1
        n = 20
        
        trap_result = self.integrator.trapezoid_rule(func, a, b, n)
        simp_result = self.integrator.simpson_13_rule(func, a, b, n)
        
        expected = 0.2  # ∫₀¹ x⁴ dx = 1/5
        
        trap_error = abs(trap_result.value - expected)
        simp_error = abs(simp_result.value - expected)
        
        # Simpson debe ser más preciso
        self.assertLess(simp_error, trap_error)


if __name__ == "__main__":
    unittest.main(verbosity=2)
