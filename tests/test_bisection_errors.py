"""
Demostración de la diferencia entre Error y Error Absoluto en Bisección
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.root_finding import RootFinder, create_function_from_string

def demo_bisection_errors():
    """Demuestra la diferencia entre error y error absoluto"""
    
    print("="*80)
    print("DEMOSTRACIÓN: ERROR vs ERROR ABSOLUTO EN BISECCIÓN")
    print("="*80)
    
    # Función ejemplo: x² - 4 = 0 (raíz exacta en x = 2)
    f = create_function_from_string("x**2 - 4")
    solver = RootFinder(tolerance=1e-6, max_iterations=20)
    
    print("Función: f(x) = x² - 4")
    print("Raíz exacta: x = 2.0")
    print("Intervalo inicial: [1, 3]")
    print("Tolerancia: 1e-6")
    
    result = solver.bisection_method(f, 1.0, 3.0)
    
    print(f"\nRESULTADO FINAL:")
    print(f"Raíz encontrada: {result.root:.8f}")
    print(f"Error final: {result.error:.8f}")
    print(f"Iteraciones: {result.iterations}")
    print(f"Convergió: {result.converged}")
    
    print(f"\n{'Iter':<4} {'a':<10} {'b':<10} {'c (aprox)':<12} {'f(c)':<12} {'Error':<12} {'Error Real':<12} {'Criterio'}")
    print("-" * 95)
    
    for i, data in enumerate(result.iteration_data):
        iter_num = data['iteration']
        a = data['a']
        b = data['b']
        c = data['c']
        fc = data['f_c']
        error_intervalo = data['error']
        
        # Error real (distancia a la raíz verdadera x=2)
        error_real = abs(c - 2.0)
        
        # Determinar qué criterio se usa para parar
        if abs(fc) < 1e-6:
            criterio = "f(c) pequeño"
        elif error_intervalo < 1e-6:
            criterio = "intervalo pequeño"
        else:
            criterio = "continúa"
        
        print(f"{iter_num:<4} {a:<10.6f} {b:<10.6f} {c:<12.8f} {fc:<12.6f} {error_intervalo:<12.8f} {error_real:<12.8f} {criterio}")
        
        # Parar si cumple criterio (simular la lógica del algoritmo)
        if abs(fc) < 1e-6 or error_intervalo < 1e-6:
            print(f"\n✅ CONVERGENCIA en iteración {iter_num}:")
            if abs(fc) < 1e-6:
                print(f"   - |f(c)| = {abs(fc):.2e} < tolerancia")
            if error_intervalo < 1e-6:
                print(f"   - Error de intervalo = {error_intervalo:.2e} < tolerancia")
            break
    
    print(f"\n" + "="*80)
    print("ANÁLISIS DE LOS ERRORES")
    print("="*80)
    
    print(f"📊 TIPOS DE ERROR:")
    print(f"   • Error de Intervalo: (b-a)/2 = {result.error:.8f}")
    print(f"   • Error Real: |c - raíz_exacta| = {abs(result.root - 2.0):.8f}")
    print(f"   • Valor función: |f(c)| = {abs(result.function_value):.8f}")
    
    print(f"\n🎯 CRITERIOS DE PARADA:")
    print(f"   • El programa para cuando: |f(c)| < tolerancia OR (b-a)/2 < tolerancia")
    print(f"   • En este caso paró por: {'f(c) pequeño' if abs(result.function_value) < 1e-6 else 'intervalo pequeño'}")
    
    print(f"\n✅ GARANTÍAS DEL MÉTODO:")
    print(f"   • La raíz está GARANTIZADA en el intervalo final")
    print(f"   • Error de intervalo es una COTA SUPERIOR del error real")
    print(f"   • El error real ({abs(result.root - 2.0):.8f}) ≤ Error de intervalo ({result.error:.8f})")
    
    print(f"\n📈 CONVERGENCIA:")
    print(f"   • Bisección tiene convergencia lineal")
    print(f"   • El intervalo se reduce a la mitad en cada iteración")
    print(f"   • Error garantizado ≤ (intervalo_inicial) / 2^n")

if __name__ == "__main__":
    demo_bisection_errors()