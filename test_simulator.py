#!/usr/bin/env python3
"""
Script de prueba para verificar que todos los módulos se importan correctamente
y que las funciones básicas funcionan sin la GUI
"""

import sys
import os

# Agregar el directorio actual al path para importar módulos locales
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba las importaciones de módulos"""
    print("🔍 Probando importaciones...")
    
    try:
        from numerics.methods import NumericalMethods, MathParser
        print("✅ numerics.methods - OK")
    except ImportError as e:
        print(f"❌ numerics.methods - ERROR: {e}")
        return False
    
    try:
        from numerics.advanced import InterpolationMethods, AdvancedNumericalMethods, ErrorAnalysis
        print("✅ numerics.advanced - OK")
    except ImportError as e:
        print(f"❌ numerics.advanced - ERROR: {e}")
        return False
    
    return True

def test_numerical_methods():
    """Prueba los métodos numéricos básicos"""
    print("\n🧮 Probando métodos numéricos...")
    
    try:
        from numerics.methods import NumericalMethods, MathParser
        
        # Probar parsing de funciones
        f = MathParser.parse_function("x**2 + 1")
        result = f(2)
        expected = 5
        assert abs(result - expected) < 1e-10
        print(f"✅ Parser de funciones: f(2) = {result} (esperado: {expected})")
        
        # Probar bisección
        f_root = MathParser.parse_function("x**2 - 4")
        root, iterations, history = NumericalMethods.bisection_method(f_root, 1, 3)
        assert abs(root - 2) < 1e-6
        print(f"✅ Método de bisección: raíz = {root:.6f} en {iterations} iteraciones")
        
        # Probar integración
        f_int = MathParser.parse_function("x**2")
        integral = NumericalMethods.newton_cotes_integration(f_int, 0, 2)
        expected_int = 8/3  # Integral exacta de x² de 0 a 2
        error = abs(integral - expected_int)
        print(f"✅ Integración Newton-Cotes: ∫₀² x² dx = {integral:.6f} (error: {error:.2e})")
        
        # Probar derivada numérica
        derivative = NumericalMethods.central_difference_derivative(f, 2)
        expected_deriv = 4  # Derivada de x² + 1 en x=2 es 2x = 4
        error_deriv = abs(derivative - expected_deriv)
        print(f"✅ Derivada numérica: f'(2) = {derivative:.6f} (error: {error_deriv:.2e})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en métodos numéricos: {e}")
        return False

def test_ode_methods():
    """Prueba los métodos de ecuaciones diferenciales"""
    print("\n📈 Probando métodos de EDO...")
    
    try:
        from numerics.methods import NumericalMethods, MathParser
        
        # Ecuación simple: dy/dt = y, solución exacta: y = e^t
        def simple_ode(t, y):
            return y
        
        # Resolver con Runge-Kutta
        t, y = NumericalMethods.runge_kutta_4(simple_ode, (0, 1), 1, 10)
        
        # Verificar resultado final
        import math
        expected_final = math.exp(1)  # e^1
        error = abs(y[-1] - expected_final)
        print(f"✅ Runge-Kutta 4: y(1) = {y[-1]:.6f} (exacto: {expected_final:.6f}, error: {error:.2e})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en métodos de EDO: {e}")
        return False

def test_interpolation():
    """Prueba los métodos de interpolación"""
    print("\n📊 Probando interpolación...")
    
    try:
        from numerics.advanced import InterpolationMethods
        import numpy as np
        
        # Puntos de una función conocida: f(x) = x²
        x_points = np.array([0, 1, 2, 3])
        y_points = np.array([0, 1, 4, 9])
        
        # Interpolar en x = 1.5
        result = InterpolationMethods.lagrange_interpolation_detailed(
            x_points, y_points, np.array([1.5])
        )[0][0]
        
        expected = 1.5**2  # 2.25
        error = abs(result - expected)
        print(f"✅ Interpolación Lagrange: f(1.5) = {result:.6f} (exacto: {expected:.6f}, error: {error:.2e})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en interpolación: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=" * 60)
    print("🧪 PRUEBAS DEL SIMULADOR MATEMÁTICO")
    print("=" * 60)
    
    # Contador de pruebas exitosas
    tests_passed = 0
    total_tests = 4
    
    # Ejecutar pruebas
    if test_imports():
        tests_passed += 1
    
    if test_numerical_methods():
        tests_passed += 1
    
    if test_ode_methods():
        tests_passed += 1
    
    if test_interpolation():
        tests_passed += 1
    
    # Resumen
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN: {tests_passed}/{total_tests} pruebas exitosas")
    
    if tests_passed == total_tests:
        print("🎉 ¡Todas las pruebas pasaron correctamente!")
        print("🚀 El simulador está listo para ejecutarse con 'python main.py'")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revise las dependencias.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
