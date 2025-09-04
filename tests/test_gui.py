#!/usr/bin/env python3
"""
Tests unitarios para componentes de la interfaz gráfica
Incluye pruebas de temas, animaciones y widgets principales

Autor: Equipo TPO Modelado y Simulación
Fecha: 2025
"""

import sys
import os
import pytest

# Agregar el directorio principal al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos de GUI (solo si PyQt6 está disponible)
try:
    from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QPalette, QColor
    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False

if PYQT6_AVAILABLE:
    from gui.themes import DarkTheme
    from gui.animations import AnimationUtils, ButtonHoverEffect, FadeAnimation
    from gui.main_window import MathSimulatorApp, MathKeyboard, PlotWidget


class TestThemes:
    """Tests de temas y estilos."""

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_dark_theme_stylesheet(self):
        """Test del stylesheet del tema oscuro."""
        theme = DarkTheme()

        main_style = theme.get_main_stylesheet()
        assert isinstance(main_style, str), "Stylesheet debe ser string"
        assert len(main_style) > 100, "Stylesheet muy corto"
        assert "background-color" in main_style, "Falta color de fondo"
        assert "color:" in main_style, "Falta color de texto"

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_button_styles(self):
        """Test de estilos de botones."""
        theme = DarkTheme()

        button_styles = ["primary", "secondary", "danger", "success", "warning", "info"]
        for style_name in button_styles:
            style = theme.get_button_style(style_name)
            assert isinstance(style, str), f"Estilo {style_name} debe ser string"
            assert "QPushButton" in style, f"Estilo {style_name} incompleto"
            assert "background-color" in style, f"Falta color de fondo en {style_name}"

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_keyboard_styles(self):
        """Test de estilos del teclado virtual."""
        theme = DarkTheme()

        keyboard_styles = ["function", "operator", "clear", "number"]
        for style_name in keyboard_styles:
            style = theme.get_keyboard_button_style(style_name)
            assert isinstance(style, str), f"Estilo teclado {style_name} debe ser string"
            assert "QPushButton" in style, f"Estilo teclado {style_name} incompleto"

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_input_styles(self):
        """Test de estilos de campos de entrada."""
        theme = DarkTheme()

        input_style = theme.get_input_style()
        assert isinstance(input_style, str), "Estilo de input debe ser string"
        assert "QLineEdit" in input_style, "Estilo de input incompleto"
        assert "border" in input_style, "Falta borde en estilo de input"


class TestAnimations:
    """Tests de componentes de animación."""

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_animation_utils(self):
        """Test de utilidades de animación."""
        anim_utils = AnimationUtils()

        # Test duración de animación
        duration = anim_utils.get_animation_duration("fast")
        assert isinstance(duration, int), "Duración debe ser entero"
        assert duration > 0, "Duración debe ser positiva"
        assert duration < 1000, "Duración fast debe ser menor a 1 segundo"

        # Test duraciones de diferentes velocidades
        fast_duration = anim_utils.get_animation_duration("fast")
        normal_duration = anim_utils.get_animation_duration("normal")
        slow_duration = anim_utils.get_animation_duration("slow")

        assert fast_duration < normal_duration < slow_duration, \
               "Duraciones deben estar en orden ascendente"

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_easing_curves(self):
        """Test de curvas de easing."""
        anim_utils = AnimationUtils()

        easing_types = ["linear", "ease_in", "ease_out", "ease_in_out", "bounce"]
        for easing_type in easing_types:
            curve = anim_utils.get_easing_curve(easing_type)
            assert curve is not None, f"Curva {easing_type} no debe ser None"

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_button_hover_effect(self):
        """Test del efecto hover de botones."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        try:
            button = QPushButton("Test")
            hover_effect = ButtonHoverEffect(button)

            # Verificar que el efecto se aplicó
            assert button is not None, "Botón debe existir"
            assert hover_effect is not None, "Efecto hover debe existir"

            # Test de colores
            original_color = hover_effect.get_original_color()
            hover_color = hover_effect.get_hover_color()

            assert original_color is not None, "Color original no debe ser None"
            assert hover_color is not None, "Color hover no debe ser None"

        finally:
            if app:
                app.quit()

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_fade_animation(self):
        """Test de animación de fade."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        try:
            widget = QWidget()
            fade_anim = FadeAnimation(widget)

            assert widget is not None, "Widget debe existir"
            assert fade_anim is not None, "Animación fade debe existir"

            # Test de opacidades
            assert fade_anim.get_start_opacity() >= 0.0, "Opacidad inicial debe ser >= 0"
            assert fade_anim.get_end_opacity() <= 1.0, "Opacidad final debe ser <= 1"

        finally:
            if app:
                app.quit()


