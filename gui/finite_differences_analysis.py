"""
Analysis tab for Finite Differences
"""

import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QDoubleSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt

from numerics.methods import MathParser
from core.finite_differences import FiniteDifferences

class AnalysisTab(QWidget):
    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Panel izquierdo: Controles
        left_panel = QGroupBox("Análisis Avanzado")
        left_layout = QVBoxLayout()

        # Función para análisis
        self.analysis_function = QLineEdit()
        self.analysis_function.setPlaceholderText("Ej: sin(x), exp(x), x**2")
        self.analysis_function.focusInEvent = lambda e: self.keyboard.set_target(self.analysis_function)
        left_layout.addWidget(QLabel("Función f(x):"))
        left_layout.addWidget(self.analysis_function)

        # Punto de análisis
        self.analysis_point = QDoubleSpinBox()
        self.analysis_point.setRange(-100, 100)
        self.analysis_point.setValue(1)
        self.analysis_point.setDecimals(4)
        left_layout.addWidget(QLabel("Punto x:"))
        left_layout.addWidget(self.analysis_point)

        # Botones de análisis
        stability_btn = QPushButton("Análisis de Estabilidad")
        stability_btn.setStyleSheet("background-color: #e84393; color: white; font-weight: bold; padding: 8px;")
        stability_btn.clicked.connect(self.fd_stability_analysis)
        left_layout.addWidget(stability_btn)

        convergence_btn = QPushButton("Convergencia Detallada")
        convergence_btn.setStyleSheet("background-color: #6c5ce7; color: white; font-weight: bold; padding: 8px;")
        convergence_btn.clicked.connect(self.fd_detailed_convergence)
        left_layout.addWidget(convergence_btn)

        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(300)

        # Panel derecho: Resultados
        right_panel = QGroupBox("Análisis")
        right_layout = QVBoxLayout()

        self.analysis_results = QTextEdit()
        self.analysis_results.setMaximumHeight(300)
        right_layout.addWidget(self.analysis_results)

        right_panel.setLayout(right_layout)

        layout.addWidget(left_panel)
        layout.addWidget(right_panel)

        self.setLayout(layout)

    def fd_stability_analysis(self):
        """Análisis de estabilidad"""
        try:
            function_str = self.analysis_function.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese una función")
                return

            f = MathParser.parse_function(function_str)
            x = self.analysis_point.value()

            analysis = FiniteDifferences.stability_analysis(f, x)

            result = f"""
ANÁLISIS DE ESTABILIDAD
Función: f(x) = {function_str}
Punto: x = {x}

RANGO ESTABLE: h ∈ [{analysis['stable_range']:.2e}, 1e-2] (aprox.)
Números de condición calculados para diferentes h
            """

            self.analysis_results.setText(result)

            # Graficar estabilidad
            self.plot_fd_stability(analysis)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en análisis: {str(e)}")

    def fd_detailed_convergence(self):
        """Análisis detallado de convergencia"""
        try:
            function_str = self.analysis_function.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese una función")
                return

            f = MathParser.parse_function(function_str)
            x = self.analysis_point.value()

            analysis = FiniteDifferences.convergence_analysis(f, x)

            result = f"""
ANÁLISIS DETALLADO DE CONVERGENCIA
Función: f(x) = {function_str}
Punto: x = {x}

MÉTODO ÓPTIMO: {analysis['optimal_method']}
PASO ÓPTIMO: h = {analysis['optimal_h']:.2e}
ERROR MÍNIMO: {min(analysis['errors_central']):.2e}
            """

            self.analysis_results.setText(result)

            # Graficar convergencia detallada
            self.plot_fd_convergence(analysis)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en análisis: {str(e)}")

    def plot_fd_stability(self, analysis):
        """Grafica análisis de estabilidad"""
        self.plot_widget.figure.clear()
        ax = self.plot_widget.figure.add_subplot(111)
        ax.semilogx(analysis['h_values'], analysis['condition_numbers'], 'r-o', linewidth=2)
        ax.set_title('Análisis de Estabilidad Numérica', fontsize=14, fontweight='bold')
        ax.set_xlabel('Paso h')
        ax.set_ylabel('Número de condición')
        ax.grid(True, alpha=0.3)
        self.plot_widget.canvas.draw()

    def plot_fd_convergence(self, analysis):
        """Grafica convergencia detallada"""
        self.plot_widget.figure.clear()
        ax = self.plot_widget.figure.add_subplot(111)

        if analysis['errors_central']:
            ax.loglog(analysis['h_values'], analysis['errors_central'], 'b-o',
                     label='Diferencias centrales', linewidth=2)

        ax.set_title('Convergencia de Métodos', fontsize=14, fontweight='bold')
        ax.set_xlabel('Paso h')
        ax.set_ylabel('Error absoluto')
        ax.grid(True, alpha=0.3)
        ax.legend()
        self.plot_widget.canvas.draw()
