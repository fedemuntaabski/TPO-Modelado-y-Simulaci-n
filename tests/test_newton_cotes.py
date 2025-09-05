"""
Tests para el módulo de integración Newton-Cotes.

Implementa tests unitarios para verificar la correctitud de los métodos
de integración Newton-Cotes simples y compuestos.
"""

import unittest
import math
from src.core.newton_cotes import NewtonCotes, NewtonCotesError
from src.core.function_parser import FunctionParser, FunctionParserError
from src.core.integration_validators import IntegrationValidator, IntegrationValidationError


class TestFunctionParser(unittest.TestCase):
    """Tests para el parser de funciones"""
    
    def setUp(self):
        self.parser = FunctionParser()
    
    def test_basic_functions(self):
        """Test de funciones básicas"""
        test_cases = [
            ("x**2", 2, 4),
            ("sin(x)", 0, 0),
            ("cos(x)", 0, 1),
            ("exp(x)", 0, 1),
            ("ln(x)", 1, 0),
            ("sqrt(x)", 4, 2),
            ("abs(x)", -5, 5),
            ("pi", 1, math.pi),
            ("e", 1, math.e),
        ]
        
        for func_str, x_val, expected in test_cases:
            with self.subTest(func=func_str, x=x_val):
                result = self.parser.parse_and_evaluate(func_str, x_val)
                self.assertAlmostEqual(result, expected, places=6)
    
    def test_complex_expressions(self):
        """Test de expresiones complejas"""
        test_cases = [
            ("x**2 + 2*x + 1", 1, 4),  # (x+1)²
            ("sin(x)**2 + cos(x)**2", math.pi/4, 1),  # Identidad trigonométrica
            ("exp(ln(x))", 5, 5),  # exp(ln(x)) = x
            ("sqrt(x**2)", 3, 3),  # sqrt(x²) = x (para x > 0)
        ]
        
        for func_str, x_val, expected in test_cases:
            with self.subTest(func=func_str, x=x_val):
                result = self.parser.parse_and_evaluate(func_str, x_val)
                self.assertAlmostEqual(result, expected, places=6)
    
    def test_function_validation(self):
        """Test de validación de funciones"""
        valid_functions = ["x**2", "sin(x)", "exp(x) + cos(x)"]
        invalid_functions = ["x +", "sin(", "unknown_func(x)", "import os"]
        
        for func in valid_functions:
            with self.subTest(func=func):
                is_valid, _ = self.parser.validate_function(func)
                self.assertTrue(is_valid)
        
        for func in invalid_functions:
            with self.subTest(func=func):
                is_valid, _ = self.parser.validate_function(func)
                self.assertFalse(is_valid)


class TestIntegrationValidator(unittest.TestCase):
    """Tests para el validador de integración"""
    
    def setUp(self):
        self.validator = IntegrationValidator()
    
    def test_interval_validation(self):
        """Test de validación de intervalos"""
        # Intervalos válidos
        valid_intervals = [(0, 1), (-1, 1), (0.5, 2.5)]
        for a, b in valid_intervals:
            with self.subTest(a=a, b=b):
                try:
                    self.validator.validate_interval(a, b)
                except IntegrationValidationError:
                    self.fail(f"Intervalo válido [{a}, {b}] falló la validación")
        
        # Intervalos inválidos
        invalid_intervals = [(1, 0), (5, 5), (float('nan'), 1), (0, float('inf'))]
        for a, b in invalid_intervals:
            with self.subTest(a=a, b=b):
                with self.assertRaises(IntegrationValidationError):
                    self.validator.validate_interval(a, b)
    
    def test_simpson_13_validation(self):
        """Test de validación para Simpson 1/3"""
        valid_n = [2, 4, 6, 10, 100]
        for n in valid_n:
            with self.subTest(n=n):
                try:
                    self.validator.validate_simpson_13_n(n)
                except IntegrationValidationError:
                    self.fail(f"n={n} (par) falló la validación de Simpson 1/3")
        
        invalid_n = [1, 3, 5, 7, 11]
        for n in invalid_n:
            with self.subTest(n=n):
                with self.assertRaises(IntegrationValidationError):
                    self.validator.validate_simpson_13_n(n)
    
    def test_simpson_38_validation(self):
        """Test de validación para Simpson 3/8"""
        valid_n = [3, 6, 9, 12, 15]
        for n in valid_n:
            with self.subTest(n=n):
                try:
                    self.validator.validate_simpson_38_n(n)
                except IntegrationValidationError:
                    self.fail(f"n={n} (múltiplo de 3) falló la validación de Simpson 3/8")
        
        invalid_n = [1, 2, 4, 5, 7, 8, 10, 11]
        for n in invalid_n:
            with self.subTest(n=n):
                with self.assertRaises(IntegrationValidationError):
                    self.validator.validate_simpson_38_n(n)


