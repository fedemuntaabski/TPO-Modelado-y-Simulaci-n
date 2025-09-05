"""
Implementación completa de métodos de integración Newton-Cotes.

Incluye reglas simples y compuestas para:
- Rectángulo (punto medio)
- Trapecio
- Simpson 1/3
- Simpson 3/8

Cada método incluye validaciones, optimizaciones de rendimiento y 
información detallada de resultados.
"""

import math
import time
from typing import Dict, Any, Optional, List, Tuple
import logging

from src.core.function_parser import FunctionParser, FunctionParserError
from src.core.integration_validators import IntegrationValidator, IntegrationValidationError

logger = logging.getLogger(__name__)


class NewtonCotesError(Exception):
    """Excepción para errores específicos de Newton-Cotes"""
    pass


class NewtonCotesResult:
    """Resultado de integración Newton-Cotes con información completa"""
    
    def __init__(self, method: str, function: str, interval: List[float],
                 result: float, **kwargs):
        self.method = method
        self.function = function
        self.interval = interval
        self.result = result
        
        # Información adicional
        self.n_subdivisions = kwargs.get('n_subdivisions')
        self.h = kwargs.get('h')
        self.formula = kwargs.get('formula', '')
        self.evaluations = kwargs.get('evaluations', 0)
        self.computation_time = kwargs.get('computation_time', 0.0)
        self.error_order = kwargs.get('error_order', '')
        self.accuracy_estimate = kwargs.get('accuracy_estimate', '')
        self.sample_points = kwargs.get('sample_points', [])
        
    def to_dict(self) -> Dict[str, Any]:
        """Convertir resultado a diccionario"""
        return {
            'method': self.method,
            'function': self.function,
            'interval': self.interval,
            'result': self.result,
            'n_subdivisions': self.n_subdivisions,
            'h': self.h,
            'formula': self.formula,
            'evaluations': self.evaluations,
            'computation_time': self.computation_time,
            'error_order': self.error_order,
            'accuracy_estimate': self.accuracy_estimate,
            'sample_points': self.sample_points[:10]  # Limitar para no sobrecargar
        }
    
    def __str__(self) -> str:
        """Representación string del resultado"""
        return (f"Newton-Cotes Result:\n"
                f"  Method: {self.method}\n"
                f"  Function: {self.function}\n"
                f"  Interval: [{self.interval[0]}, {self.interval[1]}]\n"
                f"  Result: {self.result:.8f}\n"
                f"  Time: {self.computation_time:.4f}s")


