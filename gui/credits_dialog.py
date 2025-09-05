"""
Información del Equipo y Créditos - Diálogo Principal
Simulador Matemático Avanzado v3.0

Equipo TPO Modelado y Simulación - 2025
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .credits_tabs import CreditsTabs


class CreditsDialog(QDialog):
    """
    Diálogo de créditos e información del equipo
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Créditos - Simulador Matemático Avanzado v3.0")
        self.setFixedSize(800, 600)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del diálogo de créditos"""
        layout = QVBoxLayout()
        
        # Título principal
        title_label = QLabel("🧮 SIMULADOR MATEMÁTICO AVANZADO v3.0")
        title_font = QFont("Arial", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #3498db; margin: 20px;")
        layout.addWidget(title_label)
        
        # Pestañas de información
        tab_widget = QTabWidget()
        
        # Pestaña del equipo
        team_tab = CreditsTabs.create_team_tab()
        tab_widget.addTab(team_tab, "👥 Equipo")
        
        # Pestaña de tecnologías
        tech_tab = CreditsTabs.create_tech_tab()
        tab_widget.addTab(tech_tab, "⚙️ Tecnologías")
        
        # Pestaña de características
        features_tab = CreditsTabs.create_features_tab()
        tab_widget.addTab(features_tab, "✨ Características")
        
        # Pestaña de agradecimientos
        thanks_tab = CreditsTabs.create_thanks_tab()
        tab_widget.addTab(thanks_tab, "🙏 Agradecimientos")
        
        layout.addWidget(tab_widget)
        
        # Botón cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 30px;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
