"""
Test específico para verificar el efecto del parámetro error_maximo en Monte Carlo.
"""

import unittest
import numpy as np
import sys
import os

# Añadir el directorio raíz del proyecto al path para poder importar desde src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.monte_carlo_engine import MonteCarloEngine

class TestMonteCarloErrorMaximo(unittest.TestCase):
    """Tests para verificar el efecto del parámetro error_maximo en Monte Carlo"""
    
    def setUp(self):
        """Configuración inicial para pruebas"""
        self.mc_engine = MonteCarloEngine()
        
        # Función simple para testing: x^2
        self.test_func = lambda x: x**2
        
        # Semilla para reproducibilidad
        self.seed = 42
        
        # Valor exacto de la integral
        self.exact_integral = 1/3  # Integral de x^2 en [0,1]
        
        # Número de muestras a utilizar
        self.n_samples = 10000
        
    def test_error_maximo_effect(self):
        """
        Test para verificar si el cambio en el parámetro error_maximo 
        afecta los resultados de la simulación Monte Carlo.
        """
        # Ejecutar simulaciones con diferentes valores de error_maximo
        error_values = [0.01, 0.05, 0.1, 0.2]
        results = []
        
        for error_max in error_values:
            result = self.mc_engine.simular(
                func=self.test_func,
                n=self.n_samples,
                semilla=self.seed,
                error_maximo=error_max,
                dimensiones=1,
                rango_x=(0, 1)
            )
            results.append(result)
        
        # Verificar si el error_maximo afecta el resultado de la integración
        for i in range(1, len(results)):
            self.assertEqual(
                results[0]['resultado_integracion'],
                results[i]['resultado_integracion'],
                "El resultado de la integración no debería cambiar con diferentes valores de error_maximo"
            )
        
        # Verificar si el error_maximo afecta el error estándar
        for i in range(1, len(results)):
            self.assertEqual(
                results[0]['error_estandar'],
                results[i]['error_estandar'],
                "El error estándar no debería cambiar con diferentes valores de error_maximo"
            )
        
        # Verificar si el error_maximo afecta el intervalo de confianza
        # Ahora esperamos que los intervalos sean diferentes con diferentes valores de error_maximo
        for i in range(1, len(results)):
            # El test original verificaba igualdad, ahora verificamos diferencia
            self.assertNotEqual(
                results[0]['intervalo_confianza'],
                results[i]['intervalo_confianza'],
                "El intervalo de confianza debería cambiar con diferentes valores de error_maximo"
            )
    
    def test_error_maximo_implementation(self):
        """
        Test para verificar cómo se implementa el parámetro error_maximo
        en el cálculo de estadísticas.
        """
        # Verificar si el error_maximo afecta la amplitud del intervalo de confianza
        # Si el error_maximo es utilizado correctamente, debería influir en la amplitud
        # del intervalo de confianza
        
        # Ejecutar simulaciones con valores extremos de error_maximo
        result_small_error = self.mc_engine.simular(
            func=self.test_func,
            n=self.n_samples,
            semilla=self.seed,
            error_maximo=0.01,  # Error pequeño
            dimensiones=1,
            rango_x=(0, 1)
        )
        
        result_large_error = self.mc_engine.simular(
            func=self.test_func,
            n=self.n_samples,
            semilla=self.seed,
            error_maximo=0.5,  # Error grande
            dimensiones=1,
            rango_x=(0, 1)
        )
        
        # Obtener los intervalos de confianza
        ci_small = result_small_error['intervalo_confianza']
        ci_large = result_large_error['intervalo_confianza']
        
        # Calcular las amplitudes de los intervalos
        width_small = ci_small[1] - ci_small[0]
        width_large = ci_large[1] - ci_large[0]
        
        # Si error_maximo afecta el intervalo, las amplitudes deberían ser diferentes
        # Un error máximo mayor debería resultar en un intervalo más estrecho
        # (porque permite más error, así que requiere menos confianza)
        self.assertLess(
            width_large, width_small,
            "Un error_maximo mayor debería resultar en un intervalo de confianza más estrecho"
        )
        
        # Imprimir mensaje informativo sobre cómo se está utilizando error_maximo
        print("\nResultado del test: El parámetro error_maximo afecta correctamente el cálculo del intervalo de confianza.")
        print(f"Amplitud del IC con error_maximo=0.01: {width_small}")
        print(f"Amplitud del IC con error_maximo=0.5: {width_large}")
        print("El parámetro error_maximo se utiliza para determinar el nivel de confianza en los cálculos estadísticos.")

if __name__ == '__main__':
    unittest.main()