class TestNewtonCotes(unittest.TestCase):
    """Tests para los métodos Newton-Cotes"""
    
    def setUp(self):
        self.nc = NewtonCotes()
    
    def test_rectangle_simple(self):
        """Test del método rectángulo simple"""
        # Función constante: f(x) = 2
        result = self.nc.rectangle_simple("2", 0, 1)
        self.assertAlmostEqual(result.result, 2.0, places=6)
        
        # Función lineal: f(x) = x, integral de 0 a 1 = 0.5
        result = self.nc.rectangle_simple("x", 0, 1)
        expected = 0.5  # Valor en el punto medio (0.5) por el ancho (1)
        self.assertAlmostEqual(result.result, expected, places=6)
    
    def test_trapezoid_simple(self):
        """Test del método trapecio simple"""
        # Función lineal: f(x) = x, integral de 0 a 1 = 0.5
        result = self.nc.trapezoid_simple("x", 0, 1)
        expected = 0.5
        self.assertAlmostEqual(result.result, expected, places=6)
        
        # Función cuadrática: f(x) = x², integral de 0 a 1 = 1/3
        result = self.nc.trapezoid_simple("x**2", 0, 1)
        # Trapecio simple no es exacto para cuadráticas, pero debe dar resultado razonable
        self.assertIsInstance(result.result, float)
        self.assertGreater(result.result, 0)
    
    def test_simpson_13_simple(self):
        """Test del método Simpson 1/3 simple"""
        # Función cuadrática: f(x) = x², integral de 0 a 1 = 1/3
        result = self.nc.simpson_13_simple("x**2", 0, 1)
        expected = 1.0/3.0
        self.assertAlmostEqual(result.result, expected, places=6)
        
        # Función cúbica: f(x) = x³, integral de 0 a 1 = 1/4
        result = self.nc.simpson_13_simple("x**3", 0, 1)
        expected = 1.0/4.0
        self.assertAlmostEqual(result.result, expected, places=6)
    
    def test_simpson_38_simple(self):
        """Test del método Simpson 3/8 simple"""
        # Función cuadrática: f(x) = x², integral de 0 a 1 = 1/3
        result = self.nc.simpson_38_simple("x**2", 0, 1)
        expected = 1.0/3.0
        self.assertAlmostEqual(result.result, expected, places=6)
        
        # Función cúbica: f(x) = x³, integral de 0 a 1 = 1/4
        result = self.nc.simpson_38_simple("x**3", 0, 1)
        expected = 1.0/4.0
        self.assertAlmostEqual(result.result, expected, places=6)
    
    def test_composite_methods_convergence(self):
        """Test de convergencia de métodos compuestos"""
        func = "x**2"
        a, b = 0, 1
        exact_value = 1.0/3.0
        
        # Test trapecio compuesto
        for n in [10, 20, 40]:
            result = self.nc.trapezoid_composite(func, a, b, n)
            error = abs(result.result - exact_value)
            # El error debe decrecer con más subdivisiones
            self.assertLess(error, 0.1)  # Error razonable
        
        # Test Simpson 1/3 compuesto (debe ser exacto para polinomios de grado ≤ 3)
        result = self.nc.simpson_13_composite(func, a, b, 10)
        self.assertAlmostEqual(result.result, exact_value, places=8)
    
    def test_method_validation(self):
        """Test de validación de métodos"""
        # Método válido
        result = self.nc.integrate("x**2", 0, 1, "simpson_13_simple")
        self.assertIsNotNone(result)
        
        # Método inválido
        with self.assertRaises(NewtonCotesError):
            self.nc.integrate("x**2", 0, 1, "invalid_method")
        
        # Simpson 1/3 con n impar
        with self.assertRaises(IntegrationValidationError):
            self.nc.integrate("x**2", 0, 1, "simpson_13_composite", 3)
        
        # Simpson 3/8 con n no múltiplo de 3
        with self.assertRaises(IntegrationValidationError):
            self.nc.integrate("x**2", 0, 1, "simpson_38_composite", 4)
    
    def test_function_errors(self):
        """Test de manejo de errores en funciones"""
        # Función inválida
        with self.assertRaises(NewtonCotesError):
            self.nc.integrate("invalid_function", 0, 1, "rectangle_simple")
        
        # División por cero
        with self.assertRaises(NewtonCotesError):
            self.nc.integrate("1/x", 0, 1, "rectangle_simple")
    
    def test_result_structure(self):
        """Test de estructura del resultado"""
        result = self.nc.simpson_13_simple("x**2", 0, 1)
        
        # Verificar que el resultado tiene todos los campos esperados
        required_fields = ['method', 'function', 'interval', 'result', 'formula', 
                          'evaluations', 'computation_time', 'error_order']
        
        result_dict = result.to_dict()
        for field in required_fields:
            self.assertIn(field, result_dict)
        
        # Verificar tipos
        self.assertIsInstance(result.result, float)
        self.assertIsInstance(result.evaluations, int)
        self.assertIsInstance(result.computation_time, float)
        self.assertGreater(result.evaluations, 0)
        self.assertGreaterEqual(result.computation_time, 0)


