"""
Pruebas para el módulo de interpolación de Lagrange.
"""

import os
import sys
import unittest
import numpy as np
import math

# Añadir el directorio raíz al path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from lagrange_interpolation.lagrange import LagrangeInterpolation


class TestLagrangeInterpolation(unittest.TestCase):
    """Pruebas unitarias para la interpolación de Lagrange."""

    def test_basic_interpolation(self):
        """Prueba la interpolación básica con puntos simples."""
        # Definir puntos de prueba
        points = [(1, 1), (2, 4), (3, 9)]
        
        # Crear interpolador
        interp = LagrangeInterpolation(points)
        
        # Verificar que el polinomio pasa por los puntos originales
        for x, y in points:
            self.assertAlmostEqual(interp.interpolate(x), y, places=10)
        
        # Verificar interpolación en puntos intermedios (polinomio cuadrático)
        self.assertAlmostEqual(interp.interpolate(1.5), 2.25, places=10)
        self.assertAlmostEqual(interp.interpolate(2.5), 6.25, places=10)
    
    def test_trigonometric_function(self):
        """Prueba la interpolación de una función trigonométrica."""
        # Crear puntos a partir de la función seno
        x_values = np.linspace(0, 2*np.pi, 10)
        points = [(float(x), float(np.sin(x))) for x in x_values]
        
        # Crear interpolador
        interp = LagrangeInterpolation(points)
        
        # Verificar que el polinomio pasa por los puntos originales
        for x, y in points:
            self.assertAlmostEqual(interp.interpolate(x), y, places=10)
        
        # Verificar el error en puntos intermedios
        # (el error debe ser pequeño pero no necesariamente cero)
        test_points = np.linspace(0, 2*np.pi, 20)[1::2]  # Puntos entre los originales
        for x in test_points:
            error = abs(interp.interpolate(x) - np.sin(x))
            self.assertLess(error, 0.1)  # Error menor que 0.1
    
    def test_error_handling(self):
        """Prueba el manejo de errores."""
        # Crear interpolador vacío
        interp = LagrangeInterpolation()
        
        # Intentar interpolar sin puntos
        with self.assertRaises(ValueError):
            interp.interpolate(0)
        
        # Intentar crear interpolador con menos de 2 puntos
        with self.assertRaises(ValueError):
            interp.set_points([(1, 1)])
        
        # Intentar crear interpolador con valores x duplicados
        with self.assertRaises(ValueError):
            interp.set_points([(1, 1), (1, 2), (2, 3)])
    
    def test_polynomial_function(self):
        """Prueba la interpolación de un polinomio conocido."""
        # Polinomio de prueba: f(x) = 2x^2 - 3x + 1
        f = lambda x: 2*x**2 - 3*x + 1
        
        # Generar puntos
        x_values = np.linspace(-2, 2, 5)
        points = [(float(x), float(f(x))) for x in x_values]
        
        # Crear interpolador
        interp = LagrangeInterpolation(points)
        
        # Verificar en puntos intermedios
        test_points = np.linspace(-2, 2, 10)
        for x in test_points:
            expected = f(x)
            actual = interp.interpolate(x)
            self.assertAlmostEqual(actual, expected, places=10)
    
    def test_get_polynomial_function(self):
        """Prueba la obtención de una función para el polinomio."""
        # Definir puntos de prueba
        points = [(0, 1), (1, 3), (2, 2)]
        
        # Crear interpolador
        interp = LagrangeInterpolation(points)
        
        # Obtener función del polinomio
        poly_func = interp.get_polynomial_function()
        
        # Verificar que la función pasa por los puntos originales
        for x, y in points:
            self.assertAlmostEqual(poly_func(x), y, places=10)
    
    def test_error_bounds(self):
        """Prueba el cálculo de las cotas de error."""
        # Crear puntos a partir de la función seno
        x_values = np.linspace(0, np.pi, 5)
        points = [(float(x), float(np.sin(x))) for x in x_values]
        
        # Crear interpolador
        interp = LagrangeInterpolation(points)
        
        # Calcular cotas de error sin función original
        error_stats = interp.get_error_bounds()
        
        # El error en los puntos de interpolación debe ser cercano a cero
        self.assertLess(error_stats["max_error"], 1e-10)
        
        # Calcular cotas de error con función original
        error_stats = interp.get_error_bounds(
            func=np.sin, 
            a=0, 
            b=np.pi, 
            n_points=100
        )
        
        # Debe haber algún error en puntos que no son de interpolación
        self.assertGreater(error_stats["max_error"], 0)


if __name__ == "__main__":
    unittest.main()