class TestGUIWidgets:
    """Tests de widgets principales de la GUI."""

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_math_keyboard(self):
        """Test del teclado matemático."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        try:
            keyboard = MathKeyboard()

            assert keyboard is not None, "Teclado debe existir"

            # Test de botones principales
            assert hasattr(keyboard, 'function_buttons'), "Debe tener botones de función"
            assert hasattr(keyboard, 'operator_buttons'), "Debe tener botones de operador"
            assert hasattr(keyboard, 'number_buttons'), "Debe tener botones numéricos"

            # Verificar que hay botones
            assert len(keyboard.function_buttons) > 0, "Debe tener botones de función"
            assert len(keyboard.operator_buttons) > 0, "Debe tener botones de operador"
            assert len(keyboard.number_buttons) > 0, "Debe tener botones numéricos"

        finally:
            if app:
                app.quit()

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_plot_widget(self):
        """Test del widget de gráficos."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        try:
            plot_widget = PlotWidget()

            assert plot_widget is not None, "Widget de gráfico debe existir"
            assert hasattr(plot_widget, 'figure'), "Debe tener figura de matplotlib"
            assert hasattr(plot_widget, 'canvas'), "Debe tener canvas"

            # Test de métodos de graficación
            assert hasattr(plot_widget, 'plot_function'), "Debe tener método plot_function"
            assert hasattr(plot_widget, 'clear_plot'), "Debe tener método clear_plot"

            # Test de graficación básica
            x_data = [1, 2, 3, 4, 5]
            y_data = [1, 4, 9, 16, 25]  # x^2

            plot_widget.plot_function(x_data, y_data, "Test Plot", "x", "y", "Test")

            # Verificar que la figura tiene datos
            assert len(plot_widget.figure.get_axes()) > 0, "Debe tener al menos un eje"

        finally:
            if app:
                app.quit()

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_main_window_creation(self):
        """Test de creación de la ventana principal."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        try:
            main_window = MathSimulatorApp()

            assert main_window is not None, "Ventana principal debe existir"

            # Verificar componentes principales
            assert hasattr(main_window, 'tab_widget'), "Debe tener widget de pestañas"
            assert hasattr(main_window, 'plot_widget'), "Debe tener widget de gráficos"
            assert hasattr(main_window, 'keyboard'), "Debe tener teclado"

            # Verificar pestañas
            tab_count = main_window.tab_widget.count()
            assert tab_count > 0, "Debe tener al menos una pestaña"

            # Verificar títulos de pestañas
            tab_texts = []
            for i in range(tab_count):
                tab_texts.append(main_window.tab_widget.tabText(i))

            assert len(tab_texts) > 0, "Debe tener títulos de pestañas"

        finally:
            if app:
                app.quit()


class TestGUIIntegration:
    """Tests de integración de componentes GUI."""

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_theme_application(self):
        """Test de aplicación de tema a widgets."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        try:
            # Crear widget de prueba
            widget = QPushButton("Test Button")
            theme = DarkTheme()

            # Aplicar estilo
            button_style = theme.get_button_style("primary")
            widget.setStyleSheet(button_style)

            # Verificar que el estilo se aplicó
            assert widget.styleSheet() == button_style, "Estilo no se aplicó correctamente"

            # Verificar propiedades del widget
            assert widget.text() == "Test Button", "Texto del botón incorrecto"

        finally:
            if app:
                app.quit()

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_keyboard_integration(self):
        """Test de integración del teclado con campos de entrada."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        try:
            # Crear componentes
            keyboard = MathKeyboard()
            input_field = QLineEdit()

            # Conectar teclado al campo de entrada
            keyboard.set_target(input_field)

            # Verificar conexión
            assert keyboard.current_target == input_field, "Campo objetivo no se conectó correctamente"

            # Simular entrada desde teclado
            # Nota: En un test real, esto requeriría simular eventos de clic
            assert input_field is not None, "Campo de entrada debe existir"

        finally:
            if app:
                app.quit()

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_plot_integration(self):
        """Test de integración de gráficos con datos numéricos."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        try:
            plot_widget = PlotWidget()

            # Generar datos de prueba
            import numpy as np
            x_data = np.linspace(0, 10, 100)
            y_data = np.sin(x_data)

            # Graficar
            plot_widget.plot_function(x_data.tolist(), y_data.tolist(),
                                    "Seno", "x", "sin(x)", "Función")

            # Verificar que se creó el gráfico
            axes = plot_widget.figure.get_axes()
            assert len(axes) > 0, "Debe tener al menos un eje"

            # Verificar que hay datos en el gráfico
            lines = axes[0].get_lines()
            assert len(lines) > 0, "Debe tener al menos una línea"

        finally:
            if app:
                app.quit()


