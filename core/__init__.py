"""
Módulo Core del Simulador Matemático Avanzado
Contiene las implementaciones fundamentales de métodos numéricos
"""

from .differential_equations import DifferentialEquations
from .numerical_integration import NumericalIntegration  
from .finite_differences import FiniteDifferences

__all__ = ['DifferentialEquations', 'NumericalIntegration', 'FiniteDifferences']
