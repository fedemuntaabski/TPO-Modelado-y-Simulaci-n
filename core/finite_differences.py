"""
Diferencias Finitas
Implementa métodos de diferenciación numérica usando diferencias finitas

Métodos incluidos:
- Diferencias hacia adelante
- Diferencias hacia atrás
- Diferencias centrales
- Derivadas de orden superior
"""

import numpy as np
from typing import Callable

class FiniteDifferences:
    """
    Clase que implementa métodos de diferenciación numérica
    """
    
    @staticmethod
    def forward(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Diferencias hacia adelante para primera derivada
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f'(x) usando diferencias hacia adelante
        """
        return (f(x + h) - f(x)) / h
    
    @staticmethod
    def backward(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Diferencias hacia atrás para primera derivada
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f'(x) usando diferencias hacia atrás
        """
        return (f(x) - f(x - h)) / h
    
    @staticmethod
    def central(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Diferencias centrales para primera derivada
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f'(x) usando diferencias centrales
        """
        return (f(x + h) - f(x - h)) / (2 * h)
    
    @staticmethod
    def second_derivative(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Segunda derivada usando diferencias finitas centrales
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la segunda derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f''(x)
        """
        return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)
    
    @staticmethod
    def third_derivative(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Tercera derivada usando diferencias finitas centrales
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la tercera derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f'''(x)
        """
        return (f(x + 2*h) - 2*f(x + h) + 2*f(x - h) - f(x - 2*h)) / (2 * h**3)
    
    @staticmethod
    def fourth_derivative(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Cuarta derivada usando diferencias finitas centrales
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la cuarta derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f''''(x)
        """
        return (f(x + 2*h) - 4*f(x + h) + 6*f(x) - 4*f(x - h) + f(x - 2*h)) / (h**4)
    
    @staticmethod
    def derivative_table(f: Callable, x: float, max_order: int = 4, h: float = 1e-5) -> dict:
        """
        Calcula derivadas de múltiples órdenes en un punto
        
        Args:
            f: Función a derivar
            x: Punto de evaluación
            max_order: Máximo orden de derivada a calcular
            h: Paso para diferencias finitas
            
        Returns:
            Diccionario con las derivadas de cada orden
        """
        derivatives = {}
        
        if max_order >= 1:
            derivatives[1] = FiniteDifferences.central(f, x, h)
        if max_order >= 2:
            derivatives[2] = FiniteDifferences.second_derivative(f, x, h)
        if max_order >= 3:
            derivatives[3] = FiniteDifferences.third_derivative(f, x, h)
        if max_order >= 4:
            derivatives[4] = FiniteDifferences.fourth_derivative(f, x, h)
        
        return derivatives
    
    @staticmethod
    def richardson_extrapolation(f: Callable, x: float, h_values: list) -> float:
        """
        Extrapolación de Richardson para mejorar la precisión de derivadas
        
        Args:
            f: Función a derivar
            x: Punto de evaluación
            h_values: Lista de valores de h en orden decreciente
            
        Returns:
            Aproximación mejorada de f'(x)
        """
        if len(h_values) < 2:
            return FiniteDifferences.central(f, x, h_values[0])
        
        # Calcular aproximaciones con diferentes h
        D = {}
        for i, h in enumerate(h_values):
            D[i, 0] = FiniteDifferences.central(f, x, h)
        
        # Aplicar extrapolación de Richardson
        for j in range(1, len(h_values)):
            for i in range(len(h_values) - j):
                D[i, j] = D[i+1, j-1] + (D[i+1, j-1] - D[i, j-1]) / (4**j - 1)
        
        return D[0, len(h_values)-1]
