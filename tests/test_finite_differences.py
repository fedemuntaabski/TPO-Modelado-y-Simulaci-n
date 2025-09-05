"""
Tests unitarios para los métodos de diferencias finitas.

Verifica la precisión y convergencia de los algoritmos de diferenciación numérica.
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.core.finite_differences import FiniteDifferenceCalculator, FiniteDifferences


class TestFiniteDifferences(unittest.TestCase):
    """Tests para métodos de diferencias finitas"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.calculator = FiniteDifferenceCalculator()
        
        # Funciones de prueba con derivadas conocidas
        self.linear_func = lambda x: 3*x + 2  # f'(x) = 3
        self.quadratic_func = lambda x: x**2  # f'(x) = 2x
        self.cubic_func = lambda x: x**3      # f'(x) = 3x²
        self.sine_func = lambda x: np.sin(x)  # f'(x) = cos(x)
        self.exp_func = lambda x: np.exp(x)   # f'(x) = exp(x)
    
    def test_forward_difference_linear(self):
        """Test diferencia hacia adelante con función lineal"""
        x = 2.0
        h = 0.1
        
        result = self.calculator.forward_difference(self.linear_func, x, h)
        
        expected = 3.0  # Derivada exacta de 3x + 2
        self.assertAlmostEqual(result.value, expected, places=8)
        self.assertEqual(result.method, "Diferencia Hacia Adelante")
        self.assertEqual(result.step_size, h)
    
    def test_backward_difference_quadratic(self):
        """Test diferencia hacia atrás con función cuadrática"""
        x = 3.0
        h = 0.01
        
        result = self.calculator.backward_difference(self.quadratic_func, x, h)
        
        expected = 6.0  # f'(3) = 2*3 = 6
        self.assertAlmostEqual(result.value, expected, places=3)
        self.assertEqual(result.method, "Diferencia Hacia Atrás")
    
    def test_central_difference_accuracy(self):
        """Test que diferencia central es más precisa"""
        x = 1.0
        h = 0.1
        
        forward_result = self.calculator.forward_difference(self.cubic_func, x, h)
        backward_result = self.calculator.backward_difference(self.cubic_func, x, h)
        central_result = self.calculator.central_difference(self.cubic_func, x, h)
        
        expected = 3.0  # f'(1) = 3*1² = 3
        
        forward_error = abs(forward_result.value - expected)
        backward_error = abs(backward_result.value - expected)
        central_error = abs(central_result.value - expected)
        
        # Diferencia central debe ser más precisa
        self.assertLess(central_error, forward_error)
        self.assertLess(central_error, backward_error)
        self.assertEqual(central_result.method, "Diferencia Central")
    
    def test_five_point_stencil_high_accuracy(self):
        """Test fórmula de 5 puntos para alta precisión"""
        x = 2.0
        h = 0.1
        
        result = self.calculator.five_point_stencil(self.cubic_func, x, h)
        
        expected = 12.0  # f'(2) = 3*2² = 12
        self.assertAlmostEqual(result.value, expected, places=5)
        self.assertEqual(result.method, "Fórmula de 5 Puntos")
    
    def test_convergence_with_smaller_h(self):
        """Test convergencia al reducir h"""
        x = 1.5
        exact_derivative = np.cos(x)  # f'(sin(x)) = cos(x)
        
        h_values = [0.1, 0.01, 0.001]
        errors = []
        
        for h in h_values:
            result = self.calculator.central_difference(self.sine_func, x, h)
            error = abs(result.value - exact_derivative)
            errors.append(error)
        
        # Los errores deben decrecer
        self.assertGreater(errors[0], errors[1])
        self.assertGreater(errors[1], errors[2])
    
    def test_richardson_extrapolation(self):
        """Test extrapolación de Richardson"""
        x = 1.0
        h = 0.1
        
        result = self.calculator.richardson_extrapolation(self.exp_func, x, h)
        
        expected = np.exp(x)  # f'(e^x) = e^x
        self.assertAlmostEqual(result.value, expected, places=6)
        self.assertEqual(result.method, "Extrapolación de Richardson")
    
    def test_computation_data_storage(self):
        """Test que se almacenan los datos de computación"""
        result = self.calculator.central_difference(self.quadratic_func, 2, 0.1)
        
        self.assertIsNotNone(result.computation_data)
        self.assertIn('function_evaluations', result.computation_data)
        self.assertIn('points_used', result.computation_data)
        self.assertIn('formula', result.computation_data)
    
    def test_step_size_storage(self):
        """Test almacenamiento correcto del tamaño de paso"""
        h = 0.05
        result = self.calculator.forward_difference(self.linear_func, 1, h)
        
        self.assertEqual(result.step_size, h)
    
    def test_adaptive_step_basic(self):
        """Test paso adaptativo básico"""
        x = 1.0
        tolerance = 1e-6
        
        result = self.calculator.adaptive_step_derivative(self.exp_func, x, tolerance)
        
        expected = np.exp(x)
        error = abs(result.value - expected)
        self.assertLess(error, tolerance * 10)  # Error dentro de tolerancia
        self.assertEqual(result.method, "Paso Adaptativo")


