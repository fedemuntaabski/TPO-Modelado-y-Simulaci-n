"""
Mixins para funcionalidades compartidas en las pestañas de UI.

Implementa el patrón Mixin siguiendo principios SOLID y DRY.
Permite composición de funcionalidades sin herencia múltiple compleja.
"""

from typing import Dict, Any, Optional, Callable
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.ui.components.base_tab import BaseTab
from config.settings import PLOT_CONFIG
from .constants import PLOT


class InputValidationMixin:
    """
    Mixin para validación de entradas de usuario.
    Principio de responsabilidad única: solo validación.
    """

    def validate_numeric_inputs(self, entries: Dict[str, ctk.CTkEntry],
                               required_fields: list) -> tuple[bool, Dict[str, float], str]:
        """
        Valida entradas numéricas comunes.
        Principio DRY: validación reutilizable.

        Returns:
            Tupla (is_valid, values_dict, error_message)
        """
        values = {}

        for field_name in required_fields:
            if field_name not in entries:
                return False, {}, f"Campo requerido '{field_name}' no encontrado"

            entry = entries[field_name]
            value_str = entry.get().strip()

            if not value_str:
                return False, {}, f"El campo '{field_name}' no puede estar vacío"

            try:
                if '.' in value_str or 'e' in value_str.lower():
                    values[field_name] = float(value_str)
                else:
                    values[field_name] = int(value_str)
            except ValueError:
                return False, {}, f"El campo '{field_name}' debe ser un número válido"

        return True, values, ""

    def validate_function_input(self, entries: Dict[str, ctk.CTkEntry],
                               function_field: str = "función_fx") -> tuple[bool, str, str]:
        """
        Valida entrada de función matemática.
        Principio DRY: validación de funciones reutilizable.

        Returns:
            Tupla (is_valid, function_string, error_message)
        """
        if function_field not in entries:
            return False, "", f"Campo de función '{function_field}' no encontrado"

        function_str = entries[function_field].get().strip()

        if not function_str:
            return False, "", "La función no puede estar vacía"

        # Validación básica de sintaxis
        invalid_chars = [';', 'exec', 'eval', '__']
        for char in invalid_chars:
            if char in function_str.lower():
                return False, "", f"Caracteres no permitidos en la función: {char}"

        return True, function_str, ""


class ResultDisplayMixin:
    """
    Mixin para mostrar resultados de cálculos.
    Principio de responsabilidad única: solo presentación de resultados.
    """

    def display_calculation_results(self, results_text_widget: ctk.CTkTextbox,
                                   title: str, main_data: Dict[str, Any],
                                   sections: Optional[Dict[str, Any]] = None) -> None:
        """
        Muestra resultados de cálculo de forma estandarizada.
        Principio DRY: formato consistente en todas las pestañas.
        """
        text = f"{title}\n"
        text += "=" * len(title) + "\n\n"

        # Datos principales
        for key, value in main_data.items():
            if isinstance(value, (int, float)):
                if abs(value) < 1e-3 or abs(value) > 1e6:
                    text += f"{key}: {value:.2e}\n"
                else:
                    text += f"{key}: {value:.8f}\n"
            else:
                text += f"{key}: {value}\n"

        # Secciones adicionales
        if sections:
            for section_name, section_data in sections.items():
                text += f"\n{section_name}:\n"
                text += "-" * len(section_name) + "\n"

                if isinstance(section_data, dict):
                    for key, value in section_data.items():
                        text += f"{key}: {value}\n"
                elif isinstance(section_data, (list, tuple)):
                    for item in section_data:
                        text += f"• {item}\n"
                else:
                    text += f"{section_data}\n"

        # Limpiar y mostrar
        results_text_widget.delete("0.0", "end")
        results_text_widget.insert("0.0", text)

    def display_iteration_table(self, results_text_widget: ctk.CTkTextbox,
                               iteration_data: list, method_name: str) -> None:
        """
        Muestra tabla de iteraciones de forma estandarizada.
        Principio DRY: formato de tablas reutilizable.
        """
        if not iteration_data:
            return

        table_text = f"\nTABLA DE ITERACIONES - {method_name}\n"
        table_text += "-" * 50 + "\n"
        table_text += "Iter | Datos de la iteración\n"
        table_text += "-" * 50 + "\n"

        for i, data in enumerate(iteration_data[:15]):  # Limitar a 15 iteraciones
            iteration = data.get('iteration', i+1)
            table_text += f"{iteration:4d} | "

            # Formatear según el método
            if 'c' in data:  # Bisección
                table_text += f"a={data['a']:.6f}, b={data['b']:.6f}, c={data['c']:.6f}, error={data['error']:.2e}"
            elif 'x_n' in data and 'x_n_plus_1' in data:  # Newton-Raphson
                table_text += f"x_n={data['x_n']:.6f}, x_n+1={data['x_n_plus_1']:.6f}, error={data['error']:.2e}"
            elif 'g_x_n' in data:  # Punto fijo
                table_text += f"x_n={data['x_n']:.6f}, g(x_n)={data['g_x_n']:.6f}, error={data['error']:.2e}"
            elif 'x_aitken' in data:  # Aitken
                table_text += f"x={data['x']:.6f}, x1={data['x1']:.6f}, x2={data['x2']:.6f}, x_aitken={data['x_aitken']:.6f}, error={data['error']:.2e}"
            else:
                table_text += str(data)

            table_text += "\n"

        if len(iteration_data) > 15:
            table_text += "... (mostrando solo las primeras 15 iteraciones)\n"

        # Agregar al widget existente
        current_text = results_text_widget.get("0.0", "end")
        results_text_widget.delete("0.0", "end")
        results_text_widget.insert("0.0", current_text + table_text)


