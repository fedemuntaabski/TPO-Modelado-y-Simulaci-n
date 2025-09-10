"""
Aplicación principal del simulador matemático.

Implementa la interfaz principal con sidebar navigation
siguiendo principios SOLID y DRY.
"""

import customtkinter as ctk
import logging
from typing import Dict, Any

from src.ui.tabs.roots_tab import RootsTab
from src.ui.tabs.integration_tab import IntegrationTab
from src.ui.tabs.ode_tab_new import ODETab
from src.ui.tabs.finite_diff_tab import FiniteDiffTab
from src.ui.tabs.newton_cotes_tab import NewtonCotesTab
from src.ui.components.tab_factory import TabFactory, create_placeholder_tab
from src.ui.components.constants import VALIDATION, UI, PLOT, COLORS
from config.settings import configure_matplotlib


logger = logging.getLogger(__name__)


class MathSimulatorApp(ctk.CTk):
    """Aplicación principal del simulador matemático"""

    def __init__(self):
        super().__init__()

        # Configurar matplotlib
        configure_matplotlib()

        # Configuración de la ventana - más grande para Newton-Cotes
        self.title("🧮 Simulador Matemático v4.0 - Modular")
        self.geometry(f"{UI.WINDOW_WIDTH}x{UI.WINDOW_HEIGHT}")
        self.minsize(UI.MIN_WINDOW_WIDTH, UI.MIN_WINDOW_HEIGHT)

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
        self.sidebar.grid_rowconfigure(7, weight=1)

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
            ("monte_carlo", "🎲 Monte Carlo"),
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
            btn.grid(row=i+1, column=0, pady=4, padx=20, sticky="ew")
            self.nav_buttons[key] = btn

        # Información del desarrollador
        dev_label = ctk.CTkLabel(
            self.sidebar,
            text="Simulador Modular \nMetodos Numéricos",
            font=ctk.CTkFont(size=12),
            text_color=["gray60", "gray50"]
        )
        dev_label.grid(row=9, column=0, pady=10, padx=20)

    def create_main_area(self):
        """Crea el área principal para mostrar pestañas"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Inicializar diccionario de pestañas (lazy loading)
        self.tabs = {}
        self._tab_cache = {}  # Cache para pestañas ya creadas

    def _get_tab(self, tab_id: str):
        """Obtener pestaña con lazy loading"""
        if tab_id not in self._tab_cache:
            if tab_id in TabFactory.get_available_tabs():
                # Crear pestaña usando factory
                self._tab_cache[tab_id] = TabFactory.create_tab(tab_id, self.main_frame)
            elif tab_id in ["interpolation", "derivatives"]:
                # Crear placeholders
                if tab_id == "interpolation":
                    self._tab_cache[tab_id] = create_placeholder_tab(
                        self.main_frame, "🔗 Interpolación",
                        "Métodos de interpolación polinomial y splines"
                    )
                else:  # derivatives
                    self._tab_cache[tab_id] = create_placeholder_tab(
                        self.main_frame, "∂ Derivadas Numéricas",
                        "Cálculo numérico de derivadas de orden superior"
                    )

        return self._tab_cache.get(tab_id)

    def show_tab(self, tab_id):
        """Mostrar pestaña específica con lazy loading"""
        # Ocultar todas las pestañas visibles
        for tab in self.tabs.values():
            if tab is not None:
                tab.grid_remove()

        # Limpiar diccionario de pestañas visibles
        self.tabs.clear()

        # Obtener y mostrar la pestaña seleccionada
        selected_tab = self._get_tab(tab_id)
        if selected_tab is not None:
            self.tabs[tab_id] = selected_tab
            selected_tab.grid(row=0, column=0, sticky="nsew")

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