class NewtonCotes:
    """
    Implementación completa de métodos de integración Newton-Cotes
    
    Incluye métodos simples y compuestos con validaciones completas
    y optimizaciones de rendimiento.
    """
    
    def __init__(self):
        self.parser = FunctionParser()
        self.validator = IntegrationValidator()
        
        # Métodos disponibles
        self.METHODS = {
            'rectangle_simple': 'Rectángulo Simple',
            'rectangle_composite': 'Rectángulo Compuesto',
            'trapezoid_simple': 'Trapecio Simple', 
            'trapezoid_composite': 'Trapecio Compuesto',
            'simpson_13_simple': 'Simpson 1/3 Simple',
            'simpson_13_composite': 'Simpson 1/3 Compuesto',
            'simpson_38_simple': 'Simpson 3/8 Simple',
            'simpson_38_composite': 'Simpson 3/8 Compuesto'
        }
    
    def rectangle_simple(self, func_str: str, a: float, b: float) -> NewtonCotesResult:
        """
        Regla del rectángulo simple (punto medio)
        I ≈ (b-a) * f((a+b)/2)
        """
        start_time = time.time()
        
        # Validaciones
        self._validate_basic_parameters(func_str, a, b, 'rectangle_simple')
        
        try:
            # Punto medio
            midpoint = (a + b) / 2
            f_mid = self.parser.parse_and_evaluate(func_str, midpoint)
            
            # Aplicar fórmula
            result = (b - a) * f_mid
            
            computation_time = time.time() - start_time
            
            return NewtonCotesResult(
                method='Rectángulo Simple',
                function=func_str,
                interval=[a, b],
                result=result,
                h=b - a,
                formula='I ≈ (b-a) * f((a+b)/2)',
                evaluations=1,
                computation_time=computation_time,
                error_order='O(h³)',
                accuracy_estimate='Moderada (método de orden 2)',
                sample_points=[{'x': midpoint, 'f(x)': f_mid}]
            )
            
        except Exception as e:
            raise NewtonCotesError(f"Error en rectángulo simple: {e}")
    
    def rectangle_composite(self, func_str: str, a: float, b: float, n: int) -> NewtonCotesResult:
        """
        Regla del rectángulo compuesta (punto medio)
        I ≈ h * Σf(xi) donde h = (b-a)/n, xi = a + (i-0.5)*h
        """
        start_time = time.time()
        
        # Validaciones
        self._validate_composite_parameters(func_str, a, b, 'rectangle_composite', n)
        
        try:
            h = (b - a) / n
            total_sum = 0.0
            sample_points = []
            
            # Sumar evaluaciones en puntos medios
            for i in range(n):
                xi = a + (i + 0.5) * h  # Punto medio del subintervalo
                fi = self.parser.parse_and_evaluate(func_str, xi)
                total_sum += fi
                
                # Guardar algunos puntos para mostrar
                if len(sample_points) < 5:
                    sample_points.append({'x': xi, 'f(x)': fi})
            
            result = h * total_sum
            computation_time = time.time() - start_time
            
            return NewtonCotesResult(
                method='Rectángulo Compuesto',
                function=func_str,
                interval=[a, b],
                result=result,
                n_subdivisions=n,
                h=h,
                formula='I ≈ h * Σf(xi) donde xi son puntos medios',
                evaluations=n,
                computation_time=computation_time,
                error_order='O(h²)',
                accuracy_estimate='Moderada (método de orden 2)',
                sample_points=sample_points
            )
            
        except Exception as e:
            raise NewtonCotesError(f"Error en rectángulo compuesto: {e}")
    
    def trapezoid_simple(self, func_str: str, a: float, b: float) -> NewtonCotesResult:
        """
        Regla del trapecio simple
        I ≈ (b-a)/2 * [f(a) + f(b)]
        """
        start_time = time.time()
        
        # Validaciones
        self._validate_basic_parameters(func_str, a, b, 'trapezoid_simple')
        
        try:
            # Evaluar en extremos
            fa = self.parser.parse_and_evaluate(func_str, a)
            fb = self.parser.parse_and_evaluate(func_str, b)
            
            # Aplicar fórmula del trapecio
            result = (b - a) / 2 * (fa + fb)
            
            computation_time = time.time() - start_time
            
            return NewtonCotesResult(
                method='Trapecio Simple',
                function=func_str,
                interval=[a, b],
                result=result,
                h=b - a,
                formula='I ≈ (b-a)/2 * [f(a) + f(b)]',
                evaluations=2,
                computation_time=computation_time,
                error_order='O(h³)',
                accuracy_estimate='Buena (método de orden 2)',
                sample_points=[
                    {'x': a, 'f(x)': fa},
                    {'x': b, 'f(x)': fb}
                ]
            )
            
        except Exception as e:
            raise NewtonCotesError(f"Error en trapecio simple: {e}")
    
    def trapezoid_composite(self, func_str: str, a: float, b: float, n: int) -> NewtonCotesResult:
        """
        Regla del trapecio compuesta
        I ≈ h/2 * [f(a) + 2*Σf(xi) + f(b)] donde h = (b-a)/n
        """
        start_time = time.time()
        
        # Validaciones
        self._validate_composite_parameters(func_str, a, b, 'trapezoid_composite', n)
        
        try:
            h = (b - a) / n
            
            # Evaluar en extremos
            fa = self.parser.parse_and_evaluate(func_str, a)
            fb = self.parser.parse_and_evaluate(func_str, b)
            
            # Sumar evaluaciones intermedias
            sum_intermediate = 0.0
            sample_points = [{'x': a, 'f(x)': fa}]
            
            for i in range(1, n):
                xi = a + i * h
                fi = self.parser.parse_and_evaluate(func_str, xi)
                sum_intermediate += fi
                
                # Guardar algunos puntos para mostrar
                if len(sample_points) < 4:
                    sample_points.append({'x': xi, 'f(x)': fi})
            
            sample_points.append({'x': b, 'f(x)': fb})
            
            # Aplicar fórmula del trapecio
            result = (h / 2) * (fa + 2 * sum_intermediate + fb)
            
            computation_time = time.time() - start_time
            
            return NewtonCotesResult(
                method='Trapecio Compuesto',
                function=func_str,
                interval=[a, b],
                result=result,
                n_subdivisions=n,
                h=h,
                formula='I ≈ h/2 * [f(a) + 2*Σf(xi) + f(b)]',
                evaluations=n + 1,
                computation_time=computation_time,
                error_order='O(h²)',
                accuracy_estimate='Buena (método de orden 2)',
                sample_points=sample_points
            )
            
        except Exception as e:
            raise NewtonCotesError(f"Error en trapecio compuesto: {e}")
    
    def simpson_13_simple(self, func_str: str, a: float, b: float) -> NewtonCotesResult:
        """
        Regla de Simpson 1/3 simple
        I ≈ (b-a)/6 * [f(a) + 4*f((a+b)/2) + f(b)]
        """
        start_time = time.time()
        
        # Validaciones
        self._validate_basic_parameters(func_str, a, b, 'simpson_13_simple')
        
        try:
            # Puntos de evaluación
            midpoint = (a + b) / 2
            
            fa = self.parser.parse_and_evaluate(func_str, a)
            fm = self.parser.parse_and_evaluate(func_str, midpoint)
            fb = self.parser.parse_and_evaluate(func_str, b)
            
            # Aplicar fórmula de Simpson 1/3
            result = (b - a) / 6 * (fa + 4 * fm + fb)
            
            computation_time = time.time() - start_time
            
            return NewtonCotesResult(
                method='Simpson 1/3 Simple',
                function=func_str,
                interval=[a, b],
                result=result,
                h=(b - a) / 2,
                formula='I ≈ (b-a)/6 * [f(a) + 4*f((a+b)/2) + f(b)]',
                evaluations=3,
                computation_time=computation_time,
                error_order='O(h⁵)',
                accuracy_estimate='Muy buena (método de orden 4)',
                sample_points=[
                    {'x': a, 'f(x)': fa},
                    {'x': midpoint, 'f(x)': fm},
                    {'x': b, 'f(x)': fb}
                ]
            )
            
        except Exception as e:
            raise NewtonCotesError(f"Error en Simpson 1/3 simple: {e}")
    
    def simpson_13_composite(self, func_str: str, a: float, b: float, n: int) -> NewtonCotesResult:
        """
        Regla de Simpson 1/3 compuesta
        I ≈ h/3 * [f(a) + 4*Σf(x_impar) + 2*Σf(x_par) + f(b)]
        Requiere n par
        """
        start_time = time.time()
        
        # Validaciones específicas
        self._validate_composite_parameters(func_str, a, b, 'simpson_13_composite', n)
        self.validator.validate_simpson_13_n(n)
        
        try:
            h = (b - a) / n
            
            # Evaluar en extremos
            fa = self.parser.parse_and_evaluate(func_str, a)
            fb = self.parser.parse_and_evaluate(func_str, b)
            
            # Sumar puntos impares (coeficiente 4)
            sum_odd = 0.0
            # Sumar puntos pares (coeficiente 2)
            sum_even = 0.0
            
            sample_points = [{'x': a, 'f(x)': fa}]
            
            for i in range(1, n):
                xi = a + i * h
                fi = self.parser.parse_and_evaluate(func_str, xi)
                
                if i % 2 == 1:  # Índice impar
                    sum_odd += fi
                else:  # Índice par
                    sum_even += fi
                
                # Guardar algunos puntos para mostrar
                if len(sample_points) < 4:
                    sample_points.append({'x': xi, 'f(x)': fi})
            
            sample_points.append({'x': b, 'f(x)': fb})
            
            # Aplicar fórmula de Simpson 1/3 compuesta
            result = (h / 3) * (fa + 4 * sum_odd + 2 * sum_even + fb)
            
            computation_time = time.time() - start_time
            
            return NewtonCotesResult(
                method='Simpson 1/3 Compuesto',
                function=func_str,
                interval=[a, b],
                result=result,
                n_subdivisions=n,
                h=h,
                formula='I ≈ h/3 * [f(a) + 4*Σf(x_impar) + 2*Σf(x_par) + f(b)]',
                evaluations=n + 1,
                computation_time=computation_time,
                error_order='O(h⁴)',
                accuracy_estimate='Excelente (método de orden 4)',
                sample_points=sample_points
            )
            
        except Exception as e:
            raise NewtonCotesError(f"Error en Simpson 1/3 compuesto: {e}")
    
    def simpson_38_simple(self, func_str: str, a: float, b: float) -> NewtonCotesResult:
        """
        Regla de Simpson 3/8 simple
        I ≈ 3*(b-a)/8 * [f(a) + 3*f(a+h) + 3*f(a+2h) + f(b)]
        donde h = (b-a)/3
        """
        start_time = time.time()
        
        # Validaciones
        self._validate_basic_parameters(func_str, a, b, 'simpson_38_simple')
        
        try:
            h = (b - a) / 3
            
            # Puntos de evaluación
            x1 = a + h
            x2 = a + 2 * h
            
            fa = self.parser.parse_and_evaluate(func_str, a)
            f1 = self.parser.parse_and_evaluate(func_str, x1)
            f2 = self.parser.parse_and_evaluate(func_str, x2)
            fb = self.parser.parse_and_evaluate(func_str, b)
            
            # Aplicar fórmula de Simpson 3/8
            result = 3 * h / 8 * (fa + 3 * f1 + 3 * f2 + fb)
            
            computation_time = time.time() - start_time
            
            return NewtonCotesResult(
                method='Simpson 3/8 Simple',
                function=func_str,
                interval=[a, b],
                result=result,
                h=h,
                formula='I ≈ 3*(b-a)/8 * [f(a) + 3*f(a+h) + 3*f(a+2h) + f(b)]',
                evaluations=4,
                computation_time=computation_time,
                error_order='O(h⁵)',
                accuracy_estimate='Muy buena (método de orden 4)',
                sample_points=[
                    {'x': a, 'f(x)': fa},
                    {'x': x1, 'f(x)': f1},
                    {'x': x2, 'f(x)': f2},
                    {'x': b, 'f(x)': fb}
                ]
            )
            
        except Exception as e:
            raise NewtonCotesError(f"Error en Simpson 3/8 simple: {e}")
    
    def simpson_38_composite(self, func_str: str, a: float, b: float, n: int) -> NewtonCotesResult:
        """
        Regla de Simpson 3/8 compuesta
        Requiere n múltiplo de 3
        """
        start_time = time.time()
        
        # Validaciones específicas
        self._validate_composite_parameters(func_str, a, b, 'simpson_38_composite', n)
        self.validator.validate_simpson_38_n(n)
        
        try:
            h = (b - a) / n
            
            # Evaluar en extremos
            fa = self.parser.parse_and_evaluate(func_str, a)
            fb = self.parser.parse_and_evaluate(func_str, b)
            
            # Para Simpson 3/8, los coeficientes son: 1, 3, 3, 2, 3, 3, 2, ..., 3, 3, 1
            total_sum = fa + fb
            sample_points = [{'x': a, 'f(x)': fa}]
            
            for i in range(1, n):
                xi = a + i * h
                fi = self.parser.parse_and_evaluate(func_str, xi)
                
                # Determinar coeficiente según posición
                if i % 3 == 0:  # Múltiplo de 3 (no extremo)
                    coeff = 2
                else:  # No múltiplo de 3
                    coeff = 3
                
                total_sum += coeff * fi
                
                # Guardar algunos puntos para mostrar
                if len(sample_points) < 4:
                    sample_points.append({'x': xi, 'f(x)': fi, 'coeff': coeff})
            
            sample_points.append({'x': b, 'f(x)': fb})
            
            # Aplicar fórmula de Simpson 3/8 compuesta
            result = 3 * h / 8 * total_sum
            
            computation_time = time.time() - start_time
            
            return NewtonCotesResult(
                method='Simpson 3/8 Compuesto',
                function=func_str,
                interval=[a, b],
                result=result,
                n_subdivisions=n,
                h=h,
                formula='I ≈ 3h/8 * [f(a) + 3*Σf(...) + f(b)]',
                evaluations=n + 1,
                computation_time=computation_time,
                error_order='O(h⁴)',
                accuracy_estimate='Excelente (método de orden 4)',
                sample_points=sample_points
            )
            
        except Exception as e:
            raise NewtonCotesError(f"Error en Simpson 3/8 compuesto: {e}")
    
    def integrate(self, func_str: str, a: float, b: float, method: str, 
                  n: Optional[int] = None) -> NewtonCotesResult:
        """
        Método unificado para integración con selector de método
        
        Args:
            func_str: String de la función a integrar
            a: Límite inferior
            b: Límite superior
            method: Nombre del método a usar
            n: Número de subdivisiones (para métodos compuestos)
            
        Returns:
            NewtonCotesResult con el resultado de la integración
        """
        # Validar método
        if method not in self.METHODS:
            available = ', '.join(self.METHODS.keys())
            raise NewtonCotesError(f"Método '{method}' no disponible. Disponibles: {available}")
        
        # Mapear métodos a funciones
        method_map = {
            'rectangle_simple': self.rectangle_simple,
            'rectangle_composite': self.rectangle_composite,
            'trapezoid_simple': self.trapezoid_simple,
            'trapezoid_composite': self.trapezoid_composite,
            'simpson_13_simple': self.simpson_13_simple,
            'simpson_13_composite': self.simpson_13_composite,
            'simpson_38_simple': self.simpson_38_simple,
            'simpson_38_composite': self.simpson_38_composite,
        }
        
        # Ejecutar método correspondiente
        if 'simple' in method:
            return method_map[method](func_str, a, b)
        else:
            if n is None:
                raise NewtonCotesError(f"Método compuesto '{method}' requiere especificar n")
            return method_map[method](func_str, a, b, n)
    
    def display_methods(self) -> None:
        """Mostrar métodos disponibles"""
        print("=== MÉTODOS DE INTEGRACIÓN NEWTON-COTES DISPONIBLES ===")
        for i, (key, name) in enumerate(self.METHODS.items(), 1):
            requirements = self.validator.get_method_requirements(key)
            print(f"{i:2d}. {name}")
            print(f"    Clave: {key}")
            if requirements['requires_n']:
                print(f"    Requiere n: Sí ({requirements['description']})")
            else:
                print(f"    Requiere n: No")
            print(f"    Orden: {requirements['order']}")
            print()
    
    def get_method_info(self, method: str) -> Dict[str, Any]:
        """Obtener información completa de un método"""
        if method not in self.METHODS:
            raise NewtonCotesError(f"Método '{method}' no disponible")
        
        requirements = self.validator.get_method_requirements(method)
        
        return {
            'name': self.METHODS[method],
            'key': method,
            'description': requirements['description'],
            'formula': requirements['formula'],
            'error_order': requirements['order'],
            'requires_n': requirements['requires_n'],
            'n_constraint': requirements['n_constraint'],
            'min_n': requirements['min_n'],
        }
    
    def _validate_basic_parameters(self, func_str: str, a: float, b: float, method: str) -> None:
        """Validaciones básicas para métodos simples"""
        self.validator.validate_function_string(func_str)
        self.validator.validate_interval(a, b)
        
        # Validar función con parser
        is_valid, message = self.parser.validate_function(func_str)
        if not is_valid:
            raise NewtonCotesError(f"Función inválida: {message}")
    
    def _validate_composite_parameters(self, func_str: str, a: float, b: float, 
                                     method: str, n: int) -> None:
        """Validaciones para métodos compuestos"""
        self._validate_basic_parameters(func_str, a, b, method)
        self.validator.validate_subdivisions(n)


