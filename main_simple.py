#!/usr/bin/env python3
"""
Simulador Matemático Avanzado - Versión 4.0 (Modular Simplificado)
Nueva interfaz con sidebar navigation usando componentes modulares
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import logging
from typing import Dict, Any, Optional, Callable
import traceback

# Configurar tema de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Configurar matplotlib para el tema oscuro
plt.style.use('dark_background')

logger = logging.getLogger(__name__)

# Importar componentes modulares
try:
    from src.core.root_finding import RootFinder
    from src.core.integration import NumericalIntegrator
    from src.core.ode_solver import ODESolver
    from src.core.finite_differences import FiniteDifferenceCalculator
    from config.settings import UI_SETTINGS, NUMERICAL_SETTINGS
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Advertencia: No se pudieron importar los módulos modulares: {e}")
    print("Asegúrese de que la estructura modular esté disponible")
    MODULES_AVAILABLE = False


class BaseTab(ctk.CTkFrame):
    """Clase base para todas las pestañas"""
    
    def __init__(self, parent, title: str):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar la interfaz base"""
        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Scroll frame principal
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(
            self.scroll_frame,
            text=self.title,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=20, padx=20)
        
        # Frame de contenido
        self.content_frame = ctk.CTkFrame(self.scroll_frame)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Llamar al método de contenido específico
        self.create_content()
    
    def create_content(self):
        """Método para ser sobrescrito por las subclases"""
        pass


