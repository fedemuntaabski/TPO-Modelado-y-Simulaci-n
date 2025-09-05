"""
Derivatives tab for Finite Differences
"""

import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QMessageBox
)
from PyQt6.QtCore import Qt

from numerics.methods import MathParser
from core.finite_differences import FiniteDifferences

class DerivativesTab(QWidget):
    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Panel izquierdo: Controles
        left_panel = QGroupBox("Derivadas Numéricas")
        left_layout = QVBoxLayout()

        # Función
        self.fd_function_input = QLineEdit()
        self.fd_function_input.setPlaceholderText("Ej: x**3 + 2*x**2 - x + 1")
        self.fd_function_input.focusInEvent = lambda e: self.keyboard.set_target(self.fd_function_input)
        func_label = QLabel("Función f(x):")
        func_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        left_layout.addWidget(func_label)
        left_layout.addWidget(self.fd_function_input)

        # Punto de evaluación
        self.fd_x_point = QDoubleSpinBox()
        self.fd_x_point.setRange(-100, 100)
        self.fd_x_point.setValue(1)
        self.fd_x_point.setDecimals(4)
        x_label = QLabel("Punto x:")
        x_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        left_layout.addWidget(x_label)
        left_layout.addWidget(self.fd_x_point)

        # Paso h
        self.fd_h_value = QDoubleSpinBox()
        self.fd_h_value.setRange(1e-10, 1)
        self.fd_h_value.setValue(1e-5)
        self.fd_h_value.setDecimals(10)
        h_label = QLabel("Paso h:")
        h_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        left_layout.addWidget(h_label)
        left_layout.addWidget(self.fd_h_value)

        # Orden de derivada
        self.fd_order = QSpinBox()
        self.fd_order.setRange(1, 4)
        self.fd_order.setValue(1)
        self.fd_order.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)  # Quitar botones
        order_label = QLabel("Orden:")
        order_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        left_layout.addWidget(order_label)
        left_layout.addWidget(self.fd_order)

        # Método
        self.fd_method = QComboBox()
        self.fd_method.addItems(["Central", "Hacia adelante", "Hacia atrás", "Adaptativo"])
        method_label = QLabel("Método:")
        method_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        left_layout.addWidget(method_label)
        left_layout.addWidget(self.fd_method)

        # Botones
        calc_btn = QPushButton("Calcular")
        calc_btn.setStyleSheet("background-color: #00cec9; color: white; font-weight: bold; padding: 8px;")
        calc_btn.clicked.connect(self.calculate_fd_derivative)
        left_layout.addWidget(calc_btn)

        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(300)

        # Panel derecho: Resultados
        right_panel = QGroupBox("Resultados")
        right_layout = QVBoxLayout()

        self.fd_results_text = QTextEdit()
        self.fd_results_text.setMaximumHeight(300)
        right_layout.addWidget(self.fd_results_text)

        right_panel.setLayout(right_layout)

        layout.addWidget(left_panel)
        layout.addWidget(right_panel)

        self.setLayout(layout)

    def calculate_fd_derivative(self):
        """Calcula derivada usando el método seleccionado"""
        try:
            function_str = self.fd_function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese una función")
                return

            f = MathParser.parse_function(function_str)
            x = self.fd_x_point.value()
            h = self.fd_h_value.value()
            order = self.fd_order.value()
            method = self.fd_method.currentText()

            if method == "Adaptativo":
                h_opt, result = FiniteDifferences.adaptive_step_size(f, x)
                method_info = f"Adaptativo (h óptimo: {h_opt:.2e})"
            elif method == "Central":
                if order == 1:
                    result = FiniteDifferences.central_difference(f, x, h)
                else:
                    derivatives = FiniteDifferences.derivative_table(f, x, order, h)
                    result = derivatives[order]
                method_info = f"Central (h: {h:.2e})"
            elif method == "Hacia adelante":
                result = FiniteDifferences.forward_difference(f, x, h)
                method_info = f"Hacia adelante (h: {h:.2e})"
            else:  # Hacia atrás
                result = FiniteDifferences.backward_difference(f, x, h)
                method_info = f"Hacia atrás (h: {h:.2e})"

            self.fd_results_text.setText(f"""
DERIVADA NUMÉRICA
Función: f(x) = {function_str}
Punto: x = {x}
Método: {method_info}
Orden: {order}

Resultado: f{order}(x) ≈ {result:.8f}
            """.strip())

            # Graficar
            self.plot_fd_function(f, function_str, x)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error calculando derivada: {str(e)}")

    def plot_fd_function(self, f, function_str, x):
        """Grafica función y punto de evaluación"""
        x_range = np.linspace(x - 2, x + 2, 1000)
        y_values = [f(xi) for xi in x_range]

        self.plot_widget.figure.clear()
        ax = self.plot_widget.figure.add_subplot(111)
        ax.plot(x_range, y_values, 'b-', label=f'f(x) = {function_str}', linewidth=2)
        ax.plot(x, f(x), 'ro', markersize=8, label='Punto de evaluación')
        ax.set_title('Función y Punto de Evaluación', fontsize=14, fontweight='bold')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)
        ax.legend()
        self.plot_widget.canvas.draw()
