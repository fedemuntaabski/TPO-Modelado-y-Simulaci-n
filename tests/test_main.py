#!/usr/bin/env python3
"""
Suite de pruebas completa para el Simulador Matemático Avanzado v3.0
Incluye tests de funcionalidad básica, mejoras v2.0 y validaciones v3.0

Autor: Equipo TPO Modelado y Simulación
Fecha: 2025
"""

import sys
import os
import pytest
import numpy as np
from typing import List, Dict, Any

# Agregar el directorio principal al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestImports:
    """Tests de importación de módulos."""
    
    def test_numerical_methods_imports(self):
        """Prueba importaciones de métodos numéricos."""
        from numerics.methods import NumericalMethods, MathParser
        from numerics.advanced import InterpolationMethods, AdvancedNumericalMethods, ErrorAnalysis
        
        assert NumericalMethods is not None
        assert MathParser is not None
        assert InterpolationMethods is not None
        assert AdvancedNumericalMethods is not None
        assert ErrorAnalysis is not None
    
    def test_gui_imports(self):
        """Prueba importaciones de componentes GUI."""
        from gui.main_window import MathSimulatorApp, MathKeyboard, PlotWidget
        from gui.themes import DarkTheme
        from gui.animations import FadeAnimation, ButtonHoverEffect
        from gui.comparison_tab import ComparisonTab
        
        assert MathSimulatorApp is not None
        assert MathKeyboard is not None
        assert PlotWidget is not None
        assert DarkTheme is not None
        assert FadeAnimation is not None
        assert ButtonHoverEffect is not None
        assert ComparisonTab is not None

class TestNumericalMethods:
    """Tests de métodos numéricos."""
    
    @pytest.fixture
    def methods(self):
        """Fixture para instancia de métodos numéricos."""
        from numerics.methods import NumericalMethods
        return NumericalMethods()
    
    def test_bisection_method(self, methods):
        """Test del método de bisección."""
        # f(x) = x^2 - 4, raíz en x = 2
        def f(x):
            return x**2 - 4
        
        root, iterations, errors = methods.bisection(f, 0, 5, tolerance=1e-6)
        
        assert abs(root - 2.0) < 1e-5, f"Raíz incorrecta: {root}"
        assert iterations > 0, "Número de iteraciones debe ser positivo"
        assert len(errors) == iterations, "Longitud de errores inconsistente"
    
    def test_newton_raphson_method(self, methods):
        """Test del método de Newton-Raphson."""
        # f(x) = x^2 - 4, f'(x) = 2x, raíz en x = 2
        def f(x):
            return x**2 - 4
        
        def df(x):
            return 2*x
        
        root, iterations, errors = methods.newton_raphson(f, df, 1.0, tolerance=1e-8)
        
        assert abs(root - 2.0) < 1e-7, f"Raíz incorrecta: {root}"
        assert iterations > 0, "Número de iteraciones debe ser positivo"
    
    def test_trapezoidal_integration(self, methods):
        """Test de integración trapezoidal."""
        # ∫x^2 dx de 0 a 2 = 8/3 ≈ 2.667
        def f(x):
            return x**2
        
        result = methods.trapezoidal_integration(f, 0, 2, 1000)
        expected = 8/3
        
        assert abs(result - expected) < 0.01, f"Integración incorrecta: {result}"
    
    def test_simpson_integration(self, methods):
        """Test de integración de Simpson."""
        # ∫x^2 dx de 0 a 2 = 8/3 ≈ 2.667
        def f(x):
            return x**2
        
        result = methods.simpson_integration(f, 0, 2, 1000)
        expected = 8/3
        
        assert abs(result - expected) < 0.001, f"Integración incorrecta: {result}"
    
    def test_euler_ode(self, methods):
        """Test del método de Euler para EDO."""
        # dy/dx = -y, y(0) = 1, solución exacta: y = e^(-x)
        def f(x, y):
            return -y
        
        x_vals, y_vals = methods.euler_ode(f, 0, 1, 1, 100)
        
        # Verificar que tenemos los valores correctos
        assert len(x_vals) == len(y_vals), "Longitudes de arrays inconsistentes"
        assert len(x_vals) == 101, "Número de puntos incorrecto"
        
        # Verificar aproximadamente la solución en x=1
        final_y = y_vals[-1]
        expected = np.exp(-1)  # e^(-1) ≈ 0.368
        
        assert abs(final_y - expected) < 0.1, f"Solución EDO incorrecta: {final_y}"