class RootsTab(BaseTab):
    """Pestaña para búsqueda de raíces"""
    
    def __init__(self, parent):
        super().__init__(parent, "🎯 Búsqueda de Raíces")
        # Inicializar el finder modular
        if MODULES_AVAILABLE:
            self.root_finder = RootFinder()
        else:
            self.root_finder = None
    
    def create_content(self):
        """Crear contenido específico para raíces"""
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Métodos numéricos para encontrar raíces de ecuaciones no lineales",
            font=ctk.CTkFont(size=14)
        )
        desc_label.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        # Entrada de función
        func_label = ctk.CTkLabel(self.content_frame, text="Función f(x):")
        func_label.grid(row=1, column=0, pady=5, padx=20, sticky="w")
        
        self.function_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Ej: x**2 - 4")
        self.function_entry.grid(row=1, column=1, pady=5, padx=20, sticky="ew")
        
        # Parámetros
        param_frame = ctk.CTkFrame(self.content_frame)
        param_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        # Intervalo o punto inicial
        ctk.CTkLabel(param_frame, text="a o x₀:").grid(row=0, column=0, pady=5, padx=10)
        self.a_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="-2")
        self.a_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ctk.CTkLabel(param_frame, text="b:").grid(row=0, column=2, pady=5, padx=10)
        self.b_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="2")
        self.b_entry.grid(row=0, column=3, pady=5, padx=5)
        
        ctk.CTkLabel(param_frame, text="Tolerancia:").grid(row=1, column=0, pady=5, padx=10)
        self.tolerance_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="1e-6")
        self.tolerance_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Botones de métodos
        methods_frame = ctk.CTkFrame(self.content_frame)
        methods_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        bisection_btn = ctk.CTkButton(methods_frame, text="Bisección", command=self.bisection_method)
        bisection_btn.grid(row=0, column=0, pady=5, padx=10)
        
        newton_btn = ctk.CTkButton(methods_frame, text="Newton-Raphson", command=self.newton_raphson_method)
        newton_btn.grid(row=0, column=1, pady=5, padx=10)
        
        fixed_btn = ctk.CTkButton(methods_frame, text="Punto Fijo", command=self.fixed_point_method)
        fixed_btn.grid(row=0, column=2, pady=5, padx=10)
        
        aitken_btn = ctk.CTkButton(methods_frame, text="Aitken", command=self.aitken_method)
        aitken_btn.grid(row=1, column=0, pady=5, padx=10)
        
        # Área de resultados
        self.results_frame = ctk.CTkFrame(self.content_frame)
        self.results_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")
        self.results_frame.grid_rowconfigure(0, weight=1)
        
        self.results_text = ctk.CTkTextbox(self.results_frame, height=200)
        self.results_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.results_frame.grid_rowconfigure(0, weight=1)
    
    def bisection_method(self):
        """Ejecutar método de bisección usando componente modular"""
        if not MODULES_AVAILABLE or not self.root_finder:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tolerance = float(self.tolerance_entry.get())
            
            # Crear función evaluable
            def create_function(func_str):
                def f(x):
                    safe_dict = {
                        "x": x,
                        "sin": np.sin, "cos": np.cos, "tan": np.tan,
                        "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
                        "pi": np.pi, "e": np.e, "abs": abs, "pow": pow
                    }
                    return eval(func_str, {"__builtins__": {}}, safe_dict)
                return f
            
            func = create_function(func_str)
            result = self.root_finder.bisection_method(func, a, b)
            
            if result.converged:
                self.show_result(f"Raíz encontrada: {result.root:.8f}\n"
                               f"Iteraciones: {result.iterations}\n"
                               f"Error: {result.error:.2e}")
            else:
                self.show_error(f"No convergió en {result.iterations} iteraciones")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def newton_raphson_method(self):
        """Ejecutar método de Newton-Raphson usando componente modular"""
        if not MODULES_AVAILABLE or not self.root_finder:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            x0 = float(self.a_entry.get())
            tolerance = float(self.tolerance_entry.get())
            
            # Crear función evaluable
            def create_function(func_str):
                def f(x):
                    safe_dict = {
                        "x": x,
                        "sin": np.sin, "cos": np.cos, "tan": np.tan,
                        "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
                        "pi": np.pi, "e": np.e, "abs": abs, "pow": pow
                    }
                    return eval(func_str, {"__builtins__": {}}, safe_dict)
                return f
            
            func = create_function(func_str)
            result = self.root_finder.newton_raphson_method(func, x0)
            
            if result.converged:
                self.show_result(f"Raíz encontrada: {result.root:.8f}\n"
                               f"Iteraciones: {result.iterations}\n"
                               f"Error: {result.error:.2e}")
            else:
                self.show_error(f"No convergió en {result.iterations} iteraciones")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def fixed_point_method(self):
        """Ejecutar método de punto fijo usando componente modular"""
        if not MODULES_AVAILABLE or not self.root_finder:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            x0 = float(self.a_entry.get())
            tolerance = float(self.tolerance_entry.get())
            
            # Crear función g(x) = x + f(x) para encontrar raíz de f(x) = 0
            def create_g_function(func_str):
                def g(x):
                    safe_dict = {
                        "x": x,
                        "sin": np.sin, "cos": np.cos, "tan": np.tan,
                        "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
                        "pi": np.pi, "e": np.e, "abs": abs, "pow": pow
                    }
                    f_val = eval(func_str, {"__builtins__": {}}, safe_dict)
                    return x + f_val  # g(x) = x + f(x)
                return g
            
            g_func = create_g_function(func_str)
            result = self.root_finder.fixed_point_method(g_func, x0)
            
            if result.converged:
                self.show_result(f"Punto fijo encontrado: {result.root:.8f}\n"
                               f"Iteraciones: {result.iterations}\n"
                               f"Error: {result.error:.2e}")
            else:
                self.show_error(f"No convergió en {result.iterations} iteraciones")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def aitken_method(self):
        """Ejecutar método de aceleración de Aitken usando componente modular"""
        if not MODULES_AVAILABLE or not self.root_finder:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            x0 = float(self.a_entry.get())
            
            # Crear función g(x) para punto fijo (x = x + f(x))
            def create_g_function(func_str):
                def g(x):
                    safe_dict = {
                        "x": x,
                        "sin": np.sin, "cos": np.cos, "tan": np.tan,
                        "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
                        "pi": np.pi, "e": np.e, "abs": abs, "pow": pow
                    }
                    f_val = eval(func_str, {"__builtins__": {}}, safe_dict)
                    return x + f_val  # g(x) = x + f(x) para encontrar raíz de f(x) = 0
                return g
            
            g_func = create_g_function(func_str)
            result = self.root_finder.aitken_acceleration(g_func, x0)
            
            if result.converged:
                self.show_result(f"Raíz encontrada (Aitken): {result.root:.8f}\n"
                               f"Iteraciones: {result.iterations}\n"
                               f"Error: {result.error:.2e}")
            else:
                self.show_error(f"No convergió en {result.iterations} iteraciones")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def show_result(self, text):
        """Mostrar resultado en el área de texto"""
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", text)
    
    def show_error(self, message):
        """Mostrar mensaje de error"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x200")
        
        label = ctk.CTkLabel(error_window, text=message, wraplength=350)
        label.pack(pady=20, padx=20)
        
        button = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
        button.pack(pady=10)


class IntegrationTab(BaseTab):
    """Pestaña para integración numérica"""
    
    def __init__(self, parent):
        super().__init__(parent, "∫ Integración Numérica")
        # Inicializar el integrador modular
        if MODULES_AVAILABLE:
            self.integrator = NumericalIntegrator()
        else:
            self.integrator = None
    
    def create_content(self):
        """Crear contenido específico para integración"""
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Métodos numéricos para calcular integrales definidas",
            font=ctk.CTkFont(size=14)
        )
        desc_label.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        # Entrada de función
        func_label = ctk.CTkLabel(self.content_frame, text="Función f(x):")
        func_label.grid(row=1, column=0, pady=5, padx=20, sticky="w")
        
        self.function_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Ej: x**2")
        self.function_entry.grid(row=1, column=1, pady=5, padx=20, sticky="ew")
        
        # Parámetros
        param_frame = ctk.CTkFrame(self.content_frame)
        param_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        # Límites de integración
        ctk.CTkLabel(param_frame, text="Límite inferior a:").grid(row=0, column=0, pady=5, padx=10)
        self.a_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="0")
        self.a_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ctk.CTkLabel(param_frame, text="Límite superior b:").grid(row=0, column=2, pady=5, padx=10)
        self.b_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="1")
        self.b_entry.grid(row=0, column=3, pady=5, padx=5)
        
        ctk.CTkLabel(param_frame, text="Subdivisiones n:").grid(row=1, column=0, pady=5, padx=10)
        self.n_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="10")
        self.n_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Botones de métodos
        methods_frame = ctk.CTkFrame(self.content_frame)
        methods_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        trapezoid_btn = ctk.CTkButton(methods_frame, text="Trapecio", command=self.trapezoid_method)
        trapezoid_btn.grid(row=0, column=0, pady=5, padx=10)
        
        simpson13_btn = ctk.CTkButton(methods_frame, text="Simpson 1/3", command=self.simpson_13_method)
        simpson13_btn.grid(row=0, column=1, pady=5, padx=10)
        
        simpson38_btn = ctk.CTkButton(methods_frame, text="Simpson 3/8", command=self.simpson_38_method)
        simpson38_btn.grid(row=0, column=2, pady=5, padx=10)
        
        # Área de resultados
        self.results_frame = ctk.CTkFrame(self.content_frame)
        self.results_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")
        self.results_frame.grid_rowconfigure(0, weight=1)
        
        self.results_text = ctk.CTkTextbox(self.results_frame, height=200)
        self.results_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.results_frame.grid_rowconfigure(0, weight=1)
    
    def trapezoid_method(self):
        """Ejecutar método del trapecio usando componente modular"""
        if not MODULES_AVAILABLE or not self.integrator:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            n = int(self.n_entry.get())
            
            # Crear función evaluable
            func = self.create_function(func_str)
            result = self.integrator.trapezoid_rule(func, a, b, n)
            
            self.show_result(f"Integral (Trapecio): {result.value:.8f}\n"
                           f"Subdivisiones: {result.subdivisions}\n"
                           f"Paso h: {result.step_size:.6f}")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def simpson_13_method(self):
        """Ejecutar método de Simpson 1/3 usando componente modular"""
        if not MODULES_AVAILABLE or not self.integrator:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            n = int(self.n_entry.get())
            
            func = self.create_function(func_str)
            result = self.integrator.simpson_13_rule(func, a, b, n)
            
            self.show_result(f"Integral (Simpson 1/3): {result.value:.8f}\n"
                           f"Subdivisiones: {result.subdivisions}\n"
                           f"Paso h: {result.step_size:.6f}")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def simpson_38_method(self):
        """Ejecutar método de Simpson 3/8 usando componente modular"""
        if not MODULES_AVAILABLE or not self.integrator:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            n = int(self.n_entry.get())
            
            func = self.create_function(func_str)
            result = self.integrator.simpson_38_rule(func, a, b, n)
            
            self.show_result(f"Integral (Simpson 3/8): {result.value:.8f}\n"
                           f"Subdivisiones: {result.subdivisions}\n"
                           f"Paso h: {result.step_size:.6f}")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def create_function(self, func_str):
        """Crear función evaluable desde string"""
        def f(x):
            safe_dict = {
                "x": x,
                "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
                "pi": np.pi, "e": np.e, "abs": abs, "pow": pow
            }
            return eval(func_str, {"__builtins__": {}}, safe_dict)
        return f
    
    def show_result(self, text):
        """Mostrar resultado en el área de texto"""
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", text)
    
    def show_error(self, message):
        """Mostrar mensaje de error"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x200")
        
        label = ctk.CTkLabel(error_window, text=message, wraplength=350)
        label.pack(pady=20, padx=20)
        
        button = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
        button.pack(pady=10)


