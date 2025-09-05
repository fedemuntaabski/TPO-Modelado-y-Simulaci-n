"""
Métodos de diferencias finitas para cálculo de derivadas numéricas.

Implementa algoritmos de diferenciación numérica siguiendo principios SOLID y DRY.
Cada método mantiene responsabilidad única y está optimizado para precisión y rendimiento.
"""

import numpy as np
from typing import Callable, Tuple, List, Optional, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)


class DerivativeResult:
    """Resultado del cálculo de derivadas siguiendo el principio de encapsulación"""
    
    def __init__(self, value: float, method: str, order: int, step_size: float,
                 point: float, exact_value: Optional[float] = None,
                 formula: str = "", error_order: str = "",
                 computation_data: Optional[Dict] = None):
        self.value = value
        self.method = method
        self.order = order
        self.step_size = step_size
        self.point = point
        self.exact_value = exact_value
        self.formula = formula
        self.error_order = error_order
        self.computation_data = computation_data or {}
        
        # Calcular errores si hay valor exacto
        if exact_value is not None:
            self.absolute_error = abs(value - exact_value)
            if exact_value != 0:
                self.relative_error = abs(self.absolute_error / exact_value) * 100
            else:
                self.relative_error = 0
        else:
            self.absolute_error = None
            self.relative_error = None


