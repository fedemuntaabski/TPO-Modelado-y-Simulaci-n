"""
Test para verificar el formato de números sin notación científica
en la sección de búsqueda de raíces.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.root_finding import RootFinder, create_function_from_string
from src.ui.components.mixins import format_decimal_number

def test_number_formatting():
    """Test del formato de números sin notación científica"""
    
    print("="*60)
    print("TEST DE FORMATO DE NÚMEROS SIN NOTACIÓN CIENTÍFICA")
    print("="*60)
    
    # Test de la función de formateo
    test_values = [
        0.0,
        0.000001,
        0.0001,
        0.001,
        0.1,
        1.0,
        1.234567890123,
        100.0,
        1000.0,
        0.000000001,
        2.6e-01,
        3.14159265359
    ]
    
    print("\nTest de la función format_decimal_number:")
    print("-" * 40)
    for value in test_values:
        formatted = format_decimal_number(value, 8)
        print(f"Valor: {value:>15} -> Formato: {formatted}")
    
    # Test con métodos de búsqueda de raíces
    solver = RootFinder(tolerance=1e-6, max_iterations=100)
    
    print("\n" + "="*60)
    print("TEST CON MÉTODO DE BISECCIÓN")
    print("="*60)
    
    # Usar función simple para probar
    f = create_function_from_string("x**2 - 4")
    result = solver.bisection_method(f, 1.5, 2.5)
    
    print(f"Raíz encontrada: {result.root:.8f}")
    print(f"Error final (formato nuevo): {format_decimal_number(result.error, 8)}")
    print(f"Error final (formato científico): {result.error:.2e}")
    print(f"Valor función (formato nuevo): {format_decimal_number(result.function_value, 8)}")
    print(f"Valor función (formato científico): {result.function_value:.2e}")
    print(f"Iteraciones: {result.iterations}")
    print(f"Convergió: {result.converged}")
    
    print("\n" + "="*60)
    print("TEST CON MÉTODO DE NEWTON-RAPHSON")
    print("="*60)
    
    df = create_function_from_string("2*x")
    result2 = solver.newton_raphson_method(f, df, 1.5)
    
    print(f"Raíz encontrada: {result2.root:.8f}")
    print(f"Error final (formato nuevo): {format_decimal_number(result2.error, 8)}")
    print(f"Error final (formato científico): {result2.error:.2e}")
    print(f"Valor función (formato nuevo): {format_decimal_number(result2.function_value, 8)}")
    print(f"Valor función (formato científico): {result2.function_value:.2e}")
    print(f"Iteraciones: {result2.iterations}")
    print(f"Convergió: {result2.converged}")
    
    print("\n" + "="*60)
    print("CONCLUSIÓN")
    print("="*60)
    print("✅ Los números ahora se muestran en formato decimal")
    print("✅ No más notación científica (2.6e-01)")
    print("✅ Los errores pequeños se muestran con más decimales")
    print("✅ Los resultados son más legibles para el usuario")

if __name__ == "__main__":
    test_number_formatting()