class TestFiniteDifferencesAdvanced(unittest.TestCase):
    """Tests avanzados para casos especiales"""
    
    def setUp(self):
        self.calculator = FiniteDifferenceCalculator()
    
    def test_oscillatory_function(self):
        """Test con función oscilatoria"""
        # f(x) = sin(5x), f'(x) = 5*cos(5x)
        func = lambda x: np.sin(5*x)
        x = np.pi/4
        h = 0.01
        
        result = self.calculator.five_point_stencil(func, x, h)
        expected = 5 * np.cos(5*x)
        
        error = abs(result.value - expected)
        self.assertLess(error, 0.01)
    
    def test_polynomial_exact_derivatives(self):
        """Test que las derivadas de polinomios son exactas (orden suficiente)"""
        # Para polinomio cuadrático, diferencia central debería ser muy precisa
        poly = lambda x: 2*x**2 + 3*x + 1  # f'(x) = 4x + 3
        x = 2.5
        h = 0.1
        
        result = self.calculator.central_difference(poly, x, h)
        expected = 4*x + 3  # = 13
        
        self.assertAlmostEqual(result.value, expected, places=8)
    
    def test_method_order_comparison(self):
        """Test comparación de orden de métodos"""
        func = lambda x: x**4  # f'(x) = 4x³
        x = 1.5
        h = 0.1
        expected = 4 * x**3
        
        forward_result = self.calculator.forward_difference(func, x, h)
        central_result = self.calculator.central_difference(func, x, h)
        five_point_result = self.calculator.five_point_stencil(func, x, h)
        
        forward_error = abs(forward_result.value - expected)
        central_error = abs(central_result.value - expected)
        five_point_error = abs(five_point_result.value - expected)
        
        # Orden de precisión: 5-puntos > central > forward
        self.assertLess(five_point_error, central_error)
        self.assertLess(central_error, forward_error)
    
    def test_boundary_behavior(self):
        """Test comportamiento en extremos del dominio"""
        func = lambda x: x**3
        x_values = [0, 0.1, 10, 100]  # Diferentes escalas
        h = 0.01
        
        for x in x_values:
            result = self.calculator.central_difference(func, x, h)
            expected = 3 * x**2
            
            if x == 0:
                # En x=0, la derivada debe ser 0
                self.assertAlmostEqual(result.value, 0, places=5)
            else:
                # Error relativo debe ser pequeño
                relative_error = abs(result.value - expected) / abs(expected)
                self.assertLess(relative_error, 0.01)


class TestFiniteDifferencesEdgeCases(unittest.TestCase):
    """Tests para casos límite y especiales"""
    
    def setUp(self):
        self.calculator = FiniteDifferenceCalculator()
    
    def test_constant_function(self):
        """Test con función constante (derivada = 0)"""
        const_func = lambda x: 5
        
        result = self.calculator.central_difference(const_func, 2, 0.1)
        
        self.assertAlmostEqual(result.value, 0, places=10)
    
    def test_very_small_step_size(self):
        """Test con tamaño de paso muy pequeño"""
        func = lambda x: x**2
        x = 1
        h = 1e-10
        
        result = self.calculator.central_difference(func, x, h)
        
        # Puede haber errores de redondeo, pero no debe explotar
        self.assertTrue(np.isfinite(result.value))
        self.assertFalse(np.isnan(result.value))
    
    def test_very_large_step_size(self):
        """Test con tamaño de paso grande"""
        func = lambda x: np.sin(x)
        x = 1
        h = 1  # Paso grande
        
        result = self.calculator.forward_difference(func, x, h)
        
        # Debe dar un resultado finito (aunque impreciso)
        self.assertTrue(np.isfinite(result.value))
        self.assertFalse(np.isnan(result.value))
    
    def test_discontinuous_function_handling(self):
        """Test comportamiento con función discontinua"""
        # Función escalón
        step_func = lambda x: 1 if x >= 0 else 0
        
        # En el punto de discontinuidad
        result = self.calculator.central_difference(step_func, 0, 0.01)
        
        # Debe manejar la discontinuidad sin errores
        self.assertTrue(np.isfinite(result.value))
    
    def test_zero_step_size_handling(self):
        """Test manejo de paso cero"""
        func = lambda x: x**2
        
        with self.assertRaises(ValueError):
            self.calculator.central_difference(func, 1, 0)
    
    def test_negative_step_size(self):
        """Test con tamaño de paso negativo"""
        func = lambda x: x**2
        
        # Debe manejar paso negativo tomando valor absoluto
        result = self.calculator.central_difference(func, 1, -0.1)
        expected_result = self.calculator.central_difference(func, 1, 0.1)
        
        self.assertAlmostEqual(result.value, expected_result.value, places=10)


