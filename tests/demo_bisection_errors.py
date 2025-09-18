"""
Demostración práctica: ERROR vs ERROR ABSOLUTO en Bisección
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.root_finding import RootFinder, create_function_from_string

def demo_errors():
    print("="*80)
    print("DEMOSTRACION: ERROR vs ERROR ABSOLUTO EN BISECCION")
    print("="*80)
    
    # Función ejemplo: x³ - x - 1 = 0
    f = create_function_from_string("x**3 - x - 1")
    solver = RootFinder(tolerance=1e-4, max_iterations=20)
    
    print("Funcion: f(x) = x^3 - x - 1")
    print("Raiz aproximada: x aprox 1.3247179572")
    print("Intervalo inicial: [1, 2]")
    print("Tolerancia: 1e-4 = 0.0001")
    
    result = solver.bisection_method(f, 1.0, 2.0)
    
    print(f"\nRESULTADO FINAL:")
    print(f"Raiz encontrada: {result.root:.8f}")
    print(f"Error final: {result.error:.8f}")
    print(f"Iteraciones: {result.iterations}")
    
    print(f"\n{'Iter':<4} {'a':<10} {'b':<10} {'c':<12} {'f(c)':<12} {'Error Int':<12} {'Error Real':<12}")
    print("-" * 85)
    
    raiz_exacta = 1.3247179572447  # Valor conocido
    
    for data in result.iteration_data:
        iter_num = data['iteration']
        a = data['a']
        b = data['b']
        c = data['c']
        fc = data['f_c']
        error_intervalo = data['error']
        error_real = abs(c - raiz_exacta)
        
        print(f"{iter_num:<4} {a:<10.6f} {b:<10.6f} {c:<12.6f} {fc:<12.6f} {error_intervalo:<12.6f} {error_real:<12.6f}")
    
    print(f"\n" + "="*80)
    print("ANALISIS DETALLADO")
    print("="*80)
    
    print(f"\nDEFINICIONES:")
    print(f"   Error de Intervalo = (b-a)/2 = {result.error:.8f}")
    print(f"   Error Real = |c - raiz_verdadera| = {abs(result.root - raiz_exacta):.8f}")
    print(f"   Valor funcion = |f(c)| = {abs(result.function_value):.8f}")
    
    print(f"\nCRITERIOS DE PARADA (el programa para cuando SE CUMPLE CUALQUIERA):")
    print(f"   1. |f(c)| < tolerancia")
    print(f"   2. Error de Intervalo < tolerancia  <- PRINCIPAL EN BISECCION")
    
    print(f"\nVERIFICACION:")
    error_ok = result.error < 1e-4
    func_ok = abs(result.function_value) < 1e-4
    print(f"   Error de Intervalo ({result.error:.8f}) {'<' if error_ok else '>='} tolerancia (0.0001): {error_ok}")
    print(f"   |f(c)| ({abs(result.function_value):.8f}) {'<' if func_ok else '>='} tolerancia (0.0001): {func_ok}")
    
    if error_ok and func_ok:
        criterio = "Ambos criterios"
    elif error_ok:
        criterio = "Error de Intervalo"
    else:
        criterio = "|f(c)| pequeno"
    print(f"   Paro por: {criterio}")
    
    print(f"\nGARANTIA MATEMATICA:")
    print(f"   La raiz real esta en [{result.root - result.error:.6f}, {result.root + result.error:.6f}]")
    cumple_garantia = abs(result.root - raiz_exacta) <= result.error
    print(f"   Error real <= Error de intervalo: {cumple_garantia}")
    print(f"   ({abs(result.root - raiz_exacta):.8f} <= {result.error:.8f})")
    
    print(f"\nCONCLUSIONES:")
    print(f"   1. El ERROR DE INTERVALO es lo que usa el programa para decidir cuando parar")
    print(f"   2. Es una COTA SUPERIOR garantizada del error real")
    print(f"   3. El error absoluto seria |c_n - c_(n-1)| entre iteraciones")
    print(f"   4. En biseccion, el criterio del intervalo es MAS CONFIABLE")

if __name__ == "__main__":
    demo_errors()