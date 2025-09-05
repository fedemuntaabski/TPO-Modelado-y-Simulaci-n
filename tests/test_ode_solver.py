"""
Tests unitarios para los métodos de resolución de ODEs.

Verifica la precisión y estabilidad de los algoritmos de integración numérica
para ecuaciones diferenciales ordinarias.
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.core.ode_solver import ODESolver


class TestODESolver(unittest.TestCase):
    """Tests para métodos de resolución de ODEs"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.solver = ODESolver()
        
        # Ecuación simple: dy/dx = y, solución: y = y₀ * e^x
        self.simple_ode = lambda x, y: y
        self.simple_solution = lambda x, y0: y0 * np.exp(x)
        
        # Ecuación lineal: dy/dx = -2x, solución: y = -x² + C
        self.linear_ode = lambda x, y: -2*x
        self.linear_solution = lambda x, y0: -x**2 + y0
        
        # Ecuación oscilador: d²y/dx² + y = 0 -> dy/dx = z, dz/dx = -y
        # Solución: y = A*cos(x) + B*sin(x)
        self.oscillator_system = lambda x, state: np.array([state[1], -state[0]])
    
    def test_euler_simple(self):
        """Test método de Euler con ecuación simple"""
        x0, y0 = 0, 1
        x_end = 1
        step_size = 0.1
        
        result = self.solver.euler_method(self.simple_ode, x0, y0, x_end, step_size)
        
        # Valor exacto en x=1: e^1 ≈ 2.718
        exact_value = self.simple_solution(x_end, y0)
        
        self.assertEqual(result.method, "Método de Euler")
        self.assertAlmostEqual(result.step_size, step_size, places=10)
        
        # Euler es de primer orden, error considerable pero no excesivo
        error = abs(result.final_value - exact_value)
        self.assertLess(error, 0.5)  # Error razonable para h=0.1
    
    def test_euler_convergence(self):
        """Test convergencia de Euler al reducir step size"""
        x0, y0 = 0, 1
        x_end = 0.5
        exact_value = self.simple_solution(x_end, y0)
        
        step_sizes = [0.1, 0.05, 0.025]
        errors = []
        
        for h in step_sizes:
            result = self.solver.euler_method(self.simple_ode, x0, y0, x_end, h)
            error = abs(result.final_value - exact_value)
            errors.append(error)
        
        # Los errores deben decrecer
        self.assertGreater(errors[0], errors[1])
        self.assertGreater(errors[1], errors[2])
    
    def test_rk2_improved_accuracy(self):
        """Test que RK2 es más preciso que Euler"""
        x0, y0 = 0, 1
        x_end = 1
        step_size = 0.1
        exact_value = self.simple_solution(x_end, y0)
        
        euler_result = self.solver.euler_method(self.simple_ode, x0, y0, x_end, step_size)
        rk2_result = self.solver.rk2_method(self.simple_ode, x0, y0, x_end, step_size)
        
        euler_error = abs(euler_result.final_value - exact_value)
        rk2_error = abs(rk2_result.final_value - exact_value)
        
        # RK2 debe ser más preciso
        self.assertLess(rk2_error, euler_error)
        self.assertEqual(rk2_result.method, "Runge-Kutta 2do Orden")
    
    def test_rk4_high_accuracy(self):
        """Test alta precisión de RK4"""
        x0, y0 = 0, 1
        x_end = 1
        step_size = 0.1
        exact_value = self.simple_solution(x_end, y0)
        
        result = self.solver.rk4_method(self.simple_ode, x0, y0, x_end, step_size)
        
        error = abs(result.final_value - exact_value)
        self.assertLess(error, 0.001)  # RK4 muy preciso
        self.assertEqual(result.method, "Runge-Kutta 4to Orden")
    
    def test_heun_method(self):
        """Test método de Heun"""
        x0, y0 = 0, 2
        x_end = 0.5
        step_size = 0.05
        
        result = self.solver.heun_method(self.linear_ode, x0, y0, x_end, step_size)
        exact_value = self.linear_solution(x_end, y0)
        
        error = abs(result.final_value - exact_value)
        self.assertLess(error, 0.01)  # Buena precisión
        self.assertEqual(result.method, "Método de Heun")
    
    def test_solution_arrays_length(self):
        """Test que los arrays de solución tienen longitud correcta"""
        x0, y0 = 0, 1
        x_end = 1
        step_size = 0.2
        
        result = self.solver.euler_method(self.simple_ode, x0, y0, x_end, step_size)
        
        expected_points = int((x_end - x0) / step_size) + 1
        self.assertEqual(len(result.x_values), expected_points)
        self.assertEqual(len(result.y_values), expected_points)
        
        # Valores inicial y final correctos
        self.assertAlmostEqual(result.x_values[0], x0, places=10)
        self.assertAlmostEqual(result.x_values[-1], x_end, places=10)
        self.assertAlmostEqual(result.y_values[0], y0, places=10)
    
    def test_computation_data_storage(self):
        """Test que se almacenan los datos de computación"""
        result = self.solver.rk4_method(self.simple_ode, 0, 1, 0.5, 0.1)
        
        self.assertIsNotNone(result.computation_data)
        self.assertIn('k_values', result.computation_data)
        self.assertIn('iterations', result.computation_data)
    
    def test_adaptive_rk45_basic(self):
        """Test básico de RK45 adaptativo"""
        x0, y0 = 0, 1
        x_end = 1
        tolerance = 1e-6
        
        result = self.solver.adaptive_rk45(self.simple_ode, x0, y0, x_end, tolerance)
        exact_value = self.simple_solution(x_end, y0)
        
        error = abs(result.final_value - exact_value)
        self.assertLess(error, tolerance * 10)  # Error dentro de tolerancia
        self.assertEqual(result.method, "Runge-Kutta-Fehlberg 4(5)")
    
    def test_step_size_consistency(self):
        """Test consistencia del tamaño de paso"""
        step_size = 0.05
        result = self.solver.heun_method(self.simple_ode, 0, 1, 0.5, step_size)
        
        self.assertAlmostEqual(result.step_size, step_size, places=10)
        
        # Verificar espaciado uniforme en x_values
        x_diffs = np.diff(result.x_values)
        for diff in x_diffs:
            self.assertAlmostEqual(diff, step_size, places=8)


