"""
Parser seguro para funciones matemáticas.

Implementa evaluación segura de funciones usando eval con contexto restringido.
Incluye soporte para ecuaciones cónicas del tipo x^2 + y^2 = 1.
"""

import math
import re
from typing import Callable, Tuple


class FunctionParserError(Exception):
    """Excepción personalizada para errores del parser"""
    pass


def parse_conic_equation(equation_str: str) -> Callable:
    """
    Parsea ecuaciones cónicas del tipo 'x**2 + y**2 = 1' y devuelve una función
    que determina si un punto (x,y) está dentro, fuera o sobre la curva.
    
    Args:
        equation_str: String de la ecuación (ej: "x**2 + y**2 = 1")
    
    Returns:
        Función que retorna 1 si el punto está dentro/sobre la curva, 0 si está fuera
    """
    # Limpiar y normalizar la ecuación
    equation = equation_str.strip().replace(' ', '').replace('^', '**')
    
    # Dividir por el signo =
    if '=' not in equation:
        raise FunctionParserError("La ecuación debe contener el signo '='")
    
    left_side, right_side = equation.split('=', 1)
    
    # Contexto seguro para evaluación
    safe_dict = {
        "__builtins__": {},
        "math": math,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "log": math.log,
        "ln": math.log,
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "pow": pow,
        "**": pow,
    }
    
    try:
        # Compilar ambos lados de la ecuación
        left_code = compile(left_side, "<left_side>", "eval")
        right_code = compile(right_side, "<right_side>", "eval")
        
        def conic_function(x, y):
            """
            Función que evalúa si un punto (x,y) satisface la ecuación cónica.
            Retorna 1 si está dentro o sobre la curva, 0 si está fuera.
            """
            local_dict = safe_dict.copy()
            local_dict['x'] = x
            local_dict['y'] = y
            
            try:
                left_val = eval(left_code, {"__builtins__": {}}, local_dict)
                right_val = eval(right_code, {"__builtins__": {}}, local_dict)
                
                # Para Monte Carlo, consideramos puntos dentro/sobre la curva
                # Por ejemplo: x² + y² ≤ 1 para el círculo unitario
                return 1 if left_val <= right_val else 0
                
            except (ZeroDivisionError, ValueError, OverflowError):
                # Si hay error matemático, considerar fuera de la región
                return 0
        
        return conic_function
        
    except Exception as e:
        raise FunctionParserError(f"Error parsing conic equation '{equation_str}': {e}")


def parse_conic_equation_strict(equation_str: str) -> Callable:
    """
    Versión estricta que solo acepta puntos exactamente sobre la curva.
    Útil para visualización de la curva.
    """
    equation = equation_str.strip().replace(' ', '').replace('^', '**')
    
    if '=' not in equation:
        raise FunctionParserError("La ecuación debe contener el signo '='")
    
    left_side, right_side = equation.split('=', 1)
    
    safe_dict = {
        "__builtins__": {},
        "math": math,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "exp": math.exp, "log": math.log, "ln": math.log,
        "sqrt": math.sqrt, "pi": math.pi, "e": math.e,
        "abs": abs, "pow": pow,
    }
    
    try:
        left_code = compile(left_side, "<left_side>", "eval")
        right_code = compile(right_side, "<right_side>", "eval")
        
        def strict_conic_function(x, y, tolerance=1e-6):
            local_dict = safe_dict.copy()
            local_dict['x'] = x
            local_dict['y'] = y
            
            try:
                left_val = eval(left_code, {"__builtins__": {}}, local_dict)
                right_val = eval(right_code, {"__builtins__": {}}, local_dict)
                
                # Verificar si están aproximadamente iguales
                return abs(left_val - right_val) <= tolerance
                
            except (ZeroDivisionError, ValueError, OverflowError):
                return False
        
        return strict_conic_function
        
    except Exception as e:
        raise FunctionParserError(f"Error parsing strict conic equation '{equation_str}': {e}")


