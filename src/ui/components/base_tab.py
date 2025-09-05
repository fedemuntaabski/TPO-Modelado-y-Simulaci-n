"""
Componente base para todas las pestañas de la interfaz.

Implementa el patrón Template Method siguiendo principios SOLID.
Proporciona funcionalidad común reutilizable (DRY).
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import Callable, Any, Optional
import logging

from config.settings import UI_CONFIG, PLOT_CONFIG

logger = logging.getLogger(__name__)


class BaseTab(ctk.CTkFrame):
    """
    Clase base para todas las pestañas.
    Implementa el patrón Template Method (SOLID - Open/Closed Principle).
    """
    
    def __init__(self, parent, title: str):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configurar la interfaz base (Template Method).
        Principio de inversión de dependencias: define la estructura,
        las subclases implementan los detalles específicos.
        """
        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Scroll frame principal
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            self.scroll_frame,
            text=self.title,
            font=ctk.CTkFont(size=UI_CONFIG["title_font_size"], weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # Container para contenido específico
        self.content_frame = ctk.CTkFrame(self.scroll_frame)
        self.content_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Hook para subclases
        self.create_content()
    
    def create_content(self):
        """
        Método abstracto para crear contenido específico.
        Cada subclase debe implementar este método (Template Method).
        """
        raise NotImplementedError("Las subclases deben implementar create_content()")
    
    def create_input_section(self, labels_and_defaults: dict) -> dict:
        """
        Crea una sección de entrada estándar.
        Principio DRY: reutilizable en todas las pestañas.
        
        Args:
            labels_and_defaults: Dict con {label: default_value}
            
        Returns:
            Dict con {field_name: entry_widget}
        """
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)
        
        entries = {}
        
        for i, (label, default) in enumerate(labels_and_defaults.items()):
            # Label
            ctk.CTkLabel(input_frame, text=label).grid(
                row=i, column=0, padx=10, pady=5, sticky="w"
            )
            
            # Entry
            entry = ctk.CTkEntry(input_frame, placeholder_text=str(default))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entry.insert(0, str(default))
            
            # Nombre del campo (sin caracteres especiales)
            field_name = label.lower().replace(" ", "_").replace(":", "").replace("(", "").replace(")", "")
            entries[field_name] = entry
        
        return entries
    
    def create_methods_section(self, methods: list) -> ctk.CTkFrame:
        """
        Crea una sección de botones para métodos.
        Principio DRY: layout consistente en todas las pestañas.
        
        Args:
            methods: Lista de tuplas (name, command)
            
        Returns:
            Frame contenedor de los botones
        """
        methods_frame = ctk.CTkFrame(self.content_frame)
        methods_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        for i, (name, command) in enumerate(methods):
            btn = ctk.CTkButton(
                methods_frame,
                text=name,
                command=command,
                height=35
            )
            btn.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            methods_frame.grid_columnconfigure(i, weight=1)
        
        return methods_frame
    
    def create_results_section(self) -> tuple:
        """
        Crea la sección de resultados estándar.
        Principio DRY: layout consistente para mostrar resultados.
        
        Returns:
            Tupla (results_frame, text_widget, plot_frame)
        """
        # Área de resultados
        results_frame = ctk.CTkFrame(self.content_frame)
        results_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        results_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(3, weight=1)
        
        # Texto de resultados
        text_widget = ctk.CTkTextbox(results_frame, height=200)
        text_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        results_frame.grid_rowconfigure(0, weight=1)
        
        # Frame para gráfico
        plot_frame = ctk.CTkFrame(results_frame)
        plot_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        return results_frame, text_widget, plot_frame
    
    def create_function_from_string(self, expr: str) -> Optional[Callable[[float], float]]:
        """
        Crea una función evaluable desde una expresión string.
        Principio DRY: reutilizable en todas las pestañas que necesiten funciones.
        Principio KISS: implementación simple y segura.
        """
        # Lista de funciones matemáticas permitidas
        allowed_names = {
            "x": None,  # Variable independiente
            "t": None,  # Variable de tiempo (para EDOs)
            "y": None,  # Variable dependiente (para EDOs)
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "log": np.log, "log10": np.log10,
            "sqrt": np.sqrt, "abs": abs,
            "pi": np.pi, "e": np.e,
            "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
            "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan
        }
        
        def safe_function(*args):
            # Preparar el namespace seguro
            namespace = allowed_names.copy()
            
            # Asignar variables según el número de argumentos
            if len(args) == 1:
                namespace["x"] = args[0]
                namespace["t"] = args[0]  # Alias para tiempo
            elif len(args) == 2:
                namespace["t"] = args[0]
                namespace["y"] = args[1]
            
            try:
                # Reemplazar notaciones comunes
                processed_expr = expr.replace('^', '**').replace('sen', 'sin').replace('ln', 'log')
                return eval(processed_expr, {"__builtins__": {}}, namespace)
            except Exception as e:
                logger.warning(f"Error evaluando función '{expr}': {e}")
                return 0
        
        return safe_function
    
    def validate_inputs(self, entries: dict, required_fields: list = None) -> tuple:
        """
        Valida las entradas del usuario.
        Principio de responsabilidad única: validación centralizada.
        
        Returns:
            Tupla (is_valid, values_dict, error_message)
        """
        if required_fields is None:
            required_fields = list(entries.keys())
        
        values = {}
        
        for field_name in required_fields:
            if field_name not in entries:
                return False, {}, f"Campo requerido '{field_name}' no encontrado"
            
            entry = entries[field_name]
            value_str = entry.get().strip()
            
            if not value_str:
                return False, {}, f"El campo '{field_name}' no puede estar vacío"
            
            # Intentar convertir a número
            try:
                if '.' in value_str or 'e' in value_str.lower():
                    values[field_name] = float(value_str)
                else:
                    # Intentar como entero primero
                    values[field_name] = int(value_str)
            except ValueError:
                # Si no es un número, mantener como string
                values[field_name] = value_str
        
        return True, values, ""
    
    def show_error(self, message: str):
        """
        Mostrar mensaje de error en una ventana modal.
        Principio DRY: manejo consistente de errores.
        """
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("500x200")
        error_window.grab_set()
        
        # Centrar la ventana
        error_window.transient(self)
        
        error_label = ctk.CTkLabel(
            error_window,
            text=message,
            wraplength=450,
            font=ctk.CTkFont(size=UI_CONFIG["default_font_size"])
        )
        error_label.pack(pady=20, padx=20)
        
        ok_btn = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy
        )
        ok_btn.pack(pady=10)
    
    def show_success(self, message: str):
        """
        Mostrar mensaje de éxito.
        Principio DRY: feedback consistente al usuario.
        """
        success_window = ctk.CTkToplevel(self)
        success_window.title("Éxito")
        success_window.geometry("400x150")
        success_window.grab_set()
        
        success_label = ctk.CTkLabel(
            success_window,
            text=message,
            wraplength=350,
            font=ctk.CTkFont(size=UI_CONFIG["default_font_size"])
        )
        success_label.pack(pady=20, padx=20)
        
        ok_btn = ctk.CTkButton(
            success_window,
            text="OK",
            command=success_window.destroy
        )
        ok_btn.pack(pady=10)
    
    def create_matplotlib_plot(self, plot_frame: ctk.CTkFrame, 
                              clear_existing: bool = True) -> tuple:
        """
        Crear un gráfico matplotlib embebido.
        Principio DRY: configuración consistente de gráficos.
        
        Returns:
            Tupla (figure, canvas)
        """
        if clear_existing:
            # Limpiar widgets existentes
            for widget in plot_frame.winfo_children():
                widget.destroy()
        
        # Crear figura con configuración consistente
        fig = plt.figure(
            figsize=PLOT_CONFIG["figure_size"],
            dpi=PLOT_CONFIG["dpi"],
            facecolor='#2b2b2b'
        )
        
        # Crear canvas
        canvas = FigureCanvasTkAgg(fig, plot_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        return fig, canvas
    
    def format_result_text(self, title: str, data: dict, 
                          sections: Optional[dict] = None) -> str:
        """
        Formatea texto de resultados de manera consistente.
        Principio DRY: formato estándar en todas las pestañas.
        
        Args:
            title: Título principal
            data: Datos principales a mostrar
            sections: Secciones adicionales {section_name: section_data}
        """
        text = f"{title}\\n"
        text += "=" * len(title) + "\\n\\n"
        
        # Datos principales
        for key, value in data.items():
            if isinstance(value, (int, float)):
                if abs(value) < 1e-3 or abs(value) > 1e6:
                    text += f"{key}: {value:.2e}\\n"
                else:
                    text += f"{key}: {value:.8f}\\n"
            else:
                text += f"{key}: {value}\\n"
        
        # Secciones adicionales
        if sections:
            for section_name, section_data in sections.items():
                text += f"\\n{section_name}:\\n"
                text += "-" * len(section_name) + "\\n"
                
                if isinstance(section_data, dict):
                    for key, value in section_data.items():
                        text += f"{key}: {value}\\n"
                elif isinstance(section_data, (list, tuple)):
                    for item in section_data:
                        text += f"• {item}\\n"
                else:
                    text += f"{section_data}\\n"
        
        return text
    
    def apply_plot_styling(self, ax, title: str = "", 
                          xlabel: str = "", ylabel: str = ""):
        """
        Aplica estilo consistente a los gráficos.
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
