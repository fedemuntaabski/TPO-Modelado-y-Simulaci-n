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
    
    # ================================ MÉTODOS ECUACIONES DIFERENCIALES ================================
    
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
    def euler_ode(f: Callable, x0: float, y0: float, xf: float, n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Método de Euler para EDO con signature alternativa
        
        Args:
            f: Función f(x, y) que define dy/dx = f(x, y)
            x0: Valor inicial de x
            y0: Condición inicial y(x0) = y0
            xf: Valor final de x
            n_points: Número de puntos de evaluación
            
        Returns:
            Tupla (x, y) con los puntos de la solución
        """
        h = (xf - x0) / n_points
        x = np.linspace(x0, xf, n_points + 1)
        y = np.zeros(n_points + 1)
        y[0] = y0
        
        for i in range(n_points):
            y[i + 1] = y[i] + h * f(x[i], y[i])
        
        return x, y
    
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
        Runge-Kutta de 4to orden (RK4) - alias de runge_kutta_4
        
        Args:
            f: Función f(t, y) que define dy/dt = f(t, y)
            t_span: Tupla (t0, tf) con el intervalo de tiempo
            y0: Condición inicial y(t0) = y0
            n_points: Número de puntos de evaluación
            
        Returns:
            Tupla (t, y) con los puntos de la solución
        """
        return NumericalMethods.runge_kutta_4(f, t_span, y0, n_points)
    
    # ================================ MÉTODOS DE INTEGRACIÓN ================================
    
    @staticmethod
    def trapezoid(f: Callable, a: float, b: float, n: int = 100) -> float:
        """
        Regla del Trapecio para integración numérica
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            n: Número de subdivisiones
            
        Returns:
            Valor de la integral aproximada
        """
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])
        
        # Regla del trapecio: h/2 * (y0 + 2*(y1 + y2 + ... + yn-1) + yn)
        integral = h/2 * (y[0] + 2*np.sum(y[1:-1]) + y[-1])
        return integral
    
    @staticmethod
    def simpson_13(f: Callable, a: float, b: float, n: int = 100) -> float:
        """
        Regla de Simpson 1/3 para integración numérica
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            n: Número de subdivisiones (debe ser par)
            
        Returns:
            Valor de la integral aproximada
        """
        if n % 2 != 0:
            n += 1  # Asegurar que n sea par
        
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])
        
        # Regla de Simpson 1/3
        integral = h/3 * (y[0] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-2:2]) + y[-1])
        return integral
    
    @staticmethod
    def simpson_38(f: Callable, a: float, b: float, n: int = 100) -> float:
        """
        Regla de Simpson 3/8 para integración numérica
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            n: Número de subdivisiones (debe ser múltiplo de 3)
            
        Returns:
            Valor de la integral aproximada
        """
        if n % 3 != 0:
            n = ((n // 3) + 1) * 3  # Asegurar que n sea múltiplo de 3
        
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])
        
        # Regla de Simpson 3/8
        integral = 3*h/8 * (y[0] + 3*np.sum(y[1:-1:3]) + 3*np.sum(y[2:-1:3]) + 2*np.sum(y[3:-1:3]) + y[-1])
        return integral
    
    @staticmethod
    def newton_cotes_integration(f: Callable, a: float, b: float, 
                               n: int = 100) -> float:
        """
        Integración numérica usando reglas de Newton-Cotes (Simpson 1/3)
        
        Args:
            f: Función a integrar
            a, b: Límites de integración
            n: Número de subdivisiones (debe ser par para Simpson)
            
        Returns:
            Valor de la integral aproximada
        """
        return NumericalMethods.simpson_13(f, a, b, n)
    
    @staticmethod
    def trapezoidal_integration(f: Callable, a: float, b: float, n: int = 100) -> float:
        """
        Integración usando regla del trapecio - alias de trapezoid
        """
        return NumericalMethods.trapezoid(f, a, b, n)
    
    @staticmethod
    def simpson_integration(f: Callable, a: float, b: float, n: int = 100) -> float:
        """
        Integración usando regla de Simpson - alias de simpson_13
        """
        return NumericalMethods.simpson_13(f, a, b, n)
    
    # ================================ ALIASES PARA COMPATIBILIDAD CON TESTS ================================
    
    @staticmethod
    def bisection(f: Callable, a: float, b: float, tolerance: float = 1e-6, max_iterations: int = 100):
        """
        Alias para bisection_method con signature compatible con tests
        """
        root, iterations, history = NumericalMethods.bisection_method(f, a, b, tolerance, max_iterations)
        return root, iterations, history
    
    @staticmethod
    def newton_raphson(f: Callable, df: Callable, x0: float, tolerance: float = 1e-6, max_iterations: int = 100):
        """
        Alias para newton_raphson_method con signature compatible con tests
        """
        root, iterations, history = NumericalMethods.newton_raphson_method(f, df, x0, tolerance, max_iterations)
        return root, iterations, history
    
    # ================================ MÉTODOS DE DIFERENCIAS FINITAS ================================
    
    @staticmethod
    def forward(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Diferencias hacia adelante para derivadas
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f'(x) usando diferencias hacia adelante
        """
        return (f(x + h) - f(x)) / h
    
    @staticmethod
    def backward(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Diferencias hacia atrás para derivadas
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f'(x) usando diferencias hacia atrás
        """
        return (f(x) - f(x - h)) / h
    
    @staticmethod
    def central(f: Callable, x: float, h: float = 1e-5) -> float:
        """
        Diferencias centrales para derivadas - alias de central_difference_derivative
        
        Args:
            f: Función a derivar
            x: Punto donde evaluar la derivada
            h: Paso para la diferencia finita
            
        Returns:
            Aproximación de f'(x) usando diferencias centrales
        """
        return NumericalMethods.central_difference_derivative(f, x, h)
    
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
    
    # Alias para compatibilidad
    fixed_point = fixed_point_method
    
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
            Tupla: (raíz, iteraciones, historial, historial_acelerado, pasos_detallados)
            historial_acelerado: Lista de valores después de aplicar Aitken
            pasos_detallados: Lista de diccionarios con información detallada de cada paso
        """
        history = [x0]  # Valores originales de g(x)
        accelerated_history = []  # Valores después de aplicar Aitken
        detailed_steps = []  # Información detallada de cada paso

        x = x0

        for iteration in range(max_iter):
            # Generar nuevo valor usando g(x)
            x_new = g(x)

            # Registrar paso detallado
            step_info = {
                'iteracion': iteration + 1,
                'x_anterior': x,
                'g_x_anterior': x_new,
                'x0_x1_x2': None,  # Se llenará cuando tengamos suficientes puntos
                'x_acelerado': None,
                'error_abs': None,
                'error_rel': None
            }

            history.append(x_new)

            # Aplicar aceleración de Aitken si tenemos suficientes puntos
            if len(history) >= 3:
                # Aplicar Aitken a los últimos 3 puntos
                last_three = history[-3:]
                step_info['x0_x1_x2'] = last_three.copy()

                accelerated = NumericalMethods.aitken_acceleration(last_three)

                if accelerated:
                    x_acc = accelerated[-1]  # Último valor acelerado
                    step_info['x_acelerado'] = x_acc
                    accelerated_history.append(x_acc)

                    # Calcular errores
                    step_info['error_abs'] = abs(x_acc - x)
                    step_info['error_rel'] = abs(x_acc - x) / abs(x_acc) if abs(x_acc) > 1e-14 else 0

                    # Verificar convergencia con el valor acelerado
                    if abs(x_acc - x) < tol:
                        detailed_steps.append(step_info)
                        return x_acc, iteration + 1, history, accelerated_history, detailed_steps

                    x = x_acc
                else:
                    x = x_new
            else:
                x = x_new

            detailed_steps.append(step_info)

            # Verificar convergencia sin aceleración
            if abs(x - history[-2]) < tol and len(history) > 1:
                return x, iteration + 1, history, accelerated_history, detailed_steps

        # Si no converge, devolver último valor
        return x, max_iter, history, accelerated_history, detailed_steps
    
    @staticmethod
    def parse_function(expression: str) -> Callable:
        """
        Parsea una función matemática f(x)
        
        Args:
            expression: Expresión como string (ej: "x**2", "sin(x)", "x**2 - 4")
            
        Returns:
            Función f(x) evaluable
        """
        expression = expression.replace('^', '**')
        
        def func(x):
            # Crear un namespace seguro con numpy y math
            import math
            safe_dict = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'exp': math.exp,
                'log': math.log,
                'log10': math.log10,
                'sqrt': math.sqrt,
                'pi': math.pi,
                'e': math.e,
                'x': x
            }
            return eval(expression, {"__builtins__": {}}, safe_dict)
        
        return func
    
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

class MathParser:
    """
    Parser matemático para evaluar expresiones
    """
    
    @staticmethod
    def evaluate_expression(expression: str, x: float = 0) -> float:
        """
        Evalúa una expresión matemática en un punto dado
        
        Args:
            expression: Expresión como string
            x: Valor donde evaluar la expresión
            
        Returns:
            Resultado numérico de la evaluación
        """
        try:
            func = NumericalMethods.parse_function(expression)
            return func(x)
        except Exception as e:
            raise ValueError(f"Error evaluando expresión: {e}")
    
    @staticmethod
    def parse_function(expression: str) -> Callable:
        """
        Parsea una función matemática
        
        Args:
            expression: Expresión como string
            
        Returns:
            Función evaluable
        """
        return NumericalMethods.parse_function(expression)
    
    @staticmethod
    def parse_ode_function(expression: str) -> Callable:
        """
        Parsea una función para ecuaciones diferenciales
        
        Args:
            expression: Expresión como string
            
        Returns:
            Función f(t, y)
        """
        return NumericalMethods.parse_ode_function(expression)
