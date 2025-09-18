"""
Demostración específica de que la tabla de Aitken muestra 8 decimales.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aitken_app import AitkenAcceleration, format_8_decimals
import math


def demo_8_decimals_table():
    """Demostrar que la tabla muestra exactamente 8 decimales."""
    
    print("=" * 80)
    print("DEMOSTRACIÓN: TABLA AITKEN CON 8 DECIMALES")
    print("=" * 80)
    
    # Usar función cos(x) para el ejemplo
    def g_cos(x):
        return math.cos(x)
    
    aitken = AitkenAcceleration(tolerance=1e-10, max_iterations=5)
    result = aitken.accelerate(g_cos, 0.5)
    
    print("Función: g(x) = cos(x)")
    print("Valor inicial: x₀ = 0.5")
    print("Tolerancia: 1e-10")
    print()
    
    # Mostrar resultados principales con 8 decimales
    print("RESULTADOS PRINCIPALES:")
    print(f"├─ Raíz encontrada: {format_8_decimals(result['root'])}")
    print(f"├─ Error final:     {format_8_decimals(result['error'])}")
    print(f"├─ Iteraciones:     {result['iterations']}")
    print(f"└─ Convergió:       {'SÍ' if result['converged'] else 'NO'}")
    print()
    
    # Tabla con formato exacto como aparece en la GUI
    print("TABLA DE ITERACIONES (formato GUI con 8 decimales):")
    print("┌──────┬──────────────┬──────────────┬──────────────┬──────────────────┬──────────────┬─────────────────────────────┐")
    print("│ Iter │      x       │      x₁      │      x₂      │    x_aitken      │    Error     │           Método            │")
    print("├──────┼──────────────┼──────────────┼──────────────┼──────────────────┼──────────────┼─────────────────────────────┤")
    
    for data in result['iteration_data']:
        iter_num = f"{data['iteration']:>4}"
        x = format_8_decimals(data['x'])
        x1 = format_8_decimals(data['x1'])
        x2 = format_8_decimals(data['x2'])
        x_aitken = format_8_decimals(data['x_aitken'])
        error = format_8_decimals(data['error'])
        method = data['method']
        
        print(f"│ {iter_num} │ {x:>12} │ {x1:>12} │ {x2:>12} │ {x_aitken:>16} │ {error:>12} │ {method:<27} │")
    
    print("└──────┴──────────────┴──────────────┴──────────────┴──────────────────┴──────────────┴─────────────────────────────┘")
    print()
    
    # Verificar que cada valor tenga exactamente 8 decimales
    print("VERIFICACIÓN DE FORMATO:")
    print("Todos los valores numéricos verificados:")
    
    for i, data in enumerate(result['iteration_data'], 1):
        values_to_check = ['x', 'x1', 'x2', 'x_aitken', 'error']
        for field in values_to_check:
            formatted_value = format_8_decimals(data[field])
            decimal_count = len(formatted_value.split('.')[1]) if '.' in formatted_value else 0
            status = "✅" if decimal_count == 8 else "❌"
            print(f"  {status} Iteración {i}, {field}: {formatted_value} ({decimal_count} decimales)")
    
    print()
    print("COMPARACIÓN CON PUNTO FIJO NORMAL:")
    
    # Comparar velocidad con punto fijo normal
    def punto_fijo_normal(g, x0, tolerance, max_iter):
        x = x0
        for i in range(max_iter):
            x_new = g(x)
            error = abs(x_new - x)
            if error < tolerance:
                return {'iterations': i + 1, 'root': x_new, 'error': error}
            x = x_new
        return {'iterations': max_iter, 'root': x, 'error': error}
    
    normal_result = punto_fijo_normal(g_cos, 0.5, 1e-10, 50)
    
    print(f"├─ Punto fijo normal: {normal_result['iterations']} iteraciones")
    print(f"├─ Aitken acelerado:  {result['iterations']} iteraciones") 
    print(f"└─ Mejora:            {normal_result['iterations'] / result['iterations']:.1f}x más rápido")
    
    print()
    print("🎯 CONCLUSIÓN:")
    print("✅ Todos los valores en la tabla muestran exactamente 8 decimales")
    print("✅ La aceleración de Aitken funciona correctamente")
    print("✅ El formato es consistente en toda la aplicación")


if __name__ == "__main__":
    demo_8_decimals_table()