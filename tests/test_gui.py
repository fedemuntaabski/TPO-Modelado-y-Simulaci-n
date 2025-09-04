"""
Tests para la interfaz gráfica
Pruebas unitarias para componentes GUI
"""

import unittest
import sys
import os
from unittest.mock import Mock, MagicMock

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock para PyQt6 si no está disponible en el entorno de test
try:
    from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QComboBox
    from PyQt6.QtCore import Qt
    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False
    # Crear mocks básicos
    class QWidget: pass
    class QLineEdit: pass
    class QComboBox: pass
    Qt = Mock()

from gui.roots_tab_ui import RootsTabUI
from gui.roots_tab_methods import RootsTabMethods
from gui.roots_tab_plotting import RootsTabPlotting
from utils.function_parser import FunctionParser
from utils.validators import InputValidator


@unittest.skipUnless(PYQT6_AVAILABLE, "PyQt6 no está disponible")
class TestRootsTabUI(unittest.TestCase):
    """Tests para la interfaz de usuario de la pestaña de raíces"""

    def setUp(self):
        """Configurar aplicación Qt para tests"""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication([])

        # Crear mocks para dependencias
        self.keyboard = Mock()
        self.plot_widget = Mock()

    def test_ui_initialization(self):
        """Test inicialización de la interfaz"""
        ui = RootsTabUI(self.keyboard, self.plot_widget)

        # Verificar que se crearon los widgets principales
        self.assertIsNotNone(ui.main_splitter)
        self.assertIsNotNone(ui.left_panel)
        self.assertIsNotNone(ui.right_panel)

        # Verificar widgets de entrada
        self.assertIsNotNone(ui.function_input)
        self.assertIsNotNone(ui.method_combo)
        self.assertIsNotNone(ui.solve_button)
        self.assertIsNotNone(ui.results_text)

    def test_method_change_updates_ui(self):
        """Test que cambiar método actualiza la UI correctamente"""
        ui = RootsTabUI(self.keyboard, self.plot_widget)

        # Test método de bisección
        ui.method_combo.setCurrentText("Bisección")
        ui.on_method_changed()

        # Verificar que se crearon los inputs para bisección
        self.assertTrue(hasattr(ui, 'a_input'))
        self.assertTrue(hasattr(ui, 'b_input'))

        # Test método Newton-Raphson
        ui.method_combo.setCurrentText("Newton-Raphson")
        ui.on_method_changed()

        # Verificar que se crearon los inputs para Newton
        self.assertTrue(hasattr(ui, 'x0_input'))
        self.assertTrue(hasattr(ui, 'derivative_input'))

    def test_get_main_widget(self):
        """Test que get_main_widget retorna el widget correcto"""
        ui = RootsTabUI(self.keyboard, self.plot_widget)

        main_widget = ui.get_main_widget()
        self.assertEqual(main_widget, ui.main_splitter)


class TestRootsTabMethods(unittest.TestCase):
    """Tests para los métodos de la pestaña de raíces"""

    def setUp(self):
        """Configurar mocks para tests"""
        # Mock UI
        self.mock_ui = Mock()
        self.mock_ui.function_input = Mock()
        self.mock_ui.function_input.text.return_value = "x**2 - 4"
        self.mock_ui.method_combo = Mock()
        self.mock_ui.method_combo.currentText.return_value = "Bisección"
        self.mock_ui.a_input = Mock()
        self.mock_ui.a_input.text.return_value = "1"
        self.mock_ui.b_input = Mock()
        self.mock_ui.b_input.text.return_value = "3"
        self.mock_ui.tolerance_input = Mock()
        self.mock_ui.tolerance_input.text.return_value = "1e-6"
        self.mock_ui.max_iter_input = Mock()
        self.mock_ui.max_iter_input.text.return_value = "100"
        self.mock_ui.results_text = Mock()

        # Mock plotting
        self.mock_plotting = Mock()

        # Crear instancia de methods
        self.methods = RootsTabMethods(self.mock_ui)

    def test_find_root_bisection(self):
        """Test búsqueda de raíz con método de bisección"""
        # Configurar UI para bisección
        self.mock_ui.method_combo.currentText.return_value = "Bisección"

        # Ejecutar búsqueda
        self.methods.find_root()

        # Verificar que se llamó a clear y append en results_text
        self.mock_ui.results_text.clear.assert_called_once()
        self.mock_ui.results_text.append.assert_called()

    def test_find_root_newton(self):
        """Test búsqueda de raíz con método de Newton-Raphson"""
        # Configurar UI para Newton
        self.mock_ui.method_combo.currentText.return_value = "Newton-Raphson"
        self.mock_ui.x0_input = Mock()
        self.mock_ui.x0_input.text.return_value = "1.5"
        self.mock_ui.derivative_input = Mock()
        self.mock_ui.derivative_input.text.return_value = "2*x"

        # Ejecutar búsqueda
        self.methods.find_root()

        # Verificar que se llamó a clear y append en results_text
        self.mock_ui.results_text.clear.assert_called_once()
        self.mock_ui.results_text.append.assert_called()


class TestRootsTabPlotting(unittest.TestCase):
    """Tests para la funcionalidad de graficación"""

    def setUp(self):
        """Configurar mocks para tests"""
        self.mock_plot_widget = Mock()
        self.plotting = RootsTabPlotting(self.mock_plot_widget)

    def test_plot_function(self):
        """Test graficación de función"""
        def f(x):
            return x**2 - 4

        x_range = (-5, 5)

        self.plotting.plot_function(f, x_range)

        # Verificar que se llamó a plot en el widget
        self.mock_plot_widget.plot.assert_called()

    def test_plot_root(self):
        """Test graficación de raíz encontrada"""
        root = 2.0

        self.plotting.plot_root(root)

        # Verificar que se llamó a plot_point
        self.mock_plot_widget.plot_point.assert_called_with(root, 0, 'red', 'Raíz encontrada')


class TestGUIIntegration(unittest.TestCase):
    """Tests de integración para la GUI"""

    def setUp(self):
        """Configurar entorno de test"""
        self.parser = FunctionParser()
        self.validator = InputValidator()

    def test_function_input_validation(self):
        """Test validación de entrada de función"""
        valid_functions = [
            "x**2 - 4",
            "sin(x) + cos(x)",
            "exp(-x**2)",
            "sqrt(x) + 1"
        ]

        for func_str in valid_functions:
            self.assertTrue(self.validator.is_valid_function(func_str),
                          f"Función {func_str} debería ser válida")

            # Verificar que se puede parsear
            func = self.parser.parse_function(func_str)
            result = func(1.0)
            self.assertIsInstance(result, (int, float))

    def test_numeric_input_validation(self):
        """Test validación de entradas numéricas"""
        valid_inputs = ["1", "1.5", "-2.3", "1e-6", "100"]
        invalid_inputs = ["abc", "1.2.3", "", "inf", "nan"]

        for inp in valid_inputs:
            self.assertTrue(self.validator.is_numeric(inp),
                          f"Input {inp} debería ser numérico válido")

        for inp in invalid_inputs:
            self.assertFalse(self.validator.is_numeric(inp),
                           f"Input {inp} debería ser numérico inválido")


if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.INFO)

    # Ejecutar tests
    unittest.main(verbosity=2)
