"""
Pestaña para interpolación de Lagrange y análisis de diferencias finitas
"""

import numpy as np
from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QTableWidget, QTableWidgetItem, QMessageBox, QSplitter, QTabWidget
)
from PyQt6.QtCore import Qt

from numerics.interpolation_methods import InterpolationMethods
from numerics.advanced_numerical_methods import AdvancedNumericalMethods
from numerics.error_analysis import ErrorAnalysis
from numerics.methods import MathParser
from .interpolation_ui import InterpolationUI
from .interpolation_logic import InterpolationLogic


class InterpolationTab(QWidget):
    """
    Pestaña para interpolación de Lagrange y análisis de diferencias finitas
    """

    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget

        # Crear instancia de UI
        self.ui = InterpolationUI(plot_widget)
        layout, data_table, eval_point, results_text, interpolate_btn, diff_btn = self.ui.create_ui()

        # Crear instancia de lógica
        self.logic = InterpolationLogic(data_table, eval_point, results_text, plot_widget)

        # Conectar botones a métodos de lógica
        interpolate_btn.clicked.connect(self.logic.interpolate_lagrange)
        diff_btn.clicked.connect(self.logic.calculate_differences)

        self.setLayout(layout)
