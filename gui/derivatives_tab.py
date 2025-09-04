"""
Pestaña para cálculo de derivadas numéricas y análisis de convergencia
"""

import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt

from numerics.advanced import InterpolationMethods, AdvancedNumericalMethods, ErrorAnalysis
from numerics.methods import MathParser

class DerivativesTab(QWidget):
    """
    Pestaña para cálculo de derivadas numéricas y análisis de convergencia
    """

    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Panel de entrada
        input_panel = QGroupBox("Derivadas Numéricas")
        input_layout = QVBoxLayout()

        # Función
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: x**3 + 2*x**2 - x + 1")
        self.function_input.focusInEvent = lambda e: self.keyboard.set_target(self.function_input)
        input_layout.addWidget(QLabel("Función f(x):"))
        input_layout.addWidget(self.function_input)

        # Punto de evaluación
        self.x_point = QDoubleSpinBox()
        self.x_point.setRange(-100, 100)
        self.x_point.setValue(1)
        self.x_point.setDecimals(4)
        input_layout.addWidget(QLabel("Punto de evaluación:"))
        input_layout.addWidget(self.x_point)

        # Paso h inicial
        self.h_initial = QDoubleSpinBox()
        self.h_initial.setRange(1e-10, 1)
        self.h_initial.setValue(0.1)
        self.h_initial.setDecimals(10)
        input_layout.addWidget(QLabel("Paso inicial h:"))
        input_layout.addWidget(self.h_initial)

        # Orden de derivada
        self.derivative_order = QSpinBox()
        self.derivative_order.setRange(1, 4)
        self.derivative_order.setValue(1)
        input_layout.addWidget(QLabel("Orden de derivada:"))
        input_layout.addWidget(self.derivative_order)

        # Función exacta de derivada (opcional)
        self.exact_derivative = QLineEdit()
        self.exact_derivative.setPlaceholderText("Opcional: derivada exacta para comparar")
        self.exact_derivative.focusInEvent = lambda e: self.keyboard.set_target(self.exact_derivative)
        input_layout.addWidget(QLabel("Derivada exacta (opcional):"))
        input_layout.addWidget(self.exact_derivative)

        # Botones
        calc_btn = QPushButton("Calcular Derivada")
        calc_btn.setStyleSheet("background-color: #00cec9; color: white; font-weight: bold; padding: 10px;")
        calc_btn.clicked.connect(self.calculate_derivative)
        input_layout.addWidget(calc_btn)

        convergence_btn = QPushButton("Análisis de Convergencia")
        convergence_btn.setStyleSheet("background-color: #e84393; color: white; font-weight: bold; padding: 10px;")
        convergence_btn.clicked.connect(self.convergence_analysis)
        input_layout.addWidget(convergence_btn)

        richardson_btn = QPushButton("Extrapolación de Richardson")
        richardson_btn.setStyleSheet("background-color: #fdcb6e; color: black; font-weight: bold; padding: 10px;")
        richardson_btn.clicked.connect(self.richardson_extrapolation)
        input_layout.addWidget(richardson_btn)

        # Resultados
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(250)
        input_layout.addWidget(QLabel("Resultados:"))
        input_layout.addWidget(self.results_text)

        input_panel.setLayout(input_layout)
        input_panel.setMaximumWidth(400)

        layout.addWidget(input_panel)
        layout.addWidget(self.plot_widget)

        self.setLayout(layout)

    def calculate_derivative(self):
        """Calcula la derivada numérica"""
        try:
            function_str = self.function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese una función")
                return

            f = MathParser.parse_function(function_str)
            x = self.x_point.value()
            h = self.h_initial.value()
            order = self.derivative_order.value()

            # Calcular derivada usando diferencias finitas centrales
            from numerics.advanced import InterpolationMethods
            derivatives = InterpolationMethods.central_finite_differences_derivative_table(
                f, x, [order], h
            )

            result = derivatives[order]

            # Comparar con derivada exacta si se proporciona
            exact_str = self.exact_derivative.text().strip()
            error_info = ""

            if exact_str:
                try:
                    exact_f = MathParser.parse_function(exact_str)
                    exact_value = exact_f(x)
                    abs_error = ErrorAnalysis.absolute_error(exact_value, result)
                    rel_error = ErrorAnalysis.relative_error(exact_value, result)

                    error_info = f"""
Comparación con valor exacto:
Valor exacto: {exact_value:.10f}
Error absoluto: {abs_error:.2e}
Error relativo: {rel_error:.2e}
                    """.strip()
                except:
                    error_info = "Error evaluando la derivada exacta"

            # Mostrar resultados
            results = f"""
Derivada Numérica - Diferencias Finitas Centrales
================================================
Función: f(x) = {function_str}
Punto: x = {x}
Paso: h = {h}
Orden: {order}

f^({order})(x) ≈ {result:.10f}

{error_info}
            """.strip()

            self.results_text.setText(results)

            # Graficar la función y marcar el punto
            x_range = np.linspace(x - 2, x + 2, 200)
            try:
                y_range = [f(xi) for xi in x_range]

                self.plot_widget.figure.clear()
                ax = self.plot_widget.figure.add_subplot(111)
                ax.plot(x_range, y_range, 'b-', linewidth=2, label=f'f(x) = {function_str}')
                ax.plot(x, f(x), 'ro', markersize=10, label=f'x = {x}')
                ax.set_xlabel('x')
                ax.set_ylabel('f(x)')
                ax.set_title(f'Función y punto de evaluación de la derivada')
                ax.grid(True, alpha=0.3)
                ax.legend()
                self.plot_widget.canvas.draw()
            except:
                pass

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error calculando derivada: {str(e)}")

    def convergence_analysis(self):
        """Analiza la convergencia de la aproximación de la derivada"""
        try:
            function_str = self.function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese una función")
                return

            f = MathParser.parse_function(function_str)
            x = self.x_point.value()
            h_initial = self.h_initial.value()
            order = self.derivative_order.value()

            # Generar secuencia de pasos h
            h_values = [h_initial / (2**i) for i in range(10)]
            derivatives = []
            errors = []

            # Calcular derivadas para diferentes h
            for h in h_values:
                from numerics.advanced import InterpolationMethods
                deriv_dict = InterpolationMethods.central_finite_differences_derivative_table(
                    f, x, [order], h
                )
                derivatives.append(deriv_dict[order])

            # Si hay derivada exacta, calcular errores
            exact_str = self.exact_derivative.text().strip()
            if exact_str:
                try:
                    exact_f = MathParser.parse_function(exact_str)
                    exact_value = exact_f(x)

                    for deriv in derivatives:
                        errors.append(abs(exact_value - deriv))

                    # Estimar orden de convergencia
                    if len(errors) > 2:
                        conv_order = ErrorAnalysis.convergence_order(errors[:5], h_values[:5])
                    else:
                        conv_order = 0

                    # Graficar convergencia
                    self.plot_widget.figure.clear()
                    ax = self.plot_widget.figure.add_subplot(111)
                    ax.loglog(h_values, errors, 'bo-', linewidth=2, markersize=6)
                    ax.set_xlabel('Paso h')
                    ax.set_ylabel('Error absoluto')
                    ax.set_title('Convergencia de Diferencias Finitas')
                    ax.grid(True, alpha=0.3)
                    self.plot_widget.canvas.draw()

                    # Mostrar tabla de convergencia
                    results = f"""
Análisis de Convergencia
========================
Función: f(x) = {function_str}
Punto: x = {x}
Orden de derivada: {order}
Orden de convergencia estimado: {conv_order:.2f}

{'h':>12} {'Derivada':>15} {'Error':>12}
{'-'*40}
"""
                    for h, deriv, error in zip(h_values, derivatives, errors):
                        results += f"{h:>12.2e} {deriv:>15.8f} {error:>12.2e}\n"

                    self.results_text.setText(results)

                except:
                    QMessageBox.warning(self, "Error", "Error evaluando la derivada exacta")
            else:
                # Sin derivada exacta, solo mostrar valores
                results = f"""
Análisis sin derivada exacta
============================
Función: f(x) = {function_str}
Punto: x = {x}
Orden de derivada: {order}

{'h':>12} {'Derivada':>15}
{'-'*28}
"""
                for h, deriv in zip(h_values, derivatives):
                    results += f"{h:>12.2e} {deriv:>15.8f}\n"

                self.results_text.setText(results)

                # Graficar solo las derivadas
                self.plot_widget.figure.clear()
                ax = self.plot_widget.figure.add_subplot(111)
                ax.semilogx(h_values, derivatives, 'bo-', linewidth=2, markersize=6)
                ax.set_xlabel('Paso h')
                ax.set_ylabel('Derivada aproximada')
                ax.set_title('Aproximaciones de la derivada vs h')
                ax.grid(True, alpha=0.3)
                self.plot_widget.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en análisis de convergencia: {str(e)}")

    def richardson_extrapolation(self):
        """Aplica extrapolación de Richardson"""
        try:
            function_str = self.function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese una función")
                return

            f = MathParser.parse_function(function_str)
            x = self.x_point.value()
            h_initial = self.h_initial.value()

            # Generar pasos h para Richardson
            h_values = [h_initial / (2**i) for i in range(5)]

            # Aplicar extrapolación de Richardson
            from numerics.advanced import AdvancedNumericalMethods
            best_approx, R_table = AdvancedNumericalMethods.richardson_extrapolation(
                f, x, h_values
            )

            # Mostrar tabla de Richardson
            results = f"""
Extrapolación de Richardson
===========================
Función: f(x) = {function_str}
Punto: x = {x}

Mejor aproximación: {best_approx:.12f}

Tabla de Richardson:
"""
            for i, row in enumerate(R_table):
                results += f"h={h_values[i]:8.2e}: "
                for j, val in enumerate(row):
                    if val != 0:
                        results += f"{val:12.8f} "
                results += "\n"

            # Comparar con exacta si disponible
            exact_str = self.exact_derivative.text().strip()
            if exact_str:
                try:
                    exact_f = MathParser.parse_function(exact_str)
                    exact_value = exact_f(x)
                    error = abs(exact_value - best_approx)
                    results += f"\nValor exacto: {exact_value:.12f}"
                    results += f"\nError: {error:.2e}"
                except:
                    pass

            self.results_text.setText(results)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en extrapolación de Richardson: {str(e)}")
