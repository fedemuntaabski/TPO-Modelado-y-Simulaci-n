"""
Módulo de interpolación polinómica de Lagrange.

Este módulo implementa el algoritmo de interpolación polinómica de Lagrange,
que permite construir un polinomio que pasa exactamente por un conjunto de puntos dados.
"""

import numpy as np
from typing import List, Tuple, Callable, Union


class LagrangeInterpolation:
    """
    Implementación del método de interpolación polinómica de Lagrange.
    
    Este método construye un polinomio de grado n-1 que pasa exactamente por n puntos dados.
    """
    
    def __init__(self, points: List[Tuple[float, float]] = None):
        """
        Inicializa el interpolador de Lagrange con puntos opcionales.
        
        Args:
            points: Lista de tuplas (x, y) que representan los puntos a interpolar.
        """
        self.points = points or []
        self.coefficients = []
        self.polynomial_str = ""
        
        if self.points:
            self._compute_interpolation()
    
    def set_points(self, points: List[Tuple[float, float]]):
        """
        Establece los puntos para la interpolación.
        
        Args:
            points: Lista de tuplas (x, y) que representan los puntos a interpolar.
        """
        self.points = points
        self._compute_interpolation()
        return self
    
    def add_point(self, x: float, y: float):
        """
        Agrega un punto a la lista de puntos a interpolar.
        
        Args:
            x: Coordenada x del punto.
            y: Coordenada y del punto.
        """
        self.points.append((x, y))
        self._compute_interpolation()
        return self
    
    def _compute_basis_polynomial(self, j: int, x: float) -> float:
        """
        Calcula el valor del j-ésimo polinomio base de Lagrange en el punto x.
        
        Args:
            j: Índice del polinomio base.
            x: Punto donde evaluar el polinomio.
            
        Returns:
            Valor del polinomio base en el punto x.
        """
        n = len(self.points)
        result = 1.0
        x_j = self.points[j][0]
        
        for i in range(n):
            if i != j:
                x_i = self.points[i][0]
                result *= (x - x_i) / (x_j - x_i)
        
        return result
    
    def _compute_interpolation(self):
        """
        Calcula la interpolación polinómica de Lagrange para los puntos dados.
        """
        if not self.points or len(self.points) < 2:
            raise ValueError("Se necesitan al menos 2 puntos para la interpolación.")
        
        # Comprobar que los valores x son únicos
        x_values = [p[0] for p in self.points]
        if len(x_values) != len(set(x_values)):
            raise ValueError("Los valores de x deben ser únicos.")
        
        # Ordenar los puntos por valor de x
        self.points.sort(key=lambda p: p[0])
        
        # Crear representación simbólica del polinomio
        self._generate_polynomial_string()
    
    def _generate_polynomial_string(self):
        """
        Genera una representación en cadena del polinomio interpolante.
        """
        n = len(self.points)
        polynomial_terms = []
        
        for j in range(n):
            y_j = self.points[j][1]
            x_j = self.points[j][0]
            
            # Construir el término del polinomio base
            basis_terms = []
            for i in range(n):
                if i != j:
                    x_i = self.points[i][0]
                    basis_terms.append(f"(x - {x_i:.6g}) / ({x_j:.6g} - {x_i:.6g})")
            
            # Unir todos los términos del polinomio base
            basis_poly = " * ".join(basis_terms)
            polynomial_terms.append(f"{y_j:.6g} * ({basis_poly})")
        
        # Unir todos los términos del polinomio interpolante
        self.polynomial_str = " + ".join(polynomial_terms)
    
    def interpolate(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Evalúa el polinomio interpolante en el punto o puntos dados.
        
        Args:
            x: Valor o array de valores donde evaluar el polinomio.
            
        Returns:
            Valor o array de valores interpolados.
        """
        if not self.points:
            raise ValueError("No hay puntos para interpolar. Use set_points() primero.")
        
        # Si x es un array, aplicar la función a cada elemento
        if isinstance(x, np.ndarray):
            return np.array([self._interpolate_single(xi) for xi in x])
        else:
            return self._interpolate_single(x)
    
    def _interpolate_single(self, x: float) -> float:
        """
        Evalúa el polinomio interpolante en un único punto.
        
        Args:
            x: Valor donde evaluar el polinomio.
            
        Returns:
            Valor interpolado.
        """
        result = 0.0
        for j, (_, y_j) in enumerate(self.points):
            result += y_j * self._compute_basis_polynomial(j, x)
        
        return result
    
    def get_polynomial_function(self) -> Callable[[float], float]:
        """
        Retorna una función que representa el polinomio interpolante.
        
        Returns:
            Función que evalúa el polinomio interpolante en un punto.
        """
        return lambda x: self.interpolate(x)
    
    def get_polynomial_string(self) -> str:
        """
        Retorna una representación en cadena del polinomio interpolante.
        
        Returns:
            Cadena que representa el polinomio interpolante.
        """
        return self.polynomial_str
    
    def get_error_bounds(self, func=None, a=None, b=None, n_points=1000) -> dict:
        """
        Calcula y retorna estimaciones del error de interpolación.
        
        Args:
            func: Función original de la que se conocen los puntos (opcional).
            a: Límite inferior del intervalo para calcular el error (opcional).
            b: Límite superior del intervalo para calcular el error (opcional).
            n_points: Número de puntos para el cálculo del error (opcional).
            
        Returns:
            Diccionario con estadísticas del error.
        """
        if not self.points:
            raise ValueError("No hay puntos para interpolar.")
        
        if func is None or a is None or b is None:
            # Si no se proporciona la función original o los límites, 
            # calculamos el error en los puntos interpolados
            x_values = np.array([p[0] for p in self.points])
            y_values = np.array([p[1] for p in self.points])
            y_interpolated = self.interpolate(x_values)
            error = y_values - y_interpolated
            
            return {
                "max_error": np.max(np.abs(error)),
                "mean_error": np.mean(np.abs(error)),
                "points_error": list(zip(x_values, error))
            }
        else:
            # Si se proporciona la función original y los límites,
            # calculamos el error en todo el intervalo
            x_values = np.linspace(a, b, n_points)
            y_original = np.array([func(x) for x in x_values])
            y_interpolated = self.interpolate(x_values)
            error = y_original - y_interpolated
            
            return {
                "max_error": np.max(np.abs(error)),
                "mean_error": np.mean(np.abs(error)),
                "max_error_at": x_values[np.argmax(np.abs(error))],
                "error_points": list(zip(x_values, error))
            }