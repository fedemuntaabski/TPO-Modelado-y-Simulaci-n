"""
Componente base para todas las pestañas de la interfaz.

Implementa el patrón Template Method siguiendo principios SOLID.
Proporciona funcionalidad común reutilizable (DRY).
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import Callable, Optional, Tuple, Dict, Any, Union
import logging

from config.settings import UI_CONFIG, PLOT_CONFIG
from .error_handler import handle_error, ErrorSeverity
from src.core.root_finding import create_function_from_string

logger = logging.getLogger(__name__)


class BaseTab(ctk.CTkFrame):
    """
    Clase base para todas las pestañas.
    Implementa el patrón Template Method (SOLID - Open/Closed Principle).
    """
    
    def __init__(self, parent, title: str):
        super().__init__(parent)
        self.title = title
        self._plot_cache = {}  # Cache para gráficos
        self._last_plot_data = None  # Datos del último gráfico
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
        plot_frame = ctk.CTkFrame(results_frame, height=300)  # Altura mínima para el gráfico
        plot_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        results_frame.grid_rowconfigure(1, weight=1)  # Permitir expansión vertical
        
        return results_frame, text_widget, plot_frame
    
    def validate_inputs(self, entries: Dict[str, ctk.CTkEntry], 
                       required_fields: Optional[list] = None) -> Tuple[bool, Dict[str, Any], str]:
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
    
    def show_error(self, message: str, severity: ErrorSeverity = ErrorSeverity.ERROR):
        """
        Mostrar mensaje de error usando el gestor centralizado.
        Principio DRY: manejo consistente de errores.
        """
        handle_error(
            Exception(message),
            context=self.title,
            severity=severity,
            show_dialog=True
        )
    
    def show_success(self, message: str):
        """
        Mostrar mensaje de éxito usando el gestor centralizado.
        Principio DRY: feedback consistente al usuario.
        """
        from .error_handler import handle_success
        handle_success("CALCULATION_SUCCESS", custom_message=message, show_dialog=True)
    
    def create_matplotlib_plot(self, plot_frame: ctk.CTkFrame, 
                              clear_existing: bool = True,
                              cache_key: Optional[str] = None) -> Tuple[plt.Figure, FigureCanvasTkAgg]:
        """
        Crear un gráfico matplotlib embebido con soporte para cache.
        Principio DRY: configuración consistente de gráficos.
        
        Args:
            plot_frame: Frame donde crear el gráfico
            clear_existing: Si limpiar widgets existentes
            cache_key: Clave para cache (opcional)
            
        Returns:
            Tupla (figure, canvas)
        """
        # Intentar obtener del cache si se proporciona una clave
        if cache_key:
            cached_result = self.get_cached_plot(cache_key, plot_frame)
            if cached_result:
                return cached_result
        
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
        
        # Almacenar en cache si se proporciona una clave
        if cache_key:
            self.cache_plot(cache_key, fig, canvas)
        
        return fig, canvas
    
    def get_cached_plot(self, cache_key: str, plot_frame: ctk.CTkFrame) -> Optional[Tuple[plt.Figure, FigureCanvasTkAgg]]:
        """
        Obtener gráfico del cache si existe y es válido.
        
        Args:
            cache_key: Clave única para identificar el gráfico
            plot_frame: Frame donde mostrar el gráfico
            
        Returns:
            Tupla (figure, canvas) o None si no está en cache
        """
        if cache_key in self._plot_cache:
            cached_fig, cached_canvas = self._plot_cache[cache_key]
            # Verificar si el canvas aún es válido
            try:
                cached_canvas.get_tk_widget().winfo_exists()
                return cached_fig, cached_canvas
            except:
                # Canvas inválido, remover del cache
                del self._plot_cache[cache_key]
        
        return None
    
    def cache_plot(self, cache_key: str, fig: plt.Figure, canvas: FigureCanvasTkAgg) -> None:
        """
        Almacenar gráfico en el cache.
        
        Args:
            cache_key: Clave única para el gráfico
            fig: Figura matplotlib
            canvas: Canvas del gráfico
        """
        # Limitar el tamaño del cache (máximo 5 gráficos por pestaña)
        if len(self._plot_cache) >= 5:
            # Remover el primer elemento (FIFO)
            first_key = next(iter(self._plot_cache))
            del self._plot_cache[first_key]
        
        self._plot_cache[cache_key] = (fig, canvas)
    
    def clear_plot_cache(self):
        """Limpiar el cache de gráficos"""
        for fig, canvas in self._plot_cache.values():
            try:
                plt.close(fig)
            except:
                pass
        self._plot_cache.clear()
    
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
