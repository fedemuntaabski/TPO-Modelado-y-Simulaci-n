"""
Ecuaciones Diferenciales Ordinarias
Implementa métodos para resolver EDO de primer orden

Métodos incluidos:
- Método de Euler
- Runge-Kutta de 2do orden (RK2)
- Runge-Kutta de 4to orden (RK4)
- Runge-Kutta-Fehlberg (RK45) para control de error
"""

import numpy as np
from typing import Callable, Tuple
from scipy.integrate import solve_ivp

class DifferentialEquations:
    """
    Clase que implementa métodos para resolver ecuaciones diferenciales ordinarias
    """
    
    @staticmethod
    def euler(f: Callable, t_span: Tuple[float, float], y0: float, 
             n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Método de Euler para ecuaciones diferenciales
        
        Args:
            f: Función f(t, y) que define dy/dt = f(t, y)
            t_span: Tupla (t0, tf) con el intervalo de tiempo
            y0: Condición inicial y(t0) = y0
            n_points: Número de puntos de evaluación
            
        Returns:
            Tupla (t, y) con los puntos de la solución
        """
        t0, tf = t_span
        h = (tf - t0) / (n_points - 1)
        t = np.linspace(t0, tf, n_points)
        y = np.zeros(n_points)
        y[0] = y0
        
        for i in range(n_points - 1):
            y[i + 1] = y[i] + h * f(t[i], y[i])
        
        return t, y
    
    @staticmethod
    def rk2(f: Callable, t_span: Tuple[float, float], y0: float, 
           n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Runge-Kutta de 2do orden (RK2)
        
        Args:
            f: Función f(t, y) que define dy/dt = f(t, y)
            t_span: Tupla (t0, tf) con el intervalo de tiempo
            y0: Condición inicial y(t0) = y0
            n_points: Número de puntos de evaluación
            
        Returns:
            Tupla (t, y) con los puntos de la solución
        """
        t0, tf = t_span
        h = (tf - t0) / (n_points - 1)
        t = np.linspace(t0, tf, n_points)
        y = np.zeros(n_points)
        y[0] = y0
        
        for i in range(n_points - 1):
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h, y[i] + k1)
            
            y[i + 1] = y[i] + (k1 + k2) / 2
        
        return t, y
    
    @staticmethod
    def rk4(f: Callable, t_span: Tuple[float, float], y0: float, 
           n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Runge-Kutta de 4to orden (RK4)
        
        Args:
            f: Función f(t, y) que define dy/dt = f(t, y)
            t_span: Tupla (t0, tf) con el intervalo de tiempo
            y0: Condición inicial y(t0) = y0
            n_points: Número de puntos de evaluación
            
        Returns:
            Tupla (t, y) con los puntos de la solución
        """
        t0, tf = t_span
        h = (tf - t0) / (n_points - 1)
        t = np.linspace(t0, tf, n_points)
        y = np.zeros(n_points)
        y[0] = y0
        
        for i in range(n_points - 1):
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + k1/2)
            k3 = h * f(t[i] + h/2, y[i] + k2/2)
            k4 = h * f(t[i] + h, y[i] + k3)
            
            y[i + 1] = y[i] + (k1 + 2*k2 + 2*k3 + k4) / 6
        
        return t, y
    
    @staticmethod
    def rk45(f: Callable, t_span: Tuple[float, float], y0: float,
             rtol: float = 1e-6, atol: float = 1e-9) -> Tuple[np.ndarray, np.ndarray]:
        """
        Runge-Kutta-Fehlberg (RK45) con control de error adaptativo
        
        Args:
            f: Función f(t, y) que define dy/dt = f(t, y)
            t_span: Tupla (t0, tf) con el intervalo de tiempo
            y0: Condición inicial y(t0) = y0
            rtol: Tolerancia relativa
            atol: Tolerancia absoluta
            
        Returns:
            Tupla (t, y) con los puntos de la solución
        """
        sol = solve_ivp(lambda t, y: f(t, y[0]), t_span, [y0], 
                       method='RK45', rtol=rtol, atol=atol)
        return sol.t, sol.y[0]
