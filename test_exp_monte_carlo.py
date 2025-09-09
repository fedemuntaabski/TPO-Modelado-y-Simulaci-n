#!/usr/bin/env python3
"""
Script de prueba para la función exp(x) en Monte Carlo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.monte_carlo_engine import MonteCarloEngine
from src.core.function_parser import parse_function
import numpy as np

def test_exp_function():
    """Probar la función exp(x) con Monte Carlo"""
    print("=== Prueba de función exp(x) con Monte Carlo ===\n")

    # Crear motor Monte Carlo
    mc_engine = MonteCarloEngine()

    # Parsear función exp(x)
    try:
        func = parse_function("exp(x)", ["x"])
        print("✓ Función exp(x) parseada correctamente")
    except Exception as e:
        print(f"✗ Error al parsear función: {e}")
        return

    # Parámetros de prueba
    n_samples = 10000
    x_range = (0, 1)  # Integral de exp(x) de 0 a 1 = e - 1 ≈ 1.71828
    max_error = 0.05
    seed = 42

    print(f"Parámetros de simulación:")
    print(f"  Función: exp(x)")
    print(f"  Rango: {x_range}")
    print(f"  Muestras: {n_samples}")
    print(f"  Error máximo IC: {max_error}")
    print(f"  Semilla: {seed}")
    print()

    try:
        # Ejecutar simulación
        print("Ejecutando simulación...")
        results = mc_engine.simulate(
            func=func,
            n_samples=n_samples,
            seed=seed,
            max_error=max_error,
            dimensions=1,
            x_range=x_range,
            y_range=None
        )

        print("✓ Simulación completada exitosamente")
        print()

        # Mostrar resultados
        print("Resultados:")
        print(f"  Valor estimado: {results['resultado_integracion']:.6f}")
        print(f"  Error estándar: {results['error_estandar']:.6f}")
        ci_lower, ci_upper = results['intervalo_confianza']
        print(f"  Intervalo de confianza (95%): [{ci_lower:.6f}, {ci_upper:.6f}]")
        print(f"  Valor real (e-1): {np.exp(1) - 1:.6f}")
        real_value = np.exp(1) - 1
        error_relativo = abs(results['resultado_integracion'] - real_value) / real_value * 100
        print(f"  Error relativo: {error_relativo:.2f}%")

        # Verificar que el resultado esté dentro del intervalo de confianza
        if ci_lower <= real_value <= ci_upper:
            print("✓ El valor real está dentro del intervalo de confianza")
        else:
            print("✗ El valor real NO está dentro del intervalo de confianza")

        print()
        print("Estadísticas adicionales:")
        print(f"  Número de puntos dentro: {len(results['puntos_dentro'])}")
        print(f"  Número de puntos fuera: {len(results['puntos_fuera'])}")

    except Exception as e:
        print(f"✗ Error en simulación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_exp_function()
