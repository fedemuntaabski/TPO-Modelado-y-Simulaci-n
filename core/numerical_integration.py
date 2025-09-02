"""
Integración Numérica
Implementa métodos de integración numérica (reglas de Newton-Cotes)

Métodos incluidos:
- Regla del Trapecio
- Regla de Simpson 1/3
- Regla de Simpson 3/8
- Cuadratura de Gauss (opcional avanzado)
"""

import numpy as np
from typing import Callable
from scipy.integrate import quad

class NumericalIntegration:
    """
    Clase que implementa métodos de integración numérica
    """
    
    @staticmethod
    def trapezoid(f: Callable, a: float, b: float, n: int = 100) -> float:
        """
        Regla del Trapecio para integración numérica
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            n: Número de subdivisiones
            
        Returns:
            Valor de la integral aproximada
        """
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])
        
        # Regla del trapecio: h/2 * (y0 + 2*(y1 + y2 + ... + yn-1) + yn)
        integral = h/2 * (y[0] + 2*np.sum(y[1:-1]) + y[-1])
        return integral
    
    @staticmethod
    def simpson_13(f: Callable, a: float, b: float, n: int = 100) -> float:
        """
        Regla de Simpson 1/3 para integración numérica
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            n: Número de subdivisiones (debe ser par)
            
        Returns:
            Valor de la integral aproximada
        """
        if n % 2 != 0:
            n += 1  # Asegurar que n sea par
        
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])
        
        # Regla de Simpson 1/3
        integral = h/3 * (y[0] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-2:2]) + y[-1])
        return integral
    
    @staticmethod
    def simpson_38(f: Callable, a: float, b: float, n: int = 100) -> float:
        """
        Regla de Simpson 3/8 para integración numérica
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            n: Número de subdivisiones (debe ser múltiplo de 3)
            
        Returns:
            Valor de la integral aproximada
        """
        if n % 3 != 0:
            n = ((n // 3) + 1) * 3  # Asegurar que n sea múltiplo de 3
        
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])
        
        # Regla de Simpson 3/8
        integral = 3*h/8 * (y[0] + 3*np.sum(y[1:-1:3]) + 3*np.sum(y[2:-1:3]) + 2*np.sum(y[3:-1:3]) + y[-1])
        return integral
    
    @staticmethod
    def gauss_quadrature(f: Callable, a: float, b: float, n: int = 5) -> float:
        """
        Cuadratura de Gauss para integración numérica (usando scipy)
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            n: Orden de la cuadratura (número de puntos)
            
        Returns:
            Valor de la integral aproximada
        """
        # Transformar intervalo [a,b] a [-1,1]
        def transformed_f(x):
            return f((b-a)/2 * x + (a+b)/2) * (b-a)/2
        
        # Usar scipy para cuadratura de Gauss
        result, _ = quad(transformed_f, -1, 1)
        return result
    
    @staticmethod
    def adaptive_simpson(f: Callable, a: float, b: float, tol: float = 1e-6) -> float:
        """
        Integración adaptativa usando regla de Simpson
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            tol: Tolerancia deseada
            
        Returns:
            Valor de la integral aproximada
        """
        def simpson_basic(a, b):
            """Regla de Simpson básica para un intervalo"""
            c = (a + b) / 2
            return (b - a) / 6 * (f(a) + 4*f(c) + f(b))
        
        def adaptive_recursive(a, b, tol, S, depth=0):
            """Función recursiva para integración adaptativa"""
            if depth > 50:  # Evitar recursión infinita
                return S
            
            c = (a + b) / 2
            S_left = simpson_basic(a, c)
            S_right = simpson_basic(c, b)
            S_new = S_left + S_right
            
            if abs(S_new - S) <= 15 * tol:
                return S_new + (S_new - S) / 15
            else:
                left_result = adaptive_recursive(a, c, tol/2, S_left, depth + 1)
                right_result = adaptive_recursive(c, b, tol/2, S_right, depth + 1)
                return left_result + right_result
        
        S = simpson_basic(a, b)
        return adaptive_recursive(a, b, tol, S)
