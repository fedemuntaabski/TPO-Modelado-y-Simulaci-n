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

from .root_basic_methods import RootBasicMethods
from .root_acceleration_methods import RootAccelerationMethods
from .root_interpolation_methods import RootInterpolationMethods

class RootMethods:
    """
    Clase que encapsula métodos para encontrar raíces de ecuaciones
    """

    @staticmethod
    def bisection_method(f, a, b, tol=1e-6, max_iter=100):
        return RootBasicMethods.bisection_method(f, a, b, tol, max_iter)

    @staticmethod
    def newton_raphson_method(f, df, x0, tol=1e-6, max_iter=100):
        return RootBasicMethods.newton_raphson_method(f, df, x0, tol, max_iter)

    @staticmethod
    def fixed_point_method(g, x0, tol=1e-6, max_iter=100):
        return RootBasicMethods.fixed_point_method(g, x0, tol, max_iter)

    @staticmethod
    def aitken_acceleration(sequence):
        return RootAccelerationMethods.aitken_acceleration(sequence)

    @staticmethod
    def aitken_method(g, x0, tol=1e-6, max_iter=100):
        return RootAccelerationMethods.aitken_method(g, x0, tol, max_iter)

    @staticmethod
    def lagrange_interpolation(x_points, y_points, x):
        return RootInterpolationMethods.lagrange_interpolation(x_points, y_points, x)

    @staticmethod
    def lagrange_polynomial(x_points, y_points):
        return RootInterpolationMethods.lagrange_polynomial(x_points, y_points)

    # Aliases for compatibility
    @staticmethod
    def bisection(f, a, b, tol=1e-6, max_iter=100):
        return RootBasicMethods.bisection_method(f, a, b, tol, max_iter)[0]

    @staticmethod
    def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
        return RootBasicMethods.newton_raphson_method(f, df, x0, tol, max_iter)[0]

    @staticmethod
    def fixed_point(g, x0, tol=1e-6, max_iter=100):
        return RootBasicMethods.fixed_point_method(g, x0, tol, max_iter)[0]

    @staticmethod
    def aitken(g, x0, tol=1e-6, max_iter=100):
        return RootAccelerationMethods.aitken_method(g, x0, tol, max_iter)[0]
