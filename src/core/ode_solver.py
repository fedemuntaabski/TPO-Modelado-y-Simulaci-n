"""
Métodos numéricos para resolver ecuaciones diferenciales ordinarias (EDO).

Implementa algoritmos clásicos siguiendo principios SOLID, DRY y KISS.
Cada método está optimizado para rendimiento y mantiene responsabilidad única.
"""

import numpy as np
from typing import Callable, Tuple, List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ODEResult:
    """Resultado de la solución de EDO siguiendo el principio de encapsulación"""
    
    def __init__(self, t: np.ndarray, y: np.ndarray, method: str,
                 step_size: float, exact_solution: Optional[np.ndarray] = None,
                 computation_data: Optional[Dict] = None):
        self.t = t
        self.y = y
        self.method = method
        self.step_size = step_size
        self.exact_solution = exact_solution
        self.computation_data = computation_data or {}
        
        # Calcular errores si hay solución exacta
        if exact_solution is not None:
            self.error = np.abs(y - exact_solution)
            self.max_error = np.max(self.error)
            self.avg_error = np.mean(self.error)
            self.final_error = self.error[-1]
        else:
            self.error = None
            self.max_error = None
            self.avg_error = None
            self.final_error = None


class ODESolver:
    """
    Clase principal para resolver ecuaciones diferenciales ordinarias.
    Sigue el principio de responsabilidad única (SRP) del SOLID.
    """
    
    def __init__(self, use_scipy: bool = True):
        self.use_scipy = use_scipy
        
        # Intentar importar scipy para soluciones exactas
        if use_scipy:
            try:
                from scipy.integrate import solve_ivp
                self._solve_ivp = solve_ivp
                self._scipy_available = True
            except ImportError:
                self._scipy_available = False
                logger.warning("SciPy no disponible. No se calcularán soluciones exactas.")
        else:
            self._scipy_available = False
    
    def euler_method(self, f: Callable[[float, float], float],
                    t0: float, tf: float, y0: float, n: int) -> ODEResult:
        """
        Método de Euler para resolver dy/dt = f(t, y).
        
        Args:
            f: Función f(t, y) del lado derecho de la EDO
            t0: Tiempo inicial
            tf: Tiempo final
            y0: Condición inicial y(t0) = y0
            n: Número de puntos
            
        Returns:
            ODEResult con la solución completa
        """
        h = (tf - t0) / (n - 1)
        t = np.linspace(t0, tf, n)
        y = np.zeros(n)
        y[0] = y0
        
        # Datos para análisis paso a paso
        step_data = []
        
        # Implementar método de Euler: y_{i+1} = y_i + h * f(t_i, y_i)
        for i in range(n - 1):
            fi = f(t[i], y[i])
            y[i + 1] = y[i] + h * fi
            
            step_data.append({
                'i': i,
                't_i': t[i],
                'y_i': y[i],
                'f_ti_yi': fi,
                'y_i_plus_1': y[i + 1]
            })
        
        # Calcular solución exacta si scipy disponible
        exact_solution = self._compute_exact_solution(f, t0, tf, y0, t)
        
        computation_data = {
            'formula': 'y_{i+1} = y_i + h * f(t_i, y_i)',
            'order': 1,
            'step_data': step_data[:10]  # Solo primeros 10 pasos para no sobrecargar
        }
        
        return ODEResult(
            t=t,
            y=y,
            method="Euler",
            step_size=h,
            exact_solution=exact_solution,
            computation_data=computation_data
        )
    
    def runge_kutta_2(self, f: Callable[[float, float], float],
                     t0: float, tf: float, y0: float, n: int) -> ODEResult:
        """
        Método de Runge-Kutta de 2do orden (RK2).
        
        Implementa el método del punto medio mejorado.
        """
        h = (tf - t0) / (n - 1)
        t = np.linspace(t0, tf, n)
        y = np.zeros(n)
        y[0] = y0
        
        step_data = []
        
        # RK2: método del punto medio
        for i in range(n - 1):
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h, y[i] + k1)
            y[i + 1] = y[i] + (k1 + k2) / 2
            
            step_data.append({
                'i': i,
                't_i': t[i],
                'y_i': y[i],
                'k1': k1,
                'k2': k2,
                'y_i_plus_1': y[i + 1]
            })
        
        exact_solution = self._compute_exact_solution(f, t0, tf, y0, t)
        
        computation_data = {
            'formula': ['k₁ = h·f(tᵢ, yᵢ)', 
                       'k₂ = h·f(tᵢ + h, yᵢ + k₁)',
                       'y_{i+1} = yᵢ + (k₁ + k₂)/2'],
            'order': 2,
            'step_data': step_data[:10]
        }
        
        return ODEResult(
            t=t,
            y=y,
            method="Runge-Kutta 2",
            step_size=h,
            exact_solution=exact_solution,
            computation_data=computation_data
        )
    
    def runge_kutta_4(self, f: Callable[[float, float], float],
                     t0: float, tf: float, y0: float, n: int) -> ODEResult:
        """
        Método de Runge-Kutta de 4to orden (RK4).
        
        El método más popular y preciso de los algoritmos explícitos.
        """
        h = (tf - t0) / (n - 1)
        t = np.linspace(t0, tf, n)
        y = np.zeros(n)
        y[0] = y0
        
        step_data = []
        
        # RK4: método clásico de cuarto orden
        for i in range(n - 1):
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + k1/2)
            k3 = h * f(t[i] + h/2, y[i] + k2/2)
            k4 = h * f(t[i] + h, y[i] + k3)
            
            y[i + 1] = y[i] + (k1 + 2*k2 + 2*k3 + k4) / 6
            
            step_data.append({
                'i': i,
                't_i': t[i],
                'y_i': y[i],
                'k1': k1,
                'k2': k2,
                'k3': k3,
                'k4': k4,
                'y_i_plus_1': y[i + 1]
            })
        
        exact_solution = self._compute_exact_solution(f, t0, tf, y0, t)
        
        computation_data = {
            'formula': ['k₁ = h·f(tᵢ, yᵢ)',
                       'k₂ = h·f(tᵢ + h/2, yᵢ + k₁/2)',
                       'k₃ = h·f(tᵢ + h/2, yᵢ + k₂/2)',
                       'k₄ = h·f(tᵢ + h, yᵢ + k₃)',
                       'y_{i+1} = yᵢ + (k₁ + 2k₂ + 2k₃ + k₄)/6'],
            'order': 4,
            'step_data': step_data[:10]
        }
        
        return ODEResult(
            t=t,
            y=y,
            method="Runge-Kutta 4",
            step_size=h,
            exact_solution=exact_solution,
            computation_data=computation_data
        )
    
    def heun_method(self, f: Callable[[float, float], float],
                   t0: float, tf: float, y0: float, n: int) -> ODEResult:
        """
        Método de Heun (predictor-corrector de 2do orden).
        
        También conocido como método de Euler mejorado.
        """
        h = (tf - t0) / (n - 1)
        t = np.linspace(t0, tf, n)
        y = np.zeros(n)
        y[0] = y0
        
        step_data = []
        
        for i in range(n - 1):
            # Predictor (Euler)
            y_predictor = y[i] + h * f(t[i], y[i])
            
            # Corrector (promedio de pendientes)
            y[i + 1] = y[i] + h/2 * (f(t[i], y[i]) + f(t[i + 1], y_predictor))
            
            step_data.append({
                'i': i,
                't_i': t[i],
                'y_i': y[i],
                'y_predictor': y_predictor,
                'y_i_plus_1': y[i + 1]
            })
        
        exact_solution = self._compute_exact_solution(f, t0, tf, y0, t)
        
        computation_data = {
            'formula': ['y*_{i+1} = yᵢ + h·f(tᵢ, yᵢ)  (predictor)',
                       'y_{i+1} = yᵢ + h/2·[f(tᵢ, yᵢ) + f(tᵢ₊₁, y*ᵢ₊₁)]  (corrector)'],
            'order': 2,
            'step_data': step_data[:10]
        }
        
        return ODEResult(
            t=t,
            y=y,
            method="Heun",
            step_size=h,
            exact_solution=exact_solution,
            computation_data=computation_data
        )
    
    def adaptive_rk45(self, f: Callable[[float, float], float],
                     t0: float, tf: float, y0: float, 
                     tolerance: float = 1e-6) -> ODEResult:
        """
        Runge-Kutta adaptativo de 4to/5to orden con control de error.
        Principio KISS: usa scipy si está disponible, sino implementación básica.
        """
        if self._scipy_available:
            try:
                sol = self._solve_ivp(
                    lambda t, y: f(t, y[0]),
                    [t0, tf],
                    [y0],
                    method='RK45',
                    rtol=tolerance,
                    atol=tolerance
                )
                
                return ODEResult(
                    t=sol.t,
                    y=sol.y[0],
                    method="Adaptive RK45",
                    step_size=-1,  # Variable
                    exact_solution=None,
                    computation_data={
                        'adaptive': True,
                        'tolerance': tolerance,
                        'evaluations': sol.nfev
                    }
                )
            except Exception as e:
                logger.warning(f"Error en RK45 adaptativo: {e}")
        
        # Fallback: usar RK4 con paso fijo
        logger.info("Usando RK4 con paso fijo como fallback")
        return self.runge_kutta_4(f, t0, tf, y0, 100)
    
    def _compute_exact_solution(self, f: Callable[[float, float], float],
                               t0: float, tf: float, y0: float,
                               t_eval: np.ndarray) -> Optional[np.ndarray]:
        """
        Calcula la solución exacta usando scipy si está disponible.
        Principio DRY: reutilizable en todos los métodos.
        """
        if not self._scipy_available:
            return None
        
        try:
            sol = self._solve_ivp(
                lambda t, y: f(t, y[0]),
                [t0, tf],
                [y0],
                t_eval=t_eval,
                method='RK45',
                rtol=1e-9,
                atol=1e-12
            )
            return sol.y[0]
        except Exception as e:
            logger.warning(f"Error calculando solución exacta: {e}")
            return None


