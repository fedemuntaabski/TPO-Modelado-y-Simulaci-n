"""
Módulo de Métodos de Interpolación
Implementa interpolación de Lagrange, diferencias finitas y splines

Métodos incluidos:
- Interpolación de Lagrange
- Diferencias finitas para tablas
- Interpolación por splines cúbicos
"""

import numpy as np
from typing import Callable, List, Tuple
import matplotlib.pyplot as plt

class InterpolationMethods:
    """
    Clase que implementa métodos de interpolación y análisis numérico avanzado
    """
    
    @staticmethod
    def lagrange_interpolation_detailed(x_points: np.ndarray, y_points: np.ndarray, 
                                      x_eval: np.ndarray) -> Tuple[np.ndarray, Callable]:
        """
        Interpolación de Lagrange con evaluación en múltiples puntos
        
        Args:
            x_points: Puntos x conocidos
            y_points: Puntos y conocidos  
            x_eval: Puntos donde evaluar la interpolación
            
        Returns:
            Tupla (valores_interpolados, función_polinomial)
        """
        n = len(x_points)
        y_eval = np.zeros_like(x_eval)
        
        # Construir el polinomio de Lagrange
        for i in range(n):
            # Calcular Li(x) para cada punto de evaluación
            Li = np.ones_like(x_eval)
            for j in range(n):
                if i != j:
                    Li *= (x_eval - x_points[j]) / (x_points[i] - x_points[j])
            
            y_eval += y_points[i] * Li
        
        # Función que evalúa el polinomio en un punto
        def polynomial(x):
            result = 0
            for i in range(n):
                Li = 1
                for j in range(n):
                    if i != j:
                        Li *= (x - x_points[j]) / (x_points[i] - x_points[j])
                result += y_points[i] * Li
            return result
        
        return y_eval, polynomial
    
    @staticmethod
    def lagrange_interpolation(x_points: np.ndarray, y_points: np.ndarray, x: float) -> float:
        """
        Interpolación de Lagrange
        
        Args:
            x_points: Puntos x conocidos
            y_points: Puntos y conocidos
            x: Punto donde evaluar la interpolación
            
        Returns:
            Valor interpolado en x
        """
        n = len(x_points)
        result = 0
        
        for i in range(n):
            # Calcular el polinomio base de Lagrange L_i(x)
            Li = 1
            for j in range(n):
                if i != j:
                    Li *= (x - x_points[j]) / (x_points[i] - x_points[j])
            
            result += y_points[i] * Li
        
        return result
    
    @staticmethod
    def finite_differences_table(x_points: np.ndarray, y_points: np.ndarray) -> np.ndarray:
        """
        Construye una tabla de diferencias finitas
        
        Args:
            x_points: Puntos x conocidos
            y_points: Puntos y conocidos
            
        Returns:
            Tabla de diferencias finitas
        """
        n = len(x_points)
        table = np.zeros((n, n))
        table[:, 0] = y_points
        
        for j in range(1, n):
            for i in range(n - j):
                table[i, j] = table[i + 1, j - 1] - table[i, j - 1]
        
        return table
    
    @staticmethod
    def central_finite_differences_derivative_table(f: Callable, x: float, 
                                                   orders: List[int], h: float = 1e-5) -> dict:
        """
        Calcula derivadas de múltiples órdenes usando diferencias finitas centrales
        
        Args:
            f: Función a derivar
            x: Punto de evaluación
            orders: Lista de órdenes de derivada a calcular
            h: Paso para diferencias finitas
            
        Returns:
            Diccionario con las derivadas de cada orden
        """
        derivatives = {}
        
        for order in orders:
            if order == 1:
                # Primera derivada: f'(x) ≈ (f(x+h) - f(x-h)) / (2h)
                derivatives[1] = (f(x + h) - f(x - h)) / (2 * h)
            
            elif order == 2:
                # Segunda derivada: f''(x) ≈ (f(x+h) - 2f(x) + f(x-h)) / h²
                derivatives[2] = (f(x + h) - 2*f(x) + f(x - h)) / (h**2)
            
            elif order == 3:
                # Tercera derivada usando diferencias finitas centrales
                derivatives[3] = (f(x + 2*h) - 2*f(x + h) + 2*f(x - h) - f(x - 2*h)) / (2 * h**3)
            
            elif order == 4:
                # Cuarta derivada
                derivatives[4] = (f(x + 2*h) - 4*f(x + h) + 6*f(x) - 4*f(x - h) + f(x - 2*h)) / (h**4)
        
        return derivatives
    
    @staticmethod
    def spline_interpolation_simple(x_points: np.ndarray, y_points: np.ndarray, 
                                  x_eval: np.ndarray) -> np.ndarray:
        """
        Interpolación por splines cúbicos naturales (implementación simplificada)
        
        Args:
            x_points: Puntos x conocidos
            y_points: Puntos y conocidos
            x_eval: Puntos donde evaluar
            
        Returns:
            Valores interpolados
        """
        # Esta es una implementación simplificada
        # Para uso completo, se recomienda usar scipy.interpolate
        n = len(x_points)
        
        # Construir sistema para segundas derivadas
        h = np.diff(x_points)
        A = np.zeros((n, n))
        b = np.zeros(n)
        
        # Condiciones de frontera naturales
        A[0, 0] = 1
        A[n-1, n-1] = 1
        
        # Ecuaciones internas
        for i in range(1, n-1):
            A[i, i-1] = h[i-1]
            A[i, i] = 2 * (h[i-1] + h[i])
            A[i, i+1] = h[i]
            b[i] = 6 * ((y_points[i+1] - y_points[i]) / h[i] - 
                       (y_points[i] - y_points[i-1]) / h[i-1])
        
        # Resolver sistema
        c = np.linalg.solve(A, b)
        
        # Evaluar spline
        y_eval = np.zeros_like(x_eval)
        
        for i, x in enumerate(x_eval):
            # Encontrar intervalo
            j = np.searchsorted(x_points[1:], x)
            j = min(j, n-2)
            
            # Evaluar polinomio cúbico en el intervalo
            dx = x - x_points[j]
            y_eval[i] = (y_points[j] + 
                        (y_points[j+1] - y_points[j]) / h[j] * dx -
                        h[j] * c[j] / 6 * dx +
                        c[j] / 2 * dx**2 +
                        (c[j+1] - c[j]) / (6 * h[j]) * dx**3)
        
        return y_eval