class ODETab(BaseTab):
    """Pestaña para ecuaciones diferenciales ordinarias"""
    
    def __init__(self, parent):
        super().__init__(parent, "📈 Ecuaciones Diferenciales")
        # Inicializar el solver modular
        if MODULES_AVAILABLE:
            self.ode_solver = ODESolver()
        else:
            self.ode_solver = None
    
    def create_content(self):
        """Crear contenido específico para ODEs"""
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Métodos numéricos para resolver ecuaciones diferenciales ordinarias",
            font=ctk.CTkFont(size=14)
        )
        desc_label.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        # Entrada de función
        func_label = ctk.CTkLabel(self.content_frame, text="dy/dt = f(t,y):")
        func_label.grid(row=1, column=0, pady=5, padx=20, sticky="w")
        
        self.function_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Ej: -2*y + t")
        self.function_entry.grid(row=1, column=1, pady=5, padx=20, sticky="ew")
        
        # Parámetros
        param_frame = ctk.CTkFrame(self.content_frame)
        param_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        # Condiciones iniciales y parámetros
        ctk.CTkLabel(param_frame, text="t₀:").grid(row=0, column=0, pady=5, padx=10)
        self.t0_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="0")
        self.t0_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ctk.CTkLabel(param_frame, text="y₀:").grid(row=0, column=2, pady=5, padx=10)
        self.y0_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="1")
        self.y0_entry.grid(row=0, column=3, pady=5, padx=5)
        
        ctk.CTkLabel(param_frame, text="t_final:").grid(row=1, column=0, pady=5, padx=10)
        self.tf_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="2")
        self.tf_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ctk.CTkLabel(param_frame, text="Paso h:").grid(row=1, column=2, pady=5, padx=10)
        self.h_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="0.1")
        self.h_entry.grid(row=1, column=3, pady=5, padx=5)
        
        # Botones de métodos
        methods_frame = ctk.CTkFrame(self.content_frame)
        methods_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        euler_btn = ctk.CTkButton(methods_frame, text="Euler", command=self.euler_method)
        euler_btn.grid(row=0, column=0, pady=5, padx=10)
        
        rk2_btn = ctk.CTkButton(methods_frame, text="RK2", command=self.rk2_method)
        rk2_btn.grid(row=0, column=1, pady=5, padx=10)
        
        rk4_btn = ctk.CTkButton(methods_frame, text="RK4", command=self.rk4_method)
        rk4_btn.grid(row=0, column=2, pady=5, padx=10)
        
        # Área de resultados
        self.results_frame = ctk.CTkFrame(self.content_frame)
        self.results_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")
        self.results_frame.grid_rowconfigure(0, weight=1)
        
        self.results_text = ctk.CTkTextbox(self.results_frame, height=200)
        self.results_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.results_frame.grid_rowconfigure(0, weight=1)
    
    def euler_method(self):
        """Ejecutar método de Euler usando componente modular"""
        if not MODULES_AVAILABLE or not self.ode_solver:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            t0 = float(self.t0_entry.get())
            y0 = float(self.y0_entry.get())
            tf = float(self.tf_entry.get())
            h = float(self.h_entry.get())
            
            # Crear función evaluable
            func = self.create_ode_function(func_str)
            result = self.ode_solver.euler_method(func, t0, y0, tf, h)
            
            self.show_result(f"Solución (Euler):\n"
                           f"Valor final: y({tf}) = {result.final_value:.6f}\n"
                           f"Pasos: {len(result.x_values)}\n"
                           f"Paso h: {result.step_size:.6f}")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def rk2_method(self):
        """Ejecutar método RK2 usando componente modular"""
        if not MODULES_AVAILABLE or not self.ode_solver:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            t0 = float(self.t0_entry.get())
            y0 = float(self.y0_entry.get())
            tf = float(self.tf_entry.get())
            h = float(self.h_entry.get())
            
            func = self.create_ode_function(func_str)
            result = self.ode_solver.runge_kutta_2(func, t0, y0, tf, h)
            
            self.show_result(f"Solución (RK2):\n"
                           f"Valor final: y({tf}) = {result.final_value:.6f}\n"
                           f"Pasos: {len(result.x_values)}\n"
                           f"Paso h: {result.step_size:.6f}")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def rk4_method(self):
        """Ejecutar método RK4 usando componente modular"""
        if not MODULES_AVAILABLE or not self.ode_solver:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            t0 = float(self.t0_entry.get())
            y0 = float(self.y0_entry.get())
            tf = float(self.tf_entry.get())
            h = float(self.h_entry.get())
            
            func = self.create_ode_function(func_str)
            result = self.ode_solver.runge_kutta_4(func, t0, y0, tf, h)
            
            self.show_result(f"Solución (RK4):\n"
                           f"Valor final: y({tf}) = {result.final_value:.6f}\n"
                           f"Pasos: {len(result.x_values)}\n"
                           f"Paso h: {result.step_size:.6f}")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def create_ode_function(self, func_str):
        """Crear función ODE evaluable desde string"""
        def f(t, y):
            safe_dict = {
                "t": t, "y": y,
                "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
                "pi": np.pi, "e": np.e, "abs": abs, "pow": pow
            }
            return eval(func_str, {"__builtins__": {}}, safe_dict)
        return f
    
    def show_result(self, text):
        """Mostrar resultado en el área de texto"""
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", text)
    
    def show_error(self, message):
        """Mostrar mensaje de error"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x200")
        
        label = ctk.CTkLabel(error_window, text=message, wraplength=350)
        label.pack(pady=20, padx=20)
        
        button = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
        button.pack(pady=10)


class FiniteDiffTab(BaseTab):
    """Pestaña para diferencias finitas"""
    
    def __init__(self, parent):
        super().__init__(parent, "🔢 Diferencias Finitas")
        # Inicializar el calculador modular
        if MODULES_AVAILABLE:
            self.diff_calculator = FiniteDifferenceCalculator()
        else:
            self.diff_calculator = None
    
    def create_content(self):
        """Crear contenido específico para diferencias finitas"""
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Métodos numéricos para calcular derivadas mediante diferencias finitas",
            font=ctk.CTkFont(size=14)
        )
        desc_label.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        # Entrada de función
        func_label = ctk.CTkLabel(self.content_frame, text="Función f(x):")
        func_label.grid(row=1, column=0, pady=5, padx=20, sticky="w")
        
        self.function_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Ej: x**3")
        self.function_entry.grid(row=1, column=1, pady=5, padx=20, sticky="ew")
        
        # Parámetros
        param_frame = ctk.CTkFrame(self.content_frame)
        param_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        # Punto y paso
        ctk.CTkLabel(param_frame, text="Punto x:").grid(row=0, column=0, pady=5, padx=10)
        self.x_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="1")
        self.x_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ctk.CTkLabel(param_frame, text="Paso h:").grid(row=0, column=2, pady=5, padx=10)
        self.h_entry = ctk.CTkEntry(param_frame, width=100, placeholder_text="0.01")
        self.h_entry.grid(row=0, column=3, pady=5, padx=5)
        
        # Botones de métodos
        methods_frame = ctk.CTkFrame(self.content_frame)
        methods_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        forward_btn = ctk.CTkButton(methods_frame, text="Adelante", command=self.forward_difference)
        forward_btn.grid(row=0, column=0, pady=5, padx=10)
        
        backward_btn = ctk.CTkButton(methods_frame, text="Atrás", command=self.backward_difference)
        backward_btn.grid(row=0, column=1, pady=5, padx=10)
        
        central_btn = ctk.CTkButton(methods_frame, text="Central", command=self.central_difference)
        central_btn.grid(row=0, column=2, pady=5, padx=10)
        
        # Área de resultados
        self.results_frame = ctk.CTkFrame(self.content_frame)
        self.results_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")
        self.results_frame.grid_rowconfigure(0, weight=1)
        
        self.results_text = ctk.CTkTextbox(self.results_frame, height=200)
        self.results_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.results_frame.grid_rowconfigure(0, weight=1)
    
    def forward_difference(self):
        """Ejecutar diferencia hacia adelante usando componente modular"""
        if not MODULES_AVAILABLE or not self.diff_calculator:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            x = float(self.x_entry.get())
            h = float(self.h_entry.get())
            
            func = self.create_function(func_str)
            result = self.diff_calculator.forward_difference(func, x, h)
            
            self.show_result(f"Derivada (Adelante): {result.value:.8f}\n"
                           f"Método: {result.method}\n"
                           f"Paso h: {result.step_size:.6f}")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def backward_difference(self):
        """Ejecutar diferencia hacia atrás usando componente modular"""
        if not MODULES_AVAILABLE or not self.diff_calculator:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            x = float(self.x_entry.get())
            h = float(self.h_entry.get())
            
            func = self.create_function(func_str)
            result = self.diff_calculator.backward_difference(func, x, h)
            
            self.show_result(f"Derivada (Atrás): {result.value:.8f}\n"
                           f"Método: {result.method}\n"
                           f"Paso h: {result.step_size:.6f}")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def central_difference(self):
        """Ejecutar diferencia central usando componente modular"""
        if not MODULES_AVAILABLE or not self.diff_calculator:
            self.show_error("Los módulos modulares no están disponibles")
            return
        
        try:
            func_str = self.function_entry.get()
            if not func_str:
                self.show_error("Ingrese una función")
                return
                
            x = float(self.x_entry.get())
            h = float(self.h_entry.get())
            
            func = self.create_function(func_str)
            result = self.diff_calculator.central_difference(func, x, h)
            
            self.show_result(f"Derivada (Central): {result.value:.8f}\n"
                           f"Método: {result.method}\n"
                           f"Paso h: {result.step_size:.6f}")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def create_function(self, func_str):
        """Crear función evaluable desde string"""
        def f(x):
            safe_dict = {
                "x": x,
                "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
                "pi": np.pi, "e": np.e, "abs": abs, "pow": pow
            }
            return eval(func_str, {"__builtins__": {}}, safe_dict)
        return f
    
    def show_result(self, text):
        """Mostrar resultado en el área de texto"""
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", text)
    
    def show_error(self, message):
        """Mostrar mensaje de error"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x200")
        
        label = ctk.CTkLabel(error_window, text=message, wraplength=350)
        label.pack(pady=20, padx=20)
        
        button = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
        button.pack(pady=10)


