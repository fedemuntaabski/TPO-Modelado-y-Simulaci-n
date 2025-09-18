#!/usr/bin/env python
"""
Test detallado para verificar cómo diferentes valores de tolerancia
afectan a los resultados del método de Aitken con una función más compleja.
"""

import math
import numpy as np
from aitken_app import AitkenAcceleration, format_8_decimals

def test_complex_function_tolerances():
    """Prueba diferentes tolerancias con una función más compleja."""
    
    print("="*70)
    print("TEST DE TOLERANCIA PARA MÉTODO DE AITKEN - FUNCIÓN COMPLEJA")
    print("="*70)
    
    # Función más compleja: g(x) = 0.5*(x + 10/x)
    # Esta función converge a sqrt(10) ≈ 3.16227766
    g_function = lambda x: 0.5 * (x + 10/x)
    x0 = 4.0  # Valor inicial relativamente lejano
    exact_value = math.sqrt(10)  # Valor exacto para comparar
    
    # Lista de tolerancias a probar (de más estricta a menos estricta)
    tolerances = [1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1e-1, 1]
    
    # Título de la tabla de resultados
    print(f"{'Tolerancia':<12} {'Resultado':<15} {'Error final':<15} {'Iteraciones':<12} {'Error vs exacto':<15}")
    print("-"*70)
    
    # Probar cada tolerancia
    for tol in tolerances:
        # Crear instancia con la tolerancia específica
        aitken = AitkenAcceleration(tolerance=tol, max_iterations=20)
        
        # Ejecutar Aitken
        result = aitken.accelerate(g_function, x0)
        
        # Calcular error respecto al valor exacto
        error_vs_exact = abs(result['root'] - exact_value) / abs(exact_value) * 100
        
        # Mostrar resultados
        print(f"{tol:<12.1e} {format_8_decimals(result['root']):<15} "
              f"{result['error']:<15.8f} {result['iterations']:<12} "
              f"{error_vs_exact:<15.8f}%")
        
        # Mostrar tabla de iteraciones para cada tolerancia
        print("\nTabla de iteraciones:")
        print(f"{'Iter':<5} {'x_aitken':<15} {'Error (%)':<15}")
        print("-"*40)
        for data in result['iteration_data']:
            print(f"{data['iteration']:<5} {format_8_decimals(data['x_aitken']):<15} "
                  f"{data['error']:<15.8f}")
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_complex_function_tolerances()