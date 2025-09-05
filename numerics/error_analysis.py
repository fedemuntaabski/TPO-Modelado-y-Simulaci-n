"""
Módulo de Análisis de Errores
Herramientas para análisis de errores numéricos y estabilidad

Métodos incluidos:
- Cálculo de errores absoluto y relativo
- Estimación de orden de convergencia
- Análisis de estabilidad numérica
"""

import numpy as np
from typing import Callable, List

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