class TestAdvancedMethods:
    """Tests de métodos numéricos avanzados."""
    
    @pytest.fixture
    def advanced_methods(self):
        """Fixture para métodos avanzados."""
        from numerics.advanced import AdvancedNumericalMethods
        return AdvancedNumericalMethods()
    
    def test_lagrange_interpolation(self, advanced_methods):
        """Test de interpolación de Lagrange."""
        x_points = [0, 1, 2]
        y_points = [1, 4, 9]  # y = x^2 + 1
        
        # Interpolar en x = 1.5
        result = advanced_methods.lagrange_interpolation(x_points, y_points, 1.5)
        expected = 1.5**2 + 1  # 3.25
        
        assert abs(result - expected) < 0.1, f"Interpolación incorrecta: {result}"
    
    def test_gaussian_elimination(self, advanced_methods):
        """Test de eliminación gaussiana."""
        # Sistema: 2x + y = 3, x + y = 2
        # Solución: x = 1, y = 1
        A = [[2, 1], [1, 1]]
        b = [3, 2]
        
        solution = advanced_methods.gaussian_elimination(A, b)
        
        assert abs(solution[0] - 1.0) < 1e-10, f"x incorrecta: {solution[0]}"
        assert abs(solution[1] - 1.0) < 1e-10, f"y incorrecta: {solution[1]}"

class TestUIComponents:
    """Tests de componentes de interfaz."""
    
    def test_theme_functionality(self):
        """Test de funcionalidad del tema."""
        from gui.themes import DarkTheme
        
        # Test stylesheet principal
        main_style = DarkTheme.get_main_stylesheet()
        assert isinstance(main_style, str), "Stylesheet debe ser string"
        assert len(main_style) > 100, "Stylesheet muy corto"
        assert "background-color" in main_style, "Falta color de fondo"
        
        # Test estilos de botones
        button_styles = ["primary", "secondary", "danger", "success"]
        for style_type in button_styles:
            style = DarkTheme.get_button_style(style_type)
            assert isinstance(style, str), f"Estilo {style_type} debe ser string"
            assert "QPushButton" in style, f"Estilo {style_type} incompleto"
        
        # Test estilos de teclado
        keyboard_styles = ["function", "operator", "clear"]
        for style_type in keyboard_styles:
            style = DarkTheme.get_keyboard_button_style(style_type)
            assert isinstance(style, str), f"Estilo teclado {style_type} debe ser string"
            assert "QPushButton" in style, f"Estilo teclado {style_type} incompleto"
    
    def test_animation_components(self):
        """Test de componentes de animación."""
        from gui.animations import AnimationUtils
        
        # Test duración de animación
        duration = AnimationUtils.get_animation_duration("fast")
        assert isinstance(duration, int), "Duración debe ser entero"
        assert duration > 0, "Duración debe ser positiva"
        
        # Test curva de animación
        curve = AnimationUtils.get_easing_curve("ease_in_out")
        assert curve is not None, "Curva de animación no debe ser None"

class TestMathParser:
    """Tests del parser matemático."""
    
    @pytest.fixture
    def parser(self):
        """Fixture para parser matemático."""
        from numerics.methods import MathParser
        return MathParser()
    
    def test_basic_expressions(self, parser):
        """Test de expresiones básicas."""
        test_cases = [
            ("2+3", 5),
            ("10-4", 6),
            ("3*4", 12),
            ("15/3", 5),
            ("2^3", 8),
        ]
        
        for expression, expected in test_cases:
            result = parser.evaluate_expression(expression)
            assert abs(result - expected) < 1e-10, f"Error en {expression}: {result} != {expected}"
    
    def test_function_expressions(self, parser):
        """Test de funciones matemáticas."""
        test_cases = [
            ("sin(0)", 0),
            ("cos(0)", 1),
            ("log(1)", 0),
            ("exp(0)", 1),
            ("sqrt(4)", 2),
        ]
        
        for expression, expected in test_cases:
            result = parser.evaluate_expression(expression)
            assert abs(result - expected) < 1e-10, f"Error en {expression}: {result} != {expected}"

class TestComparison:
    """Tests de funcionalidad de comparación."""
    
    def test_method_comparison(self):
        """Test de comparación entre métodos."""
        from gui.comparison_tab import ComparisonTab
        from numerics.methods import NumericalMethods
        
        methods = NumericalMethods()
        
        # Función de prueba: f(x) = x^2 - 4
        def test_function(x):
            return x**2 - 4
        
        def test_derivative(x):
            return 2*x
        
        # Comparar métodos de búsqueda de raíces
        bisection_result = methods.bisection(test_function, 0, 5, tolerance=1e-6)
        newton_result = methods.newton_raphson(test_function, test_derivative, 1.0, tolerance=1e-6)
        secant_result = methods.secant(test_function, 1.0, 3.0, tolerance=1e-6)
        
        # Verificar que todos convergen a la misma raíz
        roots = [bisection_result[0], newton_result[0], secant_result[0]]
        
        for root in roots:
            assert abs(root - 2.0) < 1e-5, f"Raíz incorrecta: {root}"

