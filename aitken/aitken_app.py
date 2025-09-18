"""
Implementación dedicada del método de aceleración de Aitken
con interfaz gráfica y tabla detallada mostrando 8 decimales.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


def format_8_decimals(value):
    """Formatea un número para mostrar exactamente 8 decimales."""
    return f"{value:.8f}"


class AitkenAcceleration:
    """
    Implementación del método de aceleración de Aitken para acelerar
    la convergencia de secuencias de punto fijo.
    """
    
    def __init__(self, tolerance=1e-8, max_iterations=20):
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.iteration_data = []
        
    def accelerate(self, g_function, x0):
        """
        Aplica aceleración de Aitken a una función de punto fijo.
        
        Args:
            g_function: Función g(x) para punto fijo
            x0: Valor inicial
            
        Returns:
            dict con resultados detallados
        """
        self.iteration_data = []
        x = x0
        x_aitken_previous = None  # Para calcular error relativo porcentual
        
        for i in range(self.max_iterations):
            # Calcular secuencia de punto fijo
            x1 = g_function(x)
            x2 = g_function(x1)
            
            # Aplicar fórmula de Aitken
            denominator = x2 - 2*x1 + x
            
            if abs(denominator) < 1e-14:
                # Denominador muy pequeño, usar punto fijo normal
                x_aitken = x2
                method_used = "Punto fijo (denominador pequeño)"
            else:
                x_aitken = x - (x1 - x)**2 / denominator
                method_used = "Aitken"
            
            # Calcular error relativo porcentual: abs((x1 - x0)/abs(x0))*100
            # donde x1 = x_aitken actual, x0 = x_aitken anterior
            if i == 0:
                # Primera iteración: usar diferencia absoluta como referencia
                error = abs(x_aitken - x)
            else:
                # Iteraciones siguientes: error relativo porcentual
                if abs(x_aitken_previous) > 1e-14:
                    error = abs((x_aitken - x_aitken_previous) / abs(x_aitken_previous)) * 100
                else:
                    error = abs(x_aitken - x_aitken_previous)
            
            # Guardar datos de iteración
            iter_data = {
                'iteration': i + 1,
                'x': x,
                'x1': x1,
                'x2': x2,
                'x_aitken': x_aitken,
                'error': error,
                'method': method_used
            }
            self.iteration_data.append(iter_data)
            
            # Verificar convergencia con la tolerancia establecida
            # Como ahora el error es porcentual, usamos la tolerancia directamente
            if error < self.tolerance:
                return {
                    'root': x_aitken,
                    'iterations': i + 1,
                    'converged': True,
                    'error': error,
                    'iteration_data': self.iteration_data
                }
            
            # Preparar siguiente iteración
            x_aitken_previous = x_aitken
            x = x_aitken
        
        return {
            'root': x,
            'iterations': self.max_iterations,
            'converged': False,
            'error': error,
            'iteration_data': self.iteration_data
        }


class AitkenGUI:
    """Interfaz gráfica para el método de Aitken con tabla detallada."""
    
    def __init__(self):
        # Configurar tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Ventana principal
        self.root = ctk.CTk()
        self.root.title("Método de Aceleración de Aitken")
        self.root.geometry("1200x800")
        
        # Variables
        self.function_var = ctk.StringVar(value="cos(x)")
        self.x0_var = ctk.StringVar(value="0.5")
        self.tolerance_var = ctk.StringVar(value="1e-8")
        self.max_iter_var = ctk.StringVar(value="20")
        
        # Crear interfaz
        self.create_widgets()
        
    def create_widgets(self):
        """Crear todos los widgets de la interfaz."""
        
        # Frame principal con pestañas
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña de configuración y resultados
        self.tab_main = self.notebook.add("Configuración y Tabla")
        self.tab_graph = self.notebook.add("Gráfico")
        
        self.create_main_tab()
        self.create_graph_tab()
        
    def create_main_tab(self):
        """Crear la pestaña principal con configuración y tabla."""
        
        # Frame de entrada
        input_frame = ctk.CTkFrame(self.tab_main)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(input_frame, text="Método de Aceleración de Aitken", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        # Descripción
        desc_text = ("Acelera la convergencia de métodos de punto fijo usando:\n"
                    "x_new = x - (x₁ - x)² / (x₂ - 2x₁ + x)\n"
                    "Error calculado como: ||(x_actual - x_anterior) / x_anterior|| × 100%")
        desc_label = ctk.CTkLabel(input_frame, text=desc_text, 
                                 font=ctk.CTkFont(size=12))
        desc_label.pack(pady=5)
        
        # Frame de parámetros
        params_frame = ctk.CTkFrame(input_frame)
        params_frame.pack(fill="x", padx=20, pady=10)
        
        # Función g(x)
        ctk.CTkLabel(params_frame, text="Función g(x):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        func_entry = ctk.CTkEntry(params_frame, textvariable=self.function_var, width=200)
        func_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Valor inicial
        ctk.CTkLabel(params_frame, text="Valor inicial x₀:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        x0_entry = ctk.CTkEntry(params_frame, textvariable=self.x0_var, width=100)
        x0_entry.grid(row=0, column=3, padx=10, pady=5)
        
        # Tolerancia
        ctk.CTkLabel(params_frame, text="Tolerancia:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tol_entry = ctk.CTkEntry(params_frame, textvariable=self.tolerance_var, width=100)
        tol_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Máximo de iteraciones
        ctk.CTkLabel(params_frame, text="Máx. iteraciones:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        iter_entry = ctk.CTkEntry(params_frame, textvariable=self.max_iter_var, width=100)
        iter_entry.grid(row=1, column=3, padx=10, pady=5)
        
        # Botón calcular
        calc_button = ctk.CTkButton(input_frame, text="Calcular Aitken", 
                                   command=self.calculate_aitken,
                                   font=ctk.CTkFont(size=14, weight="bold"),
                                   height=40)
        calc_button.pack(pady=15)
        
        # Frame de resultados
        results_frame = ctk.CTkFrame(self.tab_main)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Etiqueta de resultados principales
        self.result_label = ctk.CTkLabel(results_frame, text="Resultados aparecerán aquí...",
                                        font=ctk.CTkFont(size=14))
        self.result_label.pack(pady=10)
        
        # Crear tabla con Treeview
        self.create_table(results_frame)
        
    def create_table(self, parent):
        """Crear tabla para mostrar iteraciones."""
        
        # Frame para la tabla
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título de la tabla
        table_title = ctk.CTkLabel(table_frame, text="Tabla de Iteraciones (8 decimales)",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        table_title.pack(pady=5)
        
        # Crear Treeview (nativo de tkinter para tabla)
        columns = ("Iter", "x", "x₁", "x₂", "x_aitken", "Error (%)", "Método")
        
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Configurar columnas
        column_widths = [60, 120, 120, 120, 140, 120, 150]
        for col, width in zip(columns, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar tabla y scrollbars
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
    def create_graph_tab(self):
        """Crear la pestaña del gráfico."""
        
        # Frame para el gráfico
        self.graph_frame = ctk.CTkFrame(self.tab_graph)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Placeholder para el gráfico
        placeholder_label = ctk.CTkLabel(self.graph_frame, 
                                       text="El gráfico se mostrará después del cálculo",
                                       font=ctk.CTkFont(size=14))
        placeholder_label.pack(expand=True)
        
    def safe_eval_function(self, func_str, x):
        """Evaluar función de forma segura."""
        try:
            # Contexto seguro con funciones matemáticas comunes
            safe_dict = {
                "x": x,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
                "pi": math.pi, "e": math.e,
                "abs": abs, "pow": pow
            }
            return eval(func_str, {"__builtins__": {}}, safe_dict)
        except:
            raise ValueError(f"Error evaluando función: {func_str}")
    
    def calculate_aitken(self):
        """Calcular método de Aitken y mostrar resultados."""
        try:
            # Obtener parámetros
            func_str = self.function_var.get()
            x0 = float(self.x0_var.get())
            tolerance = float(self.tolerance_var.get())
            max_iter = int(self.max_iter_var.get())
            
            # Crear función lambda
            g = lambda x: self.safe_eval_function(func_str, x)
            
            # Aplicar Aitken
            aitken = AitkenAcceleration(tolerance, max_iter)
            result = aitken.accelerate(g, x0)
            
            # Mostrar resultados principales
            convergence_text = "SÍ" if result['converged'] else "NO"
            result_text = (f"Resultado: {format_8_decimals(result['root'])}\n"
                          f"Iteraciones: {result['iterations']}\n"
                          f"Error final: {format_8_decimals(result['error'])}\n"
                          f"Convergió: {convergence_text}")
            
            self.result_label.configure(text=result_text)
            
            # Llenar tabla
            self.fill_table(result['iteration_data'])
            
            # Crear gráfico
            self.create_plot(g, result, func_str)
            
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")
    
    def fill_table(self, iteration_data):
        """Llenar la tabla con datos de iteraciones."""
        
        # Limpiar tabla existente
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Llenar con nuevos datos
        for data in iteration_data:
            values = (
                data['iteration'],
                format_8_decimals(data['x']),
                format_8_decimals(data['x1']),
                format_8_decimals(data['x2']),
                format_8_decimals(data['x_aitken']),
                format_8_decimals(data['error']),
                data['method']
            )
            self.tree.insert("", "end", values=values)
    
    def create_plot(self, g_function, result, func_str):
        """Crear gráfico de convergencia."""
        
        # Limpiar frame anterior
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Crear figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor('#212121')
        
        # Gráfico 1: Función y punto fijo
        try:
            x_vals = np.linspace(result['root'] - 1, result['root'] + 1, 1000)
            y_vals = [g_function(x) for x in x_vals]
            
            ax1.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'g(x) = {func_str}')
            ax1.plot(x_vals, x_vals, 'r--', linewidth=2, label='y = x')
            ax1.plot(result['root'], result['root'], 'go', markersize=10, 
                    label=f'Punto fijo: {format_8_decimals(result["root"])}')
            
            ax1.set_xlabel('x')
            ax1.set_ylabel('y')
            ax1.set_title('Función y Punto Fijo')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.set_facecolor('#2b2b2b')
            
        except:
            ax1.text(0.5, 0.5, 'Error graficando función', 
                    transform=ax1.transAxes, ha='center')
        
        # Gráfico 2: Convergencia de errores
        iterations = [data['iteration'] for data in result['iteration_data']]
        errors = [data['error'] for data in result['iteration_data']]
        
        ax2.semilogy(iterations, errors, 'bo-', linewidth=2, markersize=6)
        ax2.set_xlabel('Iteración')
        ax2.set_ylabel('Error (escala log)')
        ax2.set_title('Convergencia del Error')
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('#2b2b2b')
        
        # Anotar última iteración
        if errors:
            ax2.annotate(f'Error final: {format_8_decimals(errors[-1])}',
                        xy=(iterations[-1], errors[-1]),
                        xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        # Estilo general
        for ax in [ax1, ax2]:
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
        
        plt.tight_layout()
        
        # Integrar en la interfaz
        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def run(self):
        """Ejecutar la aplicación."""
        self.root.mainloop()


def main():
    """Función principal."""
    app = AitkenGUI()
    app.run()


if __name__ == "__main__":
    main()