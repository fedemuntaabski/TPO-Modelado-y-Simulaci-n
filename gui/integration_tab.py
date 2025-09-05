"""
Pestaña para integración numérica
Implementa la clase IntegrationTab para el simulador matemático
"""

import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt

from numerics.methods import NumericalMethods, MathParser

class IntegrationTab(QWidget):
    """
    Pestaña para integración numérica
    """

    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Panel de entrada
        input_panel = QGroupBox("Integración Numérica")
        input_layout = QVBoxLayout()

        # Función
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: x**2, sin(x), exp(-x**2)")
        self.function_input.focusInEvent = lambda e: self.keyboard.set_target(self.function_input)
        input_layout.addWidget(QLabel("Función f(x):"))
        input_layout.addWidget(self.function_input)

        # Límites de integración
        limits_layout = QHBoxLayout()

        self.a_input = QDoubleSpinBox()
        self.a_input.setRange(-100, 100)
        self.a_input.setValue(0)
        limits_layout.addWidget(QLabel("a:"))
        limits_layout.addWidget(self.a_input)

        self.b_input = QDoubleSpinBox()
        self.b_input.setRange(-100, 100)
        self.b_input.setValue(1)
        limits_layout.addWidget(QLabel("b:"))
        limits_layout.addWidget(self.b_input)

        input_layout.addLayout(limits_layout)

        # Número de subdivisiones
        self.n_input = QSpinBox()
        self.n_input.setRange(2, 1000)
        self.n_input.setValue(100)
        input_layout.addWidget(QLabel("Subdivisiones (n):"))
        input_layout.addWidget(self.n_input)

        # Método de integración
        from PyQt6.QtWidgets import QComboBox
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Regla del Rectángulo",
            "Rectángulo Medio", 
            "Regla del Trapecio",
            "Simpson 1/3",
            "Simpson 3/8"
        ])
        self.method_combo.setCurrentText("Simpson 1/3")
        input_layout.addWidget(QLabel("Método:"))
        input_layout.addWidget(self.method_combo)

        # Botón calcular
        calc_button = QPushButton("Calcular Integral")
        from gui.themes import DarkTheme
        calc_button.setStyleSheet(DarkTheme.get_button_style("info") + "padding: 12px;")
        calc_button.clicked.connect(self.calculate_integral)
        input_layout.addWidget(calc_button)

        # Área de resultados
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        input_layout.addWidget(QLabel("Resultados:"))
        input_layout.addWidget(self.results_text)

        input_panel.setLayout(input_layout)
        input_panel.setMaximumWidth(350)

        layout.addWidget(input_panel)
        layout.addWidget(self.plot_widget)

        self.setLayout(layout)

    def calculate_integral(self):
        """Calcula la integral numérica"""
        try:
            function_str = self.function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese la función f(x)")
                return

            f = MathParser.parse_function(function_str)
            a = self.a_input.value()
            b = self.b_input.value()
            n = self.n_input.value()

            # Mapear selección del combo a método
            method_map = {
                "Regla del Rectángulo": "rectangle",
                "Rectángulo Medio": "midpoint",
                "Regla del Trapecio": "trapezoid", 
                "Simpson 1/3": "simpson_13",
                "Simpson 3/8": "simpson_38"
            }
            selected_method = self.method_combo.currentText()
            method = method_map[selected_method]

            if a >= b:
                QMessageBox.warning(self, "Error", "a debe ser menor que b")
                return

            # Calcular integral
            integral_value = NumericalMethods.newton_cotes_integration(f, a, b, n, method)

            # Graficar la función y el área bajo la curva
            x = np.linspace(a, b, 200)
            y = [f(xi) for xi in x]

            self.plot_widget.figure.clear()
            ax = self.plot_widget.figure.add_subplot(111)
            ax.plot(x, y, 'b-', linewidth=2, label=f'f(x) = {function_str}')
            ax.fill_between(x, y, alpha=0.3, label=f'Área = {integral_value:.6f}')
            ax.set_title(f'Integración Numérica: ∫ {function_str} dx')
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.grid(True, alpha=0.3)
            ax.legend()
            self.plot_widget.canvas.draw()

            # Mostrar resultados
            results = f"""
Método: {selected_method}
Función: f(x) = {function_str}
Límites: [{a}, {b}]
Subdivisiones: {n}
Integral ≈ {integral_value:.8f}
            """.strip()

            self.results_text.setText(results)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error calculando integral: {str(e)}")
