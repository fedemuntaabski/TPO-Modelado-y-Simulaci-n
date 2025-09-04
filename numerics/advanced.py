"""
Módulo de Interpolación y Métodos Adicionales
Implementa interpolación de Lagrange, diferencias finitas y aceleración de Aitken

Métodos incluidos:
- Interpolación de Lagrange
- Diferencias finitas centrales para derivadas
- Aceleración de convergencia de Aitken
- Métodos auxiliares para análisis numérico
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

class AdvancedNumericalMethods:
    """
    Métodos numéricos adicionales y análisis avanzado
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

class AdvancedNumericalMethods:
    """
    Métodos numéricos avanzados para análisis y resolución
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

# Funciones de utilidad para análisis de errores
class ErrorAnalysis:
    """
    Herramientas para análisis de errores numéricos
    """
    
    @staticmethod
    def relative_error(exact: float, approximate: float) -> float:
        """Calcula el error relativo"""
        if abs(exact) < 1e-14:
            return abs(approximate)
        return abs(exact - approximate) / abs(exact)
    
    @staticmethod
    def absolute_error(exact: float, approximate: float) -> float:
        """Calcula el error absoluto"""
        return abs(exact - approximate)
    
    @staticmethod
    def convergence_order(errors: List[float], h_values: List[float]) -> float:
        """
        Estima el orden de convergencia usando regresión logarítmica
        
        Args:
            errors: Lista de errores
            h_values: Lista de pasos correspondientes
            
        Returns:
            Orden de convergencia estimado
        """
        if len(errors) < 2 or len(h_values) < 2:
            return 0
        
        # Usar regresión logarítmica: log(error) = p*log(h) + c
        log_h = np.log(h_values)
        log_errors = np.log(errors)
        
        # Ajuste lineal
        coeffs = np.polyfit(log_h, log_errors, 1)
        return coeffs[0]  # El coeficiente de log(h) es el orden
    
    @staticmethod
    def estimate_bisection_error(a: float, b: float) -> float:
        """
        Estima el error en el método de bisección
        
        Args:
            a: Límite inferior
            b: Límite superior
            
        Returns:
            Error estimado
        """
        return abs(b - a) / 2
    
    @staticmethod
    def analyze_convergence_rate(errors: List[float]) -> float:
        """
        Analiza la tasa de convergencia de una secuencia de errores
        Asume que h se reduce a la mitad cada vez
        
        Args:
            errors: Lista de errores
            
        Returns:
            Orden de convergencia estimado
        """
        if len(errors) < 2:
            return 0
        
        ratios = []
        for i in range(1, len(errors)):
            if errors[i-1] != 0:
                ratios.append(errors[i] / errors[i-1])
        
        if not ratios:
            return 0
        
        avg_ratio = np.mean(ratios)
        if avg_ratio <= 0 or avg_ratio >= 1:
            return 0
        
        # Asumiendo h_{n+1}/h_n = 0.5
        h_ratio = 0.5
        if abs(np.log(h_ratio)) > 1e-14:
            order = np.log(avg_ratio) / np.log(h_ratio)
            return order
        return 0
    
    @staticmethod
    def check_numerical_stability(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Verifica la estabilidad numérica de una función en un punto
        Retorna un score de estabilidad (mayor es mejor)
        
        Args:
            f: Función a evaluar
            x: Punto de evaluación
            h: Paso pequeño
            
        Returns:
            Score de estabilidad (0 a 1)
        """
        try:
            f_x = f(x)
            f_x_plus_h = f(x + h)
            f_x_minus_h = f(x - h)
            
            # Verificar que no hay NaN o inf
            if not (np.isfinite(f_x) and np.isfinite(f_x_plus_h) and np.isfinite(f_x_minus_h)):
                return 0.0
            
            # Calcular derivada
            derivative = (f_x_plus_h - f_x_minus_h) / (2 * h)
            if not np.isfinite(derivative):
                return 0.0
            
            # Score basado en la magnitud de la derivada
            # Mayor derivada = menor estabilidad
            stability = 1.0 / (1.0 + abs(derivative))
            return stability
        except:
            return 0.0
