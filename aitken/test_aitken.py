"""
Pruebas para verificar que la aplicación de Aitken funciona correctamente
mostrando 8 decimales en todos los resultados.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aitken_app import AitkenAcceleration, format_8_decimals
import math


def test_format_8_decimals():
    """Probar que la función de formateo funciona correctamente."""
    print("="*60)
    print("TEST: Formato de 8 decimales")
    print("="*60)
    
    test_values = [
        3.14159265359,
        0.739085133215,
        1.618033988749,
        0.00012345,
        1234567.89,
        0.0,
        -2.718281828
    ]
    
    for value in test_values:
        formatted = format_8_decimals(value)
        print(f"Original: {value:15.12f} → Formateado: {formatted}")
        
        # Verificar que tiene exactamente 8 decimales
        if '.' in formatted:
            decimals = len(formatted.split('.')[1])
            assert decimals == 8, f"Error: {formatted} no tiene 8 decimales"
    
    print("✅ Formato de 8 decimales funciona correctamente")


def test_aitken_cos_function():
    """Probar Aitken con función cos(x)."""
    print("\n" + "="*60)
    print("TEST: Aitken con cos(x)")
    print("="*60)
    
    def g_cos(x):
        return math.cos(x)
    
    aitken = AitkenAcceleration(tolerance=1e-8, max_iterations=10)
    result = aitken.accelerate(g_cos, 0.5)
    
    print(f"Función: g(x) = cos(x)")
    print(f"Valor inicial: x₀ = 0.5")
    print(f"Resultado: {format_8_decimals(result['root'])}")
    print(f"Error final: {format_8_decimals(result['error'])}")
    print(f"Iteraciones: {result['iterations']}")
    print(f"Convergió: {'SÍ' if result['converged'] else 'NO'}")
    
    print(f"\nTabla de iteraciones:")
    print(f"{'Iter':<4} {'x':<12} {'x₁':<12} {'x₂':<12} {'x_aitken':<14} {'Error':<12}")
    print("-" * 70)
    
    for data in result['iteration_data']:
        print(f"{data['iteration']:<4} "
              f"{format_8_decimals(data['x']):<12} "
              f"{format_8_decimals(data['x1']):<12} "
              f"{format_8_decimals(data['x2']):<12} "
              f"{format_8_decimals(data['x_aitken']):<14} "
              f"{format_8_decimals(data['error']):<12}")
    
    # Verificar resultado conocido
    expected = 0.7390851332  # Valor conocido de x = cos(x)
    actual_error = abs(result['root'] - expected)
    assert actual_error < 1e-6, f"Error: resultado {result['root']} muy lejos del esperado {expected}"
    
    print("✅ Aitken con cos(x) funciona correctamente")


def test_aitken_golden_ratio():
    """Probar Aitken con sqrt(x+1) para la proporción áurea."""
    print("\n" + "="*60)
    print("TEST: Aitken con sqrt(x+1) - Proporción áurea")
    print("="*60)
    
    def g_golden(x):
        return math.sqrt(x + 1)
    
    aitken = AitkenAcceleration(tolerance=1e-10, max_iterations=8)
    result = aitken.accelerate(g_golden, 1.0)
    
    print(f"Función: g(x) = √(x + 1)")
    print(f"Valor inicial: x₀ = 1.0")
    print(f"Resultado: {format_8_decimals(result['root'])}")
    print(f"Error final: {format_8_decimals(result['error'])}")
    print(f"Iteraciones: {result['iterations']}")
    print(f"Convergió: {'SÍ' if result['converged'] else 'NO'}")
    
    # Verificar contra la proporción áurea conocida
    golden_ratio = (1 + math.sqrt(5)) / 2  # φ = 1.618033988749...
    actual_error = abs(result['root'] - golden_ratio)
    print(f"Proporción áurea teórica: {format_8_decimals(golden_ratio)}")
    print(f"Error vs valor teórico: {format_8_decimals(actual_error)}")
    
    assert actual_error < 1e-8, f"Error: resultado muy lejos de la proporción áurea"
    
    print("✅ Aitken con proporción áurea funciona correctamente")


def test_aitken_sqrt2():
    """Probar Aitken para encontrar √2."""
    print("\n" + "="*60)
    print("TEST: Aitken para √2")
    print("="*60)
    
    def g_sqrt2(x):
        return (x + 2/x) / 2
    
    aitken = AitkenAcceleration(tolerance=1e-8, max_iterations=6)
    result = aitken.accelerate(g_sqrt2, 1.5)
    
    print(f"Función: g(x) = (x + 2/x) / 2")
    print(f"Valor inicial: x₀ = 1.5")
    print(f"Resultado: {format_8_decimals(result['root'])}")
    print(f"Error final: {format_8_decimals(result['error'])}")
    print(f"Iteraciones: {result['iterations']}")
    print(f"Convergió: {'SÍ' if result['converged'] else 'NO'}")
    
    # Verificar contra √2 conocido
    sqrt2 = math.sqrt(2)
    actual_error = abs(result['root'] - sqrt2)
    print(f"√2 teórico: {format_8_decimals(sqrt2)}")
    print(f"Error vs valor teórico: {format_8_decimals(actual_error)}")
    
    assert actual_error < 1e-6, f"Error: resultado muy lejos de √2"
    
    print("✅ Aitken para √2 funciona correctamente")


def test_edge_cases():
    """Probar casos extremos."""
    print("\n" + "="*60)
    print("TEST: Casos extremos")
    print("="*60)
    
    # Caso 1: Función que puede dar denominador pequeño
    def g_linear(x):
        return x  # g(x) = x, punto fijo en cualquier valor
    
    aitken = AitkenAcceleration(tolerance=1e-8, max_iterations=3)
    result = aitken.accelerate(g_linear, 1.0)
    
    print("Caso 1: Función lineal g(x) = x")
    print(f"Resultado: {format_8_decimals(result['root'])}")
    print(f"Método usado en iter 1: {result['iteration_data'][0]['method']}")
    
    # Verificar que maneja denominadores pequeños
    assert "denominador pequeño" in result['iteration_data'][0]['method'].lower() or result['converged']
    
    print("✅ Manejo de casos extremos funciona correctamente")


def run_all_tests():
    """Ejecutar todas las pruebas."""
    print("🧪 INICIANDO PRUEBAS DE LA APLICACIÓN AITKEN")
    print("=" * 70)
    
    try:
        test_format_8_decimals()
        test_aitken_cos_function()
        test_aitken_golden_ratio()
        test_aitken_sqrt2()
        test_edge_cases()
        
        print("\n" + "="*70)
        print("🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("✅ La aplicación de Aitken está funcionando correctamente")
        print("✅ Todos los valores se muestran con 8 decimales")
        print("✅ Los cálculos matemáticos son precisos")
        print("✅ Se manejan correctamente los casos extremos")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN LAS PRUEBAS: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit_code = 0 if success else 1
    exit(exit_code)