class FiniteDifferenceCalculator:
    """
    Calculadora de diferencias finitas.
    Sigue el principio de responsabilidad única (SRP) del SOLID.
    """
    
    def __init__(self, high_precision_h: float = 1e-8):
        self.high_precision_h = high_precision_h
    
    def forward_difference(self, f: Callable[[float], float], 
                          x0: float, h: float, order: int = 1) -> DerivativeResult:
        """
        Diferencias finitas hacia adelante.
        
        Args:
            f: Función a derivar
            x0: Punto de evaluación
            h: Tamaño de paso
            order: Orden de la derivada (1, 2, o 3)
            
        Returns:
            DerivativeResult con información completa
        """
        if order == 1:
            # f'(x) ≈ [f(x+h) - f(x)] / h
            derivative = (f(x0 + h) - f(x0)) / h
            formula = "f'(x) ≈ [f(x+h) - f(x)] / h"
            points_used = [x0, x0 + h]
            
        elif order == 2:
            # f''(x) ≈ [f(x+2h) - 2f(x+h) + f(x)] / h²
            derivative = (f(x0 + 2*h) - 2*f(x0 + h) + f(x0)) / (h**2)
            formula = "f''(x) ≈ [f(x+2h) - 2f(x+h) + f(x)] / h²"
            points_used = [x0, x0 + h, x0 + 2*h]
            
        elif order == 3:
            # f'''(x) ≈ [f(x+3h) - 3f(x+2h) + 3f(x+h) - f(x)] / h³
            derivative = (f(x0 + 3*h) - 3*f(x0 + 2*h) + 3*f(x0 + h) - f(x0)) / (h**3)
            formula = "f'''(x) ≈ [f(x+3h) - 3f(x+2h) + 3f(x+h) - f(x)] / h³"
            points_used = [x0, x0 + h, x0 + 2*h, x0 + 3*h]
            
        else:
            raise ValueError(f"Orden {order} no soportado. Use 1, 2, o 3.")
        
        # Calcular valor exacto usando alta precisión
        exact_value = self._compute_exact_derivative(f, x0, order)
        
        computation_data = {
            'points_used': points_used,
            'function_evaluations': [f(x) for x in points_used],
            'coefficients': self._get_forward_coefficients(order),
            'step_size_power': order
        }
        
        return DerivativeResult(
            value=derivative,
            method="Diferencias Hacia Adelante",
            order=order,
            step_size=h,
            point=x0,
            exact_value=exact_value,
            formula=formula,
            error_order="O(h)",
            computation_data=computation_data
        )
    
    def backward_difference(self, f: Callable[[float], float],
                           x0: float, h: float, order: int = 1) -> DerivativeResult:
        """
        Diferencias finitas hacia atrás.
        """
        if order == 1:
            # f'(x) ≈ [f(x) - f(x-h)] / h
            derivative = (f(x0) - f(x0 - h)) / h
            formula = "f'(x) ≈ [f(x) - f(x-h)] / h"
            points_used = [x0 - h, x0]
            
        elif order == 2:
            # f''(x) ≈ [f(x) - 2f(x-h) + f(x-2h)] / h²
            derivative = (f(x0) - 2*f(x0 - h) + f(x0 - 2*h)) / (h**2)
            formula = "f''(x) ≈ [f(x) - 2f(x-h) + f(x-2h)] / h²"
            points_used = [x0 - 2*h, x0 - h, x0]
            
        elif order == 3:
            # f'''(x) ≈ [f(x) - 3f(x-h) + 3f(x-2h) - f(x-3h)] / h³
            derivative = (f(x0) - 3*f(x0 - h) + 3*f(x0 - 2*h) - f(x0 - 3*h)) / (h**3)
            formula = "f'''(x) ≈ [f(x) - 3f(x-h) + 3f(x-2h) - f(x-3h)] / h³"
            points_used = [x0 - 3*h, x0 - 2*h, x0 - h, x0]
            
        else:
            raise ValueError(f"Orden {order} no soportado. Use 1, 2, o 3.")
        
        exact_value = self._compute_exact_derivative(f, x0, order)
        
        computation_data = {
            'points_used': points_used,
            'function_evaluations': [f(x) for x in points_used],
            'coefficients': self._get_backward_coefficients(order),
            'step_size_power': order
        }
        
        return DerivativeResult(
            value=derivative,
            method="Diferencias Hacia Atrás",
            order=order,
            step_size=h,
            point=x0,
            exact_value=exact_value,
            formula=formula,
            error_order="O(h)",
            computation_data=computation_data
        )
    
    def central_difference(self, f: Callable[[float], float],
                          x0: float, h: float, order: int = 1) -> DerivativeResult:
        """
        Diferencias finitas centrales (mayor precisión).
        """
        if order == 1:
            # f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
            derivative = (f(x0 + h) - f(x0 - h)) / (2 * h)
            formula = "f'(x) ≈ [f(x+h) - f(x-h)] / (2h)"
            points_used = [x0 - h, x0 + h]
            
        elif order == 2:
            # f''(x) ≈ [f(x+h) - 2f(x) + f(x-h)] / h²
            derivative = (f(x0 + h) - 2*f(x0) + f(x0 - h)) / (h**2)
            formula = "f''(x) ≈ [f(x+h) - 2f(x) + f(x-h)] / h²"
            points_used = [x0 - h, x0, x0 + h]
            
        elif order == 3:
            # f'''(x) ≈ [f(x+2h) - 2f(x+h) + 2f(x-h) - f(x-2h)] / (2h³)
            derivative = (f(x0 + 2*h) - 2*f(x0 + h) + 2*f(x0 - h) - f(x0 - 2*h)) / (2 * h**3)
            formula = "f'''(x) ≈ [f(x+2h) - 2f(x+h) + 2f(x-h) - f(x-2h)] / (2h³)"
            points_used = [x0 - 2*h, x0 - h, x0 + h, x0 + 2*h]
            
        else:
            raise ValueError(f"Orden {order} no soportado. Use 1, 2, o 3.")
        
        exact_value = self._compute_exact_derivative(f, x0, order)
        
        computation_data = {
            'points_used': points_used,
            'function_evaluations': [f(x) for x in points_used],
            'coefficients': self._get_central_coefficients(order),
            'step_size_power': order if order > 1 else 2  # Central tiene O(h²) para primera derivada
        }
        
        return DerivativeResult(
            value=derivative,
            method="Diferencias Centrales",
            order=order,
            step_size=h,
            point=x0,
            exact_value=exact_value,
            formula=formula,
            error_order="O(h²)" if order == 1 else "O(h²)",
            computation_data=computation_data
        )
    
    def five_point_central(self, f: Callable[[float], float],
                          x0: float, h: float, order: int = 1) -> DerivativeResult:
        """
        Diferencias centrales de 5 puntos (mayor precisión).
        Principio de extensibilidad del SOLID.
        """
        if order == 1:
            # f'(x) ≈ [-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)] / (12h)
            derivative = (-f(x0 + 2*h) + 8*f(x0 + h) - 8*f(x0 - h) + f(x0 - 2*h)) / (12*h)
            formula = "f'(x) ≈ [-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)] / (12h)"
            error_order = "O(h⁴)"
            
        elif order == 2:
            # f''(x) ≈ [-f(x+2h) + 16f(x+h) - 30f(x) + 16f(x-h) - f(x-2h)] / (12h²)
            derivative = (-f(x0 + 2*h) + 16*f(x0 + h) - 30*f(x0) + 16*f(x0 - h) - f(x0 - 2*h)) / (12*h**2)
            formula = "f''(x) ≈ [-f(x+2h) + 16f(x+h) - 30f(x) + 16f(x-h) - f(x-2h)] / (12h²)"
            error_order = "O(h⁴)"
            
        else:
            raise ValueError("5-point central solo soporta órdenes 1 y 2")
        
        points_used = [x0 - 2*h, x0 - h, x0, x0 + h, x0 + 2*h]
        exact_value = self._compute_exact_derivative(f, x0, order)
        
        computation_data = {
            'points_used': points_used,
            'function_evaluations': [f(x) for x in points_used],
            'method_type': '5-point',
            'accuracy_order': 4
        }
        
        return DerivativeResult(
            value=derivative,
            method="5-Point Central",
            order=order,
            step_size=h,
            point=x0,
            exact_value=exact_value,
            formula=formula,
            error_order=error_order,
            computation_data=computation_data
        )
    
    def compare_all_methods(self, f: Callable[[float], float],
                           x0: float, h: float, order: int = 1) -> Dict[str, DerivativeResult]:
        """
        Compara todos los métodos disponibles.
        Principio de separación de responsabilidades.
        """
        results = {}
        
        # Métodos básicos
        results['forward'] = self.forward_difference(f, x0, h, order)
        results['backward'] = self.backward_difference(f, x0, h, order)
        results['central'] = self.central_difference(f, x0, h, order)
        
        # Método de alta precisión para órdenes 1 y 2
        if order <= 2:
            try:
                results['five_point'] = self.five_point_central(f, x0, h, order)
            except Exception as e:
                logger.warning(f"Error en 5-point: {e}")
        
        return results
    
    def step_size_analysis(self, f: Callable[[float], float],
                          x0: float, method: str = "central",
                          order: int = 1,
                          h_values: Optional[List[float]] = None) -> Dict[str, Any]:
        """
        Análisis de convergencia con diferentes tamaños de paso.
        Útil para determinar el h óptimo.
        """
        if h_values is None:
            h_values = [0.5, 0.1, 0.05, 0.01, 0.005, 0.001]
        
        results = []
        exact_value = self._compute_exact_derivative(f, x0, order)
        
        for h in h_values:
            try:
                if method == "forward":
                    result = self.forward_difference(f, x0, h, order)
                elif method == "backward":
                    result = self.backward_difference(f, x0, h, order)
                elif method == "central":
                    result = self.central_difference(f, x0, h, order)
                elif method == "five_point":
                    result = self.five_point_central(f, x0, h, order)
                else:
                    raise ValueError(f"Método '{method}' no reconocido")
                
                error = abs(result.value - exact_value) if exact_value is not None else None
                
                results.append({
                    'h': h,
                    'derivative': result.value,
                    'error': error,
                    'log_h': np.log10(h),
                    'log_error': np.log10(error) if error and error > 0 else None
                })
                
            except Exception as e:
                logger.warning(f"Error con h={h}: {e}")
                results.append({
                    'h': h,
                    'derivative': np.nan,
                    'error': np.nan,
                    'log_h': np.log10(h),
                    'log_error': None
                })
        
        return {
            'method': method,
            'order': order,
            'point': x0,
            'exact_value': exact_value,
            'results': results,
            'optimal_h': self._find_optimal_h(results)
        }
    
    def _compute_exact_derivative(self, f: Callable[[float], float],
                                 x0: float, order: int) -> Optional[float]:
        """
        Calcula la derivada exacta usando diferencias de alta precisión.
        Principio DRY: reutilizable en todos los métodos.
        """
        try:
            h = self.high_precision_h
            
            if order == 1:
                # Diferencia central de alta precisión
                return (f(x0 + h) - f(x0 - h)) / (2 * h)
            elif order == 2:
                # Segunda derivada de alta precisión
                return (f(x0 + h) - 2*f(x0) + f(x0 - h)) / (h**2)
            elif order == 3:
                # Tercera derivada de alta precisión
                return (f(x0 + 2*h) - 2*f(x0 + h) + 2*f(x0 - h) - f(x0 - 2*h)) / (2 * h**3)
            else:
                return None
        except Exception as e:
            logger.warning(f"Error calculando derivada exacta: {e}")
            return None
    
    def _get_forward_coefficients(self, order: int) -> List[float]:
        """Coeficientes para diferencias hacia adelante"""
        if order == 1:
            return [-1, 1]
        elif order == 2:
            return [1, -2, 1]
        elif order == 3:
            return [-1, 3, -3, 1]
        return []
    
    def _get_backward_coefficients(self, order: int) -> List[float]:
        """Coeficientes para diferencias hacia atrás"""
        if order == 1:
            return [-1, 1]
        elif order == 2:
            return [1, -2, 1]
        elif order == 3:
            return [-1, 3, -3, 1]
        return []
    
    def _get_central_coefficients(self, order: int) -> List[float]:
        """Coeficientes para diferencias centrales"""
        if order == 1:
            return [-0.5, 0.5]
        elif order == 2:
            return [1, -2, 1]
        elif order == 3:
            return [-0.5, 1, -1, 0.5]
        return []
    
    def _find_optimal_h(self, results: List[Dict]) -> Optional[float]:
        """Encuentra el h óptimo basado en el mínimo error"""
        valid_results = [r for r in results if r['error'] is not None and not np.isnan(r['error'])]
        
        if not valid_results:
            return None
        
        min_error_result = min(valid_results, key=lambda x: x['error'])
        return min_error_result['h']


