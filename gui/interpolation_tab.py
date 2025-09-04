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