class MathSimulatorApp(ctk.CTk):
    """Aplicación principal del simulador matemático"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("🧮 Simulador Matemático v4.0 - Modular")
        self.geometry("1200x800")
        
        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Crear interfaz
        self.create_sidebar()
        self.create_main_area()
        
        # Mostrar pestaña inicial
        self.show_tab("roots")
    
    def create_sidebar(self):
        """Crear barra lateral de navegación"""
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        
        # Logo/Título
        title_label = ctk.CTkLabel(
            self.sidebar,
            text="SIMULADOR",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=["#1f538d", "#3d8bff"]
        )
        title_label.grid(row=0, column=0, pady=(25, 35), padx=20)
        
        # Botones de navegación
        nav_buttons = [
            ("roots", "🎯 Búsqueda de Raíces"),
            ("integration", "∫ Integración"),
            ("ode", "📈 EDOs"),
            ("finite_diff", "🔢 Diferencias Finitas"),
            ("newton_cotes", "📊 Newton-Cotes"),
            ("interpolation", "🔗 Interpolación"),
            ("derivatives", "∂ Derivadas")
        ]
        
        self.nav_buttons = {}
        for i, (key, text) in enumerate(nav_buttons):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=lambda k=key: self.show_tab(k),
                height=40,
                anchor="w",
                font=ctk.CTkFont(size=14)
            )
            btn.grid(row=i+1, column=0, pady=2, padx=20, sticky="ew")
            self.nav_buttons[key] = btn
        
        # Información del desarrollador
        dev_label = ctk.CTkLabel(
            self.sidebar,
            text="Simulador Modular v4.0\nMetodos Numéricos",
            font=ctk.CTkFont(size=10),
            text_color=["gray60", "gray50"]
        )
        dev_label.grid(row=9, column=0, pady=10, padx=20)
    
    def create_main_area(self):
        """Crea el área principal para mostrar pestañas"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Crear todas las pestañas
        self.tabs = {}
        self.tabs["roots"] = RootsTab(self.main_frame)
        self.tabs["integration"] = IntegrationTab(self.main_frame)
        self.tabs["ode"] = ODETab(self.main_frame)
        self.tabs["finite_diff"] = FiniteDiffTab(self.main_frame)
        
        # Pestañas placeholder para las demás
        self.tabs["newton_cotes"] = self.create_placeholder_tab("📊 Newton-Cotes", 
                                                               "Métodos avanzados de Newton-Cotes para integración numérica")
        self.tabs["interpolation"] = self.create_placeholder_tab("🔗 Interpolación", 
                                                                "Métodos de interpolación polinomial y splines")
        self.tabs["derivatives"] = self.create_placeholder_tab("∂ Derivadas Numéricas", 
                                                              "Cálculo numérico de derivadas de orden superior")
        
        # Inicialmente ocultar todas las pestañas
        for tab in self.tabs.values():
            tab.grid_remove()
    
    def create_placeholder_tab(self, title, description):
        """Crear pestaña placeholder para módulos no implementados"""
        placeholder = ctk.CTkFrame(self.main_frame)
        placeholder.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        placeholder.grid_rowconfigure(1, weight=1)
        placeholder.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            placeholder,
            text=title,
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(40, 20))
        
        # Descripción
        desc_label = ctk.CTkLabel(
            placeholder,
            text=description,
            font=ctk.CTkFont(size=16),
            text_color=["gray60", "gray50"]
        )
        desc_label.grid(row=1, column=0, pady=10)
        
        # Estado
        status_frame = ctk.CTkFrame(placeholder)
        status_frame.grid(row=2, column=0, pady=40)
        
        status_label = ctk.CTkLabel(
            status_frame,
            text="🚧 MÓDULO EN DESARROLLO 🚧",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=["orange", "yellow"]
        )
        status_label.pack(pady=20, padx=40)
        
        info_label = ctk.CTkLabel(
            status_frame,
            text="Este módulo será implementado en la próxima versión.\nUse la estructura modular para acceder a esta funcionalidad.",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        info_label.pack(pady=(0, 20), padx=40)
        
        return placeholder
    
    def show_tab(self, tab_id):
        """Mostrar pestaña específica"""
        # Ocultar todas las pestañas
        for tab in self.tabs.values():
            tab.grid_remove()
        
        # Mostrar pestaña seleccionada
        if tab_id in self.tabs:
            self.tabs[tab_id].grid(row=0, column=0, sticky="nsew")
        
        # Actualizar apariencia de los botones
        for btn_id, btn in self.nav_buttons.items():
            if btn_id == tab_id:
                # Botón activo
                btn.configure(
                    fg_color=["#1f538d", "#3d8bff"],
                    text_color="white"
                )
            else:
                # Botón inactivo
                btn.configure(
                    fg_color=["gray75", "gray25"],
                    text_color=["gray10", "gray90"]
                )
    
    def show_error(self, message):
        """Mostrar mensaje de error"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x150")
        error_window.grab_set()
        
        error_label = ctk.CTkLabel(
            error_window,
            text=message,
            wraplength=350,
            font=ctk.CTkFont(size=12)
        )
        error_label.pack(pady=20, padx=20)
        
        ok_btn = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy
        )
        ok_btn.pack(pady=10)


def run_simple_app():
    """Ejecuta la aplicación simplificada"""
    try:
        print("🚀 Iniciando Simulador Matemático v4.0 (Modular)...")
        app = MathSimulatorApp()
        app.mainloop()
        return 0
    except Exception as e:
        logger.error(f"Error en aplicación simplificada: {e}")
        print(f"❌ Error en interfaz simplificada: {e}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit_code = run_simple_app()
    sys.exit(exit_code)
