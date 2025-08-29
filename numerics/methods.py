"""
Módulo de Métodos Numéricos
Implementa todos los algoritmos matemáticos requeridos

Métodos incluidos:
- Ecuaciones diferenciales (Runge-Kutta)
- Integración numérica (Newton-Cotes)
- Derivación numérica (diferencias finitas centrales)
- Métodos de raíces (bisección, Newton-Raphson, punto fijo)
- Interpolación (Lagrange)
- Aceleración de convergencia (Aitken)
"""

import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import fsolve
import sympy as sp
from typing import Callable, Tuple, List, Optional

class NumericalMethods:
    """
    Clase que encapsula todos los métodos numéricos
    """
    
    @staticmethod
    def runge_kutta_4(f: Callable, t_span: Tuple[float, float], y0: float, 
                     n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resuelve una ecuación diferencial usando Runge-Kutta de 4to orden
        
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
    def runge_kutta_scipy(f: Callable, t_span: Tuple[float, float], y0: float,
                         n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resuelve ecuación diferencial usando scipy.integrate.solve_ivp
        
        Args:
            f: Función f(t, y) que define dy/dt = f(t, y)
            t_span: Tupla (t0, tf) con el intervalo de tiempo
            y0: Condición inicial
            n_points: Número de puntos
            
        Returns:
            Tupla (t, y) con la solución
        """
        t_eval = np.linspace(t_span[0], t_span[1], n_points)
        sol = solve_ivp(lambda t, y: f(t, y[0]), t_span, [y0], 
                       t_eval=t_eval, method='RK45')
        return sol.t, sol.y[0]
    
    @staticmethod
    def newton_cotes_integration(f: Callable, a: float, b: float, 
                               n: int = 100) -> float:
        """
        Integración numérica usando reglas de Newton-Cotes
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            n: Número de subdivisiones (debe ser par para Simpson)
            
        Returns:
            Valor de la integral aproximada
        """
        if n % 2 != 0:
            n += 1  # Asegurar que n sea par para regla de Simpson
        
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])
        
        # Regla de Simpson 1/3
        integral = h/3 * (y[0] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-2:2]) + y[-1])
        return integral
    
    @staticmethod
    def central_difference_derivative(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Derivada numérica usando diferencias finitas centrales
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f'(x)
        """
        return (f(x + h) - f(x - h)) / (2 * h)
    
    @staticmethod
    def central_difference_second_derivative(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Segunda derivada numérica usando diferencias finitas centrales
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la segunda derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f''(x)
        """
        return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)
    
    @staticmethod
    def bisection_method(f: Callable, a: float, b: float, 
                        tol: float = 1e-6, max_iter: int = 100) -> Tuple[float, int, List[float]]:
        """
        Método de bisección para encontrar raíces
        
        Args:
            f: Función continua
            a, b: Intervalo inicial [a, b] donde f(a)*f(b) < 0
            tol: Tolerancia para convergencia
            max_iter: Máximo número de iteraciones
            
        Returns:
            Tupla (raíz, iteraciones, historial)
        """
        if f(a) * f(b) >= 0:
            raise ValueError("La función debe tener signos opuestos en los extremos")
        
        history = []
        for i in range(max_iter):
            c = (a + b) / 2
            history.append(c)
            
            if abs(f(c)) < tol or abs(b - a) / 2 < tol:
                return c, i + 1, history
            
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        
        return c, max_iter, history
    
    @staticmethod
    def newton_raphson_method(f: Callable, df: Callable, x0: float,
                             tol: float = 1e-6, max_iter: int = 100) -> Tuple[float, int, List[float]]:
        """
        Método de Newton-Raphson para encontrar raíces
        
        Args:
            f: Función
            df: Derivada de la función
            x0: Aproximación inicial
            tol: Tolerancia
            max_iter: Máximo número de iteraciones
            
        Returns:
            Tupla (raíz, iteraciones, historial)
        """
        x = x0
        history = [x0]
        
        for i in range(max_iter):
            fx = f(x)
            dfx = df(x)
            
            if abs(dfx) < 1e-14:
                raise ValueError("Derivada muy pequeña, método puede no converger")
            
            x_new = x - fx / dfx
            history.append(x_new)
            
            if abs(x_new - x) < tol:
                return x_new, i + 1, history
            
            x = x_new
        
        return x, max_iter, history
    
    @staticmethod
    def fixed_point_method(g: Callable, x0: float, tol: float = 1e-6,
                          max_iter: int = 100) -> Tuple[float, int, List[float]]:
        """
        Método de punto fijo para resolver x = g(x)
        
        Args:
            g: Función de iteración g(x)
            x0: Aproximación inicial
            tol: Tolerancia
            max_iter: Máximo número de iteraciones
            
        Returns:
            Tupla (punto_fijo, iteraciones, historial)
        """
        x = x0
        history = [x0]
        
        for i in range(max_iter):
            x_new = g(x)
            history.append(x_new)
            
            if abs(x_new - x) < tol:
                return x_new, i + 1, history
            
            x = x_new
        
        return x, max_iter, history
    
    @staticmethod
    def aitken_acceleration(sequence: List[float]) -> List[float]:
        """
        Aceleración de Aitken para mejorar convergencia
        
        Args:
            sequence: Secuencia de aproximaciones
            
        Returns:
            Secuencia acelerada
        """
        if len(sequence) < 3:
            return sequence
        
        accelerated = []
        for i in range(len(sequence) - 2):
            x_n = sequence[i]
            x_n1 = sequence[i + 1]
            x_n2 = sequence[i + 2]
            
            denominator = x_n2 - 2*x_n1 + x_n
            if abs(denominator) > 1e-14:
                x_acc = x_n - (x_n1 - x_n)**2 / denominator
                accelerated.append(x_acc)
            else:
                accelerated.append(x_n2)
        
        return accelerated
    
    @staticmethod
    def aitken_method(g, x0: float, tol: float = 1e-6, max_iter: int = 100):
        """
        Método de Aitken para encontrar raíces usando función de iteración
        
        Args:
            g: Función de iteración g(x)
            x0: Aproximación inicial
            tol: Tolerancia para convergencia
            max_iter: Máximo número de iteraciones
            
        Returns:
            Tupla: (raíz, iteraciones, historial)
        """
        history = [x0]
        x = x0
        
        for iteration in range(max_iter):
            # Generar secuencia usando g(x)
            x_new = g(x)
            history.append(x_new)
            
            # Aplicar aceleración de Aitken si tenemos suficientes puntos
            if len(history) >= 3:
                # Aplicar Aitken a los últimos 3 puntos
                last_three = history[-3:]
                accelerated = NumericalMethods.aitken_acceleration(last_three)
                
                if accelerated:
                    x_acc = accelerated[-1]  # Último valor acelerado
                    
                    # Verificar convergencia con el valor acelerado
                    if abs(x_acc - x) < tol:
                        return x_acc, iteration + 1, history
                    
                    x = x_acc
                    history.append(x_acc)
                else:
                    x = x_new
            else:
                x = x_new
            
            # Verificar convergencia sin aceleración
            if abs(x - history[-2]) < tol and len(history) > 1:
                return x, iteration + 1, history
        
        # Si no converge, devolver el último valor
        return x, max_iter, history
    
    @staticmethod
    def lagrange_interpolation(x_points: np.ndarray, y_points: np.ndarray, x: float) -> float:
        """
        Interpolación de Lagrange
        
        Args:
            x_points: Puntos x conocidos
            y_points: Puntos y conocidos
            x: Punto donde evaluar la interpolación
            
        Returns:
            Valor interpolado en x
        """
        n = len(x_points)
        result = 0
        
        for i in range(n):
            # Calcular el polinomio base de Lagrange L_i(x)
            Li = 1
            for j in range(n):
                if i != j:
                    Li *= (x - x_points[j]) / (x_points[i] - x_points[j])
            
            result += y_points[i] * Li
        
        return result
    
    @staticmethod
    def lagrange_polynomial(x_points: np.ndarray, y_points: np.ndarray) -> Callable:
        """
        Genera el polinomio de interpolación de Lagrange como función
        
        Args:
            x_points: Puntos x conocidos
            y_points: Puntos y conocidos
            
        Returns:
            Función que evalúa el polinomio de Lagrange
        """
        def polynomial(x):
            return NumericalMethods.lagrange_interpolation(x_points, y_points, x)
        
        return polynomial

# Funciones auxiliares para parsing de expresiones matemáticas
class MathParser:
    """
    Clase para parsear y evaluar expresiones matemáticas ingresadas por el usuario
    """
    
    @staticmethod
    def parse_function(expression: str) -> Callable:
        """
        Convierte una expresión string en una función evaluable
        
        Args:
            expression: Expresión matemática como string (ej: "x**2 + 2*x + 1")
            
        Returns:
            Función que puede ser evaluada
        """
        # Reemplazar funciones comunes por sus equivalentes numpy
        expression = expression.replace('^', '**')
        expression = expression.replace('sin', 'np.sin')
        expression = expression.replace('cos', 'np.cos')
        expression = expression.replace('tan', 'np.tan')
        expression = expression.replace('exp', 'np.exp')
        expression = expression.replace('log', 'np.log')
        expression = expression.replace('sqrt', 'np.sqrt')
        expression = expression.replace('pi', 'np.pi')
        expression = expression.replace('e', 'np.e')
        
        def func(x):
            return eval(expression, {"np": np, "x": x})
        
        return func
    
    @staticmethod
    def parse_ode_function(expression: str) -> Callable:
        """
        Parsea una función para ecuaciones diferenciales dy/dt = f(t, y)
        
        Args:
            expression: Expresión como string (ej: "t + y", "-y + t**2")
            
        Returns:
            Función f(t, y)
        """
        expression = expression.replace('^', '**')
        expression = expression.replace('sin', 'np.sin')
        expression = expression.replace('cos', 'np.cos')
        expression = expression.replace('tan', 'np.tan')
        expression = expression.replace('exp', 'np.exp')
        expression = expression.replace('log', 'np.log')
        expression = expression.replace('sqrt', 'np.sqrt')
        expression = expression.replace('pi', 'np.pi')
        expression = expression.replace('e', 'np.e')
        
        def func(t, y):
            return eval(expression, {"np": np, "t": t, "y": y})
        
        return func