# Funciones utilitarias para análisis y validación
def stability_analysis(solver: ODESolver, f: Callable[[float, float], float],
                      t0: float, tf: float, y0: float,
                      step_sizes: List[float]) -> Dict[str, Any]:
    """
    Analiza la estabilidad de métodos para diferentes tamaños de paso.
    Principio de separación de responsabilidades.
    """
    results = {}
    
    for method_name in ['euler', 'rk2', 'rk4']:
        results[method_name] = []
        
        for h in step_sizes:
            n = int((tf - t0) / h) + 1
            
            try:
                if method_name == 'euler':
                    result = solver.euler_method(f, t0, tf, y0, n)
                elif method_name == 'rk2':
                    result = solver.runge_kutta_2(f, t0, tf, y0, n)
                elif method_name == 'rk4':
                    result = solver.runge_kutta_4(f, t0, tf, y0, n)
                
                results[method_name].append({
                    'h': h,
                    'final_value': result.y[-1],
                    'max_error': result.max_error,
                    'stable': not np.any(np.isnan(result.y)) and not np.any(np.isinf(result.y))
                })
                
            except Exception as e:
                results[method_name].append({
                    'h': h,
                    'final_value': np.nan,
                    'max_error': np.nan,
                    'stable': False,
                    'error': str(e)
                })
    
    return results


