"""
Módulo de Métodos Básicos para Encontrar Raíces
Implementa algoritmos básicos para encontrar raíces de ecuaciones no lineales

Métodos incluidos:
- Bisección
- Newton-Raphson
- Punto fijo
"""

import numpy as np
from typing import Callable, Tuple, List

class RootBasicMethods:
    """
    Clase que encapsula métodos básicos para encontrar raíces de ecuaciones
    """

    @staticmethod
    def bisection_method(f: Callable, a: float, b: float, tol: float = 1e-6,
                        max_iter: int = 100) -> Tuple[float, int, List[float]]:
        """
        Método de bisección para encontrar raíces

        Args:
            f: Función
            a: Extremo izquierdo del intervalo
            b: Extremo derecho del intervalo
            tol: Tolerancia
            max_iter: Máximo número de iteraciones

        Returns:
            Tupla (raíz, iteraciones, historial)
        """
        if f(a) * f(b) >= 0:
            raise ValueError("La función debe tener signos opuestos en los extremos del intervalo")

        history = []
        c = (a + b) / 2
        history.append(c)

        for i in range(max_iter):
            if abs(f(c)) < tol:
                return c, i + 1, history

            if f(a) * f(c) < 0:
                b = c
            else:
                a = c

            c = (a + b) / 2
            history.append(c)

            if abs(b - a) < tol:
                return c, i + 1, history

        return c, max_iter, history

    @staticmethod
    def newton_raphson_method(f: Callable, df: Callable, x0: float,
                             tol: float = 1e-6, max_iter: int = 100) -> Tuple[float, int, List[float]]:
        """
        Método de Newton-Raphson para encontrar raíces

        Args:
            f: Función
            df: Derivada de la función
            x0: Aproximación inicial
            tol: Tolerancia
            max_iter: Máximo número de iteraciones

        Returns:
            Tupla (raíz, iteraciones, historial)
        """
        x = x0
        history = [x0]

        for i in range(max_iter):
            fx = f(x)
            dfx = df(x)

            if abs(dfx) < 1e-14:
                raise ValueError("Derivada muy pequeña, método puede no converger")

            x_new = x - fx / dfx
            history.append(x_new)

            if abs(x_new - x) < tol:
                return x_new, i + 1, history

            x = x_new

        return x, max_iter, history

    @staticmethod
    def fixed_point_method(g: Callable, x0: float, tol: float = 1e-6,
                          max_iter: int = 100) -> Tuple[float, int, List[float]]:
        """
        Método de punto fijo para resolver x = g(x)

        Args:
            g: Función de iteración g(x)
            x0: Aproximación inicial
            tol: Tolerancia
            max_iter: Máximo número de iteraciones

        Returns:
            Tupla (punto_fijo, iteraciones, historial)
        """
        x = x0
        history = [x0]

        for i in range(max_iter):
            x_new = g(x)
            history.append(x_new)

            if abs(x_new - x) < tol:
                return x_new, i + 1, history

            x = x_new

        return x, max_iter, history

    # Alias para compatibilidad
    fixed_point = fixed_point_method
