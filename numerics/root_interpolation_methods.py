"""
Módulo de Métodos de Interpolación para Raíces
Implementa métodos de interpolación relacionados con raíces

Métodos incluidos:
- Interpolación de Lagrange
- Polinomio de Lagrange
"""

import numpy as np
from typing import Callable

class RootInterpolationMethods:
    """
    Clase que encapsula métodos de interpolación para análisis de raíces
    """

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
    def lagrange_polynomial(x_points: np.ndarray, y_points: np.ndarray) -> Callable:
        """
        Genera el polinomio de interpolación de Lagrange como función

        Args:
            x_points: Puntos x conocidos
            y_points: Puntos y conocidos

        Returns:
            Función que evalúa el polinomio de Lagrange
        """
        def polynomial(x):
            return RootInterpolationMethods.lagrange_interpolation(x_points, y_points, x)

        return polynomial
