"""
Módulo de Métodos Numéricos Core
Implementa algoritmos básicos de integración, derivación y ecuaciones diferenciales

Métodos incluidos:
- Ecuaciones diferenciales (Runge-Kutta, Euler)
- Integración numérica (Trapezoidal, Simpson)
- Derivación numérica (diferencias finitas)
"""

import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import fsolve
import sympy as sp
from typing import Callable, Tuple, List, Optional

class NumericalMethods:
    """
    Clase que encapsula métodos numéricos básicos
    """

    @staticmethod
    def runge_kutta_4(f: Callable, t_span: Tuple[float, float], y0: float,
                     n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resuelve una ecuación diferencial usando Runge-Kutta de 4to orden

        Args:
            f: Función f(t, y) que define dy/dt = f(t, y)
            t_span: Tupla (t0, tf) con el intervalo de tiempo
            y0: Condición inicial y(t0) = y0
            n_points: Número de puntos de evaluación

        Returns:
            Tupla (t, y) con los puntos de la solución
        """
        t0, tf = t_span
        h = (tf - t0) / (n_points - 1)
        t = np.linspace(t0, tf, n_points)
        y = np.zeros(n_points)
        y[0] = y0

        for i in range(n_points - 1):
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + k1/2)
            k3 = h * f(t[i] + h/2, y[i] + k2/2)
            k4 = h * f(t[i] + h, y[i] + k3)

            y[i+1] = y[i] + (k1 + 2*k2 + 2*k3 + k4) / 6

        return t, y

    @staticmethod
    def euler_method(f: Callable, t_span: Tuple[float, float], y0: float,
                    n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resuelve una ecuación diferencial usando el método de Euler

        Args:
            f: Función f(t, y) que define dy/dt = f(t, y)
            t_span: Tupla (t0, tf) con el intervalo de tiempo
            y0: Condición inicial y(t0) = y0
            n_points: Número de puntos de evaluación

        Returns:
            Tupla (t, y) con los puntos de la solución
        """
        t0, tf = t_span
        h = (tf - t0) / (n_points - 1)
        t = np.linspace(t0, tf, n_points)
        y = np.zeros(n_points)
        y[0] = y0

        for i in range(n_points - 1):
            y[i+1] = y[i] + h * f(t[i], y[i])

        return t, y

    @staticmethod
    def trapezoidal_rule(f: Callable, a: float, b: float, n: int = 100) -> float:
        """
        Regla del trapecio para integración numérica

        Args:
            f: Función a integrar
            a: Límite inferior
            b: Límite superior
            n: Número de intervalos

        Returns:
            Aproximación de la integral
        """
        h = (b - a) / n
        x = np.linspace(a, b, n+1)
        y = f(x)

        integral = h * (0.5*y[0] + 0.5*y[-1] + np.sum(y[1:-1]))

        return integral

    @staticmethod
    def simpson_rule(f: Callable, a: float, b: float, n: int = 100) -> float:
        """
        Regla de Simpson para integración numérica

        Args:
            f: Función a integrar
            a: Límite inferior
            b: Límite superior
            n: Número de intervalos (debe ser par)

        Returns:
            Aproximación de la integral
        """
        if n % 2 != 0:
            n += 1  # Asegurar que n sea par

        h = (b - a) / n
        x = np.linspace(a, b, n+1)
        y = f(x)

        integral = h/3 * (y[0] + y[-1] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-1:2]))

        return integral

    @staticmethod
    def central_difference(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Derivada numérica usando diferencias centrales

        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Tamaño del paso

        Returns:
            Aproximación de f'(x)
        """
        return (f(x + h) - f(x - h)) / (2 * h)

    @staticmethod
    def forward_difference(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Derivada numérica usando diferencias hacia adelante

        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Tamaño del paso

        Returns:
            Aproximación de f'(x)
        """
        return (f(x + h) - f(x)) / h

    @staticmethod
    def backward_difference(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Derivada numérica usando diferencias hacia atrás

        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Tamaño del paso

        Returns:
            Aproximación de f'(x)
        """
        return (f(x) - f(x - h)) / h

    @staticmethod
    def second_derivative(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Segunda derivada numérica usando diferencias centrales

        Args:
            f: Función a derivar
            x: Punto donde evaluar la segunda derivada
            h: Tamaño del paso

        Returns:
            Aproximación de f''(x)
        """
        return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)

    @staticmethod
    def richardson_extrapolation(f: Callable, x: float, h: float = 1e-2,
                                order: int = 2) -> float:
        """
        Extrapolación de Richardson para mejorar precisión de derivadas

        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Tamaño del paso inicial
            order: Orden de la derivada

        Returns:
            Aproximación mejorada de f'(x)
        """
        if order == 1:
            d1 = NumericalMethods.forward_difference(f, x, h)
            d2 = NumericalMethods.forward_difference(f, x, h/2)
            return (4*d2 - d1) / 3
        elif order == 2:
            d1 = NumericalMethods.second_derivative(f, x, h)
            d2 = NumericalMethods.second_derivative(f, x, h/2)
            return (4*d2 - d1) / 3
        else:
            raise ValueError("Orden no soportado")

    @staticmethod
    def solve_ivp_scipy(f: Callable, t_span: Tuple[float, float], y0: float,
                       method: str = 'RK45') -> Tuple[np.ndarray, np.ndarray]:
        """
        Resuelve EDO usando scipy.integrate.solve_ivp

        Args:
            f: Función f(t, y)
            t_span: Intervalo de tiempo (t0, tf)
            y0: Condición inicial
            method: Método de integración ('RK45', 'RK23', 'DOP853', etc.)

        Returns:
            Tupla (t, y) con la solución
        """
        def rhs(t, y):
            return f(t, y[0])

        sol = solve_ivp(rhs, t_span, [y0], method=method, dense_output=True)

        t_eval = np.linspace(t_span[0], t_span[1], 100)
        y_eval = sol.sol(t_eval)

        return t_eval, y_eval[0]

    @staticmethod
    def integrate_scipy(f: Callable, a: float, b: float) -> float:
        """
        Integra usando scipy.integrate.quad

        Args:
            f: Función a integrar
            a: Límite inferior
            b: Límite superior

        Returns:
            Valor de la integral
        """
        result, _ = quad(f, a, b)
        return result
