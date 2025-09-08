"""
Suite de tests completa para todos los módulos del proyecto.

Ejecuta todos los tests unitarios de manera organizada.
"""

import unittest
import sys
import subprocess
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Importar todos los módulos de test
from tests.test_root_finding import TestRootFinding, TestRootFindingAdvanced
from tests.test_ode_solver import TestODESolver, TestODESystemSolver, TestODEEdgeCases
from tests.test_newton_cotes import TestFunctionParser, TestIntegrationValidator, TestNewtonCotes, TestIntegrationAccuracy
from tests.test_finite_differences import TestFiniteDifferences, TestFiniteDifferencesAdvanced, TestFiniteDifferencesEdgeCases, TestNewFiniteDifferences


def create_test_suite():
    """Crea la suite completa de tests"""
    suite = unittest.TestSuite()
    
    # Tests de búsqueda de raíces
    suite.addTest(unittest.makeSuite(TestRootFinding))
    suite.addTest(unittest.makeSuite(TestRootFindingAdvanced))
    
    # Tests de integración (usando Newton-Cotes)
    suite.addTest(unittest.makeSuite(TestFunctionParser))
    suite.addTest(unittest.makeSuite(TestIntegrationValidator))
    suite.addTest(unittest.makeSuite(TestNewtonCotes))
    suite.addTest(unittest.makeSuite(TestIntegrationAccuracy))
    
    # Tests de ODEs
    suite.addTest(unittest.makeSuite(TestODESolver))
    suite.addTest(unittest.makeSuite(TestODESystemSolver))
    suite.addTest(unittest.makeSuite(TestODEEdgeCases))
    
    # Tests de diferencias finitas
    suite.addTest(unittest.makeSuite(TestFiniteDifferences))
    suite.addTest(unittest.makeSuite(TestFiniteDifferencesAdvanced))
    suite.addTest(unittest.makeSuite(TestFiniteDifferencesEdgeCases))
    suite.addTest(unittest.makeSuite(TestNewFiniteDifferences))
    
    return suite


def run_type_check():
    """Ejecuta verificación de type hints usando mypy"""
    print("\n🔍 Verificando type hints con mypy...")
    
    try:
        # Ejecutar mypy en los directorios principales
        result = subprocess.run([
            sys.executable, "-m", "mypy",
            "--ignore-missing-imports",
            "--no-strict-optional", 
            "--show-error-codes",
            "src/core",
            "src/ui/components",
            "src/ui/tabs"
        ], capture_output=True, text=True, cwd=root_dir)
        
        if result.returncode == 0:
            print("✅ Todos los type hints son correctos!")
            return True
        else:
            print("❌ Se encontraron errores de type hints:")
            print(result.stdout)
            if result.stderr:
                print("Errores adicionales:")
                print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("⚠️  mypy no está instalado. Instale con: pip install mypy")
        print("   Omitiendo verificación de tipos...")
        return True  # No fallar si mypy no está disponible


def run_all_tests():
    """Ejecuta todos los tests con reporte detallado"""
    print("="*70)
    print("EJECUTANDO SUITE COMPLETA DE TESTS")
    print("="*70)
    
    # Verificación de tipos primero
    type_check_passed = run_type_check()
    
    # Crear runner con verbosidad alta
    runner = unittest.TextTestRunner(
        verbosity=2,
        buffer=True,
        failfast=False
    )
    
    # Ejecutar tests
    suite = create_test_suite()
    result = runner.run(suite)
    
    # Reporte final
    print("\n" + "="*70)
    print("RESUMEN FINAL")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print(f"Omitidos: {len(result.skipped)}")
    
    if result.failures:
        print(f"\nFALLOS ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\nERRORES ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\nTasa de éxito: {success_rate:.1f}%")
    
    # Verificación final
    all_passed = result.wasSuccessful() and type_check_passed
    if all_passed:
        print("🎉 ¡Todos los tests y verificaciones pasaron exitosamente!")
    else:
        print("⚠️  Algunos tests o verificaciones fallaron.")
    
    return all_passed


def run_specific_module(module_name):
    """Ejecuta tests de un módulo específico"""
    module_tests = {
        'root_finding': [TestRootFinding, TestRootFindingAdvanced],
        'integration': [TestFunctionParser, TestIntegrationValidator, TestNewtonCotes, TestIntegrationAccuracy],
        'ode_solver': [TestODESolver, TestODESystemSolver, TestODEEdgeCases],
        'finite_differences': [TestFiniteDifferences, TestFiniteDifferencesAdvanced, TestFiniteDifferencesEdgeCases, TestNewFiniteDifferences]
    }
    
    if module_name not in module_tests:
        print(f"Módulo '{module_name}' no encontrado.")
        print(f"Módulos disponibles: {list(module_tests.keys())}")
        return False
    
    print(f"Ejecutando tests del módulo: {module_name}")
    print("-" * 50)
    
    suite = unittest.TestSuite()
    for test_class in module_tests[module_name]:
        suite.addTest(unittest.makeSuite(test_class))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Ejecutar módulo específico
        module = sys.argv[1]
        run_specific_module(module)
    else:
        # Ejecutar todos los tests
        run_all_tests()
