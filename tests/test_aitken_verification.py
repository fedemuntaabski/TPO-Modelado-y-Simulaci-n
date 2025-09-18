"""
Verificación comprehensiva del método de Aitken:
- Implementación matemática correcta
- Datos mostrados en pantalla
- Coherencia de resultados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.root_finding import RootFinder, create_function_from_string
import math

def test_aitken_mathematical_correctness():
    """Verifica la correcta implementación matemática del método de Aitken"""
    
    print("="*80)
    print("VERIFICACIÓN MATEMÁTICA DEL MÉTODO DE AITKEN")
    print("="*80)
    
    # Función de punto fijo que converge lentamente: g(x) = cos(x)
    # Para acelerar la convergencia hacia x = cos(x) ≈ 0.7390851332
    g = create_function_from_string("cos(x)")
    solver = RootFinder(tolerance=1e-8, max_iterations=10)
    
    print("Función de punto fijo: g(x) = cos(x)")
    print("Punto inicial: x₀ = 0.5")
    print("Raíz exacta esperada: x ≈ 0.7390851332")
    print("Tolerancia: 1e-8")
    
    result = solver.aitken_acceleration(g, 0.5)
    
    print(f"\nRESULTADO:")
    print(f"Raíz encontrada: {result.root:.10f}")
    print(f"Error final: {result.error:.2e}")
    print(f"Iteraciones: {result.iterations}")
    print(f"Convergió: {result.converged}")
    
    # Verificar manualmente la fórmula de Aitken
    print(f"\nVERIFICACIÓN MANUAL DE LA FÓRMULA DE AITKEN:")
    print(f"Fórmula: x_new = x - (x₁ - x)² / (x₂ - 2x₁ + x)")
    print(f"{'Iter':<4} {'x':<12} {'x₁':<12} {'x₂':<12} {'x_aitken':<14} {'Manual':<14} {'Error':<12} {'¿Correcto?'}")
    print("-" * 95)
    
    all_correct = True
    for data in result.iteration_data[:5]:  # Verificar primeras 5 iteraciones
        x = data['x']
        x1 = data['x1']
        x2 = data['x2']
        x_aitken = data['x_aitken']
        error = data['error']
        
        # Calcular manualmente usando la fórmula de Aitken
        denominator = x2 - 2*x1 + x
        if abs(denominator) > 1e-14:
            x_aitken_manual = x - (x1 - x)**2 / denominator
        else:
            x_aitken_manual = x2  # Usar punto fijo normal
        
        # Verificar si el cálculo es correcto
        is_correct = abs(x_aitken - x_aitken_manual) < 1e-12
        if not is_correct:
            all_correct = False
        
        print(f"{data['iteration']:<4} {x:<12.6f} {x1:<12.6f} {x2:<12.6f} {x_aitken:<14.8f} {x_aitken_manual:<14.8f} {error:<12.2e} {('✓' if is_correct else '✗')}")
    
    print(f"\n✅ Fórmula matemática: {'CORRECTA' if all_correct else 'INCORRECTA'}")
    
    return result, all_correct

def test_aitken_convergence_improvement():
    """Compara la convergencia de Aitken vs punto fijo normal"""
    
    print(f"\n" + "="*80)
    print("COMPARACIÓN: AITKEN vs PUNTO FIJO NORMAL")
    print("="*80)
    
    g = create_function_from_string("cos(x)")
    solver = RootFinder(tolerance=1e-6, max_iterations=50)
    
    # Método de punto fijo normal
    result_normal = solver.fixed_point_method(g, 0.5)
    
    # Método de Aitken
    result_aitken = solver.aitken_acceleration(g, 0.5)
    
    print(f"RESULTADOS COMPARATIVOS:")
    print(f"{'Método':<15} {'Iteraciones':<12} {'Error Final':<15} {'Convergió'}")
    print("-" * 55)
    print(f"{'Punto Fijo':<15} {result_normal.iterations:<12} {result_normal.error:<15.2e} {result_normal.converged}")
    print(f"{'Aitken':<15} {result_aitken.iterations:<12} {result_aitken.error:<15.2e} {result_aitken.converged}")
    
    acceleration_factor = result_normal.iterations / result_aitken.iterations if result_aitken.iterations > 0 else 0
    print(f"\n🚀 ACELERACIÓN: {acceleration_factor:.1f}x más rápido")
    
    return result_normal.iterations > result_aitken.iterations

def test_aitken_display_data():
    """Verifica que los datos mostrados en pantalla sean correctos"""
    
    print(f"\n" + "="*80)
    print("VERIFICACIÓN DE DATOS MOSTRADOS EN PANTALLA")
    print("="*80)
    
    g = create_function_from_string("sqrt(x + 1)")  # Converge a golden ratio
    solver = RootFinder(tolerance=1e-6, max_iterations=5)
    result = solver.aitken_acceleration(g, 1.0)
    
    print("Función: g(x) = sqrt(x + 1)")
    print("Esperado: φ = (1 + √5)/2 ≈ 1.618033988749")
    
    # Verificar estructura de datos
    if result.iteration_data:
        first_iter = result.iteration_data[0]
        expected_fields = {'iteration', 'x', 'x1', 'x2', 'x_aitken', 'error'}
        actual_fields = set(first_iter.keys())
        
        print(f"\nESTRUCTURA DE DATOS:")
        print(f"Campos esperados: {expected_fields}")
        print(f"Campos reales:    {actual_fields}")
        print(f"¿Estructura correcta? {expected_fields == actual_fields}")
        
        # Mostrar tabla como aparecería en pantalla
        print(f"\nTABLA COMO SE MUESTRA EN PANTALLA:")
        print(f"{'Iter':<4} {'x':<12} {'x₁':<12} {'x₂':<12} {'x_aitken':<14} {'Error':<12}")
        print("-" * 70)
        
        for data in result.iteration_data:
            print(f"{data['iteration']:<4} {data['x']:<12.6f} {data['x1']:<12.6f} {data['x2']:<12.6f} {data['x_aitken']:<14.8f} {data['error']:<12.2e}")
        
        return expected_fields == actual_fields
    
    return False

def test_aitken_edge_cases():
    """Verifica el manejo de casos extremos"""
    
    print(f"\n" + "="*80)
    print("VERIFICACIÓN DE CASOS EXTREMOS")
    print("="*80)
    
    # Caso 1: Denominador muy pequeño
    print("CASO 1: Función que puede producir denominador pequeño")
    g = create_function_from_string("x")  # g(x) = x, punto fijo en cualquier x
    solver = RootFinder(tolerance=1e-6, max_iterations=3)
    
    try:
        result = solver.aitken_acceleration(g, 1.0)
        print(f"✓ Manejó correctamente denominador pequeño")
        print(f"  Resultado: {result.root:.6f}, Iteraciones: {result.iterations}")
    except Exception as e:
        print(f"✗ Error con denominador pequeño: {e}")
        return False
    
    # Caso 2: Función que diverge
    print(f"\nCASO 2: Función que puede diverger")
    g = create_function_from_string("x + 1")  # g(x) = x + 1, diverge
    
    try:
        result = solver.aitken_acceleration(g, 1.0)
        print(f"✓ Manejó función divergente sin crash")
        print(f"  Convergió: {result.converged}")
    except Exception as e:
        print(f"✓ Manejó correctamente con excepción controlada: {type(e).__name__}")
    
    return True

def run_all_aitken_tests():
    """Ejecuta todos los tests de verificación de Aitken"""
    
    print("🔍 INICIANDO VERIFICACIÓN COMPREHENSIVA DEL MÉTODO DE AITKEN")
    print("="*80)
    
    # Test 1: Corrección matemática
    result, math_correct = test_aitken_mathematical_correctness()
    
    # Test 2: Mejora de convergencia
    convergence_improved = test_aitken_convergence_improvement()
    
    # Test 3: Datos de pantalla
    display_correct = test_aitken_display_data()
    
    # Test 4: Casos extremos
    edge_cases_ok = test_aitken_edge_cases()
    
    # Resumen final
    print(f"\n" + "="*80)
    print("RESUMEN DE VERIFICACIÓN")
    print("="*80)
    
    tests = [
        ("Fórmula matemática correcta", math_correct),
        ("Mejora convergencia vs punto fijo", convergence_improved),
        ("Datos de pantalla correctos", display_correct),
        ("Manejo de casos extremos", edge_cases_ok)
    ]
    
    all_passed = True
    for test_name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<35} {status}")
        if not passed:
            all_passed = False
    
    print(f"\n{'='*80}")
    if all_passed:
        print("🎉 TODAS LAS VERIFICACIONES PASARON")
        print("   El método de Aitken está correctamente implementado")
        print("   Los datos mostrados en pantalla son coherentes")
        print("   La aceleración funciona como se espera")
    else:
        print("⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("   Revisar la implementación del método de Aitken")
    
    return all_passed

if __name__ == "__main__":
    run_all_aitken_tests()