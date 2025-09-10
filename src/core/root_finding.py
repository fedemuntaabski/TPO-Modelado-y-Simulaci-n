"""
Métodos numéricos para la búsqueda de raíces de ecuaciones no lineales.

Este módulo implementa algoritmos clásicos siguiendo el principio DRY y SOLID.
Cada método está optimizado para rendimiento y mantiene responsabilidad única.
"""

import numpy as np
from typing import Callable, Tuple, List, Optional
import logging

logger = logging.getLogger(__name__)


class RootFindingResult:
    """Resultado de búsqueda de raíces siguiendo el principio de encapsulación"""
    
    def __init__(self, root: float, iterations: int, converged: bool, 
                 error: float, function_value: float, iteration_data: List = None):
        self.root = root
        self.iterations = iterations
        self.converged = converged
        self.error = error
        self.function_value = function_value
        self.iteration_data = iteration_data or []


class RootFinder:
    """
    Clase principal para métodos de búsqueda de raíces.
    Sigue el principio de responsabilidad única (SRP) del SOLID.
    """
    
    def __init__(self, tolerance: float = 1e-6, max_iterations: int = 100) -> None:
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    
    def bisection_method(self, f: Callable[[float], float], 
                        a: float, b: float) -> RootFindingResult:
        """
        Método de bisección para encontrar raíces.
        
        Args:
            f: Función a evaluar
            a: Límite inferior del intervalo
            b: Límite superior del intervalo
            
        Returns:
            RootFindingResult con información completa del proceso
        """
        # Verificar precondiciones
        if f(a) * f(b) > 0:
            raise ValueError("No hay cambio de signo en el intervalo [a, b]")
        
        iterations_data = []
        
        for i in range(self.max_iterations):
            c = (a + b) / 2
            fc = f(c)
            error = abs(b - a) / 2
            
            iterations_data.append({
                'iteration': i + 1,
                'a': a,
                'b': b, 
                'c': c,
                'f_c': fc,
                'error': error
            })
            
            # Criterio de convergencia
            if abs(fc) < self.tolerance or error < self.tolerance:
                return RootFindingResult(
                    root=c,
                    iterations=i + 1,
                    converged=True,
                    error=error,
                    function_value=fc,
                    iteration_data=iterations_data
                )
            
            # Actualizar intervalo
            if f(a) * fc < 0:
                b = c
            else:
                a = c
        
        # No convergió
        return RootFindingResult(
            root=c,
            iterations=self.max_iterations,
            converged=False,
            error=error,
            function_value=fc,
            iteration_data=iterations_data
        )
    
    def newton_raphson_method(self, f: Callable[[float], float],
                             df: Optional[Callable[[float], float]],
                             x0: float) -> RootFindingResult:
        """
        Método de Newton-Raphson para encontrar raíces.
        
        Args:
            f: Función a evaluar
            df: Derivada de la función (si es None, se calcula numéricamente)
            x0: Punto inicial
            
        Returns:
            RootFindingResult con información completa del proceso
        """
        if df is None:
            df = self._numerical_derivative(f)
        
        x = x0
        iterations_data = []
        
        for i in range(self.max_iterations):
            fx = f(x)
            dfx = df(x)
            
            if abs(dfx) < 1e-12:
                raise ValueError("Derivada muy pequeña, el método puede no converger")
            
            x_new = x - fx / dfx
            error = abs(x_new - x)
            
            iterations_data.append({
                'iteration': i + 1,
                'x_n': x,
                'f_x_n': fx,
                'df_x_n': dfx,
                'x_n_plus_1': x_new,
                'error': error
            })
            
            if error < self.tolerance:
                return RootFindingResult(
                    root=x_new,
                    iterations=i + 1,
                    converged=True,
                    error=error,
                    function_value=f(x_new),
                    iteration_data=iterations_data
                )
            
            x = x_new
        
        return RootFindingResult(
            root=x,
            iterations=self.max_iterations,
            converged=False,
            error=error,
            function_value=f(x),
            iteration_data=iterations_data
        )
    
    def fixed_point_method(self, g: Callable[[float], float],
                          x0: float) -> RootFindingResult:
        """
        Método de punto fijo para encontrar soluciones de x = g(x).
        
        Args:
            g: Función de iteración g(x)
            x0: Punto inicial
            
        Returns:
            RootFindingResult con información completa del proceso
        """
        x = x0
        iterations_data = []
        
        for i in range(self.max_iterations):
            x_new = g(x)
            error = abs(x_new - x)
            
            iterations_data.append({
                'iteration': i + 1,
                'x_n': x,
                'g_x_n': x_new,
                'error': error
            })
            
            if error < self.tolerance:
                return RootFindingResult(
                    root=x_new,
                    iterations=i + 1,
                    converged=True,
                    error=error,
                    function_value=abs(x_new - g(x_new)),  # Para punto fijo
                    iteration_data=iterations_data
                )
            
            x = x_new
        
        return RootFindingResult(
            root=x,
            iterations=self.max_iterations,
            converged=False,
            error=error,
            function_value=abs(x - g(x)),
            iteration_data=iterations_data
        )
    
    def aitken_acceleration(self, g: Callable[[float], float], 
                           x0: float) -> RootFindingResult:
        """
        Método de aceleración de Aitken (Δ²) para mejorar convergencia.
        
        Args:
            g: Función de punto fijo x = g(x)
            x0: Punto inicial
            
        Returns:
            RootFindingResult con información completa del proceso
        """
        iteration_data = []
        x = x0
        
        for i in range(self.max_iterations):
            # Calcular tres iteraciones de punto fijo
            x1 = g(x)
            x2 = g(x1)
            
            # Aplicar aceleración de Aitken
            denominator = x2 - 2*x1 + x
            
            if abs(denominator) < 1e-14:
                # Si el denominador es muy pequeño, usar punto fijo normal
                x_new = x2
            else:
                # Fórmula de Aitken: x_new = x - (x1 - x)²/(x2 - 2*x1 + x)
                x_new = x - (x1 - x)**2 / denominator
            
            error = abs(x_new - x)
            iteration_data.append({
                'iteration': i + 1,
                'x': x,
                'x1': x1, 
                'x2': x2,
                'x_aitken': x_new,
                'error': error
            })
            
            if error < self.tolerance:
                logger.info(f"Aitken convergió en {i+1} iteraciones")
                return RootFindingResult(
                    root=x_new,
                    iterations=i + 1,
                    converged=True,
                    error=error,
                    function_value=abs(x_new - g(x_new)),
                    iteration_data=iteration_data
                )
            
            x = x_new
        
        logger.warning(f"Aitken no convergió en {self.max_iterations} iteraciones")
        return RootFindingResult(
            root=x,
            iterations=self.max_iterations,
            converged=False,
            error=error,
            function_value=abs(x - g(x)),
            iteration_data=iteration_data
        )
    
    def _numerical_derivative(self, f: Callable[[float], float], 
                             h: float = 1e-8) -> Callable[[float], float]:
        """
        Calcula la derivada numérica usando diferencias centrales.
        Principio DRY: reutilizable para cualquier función.
        """
        def df(x: float) -> float:
            return (f(x + h) - f(x - h)) / (2 * h)
        return df