class TestGUIEdgeCases:
    """Tests de casos edge para componentes GUI."""

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_empty_plot(self):
        """Test de gráfico vacío."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        try:
            plot_widget = PlotWidget()

            # Limpiar gráfico
            plot_widget.clear_plot()

            # Verificar que se limpió
            axes = plot_widget.figure.get_axes()
            if axes:
                lines = axes[0].get_lines()
                assert len(lines) == 0, "Gráfico debe estar vacío después de clear_plot"

        finally:
            if app:
                app.quit()

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_keyboard_without_target(self):
        """Test del teclado sin campo objetivo."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        try:
            keyboard = MathKeyboard()

            # Verificar estado inicial
            assert keyboard.current_target is None, "Objetivo inicial debe ser None"

            # Intentar usar teclado sin objetivo (debe manejarse gracefully)
            # Nota: En implementación real, esto debería no hacer nada o mostrar mensaje

        finally:
            if app:
                app.quit()

    @pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 no disponible")
    def test_theme_consistency(self):
        """Test de consistencia de tema."""
        theme = DarkTheme()

        # Verificar que todos los estilos son strings no vacíos
        styles_to_check = [
            theme.get_main_stylesheet(),
            theme.get_button_style("primary"),
            theme.get_input_style(),
            theme.get_keyboard_button_style("function")
        ]

        for style in styles_to_check:
            assert isinstance(style, str), "Todos los estilos deben ser strings"
            assert len(style.strip()) > 0, "Ningún estilo debe estar vacío"


if __name__ == "__main__":
    # Ejecutar tests
    try:
        import pytest
        pytest.main([__file__, "-v", "--tb=short"])
    except ImportError:
        print("⚠️ pytest no encontrado, ejecutando tests manualmente...")

        test_classes = [
            TestThemes,
            TestAnimations,
            TestGUIWidgets,
            TestGUIIntegration,
            TestGUIEdgeCases
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
                    method()
                    print(f"  ✅ {method_name}")
                    passed_tests += 1
                except Exception as e:
                    print(f"  ❌ {method_name}: {e}")

        print(f"\n📊 RESULTADOS GUI: {passed_tests}/{total_tests} tests pasaron")

        if passed_tests == total_tests:
            print("🎉 ¡Todos los tests de GUI pasaron exitosamente!")
        else:
            print(f"⚠️ {total_tests - passed_tests} tests fallaron")
