"""
Pestaña unificada para Diferencias Finitas
Combina derivadas numéricas, interpolación y análisis avanzado
Optimizada con IA para mejor distribución y precisión
"""

import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt

from numerics.advanced import InterpolationMethods, AdvancedNumericalMethods, ErrorAnalysis
from numerics.methods import MathParser

from .finite_differences_derivatives import DerivativesTab
from .finite_differences_interpolation import InterpolationTab
from .finite_differences_analysis import AnalysisTab

class FiniteDifferencesTab(QWidget):
    """
    Pestaña unificada para Diferencias Finitas
    Combina derivadas numéricas, interpolación y análisis avanzado
    Optimizada con IA para mejor distribución y precisión
    """

    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()

    def init_ui(self):
        # Layout principal con pestañas para diferentes funcionalidades
        main_layout = QVBoxLayout()

        # Crear widget de pestañas
        self.tab_widget = QTabWidget()

        # Pestaña de Derivadas
        self.derivatives_tab = DerivativesTab(self.keyboard, self.plot_widget)
        self.tab_widget.addTab(self.derivatives_tab, "🔢 Derivadas")

        # Pestaña de Interpolación
        self.interpolation_tab = InterpolationTab(self.keyboard, self.plot_widget)
        self.tab_widget.addTab(self.interpolation_tab, "📊 Interpolación")

        # Pestaña de Análisis Avanzado
        self.analysis_tab = AnalysisTab(self.keyboard, self.plot_widget)
        self.tab_widget.addTab(self.analysis_tab, "🔬 Análisis Avanzado")

        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.plot_widget)

        self.setLayout(main_layout)