class PlottingMixin:
    """
    Mixin para funcionalidades de graficación.
    Principio de responsabilidad única: solo graficación.
    """

    def setup_plot_area(self, plot_frame: ctk.CTkFrame) -> tuple:
        """
        Configura área de graficación de forma estandarizada.
        Principio DRY: configuración de matplotlib reutilizable.

        Returns:
            Tupla (figure, canvas)
        """
        # Limpiar widgets existentes
        for widget in plot_frame.winfo_children():
            widget.destroy()

        # Configurar el plot_frame para expansión
        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_columnconfigure(0, weight=1)

        # Crear figura con configuración consistente
        fig = plt.figure(figsize=(PLOT.FIGURE_WIDTH, PLOT.FIGURE_HEIGHT), dpi=PLOT.DPI)
        fig.patch.set_facecolor('#2b2b2b')

        # Crear canvas
        canvas = FigureCanvasTkAgg(fig, plot_frame)
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        return fig, canvas

    def apply_standard_plot_styling(self, ax, title: str = "",
                                   xlabel: str = "", ylabel: str = "") -> None:
        """
        Aplica estilo estándar a los gráficos.
        Principio DRY: estilo visual unificado.
        """
        ax.set_facecolor('#2b2b2b')
        ax.set_title(title, color='white', fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel, color='white', fontsize=12)
        ax.set_ylabel(ylabel, color='white', fontsize=12)

        # Configurar grid
        if PLOT_CONFIG["grid"]:
            ax.grid(True, alpha=0.3, color='white')

        # Configurar ticks
        ax.tick_params(colors='white', labelsize=10)

        # Configurar spines
        for spine in ax.spines.values():
            spine.set_color('white')

        # Leyenda si está habilitada
        if PLOT_CONFIG["legend"]:
            legend = ax.legend()
            if legend:
                legend.get_frame().set_facecolor('#2b2b2b')
                legend.get_frame().set_edgecolor('white')
                for text in legend.get_texts():
                    text.set_color('white')

    def plot_function_with_points(self, fig, ax, function: Callable[[float], float],
                                 x_range: tuple, points: list = None,
                                 point_labels: list = None) -> None:
        """
        Grafica función con puntos destacados.
        Principio DRY: graficación de funciones reutilizable.
        """
        x_min, x_max = x_range
        x_vals = [x_min + i * (x_max - x_min) / 200 for i in range(201)]
        y_vals = [function(x) for x in x_vals]

        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')

        # Graficar puntos si se proporcionan
        if points:
            x_points = [p[0] for p in points]
            y_points = [p[1] for p in points]

            ax.scatter(x_points, y_points, color='red', s=50, zorder=5)

            if point_labels:
                for i, (x, y) in enumerate(zip(x_points, y_points)):
                    if i < len(point_labels):
                        ax.annotate(point_labels[i], (x, y),
                                  xytext=(10, 10), textcoords='offset points',
                                  color='white', fontsize=10,
                                  bbox=dict(boxstyle='round,pad=0.3',
                                           facecolor='#2b2b2b', alpha=0.8))

        ax.legend()

    def plot_multiple_functions(self, fig, ax, functions: list, x_range: tuple) -> None:
        """
        Grafica múltiples funciones en el mismo gráfico.
        Principio DRY: graficación de múltiples funciones reutilizable.
        
        Args:
            functions: Lista de tuplas (function, color, label)
            x_range: Tupla (x_min, x_max)
        """
        x_min, x_max = x_range
        x_vals = [x_min + i * (x_max - x_min) / 200 for i in range(201)]
        
        for func, color, label in functions:
            y_vals = [func(x) for x in x_vals]
            ax.plot(x_vals, y_vals, color=color, linewidth=2, label=label)
        
        ax.legend()