class TestNewFiniteDifferences(unittest.TestCase):
    """Tests para la nueva clase FiniteDifferences según prompt"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.calculator = FiniteDifferences()
        
        # Funciones de prueba con derivadas conocidas
        self.linear_func = lambda x: 3*x + 2  # f'(x) = 3
        self.quadratic_func = lambda x: x**2  # f'(x) = 2x
        self.cubic_func = lambda x: x**3      # f'(x) = 3x²
        self.sine_func = lambda x: np.sin(x)  # f'(x) = cos(x)
    
    def test_progressive_method(self):
        """Test método progresivo"""
        x = 2.0
        h = 0.1
        
        result = self.calculator.progressive_method(x, h, self.linear_func)
        
        # Verificar estructura del resultado
        self.assertIn('method', result)
        self.assertIn('x', result)
        self.assertIn('h', result)
        self.assertIn('fx', result)
        self.assertIn('fx_plus_h', result)
        self.assertIn('derivative', result)
        self.assertIn('error_order', result)
        self.assertIn('formula', result)
        
        # Verificar valores
        self.assertEqual(result['method'], 'progressive')
        self.assertEqual(result['x'], x)
        self.assertEqual(result['h'], h)
        self.assertEqual(result['error_order'], 'O(h)')
        self.assertEqual(result['formula'], "f'(x) ≈ [f(x+h) - f(x)] / h")
        
        # Para función lineal, la derivada debe ser exacta (3.0)
        self.assertAlmostEqual(result['derivative'], 3.0, places=10)
    
    def test_regressive_method(self):
        """Test método regresivo"""
        x = 2.0
        h = 0.1
        
        result = self.calculator.regressive_method(x, h, self.linear_func)
        
        # Verificar estructura del resultado
        self.assertIn('method', result)
        self.assertIn('fx_minus_h', result)
        
        # Verificar valores específicos
        self.assertEqual(result['method'], 'regressive')
        self.assertEqual(result['error_order'], 'O(h)')
        self.assertEqual(result['formula'], "f'(x) ≈ [f(x) - f(x-h)] / h")
        
        # Para función lineal, la derivada debe ser exacta (3.0)
        self.assertAlmostEqual(result['derivative'], 3.0, places=10)
    
    def test_central_method(self):
        """Test método central"""
        x = 2.0
        h = 0.1
        
        result = self.calculator.central_method(x, h, self.quadratic_func)
        
        # Verificar estructura del resultado
        self.assertIn('fx_plus_h', result)
        self.assertIn('fx_minus_h', result)
        
        # Verificar valores específicos
        self.assertEqual(result['method'], 'central')
        self.assertEqual(result['error_order'], 'O(h²)')
        self.assertEqual(result['formula'], "f'(x) ≈ [f(x+h) - f(x-h)] / (2h)")
        
        # Para x²: f'(2) = 4.0
        expected = 4.0
        self.assertAlmostEqual(result['derivative'], expected, places=8)
    
    def test_calculate_single_point(self):
        """Test cálculo de punto único con método seleccionado"""
        x = 1.0
        h = 0.01
        
        # Test método progresivo
        result_prog = self.calculator.calculate_single_point(x, h, self.quadratic_func, 'progressive')
        self.assertEqual(result_prog['method'], 'progressive')
        
        # Test método regresivo
        result_reg = self.calculator.calculate_single_point(x, h, self.quadratic_func, 'regressive')
        self.assertEqual(result_reg['method'], 'regressive')
        
        # Test método central
        result_cent = self.calculator.calculate_single_point(x, h, self.quadratic_func, 'central')
        self.assertEqual(result_cent['method'], 'central')
        
        # El método central debe tener mayor precisión
        expected = 2.0  # f'(1) para x²
        error_prog = abs(result_prog['derivative'] - expected)
        error_reg = abs(result_reg['derivative'] - expected)
        error_cent = abs(result_cent['derivative'] - expected)
        
        self.assertLess(error_cent, error_prog)
        self.assertLess(error_cent, error_reg)
    
    def test_auto_calculate_list(self):
        """Test cálculo automático por lista"""
        # Crear lista de puntos de datos
        data_points = [
            {"x": 1.0, "h": 0.1, "fx": 1.0},      # Primer punto: progresivo
            {"x": 1.1, "h": 0.1, "fx": 1.21},     # Intermedio: central
            {"x": 1.2, "h": 0.1, "fx": 1.44},     # Intermedio: central
            {"x": 1.3, "h": 0.1, "fx": 1.69}      # Último: regresivo
        ]
        
        results = self.calculator.auto_calculate_list(data_points)
        
        # Verificar número de resultados
        self.assertEqual(len(results), 4)
        
        # Verificar selección automática de métodos
        self.assertEqual(results[0].get('auto_selected_method'), 'progressive')
        self.assertEqual(results[1].get('auto_selected_method'), 'central')
        self.assertEqual(results[2].get('auto_selected_method'), 'central')
        self.assertEqual(results[3].get('auto_selected_method'), 'regressive')
        
        # Verificar información de posición
        for i, result in enumerate(results):
            self.assertEqual(result['position_in_list'], i)
            self.assertEqual(result['total_points'], 4)
    
    def test_validate_input_data(self):
        """Test validación de datos de entrada"""
        # Datos válidos
        valid_data = [
            {"x": 1.0, "h": 0.1, "fx": 2.0},
            {"x": 1.1, "h": 0.1, "fx": 2.2}
        ]
        self.assertTrue(self.calculator.validate_input_data(valid_data))
        
        # Datos inválidos: lista vacía
        with self.assertRaises(ValueError):
            self.calculator.validate_input_data([])
        
        # Datos inválidos: falta key 'x'
        invalid_data1 = [{"h": 0.1, "fx": 2.0}]
        with self.assertRaises(ValueError):
            self.calculator.validate_input_data(invalid_data1)
        
        # Datos inválidos: h negativo
        invalid_data2 = [{"x": 1.0, "h": -0.1, "fx": 2.0}]
        with self.assertRaises(ValueError):
            self.calculator.validate_input_data(invalid_data2)
        
        # Datos inválidos: sin fx ni function
        invalid_data3 = [{"x": 1.0, "h": 0.1}]
        with self.assertRaises(ValueError):
            self.calculator.validate_input_data(invalid_data3)
    
    def test_get_method_info(self):
        """Test información de métodos"""
        info = self.calculator.get_method_info()
        
        # Verificar que tiene los tres métodos
        self.assertIn('progressive', info)
        self.assertIn('regressive', info)
        self.assertIn('central', info)
        
        # Verificar estructura de información
        for method_info in info.values():
            self.assertIn('name', method_info)
            self.assertIn('formula', method_info)
            self.assertIn('error_order', method_info)
            self.assertIn('best_for', method_info)
            self.assertIn('points_needed', method_info)
            self.assertIn('points_pattern', method_info)
    
    def test_error_handling(self):
        """Test manejo de errores"""
        # h = 0 debe lanzar error
        with self.assertRaises(ValueError):
            self.calculator.progressive_method(1.0, 0.0, self.linear_func)
        
        # h negativo debe lanzar error
        with self.assertRaises(ValueError):
            self.calculator.regressive_method(1.0, -0.1, self.linear_func)
        
        # Método inválido en calculate_single_point
        with self.assertRaises(ValueError):
            self.calculator.calculate_single_point(1.0, 0.1, self.linear_func, 'invalid_method')
    
    def test_precision_comparison(self):
        """Test comparación de precisión entre métodos"""
        x = 1.0
        h = 0.01
        func = self.cubic_func  # f(x) = x³, f'(x) = 3x²
        expected = 3.0  # f'(1) = 3
        
        # Calcular con todos los métodos
        result_prog = self.calculator.progressive_method(x, h, func)
        result_reg = self.calculator.regressive_method(x, h, func)
        result_cent = self.calculator.central_method(x, h, func)
        
        # Calcular errores
        error_prog = abs(result_prog['derivative'] - expected)
        error_reg = abs(result_reg['derivative'] - expected)
        error_cent = abs(result_cent['derivative'] - expected)
        
        # El método central debe ser más preciso para funciones suaves
        self.assertLess(error_cent, error_prog)
        self.assertLess(error_cent, error_reg)
        
        # Los errores deben estar en el orden esperado
        self.assertLess(error_cent, h)      # O(h²)
        self.assertLess(error_prog, 1.0)    # O(h)
        self.assertLess(error_reg, 1.0)     # O(h)


if __name__ == "__main__":
    unittest.main(verbosity=2)
