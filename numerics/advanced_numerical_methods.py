"""
Módulo de Métodos Numéricos Avanzados
Implementa extrapolación de Richardson, cuadratura adaptativa y aceleración de Aitken

Métodos incluidos:
- Extrapolación de Richardson
- Cuadratura adaptativa
- Aceleración de Aitken
- Eliminación gaussiana
"""

import numpy as np
from typing import Callable, List, Tuple

class AdvancedNumericalMethods:
    """
    Métodos numéricos avanzados para análisis y resolución
    """
    
    @staticmethod
    def richardson_extrapolation(f: Callable, x: float, h_values: List[float]) -> Tuple[float, List[float]]:
        """
        Extrapolación de Richardson para mejorar aproximaciones de derivadas
        
        Args:
            f: Función
            x: Punto de evaluación
            h_values: Lista de pasos h (en orden decreciente)
            
        Returns:
            Tupla (mejor_aproximacion, tabla_richardson)
        """
        n = len(h_values)
        R = np.zeros((n, n))
        
        # Primera columna: aproximaciones básicas
        for i in range(n):
            h = h_values[i]
            R[i, 0] = (f(x + h) - f(x - h)) / (2 * h)
        
        # Aplicar extrapolación de Richardson
        for j in range(1, n):
            for i in range(n - j):
                R[i, j] = R[i + 1, j - 1] + (R[i + 1, j - 1] - R[i, j - 1]) / (4**j - 1)
        
        return R[0, n - 1], R.tolist()
    
    @staticmethod
    def adaptive_quadrature(f: Callable, a: float, b: float, tol: float = 1e-6) -> Tuple[float, int]:
        """
        Cuadratura adaptativa usando regla de Simpson
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            tol: Tolerancia deseada
            
        Returns:
            Tupla (integral_aproximada, evaluaciones_funcion)
        """
        def simpson(a, b):
            """Regla de Simpson para un intervalo"""
            c = (a + b) / 2
            return (b - a) / 6 * (f(a) + 4*f(c) + f(b))
        
        def adaptive_simpson_recursive(a, b, tol, S, fa, fb, fc, depth=0):
            """Función recursiva para cuadratura adaptativa"""
            if depth > 50:  # Evitar recursión infinita
                return S, 3
            
            c = (a + b) / 2
            d = (a + c) / 2
            e = (c + b) / 2
            
            fd = f(d)
            fe = f(e)
            
            S_left = (c - a) / 6 * (fa + 4*fd + fc)
            S_right = (b - c) / 6 * (fc + 4*fe + fb)
            S_new = S_left + S_right
            
            evaluations = 2  # Para fd y fe
            
            if abs(S_new - S) <= 15 * tol:
                return S_new + (S_new - S) / 15, evaluations
            else:
                left_result, left_evals = adaptive_simpson_recursive(
                    a, c, tol/2, S_left, fa, fc, fd, depth + 1
                )
                right_result, right_evals = adaptive_simpson_recursive(
                    c, b, tol/2, S_right, fc, fb, fe, depth + 1
                )
                return left_result + right_result, evaluations + left_evals + right_evals
        
        # Valores iniciales
        c = (a + b) / 2
        fa, fb, fc = f(a), f(b), f(c)
        S = simpson(a, b)
        
        result, evals = adaptive_simpson_recursive(a, b, tol, S, fa, fb, fc)
        return result, evals + 3  # +3 por las evaluaciones iniciales
    
    @staticmethod
    def gaussian_elimination(A: List[List[float]], b: List[float]) -> List[float]:
        """
        Eliminación gaussiana para resolver sistemas lineales
        
        Args:
            A: Matriz de coeficientes
            b: Vector de términos independientes
            
        Returns:
            Vector solución
        """
        n = len(A)
        # Crear matriz aumentada
        augmented = [row[:] + [b[i]] for i, row in enumerate(A)]
        
        # Eliminación hacia adelante
        for i in range(n):
            # Encontrar pivote
            pivot_row = i
            for j in range(i + 1, n):
                if abs(augmented[j][i]) > abs(augmented[pivot_row][i]):
                    pivot_row = j
            
            # Intercambiar filas
            augmented[i], augmented[pivot_row] = augmented[pivot_row], augmented[i]
            
            # Verificar si el pivote es cero (matriz singular)
            if abs(augmented[i][i]) < 1e-14:
                raise ValueError("La matriz es singular o casi singular")
            
            # Hacer ceros debajo del pivote
            for j in range(i + 1, n):
                factor = augmented[j][i] / augmented[i][i]
                for k in range(i, n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
        
        # Sustitución hacia atrás
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = augmented[i][n]
            for j in range(i + 1, n):
                x[i] -= augmented[i][j] * x[j]
            x[i] /= augmented[i][i]
        
        return x
    
    @staticmethod
    def aitken_acceleration(sequence: List[float]) -> List[float]:
        """
        Aplica aceleración de Aitken a una secuencia
        
        Args:
            sequence: Secuencia original
            
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
    def aitken_acceleration_detailed(sequence: List[float]) -> Tuple[List[float], List[float]]:
        """
        Aplica aceleración de Aitken con análisis detallado
        
        Args:
            sequence: Secuencia original
            
        Returns:
            Tupla (secuencia_acelerada, errores_relativos)
        """
        if len(sequence) < 3:
            return sequence, []
        
        accelerated = []
        relative_errors = []
        
        for i in range(len(sequence) - 2):
            x_n = sequence[i]
            x_n1 = sequence[i + 1]
            x_n2 = sequence[i + 2]
            
            denominator = x_n2 - 2*x_n1 + x_n
            
            if abs(denominator) > 1e-14:
                x_acc = x_n - (x_n1 - x_n)**2 / denominator
                accelerated.append(x_acc)
                
                # Calcular error relativo si es posible
                if i < len(sequence) - 3:
                    next_acc = sequence[i + 1] - (x_n2 - x_n1)**2 / (sequence[i + 3] - 2*x_n2 + x_n1) if i + 3 < len(sequence) else x_acc
                    if abs(x_acc) > 1e-14:
                        relative_error = abs(next_acc - x_acc) / abs(x_acc)
                        relative_errors.append(relative_error)
            else:
                accelerated.append(x_n2)
                relative_errors.append(0)
        
        return accelerated, relative_errors
