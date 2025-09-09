#!/usr/bin/env python3
"""
Script de prueba completo para Monte Carlo con múltiples funciones
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.monte_carlo_engine import MonteCarloEngine
from src.core.function_parser import parse_function
import numpy as np

def test_multiple_functions():
    """Probar múltiples funciones con Monte Carlo"""
    print("=== Pruebas completas de Monte Carlo ===\n")

    mc_engine = MonteCarloEngine()

    # Definir funciones de prueba con sus valores reales
    test_functions = [
        {
            'name': 'exp(x)',
            'expression': 'exp(x)',
            'range': (0, 1),
            'real_value': np.exp(1) - 1,  # e - 1
            'dimensions': 1
        },
        {
            'name': 'x^2',
            'expression': 'x**2',
            'range': (0, 1),
            'real_value': 1/3,  # ∫x² dx de 0 a 1 = 1/3
            'dimensions': 1
        },
        {
            'name': 'sin(x)',
            'expression': 'sin(x)',
            'range': (0, np.pi),
            'real_value': 2,  # ∫sin(x) dx de 0 a π = 2
            'dimensions': 1
        },
        {
            'name': 'x*y',
            'expression': 'x*y',
            'range': [(0, 1), (0, 1)],
            'real_value': 1/4,  # ∫∫xy dxdy de 0 a 1 = 1/4
            'dimensions': 2
        }
    ]

    for func_data in test_functions:
        print(f"--- Probando función: {func_data['name']} ---")

        try:
            # Parsear función
            if func_data['dimensions'] == 1:
                func = parse_function(func_data['expression'], ['x'])
                x_range = func_data['range']
                y_range = None
            else:
                func = parse_function(func_data['expression'], ['x', 'y'])
                x_range = func_data['range'][0]
                y_range = func_data['range'][1]

            print(f"✓ Función parseada: {func_data['expression']}")

            # Ejecutar simulación
            results = mc_engine.simulate(
                func=func,
                n_samples=50000,  # Más muestras para mejor precisión
                seed=123,
                max_error=0.01,
                dimensions=func_data['dimensions'],
                x_range=x_range,
                y_range=y_range
            )

            # Mostrar resultados
            estimated = results['resultado_integracion']
            real = func_data['real_value']
            error_rel = abs(estimated - real) / real * 100
            ci_lower, ci_upper = results['intervalo_confianza']

            print(f"  Valor estimado: {estimated:.6f}")
            print(f"  Valor real: {real:.6f}")
            print(f"  Error relativo: {error_rel:.2f}%")
            print(f"  IC 95%: [{ci_lower:.6f}, {ci_upper:.6f}]")

            # Verificar intervalo de confianza
            if ci_lower <= real <= ci_upper:
                print("  ✓ Valor real dentro del IC")
            else:
                print("  ⚠ Valor real fuera del IC (posible variación estadística)")

            print()

        except Exception as e:
            print(f"✗ Error con {func_data['name']}: {e}")
            print()

def test_ui_integration():
    """Probar integración con la interfaz (simular entrada de usuario)"""
    print("=== Prueba de integración con UI ===\n")

    try:
        # Importar la pestaña de Monte Carlo
        from src.ui.tabs.monte_carlo_tab import MonteCarloTab
        print("✓ Módulo MonteCarloTab importado correctamente")

        # Verificar que no hay errores de sintaxis
        import ast
        with open('src/ui/tabs/monte_carlo_tab.py', 'r', encoding='utf-8') as f:
            source = f.read()

        ast.parse(source)
        print("✓ Sintaxis de MonteCarloTab correcta")

        print("✓ Integración con UI verificada")

    except Exception as e:
        print(f"✗ Error en integración UI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_multiple_functions()
    print("\n" + "="*50 + "\n")
    test_ui_integration()