def detect_conic_type(equation_str: str) -> str:
    """
    Detecta el tipo de cónica basándose en la ecuación.
    
    Returns:
        Tipo de cónica: 'circle', 'ellipse', 'parabola', 'hyperbola', 'unknown'
    """
    equation = equation_str.strip().replace(' ', '').replace('^', '**').lower()
    
    # Patrones básicos
    if re.search(r'x\*\*2\s*\+\s*y\*\*2', equation):
        return 'circle'
    elif re.search(r'x\*\*2\s*/\s*\d+\s*\+\s*y\*\*2\s*/\s*\d+', equation) or \
         re.search(r'x\*\*2\s*\+\s*y\*\*2\s*/\s*\d+', equation):
        return 'ellipse'
    elif re.search(r'x\*\*2\s*-\s*y\*\*2', equation) or \
         re.search(r'y\*\*2\s*-\s*x\*\*2', equation):
        return 'hyperbola'
    elif 'x**2' in equation and 'y**2' not in equation:
        return 'parabola'
    elif 'y**2' in equation and 'x**2' not in equation:
        return 'parabola'
    else:
        return 'unknown'


def parse_function(func_str: str, variables: list) -> Callable:
    """
    Crear una función segura a partir de un string.

    Args:
        func_str: String de la función
        variables: Lista de nombres de variables

    Returns:
        Función callable
    """
    # Contexto seguro
    safe_dict = {
        "__builtins__": {},
        "math": math,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "log": math.log,
        "ln": math.log,  # Alias para log natural
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,  # Agregar la función abs
    }

    # Agregar variables
    for var in variables:
        safe_dict[var] = 0  # Placeholder

    try:
        # Compilar la función
        code = compile(func_str, "<string>", "eval")

        def func(*args):
            # Actualizar variables con valores
            local_dict = safe_dict.copy()
            for i, var in enumerate(variables):
                local_dict[var] = args[i]
            return eval(code, {"__builtins__": {}}, local_dict)

        return func
    except Exception as e:
        raise FunctionParserError(f"Error parsing function: {e}")


class FunctionParser:
    """Clase para parsear funciones (placeholder)"""

    def __init__(self):
        pass

    def parse(self, func_str: str) -> Callable:
        return parse_function(func_str, ["x"])
        
    def parse_and_evaluate(self, func_str: str, x: float) -> float:
        """
        Parsear y evaluar una función en un punto
        
        Args:
            func_str: String de la función
            x: Valor donde evaluar
            
        Returns:
            Resultado de evaluar la función en x
        """
        try:
            func = self.parse(func_str)
            return func(x)
        except Exception as e:
            raise FunctionParserError(f"Error evaluating function '{func_str}' at x={x}: {e}")
            
    def validate_function(self, func_str: str, x_range=None):
        """
        Validar que una función sea parseable y evaluable
        
        Args:
            func_str: String de la función
            x_range: Rango de valores x para validar (min, max)
            
        Returns:
            (bool, str): Tupla con (es_válida, mensaje_error)
        """
        # Lista de funciones permitidas
        allowed_functions = ["sin", "cos", "tan", "exp", "log", "ln", "sqrt", "abs"]
        
        # Verificar funciones desconocidas
        import re
        function_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        matches = re.findall(function_pattern, func_str)
        
        for match in matches:
            if match not in allowed_functions and match != "x":
                return False, f"Función desconocida: {match}"
        
        try:
            # Intentar parsear
            func = self.parse(func_str)
            
            # Validar en puntos específicos si se proporciona rango
            if x_range:
                x_min, x_max = x_range
                # Probar en límites y algunos puntos intermedios
                test_points = [x_min, x_max, (x_min + x_max) / 2]
                for x in test_points:
                    try:
                        result = func(x)
                        if math.isnan(result) or math.isinf(result):
                            return False, f"La función no se puede evaluar correctamente en x={x}"
                    except Exception as e:
                        return False, f"La función no se puede evaluar en x={x}: {e}"
            
            return True, ""
        except Exception as e:
            return False, f"Función inválida: {str(e)}"