def convergence_order_analysis(solver: ODESolver, f: Callable[[float, float], float],
                              t0: float, tf: float, y0: float,
                              method: str = 'rk4') -> Dict[str, Any]:
    """
    Analiza el orden de convergencia de un método.
    Útil para validar la implementación teórica.
    """
    step_sizes = [0.1, 0.05, 0.025, 0.0125]
    errors = []
    
    for h in step_sizes:
        n = int((tf - t0) / h) + 1
        
        if method == 'euler':
            result = solver.euler_method(f, t0, tf, y0, n)
        elif method == 'rk2':
            result = solver.runge_kutta_2(f, t0, tf, y0, n)
        elif method == 'rk4':
            result = solver.runge_kutta_4(f, t0, tf, y0, n)
        else:
            raise ValueError(f"Método '{method}' no reconocido")
        
        if result.final_error is not None:
            errors.append(result.final_error)
        else:
            errors.append(np.nan)
    
    # Calcular orden de convergencia
    convergence_orders = []
    for i in range(len(errors) - 1):
        if errors[i] > 0 and errors[i+1] > 0:
            ratio = step_sizes[i] / step_sizes[i+1]
            error_ratio = errors[i] / errors[i+1]
            order = np.log(error_ratio) / np.log(ratio)
            convergence_orders.append(order)
        else:
            convergence_orders.append(np.nan)
    
    return {
        'method': method,
        'step_sizes': step_sizes,
        'errors': errors,
        'convergence_orders': convergence_orders,
        'average_order': np.nanmean(convergence_orders)
    }
