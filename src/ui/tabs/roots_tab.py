"""
Pestaña de búsqueda de raíces de ecuaciones no lineales.

Implementa la interfaz gráfica para los métodos numéricos de búsqueda de raíces
siguiendo principios SOLID y DRY.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional

from src.ui.components.base_tab import BaseTab
from src.core.root_finding import RootFinder, create_function_from_string
from config.settings import NUMERICAL_CONFIG


class RootsTab(BaseTab):
    """
    Pestaña para búsqueda de raíces.
    Hereda funcionalidad común de BaseTab (principio DRY).
    """
    
    def __init__(self, parent):
        super().__init__(parent, "🎯 Búsqueda de Raíces")
        self.root_finder = RootFinder(
            tolerance=NUMERICAL_CONFIG["default_tolerance"],
            max_iterations=NUMERICAL_CONFIG["max_iterations"]
        )
    
    def create_content(self):
        """Crear contenido específico para raíces (Template Method)"""
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Métodos numéricos para encontrar raíces de ecuaciones no lineales",
            font=ctk.CTkFont(size=14)
        )
        desc_label.grid(row=0, column=0, pady=10, padx=20, sticky="ew")
        
        # Crear sección de entrada
        input_data = {
            "Función f(x):": "x**2 - 4",
            "Intervalo a:": "0",
            "Intervalo b:": "3",
            "Tolerancia:": str(NUMERICAL_CONFIG["default_tolerance"])
        }
        self.entries = self.create_input_section(input_data)
        
        # Crear sección de métodos
        methods = [
            ("Bisección", self.bisection_method),
            ("Newton-Raphson", self.newton_raphson_method),
            ("Punto Fijo", self.fixed_point_method)
        ]
        self.create_methods_section(methods)
        
        # Crear sección de resultados
        self.results_frame, self.results_text, self.plot_frame = self.create_results_section()
    
    def bisection_method(self):
        """Ejecutar método de bisección"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries, 
                ["función_fx", "intervalo_a", "intervalo_b", "tolerancia"]
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función
            f = create_function_from_string(values["función_fx"])
            
            # Ejecutar método
            result = self.root_finder.bisection_method(
                f, values["intervalo_a"], values["intervalo_b"]
            )
            
            # Mostrar resultados
            self._display_results(result, "MÉTODO DE BISECCIÓN")
            
            # Crear gráfico
            self._plot_function_and_root(f, values["intervalo_a"], values["intervalo_b"], result.root)
            
        except Exception as e:
            self.show_error(f"Error en bisección: {e}")
    
    def newton_raphson_method(self):
        """Ejecutar método de Newton-Raphson"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries,
                ["función_fx", "intervalo_a", "tolerancia"]  # Usar 'a' como punto inicial
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función
            f = create_function_from_string(values["función_fx"])
            
            # Ejecutar método (derivada se calcula numéricamente)
            result = self.root_finder.newton_raphson_method(
                f, None, values["intervalo_a"]  # None = derivada numérica
            )
            
            # Mostrar resultados
            self._display_results(result, "MÉTODO DE NEWTON-RAPHSON")
            
            # Crear gráfico con tangentes
            self._plot_newton_raphson(f, values["intervalo_a"], result.root)
            
        except Exception as e:
            self.show_error(f"Error en Newton-Raphson: {e}")
    
    def fixed_point_method(self):
        """Ejecutar método de punto fijo"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries,
                ["función_fx", "intervalo_a", "tolerancia"]
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función original
            f = create_function_from_string(values["función_fx"])
            
            # Convertir a función de punto fijo: g(x) = x + f(x)
            g = lambda x: x + f(x)
            
            # Ejecutar método
            result = self.root_finder.fixed_point_method(g, values["intervalo_a"])
            
            # Mostrar resultados
            self._display_results(result, "MÉTODO DE PUNTO FIJO")
            
            # Crear gráfico
            self._plot_fixed_point(f, g, values["intervalo_a"], result.root)
            
        except Exception as e:
            self.show_error(f"Error en punto fijo: {e}")
    
    def _display_results(self, result, method_name: str):
        """Mostrar resultados en el área de texto"""
        # Datos principales
        main_data = {
            "Función": self.entries["función_fx"].get(),
            "Método": result.method if hasattr(result, 'method') else method_name,
            "Raíz encontrada": f"{result.root:.8f}",
            "Valor de función": f"{result.function_value:.2e}",
            "Iteraciones": result.iterations,
            "Convergió": "Sí" if result.converged else "No",
            "Error final": f"{result.error:.2e}"
        }
        
        # Secciones adicionales
        sections = {}
        
        # Tabla de iteraciones (primeras 10)
        if result.iteration_data:
            iterations_text = []
            iterations_text.append("Iter | Datos de la iteración")
            iterations_text.append("-" * 40)
            
            for i, data in enumerate(result.iteration_data[:10]):
                if 'c' in data:  # Bisección
                    iterations_text.append(
                        f"{data['iteration']:4d} | a={data['a']:.6f}, b={data['b']:.6f}, "
                        f"c={data['c']:.6f}, error={data['error']:.2e}"
                    )
                elif 'x_n' in data:  # Newton-Raphson
                    iterations_text.append(
                        f"{data['iteration']:4d} | x_n={data['x_n']:.6f}, "
                        f"x_n+1={data['x_n_plus_1']:.6f}, error={data['error']:.2e}"
                    )
                elif 'g_x_n' in data:  # Punto fijo
                    iterations_text.append(
                        f"{data['iteration']:4d} | x_n={data['x_n']:.6f}, "
                        f"g(x_n)={data['g_x_n']:.6f}, error={data['error']:.2e}"
                    )
            
            if len(result.iteration_data) > 10:
                iterations_text.append("... (mostrando solo las primeras 10 iteraciones)")
            
            sections["TABLA DE ITERACIONES"] = iterations_text
        
        # Información del método
        method_info = []
        if "bisección" in method_name.lower():
            method_info = [
                "Requiere cambio de signo en el intervalo",
                "Convergencia garantizada",
                "Convergencia lineal",
                "Error se reduce a la mitad en cada iteración"
            ]
        elif "newton" in method_name.lower():
            method_info = [
                "Requiere punto inicial cerca de la raíz",
                "Convergencia cuadrática cerca de la raíz",
                "Puede diverger si la derivada es pequeña",
                "Usa derivada numérica automáticamente"
            ]
        elif "punto fijo" in method_name.lower():
            method_info = [
                "Convierte f(x)=0 a x=g(x)",
                "Convergencia depende de |g'(x)| < 1",
                "Transformación: g(x) = x + f(x)",
                "Puede requerir diferentes transformaciones"
            ]
        
        if method_info:
            sections["CARACTERÍSTICAS DEL MÉTODO"] = method_info
        
        # Formatear y mostrar
        formatted_text = self.format_result_text(method_name, main_data, sections)
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", formatted_text)
    
    def _plot_function_and_root(self, f, a: float, b: float, root: float):
        """Crear gráfico de la función y la raíz encontrada"""
        fig, canvas = self.create_matplotlib_plot(self.plot_frame)
        ax = fig.add_subplot(111)
        
        # Rango de x expandido
        x_range = np.linspace(a - 0.5*(b-a), b + 0.5*(b-a), 1000)
        y_values = [f(x) for x in x_range]
        
        # Graficar función
        ax.plot(x_range, y_values, 'cyan', linewidth=2, label='f(x)')
        
        # Línea de y=0
        ax.axhline(y=0, color='white', linestyle='--', alpha=0.7, label='y = 0')
        
        # Marcar la raíz
        ax.plot(root, f(root), 'ro', markersize=10, label=f'Raíz: x = {root:.6f}')
        
        # Marcar intervalo inicial (para bisección)
        if abs(b - a) > 1e-10:
            ax.axvline(x=a, color='yellow', linestyle=':', alpha=0.7, label=f'a = {a}')
            ax.axvline(x=b, color='yellow', linestyle=':', alpha=0.7, label=f'b = {b}')
        
        self.apply_plot_styling(
            ax, 
            title="Función y Raíz Encontrada",
            xlabel="x",
            ylabel="f(x)"
        )
        
        canvas.draw()
    
    def _plot_newton_raphson(self, f, x0: float, root: float):
        """Crear gráfico mostrando el proceso de Newton-Raphson"""
        fig, canvas = self.create_matplotlib_plot(self.plot_frame)
        ax = fig.add_subplot(111)
        
        # Rango de x
        range_size = max(abs(root - x0), 1)
        x_range = np.linspace(x0 - range_size, root + range_size, 1000)
        y_values = [f(x) for x in x_range]
        
        # Graficar función
        ax.plot(x_range, y_values, 'cyan', linewidth=2, label='f(x)')
        
        # Línea de y=0
        ax.axhline(y=0, color='white', linestyle='--', alpha=0.7, label='y = 0')
        
        # Punto inicial
        ax.plot(x0, f(x0), 'go', markersize=8, label=f'Inicio: x₀ = {x0:.6f}')
        
        # Raíz encontrada
        ax.plot(root, f(root), 'ro', markersize=10, label=f'Raíz: x = {root:.6f}')
        
        # Mostrar algunas tangentes del proceso (si tenemos datos)
        # Esto requeriría almacenar los datos de iteración
        
        self.apply_plot_styling(
            ax,
            title="Método de Newton-Raphson",
            xlabel="x", 
            ylabel="f(x)"
        )
        
        canvas.draw()
    
    def _plot_fixed_point(self, f, g, x0: float, root: float):
        """Crear gráfico para punto fijo mostrando f(x), g(x) y y=x"""
        fig, canvas = self.create_matplotlib_plot(self.plot_frame)
        ax = fig.add_subplot(111)
        
        # Rango de x
        range_size = max(abs(root - x0), 1)
        x_range = np.linspace(x0 - range_size, root + range_size, 1000)
        
        # Graficar funciones
        f_values = [f(x) for x in x_range]
        g_values = [g(x) for x in x_range]
        
        ax.plot(x_range, f_values, 'cyan', linewidth=2, label='f(x)')
        ax.plot(x_range, g_values, 'orange', linewidth=2, label='g(x) = x + f(x)')
        ax.plot(x_range, x_range, 'white', linestyle='--', alpha=0.7, label='y = x')
        
        # Línea de y=0
        ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
        
        # Punto inicial
        ax.plot(x0, g(x0), 'go', markersize=8, label=f'Inicio: x₀ = {x0:.6f}')
        
        # Punto fijo encontrado
        ax.plot(root, root, 'ro', markersize=10, label=f'Punto fijo: x = {root:.6f}')
        
        self.apply_plot_styling(
            ax,
            title="Método de Punto Fijo",
            xlabel="x",
            ylabel="y"
        )
        
        canvas.draw()
