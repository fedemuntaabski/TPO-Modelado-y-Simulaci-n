"""
Tests para el test runner
Pruebas unitarias para el sistema de ejecución de tests
"""

import unittest
import sys
import os
import tempfile
import subprocess
from unittest.mock import Mock, patch, MagicMock

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_runner import Colors, run_single_test_file, print_banner


class TestTestRunnerFunctions(unittest.TestCase):
    """Tests para funciones del test runner"""

    def test_colors_defined(self):
        """Test que los colores están definidos"""
        self.assertEqual(Colors.GREEN, '\033[92m')
        self.assertEqual(Colors.RED, '\033[91m')
        self.assertEqual(Colors.BLUE, '\033[94m')
        self.assertEqual(Colors.END, '\033[0m')

    @patch('subprocess.run')
    def test_run_single_test_file_success(self, mock_subprocess):
        """Test ejecución exitosa de un archivo de test"""
        # Configurar mock
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "test output"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        # Ejecutar test
        exit_code, passed, time_taken = run_single_test_file("test_example.py")

        # Verificar resultados
        self.assertEqual(exit_code, 0)
        self.assertGreaterEqual(passed, 0)
        self.assertGreater(time_taken, 0)

    def test_print_banner(self):
        """Test impresión del banner"""
        # Este test verifica que no hay errores al imprimir el banner
        try:
            # Capturar output
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                print_banner()

            output = f.getvalue()
            self.assertIn("TEST RUNNER UNIFICADO", output)

        except Exception as e:
            self.fail(f"Error al imprimir banner: {e}")

    @patch('subprocess.run')
    def test_run_single_test_file_failure(self, mock_subprocess):
        """Test ejecución fallida de un archivo de test"""
        # Configurar mock para fallo
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "test failed"
        mock_subprocess.return_value = mock_result

        # Ejecutar test
        exit_code, passed, time_taken = run_single_test_file("test_example.py")

        # Verificar resultados
        self.assertEqual(exit_code, 1)
        self.assertEqual(passed, 0)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_discover_test_files(self, mock_listdir, mock_exists):
        """Test descubrimiento de archivos de test"""
        # Configurar mocks
        mock_exists.return_value = True
        mock_listdir.return_value = [
            'test_numerical.py',
            'test_gui.py',
            'not_a_test.py',
            'test_utils.py'
        ]

        # Simular descubrimiento
        test_files = []
        if os.path.exists("tests"):
            for file in os.listdir("tests"):
                if file.startswith("test_") and file.endswith(".py"):
                    test_files.append(file)

        # Verificar que se encontraron los archivos correctos
        expected_files = ['test_numerical.py', 'test_gui.py', 'test_utils.py']
        self.assertEqual(sorted(test_files), sorted(expected_files))

    def test_print_banner(self):
        """Test impresión del banner"""
        # Este test verifica que no hay errores al imprimir el banner
        try:
            # Capturar output
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                print_banner()

            output = f.getvalue()
            self.assertIn("TEST RUNNER UNIFICADO", output)
            self.assertIn("Simulador Matemático Avanzado", output)

        except Exception as e:
            self.fail(f"Error al imprimir banner: {e}")


class TestTestRunnerIntegration(unittest.TestCase):
    """Tests de integración para el test runner"""

    def test_test_structure(self):
        """Test que la estructura de tests es correcta"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tests_path = os.path.join(base_path, 'tests')

        # Verificar que existe el directorio de tests
        self.assertTrue(os.path.exists(tests_path),
                       "Directorio tests/ no existe")

        # Verificar que existe test_runner.py
        test_runner_path = os.path.join(base_path, 'test_runner.py')
        self.assertTrue(os.path.exists(test_runner_path),
                       "Archivo test_runner.py no existe")

    @patch('subprocess.run')
    def test_full_test_execution_simulation(self, mock_subprocess):
        """Test simulación de ejecución completa de tests"""
        # Configurar mock para simular ejecución exitosa
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Ran 5 tests in 0.123s\n\nOK"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        # Simular ejecución de múltiples tests
        test_files = ['test_numerical.py', 'test_utils.py', 'test_gui.py']
        total_passed = 0
        total_failed = 0

        for test_file in test_files:
            exit_code, passed, time_taken = run_single_test_file(test_file)
            if exit_code == 0:
                total_passed += passed
            else:
                total_failed += 1

        # Verificar que se ejecutaron correctamente
        self.assertGreaterEqual(total_passed, 0)
        self.assertEqual(total_failed, 0)


class TestTestConfiguration(unittest.TestCase):
    """Tests para configuración de tests"""

    def test_python_path_configuration(self):
        """Test que el path de Python está configurado correctamente"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Verificar que el directorio raíz está en sys.path
        self.assertIn(base_path, sys.path)

    def test_test_imports(self):
        """Test que se pueden importar los módulos necesarios para tests"""
        try:
            import unittest
            import numpy as np
            import matplotlib
            import scipy
            import sympy

            # Verificar que unittest está disponible
            self.assertTrue(hasattr(unittest, 'TestCase'))

            # Verificar que numpy está disponible
            self.assertTrue(hasattr(np, 'array'))

        except ImportError as e:
            self.fail(f"Error importando módulo necesario: {e}")

    def test_test_file_structure(self):
        """Test que los archivos de test tienen la estructura correcta"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tests_path = os.path.join(base_path, 'tests')

        if os.path.exists(tests_path):
            for file_name in os.listdir(tests_path):
                if file_name.startswith('test_') and file_name.endswith('.py'):
                    file_path = os.path.join(tests_path, file_name)

                    # Verificar que el archivo se puede leer
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Verificar que tiene estructura básica de test
                    self.assertIn('import unittest', content)
                    self.assertIn('class', content)


if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.INFO)

    # Ejecutar tests
    unittest.main(verbosity=2)