# Funciones de análisis y validación
def richardson_extrapolation(calc: FiniteDifferenceCalculator,
                            f: Callable[[float], float],
                            x0: float, h: float, order: int = 1,
                            method: str = "central") -> Dict[str, Any]:
    """
    Extrapolación de Richardson para mejorar la precisión.
    Principio de extensibilidad del SOLID.
    """
    # Calcular con h y h/2
    if method == "central":
        result_h = calc.central_difference(f, x0, h, order)
        result_h2 = calc.central_difference(f, x0, h/2, order)
        
        # Para diferencias centrales: error es O(h²)
        # Richardson: D_improved = (4*D(h/2) - D(h)) / 3
        improved = (4 * result_h2.value - result_h.value) / 3
        error_order = 4  # O(h⁴)
        
    else:
        # Para forward/backward: error es O(h)
        if method == "forward":
            result_h = calc.forward_difference(f, x0, h, order)
            result_h2 = calc.forward_difference(f, x0, h/2, order)
        else:
            result_h = calc.backward_difference(f, x0, h, order)
            result_h2 = calc.backward_difference(f, x0, h/2, order)
        
        # Richardson: D_improved = 2*D(h/2) - D(h)
        improved = 2 * result_h2.value - result_h.value
        error_order = 2  # O(h²)
    
    exact_value = calc._compute_exact_derivative(f, x0, order)
    error = abs(improved - exact_value) if exact_value is not None else None
    
    return {
        'method': f"Richardson {method}",
        'original_h': result_h.value,
        'original_h2': result_h2.value,
        'improved': improved,
        'exact_value': exact_value,
        'error': error,
        'error_order': f"O(h^{error_order})",
        'improvement_factor': abs(result_h.absolute_error / error) if error and error > 0 else None
    }


