"""
Aplicación para la interpolación polinómica de Lagrange.

Esta aplicación proporciona una interfaz gráfica para visualizar y utilizar
el método de interpolación polinómica de Lagrange.
"""

import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import sys
import os
from typing import List, Tuple, Optional

# Añadir el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar el módulo de interpolación de Lagrange
from lagrange_interpolation.lagrange import LagrangeInterpolation


class LagrangeApp:
    """Aplicación para la interpolación polinómica de Lagrange."""
    
    def __init__(self, root):
        """
        Inicializa la aplicación.
        
        Args:
            root: Ventana principal de la aplicación.
        """
        self.root = root
        self.root.title("Interpolación de Lagrange")
        self.root.geometry("1100x700")
        
        # Establecer tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Inicializar el interpolador
        self.interpolator = LagrangeInterpolation()
        
        # Puntos para la interpolación
        self.points = []
        
        # Configurar la interfaz
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Crear marco principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Dividir en dos columnas principales
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Configuración de columnas
        left_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # === Panel izquierdo (entrada de datos) ===
        
        # Título
        title_label = ctk.CTkLabel(
            left_frame, 
            text="Interpolación Polinómica de Lagrange",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Sección de entrada de puntos manualmente
        manual_points_frame = ctk.CTkFrame(left_frame)
        manual_points_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        manual_title = ctk.CTkLabel(
            manual_points_frame, 
            text="Agregar puntos manualmente",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        manual_title.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        
        # Entrada de coordenadas X e Y
        x_label = ctk.CTkLabel(manual_points_frame, text="Valor X:")
        x_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.x_entry = ctk.CTkEntry(manual_points_frame)
        self.x_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        y_label = ctk.CTkLabel(manual_points_frame, text="Valor Y:")
        y_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.y_entry = ctk.CTkEntry(manual_points_frame)
        self.y_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # Botón para agregar el punto
        add_point_btn = ctk.CTkButton(
            manual_points_frame, 
            text="Agregar Punto", 
            command=self.add_point
        )
        add_point_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Sección para generar puntos a partir de una función
        function_frame = ctk.CTkFrame(left_frame)
        function_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        function_title = ctk.CTkLabel(
            function_frame, 
            text="Generar puntos a partir de una función",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        function_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Entrada de la función
        func_label = ctk.CTkLabel(function_frame, text="Función f(x):")
        func_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.func_entry = ctk.CTkEntry(function_frame, placeholder_text="ej: math.sin(x)")
        self.func_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Rango de valores
        range_frame = ctk.CTkFrame(function_frame)
        range_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        start_label = ctk.CTkLabel(range_frame, text="Inicio:")
        start_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.start_entry = ctk.CTkEntry(range_frame)
        self.start_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.start_entry.insert(0, "-5")
        
        end_label = ctk.CTkLabel(range_frame, text="Fin:")
        end_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.end_entry = ctk.CTkEntry(range_frame)
        self.end_entry.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        self.end_entry.insert(0, "5")
        
        num_points_label = ctk.CTkLabel(range_frame, text="Número de puntos:")
        num_points_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.num_points_entry = ctk.CTkEntry(range_frame)
        self.num_points_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.num_points_entry.insert(0, "5")
        
        # Botón para generar puntos
        generate_btn = ctk.CTkButton(
            function_frame, 
            text="Generar Puntos", 
            command=self.generate_points
        )
        generate_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Lista de puntos
        points_frame = ctk.CTkFrame(left_frame)
        points_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        points_title = ctk.CTkLabel(
            points_frame, 
            text="Puntos actuales",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        points_title.pack(padx=10, pady=10, anchor="w")
        
        # Crear Textbox para mostrar los puntos
        self.points_textbox = ctk.CTkTextbox(points_frame, height=200)
        self.points_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.points_textbox.configure(state="disabled")
        
        # Botones para limpiar y calcular
        buttons_frame = ctk.CTkFrame(left_frame)
        buttons_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        
        clear_btn = ctk.CTkButton(
            buttons_frame, 
            text="Limpiar Puntos", 
            fg_color="darkred",
            command=self.clear_points
        )
        clear_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        calculate_btn = ctk.CTkButton(
            buttons_frame, 
            text="Calcular Interpolación", 
            fg_color="green",
            command=self.calculate_interpolation
        )
        calculate_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # === Panel derecho (resultados y gráficos) ===
        
        # Título
        results_title = ctk.CTkLabel(
            right_frame, 
            text="Resultados",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        results_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Sección de visualización
        vis_frame = ctk.CTkFrame(right_frame)
        vis_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Crear figura para el gráfico
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Interpolación de Lagrange")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        
        # Crear el canvas para la figura
        self.canvas = FigureCanvasTkAgg(self.fig, master=vis_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sección para la evaluación del polinomio
        eval_frame = ctk.CTkFrame(right_frame)
        eval_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        eval_title = ctk.CTkLabel(
            eval_frame, 
            text="Evaluar polinomio en un punto",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        eval_title.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        
        eval_x_label = ctk.CTkLabel(eval_frame, text="Valor de x:")
        eval_x_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.eval_x_entry = ctk.CTkEntry(eval_frame)
        self.eval_x_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        eval_btn = ctk.CTkButton(
            eval_frame, 
            text="Evaluar", 
            command=self.evaluate_polynomial
        )
        eval_btn.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        
        eval_result_label = ctk.CTkLabel(eval_frame, text="Resultado:")
        eval_result_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.eval_result = ctk.CTkLabel(eval_frame, text="-")
        self.eval_result.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Sección para mostrar el polinomio interpolante
        poly_frame = ctk.CTkFrame(right_frame)
        poly_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
        poly_title = ctk.CTkLabel(
            poly_frame, 
            text="Polinomio interpolante",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        poly_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.poly_textbox = ctk.CTkTextbox(poly_frame, height=100, wrap="word")
        self.poly_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.poly_textbox.configure(state="disabled")
        
        # Ajustar la expansión vertical
        left_frame.grid_rowconfigure(3, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        
    def add_point(self):
        """Agrega un punto ingresado manualmente."""
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            
            # Verificar si ya existe un punto con este valor x
            for px, _ in self.points:
                if px == x:
                    self.show_error(f"Ya existe un punto con x = {x}")
                    return
            
            self.points.append((x, y))
            self.update_points_display()
            
            # Limpiar entradas
            self.x_entry.delete(0, "end")
            self.y_entry.delete(0, "end")
            
        except ValueError:
            self.show_error("Los valores deben ser números válidos.")
    
    def generate_points(self):
        """Genera puntos a partir de una función."""
        try:
            func_str = self.func_entry.get().strip()
            start = float(self.start_entry.get())
            end = float(self.end_entry.get())
            num_points = int(self.num_points_entry.get())
            
            if num_points < 2:
                self.show_error("Se necesitan al menos 2 puntos.")
                return
            
            if start >= end:
                self.show_error("El valor de inicio debe ser menor que el valor final.")
                return
            
            if not func_str:
                self.show_error("Debe ingresar una función válida.")
                return
            
            # Crear la función usando eval (con precauciones)
            try:
                # Crear un espacio de nombres seguro con funciones matemáticas
                safe_dict = {
                    'math': math,
                    'sin': math.sin,
                    'cos': math.cos,
                    'tan': math.tan,
                    'exp': math.exp,
                    'log': math.log,
                    'sqrt': math.sqrt,
                    'pi': math.pi,
                    'e': math.e
                }
                
                # Función lambda que evalúa la expresión
                func = lambda x: eval(func_str, {"__builtins__": {}}, {**safe_dict, 'x': x})
                
                # Probar la función
                _ = func(0)
            except Exception as e:
                self.show_error(f"Error en la función: {str(e)}")
                return
            
            # Generar puntos equidistantes
            x_values = np.linspace(start, end, num_points)
            new_points = [(float(x), float(func(x))) for x in x_values]
            
            # Reemplazar puntos existentes
            self.points = new_points
            self.update_points_display()
            
        except ValueError:
            self.show_error("Los valores deben ser números válidos.")
    
    def clear_points(self):
        """Limpia la lista de puntos."""
        self.points = []
        self.update_points_display()
        self.clear_plot()
        self.clear_polynomial_display()
        self.eval_result.configure(text="-")
    
    def update_points_display(self):
        """Actualiza la visualización de los puntos en la interfaz."""
        # Habilitar el textbox para edición
        self.points_textbox.configure(state="normal")
        
        # Limpiar el contenido actual
        self.points_textbox.delete("1.0", "end")
        
        # Mostrar los puntos ordenados por valor x
        sorted_points = sorted(self.points, key=lambda p: p[0])
        
        for i, (x, y) in enumerate(sorted_points):
            self.points_textbox.insert("end", f"Punto {i+1}: ({x:.6g}, {y:.6g})\n")
        
        # Deshabilitar el textbox para solo lectura
        self.points_textbox.configure(state="disabled")
        
        # Actualizar gráfico con los puntos
        self.plot_points()
    
    def plot_points(self):
        """Dibuja los puntos en el gráfico."""
        self.ax.clear()
        
        x_values = [p[0] for p in self.points]
        y_values = [p[1] for p in self.points]
        
        self.ax.scatter(x_values, y_values, color='blue', s=50, label='Puntos')
        self.ax.grid(True)
        self.ax.set_title("Interpolación de Lagrange")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        
        # Si hay puntos, ajustar los límites del gráfico
        if self.points:
            x_min, x_max = min(x_values), max(x_values)
            y_min, y_max = min(y_values), max(y_values)
            
            x_margin = (x_max - x_min) * 0.1 if x_max != x_min else 1.0
            y_margin = (y_max - y_min) * 0.1 if y_max != y_min else 1.0
            
            self.ax.set_xlim(x_min - x_margin, x_max + x_margin)
            self.ax.set_ylim(y_min - y_margin, y_max + y_margin)
        
        self.canvas.draw()
    
    def calculate_interpolation(self):
        """Calcula la interpolación de Lagrange con los puntos actuales."""
        if len(self.points) < 2:
            self.show_error("Se necesitan al menos 2 puntos para la interpolación.")
            return
        
        try:
            # Establecer puntos en el interpolador
            self.interpolator.set_points(self.points)
            
            # Mostrar polinomio
            self.display_polynomial()
            
            # Visualizar interpolación
            self.plot_interpolation()
            
        except Exception as e:
            self.show_error(f"Error al calcular la interpolación: {str(e)}")
    
    def display_polynomial(self):
        """Muestra el polinomio interpolante en la interfaz."""
        poly_str = self.interpolator.get_polynomial_string()
        
        # Habilitar el textbox para edición
        self.poly_textbox.configure(state="normal")
        
        # Limpiar el contenido actual
        self.poly_textbox.delete("1.0", "end")
        
        # Mostrar el polinomio
        self.poly_textbox.insert("end", poly_str)
        
        # Deshabilitar el textbox para solo lectura
        self.poly_textbox.configure(state="disabled")
    
    def plot_interpolation(self):
        """Dibuja la curva de interpolación en el gráfico."""
        if not self.points:
            return
        
        # Limpiar gráfico y dibujar puntos
        self.plot_points()
        
        # Calcular rango para el gráfico
        x_values = [p[0] for p in self.points]
        x_min, x_max = min(x_values), max(x_values)
        
        # Generar puntos para dibujar el polinomio
        x_plot = np.linspace(x_min, x_max, 1000)
        y_plot = self.interpolator.interpolate(x_plot)
        
        # Dibujar el polinomio interpolante
        self.ax.plot(x_plot, y_plot, 'r-', linewidth=2, label='Polinomio interpolante')
        self.ax.legend()
        
        self.canvas.draw()
    
    def evaluate_polynomial(self):
        """Evalúa el polinomio interpolante en un punto específico."""
        if not hasattr(self.interpolator, 'points') or not self.interpolator.points:
            self.show_error("Primero debe calcular la interpolación.")
            return
        
        try:
            x = float(self.eval_x_entry.get())
            y = self.interpolator.interpolate(x)
            
            self.eval_result.configure(text=f"{y:.8g}")
            
            # Marcar el punto en el gráfico
            self.ax.plot([x], [y], 'go', markersize=8)
            self.canvas.draw()
            
        except ValueError:
            self.show_error("Debe ingresar un valor numérico válido.")
        except Exception as e:
            self.show_error(f"Error al evaluar el polinomio: {str(e)}")
    
    def clear_plot(self):
        """Limpia el gráfico."""
        self.ax.clear()
        self.ax.set_title("Interpolación de Lagrange")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        self.canvas.draw()
    
    def clear_polynomial_display(self):
        """Limpia la visualización del polinomio."""
        self.poly_textbox.configure(state="normal")
        self.poly_textbox.delete("1.0", "end")
        self.poly_textbox.configure(state="disabled")
    
    def show_error(self, message):
        """Muestra un mensaje de error."""
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("Error")
        error_window.geometry("400x150")
        error_window.grab_set()  # Hacer la ventana modal
        
        error_label = ctk.CTkLabel(
            error_window, 
            text=message,
            font=ctk.CTkFont(size=14)
        )
        error_label.pack(padx=20, pady=20)
        
        ok_button = ctk.CTkButton(
            error_window, 
            text="Aceptar",
            command=error_window.destroy
        )
        ok_button.pack(padx=20, pady=10)