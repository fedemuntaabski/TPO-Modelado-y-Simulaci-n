"""
Módulo de Utilidades para Parsing de Expresiones Matemáticas
Implementa clases y funciones para parsear y evaluar expresiones matemáticas

Funcionalidades:
- Parsing de funciones matemáticas
- Parsing de funciones para EDOs
- Evaluación segura de expresiones
"""

import numpy as np
from typing import Callable

class MathParser:
    """
    Clase para parsear y evaluar expresiones matemáticas ingresadas por el usuario
    """

    @staticmethod
    def parse_function(expression: str) -> Callable:
        """
        Convierte una expresión string en una función evaluable

        Args:
            expression: Expresión matemática como string (ej: "x**2 + 2*x + 1")

        Returns:
            Función que puede ser evaluada
        """
        # Reemplazar funciones comunes por sus equivalentes numpy
        expression = expression.replace('^', '**')
        expression = expression.replace('sin', 'np.sin')
        expression = expression.replace('cos', 'np.cos')
        expression = expression.replace('tan', 'np.tan')
        expression = expression.replace('exp', 'np.exp')
        expression = expression.replace('log', 'np.log')
        expression = expression.replace('sqrt', 'np.sqrt')
        expression = expression.replace('pi', 'np.pi')
        expression = expression.replace('e', 'np.e')

        def func(x):
            return eval(expression, {"np": np, "x": x})

        return func

    @staticmethod
    def parse_ode_function(expression: str) -> Callable:
        """
        Parsea una función para ecuaciones diferenciales dy/dt = f(t, y)

        Args:
            expression: Expresión como string (ej: "t + y", "-y + t**2")

        Returns:
            Función f(t, y)
        """
        expression = expression.replace('^', '**')
        expression = expression.replace('sin', 'np.sin')
        expression = expression.replace('cos', 'np.cos')
        expression = expression.replace('tan', 'np.tan')
        expression = expression.replace('exp', 'np.exp')
        expression = expression.replace('log', 'np.log')
        expression = expression.replace('sqrt', 'np.sqrt')
        expression = expression.replace('pi', 'np.pi')
        expression = expression.replace('e', 'np.e')

        def func(t, y):
            return eval(expression, {"np": np, "t": t, "y": y})

        return func

    @staticmethod
    def evaluate_expression(expression: str, x: float = 0) -> float:
        """
        Evalúa una expresión matemática en un punto dado

        Args:
            expression: Expresión como string
            x: Valor donde evaluar la expresión

        Returns:
            Resultado numérico de la evaluación
        """
        try:
            func = MathParser.parse_function(expression)
            return func(x)
        except Exception as e:
            raise ValueError(f"Error evaluando expresión: {e}")

class ExpressionUtils:
    """
    Utilidades para manejo de expresiones matemáticas
    """

    @staticmethod
    def safe_eval(expression: str, variables: dict = None) -> float:
        """
        Evaluación segura de expresiones matemáticas

        Args:
            expression: Expresión a evaluar
            variables: Diccionario con variables y sus valores

        Returns:
            Resultado de la evaluación
        """
        if variables is None:
            variables = {}

        # Crear namespace seguro
        safe_dict = {
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'exp': np.exp,
            'log': np.log,
            'log10': np.log10,
            'sqrt': np.sqrt,
            'pi': np.pi,
            'e': np.e,
            'abs': abs,
            'pow': pow,
            **variables
        }

        try:
            return eval(expression, {"__builtins__": {}}, safe_dict)
        except Exception as e:
            raise ValueError(f"Error en evaluación segura: {e}")

    @staticmethod
    def validate_expression(expression: str) -> bool:
        """
        Valida si una expresión matemática es sintácticamente correcta

        Args:
            expression: Expresión a validar

        Returns:
            True si es válida, False en caso contrario
        """
        try:
            # Intentar compilar la expresión
            compile(expression, '<string>', 'eval')
            return True
        except SyntaxError:
            return False

    @staticmethod
    def extract_variables(expression: str) -> set:
        """
        Extrae las variables presentes en una expresión

        Args:
            expression: Expresión matemática

        Returns:
            Conjunto de variables encontradas
        """
        import ast
        import re

        # Palabras reservadas y funciones que no son variables
        reserved = {
            'sin', 'cos', 'tan', 'exp', 'log', 'log10', 'sqrt',
            'pi', 'e', 'abs', 'pow', 'sum', 'max', 'min'
        }

        try:
            # Parsear la expresión
            tree = ast.parse(expression, mode='eval')

            variables = set()

            def visit_node(node):
                if isinstance(node, ast.Name):
                    if node.id not in reserved:
                        variables.add(node.id)
                elif hasattr(node, 'body'):
                    if isinstance(node.body, list):
                        for child in node.body:
                            visit_node(child)
                    else:
                        visit_node(node.body)

            visit_node(tree)
            return variables

        except SyntaxError:
            return set()