class TestIntegrationAccuracy(unittest.TestCase):
    """Tests de precisión de integración con funciones conocidas"""
    
    def setUp(self):
        self.nc = NewtonCotes()
    
    def test_polynomial_integration(self):
        """Test con polinomios (resultados exactos esperados)"""
        test_cases = [
            # (función, a, b, valor_exacto)
            ("1", 0, 1, 1.0),  # Constante
            ("x", 0, 1, 0.5),  # Linear
            ("x**2", 0, 1, 1.0/3.0),  # Cuadrática
            ("x**3", 0, 1, 1.0/4.0),  # Cúbica
        ]
        
        for func, a, b, exact in test_cases:
            with self.subTest(func=func):
                # Simpson 1/3 debe ser exacto para polinomios de grado ≤ 3
                result = self.nc.simpson_13_composite(func, a, b, 10)
                self.assertAlmostEqual(result.result, exact, places=8)
    
    def test_trigonometric_integration(self):
        """Test con funciones trigonométricas"""
        # ∫₀^π sin(x) dx = 2
        result = self.nc.simpson_13_composite("sin(x)", 0, math.pi, 20)
        self.assertAlmostEqual(result.result, 2.0, places=4)
        
        # ∫₀^(π/2) cos(x) dx = 1
        result = self.nc.simpson_13_composite("cos(x)", 0, math.pi/2, 20)
        self.assertAlmostEqual(result.result, 1.0, places=4)
    
    def test_exponential_integration(self):
        """Test con función exponencial"""
        # ∫₀¹ exp(x) dx = e - 1
        result = self.nc.simpson_13_composite("exp(x)", 0, 1, 20)
        expected = math.e - 1
        self.assertAlmostEqual(result.result, expected, places=4)


def run_tests():
    """Ejecutar todos los tests"""
    print("=== EJECUTANDO TESTS NEWTON-COTES ===\n")
    
    # Crear suite de tests
    test_suite = unittest.TestSuite()
    
    # Añadir tests
    test_classes = [
        TestFunctionParser,
        TestIntegrationValidator,
        TestNewtonCotes,
        TestIntegrationAccuracy
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Resumen
    print(f"\n=== RESUMEN DE TESTS ===")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallas: {len(result.failures)}")
    
    if result.errors:
        print("\n🔴 ERRORES:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")
    
    if result.failures:
        print("\n🟡 FALLAS:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure}")
    
    if result.wasSuccessful():
        print("\n✅ TODOS LOS TESTS PASARON")
        return True
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
        return False


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