class TestErrorHandling:
    """Tests de manejo de errores."""
    
    def test_invalid_function_parsing(self):
        """Test de parsing de funciones inválidas."""
        from numerics.methods import MathParser
        
        parser = MathParser()
        
        invalid_expressions = [
            "2++3",
            "sin(",
            "log(-1)",
            "1/0",
            "undefined_function(1)"
        ]
        
        for expr in invalid_expressions:
            try:
                result = parser.evaluate_expression(expr)
                # Si no hay excepción, verificar que el resultado sea válido
                assert not np.isnan(result), f"Resultado inválido para {expr}: {result}"
            except (ValueError, ZeroDivisionError, NameError, SyntaxError):
                # Estas excepciones son esperadas para expresiones inválidas
                pass

class TestPerformance:
    """Tests de rendimiento."""
    
    def test_integration_performance(self):
        """Test de rendimiento de integración."""
        import time
        from numerics.methods import NumericalMethods
        
        methods = NumericalMethods()
        
        def complex_function(x):
            return np.sin(x) * np.exp(-x) * np.cos(2*x)
        
        start_time = time.time()
        result = methods.simpson_integration(complex_function, 0, 10, 10000)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        assert execution_time < 5.0, f"Integración muy lenta: {execution_time}s"
        assert isinstance(result, (int, float)), "Resultado debe ser numérico"

def test_complete_workflow():
    """Test de flujo completo del simulador."""
    from numerics.methods import NumericalMethods, MathParser
    from gui.themes import DarkTheme
    
    # Test workflow: parse -> calculate -> display
    parser = MathParser()
    methods = NumericalMethods()
    
    # 1. Parse una función
    expression = "x^2 - 4"
    func = parser.parse_function(expression)
    
    # 2. Encontrar raíz
    root, iterations, errors = methods.bisection(func, 0, 5, tolerance=1e-6)
    
    # 3. Verificar tema para display
    theme_style = DarkTheme.get_main_stylesheet()
    
    # Validaciones
    assert abs(root - 2.0) < 1e-5, "Workflow: raíz incorrecta"
    assert iterations > 0, "Workflow: iteraciones inválidas"
    assert len(theme_style) > 100, "Workflow: tema inválido"

if __name__ == "__main__":
    # Ejecutar tests con pytest si está disponible, sino ejecutar manualmente
    try:
        import pytest
        pytest.main([__file__, "-v", "--tb=short"])
    except ImportError:
        print("⚠️ pytest no encontrado, ejecutando tests manualmente...")
        
        test_classes = [
            TestImports,
            TestNumericalMethods, 
            TestAdvancedMethods,
            TestUIComponents,
            TestMathParser,
            TestComparison,
            TestErrorHandling,
            TestPerformance
        ]
        
        total_tests = 0
        passed_tests = 0
        
        for test_class in test_classes:
            print(f"\n🧪 Ejecutando {test_class.__name__}...")
            
            instance = test_class()
            methods = [method for method in dir(instance) if method.startswith('test_')]
            
            for method_name in methods:
                total_tests += 1
                try:
                    method = getattr(instance, method_name)
                    
                    # Ejecutar fixtures si es necesario
                    if hasattr(instance, method_name.replace('test_', '') + '_fixture'):
                        fixture_method = getattr(instance, method_name.replace('test_', '') + '_fixture')
                        fixture_result = fixture_method()
                        method(fixture_result)
                    else:
                        method()
                    
                    print(f"  ✅ {method_name}")
                    passed_tests += 1
                    
                except Exception as e:
                    print(f"  ❌ {method_name}: {e}")
        
        # Test de workflow completo
        total_tests += 1
        try:
            test_complete_workflow()
            print(f"  ✅ test_complete_workflow")
            passed_tests += 1
        except Exception as e:
            print(f"  ❌ test_complete_workflow: {e}")
        
        print(f"\n📊 RESULTADOS: {passed_tests}/{total_tests} tests pasaron")
        
        if passed_tests == total_tests:
            print("🎉 ¡Todos los tests pasaron exitosamente!")
        else:
            print(f"⚠️ {total_tests - passed_tests} tests fallaron")