class TestODESystemSolver(unittest.TestCase):
    """Tests para sistemas de ODEs"""
    
    def setUp(self):
        self.solver = ODESolver()
        
        # Sistema oscilador: y'' + y = 0
        # Convertido a sistema: [y, y'] -> [y', -y]
        self.oscillator = lambda x, state: np.array([state[1], -state[0]])
    
    def test_oscillator_system_rk4(self):
        """Test sistema oscilador con RK4"""
        x0 = 0
        y0 = np.array([1, 0])  # y(0)=1, y'(0)=0 -> solución: y=cos(x)
        x_end = np.pi/2
        step_size = 0.01
        
        result = self.solver.rk4_method(self.oscillator, x0, y0, x_end, step_size)
        
        # En x=π/2, cos(π/2) = 0
        expected_y = 0
        error = abs(result.final_value[0] - expected_y)
        self.assertLess(error, 0.01)
    
    def test_system_dimensions(self):
        """Test dimensiones correctas para sistemas"""
        x0 = 0
        y0 = np.array([1, 0])
        x_end = 0.5
        step_size = 0.1
        
        result = self.solver.euler_method(self.oscillator, x0, y0, x_end, step_size)
        
        # Verificar que y_values es una matriz 2D
        self.assertEqual(result.y_values.shape[1], 2)  # 2 componentes
        
        # Primera componente debe ser array de posiciones
        # Segunda componente debe ser array de velocidades
        self.assertEqual(len(result.y_values[:, 0]), len(result.x_values))


class TestODEEdgeCases(unittest.TestCase):
    """Tests para casos especiales y límites"""
    
    def setUp(self):
        self.solver = ODESolver()
    
    def test_zero_step_interval(self):
        """Test con intervalo de paso cero"""
        result = self.solver.euler_method(lambda x, y: y, 0, 1, 0, 0.1)
        
        self.assertEqual(len(result.x_values), 1)
        self.assertEqual(len(result.y_values), 1)
        self.assertAlmostEqual(result.y_values[0], 1, places=10)
    
    def test_constant_function(self):
        """Test con función constante"""
        # dy/dx = 0 -> y = constante
        const_ode = lambda x, y: 0
        
        result = self.solver.rk4_method(const_ode, 0, 5, 2, 0.1)
        
        # Todos los valores y deben ser 5
        for y in result.y_values:
            self.assertAlmostEqual(y, 5, places=8)
    
    def test_large_step_size_stability(self):
        """Test estabilidad con paso grande"""
        # Usar ecuación simple con paso relativamente grande
        result = self.solver.rk4_method(lambda x, y: -y, 0, 1, 1, 0.5)
        
        # No debe producir valores infinitos o NaN
        self.assertTrue(np.all(np.isfinite(result.y_values)))
        self.assertFalse(np.any(np.isnan(result.y_values)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
