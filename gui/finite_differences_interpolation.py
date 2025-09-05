"""
Interpolation tab for Finite Differences
"""

import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QPushButton, QTextEdit, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt

from core.finite_differences import FiniteDifferences

class InterpolationTab(QWidget):
    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()

    def init_ui(self):
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

        self.setLayout(layout)

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
