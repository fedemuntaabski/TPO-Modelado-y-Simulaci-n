"""
Tests para la funcionalidad de Monte Carlo.

Verifica la correcta implementación del motor de simulación Monte Carlo.
"""

import unittest
import numpy as np
import math
from typing import Callable

from src.core.monte_carlo_engine import MonteCarloEngine


class TestMonteCarlo(unittest.TestCase):
    """Tests para el motor de simulación Monte Carlo"""
    
    def setUp(self):
        """Configuración inicial para pruebas"""
        self.mc_engine = MonteCarloEngine()
        
        # Función simple para testing: x^2
        self.test_func_1d = lambda x: x**2
        
        # Función simple para testing 2D: x^2 + y^2
        self.test_func_2d = lambda x, y: x**2 + y**2
        
        # Semilla para reproducibilidad
        self.seed = 42
        
        # Valores exactos conocidos de integrales
        # Integral de x^2 en [0,1] = 1/3
        self.exact_integral_1d = 1/3
        
        # Integral de x^2 + y^2 en [0,1]x[0,1] = 2/3
        self.exact_integral_2d = 2/3
    
    def test_monte_carlo_1d(self):
        """Test para integración 1D"""
        # Ejecutar simulación con un número moderado de muestras
        results = self.mc_engine.simulate(
            func=self.test_func_1d,
            n_samples=10000,
            seed=self.seed,
            dimensions=1,
            x_range=(0, 1)
        )
        
        # Verificar que el resultado está cerca del valor exacto (tolerancia 5%)
        error = abs(results['resultado_integracion'] - self.exact_integral_1d)
        relative_error = error / self.exact_integral_1d
        
        self.assertLess(relative_error, 0.05, 
                        f"Error relativo demasiado grande: {relative_error:.5f}")
        
        # Verificar que el intervalo de confianza contiene el valor exacto
        ci_lower, ci_upper = results['intervalo_confianza']
        self.assertTrue(ci_lower <= self.exact_integral_1d <= ci_upper,
                       "El intervalo de confianza no contiene el valor exacto")
    
    def test_monte_carlo_2d(self):
        """Test para integración 2D"""
        # Ejecutar simulación con un número moderado de muestras
        results = self.mc_engine.simulate(
            func=self.test_func_2d,
            n_samples=10000,
            seed=self.seed,
            dimensions=2,
            x_range=(0, 1),
            y_range=(0, 1)
        )
        
        # Verificar que el resultado está cerca del valor exacto (tolerancia 5%)
        error = abs(results['resultado_integracion'] - self.exact_integral_2d)
        relative_error = error / self.exact_integral_2d
        
        self.assertLess(relative_error, 0.05, 
                        f"Error relativo demasiado grande: {relative_error:.5f}")
        
        # Verificar que el intervalo de confianza contiene el valor exacto
        ci_lower, ci_upper = results['intervalo_confianza']
        self.assertTrue(ci_lower <= self.exact_integral_2d <= ci_upper,
                       "El intervalo de confianza no contiene el valor exacto")
    
    def test_monte_carlo_convergence(self):
        """Test para verificar la convergencia del método Monte Carlo"""
        # Realizar simulaciones con número creciente de muestras
        sample_sizes = [100, 1000, 10000]
        errors = []
        
        for n_samples in sample_sizes:
            results = self.mc_engine.simulate(
                func=self.test_func_1d,
                n_samples=n_samples,
                seed=self.seed,
                dimensions=1,
                x_range=(0, 1)
            )
            
            error = abs(results['resultado_integracion'] - self.exact_integral_1d)
            errors.append(error)
        
        # Verificar que el error disminuye con más muestras
        for i in range(1, len(errors)):
            self.assertLessEqual(errors[i], errors[i-1] * 1.5,
                               "No hay convergencia con mayor número de muestras")
    
    def test_volume_calculation(self):
        """Test para el cálculo del volumen del dominio"""
        # 1D
        volume_1d = self.mc_engine._calculate_volume(1, (0, 2))
        self.assertEqual(volume_1d, 2, "Volumen 1D incorrecto")
        
        # 2D
        volume_2d = self.mc_engine._calculate_volume(2, (0, 2), (0, 3))
        self.assertEqual(volume_2d, 6, "Volumen 2D incorrecto")
    
    def test_invalid_inputs(self):
        """Test para entradas inválidas"""
        # Probar número negativo de muestras
        with self.assertRaises(ValueError):
            self.mc_engine.simulate(
                func=self.test_func_1d,
                n_samples=-100,
                dimensions=1,
                x_range=(0, 1)
            )
        
        # Probar dimensión inválida
        with self.assertRaises(ValueError):
            self.mc_engine.simulate(
                func=self.test_func_1d,
                n_samples=100,
                dimensions=3,  # Solo se admiten 1 y 2
                x_range=(0, 1)
            )
        
        # Probar integración 2D sin rango y
        with self.assertRaises(ValueError):
            self.mc_engine.simulate(
                func=self.test_func_2d,
                n_samples=100,
                dimensions=2,
                x_range=(0, 1),
                y_range=None  # Falta rango y para 2D
            )


if __name__ == '__main__':
    unittest.main()