# Funciones de utilidad y prueba
def demo_newton_cotes():
    """Demostración completa de Newton-Cotes"""
    nc = NewtonCotes()
    
    print("=== DEMOSTRACIÓN NEWTON-COTES ===")
    
    # Función de prueba
    func = "x**2"
    a, b = 0, 2
    
    print(f"Función: {func}")
    print(f"Intervalo: [{a}, {b}]")
    print(f"Valor exacto: ∫₀² x² dx = 8/3 ≈ {8/3:.8f}")
    print()
    
    # Probar todos los métodos
    methods_to_test = [
        ('rectangle_simple', None),
        ('trapezoid_simple', None),
        ('simpson_13_simple', None),
        ('simpson_38_simple', None),
        ('rectangle_composite', 100),
        ('trapezoid_composite', 100),
        ('simpson_13_composite', 100),
        ('simpson_38_composite', 99),  # Múltiplo de 3
    ]
    
    for method, n in methods_to_test:
        try:
            result = nc.integrate(func, a, b, method, n)
            error = abs(result.result - 8/3)
            print(f"{result.method}:")
            print(f"  Resultado: {result.result:.8f}")
            print(f"  Error: {error:.2e}")
            print(f"  Tiempo: {result.computation_time:.4f}s")
            print(f"  Evaluaciones: {result.evaluations}")
            print()
        except Exception as e:
            print(f"Error en {method}: {e}")
            print()


if __name__ == "__main__":
    demo_newton_cotes()
