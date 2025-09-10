"""
Pestaña de créditos del simulador matemático.

Muestra los nombres de los integrantes del equipo de desarrollo.
"""

import customtkinter as ctk

from src.ui.components.base_tab import BaseTab


class CreditsTab(BaseTab):
    """
    Pestaña que muestra los créditos del proyecto.
    """

    def __init__(self, parent):
        super().__init__(parent, "Créditos")

    def create_content(self):
        """
        Crear el contenido de la pestaña de créditos.
        """
        # Frame para los créditos
        credits_frame = ctk.CTkFrame(self.content_frame)
        credits_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        credits_frame.grid_columnconfigure(0, weight=1)

        # Título de créditos
        title_label = ctk.CTkLabel(
            credits_frame,
            text="👥 Integrantes del Equipo",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 30), sticky="ew")

        # Lista de integrantes (placeholders - reemplazar con nombres reales)
        team_members = [
            "Federico Muntaabski",
            "Nicolas Llousas",
            "Integrante 3",
            "Integrante 4"
        ]

        for i, member in enumerate(team_members):
            member_label = ctk.CTkLabel(
                credits_frame,
                text=f"• {member}",
                font=ctk.CTkFont(size=18)
            )
            member_label.grid(row=i+1, column=0, pady=5, sticky="w")

        # Espacio adicional
        spacer = ctk.CTkLabel(credits_frame, text="")
        spacer.grid(row=len(team_members)+1, column=0, pady=20)

        # Información adicional
        info_label = ctk.CTkLabel(
            credits_frame,
            text="Proyecto: Simulador Matemático \n"
                 "Materia: Modelado y Simulación\n"
                 "Año: 2025\n",
            font=ctk.CTkFont(size=16),
            text_color=["gray60", "gray50"]
        )
        info_label.grid(row=len(team_members)+2, column=0, pady=(10, 20), sticky="ew")
