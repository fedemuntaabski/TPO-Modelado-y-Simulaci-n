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
        self.derivatives_tab = self.create_derivatives_tab()
        self.tab_widget.addTab(self.derivatives_tab, "🔢 Derivadas")

        # Pestaña de Interpolación
        self.interpolation_tab = self.create_interpolation_tab()
        self.tab_widget.addTab(self.interpolation_tab, "📊 Interpolación")

        # Pestaña de Análisis Avanzado
        self.analysis_tab = self.create_analysis_tab()
        self.tab_widget.addTab(self.analysis_tab, "🔬 Análisis Avanzado")

        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.plot_widget)

        self.setLayout(main_layout)

    def create_derivatives_tab(self):
        """Crea la pestaña de derivadas numéricas"""
        widget = QWidget()
        layout = QHBoxLayout()

        # Panel izquierdo: Controles
        left_panel = QGroupBox("Derivadas Numéricas")
        left_layout = QVBoxLayout()

        # Función
        self.fd_function_input = QLineEdit()
        self.fd_function_input.setPlaceholderText("Ej: x**3 + 2*x**2 - x + 1")
        self.fd_function_input.focusInEvent = lambda e: self.keyboard.set_target(self.fd_function_input)
        left_layout.addWidget(QLabel("Función f(x):"))
        left_layout.addWidget(self.fd_function_input)

        # Punto de evaluación
        self.fd_x_point = QDoubleSpinBox()
        self.fd_x_point.setRange(-100, 100)
        self.fd_x_point.setValue(1)
        self.fd_x_point.setDecimals(4)
        left_layout.addWidget(QLabel("Punto x:"))
        left_layout.addWidget(self.fd_x_point)

        # Paso h
        self.fd_h_value = QDoubleSpinBox()
        self.fd_h_value.setRange(1e-10, 1)
        self.fd_h_value.setValue(1e-5)
        self.fd_h_value.setDecimals(10)
        left_layout.addWidget(QLabel("Paso h:"))
        left_layout.addWidget(self.fd_h_value)

        # Orden de derivada
        self.fd_order = QSpinBox()
        self.fd_order.setRange(1, 4)
        self.fd_order.setValue(1)
        left_layout.addWidget(QLabel("Orden:"))
        left_layout.addWidget(self.fd_order)

        # Método
        self.fd_method = QComboBox()
        self.fd_method.addItems(["Central", "Hacia adelante", "Hacia atrás", "Adaptativo"])
        left_layout.addWidget(QLabel("Método:"))
        left_layout.addWidget(self.fd_method)

        # Botones
        calc_btn = QPushButton("Calcular")
        calc_btn.setStyleSheet("background-color: #00cec9; color: white; font-weight: bold; padding: 8px;")
        calc_btn.clicked.connect(self.calculate_fd_derivative)
        left_layout.addWidget(calc_btn)

        richardson_btn = QPushButton("Richardson")
        richardson_btn.setStyleSheet("background-color: #fdcb6e; color: black; font-weight: bold; padding: 8px;")
        richardson_btn.clicked.connect(self.fd_richardson)
        left_layout.addWidget(richardson_btn)

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

        widget.setLayout(layout)
        return widget

    def create_interpolation_tab(self):
        """Crea la pestaña de interpolación con diferencias finitas"""
        widget = QWidget()
        layout = QHBoxLayout()

        # Panel izquierdo: Controles
        left_panel = QGroupBox("Interpolación")
        left_layout = QVBoxLayout()

        # Tabla de puntos
        table_group = QGroupBox("Puntos de Datos")
        table_layout = QVBoxLayout()

        self.fd_data_table = QTableWidget(5, 2)
        self.fd_data_table.setHorizontalHeaderLabels(['x', 'y'])
        self.fd_data_table.setMaximumHeight(200)

        # Llenar con datos de ejemplo
        for i in range(5):
            x_val = i - 2
            y_val = x_val**2
            self.fd_data_table.setItem(i, 0, QTableWidgetItem(str(x_val)))
            self.fd_data_table.setItem(i, 1, QTableWidgetItem(str(y_val)))

        table_layout.addWidget(self.fd_data_table)

        # Botones para tabla
        table_buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Agregar")
        add_btn.clicked.connect(self.fd_add_row)
        remove_btn = QPushButton("Eliminar")
        remove_btn.clicked.connect(self.fd_remove_row)
        clear_btn = QPushButton("Limpiar")
        clear_btn.clicked.connect(self.fd_clear_table)

        table_buttons_layout.addWidget(add_btn)
        table_buttons_layout.addWidget(remove_btn)
        table_buttons_layout.addWidget(clear_btn)
        table_layout.addLayout(table_buttons_layout)

        table_group.setLayout(table_layout)
        left_layout.addWidget(table_group)

        # Punto de interpolación
        interp_layout = QHBoxLayout()
        self.fd_interp_point = QDoubleSpinBox()
        self.fd_interp_point.setRange(-100, 100)
        self.fd_interp_point.setValue(0.5)
        self.fd_interp_point.setDecimals(4)
        interp_layout.addWidget(QLabel("Interpolar en x:"))
        interp_layout.addWidget(self.fd_interp_point)
        left_layout.addLayout(interp_layout)

        # Botones
        interp_btn = QPushButton("Interpolar")
        interp_btn.setStyleSheet("background-color: #00cec9; color: white; font-weight: bold; padding: 8px;")
        interp_btn.clicked.connect(self.fd_interpolate)
        left_layout.addWidget(interp_btn)

        diff_table_btn = QPushButton("Tabla de Diferencias")
        diff_table_btn.setStyleSheet("background-color: #fd79a8; color: white; font-weight: bold; padding: 8px;")
        diff_table_btn.clicked.connect(self.fd_show_differences_table)
        left_layout.addWidget(diff_table_btn)

        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(350)

        # Panel derecho: Resultados
        right_panel = QGroupBox("Resultados")
        right_layout = QVBoxLayout()

        self.fd_interp_results = QTextEdit()
        self.fd_interp_results.setMaximumHeight(300)
        right_layout.addWidget(self.fd_interp_results)

        right_panel.setLayout(right_layout)

        layout.addWidget(left_panel)
        layout.addWidget(right_panel)

        widget.setLayout(layout)
        return widget

    def create_analysis_tab(self):
        """Crea la pestaña de análisis avanzado"""
        widget = QWidget()
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

        widget.setLayout(layout)
        return widget

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

            from core.finite_differences import FiniteDifferences

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

    def fd_richardson(self):
        """Aplica extrapolación de Richardson"""
        try:
            function_str = self.fd_function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese una función")
                return

            f = MathParser.parse_function(function_str)
            x = self.fd_x_point.value()

            from core.finite_differences import FiniteDifferences
            result, info = FiniteDifferences.richardson_extrapolation(f, x)

            self.fd_results_text.setText(f"""
EXTRAPOLACIÓN DE RICHARDSON
Función: f(x) = {function_str}
Punto: x = {x}

Derivada mejorada: f'(x) ≈ {result:.10f}
Error estimado: {info['estimated_error']:.2e}

Valores de h utilizados:
{', '.join([f'{h:.2e}' for h in info['h_values']])}
            """.strip())

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en Richardson: {str(e)}")

    def fd_interpolate(self):
        """Realiza interpolación usando diferencias finitas"""
        try:
            # Obtener puntos de la tabla
            x_points = []
            y_points = []

            for i in range(self.fd_data_table.rowCount()):
                x_item = self.fd_data_table.item(i, 0)
                y_item = self.fd_data_table.item(i, 1)

                if x_item and y_item and x_item.text().strip() and y_item.text().strip():
                    x_points.append(float(x_item.text()))
                    y_points.append(float(y_item.text()))

            if len(x_points) < 2:
                QMessageBox.warning(self, "Error", "Necesita al menos 2 puntos")
                return

            x_eval = self.fd_interp_point.value()

            from core.finite_differences import FiniteDifferences
            result = FiniteDifferences.interpolate_with_differences(
                np.array(x_points), np.array(y_points), x_eval
            )

            self.fd_interp_results.setText(f"""
INTERPOLACIÓN
Puntos: {len(x_points)}
x = {x_eval}

Valor interpolado: f(x) ≈ {result:.6f}
            """.strip())

            # Graficar
            self.plot_fd_interpolation(x_points, y_points, x_eval, result)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error interpolando: {str(e)}")

    def fd_show_differences_table(self):
        """Muestra la tabla de diferencias finitas"""
        try:
            # Obtener puntos
            x_points = []
            y_points = []

            for i in range(self.fd_data_table.rowCount()):
                x_item = self.fd_data_table.item(i, 0)
                y_item = self.fd_data_table.item(i, 1)

                if x_item and y_item and x_item.text().strip() and y_item.text().strip():
                    x_points.append(float(x_item.text()))
                    y_points.append(float(y_item.text()))

            if len(x_points) < 2:
                QMessageBox.warning(self, "Error", "Necesita al menos 2 puntos")
                return

            from core.finite_differences import FiniteDifferences
            table = FiniteDifferences.finite_differences_table(
                np.array(x_points), np.array(y_points)
            )

            # Mostrar tabla
            result = "TABLA DE DIFERENCIAS FINITAS\n\n"
            result += "x\t\t" + "\t\t".join([f"Δ{i}" for i in range(table.shape[1])]) + "\n"
            result += "-" * (15 * table.shape[1]) + "\n"

            for i in range(table.shape[0]):
                row = f"{x_points[i]:.4f}\t"
                for j in range(table.shape[1]):
                    if not np.isnan(table[i, j]):
                        row += f"{table[i, j]:.6f}\t"
                    else:
                        row += "-\t"
                result += row + "\n"

            self.fd_interp_results.setText(result)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generando tabla: {str(e)}")

    def fd_stability_analysis(self):
        """Análisis de estabilidad"""
        try:
            function_str = self.analysis_function.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese una función")
                return

            f = MathParser.parse_function(function_str)
            x = self.analysis_point.value()

            from core.finite_differences import FiniteDifferences
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

            from core.finite_differences import FiniteDifferences
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

    def fd_add_row(self):
        """Agrega fila a la tabla"""
        current_rows = self.fd_data_table.rowCount()
        self.fd_data_table.insertRow(current_rows)

    def fd_remove_row(self):
        """Elimina última fila"""
        current_rows = self.fd_data_table.rowCount()
        if current_rows > 1:
            self.fd_data_table.removeRow(current_rows - 1)

    def fd_clear_table(self):
        """Limpia tabla"""
        for i in range(self.fd_data_table.rowCount()):
            for j in range(self.fd_data_table.columnCount()):
                self.fd_data_table.setItem(i, j, QTableWidgetItem(""))

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

    def plot_fd_interpolation(self, x_points, y_points, x_eval, y_eval):
        """Grafica interpolación"""
        x_range = np.linspace(min(x_points) - 1, max(x_points) + 1, 1000)

        self.plot_widget.figure.clear()
        ax = self.plot_widget.figure.add_subplot(111)
        ax.plot(x_points, y_points, 'bo', markersize=8, label='Puntos dados')
        ax.plot(x_eval, y_eval, 'rx', markersize=10, label=f'Interpolación en x={x_eval}')
        ax.set_title('Interpolación con Diferencias Finitas', fontsize=14, fontweight='bold')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)
        ax.legend()
        self.plot_widget.canvas.draw()

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
