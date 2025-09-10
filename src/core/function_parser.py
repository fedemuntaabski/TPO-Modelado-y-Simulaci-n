"""
Parser seguro para funciones matemáticas.

Implementa evaluación segura de funciones usando eval con contexto restringido.
"""

import math
from typing import Callable


class FunctionParserError(Exception):
    """Excepción personalizada para errores del parser"""
    pass


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
