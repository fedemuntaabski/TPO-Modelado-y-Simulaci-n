"""
Parser de Funciones Matemáticas
Convierte strings de entrada en funciones evaluables de Python

Características:
- Parser robusto para sintaxis matemática estándar
- Soporte para funciones trigonométricas, exponenciales, logarítmicas
- Validación de sintaxis
- Conversión automática de notación matemática
"""

import numpy as np
import sympy as sp
from typing import Callable, Union
import re

class FunctionParser:
    """
    Clase para parsear y evaluar expresiones matemáticas ingresadas por el usuario
    """
    
    @staticmethod
    def normalize_expression(expression: str) -> str:
        """
        Normaliza una expresión matemática para evaluación en Python
        
        Args:
            expression: Expresión como string
            
        Returns:
            Expresión normalizada
        """
        # Remover espacios y convertir a minúsculas
        expr = expression.strip().lower()
        
        # Reemplazos básicos
        replacements = {
            '^': '**',
            'ln': 'log',
            'log10': 'log10',
            'lg': 'log10',
            'sen': 'sin',
            'cos': 'cos',
            'tan': 'tan',
            'tg': 'tan',
            'sec': '1/cos',
            'csc': '1/sin',
            'cot': '1/tan',
            'arcsin': 'asin',
            'arccos': 'acos',
            'arctan': 'atan',
            'sinh': 'sinh',
            'cosh': 'cosh',
            'tanh': 'tanh',
            'sqrt': 'sqrt',
            'exp': 'exp',
            'abs': 'abs',
            'pi': 'pi',
            'e': 'e'
        }
        
        for old, new in replacements.items():
            expr = expr.replace(old, new)
        
        # Agregar prefijo numpy a funciones matemáticas
        math_functions = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 
                         'sinh', 'cosh', 'tanh', 'exp', 'log', 'log10', 
                         'sqrt', 'abs']
        
        for func in math_functions:
            expr = re.sub(rf'\\b{func}\\b', f'np.{func}', expr)
        
        # Reemplazar constantes
        expr = re.sub(r'\\bpi\\b', 'np.pi', expr)
        expr = re.sub(r'\\be\\b', 'np.e', expr)
        
        return expr
    
    @staticmethod
    def parse_function(expression: str) -> Callable:
        """
        Parsea una función matemática de una variable
        
        Args:
            expression: Expresión como string (ej: "x**2 + sin(x)")
            
        Returns:
            Función evaluable f(x)
        """
        expr = FunctionParser.normalize_expression(expression)
        
        def func(x):
            try:
                # Crear diccionario local con numpy y la variable x
                local_vars = {'x': x, 'np': np}
                return eval(expr, {"__builtins__": {}}, local_vars)
            except Exception as e:
                raise ValueError(f"Error evaluando función: {e}")
        
        return func
    
    @staticmethod
    def parse_ode_function(expression: str) -> Callable:
        """
        Parsea una función para ecuaciones diferenciales dy/dt = f(t, y)
        
        Args:
            expression: Expresión como string (ej: "t + y", "-y + sin(t)")
            
        Returns:
            Función f(t, y)
        """
        expr = FunctionParser.normalize_expression(expression)
        
        def func(t, y):
            try:
                # Crear diccionario local con numpy y las variables t, y
                local_vars = {'t': t, 'y': y, 'np': np}
                return eval(expr, {"__builtins__": {}}, local_vars)
            except Exception as e:
                raise ValueError(f"Error evaluando función ODE: {e}")
        
        return func
    
    @staticmethod
    def parse_parametric_function(x_expr: str, y_expr: str) -> Callable:
        """
        Parsea funciones paramétricas x(t), y(t)
        
        Args:
            x_expr: Expresión para x(t)
            y_expr: Expresión para y(t)
            
        Returns:
            Función que retorna (x(t), y(t))
        """
        x_func = FunctionParser.parse_function(x_expr.replace('x', 't'))
        y_func = FunctionParser.parse_function(y_expr.replace('y', 't'))
        
        def parametric_func(t):
            return x_func(t), y_func(t)
        
        return parametric_func
    
    @staticmethod
    def validate_syntax(expression: str) -> bool:
        """
        Valida si una expresión tiene sintaxis correcta
        
        Args:
            expression: Expresión a validar
            
        Returns:
            True si la sintaxis es válida, False en caso contrario
        """
        try:
            expr = FunctionParser.normalize_expression(expression)
            # Intentar parsear con sympy
            sympy_expr = sp.sympify(expr.replace('np.', ''))
            return True
        except:
            return False
    
    @staticmethod
    def get_derivative(expression: str) -> Callable:
        """
        Calcula la derivada simbólica de una función
        
        Args:
            expression: Expresión como string
            
        Returns:
            Función derivada evaluable
        """
        try:
            # Usar sympy para calcular derivada simbólica
            expr = FunctionParser.normalize_expression(expression)
            sympy_expr = sp.sympify(expr.replace('np.', ''))
            x = sp.Symbol('x')
            derivative = sp.diff(sympy_expr, x)
            
            # Convertir de vuelta a función evaluable
            derivative_str = str(derivative)
            return FunctionParser.parse_function(derivative_str)
        except Exception as e:
            raise ValueError(f"Error calculando derivada: {e}")
    
    @staticmethod
    def get_integral(expression: str) -> Callable:
        """
        Calcula la integral simbólica de una función
        
        Args:
            expression: Expresión como string
            
        Returns:
            Función integral evaluable
        """
        try:
            # Usar sympy para calcular integral simbólica
            expr = FunctionParser.normalize_expression(expression)
            sympy_expr = sp.sympify(expr.replace('np.', ''))
            x = sp.Symbol('x')
            integral = sp.integrate(sympy_expr, x)
            
            # Convertir de vuelta a función evaluable
            integral_str = str(integral)
            return FunctionParser.parse_function(integral_str)
        except Exception as e:
            raise ValueError(f"Error calculando integral: {e}")
    
    @staticmethod
    def substitute_constants(expression: str, constants: dict) -> str:
        """
        Sustituye constantes en una expresión
        
        Args:
            expression: Expresión original
            constants: Diccionario de constantes {nombre: valor}
            
        Returns:
            Expresión con constantes sustituidas
        """
        result = expression
        for name, value in constants.items():
            result = result.replace(name, str(value))
        return result
