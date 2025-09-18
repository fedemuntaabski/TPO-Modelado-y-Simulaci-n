"""
Test específico para la función x³ - x - 1 = 0 con punto fijo
Este test verifica las diferentes conversiones a punto fijo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.root_finding import RootFinder, create_function_from_string
import math

def test_cubic_fixed_point():
    """Test específico para x³ - x - 1 = 0"""
    
    solver = RootFinder(tolerance=1e-6, max_iterations=1000)
    
    print("="*70)
    print("TEST ESPECÍFICO: x³ - x - 1 = 0")
    print("="*70)
    
    # Función original
    f = create_function_from_string("x**3 - x - 1")
    
    print("Función: f(x) = x³ - x - 1")
    print("Raíz exacta esperada: 1.324717957244746")
    print("Punto inicial: x₀ = 1")
    
    # Test 1: Conversión incorrecta que mencionas
    print("\n" + "-"*50)
    print("TEST 1: g(x) = 1/(3*(sqrt(x+1))²) = 1/(3(x+1))")
    print("-"*50)
    
    def g_incorrect(x):
        return 1 / (3 * (x + 1))
    
    result1 = solver.fixed_point_method(g_incorrect, 1.0)
    print(f"Resultado: x = {result1.root:.8f}")
    print(f"Iteraciones: {result1.iterations}")
    print(f"Convergió: {result1.converged}")
    print(f"Verificación f(x): {f(result1.root):.6f}")
    print("❌ INCORRECTO - No es la raíz de x³ - x - 1 = 0")
    
    # Test 2: Conversión correcta
    print("\n" + "-"*50)
    print("TEST 2: g(x) = (x + 1)^(1/3)")
    print("-"*50)
    
    def g_correct(x):
        return (x + 1)**(1/3)
    
    result2 = solver.fixed_point_method(g_correct, 1.0)
    print(f"Resultado: x = {result2.root:.8f}")
    print(f"Iteraciones: {result2.iterations}")
    print(f"Convergió: {result2.converged}")
    print(f"Verificación f(x): {f(result2.root):.6f}")
    print("✅ CORRECTO - Raíz válida de x³ - x - 1 = 0")
    
    # Test 3: Con Newton-Raphson para comparar
    print("\n" + "-"*50)
    print("TEST 3: Newton-Raphson (para comparación)")
    print("-"*50)
    
    df = create_function_from_string("3*x**2 - 1")
    result3 = solver.newton_raphson_method(f, df, 1.0)
    print(f"Resultado: x = {result3.root:.8f}")
    print(f"Iteraciones: {result3.iterations}")
    print(f"Convergió: {result3.converged}")
    print(f"Verificación f(x): {f(result3.root):.6f}")
    
    # Test 4: Probar en el programa con string
    print("\n" + "-"*50)
    print("TEST 4: Función desde string (como en interfaz)")
    print("-"*50)
    
    try:
        # Función incorrecta como string
        g_str_incorrect = create_function_from_string("1/(3*(x + 1))")
        result4 = solver.fixed_point_method(g_str_incorrect, 1.0)
        print(f"g(x) = '1/(3*(x + 1))'")
        print(f"Resultado: x = {result4.root:.8f}")
        print(f"Iteraciones: {result4.iterations}")
        print(f"Verificación f(x): {f(result4.root):.6f}")
        print("❌ INCORRECTO")
        
        # Función correcta como string  
        g_str_correct = create_function_from_string("(x + 1)**(1/3)")
        result5 = solver.fixed_point_method(g_str_correct, 1.0)
        print(f"\ng(x) = '(x + 1)**(1/3)'")
        print(f"Resultado: x = {result5.root:.8f}")
        print(f"Iteraciones: {result5.iterations}")
        print(f"Verificación f(x): {f(result5.root):.6f}")
        print("✅ CORRECTO")
        
    except Exception as e:
        print(f"Error con funciones string: {e}")
    
    # Análisis matemático
    print("\n" + "="*70)
    print("ANÁLISIS MATEMÁTICO")
    print("="*70)
    print("Para convertir f(x) = x³ - x - 1 = 0 a punto fijo:")
    print("1. x³ - x - 1 = 0")
    print("2. x³ = x + 1")
    print("3. x = (x + 1)^(1/3)  ← CORRECTO")
    print("")
    print("La función g(x) = 1/(3(x+1)) NO viene de esta ecuación.")
    print("Esa conversión daría la raíz de una ecuación diferente.")
    print("")
    print("CONCLUSIÓN:")
    print("- Use g(x) = (x + 1)^(1/3) para obtener x ≈ 1.324717")
    print("- La función g(x) = 1/(3(x+1)) es matemáticamente incorrecta")

if __name__ == "__main__":
    test_cubic_fixed_point()