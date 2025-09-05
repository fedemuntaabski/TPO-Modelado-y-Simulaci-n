"""
Módulo de Métodos de Aceleración para Raíces
Implementa algoritmos de aceleración para mejorar convergencia

Métodos incluidos:
- Aceleración de Aitken
- Método de Aitken para raíces
"""

import numpy as np
from typing import Callable, Tuple, List

class RootAccelerationMethods:
    """
    Clase que encapsula métodos de aceleración para encontrar raíces
    """

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

                accelerated = RootAccelerationMethods.aitken_acceleration(last_three)

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
