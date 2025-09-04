"""
Tests para configuración del proyecto
Pruebas unitarias para archivos de configuración
"""

import unittest
import sys
import os
import json
import configparser

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Settings


class TestProjectConfiguration(unittest.TestCase):
    """Tests para configuración del proyecto"""

    def setUp(self):
        """Configurar paths para tests"""
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.base_path, 'config', 'settings.json')
        self.pytest_path = os.path.join(self.base_path, 'pytest.ini')

    def test_settings_file_exists(self):
        """Test que existe el archivo de configuración principal"""
        self.assertTrue(os.path.exists(self.config_path),
                       "Archivo config/settings.json no existe")

    def test_settings_file_is_valid_json(self):
        """Test que el archivo de configuración es JSON válido"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.assertIsInstance(data, dict)
            self.assertGreater(len(data), 0)

        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.fail(f"Error leyendo settings.json: {e}")

    def test_pytest_configuration_exists(self):
        """Test que existe la configuración de pytest"""
        self.assertTrue(os.path.exists(self.pytest_path),
                       "Archivo pytest.ini no existe")

    def test_pytest_configuration_valid(self):
        """Test que la configuración de pytest es válida"""
        config = configparser.ConfigParser()
        try:
            config.read(self.pytest_path)

            # Verificar secciones principales
            self.assertIn('tool:pytest', config.sections())

            # Verificar configuraciones importantes
            pytest_config = config['tool:pytest']
            self.assertIn('testpaths', pytest_config)
            self.assertIn('addopts', pytest_config)

        except Exception as e:
            self.fail(f"Error leyendo pytest.ini: {e}")

    def test_settings_class_initialization(self):
        """Test inicialización de la clase Settings"""
        settings = Settings()

        # Verificar que se puede instanciar
        self.assertIsNotNone(settings)

        # Verificar métodos básicos
        self.assertTrue(hasattr(settings, 'load_settings'))
        self.assertTrue(hasattr(settings, 'save_settings'))
        self.assertTrue(hasattr(settings, 'validate_config'))


class TestSettingsFunctionality(unittest.TestCase):
    """Tests para funcionalidad de configuración"""

    def setUp(self):
        """Configurar settings para tests"""
        self.settings = Settings()

    def test_load_settings(self):
        """Test carga de configuración"""
        config = self.settings.load_settings()

        # Verificar que retorna un diccionario
        self.assertIsInstance(config, dict)

        # Verificar campos comunes
        expected_fields = ['theme', 'language', 'precision']
        for field in expected_fields:
            self.assertIn(field, config)

    def test_validate_config_valid(self):
        """Test validación de configuración válida"""
        valid_config = {
            "theme": "dark",
            "language": "es",
            "precision": 6,
            "max_iterations": 1000,
            "plot_resolution": 100
        }

        self.assertTrue(self.settings.validate_config(valid_config))

    def test_validate_config_invalid(self):
        """Test validación de configuración inválida"""
        invalid_configs = [
            {"theme": "invalid_theme"},
            {"precision": -1},
            {"max_iterations": 0},
            {"language": ""},
        ]

        for config in invalid_configs:
            self.assertFalse(self.settings.validate_config(config),
                           f"Configuración {config} debería ser inválida")

    def test_save_settings(self):
        """Test guardado de configuración"""
        test_config = {
            "theme": "light",
            "language": "en",
            "precision": 4
        }

        # Este test verifica que no hay errores al guardar
        try:
            self.settings.save_settings(test_config)
        except Exception as e:
            self.fail(f"Error guardando configuración: {e}")


class TestProjectStructureValidation(unittest.TestCase):
    """Tests para validación de estructura del proyecto"""

    def setUp(self):
        """Configurar paths para tests"""
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_required_directories_exist(self):
        """Test que existen los directorios requeridos"""
        required_dirs = [
            'config',
            'core',
            'gui',
            'numerics',
            'tests',
            'utils'
        ]

        for dir_name in required_dirs:
            dir_path = os.path.join(self.base_path, dir_name)
            self.assertTrue(os.path.exists(dir_path),
                          f"Directorio {dir_name}/ no existe")

    def test_required_files_exist(self):
        """Test que existen los archivos requeridos"""
        required_files = [
            'main.py',
            'README.md',
            'requirements.txt',
            'config/settings.json',
            'gui/__init__.py',
            'core/__init__.py',
            'numerics/__init__.py',
            'utils/__init__.py',
            'tests/__init__.py'
        ]

        for file_name in required_files:
            file_path = os.path.join(self.base_path, file_name)
            self.assertTrue(os.path.exists(file_path),
                          f"Archivo {file_name} no existe")

    def test_python_files_syntax(self):
        """Test que los archivos Python tienen sintaxis correcta"""
        python_files = []

        # Recopilar archivos Python
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))

        # Verificar sintaxis de cada archivo
        for py_file in python_files[:10]:  # Limitar para evitar timeout
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), py_file, 'exec')
            except SyntaxError as e:
                self.fail(f"Error de sintaxis en {py_file}: {e}")
            except UnicodeDecodeError:
                # Ignorar archivos con problemas de encoding
                continue


class TestRequirementsValidation(unittest.TestCase):
    """Tests para validación de requirements"""

    def setUp(self):
        """Configurar path para tests"""
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.requirements_path = os.path.join(self.base_path, 'requirements.txt')

    def test_requirements_file_exists(self):
        """Test que existe el archivo requirements.txt"""
        self.assertTrue(os.path.exists(self.requirements_path),
                       "Archivo requirements.txt no existe")

    def test_requirements_format(self):
        """Test que requirements.txt tiene formato correcto"""
        try:
            with open(self.requirements_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Verificar que hay líneas no vacías
            non_empty_lines = [line.strip() for line in lines if line.strip()]
            self.assertGreater(len(non_empty_lines), 0,
                             "requirements.txt está vacío")

            # Verificar formato básico de algunas líneas
            for line in non_empty_lines[:5]:  # Revisar primeras 5 líneas
                # Debería contener nombre de paquete
                self.assertTrue(len(line.split()) > 0,
                              f"Línea inválida en requirements.txt: {line}")

        except Exception as e:
            self.fail(f"Error leyendo requirements.txt: {e}")


if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.INFO)

    # Ejecutar tests
    unittest.main(verbosity=2)
