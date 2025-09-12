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
    
    def simular(self, 
                func: Callable,
                n: int,
                semilla: Optional[int] = None,
                error_maximo: float = 0.05,
                dimensiones: int = 1,
                rango_x: Tuple[float, float] = (0, 1),
                rango_y: Optional[Tuple[float, float]] = None) -> Dict:
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
        if n <= 0:
            raise ValueError("El número de muestras debe ser positivo")
        
        if dimensiones not in [1, 2]:
            raise ValueError("Solo se admiten integraciones 1D o 2D")
        
        if dimensiones == 2 and rango_y is None:
            raise ValueError("Para integraciones 2D se requiere el rango y")
        
        # Establecer semilla si se proporciona
        if semilla is not None:
            np.random.seed(semilla)
        
        # Calcular volumen del dominio
        volumen = self._calcular_volumen(dimensiones, rango_x, rango_y)
        
        # Generar puntos aleatorios
        puntos, valores_puntos = self._generar_puntos(func, n, dimensiones, rango_x, rango_y)
        
        # Calcular el resultado de la integración
        resultado_integracion = self._calcular_integracion(valores_puntos, volumen)
        
        # Calcular estadísticas
        desviacion_estandar, error_estandar, intervalo_de_confianza = self._calcular_estadisticas(valores_puntos, volumen, error_maximo)
        
        # Generar datos para visualización de convergencia
        convergence_data = self._calcular_convergencia(func, n, dimensiones, rango_x, volumen, rango_y)
        
        # Separar puntos para visualización
        puntos_exito, puntos_fracaso = self._clasificar_puntos_exito_fracaso(puntos, valores_puntos, dimensiones)
        
        # Guardar resultados
        self._last_results = {
            'desviacion_estandar': desviacion_estandar,
            'error_estandar': error_estandar,
            'intervalo_confianza': intervalo_de_confianza,
            'volumen': volumen,
            'resultado_integracion': resultado_integracion,
            'puntos_dentro': puntos_exito,
            'puntos_fuera': puntos_fracaso,
            'convergencia': convergence_data
        }
        
        return self._last_results
    
    def _calcular_volumen(self, dimension: int, rango_x: Tuple[float, float], 
                          rango_y: Optional[Tuple[float, float]] = None) -> float:
        """Calcula el volumen del dominio de integración"""
        volumen_x = rango_x[1] - rango_x[0]
        
        if dimension == 1:
            return volumen_x
        else:
            volumen_y = rango_y[1] - rango_y[0]
            return volumen_x * volumen_y
    
    def _generar_puntos(self, func: Callable, n: int, dimension: int,
                        rango_x: Tuple[float, float], 
                        rango_y: Optional[Tuple[float, float]] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Genera puntos aleatorios y evalúa la función en ellos"""
        if dimension == 1:
            # Generar puntos aleatorios 1D
            x = np.random.uniform(rango_x[0], rango_x[1], n)
            puntos = x.reshape(-1, 1)
            valores = np.array([func(xi) for xi in x])
            
        else:
            # Generar puntos aleatorios 2D
            x = np.random.uniform(rango_x[0], rango_x[1], n)
            y = np.random.uniform(rango_y[0], rango_y[1], n)
            puntos = np.column_stack((x, y))
            valores = np.array([func(xi, yi) for xi, yi in zip(x, y)])
        
        return puntos, valores
    
    def _calcular_integracion(self, valores: np.ndarray, volumen: float) -> float:
        """Calcula el resultado de la integración mediante Monte Carlo"""
        return volumen * np.mean(valores)
    
    def _calcular_estadisticas(self, valores: np.ndarray, volumen: float, 
                             error_maximo: float) -> Tuple[float, float, Tuple[float, float]]:
        """Calcula estadísticas de la simulación"""
        # Desviación estándar
        std_dev = np.std(valores, ddof=1)
        
        # Error estándar
        n = len(valores)
        std_error = std_dev / np.sqrt(n)
        
        # Intervalo de confianza adaptado al error máximo
        # Convertir error_maximo a nivel de confianza
        # Por ejemplo, error_maximo=0.05 corresponde a 95% de confianza (1-0.05)
        nivel_confianza = 1 - error_maximo
        
        # Calcular el valor z para el nivel de confianza deseado
        # Ejemplo: Para 95% de confianza (error_maximo=0.05), z_value ≈ 1.96
        # Para 99% de confianza (error_maximo=0.01), z_value ≈ 2.58
        z_value = stats.norm.ppf(1 - error_maximo/2)
        
        margen_de_error = z_value * std_error
        mean_value = np.mean(valores)
        
        # Ajustar el resultado por el volumen
        adjusted_error = volumen * margen_de_error
        adjusted_mean = volumen * mean_value
        
        intervalo_de_confianza = (adjusted_mean - adjusted_error, adjusted_mean + adjusted_error)
        
        return std_dev, std_error * volumen, intervalo_de_confianza
    
    def _calcular_convergencia(self, func: Callable, n_samples: int, dimensions: int,
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
            points, values = self._generar_puntos(func, n, dimensions, x_range, y_range)
            result = volume * np.mean(values)
            results.append((n, result))
        
        return np.array(results)
    
    def _clasificar_puntos_exito_fracaso(self, points: np.ndarray, values: np.ndarray, dimensions: int) -> Tuple[np.ndarray, np.ndarray]:
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
