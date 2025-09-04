"""
Módulo de Métodos para Encontrar Raíces
Implementa algoritmos para encontrar raíces de ecuaciones no lineales

Métodos incluidos:
- Bisección
- Newton-Raphson
- Punto fijo
- Aceleración de Aitken
- Interpolación de Lagrange
"""

import numpy as np
from typing import Callable, Tuple, List

class RootMethods:
    """
    Clase que encapsula métodos para encontrar raíces de ecuaciones
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

    @staticmethod
    def aitken_acceleration(sequence: List[float]) -> List[float]:
        """
        Aceleración de Aitken para mejorar convergencia

        Args:
            sequence: Secuencia de aproximaciones

        Returns:
            Secuencia acelerada
        """
        if len(sequence) < 3:
            return sequence

        accelerated = []
        for i in range(len(sequence) - 2):
            x_n = sequence[i]
            x_n1 = sequence[i + 1]
            x_n2 = sequence[i + 2]

            denominator = x_n2 - 2*x_n1 + x_n
            if abs(denominator) > 1e-14:
                x_acc = x_n - (x_n1 - x_n)**2 / denominator
                accelerated.append(x_acc)
            else:
                accelerated.append(x_n2)

        return accelerated

    @staticmethod
    def aitken_method(g, x0: float, tol: float = 1e-6, max_iter: int = 100):
        """
        Método de Aitken para encontrar raíces usando función de iteración

        Args:
            g: Función de iteración g(x)
            x0: Aproximación inicial
            tol: Tolerancia para convergencia
            max_iter: Máximo número de iteraciones

        Returns:
            Tupla: (raíz, iteraciones, historial, historial_acelerado, pasos_detallados)
            historial_acelerado: Lista de valores después de aplicar Aitken
            pasos_detallados: Lista de diccionarios con información detallada de cada paso
        """
        history = [x0]  # Valores originales de g(x)
        accelerated_history = []  # Valores después de aplicar Aitken
        detailed_steps = []  # Información detallada de cada paso

        x = x0

        for iteration in range(max_iter):
            # Generar nuevo valor usando g(x)
            x_new = g(x)

            # Registrar paso detallado
            step_info = {
                'iteracion': iteration + 1,
                'x_anterior': x,
                'g_x_anterior': x_new,
                'x0_x1_x2': None,  # Se llenará cuando tengamos suficientes puntos
                'x_acelerado': None,
                'error_abs': None,
                'error_rel': None
            }

            history.append(x_new)

            # Aplicar aceleración de Aitken si tenemos suficientes puntos
            if len(history) >= 3:
                # Aplicar Aitken a los últimos 3 puntos
                last_three = history[-3:]
                step_info['x0_x1_x2'] = last_three.copy()

                accelerated = RootMethods.aitken_acceleration(last_three)

                if accelerated:
                    x_acc = accelerated[-1]  # Último valor acelerado
                    step_info['x_acelerado'] = x_acc
                    accelerated_history.append(x_acc)

                    # Calcular errores
                    step_info['error_abs'] = abs(x_acc - x)
                    step_info['error_rel'] = abs(x_acc - x) / abs(x_acc) if abs(x_acc) > 1e-14 else 0

                    # Verificar convergencia con el valor acelerado
                    if abs(x_acc - x) < tol:
                        detailed_steps.append(step_info)
                        return x_acc, iteration + 1, history, accelerated_history, detailed_steps

                    x = x_acc
                else:
                    x = x_new
            else:
                x = x_new

            detailed_steps.append(step_info)

            # Verificar convergencia sin aceleración
            if abs(x - history[-2]) < tol and len(history) > 1:
                return x, iteration + 1, history, accelerated_history, detailed_steps

        # Si no converge, devolver último valor
        return x, max_iter, history, accelerated_history, detailed_steps

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
            return RootMethods.lagrange_interpolation(x_points, y_points, x)

        return polynomial
