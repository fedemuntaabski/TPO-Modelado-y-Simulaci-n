"""
Factory para creación de pestañas de la interfaz.

Implementa el patrón Factory Method para centralizar la creación de pestañas
y mejorar la mantenibilidad siguiendo principios SOLID.
"""

from typing import Dict, Type, Any
import customtkinter as ctk

from src.ui.tabs.roots_tab import RootsTab
from src.ui.tabs.integration_tab import IntegrationTab
from src.ui.tabs.ode_tab_new import ODETab
from src.ui.tabs.finite_diff_tab import FiniteDiffTab
from src.ui.tabs.newton_cotes_tab import NewtonCotesTab
from src.ui.tabs.monte_carlo_tab import MonteCarloTab
from src.ui.tabs.monte_carlo_3d_tab import MonteCarlo3DTab
from src.ui.tabs.credits_tab import CreditsTab


class TabFactory:
    """
    Factory para crear instancias de pestañas.
    Principio de responsabilidad única: solo crea pestañas.
    """

    # Registro de pestañas disponibles
    _tab_registry: Dict[str, Type] = {
        "roots": RootsTab,
        "integration": IntegrationTab,
        "ode": ODETab,
        "finite_diff": FiniteDiffTab,
        "newton_cotes": NewtonCotesTab,
        "monte_carlo": MonteCarloTab,
        "monte_carlo_3d": MonteCarlo3DTab,
        "credits": CreditsTab,
    }

    @classmethod
    def create_tab(cls, tab_type: str, parent: ctk.CTkFrame, **kwargs) -> Any:
        """
        Crea una instancia de pestaña según el tipo especificado.

        Args:
            tab_type: Tipo de pestaña a crear
            parent: Frame padre donde se creará la pestaña
            **kwargs: Argumentos adicionales para el constructor

        Returns:
            Instancia de la pestaña creada

        Raises:
            ValueError: Si el tipo de pestaña no está registrado
        """
        if tab_type not in cls._tab_registry:
            raise ValueError(f"Tipo de pestaña no registrado: {tab_type}")

        tab_class = cls._tab_registry[tab_type]
        return tab_class(parent, **kwargs)

    @classmethod
    def get_available_tabs(cls) -> list:
        """
        Retorna la lista de tipos de pestañas disponibles.

        Returns:
            Lista de strings con los tipos de pestañas
        """
        return list(cls._tab_registry.keys())

    @classmethod
    def register_tab(cls, tab_type: str, tab_class: Type) -> None:
        """
        Registra una nueva pestaña en el factory.

        Args:
            tab_type: Identificador único de la pestaña
            tab_class: Clase de la pestaña a registrar
        """
        cls._tab_registry[tab_type] = tab_class

    @classmethod
    def unregister_tab(cls, tab_type: str) -> None:
        """
        Remueve una pestaña del registro del factory.

        Args:
            tab_type: Tipo de pestaña a remover
        """
        if tab_type in cls._tab_registry:
            del cls._tab_registry[tab_type]


def create_placeholder_tab(parent: ctk.CTkFrame, title: str, description: str) -> ctk.CTkFrame:
    """
    Crea una pestaña placeholder para módulos no implementados.
    Función utilitaria para mantener compatibilidad.

    Args:
        parent: Frame padre
        title: Título de la pestaña
        description: Descripción del módulo

    Returns:
        Frame configurado como placeholder
    """
    placeholder = ctk.CTkFrame(parent)
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
