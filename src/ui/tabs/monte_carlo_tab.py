"""
Pestaña para simulación Monte Carlo.

Implementa la interfaz gráfica para el método de Monte Carlo
siguiendo principios SOLID y DRY.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional, Dict, Callable, Any, Tuple
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

from src.ui.components.base_tab import BaseTab
from src.ui.components.mixins import InputValidationMixin, ResultDisplayMixin, PlottingMixin
from src.ui.components.constants import VALIDATION, DEFAULT_CONFIGS, UI, PLOT, COLORS
from config.settings import NUMERICAL_CONFIG


class MonteCarloEngine:
    """Implementación simplificada de Monte Carlo para evitar problemas de importación"""
    
    def simulate(self, func, n_samples, seed=42, dimensions=2, x_range=(0,1), y_range=(0,1), max_error=0.05):
        """Simulación simplificada de Monte Carlo"""
        np.random.seed(seed)
        
        if dimensions == 1:
            # Simulación 1D
            x_points = np.random.uniform(x_range[0], x_range[1], n_samples)
            
            # Usar la función proporcionada en lugar de la predefinida
            f_values = np.array([func(x) for x in x_points])
            max_f = np.max(f_values) if len(f_values) > 0 else 1.0
            
            # Generar puntos aleatorios en el rectángulo (puntos y entre 0 y max_f)
            y_points = np.random.uniform(0, max_f, n_samples)
            
            # Determinar qué puntos están dentro o fuera
            inside = y_points <= f_values
            
            # Guardar tanto coordenadas x como y para la visualización
            points_inside_xy = np.column_stack([x_points[inside], y_points[inside]])
            points_outside_xy = np.column_stack([x_points[~inside], y_points[~inside]])
            
            integral = (x_range[1] - x_range[0]) * np.mean(f_values)
            std_dev = np.std(f_values)
            std_error = std_dev / np.sqrt(n_samples)
            
            # Calcular el valor z para el nivel de confianza basado en max_error
            from scipy import stats
            z_value = stats.norm.ppf(1 - max_error/2)
            
            return {
                'resultado_integracion': integral,
                'desviacion_estandar': std_dev,
                'error_estandar': std_error,
                'intervalo_confianza': (integral - z_value*std_error, integral + z_value*std_error),
                'puntos_dentro': points_inside_xy,
                'puntos_fuera': points_outside_xy,
                'volumen': x_range[1] - x_range[0],
                'estadisticas': {
                    'n_muestras': n_samples,
                    'fraccion_dentro': np.mean(inside)
                }
            }
        else:
            # Simulación 2D
            x_points = np.random.uniform(x_range[0], x_range[1], n_samples)
            y_points = np.random.uniform(y_range[0], y_range[1], n_samples)
            
            # Calcular valores de la función
            f_values = np.array([func(x, y) for x, y in zip(x_points, y_points)])
            max_f = np.max(f_values) if len(f_values) > 0 else 1.0
            
            # Generar valores z aleatorios entre 0 y max_f para determinar puntos dentro/fuera
            z_points = np.random.uniform(0, max_f, n_samples)
            
            # Determinar puntos dentro y fuera
            inside = z_points <= f_values
            
            # Guardar coordenadas completas para visualización
            points_inside_xyz = np.column_stack([x_points[inside], y_points[inside], z_points[inside]])
            points_outside_xyz = np.column_stack([x_points[~inside], y_points[~inside], z_points[~inside]])
            
            area = (x_range[1] - x_range[0]) * (y_range[1] - y_range[0])
            integral = area * np.mean(f_values)
            std_dev = np.std(f_values * area)
            std_error = std_dev / np.sqrt(n_samples)
            
            # Calcular el valor z para el nivel de confianza basado en max_error
            from scipy import stats
            z_value = stats.norm.ppf(1 - max_error/2)
            
            # Separar puntos dentro y fuera
            points_inside = np.column_stack([x_points[inside], y_points[inside]])
            points_outside = np.column_stack([x_points[~inside], y_points[~inside]])
            
            return {
                'resultado_integracion': integral,
                'desviacion_estandar': std_dev,
                'error_estandar': std_error,
                'intervalo_confianza': (integral - z_value*std_error, integral + z_value*std_error),
                'puntos_dentro': points_inside_xyz,
                'puntos_fuera': points_outside_xyz,
                'volumen': area,
                'estadisticas': {
                    'n_muestras': n_samples,
                    'fraccion_dentro': np.mean(inside)
                }
            }


class MonteCarloTab(BaseTab, InputValidationMixin, ResultDisplayMixin, PlottingMixin):
    """
    Pestaña para simulación Monte Carlo.
    Hereda funcionalidad común de BaseTab y usa mixins para reducir duplicación.
    """
    
    def __init__(self, parent):
        # Inicializar atributos antes de llamar a super().__init__()
        self.dimension_var = ctk.StringVar(value="1D")
        self.last_result = None
        
        # Inicializar mixins primero
        InputValidationMixin.__init__(self)
        
        super().__init__(parent, "🎲 Simulación Monte Carlo")
        self.mc_engine = MonteCarloEngine()
        self.setup_tooltips()
    
    def _crear_funcion_1d(self, expression):
        """Crear función 1D de manera segura"""
        import math
        import numpy as np
        
        def safe_eval(expr, x):
            # Reemplazar funciones comunes
            expr = expr.replace('^', '**')
            expr = expr.replace('e^', 'exp(')
            expr = expr.replace('ln(', 'log(')
            expr = expr.replace('log(', 'log(')
            
            # Crear namespace seguro
            safe_dict = {
                'x': x,
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
        
        return lambda x_val: safe_eval(expression, x_val)
    
    def _create_funcion_2d(self, expression):
        """Crear función 2D de manera segura"""
        import math
        import numpy as np
        
        def safe_eval(expr, x, y):
            # Reemplazar funciones comunes
            expr = expr.replace('^', '**')
            expr = expr.replace('e^', 'exp(')
            expr = expr.replace('ln(', 'log(')
            expr = expr.replace('log(', 'log(')
            
            # Crear namespace seguro
            safe_dict = {
                'x': x,
                'y': y,
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
        
        return lambda x_val, y_val: safe_eval(expression, x_val, y_val)
    
    def setup_tooltips(self):
        """Configura los tooltips para elementos UI"""
        self.tooltips = {
            "dimension": "Dimensionalidad de la integración",
            "function": "Función a integrar",
            "n_samples": "Número de puntos aleatorios",
            "seed": "Semilla para reproducibilidad (opcional)",
            "max_error": "Error máximo deseado para el intervalo de confianza",
            "x_range": "Rango de integración en x [a, b]",
            "y_range": "Rango de integración en y [c, d] (solo para 2D)"
        }
    
    def create_content(self):
        """Crear contenido específico para Monte Carlo (Template Method)"""
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Método de Monte Carlo para estimar integrales mediante técnicas estocásticas",
            font=ctk.CTkFont(size=14)
        )
        desc_label.grid(row=0, column=0, pady=10, padx=20, sticky="ew")
        
        # Crear sección de entrada principal
        self.create_input_fields()
        
        # Crear sección de botones
        self.create_buttons_section()
        
        # Crear sección de resultados
        self.results_frame = self.create_results_section()
        
        # Crear sección de gráficos
        self.create_plot_section()
        
        # Crear sección de fórmulas
        self.create_formula_section()
    
    def create_input_fields(self):
        """Crear campos de entrada para la simulación Monte Carlo"""
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Dimensiones (Radio buttons)
        dim_label = ctk.CTkLabel(input_frame, text="Dimensiones:")
        dim_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        dim_frame = ctk.CTkFrame(input_frame)
        dim_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        dim_1d = ctk.CTkRadioButton(dim_frame, text="1D", variable=self.dimension_var, value="1D", command=self.on_dimension_change)
        dim_1d.grid(row=0, column=0, padx=20, pady=5)
        
        dim_2d = ctk.CTkRadioButton(dim_frame, text="2D", variable=self.dimension_var, value="2D", command=self.on_dimension_change)
        dim_2d.grid(row=0, column=1, padx=20, pady=5)
        
        # Función (solo entrada personalizada)
        func_label = ctk.CTkLabel(input_frame, text="Función:")
        func_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.custom_func_entry = ctk.CTkEntry(input_frame, placeholder_text="Ej: x**2 + y**2 = 1, x**2, exp(x), sin(x)")
        self.custom_func_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Label de ayuda para ecuaciones cónicas
        help_label = ctk.CTkLabel(input_frame, 
                                 text="💡 Ecuaciones cónicas: x**2 + y**2 = 1 (círculo), x**2/4 + y**2/9 = 1 (elipse)\n" +
                                      "Para área entre curvas, usa integración: sqrt(x) - x**2",
                                 font=ctk.CTkFont(size=11),
                                 text_color="gray")
        help_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        # Parámetros de la simulación
        self.entries = {}
        
        # Número de muestras
        n_samples_label = ctk.CTkLabel(input_frame, text="Número de muestras:")
        n_samples_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.entries["n_samples"] = ctk.CTkEntry(input_frame)
        self.entries["n_samples"].insert(0, "10000")
        self.entries["n_samples"].grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Semilla (opcional)
        seed_label = ctk.CTkLabel(input_frame, text="Semilla (opcional):")
        seed_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        self.entries["seed"] = ctk.CTkEntry(input_frame)
        self.entries["seed"].grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        
        # Error máximo IC
        error_label = ctk.CTkLabel(input_frame, text="Error máximo IC:")
        error_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        
        self.entries["max_error"] = ctk.CTkEntry(input_frame)
        self.entries["max_error"].insert(0, "0.05")
        self.entries["max_error"].grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        
        # Rango X
        x_range_label = ctk.CTkLabel(input_frame, text="Rango X [a, b]:")
        x_range_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        
        x_range_frame = ctk.CTkFrame(input_frame)
        x_range_frame.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
        x_range_frame.grid_columnconfigure(0, weight=1)
        x_range_frame.grid_columnconfigure(1, weight=1)
        
        self.entries["x_min"] = ctk.CTkEntry(x_range_frame)
        self.entries["x_min"].insert(0, "0")
        self.entries["x_min"].grid(row=0, column=0, padx=5, sticky="ew")
        
        self.entries["x_max"] = ctk.CTkEntry(x_range_frame)
        self.entries["x_max"].insert(0, "1")
        self.entries["x_max"].grid(row=0, column=1, padx=5, sticky="ew")
        
        # Rango Y (solo para 2D)
        self.y_range_label = ctk.CTkLabel(input_frame, text="Rango Y [c, d]:")
        self.y_range_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        
        self.y_range_frame = ctk.CTkFrame(input_frame)
        self.y_range_frame.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
        self.y_range_frame.grid_columnconfigure(0, weight=1)
        self.y_range_frame.grid_columnconfigure(1, weight=1)
        
        self.entries["y_min"] = ctk.CTkEntry(self.y_range_frame)
        self.entries["y_min"].insert(0, "0")
        self.entries["y_min"].grid(row=0, column=0, padx=5, sticky="ew")
        
        self.entries["y_max"] = ctk.CTkEntry(self.y_range_frame)
        self.entries["y_max"].insert(0, "1")
        self.entries["y_max"].grid(row=0, column=1, padx=5, sticky="ew")
        
        # Inicialmente ocultar los campos de rango Y
        if self.dimension_var.get() == "1D":
            self.y_range_label.grid_remove()
            self.y_range_frame.grid_remove()
    
    def on_dimension_change(self):
        """Manejar cambio de dimensión"""
        dimension = self.dimension_var.get()
        
        if dimension == "1D":
            # Ocultar campos de rango Y
            self.y_range_label.grid_remove()
            self.y_range_frame.grid_remove()
        else:
            # Mostrar campos de rango Y
            self.y_range_label.grid()
            self.y_range_frame.grid()
    
    def create_buttons_section(self):
        """Crear sección de botones"""
        button_frame = ctk.CTkFrame(self.content_frame)
        button_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
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
    
    def create_results_section(self) -> ctk.CTkFrame:
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
            
            value_label = ctk.CTkLabel(results_frame, text="-")
            value_label.grid(row=i+1, column=1, padx=10, pady=5, sticky="e")
            
            self.result_labels[key] = value_label
        
        return results_frame
    
    def create_plot_section(self):
        """Crear sección de gráficos"""
        plot_frame = ctk.CTkFrame(self.content_frame)
        plot_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        plot_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        plot_title = ctk.CTkLabel(
            plot_frame,
            text="Visualización",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        plot_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Tabs para diferentes gráficos
        plot_tabs = ctk.CTkTabview(plot_frame)
        plot_tabs.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Tab para puntos
        self.points_tab = plot_tabs.add("Puntos")
        self.points_tab.grid_columnconfigure(0, weight=1)
        self.points_tab.grid_rowconfigure(0, weight=1)
        
        # Figuras para los gráficos
        self.create_plot_figures()
    
    def create_plot_figures(self):
        """Crear figuras para los gráficos con configuración optimizada"""
        # Crear figura con tamaño adecuado para visualizaciones 1D y 2D
        self.points_fig = Figure(figsize=(12, 9), dpi=PLOT.DPI)
        
        # Configurar fondo y estilo (usando un color de fondo estándar)
        self.points_fig.patch.set_facecolor("#f0f0f0")
        
        # Configurar márgenes amplios para evitar recortes
        self.points_fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
        
        # Crear canvas para visualización
        self.points_canvas = self.create_canvas(self.points_fig, self.points_tab)
    
    def create_canvas(self, figure, parent) -> FigureCanvasTkAgg:
        """Crear canvas para una figura matplotlib con barra de herramientas"""
        # Crear el canvas principal
        canvas = FigureCanvasTkAgg(figure, parent)
        canvas.draw()
        
        # Configurar el canvas para que ocupe todo el espacio disponible
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Añadir barra de herramientas de navegación para interacción
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        
        # Crear frame para la barra de herramientas
        toolbar_frame = ctk.CTkFrame(parent)
        toolbar_frame.grid(row=1, column=0, sticky="ew", padx=10)
        
        # Añadir barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        
        return canvas
    
    def create_formula_section(self):
        """Crear sección de fórmulas"""
        formula_frame = ctk.CTkFrame(self.content_frame)
        formula_frame.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
        formula_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        formula_title = ctk.CTkLabel(
            formula_frame,
            text="Fórmulas Utilizadas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        formula_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Texto de fórmulas
        formulas_text = """
        1. Integración Monte Carlo (1D):
           ∫[a,b] f(x) dx ≈ (b-a) * 1/n * Σ[i=1 to n] f(xi)
           
        2. Integración Monte Carlo (2D):
           ∫∫[a,b]×[c,d] f(x,y) dxdy ≈ (b-a)(d-c) * 1/n * Σ[i=1 to n] f(xi,yi)
           
        3. Error estándar:
           σ = √(1/n * Σ[i=1 to n] (f(xi) - μ)²)
           
        4. Intervalo de confianza (95%):
           IC = [μ - 1.96*σ/√n, μ + 1.96*σ/√n]
        """
        
        formulas_label = ctk.CTkLabel(
            formula_frame,
            text=formulas_text,
            justify="left",
            font=("Courier New", 12)
        )
        formulas_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    
    def run_monte_carlo(self):
        """Ejecutar simulación Monte Carlo"""
        try:
            # Limpiar cualquier error previo
            self.clear_error_message()
            
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs()
            if not is_valid:
                self.show_error_message(error_msg)
                return
            
            # Obtener función a utilizar
            custom_func = self.custom_func_entry.get().strip()
            dimension = self.dimension_var.get()
            
            if not custom_func:
                self.show_error_message("Ingrese una función válida")
                return
            
            # Detectar si es una ecuación cónica (contiene '=')
            is_conic_equation = '=' in custom_func
            
            # Parsear función personalizada
            try:
                if is_conic_equation:
                    # Importar el parser de ecuaciones cónicas
                    from src.core.function_parser import parse_conic_equation, detect_conic_type
                    
                    # Detectar tipo de cónica para informar al usuario
                    conic_type = detect_conic_type(custom_func)
                    self.update_status(f"Detectada ecuación cónica: {conic_type}")
                    
                    # Forzar 2D para ecuaciones cónicas
                    if dimension == "1D":
                        self.dimension_var.set("2D")
                        dimension = "2D"
                        self.show_error_message("Las ecuaciones cónicas requieren 2D. Cambiando automáticamente a 2D.")
                        # Dar tiempo al usuario para ver el mensaje
                        self.master.after(2000, lambda: self.clear_error_message())
                    
                    func = parse_conic_equation(custom_func)
                    
                else:
                    # Función tradicional
                    if dimension == "1D":
                        func = self._crear_funcion_1d(custom_func)
                    else:
                        func = self._create_funcion_2d(custom_func)
                        
            except Exception as e:
                self.show_error_message(f"Error al parsear función: {str(e)}")
                return
            
            # Configurar parámetros
            dimension_int = 1 if dimension == "1D" else 2
            x_range = (values["x_min"], values["x_max"])
            y_range = (values["y_min"], values["y_max"]) if dimension == "2D" else None
            
            # Sugerencias de rangos
            if is_conic_equation and x_range == (0, 1) and y_range == (0, 1):
                # Sugerir rango [-2, 2] para ecuaciones cónicas típicas
                self.show_error_message("Sugerencia: Para ecuaciones cónicas como círculos, considera usar rangos como [-2, 2]")
                self.master.after(3000, lambda: self.clear_error_message())
            
            # Convertir seed a None si está vacío
            seed = values.get("seed")
            if seed == "" or seed is None:
                seed = None
            else:
                seed = int(seed)
            
            # Ejecutar simulación
            status_msg = "Ejecutando simulación Monte Carlo..."
            if is_conic_equation:
                status_msg += f" para ecuación cónica ({conic_type})"
            self.update_status(status_msg)
            
            results = self.mc_engine.simulate(
                func=func,
                n_samples=values["n_samples"],
                seed=seed,
                max_error=values["max_error"],
                dimensions=dimension_int,
                x_range=x_range,
                y_range=y_range
            )
            
            # Guardar resultados
            self.last_result = results
            
            # Actualizar interfaz
            self.update_results(results)
            self.update_plots(results, dimension_int, func, x_range, y_range)
            self.update_status("Simulación completada")
            
        except Exception as e:
            self.show_error_message(f"Error en simulación: {str(e)}")
    
    def validate_inputs(self):
        """Validar entradas de la simulación"""
        required_numeric = ["n_samples", "max_error", "x_min", "x_max"]
        dimension = self.dimension_var.get()
        
        if dimension == "2D":
            required_numeric.extend(["y_min", "y_max"])
        
        # Validar campos numéricos
        values = {}
        for field in required_numeric:
            if field not in self.entries:
                return False, {}, f"Campo requerido '{field}' no encontrado"
            
            entry = self.entries[field]
            value_str = entry.get().strip()
            
            if not value_str:
                return False, {}, f"El campo '{field}' no puede estar vacío"
            
            try:
                if field == "n_samples":
                    value = int(value_str)
                    if value <= 0:
                        return False, {}, "El número de muestras debe ser positivo"
                else:
                    value = float(value_str)
                values[field] = value
            except ValueError:
                return False, {}, f"Valor inválido en '{field}': debe ser un número"
        
        # Validar semilla (opcional)
        seed_str = self.entries["seed"].get().strip()
        if seed_str:
            try:
                values["seed"] = int(seed_str)
            except ValueError:
                return False, {}, "La semilla debe ser un número entero"
        
        # Validar rangos
        if values["x_max"] <= values["x_min"]:
            return False, {}, "El rango X debe ser [a,b] con a < b"
        
        if dimension == "2D" and values["y_max"] <= values["y_min"]:
            return False, {}, "El rango Y debe ser [c,d] con c < d"
        
        return True, values, ""
    
    def update_results(self, results):
        """Actualizar sección de resultados con los valores calculados"""
        # Actualizar etiquetas de resultados
        self.result_labels["resultado_integracion"].configure(text=f"{results['resultado_integracion']:.6f}")
        self.result_labels["desviacion_estandar"].configure(text=f"{results['desviacion_estandar']:.6f}")
        self.result_labels["error_estandar"].configure(text=f"{results['error_estandar']:.6f}")
        
        ic_lower, ic_upper = results['intervalo_confianza']
        self.result_labels["intervalo_confianza"].configure(text=f"[{ic_lower:.6f}, {ic_upper:.6f}]")
        
        self.result_labels["volumen"].configure(text=f"{results['volumen']:.6f}")
    
    def update_plots(self, results, dimensions, func=None, x_range=None, y_range=None):
        """Actualizar gráficos con los resultados de la simulación"""
        # Limpiar figuras anteriores
        self.points_fig.clear()
        
        # Configurar el estilo global de la figura
        self.points_fig.set_facecolor('#2b2b2b')
        
        # Gráfico de puntos
        if dimensions == 1:
            # Para 1D: Crear un subplot normal
            ax_points = self.points_fig.add_subplot(111)
            self.plot_1d_integration(ax_points, results, func, x_range)
        else:
            # Para 2D: Crear un subplot 3D con configuración óptima
            ax_points = self.points_fig.add_subplot(111, projection='3d')
            
            # Ajustar tamaño y espaciado para la visualización 3D
            self.points_fig.set_figheight(9)  # Altura aumentada para 3D
            self.points_fig.set_figwidth(12)  # Ancho adecuado para 3D
            
            # Dar más espacio a los márgenes para la visualización 3D
            self.points_fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)
            
            # Llamar a la función para graficar la integración 2D
            self.plot_2d_integration(ax_points, results, func, x_range, y_range)
        
        # Aplicar configuración global a la figura
        self.points_fig.tight_layout()
        
        # Actualizar el canvas para mostrar los cambios
        self.points_canvas.draw()
        
        # Mostrar mensaje de éxito
        self.update_status("Visualización actualizada correctamente")
    
    def plot_1d_integration(self, ax, results, func, x_range):
        """Graficar integración 1D con función y puntos"""
        if func is None or x_range is None:
            return
            
        # Crear puntos para graficar la función con mayor resolución
        x_vals = np.linspace(x_range[0], x_range[1], 1000)
        y_vals = np.array([func(x) for x in x_vals])
        
        # Graficar la función original con línea más visible
        ax.plot(x_vals, y_vals, 'cyan', linewidth=2.5, label='f(x)', alpha=0.9)
        
        # Rellenar el área bajo la curva (solo donde y >= 0 para visualización clara)
        y_fill = np.maximum(y_vals, 0)
        ax.fill_between(x_vals, 0, y_fill, alpha=0.3, color='cyan', label='Área bajo la curva')
        
        # Obtener puntos de la simulación
        points_inside = results['puntos_dentro']
        points_outside = results['puntos_fuera']
        
        # Graficar puntos clasificados con mejor visibilidad
        if len(points_inside) > 0:
            # Usar directamente los puntos generados en la simulación
            # Los puntos dentro ya tienen coordenadas (x,y) correctas
            ax.scatter(points_inside[:, 0], points_inside[:, 1], 
                       color='lime', s=60, alpha=0.8, label='Puntos de éxito', 
                       marker='o', edgecolors='darkgreen')
        
        if len(points_outside) > 0:
            # Usar directamente los puntos generados en la simulación
            # Los puntos fuera ya tienen coordenadas (x,y) correctas
            ax.scatter(points_outside[:, 0], points_outside[:, 1], 
                       color='red', s=60, alpha=0.8, label='Puntos de fracaso', 
                       marker='x', linewidths=2)
        
        # Configurar gráfico con mejor presentación
        ax.set_facecolor('#2b2b2b')  # Fondo oscuro para mejor contraste
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('f(x)', fontsize=14)
        ax.set_title('Integración Monte Carlo 1D', fontsize=16, fontweight='bold')
        ax.legend(loc='upper right', fontsize=12, framealpha=0.8)
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # Ajustar límites del eje Y para incluir todos los puntos
        y_max = np.max(y_vals)
        ax.set_ylim(-0.1 * y_max, y_max * 1.6)  # Ampliar límite superior para puntos rojos
        
        # Agregar anotaciones con resultados con mejor visibilidad
        integral_val = results['resultado_integracion']
        ci_lower, ci_upper = results['intervalo_confianza']
        ax.annotate(f'Integral: {integral_val:.4f}\nIC: [{ci_lower:.4f}, {ci_upper:.4f}]', 
                    xy=(0.02, 0.98), xycoords='axes fraction',
                    fontsize=12, weight='bold', verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9, edgecolor='black'))
    
    def plot_2d_integration(self, ax, results, func, x_range, y_range):
        """Graficar integración 2D con superficie 3D y puntos
        
        Esta implementación se basa en la que funciona correctamente en el script de prueba.
        """
        if func is None or x_range is None or y_range is None:
            return
        
        # Configurar el aspecto del eje para mejor visualización
        ax.set_facecolor('#2b2b2b')
        
        # Configurar elementos 3D
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('white')
        ax.yaxis.pane.set_edgecolor('white')
        ax.zaxis.pane.set_edgecolor('white')
        ax.tick_params(colors='white')
            
        # Crear malla para la superficie con resolución óptima
        x_surf = np.linspace(x_range[0], x_range[1], 30)
        y_surf = np.linspace(y_range[0], y_range[1], 30)
        X, Y = np.meshgrid(x_surf, y_surf)
        
        # Evaluar función en la malla (usar x, y como parámetros para 2D)
        Z = np.zeros_like(X)
        for i in range(len(x_surf)):
            for j in range(len(y_surf)):
                Z[j, i] = func(X[j, i], Y[j, i])
        
        # Graficar superficie con colores vivos
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, 
                              linewidth=0, antialiased=True)
        
        # Obtener puntos de la simulación
        points_inside = results.get('puntos_dentro', np.array([]))
        points_outside = results.get('puntos_fuera', np.array([]))
        
        # Graficar puntos clasificados con mejor visibilidad
        if len(points_inside) > 0:
            # Usar directamente los puntos generados en la simulación con sus coordenadas 3D
            ax.scatter(points_inside[:, 0], points_inside[:, 1], points_inside[:, 2],
                      color='lime', s=40, alpha=0.9, label='Puntos de éxito', 
                      marker='o', edgecolors='darkgreen')
        
        if len(points_outside) > 0:
            # Usar directamente los puntos generados en la simulación con sus coordenadas 3D
            ax.scatter(points_outside[:, 0], points_outside[:, 1], points_outside[:, 2],
                      color='red', s=40, alpha=0.9, label='Puntos de fracaso', 
                      marker='x', linewidths=2)
        
        # Configurar gráfico 3D con etiquetas claras
        ax.set_xlabel('x', fontsize=14, labelpad=10, color='white')
        ax.set_ylabel('y', fontsize=14, labelpad=10, color='white')
        ax.set_zlabel('f(x,y)', fontsize=14, labelpad=10, color='white')
        ax.set_title('Integración Monte Carlo 2D', fontsize=16, fontweight='bold', color='white')
        
        # Agregar leyenda con mejor visibilidad
        ax.legend(loc='upper right', fontsize=12, framealpha=0.8)
        
        # Ajustar vista para mejor visualización
        ax.view_init(elev=30, azim=45)
        
        # Agregar barra de color
        cbar = self.points_fig.colorbar(surf, ax=ax, shrink=0.7, aspect=10, pad=0.1)
        cbar.set_label('f(x,y)', fontsize=12, color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        cbar.outline.set_edgecolor('white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        
        # Agregar anotaciones con resultados
        integral_val = results['resultado_integracion']
        ci_lower, ci_upper = results['intervalo_confianza']
        ax.text2D(0.02, 0.98, f'Integral: {integral_val:.4f}\nIC: [{ci_lower:.4f}, {ci_upper:.4f}]', 
                 transform=ax.transAxes, fontsize=12, weight='bold', color='white',
                 bbox=dict(boxstyle='round', facecolor='#444444', alpha=0.9))
    
    def plot_histogram(self, ax, results):
        """Graficar histograma de valores de la función"""
        # Combinar puntos dentro y fuera para el histograma
        all_points = np.vstack((results['puntos_dentro'], results['puntos_fuera']))
        
        if len(all_points) > 0:
            # Crear histograma
            n, bins, patches = ax.hist(all_points[:, 0], bins=30, alpha=0.7, color='blue')
            
            # Configurar gráfico
            ax.set_xlabel('Valores')
            ax.set_ylabel('Frecuencia')
            ax.set_title('Histograma de Distribución')
            ax.grid(True, linestyle='--', alpha=0.7)
    
    def plot_convergence(self, ax, results):
        """Graficar convergencia del método"""
        convergence_data = results['convergencia']
        
        if len(convergence_data) > 0:
            # Extraer datos de convergencia
            samples = convergence_data[:, 0]
            values = convergence_data[:, 1]
            
            # Graficar convergencia
            ax.plot(samples, values, marker='o', linestyle='-', color='blue')
            
            # Línea de valor final
            ax.axhline(y=results['resultado_integracion'], color='red', linestyle='--', 
                      label=f'Valor final: {results["resultado_integracion"]:.6f}')
            
            # Configurar gráfico
            ax.set_xlabel('Número de muestras')
            ax.set_ylabel('Estimación de la integral')
            ax.set_title('Convergencia del Método')
            ax.set_xscale('log')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend()
    
    def clear_results(self):
        """Limpiar resultados y gráficos"""
        # Limpiar etiquetas de resultados
        for key in self.result_labels:
            self.result_labels[key].configure(text="-")
        
        # Limpiar gráficos
        self.points_fig.clear()
        self.points_canvas.draw()
        
        # Limpiar status
        self.update_status("")
        
        # Limpiar entrada personalizada
        self.custom_func_entry.delete(0, 'end')
    
    def update_status(self, message):
        """Actualizar mensaje de estado"""
        # Si hay un widget de status, actualizarlo
        status_label = getattr(self, 'status_label', None)
        if status_label:
            status_label.configure(text=message)
        else:
            # Crear un nuevo widget de status si no existe
            self.status_label = ctk.CTkLabel(
                self.content_frame,
                text=message,
                font=ctk.CTkFont(size=12),
                text_color=["gray60", "gray50"]
            )
            self.status_label.grid(row=6, column=0, pady=5, padx=20, sticky="ew")
    
    def show_error_message(self, message):
        """Mostrar mensaje de error"""
        self.update_status(f"Error: {message}")
    
    def clear_error_message(self):
        """Limpiar mensaje de error"""
        self.update_status("")
