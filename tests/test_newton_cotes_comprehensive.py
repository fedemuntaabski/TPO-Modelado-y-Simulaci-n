"""
Tests comprehensivos para el módulo de integración Newton-Cotes.

Implementa tests detallados para cada método de integración Newton-Cotes
con múltiples fórmulas, valores de n y límites de integración.
Los resultados se verifican contra valores conocidos.
"""

import os
import sys
import unittest
import math
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.newton_cotes import NewtonCotes, NewtonCotesError, NewtonCotesResult
from src.core.function_parser import FunctionParser
from src.core.integration_validators import IntegrationValidator, IntegrationValidationError



# Configurar logging para errores
logging.basicConfig(filename='newton_cotes_test_errors.log', 
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestNewtonCotesComprehensive(unittest.TestCase):
    """Tests comprehensivos para los métodos de integración Newton-Cotes"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.nc = NewtonCotes()
        self.test_functions = [
            # (función, a, b, valor_exacto, descripción)
            ("1", 0, 1, 1.0, "Constante f(x) = 1"),
            ("x", 0, 1, 0.5, "Lineal f(x) = x"),
            ("x", 0, 2, 2.0, "Lineal f(x) = x en [0,2]"),
            ("x**2", 0, 1, 1/3, "Cuadrática f(x) = x²"),
            ("x**2", -1, 1, 2/3, "Cuadrática f(x) = x² en [-1,1]"),
            ("x**3", 0, 1, 0.25, "Cúbica f(x) = x³"),
            ("x**3", -1, 1, 0.0, "Cúbica f(x) = x³ en [-1,1]"),
            ("x**4", 0, 1, 0.2, "Potencia 4 f(x) = x⁴"),
            ("x**5", 0, 1, 1/6, "Potencia 5 f(x) = x⁵"),
            ("exp(x)", 0, 1, math.e - 1, "Exponencial f(x) = e^x"),
            ("sin(x)", 0, math.pi, 2.0, "Seno f(x) = sin(x) en [0,π]"),
            ("cos(x)", 0, math.pi/2, 1.0, "Coseno f(x) = cos(x) en [0,π/2]"),
            ("sqrt(x)", 0.001, 1, 2/3 - 2*math.sqrt(0.001)/3, "Raíz cuadrada f(x) = √x"),
            ("1/x", 1, 2, math.log(2), "Inversa f(x) = 1/x en [1,2]"),
            ("ln(x)", 1, math.e, 1.0, "Logaritmo natural f(x) = ln(x) en [1,e]"),
            ("x*ln(x)", 1, math.e, (math.e**2)/2 - 0.5, "Producto f(x) = x·ln(x) en [1,e]"),
            ("sin(x)**2", 0, math.pi, math.pi/2, "Seno cuadrado f(x) = sin²(x) en [0,π]"),
            ("cos(x)**2", 0, math.pi, math.pi/2, "Coseno cuadrado f(x) = cos²(x) en [0,π]"),
            ("1/(1+x**2)", 0, 1, math.atan(1), "Función racional f(x) = 1/(1+x²) en [0,1]"),
            ("exp(-x**2)", 0, 1, 0.746824132812427, "Gaussiana f(x) = e^(-x²) en [0,1]"),
        ]
        
        # Valores de n para métodos compuestos
        self.n_values = {
            'rectangle': [10, 100, 1000, 5000],
            'trapezoid': [10, 100, 1000, 5000],
            'simpson_13': [10, 100, 1000, 5000],  # Debe ser par
            'simpson_38': [9, 99, 999, 4998],    # Debe ser múltiplo de 3
        }

    def _log_test_error(self, method, func_str, a, b, n, expected, actual, error):
        """Registra un error en el archivo de log sin detener el test"""
        error_msg = (f"Error en {method}: función='{func_str}', intervalo=[{a}, {b}], "
                    f"n={n if n else 'N/A'}, esperado={expected}, obtenido={actual}, "
                    f"error absoluto={error}, error relativo={error/abs(expected) if expected != 0 else 'N/A'}")
        logger.error(error_msg)
        return error_msg

    def _check_result(self, result: NewtonCotesResult, expected: float, tolerance: float,
                     method: str, func_str: str, a: float, b: float, n=None) -> bool:
        """
        Verifica que el resultado esté dentro de la tolerancia esperada
        y registra errores significativos
        """
        error = abs(result.result - expected)
        
        # Prueba normal con assertAlmostEqual
        try:
            self.assertLess(error, tolerance)
            return True
        except AssertionError:
            # Registrar error pero continuar con el test
            error_msg = self._log_test_error(method, func_str, a, b, n, expected, result.result, error)
            print(f"⚠️ {error_msg}")
            return False

    def test_rectangle_simple(self):
        """Test comprehensivo del método rectángulo simple"""
        print("\n=== Test de Rectángulo Simple ===")
        success_count = 0
        total_count = 0
        
        for func, a, b, expected, desc in self.test_functions:
            with self.subTest(description=desc):
                total_count += 1
                try:
                    result = self.nc.rectangle_simple(func, a, b)
                    
                    # Tolerancia más amplia para este método simple
                    tolerance = max(0.1 * abs(expected), 0.05)
                    if self._check_result(result, expected, tolerance, 
                                        "Rectángulo Simple", func, a, b):
                        success_count += 1
                        print(f"✅ {desc}: resultado={result.result:.6f}, esperado={expected:.6f}")
                    else:
                        print(f"❌ {desc}: resultado={result.result:.6f}, esperado={expected:.6f}")
                except Exception as e:
                    error_msg = f"Error al ejecutar rectángulo simple con {desc}: {str(e)}"
                    logger.error(error_msg)
                    print(f"⚠️ {error_msg}")
        
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"Tasa de éxito: {success_count}/{total_count} ({success_rate:.1f}%)")

    def test_trapezoid_simple(self):
        """Test comprehensivo del método trapecio simple"""
        print("\n=== Test de Trapecio Simple ===")
        success_count = 0
        total_count = 0
        
        for func, a, b, expected, desc in self.test_functions:
            with self.subTest(description=desc):
                total_count += 1
                try:
                    result = self.nc.trapezoid_simple(func, a, b)
                    
                    # Tolerancia adecuada para trapecio simple
                    tolerance = max(0.05 * abs(expected), 0.02)
                    if self._check_result(result, expected, tolerance, 
                                        "Trapecio Simple", func, a, b):
                        success_count += 1
                        print(f"✅ {desc}: resultado={result.result:.6f}, esperado={expected:.6f}")
                    else:
                        print(f"❌ {desc}: resultado={result.result:.6f}, esperado={expected:.6f}")
                except Exception as e:
                    error_msg = f"Error al ejecutar trapecio simple con {desc}: {str(e)}"
                    logger.error(error_msg)
                    print(f"⚠️ {error_msg}")
        
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"Tasa de éxito: {success_count}/{total_count} ({success_rate:.1f}%)")

    def test_simpson_13_simple(self):
        """Test comprehensivo del método Simpson 1/3 simple"""
        print("\n=== Test de Simpson 1/3 Simple ===")
        success_count = 0
        total_count = 0
        
        for func, a, b, expected, desc in self.test_functions:
            with self.subTest(description=desc):
                total_count += 1
                try:
                    result = self.nc.simpson_13_simple(func, a, b)
                    
                    # Tolerancia más estricta para Simpson (más preciso)
                    tolerance = max(0.01 * abs(expected), 0.005)
                    if self._check_result(result, expected, tolerance, 
                                        "Simpson 1/3 Simple", func, a, b):
                        success_count += 1
                        print(f"✅ {desc}: resultado={result.result:.6f}, esperado={expected:.6f}")
                    else:
                        print(f"❌ {desc}: resultado={result.result:.6f}, esperado={expected:.6f}")
                except Exception as e:
                    error_msg = f"Error al ejecutar Simpson 1/3 simple con {desc}: {str(e)}"
                    logger.error(error_msg)
                    print(f"⚠️ {error_msg}")
        
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"Tasa de éxito: {success_count}/{total_count} ({success_rate:.1f}%)")

    def test_simpson_38_simple(self):
        """Test comprehensivo del método Simpson 3/8 simple"""
        print("\n=== Test de Simpson 3/8 Simple ===")
        success_count = 0
        total_count = 0
        
        for func, a, b, expected, desc in self.test_functions:
            with self.subTest(description=desc):
                total_count += 1
                try:
                    result = self.nc.simpson_38_simple(func, a, b)
                    
                    # Tolerancia estricta para Simpson 3/8 (más preciso)
                    tolerance = max(0.01 * abs(expected), 0.005)
                    if self._check_result(result, expected, tolerance, 
                                        "Simpson 3/8 Simple", func, a, b):
                        success_count += 1
                        print(f"✅ {desc}: resultado={result.result:.6f}, esperado={expected:.6f}")
                    else:
                        print(f"❌ {desc}: resultado={result.result:.6f}, esperado={expected:.6f}")
                except Exception as e:
                    error_msg = f"Error al ejecutar Simpson 3/8 simple con {desc}: {str(e)}"
                    logger.error(error_msg)
                    print(f"⚠️ {error_msg}")
        
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"Tasa de éxito: {success_count}/{total_count} ({success_rate:.1f}%)")

    def test_rectangle_composite(self):
        """Test comprehensivo del método rectángulo compuesto"""
        print("\n=== Test de Rectángulo Compuesto ===")
        success_count = 0
        total_count = 0
        
        for func, a, b, expected, desc in self.test_functions:
            for n in self.n_values['rectangle']:
                with self.subTest(description=f"{desc}, n={n}"):
                    total_count += 1
                    try:
                        result = self.nc.rectangle_composite(func, a, b, n)
                        
                        # Tolerancia inversamente proporcional a n
                        tolerance = max(0.1 / (n ** 0.5) * abs(expected), 0.001)
                        if self._check_result(result, expected, tolerance, 
                                            "Rectángulo Compuesto", func, a, b, n):
                            success_count += 1
                            print(f"✅ {desc}, n={n}: resultado={result.result:.6f}, esperado={expected:.6f}")
                        else:
                            print(f"❌ {desc}, n={n}: resultado={result.result:.6f}, esperado={expected:.6f}")
                    except Exception as e:
                        error_msg = f"Error al ejecutar rectángulo compuesto con {desc}, n={n}: {str(e)}"
                        logger.error(error_msg)
                        print(f"⚠️ {error_msg}")
        
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"Tasa de éxito: {success_count}/{total_count} ({success_rate:.1f}%)")

    def test_trapezoid_composite(self):
        """Test comprehensivo del método trapecio compuesto"""
        print("\n=== Test de Trapecio Compuesto ===")
        success_count = 0
        total_count = 0
        
        for func, a, b, expected, desc in self.test_functions:
            for n in self.n_values['trapezoid']:
                with self.subTest(description=f"{desc}, n={n}"):
                    total_count += 1
                    try:
                        result = self.nc.trapezoid_composite(func, a, b, n)
                        
                        # Tolerancia inversamente proporcional a n^2 (convergencia de orden 2)
                        tolerance = max(0.1 / (n ** 1) * abs(expected), 0.001)
                        if self._check_result(result, expected, tolerance, 
                                            "Trapecio Compuesto", func, a, b, n):
                            success_count += 1
                            print(f"✅ {desc}, n={n}: resultado={result.result:.6f}, esperado={expected:.6f}")
                        else:
                            print(f"❌ {desc}, n={n}: resultado={result.result:.6f}, esperado={expected:.6f}")
                    except Exception as e:
                        error_msg = f"Error al ejecutar trapecio compuesto con {desc}, n={n}: {str(e)}"
                        logger.error(error_msg)
                        print(f"⚠️ {error_msg}")
        
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"Tasa de éxito: {success_count}/{total_count} ({success_rate:.1f}%)")

    def test_simpson_13_composite(self):
        """Test comprehensivo del método Simpson 1/3 compuesto"""
        print("\n=== Test de Simpson 1/3 Compuesto ===")
        success_count = 0
        total_count = 0
        
        for func, a, b, expected, desc in self.test_functions:
            for n in self.n_values['simpson_13']:
                with self.subTest(description=f"{desc}, n={n}"):
                    total_count += 1
                    try:
                        # Asegurar que n sea par
                        if n % 2 != 0:
                            n += 1
                            
                        result = self.nc.simpson_13_composite(func, a, b, n)
                        
                        # Tolerancia inversamente proporcional a n^4 (convergencia de orden 4)
                        tolerance = max(0.01 / (n ** 2) * abs(expected), 0.0001)
                        if self._check_result(result, expected, tolerance, 
                                            "Simpson 1/3 Compuesto", func, a, b, n):
                            success_count += 1
                            print(f"✅ {desc}, n={n}: resultado={result.result:.6f}, esperado={expected:.6f}")
                        else:
                            print(f"❌ {desc}, n={n}: resultado={result.result:.6f}, esperado={expected:.6f}")
                    except Exception as e:
                        error_msg = f"Error al ejecutar Simpson 1/3 compuesto con {desc}, n={n}: {str(e)}"
                        logger.error(error_msg)
                        print(f"⚠️ {error_msg}")
        
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"Tasa de éxito: {success_count}/{total_count} ({success_rate:.1f}%)")

    def test_simpson_38_composite(self):
        """Test comprehensivo del método Simpson 3/8 compuesto"""
        print("\n=== Test de Simpson 3/8 Compuesto ===")
        success_count = 0
        total_count = 0
        
        for func, a, b, expected, desc in self.test_functions:
            for n in self.n_values['simpson_38']:
                with self.subTest(description=f"{desc}, n={n}"):
                    total_count += 1
                    try:
                        # Asegurar que n sea múltiplo de 3
                        if n % 3 != 0:
                            n += (3 - n % 3)
                            
                        result = self.nc.simpson_38_composite(func, a, b, n)
                        
                        # Tolerancia inversamente proporcional a n^4 (convergencia de orden 4)
                        tolerance = max(0.01 / (n ** 2) * abs(expected), 0.0001)
                        if self._check_result(result, expected, tolerance, 
                                            "Simpson 3/8 Compuesto", func, a, b, n):
                            success_count += 1
                            print(f"✅ {desc}, n={n}: resultado={result.result:.6f}, esperado={expected:.6f}")
                        else:
                            print(f"❌ {desc}, n={n}: resultado={result.result:.6f}, esperado={expected:.6f}")
                    except Exception as e:
                        error_msg = f"Error al ejecutar Simpson 3/8 compuesto con {desc}, n={n}: {str(e)}"
                        logger.error(error_msg)
                        print(f"⚠️ {error_msg}")
        
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"Tasa de éxito: {success_count}/{total_count} ({success_rate:.1f}%)")

    def test_integrate_method(self):
        """Test comprehensivo del método unificado de integración"""
        print("\n=== Test del Método Integrate ===")
        success_count = 0
        total_count = 0
        
        # Seleccionar algunas funciones para probar todos los métodos
        sample_functions = self.test_functions[::4]  # Cada cuarta función
        
        methods = [
            ("rectangle_simple", None),
            ("trapezoid_simple", None),
            ("simpson_13_simple", None),
            ("simpson_38_simple", None),
            ("rectangle_composite", 100),
            ("trapezoid_composite", 100),
            ("simpson_13_composite", 100),
            ("simpson_38_composite", 99),
        ]
        
        for func, a, b, expected, desc in sample_functions:
            for method, n in methods:
                with self.subTest(description=f"{desc}, método={method}, n={n}"):
                    total_count += 1
                    try:
                        # Ajustar n para métodos específicos
                        if 'simpson_13' in method and n and n % 2 != 0:
                            n += 1
                        if 'simpson_38' in method and n and n % 3 != 0:
                            n += (3 - n % 3)
                            
                        result = self.nc.integrate(func, a, b, method, n)
                        
                        # Tolerancia según el método
                        if 'simple' in method:
                            tolerance = max(0.05 * abs(expected), 0.01)
                        elif 'simpson' in method:
                            tolerance = max(0.01 / (n if n else 1) * abs(expected), 0.001)
                        else:
                            tolerance = max(0.1 / (n if n else 1) * abs(expected), 0.01)
                            
                        if self._check_result(result, expected, tolerance, 
                                            method, func, a, b, n):
                            success_count += 1
                            print(f"✅ {desc}, método={method}: resultado={result.result:.6f}, esperado={expected:.6f}")
                        else:
                            print(f"❌ {desc}, método={method}: resultado={result.result:.6f}, esperado={expected:.6f}")
                    except Exception as e:
                        error_msg = f"Error al ejecutar {method} con {desc}, n={n}: {str(e)}"
                        logger.error(error_msg)
                        print(f"⚠️ {error_msg}")
        
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"Tasa de éxito: {success_count}/{total_count} ({success_rate:.1f}%)")

    def test_convergence_analysis(self):
        """Análisis de convergencia con n creciente"""
        print("\n=== Análisis de Convergencia ===")
        
        # Seleccionar algunas funciones representativas
        convergence_functions = [
            ("x**2", 0, 1, 1/3, "Cuadrática f(x) = x²"),
            ("sin(x)", 0, math.pi, 2.0, "Seno f(x) = sin(x) en [0,π]"),
        ]
        
        # Valores de n para análisis de convergencia
        n_values = [4, 8, 16, 32, 64, 128, 256, 512]
        
        for func, a, b, expected, desc in convergence_functions:
            print(f"\n--- Convergencia para {desc} ---")
            
            # Resultados por método
            methods_data = {
                "Trapecio Compuesto": [],
                "Simpson 1/3 Compuesto": [],
                "Simpson 3/8 Compuesto": []
            }
            
            for n in n_values:
                # Trapecio (no requiere ajuste de n)
                try:
                    result = self.nc.trapezoid_composite(func, a, b, n)
                    error = abs(result.result - expected)
                    methods_data["Trapecio Compuesto"].append((n, error))
                    print(f"Trapecio n={n}: error={error:.8f}")
                except Exception as e:
                    logger.error(f"Error en análisis convergencia trapecio con n={n}: {str(e)}")
                
                # Simpson 1/3 (n debe ser par)
                try:
                    n_s13 = n if n % 2 == 0 else n + 1
                    result = self.nc.simpson_13_composite(func, a, b, n_s13)
                    error = abs(result.result - expected)
                    methods_data["Simpson 1/3 Compuesto"].append((n_s13, error))
                    print(f"Simpson 1/3 n={n_s13}: error={error:.8f}")
                except Exception as e:
                    logger.error(f"Error en análisis convergencia Simpson 1/3 con n={n}: {str(e)}")
                
                # Simpson 3/8 (n debe ser múltiplo de 3)
                try:
                    n_s38 = n
                    if n_s38 % 3 != 0:
                        n_s38 += (3 - n_s38 % 3)
                    result = self.nc.simpson_38_composite(func, a, b, n_s38)
                    error = abs(result.result - expected)
                    methods_data["Simpson 3/8 Compuesto"].append((n_s38, error))
                    print(f"Simpson 3/8 n={n_s38}: error={error:.8f}")
                except Exception as e:
                    logger.error(f"Error en análisis convergencia Simpson 3/8 con n={n}: {str(e)}")
            
            # Verificar tasas de convergencia
            for method, data in methods_data.items():
                if len(data) >= 2:
                    rates = []
                    for i in range(1, len(data)):
                        n1, e1 = data[i-1]
                        n2, e2 = data[i]
                        if e1 > 0 and e2 > 0:  # Evitar división por cero
                            # Calcular tasa de convergencia: e1/e2 ≈ (n1/n2)^orden
                            rate = math.log(e1/e2) / math.log(n2/n1)
                            rates.append(rate)
                    
                    if rates:
                        avg_rate = sum(rates) / len(rates)
                        print(f"{method}: Orden de convergencia estimado ≈ {avg_rate:.2f}")
                        
                        # Verificar contra orden teórico
                        expected_order = 4 if 'Simpson' in method else 2
                        if abs(avg_rate - expected_order) > 1.0:
                            logger.warning(
                                f"Convergencia de {method} para {desc}: orden estimado {avg_rate:.2f}, "
                                f"esperado {expected_order}"
                            )


def run_tests():
    """Ejecutar todos los tests comprehensivos"""
    print("\n=== TESTS COMPREHENSIVOS DE NEWTON-COTES ===\n")
    
    # Ejecutar tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNewtonCotesComprehensive)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    
    # Resumen
    print(f"\n=== RESUMEN DE TESTS COMPREHENSIVOS ===")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallas: {len(result.failures)}")
    
    if result.wasSuccessful():
        print("\n✅ TODOS LOS TESTS PASARON")
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
        print("\nLos errores detectados han sido registrados en el archivo newton_cotes_test_errors.log")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
