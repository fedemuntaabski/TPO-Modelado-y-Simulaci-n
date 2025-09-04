"""
Pestañas adicionales para métodos avanzados
Incluye interpolación, diferencias finitas y aceleración de Aitken
"""

# Importar las clases modularizadas
from .interpolation_tab import InterpolationTab
from .derivatives_tab import DerivativesTab
from .finite_differences_tab import FiniteDifferencesTab

# Exportar las clases para compatibilidad
__all__ = ['InterpolationTab', 'DerivativesTab', 'FiniteDifferencesTab']
