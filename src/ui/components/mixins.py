"""
Mixins para funcionalidades compartidas en las pestañas de UI.

Implementa el patrón Mixin siguiendo principios SOLID y DRY.
Permite composición de funcionalidades sin herencia múltiple compleja.
"""

from typing import Dict, Any, Optional, Callable
import customtkinter as ctk
from customtkinter import CTkScrollableFrame
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

    def display_iteration_table_popup(self, parent_widget, iteration_data, method_name: str) -> None:
        """
        Muestra tabla de iteraciones en un popup movible y cerrable.
        Implementa una interfaz moderna y legible.
        """
        # Verificar si hay datos de iteración
        if not iteration_data:
            return
            
        # Convertir a lista si es un solo diccionario
        if isinstance(iteration_data, dict):
            iteration_data = [iteration_data]
            
        # Crear ventana popup
        popup = ctk.CTkToplevel(parent_widget)
        popup.title(f"Tabla de Iteraciones - {method_name}")
        popup.geometry("900x650")
        popup.resizable(True, True)
        
        # Hacer que sea modal pero movible
        popup.transient(parent_widget)
        popup.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(popup)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"Tabla de Iteraciones - {method_name}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(15, 10))
        
        # Descripción del método
        description = ""
        if method_name.upper().startswith("BISECCIÓN"):
            description = "Método de búsqueda de raíces que divide el intervalo repetidamente"
        elif method_name.upper().startswith("NEWTON-RAPHSON"):
            description = "Método iterativo que utiliza la derivada para aproximar raíces"
        elif method_name.upper().startswith("PUNTO FIJO"):
            description = "Método que convierte f(x)=0 a x=g(x) y resuelve iterativamente"
        elif method_name.upper().startswith("AITKEN"):
            description = "Método de aceleración que mejora la convergencia de punto fijo"
        elif method_name.upper().startswith("SECANTE"):
            description = "Método que aproxima la derivada con dos puntos consecutivos"
            
        if description:
            desc_label = ctk.CTkLabel(
                main_frame,
                text=description,
                font=ctk.CTkFont(size=13)
            )
            desc_label.pack(pady=(0, 15))
        
        # Frame para la tabla con scroll
        table_container = ctk.CTkFrame(main_frame)
        table_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Crear tabla
        self._create_iteration_table(table_container, iteration_data, method_name)
        
        # Información adicional
        if len(iteration_data) > 0:
            info_frame = ctk.CTkFrame(main_frame)
            info_frame.pack(fill="x", padx=10, pady=(5, 10))
            
            # Mostrar resultado final
            last_iter = iteration_data[-1]
            
            # Determinar si convergió (basado en número de iteraciones o flag de convergencia)
            if isinstance(last_iter, dict) and 'converged' in last_iter:
                converged = last_iter['converged']
            else:
                # Aproximación basada en número de iteraciones máximas
                max_iterations = 100  # Valor predeterminado
                converged = len(iteration_data) < max_iterations
            
            # Obtener error final
            error_final = last_iter.get('error', 0) if isinstance(last_iter, dict) else 0
            
            result_label = ctk.CTkLabel(
                info_frame,
                text=f"Resultado final: {len(iteration_data)} iteraciones | " + 
                     f"Error final: {error_final:.2e} | " +
                     f"Estado: {'✓ Convergió' if converged else '⚠ Alcanzó máximo de iteraciones'}",
                font=ctk.CTkFont(size=13)
            )
            result_label.pack(pady=10, padx=20)
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        close_button = ctk.CTkButton(
            buttons_frame,
            text="Cerrar",
            command=popup.destroy,
            font=ctk.CTkFont(size=13, weight="bold"),
            width=120
        )
        close_button.pack(side="right", padx=20, pady=10)
        
        # Centrar la ventana
        popup.geometry("900x650+100+100")
    
    def _create_iteration_table(self, parent_frame, iteration_data, method_name: str) -> None:
        """
        Crea una tabla de iteraciones visualmente mejorada usando un enfoque basado en grid.
        """
        # Asegurar que iteration_data sea una lista
        if isinstance(iteration_data, dict):
            iteration_data = [iteration_data]
            
        # Crear frame con scroll para la tabla
        table_canvas = ctk.CTkScrollableFrame(parent_frame)
        table_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Definir los headers según el método
        if method_name.upper().startswith("BISECCIÓN"):
            headers = ["Iter", "a", "b", "c", "f(c)", "Error"]
        elif method_name.upper().startswith("NEWTON-RAPHSON"):
            headers = ["Iter", "xₙ", "f(xₙ)", "f'(xₙ)", "xₙ₊₁", "Error"]
        elif method_name.upper().startswith("PUNTO FIJO"):
            headers = ["Iter", "xₙ", "g(xₙ)", "Error"]
        elif method_name.upper().startswith("AITKEN"):
            headers = ["Iter", "x", "x₁", "x₂", "x_aitken", "Error"]
        elif method_name.upper().startswith("SECANTE"):
            headers = ["Iter", "xₙ₋₁", "xₙ", "xₙ₊₁", "f(xₙ)", "Error"]
        else:
            # Para métodos no reconocidos, intentar derivar los headers del diccionario
            if iteration_data and isinstance(iteration_data[0], dict):
                # Si el primer elemento es un diccionario, usar sus claves como headers
                if len(iteration_data[0]) <= 8:  # Si hay pocas claves, usar todas
                    headers = ["Iter"] + list(iteration_data[0].keys())
                    if "iteration" in headers:
                        headers.remove("iteration")  # Ya tenemos la columna Iter
                else:
                    # Si hay muchas claves, usar columna genérica
                    headers = ["Iter", "Datos"]
            else:
                # Default genérico
                headers = ["Iter", "Datos"]
        
        # Configurar ancho de columnas
        col_width = 115
        iter_width = 60
        error_width = 130
        
        # Color para headers y filas alternadas
        header_bg = "#1a1a2e"
        alt_row_bg = "#2a2a3e"
        
        # Configurar el grid para que las columnas se distribuyan adecuadamente
        for i in range(len(headers)):
            table_canvas.grid_columnconfigure(i, weight=1)
        
        # Crear headers
        for col, header in enumerate(headers):
            width = iter_width if col == 0 else error_width if header == "Error" else col_width
            frame = ctk.CTkFrame(table_canvas, fg_color=header_bg, corner_radius=0)
            frame.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
            
            label = ctk.CTkLabel(
                frame, 
                text=header,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="center",
                width=width,
                height=30
            )
            label.pack(fill="both", expand=True)
        
            # Mostrar datos (limitar a 100 para mejorar rendimiento)
        max_rows = min(len(iteration_data), 100)
        for row, data in enumerate(iteration_data[:max_rows], start=1):
            row_bg = alt_row_bg if row % 2 == 0 else None
            
            # Columna de iteración
            iter_frame = ctk.CTkFrame(table_canvas, fg_color=row_bg, corner_radius=0)
            iter_frame.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
            
            # Usar el valor de iteración si existe, o el índice si no
            iter_value = data.get('iteration', row) if isinstance(data, dict) else row
            
            iter_label = ctk.CTkLabel(
                iter_frame,
                text=str(iter_value),
                font=ctk.CTkFont(size=12),
                anchor="center",
                width=iter_width
            )
            iter_label.pack(fill="both")
            
            # Extraer datos según el método
            if not isinstance(data, dict):
                # Si no es un diccionario, mostrar como texto en una sola columna
                values = [str(data)]
            elif method_name.upper().startswith("BISECCIÓN"):
                values = [
                    f"{data.get('a', 0):.6f}",
                    f"{data.get('b', 0):.6f}",
                    f"{data.get('c', 0):.6f}",
                    f"{data.get('f_c', 0):.6f}",
                    f"{data.get('error', 0):.2e}"
                ]
            elif method_name.upper().startswith("NEWTON-RAPHSON"):
                values = [
                    f"{data.get('x_n', 0):.6f}",
                    f"{data.get('f_x_n', 0):.6f}",
                    f"{data.get('df_x_n', 0):.6f}",
                    f"{data.get('x_n_plus_1', 0):.6f}",
                    f"{data.get('error', 0):.2e}"
                ]
            elif method_name.upper().startswith("PUNTO FIJO"):
                values = [
                    f"{data.get('x_n', 0):.6f}",
                    f"{data.get('g_x_n', 0):.6f}",
                    f"{data.get('error', 0):.2e}"
                ]
            elif method_name.upper().startswith("AITKEN"):
                values = [
                    f"{data.get('x', 0):.6f}",
                    f"{data.get('x1', 0):.6f}",
                    f"{data.get('x2', 0):.6f}",
                    f"{data.get('x_aitken', 0):.6f}",
                    f"{data.get('error', 0):.2e}"
                ]
            elif method_name.upper().startswith("SECANTE"):
                values = [
                    f"{data.get('x_prev', 0):.6f}",
                    f"{data.get('x_curr', 0):.6f}",
                    f"{data.get('x_new', 0):.6f}",
                    f"{data.get('f_curr', 0):.6f}",
                    f"{data.get('error', 0):.2e}"
                ]
            else:
                # Para casos genéricos o no reconocidos
                if isinstance(data, dict):
                    # Si tenemos headers específicos, usarlos para extraer valores
                    if len(headers) > 2:  # Más allá de solo "Iter" y "Datos"
                        values = []
                        for header in headers[1:]:  # Saltamos el header "Iter"
                            if header in data:
                                val = data[header]
                                if isinstance(val, (int, float)):
                                    if header == "error" or abs(val) < 0.0001 or abs(val) > 100000:
                                        values.append(f"{val:.2e}")
                                    else:
                                        values.append(f"{val:.6f}")
                                else:
                                    values.append(str(val))
                            else:
                                values.append("N/A")
                    else:
                        # Formato genérico: todos los datos en una columna
                        formatted_items = []
                        for k, v in data.items():
                            if k == "iteration":
                                continue  # Saltamos la iteración que ya mostramos
                            if isinstance(v, (int, float)):
                                if k == 'error' or abs(v) < 0.0001 or abs(v) > 100000:
                                    formatted_items.append(f"{k}: {v:.2e}")
                                else:
                                    formatted_items.append(f"{k}: {v:.6f}")
                            else:
                                formatted_items.append(f"{k}: {v}")
                        values = [", ".join(formatted_items)]
                else:
                    values = [str(data)]
                    
            # Asegurar que tengamos suficientes valores para todas las columnas
            expected_cols = len(headers) - 1  # -1 porque la columna "Iter" ya está manejada
            if len(values) < expected_cols:
                values.extend([""] * (expected_cols - len(values)))
            elif len(values) > expected_cols and expected_cols > 0:
                # Si hay más valores que columnas, concatenar los extras en la última columna
                extra_values = values[expected_cols-1:]
                values = values[:expected_cols-1] + [", ".join(extra_values)]
            
            # Mostrar valores
            for col, value in enumerate(values, start=1):
                width = error_width if col == len(values) else col_width
                cell_frame = ctk.CTkFrame(table_canvas, fg_color=row_bg, corner_radius=0)
                cell_frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                
                # Si el texto es demasiado largo, agregar ellipsis
                if len(value) > 20:
                    display_value = value[:17] + "..."
                else:
                    display_value = value
                
                cell_label = ctk.CTkLabel(
                    cell_frame,
                    text=display_value,
                    font=ctk.CTkFont(size=12),
                    anchor="center",
                    width=width
                )
                cell_label.pack(fill="both", expand=True)
                
                # Agregar tooltip para valores largos
                if len(value) > 20:
                    cell_label._tooltip_label = value  # Almacenar valor completo para tooltip
        
        # Mensaje si hay más iteraciones
        if len(iteration_data) > max_rows:
            note_frame = ctk.CTkFrame(table_canvas)
            note_frame.grid(row=max_rows+1, column=0, columnspan=len(headers), 
                           sticky="ew", padx=5, pady=10)
            
            note_label = ctk.CTkLabel(
                note_frame,
                text=f"Mostrando {max_rows} de {len(iteration_data)} iteraciones",
                font=ctk.CTkFont(size=12, slant="italic")
            )
            note_label.pack(pady=5)


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