def adaptive_step_size(calc: FiniteDifferenceCalculator,
                      f: Callable[[float], float],
                      x0: float, target_error: float = 1e-8,
                      method: str = "central", order: int = 1) -> Dict[str, Any]:
    """
    Encuentra automáticamente el tamaño de paso para alcanzar una precisión objetivo.
    Principio KISS: algoritmo simple pero efectivo.
    """
    h = 0.1  # Paso inicial
    min_h = 1e-12
    max_iterations = 20
    
    exact_value = calc._compute_exact_derivative(f, x0, order)
    if exact_value is None:
        return {'error': 'No se pudo calcular valor exacto'}
    
    results = []
    
    for i in range(max_iterations):
        if method == "central":
            result = calc.central_difference(f, x0, h, order)
        elif method == "forward":
            result = calc.forward_difference(f, x0, h, order)
        elif method == "backward":
            result = calc.backward_difference(f, x0, h, order)
        else:
            raise ValueError(f"Método '{method}' no reconocido")
        
        error = abs(result.value - exact_value)
        results.append({'h': h, 'error': error, 'derivative': result.value})
        
        if error <= target_error:
            return {
                'success': True,
                'optimal_h': h,
                'final_error': error,
                'derivative': result.value,
                'iterations': i + 1,
                'results': results
            }
        
        # Reducir h
        h /= 2
        
        if h < min_h:
            break
    
    return {
        'success': False,
        'reason': 'No se alcanzó la precisión objetivo',
        'final_h': h,
        'final_error': error,
        'results': results
    }


