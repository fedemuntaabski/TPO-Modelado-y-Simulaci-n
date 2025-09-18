#!/usr/bin/env python
"""
Test para verificar cómo diferentes valores de tolerancia
afectan a los resultados del método de Aitken.
"""

import math
import numpy as np
from aitken_app import AitkenAcceleration, format_8_decimals

def test_tolerances():
    """Prueba diferentes tolerancias y muestra cómo afectan al resultado."""
    
    print("="*70)
    print("TEST DE TOLERANCIA PARA MÉTODO DE AITKEN")
    print("="*70)
    
    # Función de prueba: g(x) = cos(x) 
    # (converge al punto fijo x ≈ 0.73908513)
    g_function = lambda x: math.cos(x)
    x0 = 0.5
    
    # Lista de tolerancias a probar (de más estricta a menos estricta)
    tolerances = [1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1e-1]
    
    # Título de la tabla
    print(f"{'Tolerancia':<12} {'Resultado':<15} {'Error final':<15} {'Iteraciones':<12} {'Convergió':<10}")
    print("-"*70)
    
    # Probar cada tolerancia
    for tol in tolerances:
        # Crear instancia con la tolerancia específica
        aitken = AitkenAcceleration(tolerance=tol, max_iterations=20)
        
        # Ejecutar Aitken
        result = aitken.accelerate(g_function, x0)
        
        # Mostrar resultados
        converged = "SÍ" if result['converged'] else "NO"
        print(f"{tol:<12.1e} {format_8_decimals(result['root']):<15} "
              f"{result['error']:<15.8f} {result['iterations']:<12} {converged:<10}")
        
        # Mostrar tabla de iteraciones para cada tolerancia
        print("\nTabla de iteraciones:")
        print(f"{'Iter':<5} {'x_aitken':<15} {'Error (%)':<15}")
        print("-"*40)
        for data in result['iteration_data']:
            print(f"{data['iteration']:<5} {format_8_decimals(data['x_aitken']):<15} "
                  f"{data['error']:<15.8f}")
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_tolerances()
