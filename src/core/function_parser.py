"""
Parser seguro para funciones matemáticas.

Implementa evaluación segura de funciones usando AST para prevenir
inyección de código malicioso. Soporte para funciones trigonométricas,
exponenciales, logarítmicas y constantes matemáticas.
"""

import ast
import math
import re
from typing import Dict, Tuple, Any, Union, Callable
import operator
import logging

logger = logging.getLogger(__name__)


class FunctionParserError(Exception):
    """Excepción personalizada para errores del parser"""
    pass


class SafeFunctionEvaluator:
    """Evaluador seguro de funciones matemáticas usando AST"""
    
    def __init__(self) -> None:
        # Operadores permitidos
        self.allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }
        
        # Funciones matemáticas permitidas
        self.allowed_functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'ln': math.log,
            'log': math.log10,
            'log2': math.log2,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'abs': abs,
            'floor': math.floor,
            'ceil': math.ceil,
            'factorial': math.factorial,
        }
        
        # Constantes matemáticas permitidas
        self.allowed_constants = {
            'pi': math.pi,
            'e': math.e,
            'inf': math.inf,
            'nan': math.nan,
        }
        
        # Contexto seguro para evaluación
        self.safe_context = {
            "__builtins__": {},
            **self.allowed_functions,
            **self.allowed_constants
        }
    
    def validate_function(self, func_str: str) -> Tuple[bool, str]:
        """
        Validar sintaxis y seguridad de función matemática
        
        Args:
            func_str: String de la función a validar
            
        Returns:
            Tuple con (es_válida, mensaje_error)
        """
        try:
            # Normalizar función
            normalized = self._normalize_function(func_str)
            
            # Parsear usando AST
            tree = ast.parse(normalized, mode='eval')
            
            # Validar nodos del AST
            self._validate_ast_nodes(tree)
            
            # Intentar evaluación con valor de prueba
            test_result = self.safe_eval(func_str, 1.0)
            
            if not isinstance(test_result, (int, float)) or math.isnan(test_result):
                return False, "La función no retorna un valor numérico válido"
                
            return True, "Función válida"
            
        except SyntaxError as e:
            return False, f"Error de sintaxis: {e}"
        except Exception as e:
            return False, f"Error de validación: {e}"
    
    def safe_eval(self, func_str: str, x_value: float) -> float:
        """
        Evaluación segura de función en punto x
        
        Args:
            func_str: String de la función
            x_value: Valor de x para evaluar
            
        Returns:
            Resultado de f(x)
            
        Raises:
            FunctionParserError: Si hay error en evaluación
        """
        try:
            # Normalizar función
            normalized = self._normalize_function(func_str)
            
            # Parsear y validar ANTES de reemplazar x
            tree = ast.parse(normalized, mode='eval')
            self._validate_ast_nodes(tree)
            
            # Crear contexto con x como variable
            eval_context = self.safe_context.copy()
            eval_context['x'] = x_value
            
            # Evaluar de forma segura
            result = eval(compile(tree, '<string>', 'eval'), eval_context)
            
            # Validar resultado
            if not isinstance(result, (int, float)):
                raise FunctionParserError(f"Resultado no numérico: {type(result)}")
            
            if math.isnan(result):
                raise FunctionParserError("La función retorna NaN")
            
            if math.isinf(result):
                raise FunctionParserError("La función retorna infinito")
                
            return float(result)
            
        except FunctionParserError:
            raise
        except Exception as e:
            raise FunctionParserError(f"Error evaluando función en x={x_value}: {e}")
    
    def _normalize_function(self, func_str: str) -> str:
        """Normalizar función para evaluación consistente"""
        # Remover espacios
        normalized = func_str.strip()
        
        # Reemplazar notaciones comunes
        replacements = {
            '^': '**',  # Potencia
            'ln(': 'ln(',  # Ya está bien
            'log(': 'log(',  # Ya está bien
            'PI': 'pi',
            'E': 'e',
        }
        
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        # Agregar multiplicación implícita antes de paréntesis
        normalized = re.sub(r'(\d)\(', r'\1*(', normalized)
        normalized = re.sub(r'([a-zA-Z])\(', r'\1(', normalized)
        
        return normalized
    
    def _validate_ast_nodes(self, node: ast.AST) -> None:
        """Validar que todos los nodos del AST sean seguros"""
        if isinstance(node, ast.Expression):
            self._validate_ast_nodes(node.body)
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in self.allowed_operators:
                raise FunctionParserError(f"Operador no permitido: {type(node.op)}")
            self._validate_ast_nodes(node.left)
            self._validate_ast_nodes(node.right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in self.allowed_operators:
                raise FunctionParserError(f"Operador unario no permitido: {type(node.op)}")
            self._validate_ast_nodes(node.operand)
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise FunctionParserError("Solo se permiten llamadas a funciones simples")
            if node.func.id not in self.allowed_functions:
                raise FunctionParserError(f"Función no permitida: {node.func.id}")
            for arg in node.args:
                self._validate_ast_nodes(arg)
        elif isinstance(node, ast.Name):
            if node.id not in self.allowed_constants and node.id != 'x':
                raise FunctionParserError(f"Variable/constante no permitida: {node.id}")
        elif isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise FunctionParserError(f"Constante no numérica: {type(node.value)}")
        elif isinstance(node, ast.Num):  # Compatibilidad con Python < 3.8
            if not isinstance(node.n, (int, float)):
                raise FunctionParserError(f"Número inválido: {type(node.n)}")
        else:
            raise FunctionParserError(f"Nodo AST no permitido: {type(node)}")


class FunctionParser:
    """Parser principal para funciones matemáticas"""
    
    def __init__(self) -> None:
        self.evaluator = SafeFunctionEvaluator()
    
    def parse_and_evaluate(self, func_str: str, x: float) -> float:
        """
        Parsear y evaluar función en punto x
        
        Args:
            func_str: String de la función
            x: Valor de x para evaluar
            
        Returns:
            Resultado de f(x)
        """
        return self.evaluator.safe_eval(func_str, x)
    
    def validate_function(self, func_str: str) -> Tuple[bool, str]:
        """
        Validar función matemática
        
        Args:
            func_str: String de la función a validar
            
        Returns:
            Tuple con (es_válida, mensaje)
        """
        return self.evaluator.validate_function(func_str)
    
    def get_function_info(self, func_str: str) -> Dict[str, Any]:
        """
        Obtener información completa sobre una función
        
        Args:
            func_str: String de la función
            
        Returns:
            Diccionario con información de la función
        """
        is_valid, message = self.validate_function(func_str)
        
        info = {
            'function_string': func_str,
            'is_valid': is_valid,
            'validation_message': message,
            'normalized': None,
            'sample_evaluations': []
        }
        
        if is_valid:
            try:
                info['normalized'] = self.evaluator._normalize_function(func_str)
                
                # Evaluaciones de muestra
                test_points = [0, 1, -1, 0.5, 2]
                for x in test_points:
                    try:
                        result = self.parse_and_evaluate(func_str, x)
                        info['sample_evaluations'].append({'x': x, 'f(x)': result})
                    except Exception as e:
                        info['sample_evaluations'].append({'x': x, 'error': str(e)})
                        
            except Exception as e:
                info['error'] = str(e)
        
        return info


# Funciones de utilidad
def create_function_evaluator(func_str: str) -> Callable[[float], float]:
    """
    Crear función evaluadora a partir de string
    
    Args:
        func_str: String de la función
        
    Returns:
        Función que evalúa f(x)
    """
    parser = FunctionParser()
    
    # Validar función
    is_valid, message = parser.validate_function(func_str)
    if not is_valid:
        raise FunctionParserError(f"Función inválida: {message}")
    
    def evaluator(x: float) -> float:
        return parser.parse_and_evaluate(func_str, x)
    
    return evaluator


def test_function_parser() -> None:
    """Función de prueba para el parser"""
    parser = FunctionParser()
    
    test_functions = [
        "x**2",
        "sin(x)",
        "exp(x) + cos(x)",
        "ln(x + 1)",
        "sqrt(x**2 + 1)",
        "x**3 - 2*x + 1",
        "abs(sin(x))",
        "pi * x**2",
    ]
    
    print("=== Pruebas del Parser de Funciones ===")
    for func in test_functions:
        is_valid, message = parser.validate_function(func)
        print(f"Función: {func}")
        print(f"  Válida: {is_valid}")
        print(f"  Mensaje: {message}")
        
        if is_valid:
            try:
                result = parser.parse_and_evaluate(func, 1.0)
                print(f"  f(1) = {result:.6f}")
            except Exception as e:
                print(f"  Error evaluando f(1): {e}")
        print()


if __name__ == "__main__":
    test_function_parser()
