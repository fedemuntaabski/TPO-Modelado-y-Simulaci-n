"""
Métodos numéricos para integración definida.

Implementa algoritmos de integración numérica siguiendo principios SOLID y DRY.
Cada método mantiene responsabilidad única y está optimizado para rendimiento.
"""

import numpy as np
from typing import Callable, Tuple, List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class IntegrationResult:
    """Resultado de integración numérica siguiendo el principio de encapsulación"""
    
    def __init__(self, value: float, method: str, subdivisions: int,
                 step_size: float, error: Optional[float] = None,
                 exact_value: Optional[float] = None,
                 computation_data: Optional[Dict] = None):
        self.value = value
        self.method = method
        self.subdivisions = subdivisions
        self.step_size = step_size
        self.error = error
        self.exact_value = exact_value
        self.computation_data = computation_data or {}
        
        # Calcular error relativo si es posible
        if self.exact_value is not None and self.exact_value != 0:
            self.relative_error = abs(self.error / self.exact_value) * 100
        else:
            self.relative_error = None


class NumericalIntegrator:
    """
    Clase principal para métodos de integración numérica.
    Sigue el principio de responsabilidad única (SRP) del SOLID.
    """
    
    def __init__(self, use_scipy: bool = True) -> None:
        self.use_scipy = use_scipy
        
        # Intentar importar scipy para valores exactos
        if use_scipy:
            try:
                from scipy.integrate import quad
                self._quad = quad
                self._scipy_available = True
            except ImportError:
                self._scipy_available = False
                logger.warning("SciPy no disponible. No se calcularán valores exactos.")
        else:
            self._scipy_available = False
    
    def trapezoid_rule(self, f: Callable[[float], float],
                      a: float, b: float, n: int) -> IntegrationResult:
        """
        Regla del trapecio para integración numérica.
        
        Args:
            f: Función a integrar
            a: Límite inferior
            b: Límite superior  
            n: Número de subdivisiones
            
        Returns:
            IntegrationResult con información completa
        """
        h = (b - a) / n
        x_values = np.linspace(a, b, n + 1)
        y_values = np.array([f(x) for x in x_values])
        
        # Fórmula del trapecio: h * [f(a)/2 + f(a+h) + ... + f(b)/2]
        integral = h * (y_values[0]/2 + np.sum(y_values[1:-1]) + y_values[-1]/2)
        
        # Calcular valor exacto y error si scipy disponible
        exact_value, error = self._compute_exact_value_and_error(f, a, b, integral)
        
        computation_data = {
            'x_values': x_values.tolist(),
            'y_values': y_values.tolist(),
            'formula': 'h * [f(a)/2 + Σf(xi) + f(b)/2]'
        }
        
        return IntegrationResult(
            value=integral,
            method="Regla del Trapecio",
            subdivisions=n,
            step_size=h,
            error=error,
            exact_value=exact_value,
            computation_data=computation_data
        )
    
    def simpson_13_rule(self, f: Callable[[float], float],
                       a: float, b: float, n: int) -> IntegrationResult:
        """
        Regla de Simpson 1/3 para integración numérica.
        
        Args:
            f: Función a integrar
            a: Límite inferior
            b: Límite superior
            n: Número de subdivisiones (se ajustará a par si es necesario)
            
        Returns:
            IntegrationResult con información completa
        """
        # Simpson 1/3 requiere n par
        if n % 2 != 0:
            n += 1
            logger.info(f"Ajustando n a {n} (debe ser par para Simpson 1/3)")
        
        h = (b - a) / n
        x_values = np.linspace(a, b, n + 1)
        y_values = np.array([f(x) for x in x_values])
        
        # Fórmula de Simpson 1/3: h/3 * [f(a) + 4*Σf(xi impares) + 2*Σf(xi pares) + f(b)]
        odd_sum = np.sum(y_values[1::2])    # Índices impares
        even_sum = np.sum(y_values[2:-1:2]) # Índices pares (excluyendo extremos)
        
        integral = h/3 * (y_values[0] + 4*odd_sum + 2*even_sum + y_values[-1])
        
        # Calcular valor exacto y error
        exact_value, error = self._compute_exact_value_and_error(f, a, b, integral)
        
        computation_data = {
            'x_values': x_values.tolist(),
            'y_values': y_values.tolist(),
            'odd_sum': float(odd_sum),
            'even_sum': float(even_sum),
            'formula': 'h/3 * [f(a) + 4*Σf(xi_odd) + 2*Σf(xi_even) + f(b)]'
        }
        
        return IntegrationResult(
            value=integral,
            method="Regla de Simpson 1/3",
            subdivisions=n,
            step_size=h,
            error=error,
            exact_value=exact_value,
            computation_data=computation_data
        )
    
    def simpson_38_rule(self, f: Callable[[float], float],
                       a: float, b: float, n: int) -> IntegrationResult:
        """
        Regla de Simpson 3/8 para integración numérica.
        
        Args:
            f: Función a integrar
            a: Límite inferior
            b: Límite superior
            n: Número de subdivisiones (se ajustará a múltiplo de 3 si es necesario)
            
        Returns:
            IntegrationResult con información completa
        """
        # Simpson 3/8 requiere n múltiplo de 3
        if n % 3 != 0:
            n = ((n // 3) + 1) * 3
            logger.info(f"Ajustando n a {n} (debe ser múltiplo de 3 para Simpson 3/8)")
        
        h = (b - a) / n
        x_values = np.linspace(a, b, n + 1)
        y_values = np.array([f(x) for x in x_values])
        
        # Fórmula de Simpson 3/8
        integral = 0
        for i in range(0, n, 3):
            # Cada triplete: 3h/8 * [f(xi) + 3*f(xi+1) + 3*f(xi+2) + f(xi+3)]
            segment = 3*h/8 * (y_values[i] + 3*y_values[i+1] + 3*y_values[i+2] + y_values[i+3])
            integral += segment
        
        # Calcular valor exacto y error
        exact_value, error = self._compute_exact_value_and_error(f, a, b, integral)
        
        computation_data = {
            'x_values': x_values.tolist(),
            'y_values': y_values.tolist(),
            'formula': '3h/8 * Σ[f(xi) + 3*f(xi+1) + 3*f(xi+2) + f(xi+3)]'
        }
        
        return IntegrationResult(
            value=integral,
            method="Regla de Simpson 3/8",
            subdivisions=n,
            step_size=h,
            error=error,
            exact_value=exact_value,
            computation_data=computation_data
        )
    
    def composite_trapezoid(self, f: Callable[[float], float],
                          a: float, b: float, n: int) -> IntegrationResult:
        """
        Regla del trapecio compuesta con análisis de convergencia.
        """
        return self.trapezoid_rule(f, a, b, n)
    
    def adaptive_simpson(self, f: Callable[[float], float],
                        a: float, b: float, tolerance: float = 1e-6) -> IntegrationResult:
        """
        Simpson adaptativo con refinamiento automático.
        Principio KISS: mantiene la lógica simple pero efectiva.
        """
        def simpson_single(fa: float, fb: float, fc: float, h: float) -> float:
            """Simpson simple en un intervalo"""
            return h/6 * (fa + 4*fc + fb)
        
        # Comenzar con estimación simple
        c = (a + b) / 2
        h = b - a
        fa, fb, fc = f(a), f(b), f(c)
        
        s1 = simpson_single(fa, fb, fc, h)
        
        # Refinar recursivamente
        def recursive_simpson(xa: float, xb: float, fa: float, fb: float, s_total: float, tolerance: float, depth: int = 0) -> float:
            if depth > 20:  # Evitar recursión infinita
                return s_total
            
            xc = (xa + xb) / 2
            fc = f(xc)
            h = xb - xa
            
            # Calcular Simpson en cada mitad
            xd = (xa + xc) / 2
            xe = (xc + xb) / 2
            fd, fe = f(xd), f(xe)
            
            s_left = simpson_single(fa, fc, fd, h/2)
            s_right = simpson_single(fc, fb, fe, h/2)
            s_new = s_left + s_right
            
            # Verificar tolerancia (regla de Richardson)
            if abs(s_new - s_total) <= 15 * tolerance:
                return s_new
            
            # Refinar recursivamente
            tol_half = tolerance / 2
            left_result = recursive_simpson(xa, xc, fa, fc, s_left, tol_half, depth+1)
            right_result = recursive_simpson(xc, xb, fc, fb, s_right, tol_half, depth+1)
            
            return left_result + right_result
        
        final_result = recursive_simpson(a, b, fa, fb, s1, tolerance)
        
        # Calcular valor exacto y error
        exact_value, error = self._compute_exact_value_and_error(f, a, b, final_result)
        
        return IntegrationResult(
            value=final_result,
            method="Simpson Adaptativo",
            subdivisions=-1,  # Variable
            step_size=-1,     # Variable
            error=error,
            exact_value=exact_value,
            computation_data={'tolerance_used': tolerance}
        )
    
    def _compute_exact_value_and_error(self, f: Callable[[float], float],
                                      a: float, b: float, 
                                      computed_value: float) -> Tuple[Optional[float], Optional[float]]:
        """
        Calcula valor exacto y error usando scipy si está disponible.
        Principio DRY: reutilizable en todos los métodos.
        """
        if not self._scipy_available:
            return None, None
        
        try:
            exact_value, _ = self._quad(f, a, b)
            error = abs(computed_value - exact_value)
            return exact_value, error
        except Exception as e:
            logger.warning(f"Error calculando valor exacto: {e}")
            return None, None


# Funciones utilitarias para análisis de convergencia
def convergence_analysis(integrator: NumericalIntegrator,
                        f: Callable[[float], float],
                        a: float, b: float,
                        method: str = "trapezoid",
                        n_values: List[int] = None) -> Dict[str, Any]:
    """
    Analiza la convergencia de un método de integración.
    Principio de separación de responsabilidades.
    """
    if n_values is None:
        n_values = [10, 20, 50, 100, 200, 500]
    
    results = []
    
    for n in n_values:
        if method == "trapezoid":
            result = integrator.trapezoid_rule(f, a, b, n)
        elif method == "simpson13":
            result = integrator.simpson_13_rule(f, a, b, n)
        elif method == "simpson38":
            result = integrator.simpson_38_rule(f, a, b, n)
        else:
            raise ValueError(f"Método '{method}' no reconocido")
        
        results.append({
            'n': n,
            'h': result.step_size,
            'value': result.value,
            'error': result.error,
            'relative_error': result.relative_error
        })
    
    return {
        'method': method,
        'results': results,
        'exact_value': results[0].get('exact_value') if results else None
    }