# Funciones de utilidad para conversión de funciones (principio KISS)
def create_function_from_string(expr: str) -> Callable[..., float]:
    """
    Crea una función evaluable desde una expresión string.
    Soporta múltiples argumentos para diferentes contextos (raíces, integración, EDOs).
    Principio DRY: versión consolidada y mejorada.
    """
    # Lista completa de funciones matemáticas permitidas
    allowed_names = {
        "x": None,  # Variable independiente
        "t": None,  # Variable de tiempo (para EDOs)
        "y": None,  # Variable dependiente (para EDOs)
        "sin": np.sin, "cos": np.cos, "tan": np.tan,
        "exp": np.exp, "log": np.log, "log10": np.log10,
        "sqrt": np.sqrt, "abs": abs,
        "pi": np.pi, "e": np.e,
        "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
        "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan
    }

    def safe_function(*args):
        # Preparar el namespace seguro
        namespace = allowed_names.copy()

        # Asignar variables según el número de argumentos
        if len(args) == 1:
            namespace["x"] = args[0]
            namespace["t"] = args[0]  # Alias para tiempo
        elif len(args) == 2:
            namespace["t"] = args[0]
            namespace["y"] = args[1]

        try:
            # Reemplazar notaciones comunes
            processed_expr = expr.replace('^', '**').replace('sen', 'sin').replace('ln', 'log')
            return eval(processed_expr, {"__builtins__": {}}, namespace)
        except Exception as e:
            raise ValueError(f"Error evaluando función '{expr}': {e}")

    return safe_function


def convert_to_fixed_point(f: Callable[[float], float], 
                          method: str = "simple") -> Callable[[float], float]:
    """
    Convierte f(x) = 0 a una función de punto fijo x = g(x).
    Implementa diferentes estrategias de conversión.
    """
    if method == "simple":
        # g(x) = x + f(x)
        return lambda x: x + f(x)
    elif method == "damped":
        # g(x) = x + α*f(x) con α = 0.1 (amortiguado)
        alpha = 0.1
        return lambda x: x + alpha * f(x)
    else:
        raise ValueError(f"Método de conversión '{method}' no reconocido")
