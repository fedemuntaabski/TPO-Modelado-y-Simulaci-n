"""
Pestañas adicionales para métodos avanzados
Incluye interpolación, diferencias finitas y aceleración de Aitken
"""

import numpy as np
from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QTableWidget, QTableWidgetItem, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt

from numerics.advanced import InterpolationMethods, AdvancedNumericalMethods, ErrorAnalysis
from numerics.methods import MathParser

class InterpolationTab(QWidget):
    """
    Pestaña para interpolación de Lagrange y análisis de diferencias finitas
    """
    
    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        
        # Panel izquierdo: Entrada de datos
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Datos para interpolación
        data_group = QGroupBox("Puntos de Datos")
        data_layout = QVBoxLayout()
        
        # Tabla para puntos
        self.data_table = QTableWidget(5, 2)
        self.data_table.setHorizontalHeaderLabels(['x', 'y'])
        self.data_table.setMaximumHeight(200)
        
        # Llenar con datos de ejemplo
        example_x = [0, 1, 2, 3, 4]
        example_y = [1, 2, 5, 10, 17]  # x^2 + 1
        
        for i, (x, y) in enumerate(zip(example_x, example_y)):
            self.data_table.setItem(i, 0, QTableWidgetItem(str(x)))
            self.data_table.setItem(i, 1, QTableWidgetItem(str(y)))
        
        data_layout.addWidget(self.data_table)
        
        # Botones para gestionar datos
        data_buttons = QHBoxLayout()
        
        add_row_btn = QPushButton("Agregar Fila")
        add_row_btn.clicked.connect(self.add_row)
        remove_row_btn = QPushButton("Quitar Fila")
        remove_row_btn.clicked.connect(self.remove_row)
        clear_btn = QPushButton("Limpiar")
        clear_btn.clicked.connect(self.clear_data)
        
        data_buttons.addWidget(add_row_btn)
        data_buttons.addWidget(remove_row_btn)
        data_buttons.addWidget(clear_btn)
        
        data_layout.addLayout(data_buttons)
        data_group.setLayout(data_layout)
        left_layout.addWidget(data_group)
        
        # Evaluación de interpolación
        eval_group = QGroupBox("Evaluación")
        eval_layout = QVBoxLayout()
        
        self.eval_point = QDoubleSpinBox()
        self.eval_point.setRange(-100, 100)
        self.eval_point.setValue(2.5)
        self.eval_point.setDecimals(4)
        eval_layout.addWidget(QLabel("Punto de evaluación:"))
        eval_layout.addWidget(self.eval_point)
        
        # Botón interpolar
        interpolate_btn = QPushButton("Interpolar con Lagrange")
        interpolate_btn.setStyleSheet("background-color: #a29bfe; color: white; font-weight: bold; padding: 10px;")
        interpolate_btn.clicked.connect(self.interpolate_lagrange)
        eval_layout.addWidget(interpolate_btn)
        
        eval_group.setLayout(eval_layout)
        left_layout.addWidget(eval_group)
        
        # Diferencias finitas
        diff_group = QGroupBox("Diferencias Finitas")
        diff_layout = QVBoxLayout()
        
        diff_btn = QPushButton("Tabla de Diferencias")
        diff_btn.setStyleSheet("background-color: #fd79a8; color: white; font-weight: bold; padding: 10px;")
        diff_btn.clicked.connect(self.calculate_differences)
        diff_layout.addWidget(diff_btn)
        
        diff_group.setLayout(diff_layout)
        left_layout.addWidget(diff_group)
        
        # Resultados
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(200)
        left_layout.addWidget(QLabel("Resultados:"))
        left_layout.addWidget(self.results_text)
        
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(400)
        
        # Panel derecho: Gráfico
        layout.addWidget(left_panel)
        layout.addWidget(self.plot_widget)
        
        self.setLayout(layout)
    
    def add_row(self):
        """Agrega una fila a la tabla"""
        current_rows = self.data_table.rowCount()
        self.data_table.insertRow(current_rows)
    
    def remove_row(self):
        """Elimina la última fila de la tabla"""
        current_rows = self.data_table.rowCount()
        if current_rows > 1:
            self.data_table.removeRow(current_rows - 1)
    
    def clear_data(self):
        """Limpia todos los datos de la tabla"""
        for i in range(self.data_table.rowCount()):
            for j in range(self.data_table.columnCount()):
                self.data_table.setItem(i, j, QTableWidgetItem(""))
    
    def get_data_points(self):
        """Extrae los puntos de datos de la tabla"""
        x_points = []
        y_points = []
        
        for i in range(self.data_table.rowCount()):
            x_item = self.data_table.item(i, 0)
            y_item = self.data_table.item(i, 1)
            
            if x_item and y_item and x_item.text().strip() and y_item.text().strip():
                try:
                    x = float(x_item.text())
                    y = float(y_item.text())
                    x_points.append(x)
                    y_points.append(y)
                except ValueError:
                    continue
        
        return np.array(x_points), np.array(y_points)
    
    def interpolate_lagrange(self):
        """Realiza interpolación de Lagrange"""
        try:
            x_points, y_points = self.get_data_points()
            
            if len(x_points) < 2:
                QMessageBox.warning(self, "Error", "Se necesitan al menos 2 puntos")
                return
            
            # Verificar que no hay puntos x repetidos
            if len(np.unique(x_points)) != len(x_points):
                QMessageBox.warning(self, "Error", "Los puntos x deben ser únicos")
                return
            
            # Ordenar puntos por x
            sorted_indices = np.argsort(x_points)
            x_points = x_points[sorted_indices]
            y_points = y_points[sorted_indices]
            
            # Punto de evaluación
            x_eval_point = self.eval_point.value()
            
            # Crear rango para graficar
            x_min, x_max = x_points.min(), x_points.max()
            x_range = x_max - x_min
            x_plot = np.linspace(x_min - 0.2*x_range, x_max + 0.2*x_range, 200)
            
            # Interpolar
            y_plot, polynomial = InterpolationMethods.lagrange_interpolation_detailed(
                x_points, y_points, x_plot
            )
            
            # Evaluar en el punto específico
            y_eval = polynomial(x_eval_point)
            
            # Graficar
            self.plot_widget.figure.clear()
            ax = self.plot_widget.figure.add_subplot(111)
            
            # Puntos originales
            ax.plot(x_points, y_points, 'ro', markersize=8, label='Puntos dados')
            
            # Polinomio interpolador
            ax.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio de Lagrange')
            
            # Punto evaluado
            ax.plot(x_eval_point, y_eval, 'gs', markersize=10, label=f'Evaluación en x={x_eval_point}')
            
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Interpolación de Lagrange')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            self.plot_widget.canvas.draw()
            
            # Mostrar resultados
            results = f"""
Interpolación de Lagrange
------------------------
Puntos utilizados: {len(x_points)}
Grado del polinomio: {len(x_points) - 1}

Evaluación:
x = {x_eval_point}
y = {y_eval:.8f}

Puntos dados:
"""
            for i, (x, y) in enumerate(zip(x_points, y_points)):
                results += f"  P{i+1}: ({x}, {y})\n"
            
            self.results_text.setText(results)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en interpolación: {str(e)}")
    
    def calculate_differences(self):
        """Calcula la tabla de diferencias finitas"""
        try:
            x_points, y_points = self.get_data_points()
            
            if len(x_points) < 2:
                QMessageBox.warning(self, "Error", "Se necesitan al menos 2 puntos")
                return
            
            # Ordenar puntos
            sorted_indices = np.argsort(x_points)
            x_points = x_points[sorted_indices]
            y_points = y_points[sorted_indices]
            
            # Calcular tabla de diferencias
            diff_table = InterpolationMethods.finite_differences_table(x_points, y_points)
            
            # Formatear resultados
            results = "Tabla de Diferencias Finitas\n"
            results += "=" * 40 + "\n\n"
            results += f"{'i':>3} {'x':>8} {'f(x)':>12}"
            
            n = len(x_points)
            for j in range(1, n):
                results += f"{'Δ^' + str(j) + 'f':>12}"
            results += "\n"
            results += "-" * (15 + 12 * n) + "\n"
            
            for i in range(n):
                results += f"{i:>3} {x_points[i]:>8.3f} {y_points[i]:>12.6f}"
                for j in range(1, n - i):
                    if i + j <= n:
                        results += f"{diff_table[i, j]:>12.6f}"
                results += "\n"
            
            # Verificar si las diferencias son constantes (polinomio)
            last_col = n - 1
            if n > 2:
                last_diffs = diff_table[:n-last_col, last_col]
                if len(last_diffs) > 1 and np.allclose(last_diffs, last_diffs[0], rtol=1e-10):
                    results += f"\n📊 Los datos parecen seguir un polinomio de grado {last_col}\n"
                    results += f"   (diferencia constante en la columna {last_col})\n"
            
            self.results_text.setText(results)
            
            # Graficar solo los puntos
            self.plot_widget.figure.clear()
            ax = self.plot_widget.figure.add_subplot(111)
            ax.plot(x_points, y_points, 'ro-', markersize=8, linewidth=2)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title('Puntos de Datos para Diferencias Finitas')
            ax.grid(True, alpha=0.3)
            self.plot_widget.canvas.draw()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error calculando diferencias: {str(e)}")

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
