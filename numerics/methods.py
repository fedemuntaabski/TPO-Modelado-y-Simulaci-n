"""
Módulo de Métodos Numéricos
Punto de entrada unificado para todos los métodos numéricos

Este módulo importa y reexporta todas las funcionalidades
desde los módulos especializados para mantener compatibilidad
"""

# Importar todas las clases y métodos desde los módulos especializados
from .core_methods import NumericalMethods as CoreMethods
from .root_methods import RootMethods
from .parser_utils import MathParser, ExpressionUtils

# Crear una clase NumericalMethods que combine funcionalidades para compatibilidad
class NumericalMethods(CoreMethods):
    """
    Clase principal que combina todos los métodos numéricos
    para mantener compatibilidad con el código existente
    """

    # Agregar métodos de raíces a la clase principal
    @staticmethod
    def bisection_method(f, a, b, tol=1e-6, max_iter=100):
        return RootMethods.bisection_method(f, a, b, tol, max_iter)

    @staticmethod
    def newton_raphson_method(f, df, x0, tol=1e-6, max_iter=100):
        return RootMethods.newton_raphson_method(f, df, x0, tol, max_iter)

    @staticmethod
    def fixed_point_method(g, x0, tol=1e-6, max_iter=100):
        return RootMethods.fixed_point_method(g, x0, tol, max_iter)

    @staticmethod
    def aitken_acceleration(sequence):
        return RootMethods.aitken_acceleration(sequence)

    @staticmethod
    def aitken_method(g, x0, tol=1e-6, max_iter=100):
        return RootMethods.aitken_method(g, x0, tol, max_iter)

    @staticmethod
    def lagrange_interpolation(x_points, y_points, x):
        return RootMethods.lagrange_interpolation(x_points, y_points, x)

    @staticmethod
    def lagrange_polynomial(x_points, y_points):
        return RootMethods.lagrange_polynomial(x_points, y_points)

# Re-exportar para compatibilidad hacia atrás
__all__ = [
    'NumericalMethods',
    'RootMethods',
    'MathParser',
    'ExpressionUtils'
]
