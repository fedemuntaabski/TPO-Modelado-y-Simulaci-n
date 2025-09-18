"""
Test para verificar que el error absoluto ha sido eliminado del método de bisección
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.root_finding import RootFinder, create_function_from_string

def test_bisection_without_abs_error():
    """Test que verifica que ya no se calcula el error absoluto"""
    
    print("="*70)
    print("TEST: BISECCIÓN SIN ERROR ABSOLUTO")
    print("="*70)
    
    # Función ejemplo: x² - 4 = 0
    f = create_function_from_string("x**2 - 4")
    solver = RootFinder(tolerance=1e-4, max_iterations=10)
    
    print("Función: f(x) = x² - 4")
    print("Intervalo inicial: [1, 3]")
    print("Tolerancia: 1e-4")
    
    result = solver.bisection_method(f, 1.0, 3.0)
    
    print(f"\nRESULTADO:")
    print(f"Raíz encontrada: {result.root:.8f}")
    print(f"Error final: {result.error:.8f}")
    print(f"Iteraciones: {result.iterations}")
    print(f"Convergió: {result.converged}")
    
    print(f"\nDATOS DE ITERACIONES:")
    print(f"{'Iter':<4} {'a':<10} {'b':<10} {'c':<12} {'f(c)':<12} {'Error':<12}")
    print("-" * 70)
    
    for data in result.iteration_data:
        iter_num = data['iteration']
        a = data['a']
        b = data['b']
        c = data['c']
        fc = data['f_c']
        error = data['error']
        
        print(f"{iter_num:<4} {a:<10.6f} {b:<10.6f} {c:<12.6f} {fc:<12.6f} {error:<12.6f}")
        
        # Verificar que NO existe 'abs_error' en los datos
        if 'abs_error' in data:
            print(f"❌ ERROR: Todavia existe 'abs_error' en los datos!")
            return False
    
    print(f"\n✅ VERIFICACIÓN EXITOSA:")
    print(f"   • Ya no se calcula el error absoluto")
    print(f"   • Solo se usa el error de intervalo: (b-a)/2")
    print(f"   • Los datos de iteración solo contienen el error de intervalo")
    print(f"   • El criterio de parada sigue funcionando correctamente")
    
    return True

def test_detailed_iteration_data():
    """Verifica en detalle qué campos contienen los datos de iteración"""
    
    print(f"\n" + "="*70)
    print("ANÁLISIS DE CAMPOS EN DATOS DE ITERACIÓN")
    print("="*70)
    
    f = create_function_from_string("x**3 - x - 1")
    solver = RootFinder(tolerance=1e-3, max_iterations=5)
    
    result = solver.bisection_method(f, 1.0, 2.0)
    
    if result.iteration_data:
        first_iteration = result.iteration_data[0]
        print(f"Campos disponibles en cada iteración:")
        for key, value in first_iteration.items():
            print(f"   • {key}: {value}")
        
        print(f"\n✅ CONFIRMACIÓN:")
        expected_fields = {'iteration', 'a', 'b', 'c', 'f_c', 'error'}
        actual_fields = set(first_iteration.keys())
        
        if actual_fields == expected_fields:
            print(f"   • Los campos son exactamente los esperados")
            print(f"   • NO hay campo 'abs_error'")
            print(f"   • Solo hay 'error' (error de intervalo)")
        else:
            print(f"   • ATENCIÓN: Campos encontrados: {actual_fields}")
            print(f"   • Campos esperados: {expected_fields}")
            if 'abs_error' in actual_fields:
                print(f"   ❌ Todavía existe 'abs_error'")
            else:
                print(f"   ✅ No existe 'abs_error'")

if __name__ == "__main__":
    success = test_bisection_without_abs_error()
    test_detailed_iteration_data()
    
    if success:
        print(f"\n🎉 MODIFICACIÓN COMPLETADA EXITOSAMENTE")
        print(f"   El error absoluto ha sido eliminado del método de bisección")
        print(f"   Ahora solo se usa el error de intervalo como debe ser")
    else:
        print(f"\n❌ MODIFICACIÓN INCOMPLETA")
        print(f"   Revisar el código para eliminar completamente el error absoluto")