class FiniteDifferences:
    """
    Clase para diferencias finitas según especificaciones del prompt.
    Implementa métodos progresivo, regresivo y central con modo automático por listas.
    """
    
    def __init__(self):
        """Inicialización del calculador de diferencias finitas"""
        self.logger = logging.getLogger(__name__)
    
    def progressive_method(self, x: float, h: float, f_func: callable) -> dict:
        """
        Método progresivo: f'(x) ≈ [f(x+h) - f(x)] / h
        Error de truncamiento: O(h)
        
        Args:
            x: Punto de evaluación
            h: Tamaño de paso
            f_func: Función a derivar
            
        Returns:
            Diccionario con información completa del cálculo
        """
        try:
            # Validar inputs
            if h <= 0:
                raise ValueError("h debe ser positivo")
            if h >= 1:
                self.logger.warning(f"h={h} es muy grande, puede afectar precisión")
            
            # Calcular valores de función
            fx = f_func(x)
            fx_plus_h = f_func(x + h)
            
            # Calcular derivada
            derivative = (fx_plus_h - fx) / h
            
            return {
                'method': 'progressive',
                'x': x,
                'h': h,
                'fx': fx,
                'fx_plus_h': fx_plus_h,
                'derivative': derivative,
                'error_order': 'O(h)',
                'formula': "f'(x) ≈ [f(x+h) - f(x)] / h",
                'points_used': [x, x + h],
                'function_values': [fx, fx_plus_h]
            }
            
        except Exception as e:
            self.logger.error(f"Error en método progresivo: {e}")
            raise ValueError(f"Error calculando derivada progresiva: {e}")
    
    def regressive_method(self, x: float, h: float, f_func: callable) -> dict:
        """
        Método regresivo: f'(x) ≈ [f(x) - f(x-h)] / h
        Error de truncamiento: O(h)
        
        Args:
            x: Punto de evaluación
            h: Tamaño de paso
            f_func: Función a derivar
            
        Returns:
            Diccionario con información completa del cálculo
        """
        try:
            # Validar inputs
            if h <= 0:
                raise ValueError("h debe ser positivo")
            if h >= 1:
                self.logger.warning(f"h={h} es muy grande, puede afectar precisión")
            
            # Calcular valores de función
            fx = f_func(x)
            fx_minus_h = f_func(x - h)
            
            # Calcular derivada
            derivative = (fx - fx_minus_h) / h
            
            return {
                'method': 'regressive',
                'x': x,
                'h': h,
                'fx': fx,
                'fx_minus_h': fx_minus_h,
                'derivative': derivative,
                'error_order': 'O(h)',
                'formula': "f'(x) ≈ [f(x) - f(x-h)] / h",
                'points_used': [x - h, x],
                'function_values': [fx_minus_h, fx]
            }
            
        except Exception as e:
            self.logger.error(f"Error en método regresivo: {e}")
            raise ValueError(f"Error calculando derivada regresiva: {e}")
    
    def central_method(self, x: float, h: float, f_func: callable) -> dict:
        """
        Método central: f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
        Error de truncamiento: O(h²) - Mayor precisión
        
        Args:
            x: Punto de evaluación
            h: Tamaño de paso
            f_func: Función a derivar
            
        Returns:
            Diccionario con información completa del cálculo
        """
        try:
            # Validar inputs
            if h <= 0:
                raise ValueError("h debe ser positivo")
            if h >= 1:
                self.logger.warning(f"h={h} es muy grande, puede afectar precisión")
            
            # Calcular valores de función
            fx_plus_h = f_func(x + h)
            fx_minus_h = f_func(x - h)
            fx = f_func(x)  # Para información completa
            
            # Calcular derivada
            derivative = (fx_plus_h - fx_minus_h) / (2 * h)
            
            return {
                'method': 'central',
                'x': x,
                'h': h,
                'fx': fx,
                'fx_plus_h': fx_plus_h,
                'fx_minus_h': fx_minus_h,
                'derivative': derivative,
                'error_order': 'O(h²)',
                'formula': "f'(x) ≈ [f(x+h) - f(x-h)] / (2h)",
                'points_used': [x - h, x, x + h],
                'function_values': [fx_minus_h, fx, fx_plus_h]
            }
            
        except Exception as e:
            self.logger.error(f"Error en método central: {e}")
            raise ValueError(f"Error calculando derivada central: {e}")
    
    def auto_calculate_list(self, data_points: List[Dict]) -> List[Dict]:
        """
        Cálculo automático por lista con método óptimo según posición.
        
        - Primer punto: método progresivo
        - Puntos intermedios: método central (mayor precisión)
        - Último punto: método regresivo
        
        Args:
            data_points: Lista de diccionarios con keys: 'x', 'h', 'fx'
                        O con 'x', 'h' y función será evaluada
                        
        Returns:
            Lista de diccionarios con resultados de derivadas
        """
        try:
            if not data_points:
                raise ValueError("La lista de puntos no puede estar vacía")
            
            if len(data_points) < 1:
                raise ValueError("Se requiere al menos un punto de datos")
            
            results = []
            n_points = len(data_points)
            
            for i, point in enumerate(data_points):
                # Validar estructura del punto
                if 'x' not in point or 'h' not in point:
                    raise ValueError(f"Punto {i}: debe contener 'x' y 'h'")
                
                x = point['x']
                h = point['h']
                
                # Si tenemos fx, crear función constante, sino evaluar función dada
                if 'fx' in point:
                    # Crear función que interpolará entre puntos conocidos
                    fx_value = point['fx']
                    
                    # Para modo lista con valores fx, creamos función usando interpolación
                    # o diferencias finitas entre puntos adyacentes
                    if i == 0 and n_points > 1:
                        # Primer punto: usar siguiente punto para estimación
                        next_point = data_points[i + 1]
                        slope = (next_point.get('fx', fx_value) - fx_value) / (next_point['x'] - x)
                        f_func = lambda t, fx=fx_value, x0=x, m=slope: fx + m * (t - x0)
                    elif i == n_points - 1 and n_points > 1:
                        # Último punto: usar punto anterior
                        prev_point = data_points[i - 1]
                        slope = (fx_value - prev_point.get('fx', fx_value)) / (x - prev_point['x'])
                        f_func = lambda t, fx=fx_value, x0=x, m=slope: fx + m * (t - x0)
                    else:
                        # Punto intermedio: interpolación con puntos adyacentes
                        if n_points > 2:
                            prev_point = data_points[i - 1]
                            next_point = data_points[i + 1]
                            # Interpolación cuadrática simple
                            def quadratic_interp(t):
                                x0, x1, x2 = prev_point['x'], x, next_point['x']
                                y0, y1, y2 = prev_point.get('fx', fx_value), fx_value, next_point.get('fx', fx_value)
                                
                                # Interpolación de Lagrange
                                L0 = ((t - x1) * (t - x2)) / ((x0 - x1) * (x0 - x2))
                                L1 = ((t - x0) * (t - x2)) / ((x1 - x0) * (x1 - x2))
                                L2 = ((t - x0) * (t - x1)) / ((x2 - x0) * (x2 - x1))
                                
                                return y0 * L0 + y1 * L1 + y2 * L2
                            
                            f_func = quadratic_interp
                        else:
                            # Función constante si solo hay 2 puntos
                            f_func = lambda t, fx=fx_value: fx_value
                else:
                    # Usar función proporcionada
                    if 'function' not in point:
                        raise ValueError(f"Punto {i}: debe contener 'fx' o 'function'")
                    f_func = point['function']
                
                # Seleccionar método según posición
                if n_points == 1:
                    # Solo un punto: usar central por defecto
                    method = 'central'
                elif i == 0:
                    # Primer punto: progresivo
                    method = 'progressive'
                elif i == n_points - 1:
                    # Último punto: regresivo
                    method = 'regressive'
                else:
                    # Puntos intermedios: central (mayor precisión)
                    method = 'central'
                
                # Calcular derivada con método seleccionado
                result = self.calculate_single_point(x, h, f_func, method)
                result['position_in_list'] = i
                result['total_points'] = n_points
                result['auto_selected_method'] = method
                
                results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error en cálculo automático por lista: {e}")
            raise ValueError(f"Error en auto_calculate_list: {e}")
    
    def calculate_single_point(self, x: float, h: float, f_func: callable, method: str) -> dict:
        """
        Cálculo para un punto específico con método seleccionado.
        
        Args:
            x: Punto de evaluación
            h: Tamaño de paso
            f_func: Función a derivar
            method: 'progressive', 'regressive', o 'central'
            
        Returns:
            Diccionario con resultado del cálculo
        """
        try:
            method = method.lower()
            
            if method == 'progressive':
                return self.progressive_method(x, h, f_func)
            elif method == 'regressive':
                return self.regressive_method(x, h, f_func)
            elif method == 'central':
                return self.central_method(x, h, f_func)
            else:
                raise ValueError(f"Método '{method}' no válido. Use: 'progressive', 'regressive', o 'central'")
                
        except Exception as e:
            self.logger.error(f"Error en cálculo de punto único: {e}")
            raise ValueError(f"Error en calculate_single_point: {e}")
    
    def validate_input_data(self, data_points: List[Dict]) -> bool:
        """
        Valida la estructura de los datos de entrada.
        
        Args:
            data_points: Lista de puntos a validar
            
        Returns:
            True si los datos son válidos
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        if not isinstance(data_points, list):
            raise ValueError("data_points debe ser una lista")
        
        if len(data_points) == 0:
            raise ValueError("La lista no puede estar vacía")
        
        for i, point in enumerate(data_points):
            if not isinstance(point, dict):
                raise ValueError(f"Punto {i}: debe ser un diccionario")
            
            # Validar keys requeridos
            required_keys = ['x', 'h']
            for key in required_keys:
                if key not in point:
                    raise ValueError(f"Punto {i}: falta key requerido '{key}'")
            
            # Validar tipos
            try:
                float(point['x'])
                float(point['h'])
            except (ValueError, TypeError):
                raise ValueError(f"Punto {i}: 'x' y 'h' deben ser numéricos")
            
            # Validar h positivo
            if float(point['h']) <= 0:
                raise ValueError(f"Punto {i}: 'h' debe ser positivo")
            
            # Validar que tenga fx o function
            if 'fx' not in point and 'function' not in point:
                raise ValueError(f"Punto {i}: debe contener 'fx' o 'function'")
        
        return True
    
    def get_method_info(self) -> Dict[str, Dict]:
        """
        Retorna información sobre los métodos disponibles.
        
        Returns:
            Diccionario con información de cada método
        """
        return {
            'progressive': {
                'name': 'Método Progresivo',
                'formula': "f'(x) ≈ [f(x+h) - f(x)] / h",
                'error_order': 'O(h)',
                'best_for': 'Primer punto de una lista o cuando solo se conoce f(x) y f(x+h)',
                'points_needed': 2,
                'points_pattern': '[x, x+h]'
            },
            'regressive': {
                'name': 'Método Regresivo', 
                'formula': "f'(x) ≈ [f(x) - f(x-h)] / h",
                'error_order': 'O(h)',
                'best_for': 'Último punto de una lista o cuando solo se conoce f(x-h) y f(x)',
                'points_needed': 2,
                'points_pattern': '[x-h, x]'
            },
            'central': {
                'name': 'Método Central',
                'formula': "f'(x) ≈ [f(x+h) - f(x-h)] / (2h)",
                'error_order': 'O(h²)',
                'best_for': 'Puntos intermedios, mayor precisión',
                'points_needed': 3,
                'points_pattern': '[x-h, x, x+h]'
            }
        }
