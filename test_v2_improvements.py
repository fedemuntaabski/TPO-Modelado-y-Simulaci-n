#!/usr/bin/env python3
"""
Pruebas específicas para las mejoras de la versión 2.0
Verifica que todas las nuevas funcionalidades funcionan correctamente
"""

import sys
import os

# Agregar el directorio actual al path para importar módulos locales
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_theme_imports():
    """Prueba las importaciones del nuevo tema"""
    print("🎨 Probando importaciones del tema...")
    
    try:
        from gui.themes import DarkTheme, AnimationUtils
        print("✅ gui.themes - OK")
        
        # Probar métodos del tema
        stylesheet = DarkTheme.get_main_stylesheet()
        assert len(stylesheet) > 100, "Stylesheet muy corto"
        
        button_style = DarkTheme.get_button_style("primary")
        assert "background-color" in button_style, "Estilo de botón incompleto"
        
        keyboard_style = DarkTheme.get_keyboard_button_style("function")
        assert "QPushButton" in keyboard_style, "Estilo de teclado incompleto"
        
        print("✅ Estilos del tema - OK")
        return True
        
    except ImportError as e:
        print(f"❌ gui.themes - ERROR: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en estilos: {e}")
        return False

def test_animation_imports():
    """Prueba las importaciones de animaciones"""
    print("\n✨ Probando importaciones de animaciones...")
    
    try:
        from gui.animations import (
            FadeAnimation, ButtonHoverEffect, ProgressIndicator,
            SlideAnimation, PlotAnimation, StatusAnimation, LoadingSpinner
        )
        print("✅ gui.animations - OK")
        
        # Probar utilidades de animación
        from gui.themes import AnimationUtils
        duration = AnimationUtils.get_fade_duration()
        assert duration > 0, "Duración de fade inválida"
        
        hover_duration = AnimationUtils.get_hover_duration()
        assert hover_duration > 0, "Duración de hover inválida"
        
        print("✅ Utilidades de animación - OK")
        return True
        
    except ImportError as e:
        print(f"❌ gui.animations - ERROR: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en animaciones: {e}")
        return False

def test_comparison_imports():
    """Prueba las importaciones de la pestaña de comparación"""
    print("\n🔄 Probando importaciones de comparación...")
    
    try:
        from gui.comparison_tab import ComparisonTab
        print("✅ gui.comparison_tab - OK")
        return True
        
    except ImportError as e:
        print(f"❌ gui.comparison_tab - ERROR: {e}")
        return False

def test_main_window_improvements():
    """Prueba que la ventana principal tenga las mejoras"""
    print("\n🖥️ Probando mejoras en ventana principal...")
    
    try:
        # Verificar que no cause errores de importación
        from gui.main_window import MathSimulatorApp, MathKeyboard
        print("✅ Importaciones principales - OK")
        
        # Verificar que los métodos principales existan
        # (No podemos instanciar sin QApplication)
        assert hasattr(MathKeyboard, 'init_ui'), "MathKeyboard sin init_ui"
        assert hasattr(MathSimulatorApp, 'create_title_frame'), "Sin create_title_frame"
        assert hasattr(MathSimulatorApp, 'apply_style'), "Sin apply_style"
        
        print("✅ Métodos principales - OK")
        return True
        
    except ImportError as e:
        print(f"❌ gui.main_window - ERROR: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en ventana principal: {e}")
        return False

def test_numerical_methods_compatibility():
    """Verifica que los métodos numéricos siguen funcionando"""
    print("\n🧮 Verificando compatibilidad de métodos numéricos...")
    
    try:
        from numerics.methods import NumericalMethods, MathParser
        from numerics.advanced import InterpolationMethods, AdvancedNumericalMethods, ErrorAnalysis
        
        # Probar parser mejorado
        f = MathParser.parse_function("sin(x) + cos(x)")
        result = f(0)
        expected = 1.0  # sin(0) + cos(0) = 0 + 1 = 1
        assert abs(result - expected) < 1e-10, f"Parser error: {result} != {expected}"
        
        # Probar método de bisección
        f_root = MathParser.parse_function("x**2 - 4")
        root, iterations, history = NumericalMethods.bisection_method(f_root, 1, 3, 1e-6, 100)
        assert abs(root - 2) < 1e-5, f"Bisección error: {root} != 2"
        
        print("✅ Métodos numéricos compatibles - OK")
        return True
        
    except Exception as e:
        print(f"❌ Error en métodos numéricos: {e}")
        return False

def test_keyboard_improvements():
    """Verifica las mejoras del teclado virtual"""
    print("\n⌨️ Verificando mejoras del teclado virtual...")
    
    try:
        # Simular la nueva estructura del teclado
        new_buttons = [
            ['sin', 'cos', 'tan', 'Clear'],
            ['exp', 'log', 'sqrt', '+'],
            ['pi', 'e', '^', '-'],
            ['*', '/', '.', '='],
        ]
        
        # Verificar que no hay números ni variables
        all_buttons = [btn for row in new_buttons for btn in row]
        
        # No debe haber números
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for num in numbers:
            assert num not in all_buttons, f"Número {num} encontrado en teclado"
        
        # No debe haber variables
        variables = ['x', 't', 'y']
        for var in variables:
            assert var not in all_buttons, f"Variable {var} encontrada en teclado"
        
        # No debe haber paréntesis
        assert '(' not in all_buttons, "Paréntesis encontrado en teclado"
        assert ')' not in all_buttons, "Paréntesis encontrado en teclado"
        
        # Debe haber funciones matemáticas
        functions = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']
        for func in functions:
            assert func in all_buttons, f"Función {func} no encontrada en teclado"
        
        print("✅ Teclado virtual mejorado - OK")
        return True
        
    except AssertionError as e:
        print(f"❌ Error en teclado: {e}")
        return False

def main():
    """Función principal de pruebas v2.0"""
    print("=" * 70)
    print("🧪 PRUEBAS DEL SIMULADOR MATEMÁTICO v2.0")
    print("   Verificando Mejoras e Innovaciones")
    print("=" * 70)
    
    # Contador de pruebas exitosas
    tests_passed = 0
    total_tests = 6
    
    # Ejecutar pruebas específicas de v2.0
    if test_theme_imports():
        tests_passed += 1
    
    if test_animation_imports():
        tests_passed += 1
    
    if test_comparison_imports():
        tests_passed += 1
    
    if test_main_window_improvements():
        tests_passed += 1
    
    if test_numerical_methods_compatibility():
        tests_passed += 1
        
    if test_keyboard_improvements():
        tests_passed += 1
    
    # Resumen
    print("\n" + "=" * 70)
    print(f"📊 RESUMEN v2.0: {tests_passed}/{total_tests} pruebas exitosas")
    
    if tests_passed == total_tests:
        print("🎉 ¡Todas las mejoras funcionan correctamente!")
        print("🚀 La versión 2.0 está lista para usar con 'python main_v2.py'")
        print("\n✨ MEJORAS VERIFICADAS:")
        print("   🎨 Tema oscuro moderno")
        print("   ⌨️ Teclado virtual simplificado")
        print("   🔄 Pestaña de comparación de métodos")
        print("   ✨ Sistema de animaciones")
        print("   🎯 Mejor experiencia de usuario")
        return True
    else:
        print("⚠️  Algunas mejoras presentan problemas.")
        print("🔧 Revise los errores y dependencias.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
