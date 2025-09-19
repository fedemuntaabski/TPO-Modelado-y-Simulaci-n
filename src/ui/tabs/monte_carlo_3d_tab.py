"""
Pestaña para simulación Monte Carlo en 3D.

Implementa la interfaz gráfica para el método de Monte Carlo en 3D
para calcular volúmenes mediante integración triple.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import math
from typing import Optional, Dict, Callable, Any, Tuple
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import time

from src.ui.components.base_tab import BaseTab
from src.ui.components.mixins import InputValidationMixin, ResultDisplayMixin, PlottingMixin
from src.ui.components.constants import VALIDATION, DEFAULT_CONFIGS, UI, PLOT, COLORS
from config.settings import NUMERICAL_CONFIG


class MonteCarlo3DEngine:
    """Implementación simplificada de Monte Carlo en 3D para cálculo de volúmenes"""
    
    def simulate(self, func, n_samples, seed=42, x_range=(0,1), y_range=(0,1), z_range=(0,1), max_error=0.05):
        """Simulación Monte Carlo para integrales triples (3D)"""
        np.random.seed(seed)
        
        # Generar puntos aleatorios en el dominio 3D
        x_points = np.random.uniform(x_range[0], x_range[1], n_samples)
        y_points = np.random.uniform(y_range[0], y_range[1], n_samples)
        z_points = np.random.uniform(z_range[0], z_range[1], n_samples)
        
        # Calcular valores de la función
        f_values = np.array([func(x, y, z) for x, y, z in zip(x_points, y_points, z_points)])
        
        # Calcular el volumen del dominio
        volume = (x_range[1] - x_range[0]) * (y_range[1] - y_range[0]) * (z_range[1] - z_range[0])
        
        # Para cónicas, f_values contendrá 1.0 para puntos dentro y 0.0 para puntos fuera
        # Para funciones regulares, usamos el signo para determinar puntos dentro/fuera
        if np.all(np.logical_or(f_values == 0.0, f_values == 1.0)):
            # Es una función para cónica (devuelve 0.0 o 1.0)
            inside = f_values > 0.5  # Los puntos con valor 1.0 están dentro
            # Para cónicas, la integral es la fracción de puntos dentro * volumen total
            integral = volume * np.mean(inside)
        
        # Calcular la integral triple (volumen)
        else:
            # Función normal
            inside = f_values > 0
            integral = volume * np.mean(f_values)
        
        # Calcular estadísticas
        if np.all(np.logical_or(f_values == 0.0, f_values == 1.0)):
            # Para cónicas, la desviación estándar se calcula sobre los valores binarios
            std_dev = np.std(f_values * volume)
        else:
            # Para funciones normales
            std_dev = np.std(f_values * volume)
            
        std_error = std_dev / np.sqrt(n_samples)
        
        # Calcular intervalo de confianza
        from scipy import stats
        z_value = stats.norm.ppf(1 - max_error/2)
        confidence_interval = (integral - z_value*std_error, integral + z_value*std_error)
        
        # Separar puntos dentro y fuera para visualización
        # En 3D, consideramos puntos "dentro" si f(x,y,z) > 0
        inside = f_values > 0
        
        points_inside = np.column_stack([x_points[inside], y_points[inside], z_points[inside]])
        points_outside = np.column_stack([x_points[~inside], y_points[~inside], z_points[~inside]])
        
        return {
            'resultado_integracion': integral,
            'desviacion_estandar': std_dev,
            'error_estandar': std_error,
            'intervalo_confianza': confidence_interval,
            'puntos_dentro': points_inside,
            'puntos_fuera': points_outside,
            'volumen': volume,
            'estadisticas': {
                'n_muestras': n_samples,
                'fraccion_dentro': np.mean(inside)
            }
        }


class MonteCarlo3DTab(BaseTab):
    """Pestaña para integración Monte Carlo en 3D."""
    
    def __init__(self, parent):
        super().__init__(parent, "Monte Carlo 3D")
        self.engine = MonteCarlo3DEngine()
        self.result_cache = {}
    
    def create_content(self):
        """Implementar el contenido específico de la pestaña"""
        # Crear secciones principales
        self.create_input_section()
        self.create_control_section()
        self.create_visualization_section()
        self.create_results_section()
    
    def create_input_section(self):
        """Crear sección de entrada de datos"""
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Título de la sección
        section_title = ctk.CTkLabel(
            input_frame,
            text="Configuración",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        section_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Función
        ctk.CTkLabel(input_frame, text="Función f(x,y,z) o cónica:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.function_entry = ctk.CTkEntry(input_frame, placeholder_text="x^2 + y^2 + z^2 = 1")
        self.function_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.function_entry.insert(0, "1 - (x**2 + y**2 + z**2)")
        
        # Descripción para ecuaciones cónicas
        conic_label = ctk.CTkLabel(
            input_frame,
            text="Soporta funciones regulares como '1-(x**2+y**2+z**2)' o ecuaciones cónicas como 'x**2+y**2+z**2=1'",
            text_color=["gray60", "gray50"],
            font=ctk.CTkFont(size=10)
        )
        conic_label.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")
        
        # Límites de integración
        # Para x
        ctk.CTkLabel(input_frame, text="Límite a (min x):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.a_entry = ctk.CTkEntry(input_frame)
        self.a_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.a_entry.insert(0, "-1")
        
        ctk.CTkLabel(input_frame, text="Límite b (max x):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.b_entry = ctk.CTkEntry(input_frame)
        self.b_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.b_entry.insert(0, "1")
        
        # Para y
        ctk.CTkLabel(input_frame, text="Límite c (min y):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.c_entry = ctk.CTkEntry(input_frame)
        self.c_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        self.c_entry.insert(0, "-1")
        
        ctk.CTkLabel(input_frame, text="Límite d (max y):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.d_entry = ctk.CTkEntry(input_frame)
        self.d_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        self.d_entry.insert(0, "1")
        
        # Para z
        ctk.CTkLabel(input_frame, text="Límite e (min z):").grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.e_entry = ctk.CTkEntry(input_frame)
        self.e_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")
        self.e_entry.insert(0, "-1")
        
        ctk.CTkLabel(input_frame, text="Límite f (max z):").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.f_entry = ctk.CTkEntry(input_frame)
        self.f_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
        self.f_entry.insert(0, "1")
        
        # Número de muestras
        ctk.CTkLabel(input_frame, text="Número de muestras:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.n_samples_entry = ctk.CTkEntry(input_frame)
        self.n_samples_entry.grid(row=9, column=1, padx=10, pady=5, sticky="ew")
        self.n_samples_entry.insert(0, "10000")
        
        # Error máximo
        ctk.CTkLabel(input_frame, text="Error máximo:").grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.max_error_entry = ctk.CTkEntry(input_frame)
        self.max_error_entry.grid(row=10, column=1, padx=10, pady=5, sticky="ew")
        self.max_error_entry.insert(0, "0.05")
        
        # Semilla
        ctk.CTkLabel(input_frame, text="Semilla (opcional):").grid(row=11, column=0, padx=10, pady=5, sticky="w")
        self.seed_entry = ctk.CTkEntry(input_frame)
        self.seed_entry.grid(row=11, column=1, padx=10, pady=5, sticky="ew")
        self.seed_entry.insert(0, "42")
    
    def create_control_section(self):
        """Crear sección de controles"""
        button_frame = ctk.CTkFrame(self.content_frame)
        button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # Botón Calcular
        self.calculate_button = ctk.CTkButton(
            button_frame,
            text="Calcular",
            command=self.run_monte_carlo,
            height=40,
            fg_color=COLORS.PRIMARY
        )
        self.calculate_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Botón Limpiar
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Limpiar",
            command=self.clear_results,
            height=40,
            fg_color=COLORS.SECONDARY
        )
        self.clear_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    def create_visualization_section(self):
        """Crear sección de visualización"""
        vis_frame = ctk.CTkFrame(self.content_frame)
        vis_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        vis_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        vis_title = ctk.CTkLabel(
            vis_frame,
            text="Visualización 3D",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        vis_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Crear figura 3D
        self.fig = Figure(figsize=(6, 5))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Integración Monte Carlo 3D')
        
        # Crear canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=vis_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def create_results_section(self):
        """Crear sección de resultados"""
        results_frame = ctk.CTkFrame(self.content_frame)
        results_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        results_title = ctk.CTkLabel(
            results_frame,
            text="Resultados",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Crear widgets para resultados (inicialmente vacíos)
        self.result_labels = {}
        
        result_fields = [
            ("Resultado integral", "resultado_integracion"),
            ("Desviación estándar", "desviacion_estandar"),
            ("Error estándar", "error_estandar"),
            ("Intervalo de confianza", "intervalo_confianza"),
            ("Volumen del dominio", "volumen")
        ]
        
        for i, (label_text, key) in enumerate(result_fields):
            label = ctk.CTkLabel(results_frame, text=f"{label_text}:")
            label.grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            
            value_label = ctk.CTkLabel(results_frame, text="")
            value_label.grid(row=i+1, column=1, padx=10, pady=5, sticky="e")
            
            self.result_labels[key] = value_label
    
    def _create_funcion_3d(self, expression):
        """Crear función 3D de manera segura"""
        import math
        import numpy as np
        
        # Comprobar si es una ecuación cónica (contiene un '=')
        if '=' in expression:
            # Separar la ecuación en lado izquierdo y derecho
            left_side, right_side = expression.split('=', 1)
            left_side = left_side.strip()
            right_side = right_side.strip()
            
            def safe_eval_conic(expr, x, y, z):
                # Reemplazar funciones comunes
                expr = expr.replace('^', '**')
                expr = expr.replace('e^', 'exp(')
                expr = expr.replace('ln(', 'log(')
                
                # Crear namespace seguro
                safe_dict = {
                    'x': x,
                    'y': y,
                    'z': z,
                    'sin': math.sin,
                    'cos': math.cos,
                    'tan': math.tan,
                    'exp': math.exp,
                    'log': math.log,
                    'sqrt': math.sqrt,
                    'pi': math.pi,
                    'e': math.e,
                    'abs': abs,
                    'np': np
                }
                
                return eval(expr, {"__builtins__": {}}, safe_dict)
            
            # Crear función que evalúa si un punto está dentro de la región definida por la cónica
            def conic_function(x_val, y_val, z_val):
                left_result = safe_eval_conic(left_side, x_val, y_val, z_val)
                right_result = safe_eval_conic(right_side, x_val, y_val, z_val)
                
                # Para Monte Carlo 3D, consideramos puntos dentro si la diferencia es ≤ 0
                # Ejemplo: para x^2 + y^2 + z^2 = 1, los puntos dentro cumplen x^2 + y^2 + z^2 <= 1
                if left_result <= right_result:
                    return 1.0  # Punto dentro
                else:
                    return 0.0  # Punto fuera
            
            return conic_function
        else:
            # Función normal (no cónica)
            def safe_eval(expr, x, y, z):
                # Reemplazar funciones comunes
                expr = expr.replace('^', '**')
                expr = expr.replace('e^', 'exp(')
                expr = expr.replace('ln(', 'log(')
                
                # Crear namespace seguro
                safe_dict = {
                    'x': x,
                    'y': y,
                    'z': z,
                    'sin': math.sin,
                    'cos': math.cos,
                    'tan': math.tan,
                    'exp': math.exp,
                    'log': math.log,
                    'sqrt': math.sqrt,
                    'pi': math.pi,
                    'e': math.e,
                    'abs': abs,
                    'np': np
                }
                
                return eval(expr, {"__builtins__": {}}, safe_dict)
            
            return lambda x_val, y_val, z_val: safe_eval(expression, x_val, y_val, z_val)
    
    def run_monte_carlo(self):
        """Ejecutar la simulación Monte Carlo 3D"""
        try:
            # Leer datos de entrada
            func_str = self.function_entry.get().strip()
            a = float(self.a_entry.get().strip())
            b = float(self.b_entry.get().strip())
            c = float(self.c_entry.get().strip())
            d = float(self.d_entry.get().strip())
            e = float(self.e_entry.get().strip())
            f = float(self.f_entry.get().strip())
            n_samples = int(self.n_samples_entry.get().strip())
            max_error = float(self.max_error_entry.get().strip())
            
            # Semilla opcional
            seed_str = self.seed_entry.get().strip()
            seed = int(seed_str) if seed_str else None
            
            # Crear función
            func = self._create_funcion_3d(func_str)
            
            # Ejecutar Monte Carlo
            start_time = time.time()
            results = self.engine.simulate(
                func, 
                n_samples, 
                seed=seed, 
                x_range=(a, b), 
                y_range=(c, d), 
                z_range=(e, f), 
                max_error=max_error
            )
            end_time = time.time()
            
            # Guardar resultados en caché
            self.result_cache = results
            self.result_cache['tiempo_calculo'] = end_time - start_time
            
            # Mostrar resultados
            self.display_results(results)
            
            # Visualizar resultados
            self.visualize_results(results)
            
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def display_results(self, results):
        """Mostrar resultados en la interfaz"""
        # Mostrar resultados numéricos
        self.result_labels["resultado_integracion"].configure(
            text=f"{results['resultado_integracion']:.8f}"
        )
        
        self.result_labels["desviacion_estandar"].configure(
            text=f"{results['desviacion_estandar']:.8f}"
        )
        
        self.result_labels["error_estandar"].configure(
            text=f"{results['error_estandar']:.8f}"
        )
        
        ci = results["intervalo_confianza"]
        self.result_labels["intervalo_confianza"].configure(
            text=f"({ci[0]:.8f}, {ci[1]:.8f})"
        )
        
        self.result_labels["volumen"].configure(
            text=f"{results['volumen']:.8f}"
        )
    
    def visualize_results(self, results):
        """Visualizar resultados en el gráfico 3D"""
        self.ax.clear()
        
        points_inside = results.get('puntos_dentro', np.array([]))
        points_outside = results.get('puntos_fuera', np.array([]))
        
        # Si hay puntos para visualizar
        if len(points_inside) > 0:
            # Limitar el número de puntos para mejor rendimiento
            max_points = 1000
            if len(points_inside) > max_points:
                indices = np.random.choice(len(points_inside), max_points, replace=False)
                points_inside = points_inside[indices]
            
            self.ax.scatter(
                points_inside[:, 0], 
                points_inside[:, 1], 
                points_inside[:, 2], 
                c='green', 
                alpha=0.6, 
                label='Dentro'
            )
        
        if len(points_outside) > 0:
            # Limitar el número de puntos para mejor rendimiento
            max_points = 1000
            if len(points_outside) > max_points:
                indices = np.random.choice(len(points_outside), max_points, replace=False)
                points_outside = points_outside[indices]
            
            self.ax.scatter(
                points_outside[:, 0], 
                points_outside[:, 1], 
                points_outside[:, 2], 
                c='red', 
                alpha=0.3, 
                label='Fuera'
            )
        
        # Configurar límites del gráfico
        x_range = (float(self.a_entry.get()), float(self.b_entry.get()))
        y_range = (float(self.c_entry.get()), float(self.d_entry.get()))
        z_range = (float(self.e_entry.get()), float(self.f_entry.get()))
        
        self.ax.set_xlim(x_range)
        self.ax.set_ylim(y_range)
        self.ax.set_zlim(z_range)
        
        # Verificar si la función es una cónica e intentar visualizarla como superficie
        func_str = self.function_entry.get().strip()
        if '=' in func_str and any(term in func_str for term in ["**2", "^2", "x*x", "y*y", "z*z"]):
            try:
                # Crear malla para superficie
                x = np.linspace(x_range[0], x_range[1], 30)
                y = np.linspace(y_range[0], y_range[1], 30)
                X, Y = np.meshgrid(x, y)
                
                # Separar lados de la ecuación
                left_side, right_side = func_str.split('=', 1)
                left_side = left_side.strip().replace('^', '**')
                right_side = right_side.strip().replace('^', '**')
                
                # Intento de resolver para Z (asumiendo que podemos despejar z)
                # Esto solo funciona para algunas cónicas, como x²+y²+z²=1
                if "z**2" in left_side and right_side.replace(' ', '').isdigit():
                    # Caso particular: x²+y²+z²=R² (esfera)
                    # Despejamos z = sqrt(R² - x² - y²)
                    radius_squared = float(right_side)
                    expr = left_side.replace("z**2", "0")  # Quitamos z² temporalmente
                    
                    # Definir namespace seguro para eval
                    def safe_eval_surf(expr, x, y):
                        safe_dict = {
                            'x': x, 'y': y, 'np': np,
                            'sin': np.sin, 'cos': np.cos, 'sqrt': np.sqrt
                        }
                        return eval(expr, {"__builtins__": {}}, safe_dict)
                    
                    # Calcular el resto de la expresión
                    rest_expr = np.vectorize(lambda x, y: safe_eval_surf(expr, x, y))(X, Y)
                    
                    # z² = R² - resto, por lo que z = sqrt(R² - resto)
                    under_root = radius_squared - rest_expr
                    
                    # Solo mostrar puntos donde la raíz es real (under_root >= 0)
                    mask_pos = under_root >= 0
                    if np.any(mask_pos):
                        Z_pos = np.sqrt(under_root)
                        Z_pos[~mask_pos] = np.nan  # Marcar como NaN los puntos fuera del dominio
                        self.ax.plot_surface(X, Y, Z_pos, alpha=0.2, color='cyan')
                        
                        # También dibujar la superficie inferior (z negativo)
                        Z_neg = -Z_pos
                        self.ax.plot_surface(X, Y, Z_neg, alpha=0.2, color='cyan')
            except Exception as e:
                # Si falla, continuamos sin mostrar la superficie
                pass
        
        # Etiquetas y título
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title(f'Monte Carlo 3D: {self.function_entry.get()}')
        
        # Leyenda
        if len(points_inside) > 0 or len(points_outside) > 0:
            self.ax.legend()
        
        # Actualizar canvas
        self.canvas.draw()
    
    def clear_results(self):
        """Limpiar resultados y gráficos"""
        # Limpiar etiquetas de resultados
        for label in self.result_labels.values():
            label.configure(text="")
        
        # Limpiar gráfico
        self.ax.clear()
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Integración Monte Carlo 3D')
        self.canvas.draw()
        
        # Limpiar caché de resultados
        self.result_cache = {}
    
    def show_error(self, message):
        """Mostrar mensaje de error"""
        import tkinter as tk
        from tkinter import messagebox
        messagebox.showerror("Error", message)