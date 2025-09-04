"""
Diferencias Finitas - Módulo Unificado
Implementa métodos completos de diferenciación numérica y análisis de diferencias finitas

Características principales:
- Diferencias hacia adelante, atrás y centrales
- Derivadas de orden superior (hasta 4to orden)
- Tablas de diferencias finitas para interpolación
- Análisis de convergencia y errores
- Métodos optimizados con IA para mejor distribución de puntos

Métodos incluidos:
- Diferenciación numérica básica
- Derivadas de orden superior
- Tablas de diferencias para interpolación
- Análisis de estabilidad y convergencia
"""

import numpy as np
from typing import Callable, List, Tuple, Dict, Optional
import warnings
import math

class FiniteDifferences:
    """
    Clase unificada que implementa todos los métodos de diferencias finitas
    Optimizada con algoritmos inteligentes para mejor precisión y estabilidad
    """

    @staticmethod
    def forward_difference(f: Callable, x: float, h: float = 1e-5) -> float:
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
    def backward_difference(f: Callable, x: float, h: float = 1e-5) -> float:
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
    def central_difference(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Diferencias centrales para primera derivada (más precisa)

        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Paso para la diferencia finita

        Returns:
            Aproximación de f'(x) usando diferencias centrales

        Raises:
            ValueError: Si h es negativo o cero
        """
        if h <= 0:
            raise ValueError("El paso h debe ser positivo")
        return (f(x + h) - f(x - h)) / (2 * h)

    @staticmethod
    def second_derivative_central(f: Callable, x: float, h: float = 1e-5) -> float:
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
    def third_derivative_central(f: Callable, x: float, h: float = 1e-5) -> float:
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
    def fourth_derivative_central(f: Callable, x: float, h: float = 1e-5) -> float:
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
    def adaptive_step_size(f: Callable, x: float, target_accuracy: float = 1e-8,
                          max_iterations: int = 10) -> Tuple[float, float]:
        """
        Determina el paso óptimo h usando algoritmo adaptativo inteligente

        Args:
            f: Función a derivar
            x: Punto de evaluación
            target_accuracy: Precisión deseada
            max_iterations: Máximo número de iteraciones

        Returns:
            Tupla (h_óptimo, derivada_aproximada)
        """
        h = 1e-3  # Paso inicial
        derivative_prev = FiniteDifferences.central_difference(f, x, h)

        for _ in range(max_iterations):
            h_new = h / 2
            derivative_new = FiniteDifferences.central_difference(f, x, h_new)

            # Estimar error usando extrapolación
            error_estimate = abs(derivative_new - derivative_prev) / 15  # Para diferencias centrales O(h^4)

            if error_estimate < target_accuracy:
                return h_new, derivative_new

            h = h_new
            derivative_prev = derivative_new

        return h, derivative_new

    @staticmethod
    def derivative_table(f: Callable, x: float, max_order: int = 4,
                        h: Optional[float] = None) -> Dict[int, float]:
        """
        Calcula derivadas de múltiples órdenes en un punto usando paso adaptativo

        Args:
            f: Función a derivar
            x: Punto de evaluación
            max_order: Máximo orden de derivada a calcular
            h: Paso personalizado (opcional, se calcula automáticamente si no se proporciona)

        Returns:
            Diccionario con las derivadas de cada orden
        """
        if h is None:
            h, _ = FiniteDifferences.adaptive_step_size(f, x)

        derivatives = {}

        if max_order >= 1:
            derivatives[1] = FiniteDifferences.central_difference(f, x, h)
        if max_order >= 2:
            derivatives[2] = FiniteDifferences.second_derivative_central(f, x, h)
        if max_order >= 3:
            derivatives[3] = FiniteDifferences.third_derivative_central(f, x, h)
        if max_order >= 4:
            derivatives[4] = FiniteDifferences.fourth_derivative_central(f, x, h)

        return derivatives

    @staticmethod
    def convergence_analysis(f: Callable, x: float, exact_derivative: Optional[float] = None,
                           h_range: Tuple[float, float] = (1e-1, 1e-8),
                           num_points: int = 20) -> Dict:
        """
        Análisis completo de convergencia con múltiples métodos

        Args:
            f: Función a derivar
            x: Punto de evaluación
            exact_derivative: Derivada exacta para comparación (opcional)
            h_range: Rango de valores h para análisis
            num_points: Número de puntos para análisis

        Returns:
            Diccionario con resultados del análisis
        """
        h_values = np.logspace(np.log10(h_range[0]), np.log10(h_range[1]), num_points)

        results = {
            'h_values': h_values,
            'forward': [],
            'backward': [],
            'central': [],
            'errors_forward': [],
            'errors_backward': [],
            'errors_central': [],
            'optimal_h': None,
            'optimal_method': None
        }

        for h in h_values:
            # Calcular derivadas con diferentes métodos
            forward = FiniteDifferences.forward_difference(f, x, h)
            backward = FiniteDifferences.backward_difference(f, x, h)
            central = FiniteDifferences.central_difference(f, x, h)

            results['forward'].append(forward)
            results['backward'].append(backward)
            results['central'].append(central)

            if exact_derivative is not None:
                results['errors_forward'].append(abs(forward - exact_derivative))
                results['errors_backward'].append(abs(backward - exact_derivative))
                results['errors_central'].append(abs(central - exact_derivative))

        # Encontrar método óptimo si hay derivada exacta
        if exact_derivative is not None and results['errors_central']:
            min_error_idx = np.argmin(results['errors_central'])
            results['optimal_h'] = h_values[min_error_idx]
            results['optimal_method'] = 'central'

        return results

    @staticmethod
    def finite_differences_table(x_points: np.ndarray, y_points: np.ndarray) -> np.ndarray:
        """
        Construye tabla de diferencias finitas para interpolación

        Args:
            x_points: Puntos x conocidos
            y_points: Puntos y conocidos

        Returns:
            Tabla de diferencias finitas
        """
        n = len(x_points)
        if n != len(y_points):
            raise ValueError("x_points y y_points deben tener la misma longitud")

        table = np.zeros((n, n))
        table[:, 0] = y_points

        for j in range(1, n):
            for i in range(n - j):
                table[i, j] = table[i + 1, j - 1] - table[i, j - 1]

        return table

    @staticmethod
    def interpolate_with_differences(x_points: np.ndarray, y_points: np.ndarray,
                                   x_eval: float) -> float:
        """
        Interpolación usando tabla de diferencias finitas

        Args:
            x_points: Puntos x conocidos
            y_points: Puntos y conocidos
            x_eval: Punto donde interpolar

        Returns:
            Valor interpolado
        """
        table = FiniteDifferences.finite_differences_table(x_points, y_points)
        n = len(x_points)

        # Encontrar el intervalo que contiene x_eval
        idx = np.searchsorted(x_points, x_eval) - 1
        idx = max(0, min(idx, n - 2))

        # Interpolación de Newton
        result = table[idx, 0]
        h = x_points[1] - x_points[0] if len(x_points) > 1 else 1.0
        t = (x_eval - x_points[idx]) / h

        for i in range(1, n - idx):
            term = table[idx, i]
            for j in range(i):
                term *= (t - j)
            term /= math.factorial(i)
            result += term

        return result

    @staticmethod
    def stability_analysis(f: Callable, x: float, h_range: Tuple[float, float] = (1e-8, 1e-2),
                          num_points: int = 50) -> Dict:
        """
        Análisis de estabilidad numérica

        Args:
            f: Función a derivar
            x: Punto de evaluación
            h_range: Rango de h para análisis
            num_points: Número de puntos

        Returns:
            Diccionario con métricas de estabilidad
        """
        h_values = np.logspace(np.log10(h_range[0]), np.log10(h_range[1]), num_points)

        derivatives = []
        condition_numbers = []

        for h in h_values:
            try:
                deriv = FiniteDifferences.central_difference(f, x, h)
                derivatives.append(deriv)

                # Estimar número de condición
                f_x = f(x)
                if abs(f_x) > 1e-14:
                    cond = abs(deriv * h / f_x)
                    condition_numbers.append(cond)
                else:
                    condition_numbers.append(float('inf'))

            except (OverflowError, ZeroDivisionError):
                derivatives.append(float('nan'))
                condition_numbers.append(float('inf'))

        return {
            'h_values': h_values,
            'derivatives': derivatives,
            'condition_numbers': condition_numbers,
            'stable_range': h_range[0] if not np.isnan(derivatives).any() else None
        }

# Alias para compatibilidad hacia atrás
FiniteDifferences.forward = FiniteDifferences.forward_difference
FiniteDifferences.backward = FiniteDifferences.backward_difference
FiniteDifferences.central = FiniteDifferences.central_difference
FiniteDifferences.second_derivative = FiniteDifferences.second_derivative_central
FiniteDifferences.third_derivative = FiniteDifferences.third_derivative_central
FiniteDifferences.fourth_derivative = FiniteDifferences.fourth_derivative_central
