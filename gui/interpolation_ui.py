"""
Módulo para los componentes de la interfaz de usuario de interpolación
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QTableWidget, QTableWidgetItem, QMessageBox, QSplitter, QTabWidget
)
from PyQt6.QtCore import Qt


class InterpolationUI:
    """
    Clase que maneja la interfaz de usuario para interpolación
    """

    def __init__(self, plot_widget):
        self.plot_widget = plot_widget
        self.data_table = None
        self.eval_point = None
        self.results_text = None

    def create_ui(self):
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
        eval_layout.addWidget(interpolate_btn)

        eval_group.setLayout(eval_layout)
        left_layout.addWidget(eval_group)

        # Diferencias finitas
        diff_group = QGroupBox("Diferencias Finitas")
        diff_layout = QVBoxLayout()

        diff_btn = QPushButton("Tabla de Diferencias")
        diff_btn.setStyleSheet("background-color: #fd79a8; color: white; font-weight: bold; padding: 10px;")
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

        return layout, self.data_table, self.eval_point, self.results_text, interpolate_btn, diff_btn

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
