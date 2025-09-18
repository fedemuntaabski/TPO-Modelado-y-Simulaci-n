"""
Test comprehensivo para todos los métodos de búsqueda de raíces.

Este test verifica la corrección matemática de:
- Método de bisección
- Método de Newton-Raphson  
- Método de punto fijo
- Método de aceleración de Aitken
"""

import numpy as np
import math
import sys
import os

# Agregar el directorio padre al path para importar src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.root_finding import RootFinder, create_function_from_string, convert_to_fixed_point


class TestRootFinding:
    """Test cases para validar métodos de búsqueda de raíces"""
    
    def __init__(self):
        self.solver = RootFinder(tolerance=1e-6, max_iterations=1000)
        self.test_results = []
        
    def test_bisection_method(self):
        """Test del método de bisección con problemas conocidos"""
        print("\n" + "="*60)
        print("TESTING BISECCIÓN METHOD")
        print("="*60)
        
        test_cases = [
            {
                'name': 'x² - 4 = 0',
                'function': 'x**2 - 4',
                'interval': [1, 3],
                'expected_root': 2.0,
                'description': 'Raíz cuadrática simple'
            },
            {
                'name': 'x³ - x - 1 = 0',
                'function': 'x**3 - x - 1',
                'interval': [1, 2],
                'expected_root': 1.3247179572447,
                'description': 'Ecuación cúbica'
            },
            {
                'name': 'cos(x) - x = 0',
                'function': 'cos(x) - x',
                'interval': [0, 1],
                'expected_root': 0.7390851332152,
                'description': 'Ecuación trascendente'
            },
            {
                'name': 'e^x - 2x - 1 = 0',
                'function': 'exp(x) - 2*x - 1',
                'interval': [1, 2],
                'expected_root': 1.256431208626,
                'description': 'Exponencial'
            }
        ]
        
        for test in test_cases:
            print(f"\nTest: {test['name']} - {test['description']}")
            try:
                f = create_function_from_string(test['function'])
                result = self.solver.bisection_method(
                    f, test['interval'][0], test['interval'][1]
                )
                
                error = abs(result.root - test['expected_root'])
                success = error < 1e-5
                
                print(f"  Raíz encontrada: {result.root:.10f}")
                print(f"  Raíz esperada:   {test['expected_root']:.10f}")
                print(f"  Error:           {error:.2e}")
                print(f"  Iteraciones:     {result.iterations}")
                print(f"  Convergió:       {result.converged}")
                print(f"  RESULTADO:       {'✓ PASS' if success else '✗ FAIL'}")
                
                self.test_results.append({
                    'method': 'Bisección',
                    'test': test['name'],
                    'success': success,
                    'error': error,
                    'iterations': result.iterations
                })
                
            except Exception as e:
                print(f"  ERROR: {e}")
                self.test_results.append({
                    'method': 'Bisección',
                    'test': test['name'],
                    'success': False,
                    'error': f"Exception: {e}",
                    'iterations': 0
                })
    
    def test_newton_raphson_method(self):
        """Test del método de Newton-Raphson"""
        print("\n" + "="*60)
        print("TESTING NEWTON-RAPHSON METHOD")
        print("="*60)
        
        test_cases = [
            {
                'name': 'x² - 4 = 0',
                'function': 'x**2 - 4',
                'derivative': '2*x',
                'x0': 1.5,
                'expected_root': 2.0,
                'description': 'Raíz cuadrática con derivada'
            },
            {
                'name': 'x³ - x - 1 = 0',
                'function': 'x**3 - x - 1',
                'derivative': '3*x**2 - 1',
                'x0': 1.5,
                'expected_root': 1.3247179572447,
                'description': 'Ecuación cúbica'
            },
            {
                'name': 'cos(x) - x = 0',
                'function': 'cos(x) - x',
                'derivative': '-sin(x) - 1',
                'x0': 0.5,
                'expected_root': 0.7390851332152,
                'description': 'Ecuación trascendente'
            },
            {
                'name': 'e^x - 2x - 1 = 0',
                'function': 'exp(x) - 2*x - 1',
                'derivative': 'exp(x) - 2',
                'x0': 1.0,
                'expected_root': 1.256431208626,
                'description': 'Exponencial con derivada'
            }
        ]
        
        for test in test_cases:
            print(f"\nTest: {test['name']} - {test['description']}")
            try:
                f = create_function_from_string(test['function'])
                df = create_function_from_string(test['derivative'])
                
                result = self.solver.newton_raphson_method(f, df, test['x0'])
                
                error = abs(result.root - test['expected_root'])
                success = error < 1e-8  # Newton-Raphson debería ser más preciso
                
                print(f"  Punto inicial:   {test['x0']}")
                print(f"  Raíz encontrada: {result.root:.10f}")
                print(f"  Raíz esperada:   {test['expected_root']:.10f}")
                print(f"  Error:           {error:.2e}")
                print(f"  Iteraciones:     {result.iterations}")
                print(f"  Convergió:       {result.converged}")
                print(f"  RESULTADO:       {'✓ PASS' if success else '✗ FAIL'}")
                
                self.test_results.append({
                    'method': 'Newton-Raphson',
                    'test': test['name'],
                    'success': success,
                    'error': error,
                    'iterations': result.iterations
                })
                
            except Exception as e:
                print(f"  ERROR: {e}")
                self.test_results.append({
                    'method': 'Newton-Raphson',
                    'test': test['name'],
                    'success': False,
                    'error': f"Exception: {e}",
                    'iterations': 0
                })
    
    def test_fixed_point_method(self):
        """Test del método de punto fijo"""
        print("\n" + "="*60)
        print("TESTING FIXED POINT METHOD")
        print("="*60)
        
        test_cases = [
            {
                'name': 'x = cos(x)',
                'g_function': 'cos(x)',
                'x0': 0.5,
                'expected_root': 0.7390851332152,
                'description': 'Punto fijo directo'
            },
            {
                'name': 'x = sqrt(x + 1)',
                'g_function': 'sqrt(x + 1)',
                'x0': 1.0,
                'expected_root': 1.618033988749,  # Golden ratio
                'description': 'Raíz cuadrada'
            },
            {
                'name': 'x = (x² + 2)/3',
                'g_function': '(x**2 + 2)/3',
                'x0': 1.0,
                'expected_root': 1.0,  # From x=1, converges to x=1
                'description': 'Función racional'
            },
            {
                'name': 'x = exp(-x)',
                'g_function': 'exp(-x)',
                'x0': 0.5,
                'expected_root': 0.5671432904,
                'description': 'Exponencial negativa'
            }
        ]
        
        for test in test_cases:
            print(f"\nTest: {test['name']} - {test['description']}")
            try:
                g = create_function_from_string(test['g_function'])
                
                result = self.solver.fixed_point_method(g, test['x0'])
                
                error = abs(result.root - test['expected_root'])
                success = error < 1e-5
                
                print(f"  Punto inicial:   {test['x0']}")
                print(f"  Raíz encontrada: {result.root:.10f}")
                print(f"  Raíz esperada:   {test['expected_root']:.10f}")
                print(f"  Error:           {error:.2e}")
                print(f"  Iteraciones:     {result.iterations}")
                print(f"  Convergió:       {result.converged}")
                print(f"  RESULTADO:       {'✓ PASS' if success else '✗ FAIL'}")
                
                self.test_results.append({
                    'method': 'Punto Fijo',
                    'test': test['name'],
                    'success': success,
                    'error': error,
                    'iterations': result.iterations
                })
                
            except Exception as e:
                print(f"  ERROR: {e}")
                self.test_results.append({
                    'method': 'Punto Fijo',
                    'test': test['name'],
                    'success': False,
                    'error': f"Exception: {e}",
                    'iterations': 0
                })
    
    def test_aitken_method(self):
        """Test del método de aceleración de Aitken"""
        print("\n" + "="*60)
        print("TESTING AITKEN ACCELERATION METHOD")
        print("="*60)
        
        # Los mismos casos que punto fijo para comparar convergencia
        test_cases = [
            {
                'name': 'x = cos(x)',
                'g_function': 'cos(x)',
                'x0': 0.5,
                'expected_root': 0.7390851332152,
                'description': 'Punto fijo con aceleración'
            },
            {
                'name': 'x = sqrt(x + 1)',
                'g_function': 'sqrt(x + 1)',
                'x0': 1.0,
                'expected_root': 1.618033988749,
                'description': 'Golden ratio acelerado'
            },
            {
                'name': 'x = (x² + 2)/3',
                'g_function': '(x**2 + 2)/3',
                'x0': 1.0,
                'expected_root': 1.0,  # From x=1, converges to x=1
                'description': 'Función racional acelerada'
            },
            {
                'name': 'x = exp(-x)',
                'g_function': 'exp(-x)',
                'x0': 0.5,
                'expected_root': 0.5671432904,
                'description': 'Exponencial con Aitken'
            }
        ]
        
        for test in test_cases:
            print(f"\nTest: {test['name']} - {test['description']}")
            try:
                g = create_function_from_string(test['g_function'])
                
                result = self.solver.aitken_acceleration(g, test['x0'])
                
                error = abs(result.root - test['expected_root'])
                success = error < 1e-6
                
                print(f"  Punto inicial:   {test['x0']}")
                print(f"  Raíz encontrada: {result.root:.10f}")
                print(f"  Raíz esperada:   {test['expected_root']:.10f}")
                print(f"  Error:           {error:.2e}")
                print(f"  Iteraciones:     {result.iterations}")
                print(f"  Convergió:       {result.converged}")
                print(f"  RESULTADO:       {'✓ PASS' if success else '✗ FAIL'}")
                
                self.test_results.append({
                    'method': 'Aitken',
                    'test': test['name'],
                    'success': success,
                    'error': error,
                    'iterations': result.iterations
                })
                
            except Exception as e:
                print(f"  ERROR: {e}")
                self.test_results.append({
                    'method': 'Aitken',
                    'test': test['name'],
                    'success': False,
                    'error': f"Exception: {e}",
                    'iterations': 0
                })
    
    def run_all_tests(self):
        """Ejecuta todos los tests y muestra un resumen"""
        print("INICIANDO TESTS COMPREHENSIVOS DE BÚSQUEDA DE RAÍCES")
        print("="*60)
        
        # Ejecutar todos los tests
        self.test_bisection_method()
        self.test_newton_raphson_method()
        self.test_fixed_point_method()
        self.test_aitken_method()
        
        # Mostrar resumen
        self.print_summary()
    
    def print_summary(self):
        """Imprime un resumen de todos los tests"""
        print("\n" + "="*80)
        print("RESUMEN FINAL DE TESTS")
        print("="*80)
        
        methods = {}
        for result in self.test_results:
            method = result['method']
            if method not in methods:
                methods[method] = {'total': 0, 'passed': 0, 'failed': 0}
            
            methods[method]['total'] += 1
            if result['success']:
                methods[method]['passed'] += 1
            else:
                methods[method]['failed'] += 1
        
        for method, stats in methods.items():
            success_rate = (stats['passed'] / stats['total']) * 100
            print(f"\n{method}:")
            print(f"  Tests totales: {stats['total']}")
            print(f"  Exitosos:      {stats['passed']}")
            print(f"  Fallidos:      {stats['failed']}")
            print(f"  Tasa éxito:    {success_rate:.1f}%")
        
        # Tests fallidos en detalle
        failed_tests = [r for r in self.test_results if not r['success']]
        if failed_tests:
            print(f"\nTESTS FALLIDOS ({len(failed_tests)} total):")
            for test in failed_tests:
                print(f"  {test['method']}: {test['test']} - {test['error']}")
        
        total_tests = len(self.test_results)
        total_passed = sum(1 for r in self.test_results if r['success'])
        overall_success = (total_passed / total_tests) * 100
        
        print(f"\nRESULTADO GENERAL:")
        print(f"  Total tests:   {total_tests}")
        print(f"  Exitosos:      {total_passed}")
        print(f"  Tasa éxito:    {overall_success:.1f}%")
        print(f"  ESTADO:        {'✓ TODOS LOS MÉTODOS FUNCIONAN' if overall_success >= 90 else '⚠ REVISAR MÉTODOS'}")


if __name__ == "__main__":
    tester = TestRootFinding()
    tester.run_all_tests()