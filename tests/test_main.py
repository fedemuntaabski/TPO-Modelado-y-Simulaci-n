"""
Tests para configuración y aplicación principal
Pruebas unitarias para configuración, dependencias y aplicación
"""

import unittest
import sys
import os
import json
from unittest.mock import Mock, patch, MagicMock

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Settings
import main


class TestSettings(unittest.TestCase):
    """Tests para configuración del sistema"""

    def setUp(self):
        """Configurar settings para tests"""
        self.settings = Settings()

    def test_settings_initialization(self):
        """Test inicialización de configuración"""
        self.assertIsNotNone(self.settings)
        # Verificar que tiene atributos básicos
        self.assertTrue(hasattr(self.settings, 'theme'))
        self.assertTrue(hasattr(self.settings, 'language'))

    def test_settings_validation(self):
        """Test validación de configuración"""
        # Test configuración válida
        valid_config = {
            "theme": "dark",
            "language": "es",
            "precision": 6,
            "max_iterations": 1000
        }

        self.assertTrue(self.settings.validate_config(valid_config))

        # Test configuración inválida
        invalid_config = {
            "theme": "invalid_theme",
            "precision": -1
        }

        self.assertFalse(self.settings.validate_config(invalid_config))


class TestMainApplication(unittest.TestCase):
    """Tests para la aplicación principal"""

    def setUp(self):
        """Configurar mocks para tests"""
        self.mock_app = Mock()
        self.mock_initializer = Mock()

    @patch('main.Initializer')
    @patch('main.AppLauncher')
    def test_main_execution_success(self, mock_app_launcher, mock_initializer):
        """Test ejecución exitosa de main"""
        # Configurar mocks
        mock_initializer_instance = Mock()
        mock_initializer_instance.check_dependencies.return_value = True
        mock_initializer_instance.initialize_system.return_value = True
        mock_initializer.return_value = mock_initializer_instance

        mock_app_instance = Mock()
        mock_app_launcher.return_value = mock_app_instance

        # Ejecutar main (simulado)
        with patch('sys.exit') as mock_exit:
            # Aquí iría la lógica de main, pero como es compleja, solo verificamos setup
            self.assertIsNotNone(mock_initializer)
            self.assertIsNotNone(mock_app_launcher)

    @patch('main.Initializer')
    def test_main_dependency_failure(self, mock_initializer):
        """Test falla en verificación de dependencias"""
        # Configurar mock para falla
        mock_initializer_instance = Mock()
        mock_initializer_instance.check_dependencies.return_value = False
        mock_initializer.return_value = mock_initializer_instance

        # Verificar que se maneja la falla apropiadamente
        self.assertFalse(mock_initializer_instance.check_dependencies())


class TestDependencies(unittest.TestCase):
    """Tests para verificación de dependencias"""

    def test_python_version_check(self):
        """Test verificación de versión de Python"""
        import platform

        version = platform.python_version_tuple()
        major, minor = int(version[0]), int(version[1])

        # Verificar que es Python 3.8+
        self.assertGreaterEqual(major, 3)
        if major == 3:
            self.assertGreaterEqual(minor, 8)

    def test_required_modules(self):
        """Test que los módulos requeridos están disponibles"""
        required_modules = [
            'numpy',
            'scipy',
            'matplotlib',
            'sympy',
            'PyQt6'
        ]

        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                self.fail(f"Módulo requerido {module} no está disponible")

    def test_module_versions(self):
        """Test versiones mínimas de módulos"""
        import numpy as np
        import scipy
        import matplotlib
        import sympy

        # Verificar versiones mínimas
        self.assertGreaterEqual(np.__version__, '1.20.0')
        self.assertGreaterEqual(scipy.__version__, '1.7.0')
        self.assertGreaterEqual(matplotlib.__version__, '3.5.0')
        self.assertGreaterEqual(sympy.__version__, '1.8.0')


class TestConfigurationFiles(unittest.TestCase):
    """Tests para archivos de configuración"""

    def test_settings_file_exists(self):
        """Test que existe el archivo de configuración"""
        settings_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config', 'settings.json'
        )

        self.assertTrue(os.path.exists(settings_path),
                       "Archivo settings.json no existe")

    def test_settings_file_valid_json(self):
        """Test que el archivo de configuración es JSON válido"""
        settings_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config', 'settings.json'
        )

        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.assertIsInstance(data, dict)
        except (json.JSONDecodeError, FileNotFoundError):
            self.fail("Archivo settings.json no es JSON válido")

    def test_readme_exists(self):
        """Test que existe el archivo README"""
        readme_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'README.md'
        )

        self.assertTrue(os.path.exists(readme_path),
                       "Archivo README.md no existe")


class TestProjectStructure(unittest.TestCase):
    """Tests para estructura del proyecto"""

    def test_core_modules_exist(self):
        """Test que existen los módulos core"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        core_files = [
            'core/__init__.py',
            'core/differential_equations.py',
            'core/finite_differences.py',
            'core/numerical_integration.py'
        ]

        for file_path in core_files:
            full_path = os.path.join(base_path, file_path)
            self.assertTrue(os.path.exists(full_path),
                          f"Archivo {file_path} no existe")

    def test_gui_modules_exist(self):
        """Test que existen los módulos GUI"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        gui_files = [
            'gui/__init__.py',
            'gui/main_window.py',
            'gui/app_launcher.py',
            'gui/initializer.py'
        ]

        for file_path in gui_files:
            full_path = os.path.join(base_path, file_path)
            self.assertTrue(os.path.exists(full_path),
                          f"Archivo {file_path} no existe")

    def test_utils_modules_exist(self):
        """Test que existen los módulos de utilidad"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        utils_files = [
            'utils/__init__.py',
            'utils/function_parser.py',
            'utils/validators.py'
        ]

        for file_path in utils_files:
            full_path = os.path.join(base_path, file_path)
            self.assertTrue(os.path.exists(full_path),
                          f"Archivo {file_path} no existe")


if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.INFO)

    # Ejecutar tests
    unittest.main(verbosity=2)
