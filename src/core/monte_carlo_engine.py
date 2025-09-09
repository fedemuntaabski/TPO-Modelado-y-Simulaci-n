"""
Módulo para simulación Monte Carlo.

Implementa los algoritmos para realizar análisis numéricos de funciones 
mediante métodos estocásticos.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from typing import Callable, Optional, Tuple, Dict, List, Union, Any
import logging

logger = logging.getLogger(__name__)

class MonteCarloEngine:
    """
    Motor de simulación Monte Carlo para integrales y análisis numérico.
    Proporciona métodos para estimar integrales mediante técnicas estocásticas.
    """
    
    def __init__(self):
        """Inicializa el motor de simulación Monte Carlo"""
        self._last_results = None
        self._cache = {}  # Caché para resultados previos
    
    def simulate(self, 
                func: Callable,
                n_samples: int,
                seed: Optional[int] = None,
                max_error: float = 0.05,
                dimensions: int = 1,
                x_range: Tuple[float, float] = (0, 1),
                y_range: Optional[Tuple[float, float]] = None) -> Dict:
        """
        Ejecuta simulación Monte Carlo para estimar una integral.
        
        Args:
            func: Función a integrar
            n_samples: Número de muestras aleatorias
            seed: Semilla para reproducibilidad
            max_error: Error máximo aceptable para IC
            dimensions: Dimensiones de la integración (1 o 2)
            x_range: Rango en el eje x (a, b)
            y_range: Rango en el eje y (c, d) para integrales 2D
            
        Returns:
            Diccionario con todos los resultados de la simulación
        """
        # Validaciones básicas
        if n_samples <= 0:
            raise ValueError("El número de muestras debe ser positivo")
        
        if dimensions not in [1, 2]:
            raise ValueError("Solo se admiten integraciones 1D o 2D")
        
        if dimensions == 2 and y_range is None:
            raise ValueError("Para integraciones 2D se requiere el rango y")
        
        # Establecer semilla si se proporciona
        if seed is not None:
            np.random.seed(seed)
        
        # Calcular volumen del dominio
        volume = self._calculate_volume(dimensions, x_range, y_range)
        
        # Generar puntos aleatorios
        points, values = self._generate_points(func, n_samples, dimensions, x_range, y_range)
        
        # Calcular el resultado de la integración
        integration_result = self._calculate_integration(values, volume)
        
        # Calcular estadísticas
        std_dev, std_error, confidence_interval = self._calculate_statistics(values, volume, max_error)
        
        # Generar datos para visualización de convergencia
        convergence_data = self._calculate_convergence(func, n_samples, dimensions, x_range, volume, y_range)
        
        # Separar puntos para visualización
        points_inside, points_outside = self._classify_points(points, values, dimensions)
        
        # Guardar resultados
        self._last_results = {
            'desviacion_estandar': std_dev,
            'error_estandar': std_error,
            'intervalo_confianza': confidence_interval,
            'volumen': volume,
            'resultado_integracion': integration_result,
            'puntos_dentro': points_inside,
            'puntos_fuera': points_outside,
            'convergencia': convergence_data
        }
        
        return self._last_results
    
    def _calculate_volume(self, dimensions: int, x_range: Tuple[float, float], 
                          y_range: Optional[Tuple[float, float]] = None) -> float:
        """Calcula el volumen del dominio de integración"""
        x_volume = x_range[1] - x_range[0]
        
        if dimensions == 1:
            return x_volume
        else:
            y_volume = y_range[1] - y_range[0]
            return x_volume * y_volume
    
    def _generate_points(self, func: Callable, n_samples: int, dimensions: int,
                        x_range: Tuple[float, float], 
                        y_range: Optional[Tuple[float, float]] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Genera puntos aleatorios y evalúa la función en ellos"""
        if dimensions == 1:
            # Generar puntos aleatorios 1D
            x = np.random.uniform(x_range[0], x_range[1], n_samples)
            points = x.reshape(-1, 1)
            values = np.array([func(xi) for xi in x])
            
        else:
            # Generar puntos aleatorios 2D
            x = np.random.uniform(x_range[0], x_range[1], n_samples)
            y = np.random.uniform(y_range[0], y_range[1], n_samples)
            points = np.column_stack((x, y))
            values = np.array([func(xi, yi) for xi, yi in zip(x, y)])
        
        return points, values
    
    def _calculate_integration(self, values: np.ndarray, volume: float) -> float:
        """Calcula el resultado de la integración mediante Monte Carlo"""
        return volume * np.mean(values)
    
    def _calculate_statistics(self, values: np.ndarray, volume: float, 
                             max_error: float) -> Tuple[float, float, Tuple[float, float]]:
        """Calcula estadísticas de la simulación"""
        # Desviación estándar
        std_dev = np.std(values, ddof=1)
        
        # Error estándar
        n = len(values)
        std_error = std_dev / np.sqrt(n)
        
        # Intervalo de confianza (95%)
        z_value = stats.norm.ppf(0.975)  # Valor z para IC 95%
        margin_error = z_value * std_error
        mean_value = np.mean(values)
        
        # Ajustar el resultado por el volumen
        adjusted_error = volume * margin_error
        adjusted_mean = volume * mean_value
        
        confidence_interval = (adjusted_mean - adjusted_error, adjusted_mean + adjusted_error)
        
        return std_dev, std_error * volume, confidence_interval
    
    def _calculate_convergence(self, func: Callable, n_samples: int, dimensions: int,
                              x_range: Tuple[float, float], volume: float,
                              y_range: Optional[Tuple[float, float]] = None) -> np.ndarray:
        """Calcula datos de convergencia del método"""
        # Tomar puntos logarítmicamente espaciados para mostrar convergencia
        if n_samples <= 100:
            sample_points = list(range(10, n_samples + 1, 10))
        else:
            # Usar puntos logarítmicamente espaciados para muestras grandes
            log_space = np.logspace(1, np.log10(n_samples), 30).astype(int)
            sample_points = np.unique(log_space)
        
        results = []
        
        for n in sample_points:
            points, values = self._generate_points(func, n, dimensions, x_range, y_range)
            result = volume * np.mean(values)
            results.append((n, result))
        
        return np.array(results)
    
    def _classify_points(self, points: np.ndarray, values: np.ndarray, dimensions: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Clasifica puntos para visualización según si están dentro o fuera
        del dominio de éxito (valores positivos vs negativos)
        """
        mask_inside = values >= 0
        mask_outside = ~mask_inside
        
        points_inside = points[mask_inside]
        points_outside = points[mask_outside]
        
        return points_inside, points_outside


# Funciones predeterminadas para testing
DEFAULT_FUNCTIONS = {
    '1D': {
        'sin(x)': lambda x: np.sin(x),
        'x²': lambda x: x**2,
        'e^(-x²)': lambda x: np.exp(-x**2),
        'sqrt(1-x²)': lambda x: np.sqrt(1-x**2) if abs(x) <= 1 else 0
    },
    '2D': {
        'x² + y²': lambda x, y: x**2 + y**2,
        'sin(x)cos(y)': lambda x, y: np.sin(x) * np.cos(y),
        'e^(-(x²+y²))': lambda x, y: np.exp(-(x**2 + y**2))
    }
}

def get_formula_latex(formula_name: str, dimensions: int) -> str:
    """Devuelve la fórmula LaTeX para visualización"""
    formulas_1d = {
        'sin(x)': r'$\sin(x)$',
        'x²': r'$x^2$',
        'e^(-x²)': r'$e^{-x^2}$',
        'sqrt(1-x²)': r'$\sqrt{1-x^2}$'
    }
    
    formulas_2d = {
        'x² + y²': r'$x^2 + y^2$',
        'sin(x)cos(y)': r'$\sin(x)\cos(y)$',
        'e^(-(x²+y²))': r'$e^{-(x^2+y^2)}$'
    }
    
    if dimensions == 1:
        return formulas_1d.get(formula_name, formula_name)
    else:
        return formulas_2d.get(formula_name, formula_name)
