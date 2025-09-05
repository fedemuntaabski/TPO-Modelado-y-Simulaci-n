"""
Pestaña dedicada para métodos de Newton-Cotes
Implementa la clase NewtonCotesTab con tabla de resultados y visualización
"""

import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox,
    QDoubleSpinBox, QMessageBox, QCheckBox, QSplitter, QComboBox
)
from PyQt6.QtCore import Qt

from numerics.methods import NumericalMethods, MathParser

class NewtonCotesTab(QWidget):
    """
    Pestaña dedicada para métodos de Newton-Cotes con tabla comparativa
    """

    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.methods = {
            "Rectángulo Compuesto": "rectangle",
            "Rectángulo Medio Compuesto": "midpoint",
            "Trapecio Compuesto": "trapezoid",
            "Simpson 1/3 Compuesto": "simpson_13",
            "Simpson 3/8 Compuesto": "simpson_38",
            "Rectángulo Simple": "rectangle_simple",
            "Rectángulo Medio Simple": "midpoint_simple",
            "Trapecio Simple": "trapezoid_simple",
            "Simpson 1/3 Simple": "simpson_13_simple",
            "Simpson 3/8 Simple": "simpson_38_simple"
        }
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Panel izquierdo - Controles
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        # Grupo de entrada de función
        input_group = QGroupBox("Función y Límites")
        input_layout = QVBoxLayout()

        # Función
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: x**2, sin(x), exp(-x**2)")
        self.function_input.focusInEvent = lambda e: self.keyboard.set_target(self.function_input)
        function_label = QLabel("f(x):")
        function_label.setStyleSheet("font-size: 8px; margin: 0px; padding: 0px;")
        input_layout.addWidget(function_label)
        input_layout.addWidget(self.function_input)

        # Límites de integración
        limits_layout = QHBoxLayout()

        self.a_input = QLineEdit()
        self.a_input.setText("0")
        self.a_input.setPlaceholderText("Ej: 0, pi/2, sqrt(2)")
        self.a_input.setMaximumWidth(80)
        a_label = QLabel("a:")
        a_label.setStyleSheet("font-size: 8px; margin: 0px; padding: 0px;")
        limits_layout.addWidget(a_label)
        limits_layout.addWidget(self.a_input)

        self.b_input = QLineEdit()
        self.b_input.setText("1")
        self.b_input.setPlaceholderText("Ej: 1, pi, 2*pi")
        self.b_input.setMaximumWidth(80)
        b_label = QLabel("b:")
        b_label.setStyleSheet("font-size: 8px; margin: 0px; padding: 0px;")
        limits_layout.addWidget(b_label)
        limits_layout.addWidget(self.b_input)

        input_layout.addLayout(limits_layout)

        # Número de subdivisiones
        self.n_input = QSpinBox()
        self.n_input.setRange(2, 1000)
        self.n_input.setValue(100)
        n_label = QLabel("n:")
        n_label.setStyleSheet("font-size: 8px; margin: 0px; padding: 0px;")
        input_layout.addWidget(n_label)
        input_layout.addWidget(self.n_input)

        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)

        # Método de integración
        method_layout = QHBoxLayout()
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Rectángulo Compuesto",
            "Rectángulo Medio Compuesto", 
            "Trapecio Compuesto",
            "Simpson 1/3 Compuesto",
            "Simpson 3/8 Compuesto",
            "Rectángulo Simple",
            "Rectángulo Medio Simple",
            "Trapecio Simple", 
            "Simpson 1/3 Simple",
            "Simpson 3/8 Simple"
        ])
        self.method_combo.setCurrentText("Simpson 1/3 Compuesto")
        method_label = QLabel("Método:")
        method_label.setStyleSheet("font-size: 8px; margin: 0px; padding: 0px;")
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo)
        input_layout.addLayout(method_layout)

        # Botones
        buttons_layout = QHBoxLayout()

        calc_button = QPushButton("Calcular")
        calc_button.clicked.connect(self.calculate_integral)
        buttons_layout.addWidget(calc_button)

        plot_button = QPushButton("Graficar")
        plot_button.clicked.connect(self.plot_function)
        buttons_layout.addWidget(plot_button)

        clear_button = QPushButton("Limpiar")
        clear_button.clicked.connect(self.clear_results)
        buttons_layout.addWidget(clear_button)

        left_layout.addLayout(buttons_layout)

        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(350)

        # Panel derecho - Resultados
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        # Tabla de resultados
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels([
            "Método", "Resultado", "Error Relativo"
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        right_layout.addWidget(QLabel("Resultados de Integración:"))
        right_layout.addWidget(self.results_table)

        right_panel.setLayout(right_layout)

        # Splitter para dividir los paneles
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.addWidget(self.plot_widget)
        splitter.setSizes([350, 400, 400])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def calculate_integral(self):
        """Calcula la integral usando el método seleccionado"""
        try:
            function_str = self.function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese la función f(x)")
                return

            f = MathParser.parse_function(function_str)
            a = self.evaluate_expression(self.a_input.text())
            b = self.evaluate_expression(self.b_input.text())
            n = self.n_input.value()

            if a >= b:
                QMessageBox.warning(self, "Error", "a debe ser menor que b")
                return

            # Obtener método seleccionado
            selected_method = self.method_combo.currentText()
            method_key = self.methods[selected_method]

            # Calcular valor de referencia usando scipy
            try:
                from scipy.integrate import quad
                reference_value, _ = quad(f, a, b)
            except:
                reference_value = None

            # Calcular integral
            result = NumericalMethods.newton_cotes_integration(f, a, b, n, method_key)

            # Calcular error relativo si tenemos valor de referencia
            if reference_value is not None:
                relative_error = abs((result - reference_value) / reference_value) * 100
                error_str = f"{relative_error:.2f}%"
            else:
                error_str = "N/A"

            # Preparar tabla
            self.results_table.setRowCount(1)

            # Llenar tabla
            self.results_table.setItem(0, 0, QTableWidgetItem(selected_method))
            self.results_table.setItem(0, 1, QTableWidgetItem(f"{result:.8f}"))
            self.results_table.setItem(0, 2, QTableWidgetItem(error_str))

            # Graficar
            self.plot_function(f, function_str, a, b, [(selected_method, result, error_str)])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error calculando integral: {str(e)}")

    def plot_function(self, f, function_str, a, b, results):
        """Grafica la función y resalta el área bajo la curva"""
        x = np.linspace(a, b, 200)
        y = [f(xi) for xi in x]

        self.plot_widget.figure.clear()
        ax = self.plot_widget.figure.add_subplot(111)

        # Graficar función
        ax.plot(x, y, 'b-', linewidth=2, label=f'f(x) = {function_str}')

        # Rellenar área bajo la curva
        ax.fill_between(x, y, alpha=0.3, color='blue', label='Área bajo la curva')

        # Configurar gráfico
        ax.set_title(f'Método de Newton-Cotes: ∫ {function_str} dx')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.grid(True, alpha=0.3)
        ax.legend()

        # Agregar información del resultado en el gráfico
        if results:
            method_name, result, error = results[0]
            result_text = f"Método: {method_name}\nResultado: {result:.8f}"
            if error != "N/A":
                result_text += f"\nError: {error}"

        ax.text(0.02, 0.98, result_text, transform=ax.transAxes,
                verticalalignment='top', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        self.plot_widget.canvas.draw()

    def adjust_value(self, line_edit, delta):
        """Ajusta el valor del line edit por el delta especificado"""
        try:
            current_value = float(line_edit.text())
            new_value = current_value + delta
            line_edit.setText(str(new_value))
        except ValueError:
            # Si no puede convertir a float, intentar evaluar la expresión
            try:
                current_value = self.evaluate_expression(line_edit.text())
                new_value = current_value + delta
                line_edit.setText(str(new_value))
            except:
                # Si falla, no hacer nada
                pass

    def evaluate_expression(self, expr_str):
        """Evalúa expresiones matemáticas simples"""
        if not expr_str or expr_str.strip() == "":
            return 0.0

        try:
            # Si es un número simple, devolverlo directamente
            return float(expr_str)
        except ValueError:
            # Si contiene expresiones matemáticas, intentar evaluar
            try:
                import math
                expr = str(expr_str).strip()

                # Reemplazar constantes y funciones comunes
                expr = expr.replace('pi', str(math.pi))
                expr = expr.replace('π', str(math.pi))  # También aceptar π

                # Reemplazar funciones PRIMERO
                expr = expr.replace('sin(', 'math.sin(')
                expr = expr.replace('cos(', 'math.cos(')
                expr = expr.replace('tan(', 'math.tan(')
                expr = expr.replace('sqrt(', 'math.sqrt(')
                expr = expr.replace('exp(', 'math.exp(')
                expr = expr.replace('log(', 'math.log(')
                expr = expr.replace('ln(', 'math.log(')
                
                # Reemplazar la constante e de manera más específica
                # Usar word boundaries para evitar conflictos con funciones
                import re
                expr = re.sub(r'\b e \b', str(math.e), expr)
                expr = re.sub(r'^e$', str(math.e), expr)
                expr = re.sub(r'^e\b', str(math.e), expr)
                expr = re.sub(r'\be$', str(math.e), expr)

                # Evaluar la expresión de forma segura
                result = eval(expr, {"__builtins__": {}}, {"math": math})

                return float(result)
            except Exception as e:
                print(f"Error evaluando expresión '{expr_str}': {e}")
                # Si falla, intentar devolver el valor como número
                try:
                    return float(expr_str)
                except:
                    return 0.0

    def clear_results(self):
        """Limpia la tabla de resultados y el gráfico"""
        self.results_table.setRowCount(0)
        self.plot_widget.figure.clear()
        self.plot_widget.canvas.draw()

    def plot_function(self):
        """Grafica la función en el rango de integración"""
        try:
            # Obtener la función
            function_str = self.function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Por favor ingrese una función.")
                return

            # Obtener límites
            a_str = self.a_input.text().strip()
            b_str = self.b_input.text().strip()

            if not a_str or not b_str:
                QMessageBox.warning(self, "Error", "Por favor ingrese los límites de integración.")
                return

            a = self.evaluate_expression(a_str)
            b = self.evaluate_expression(b_str)

            if a >= b:
                QMessageBox.warning(self, "Error", "El límite inferior debe ser menor que el superior.")
                return

            # Crear puntos para graficar
            x_points = np.linspace(a - 0.5, b + 0.5, 1000)
            y_points = []

            for x in x_points:
                try:
                    y = self.evaluate_function(function_str, x)
                    y_points.append(y)
                except:
                    y_points.append(0)

            # Graficar
            self.plot_widget.clear_plot()
            self.plot_widget.plot_function(x_points, y_points,
                                         f"Función: {function_str}",
                                         "x", "f(x)")

            # Agregar líneas verticales para los límites de integración
            ax = self.plot_widget.figure.gca()
            ax.axvline(x=a, color='red', linestyle='--', alpha=0.7, label=f'Límite inferior: {a}')
            ax.axvline(x=b, color='red', linestyle='--', alpha=0.7, label=f'Límite superior: {b}')
            ax.legend()
            self.plot_widget.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al graficar la función:\n{str(e)}")
