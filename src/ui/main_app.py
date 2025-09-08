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
from src.ui.tabs.ode_tab import ODETab
from src.ui.tabs.finite_diff_tab import FiniteDiffTab
from src.ui.tabs.newton_cotes_tab import NewtonCotesTab
from src.ui.components.constants import VALIDATION, UI, PLOT, COLORS


logger = logging.getLogger(__name__)


class MathSimulatorApp(ctk.CTk):
    """Aplicación principal del simulador matemático"""

    def __init__(self):
        super().__init__()

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
        self.tabs["newton_cotes"] = NewtonCotesTab(self.main_frame)

        # Pestañas placeholder para las demás
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
