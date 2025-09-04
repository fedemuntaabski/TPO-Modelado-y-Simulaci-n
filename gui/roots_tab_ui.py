"""
Módulo de Interfaz de Usuario para la Pestaña de Raíces
Contiene la configuración de widgets y layouts para RootsTab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QMessageBox, QTableWidget, QSplitter
)
from PyQt6.QtCore import Qt

class RootsTabUI:
    """
    Clase que maneja la interfaz de usuario de la pestaña de raíces
    """

    def __init__(self, keyboard, plot_widget):
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario principal"""
        # Layout principal con splitter para mejor organización
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Panel izquierdo: Controles de entrada
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Panel de entrada
        self.input_panel = QGroupBox("Búsqueda de Raíces")
        self.input_layout = QVBoxLayout()
        self.input_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Función
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: x**2 - 4, sin(x) - 0.5")
        self.function_input.focusInEvent = lambda e: self.keyboard.set_target(self.function_input)
        # Aumentar tamaño para mejor visibilidad
        self.function_input.setMaximumSize(280, 35)
        self.function_input.setMinimumSize(250, 30)
        self.function_input.setStyleSheet("font-size: 14px; padding: 5px;")
        self.input_layout.addWidget(QLabel("Función f(x):"))
        self.input_layout.addWidget(self.function_input)

        # Método
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Bisección", "Newton-Raphson", "Punto Fijo", "Aitken"])
        self.method_combo.currentTextChanged.connect(self.on_method_changed)
        # Aumentar tamaño para mejor visibilidad
        self.method_combo.setMaximumSize(280, 35)
        self.method_combo.setMinimumSize(250, 30)
        self.method_combo.setStyleSheet("font-size: 14px; padding: 5px;")
        self.input_layout.addWidget(QLabel("Método:"))
        self.input_layout.addWidget(self.method_combo)

        # Parámetros específicos del método
        self.params_widget = QWidget()
        self.params_layout = QVBoxLayout()
        self.params_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.params_widget.setLayout(self.params_layout)
        self.input_layout.addWidget(self.params_widget)

        # Tolerancia e iteraciones
        tolerance_layout = QHBoxLayout()
        tolerance_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.tolerance_input = QLineEdit("1e-6")
        self.tolerance_input.setPlaceholderText("Ej: 1e-6, 0.000001")
        # Aumentar tamaño para mejor visibilidad
        self.tolerance_input.setMaximumSize(180, 35)
        self.tolerance_input.setMinimumSize(150, 30)
        self.tolerance_input.setStyleSheet("font-size: 14px; padding: 5px;")
        tolerance_layout.addWidget(QLabel("Tolerancia:"))
        tolerance_layout.addWidget(self.tolerance_input)

        self.max_iter_input = QLineEdit("100")
        self.max_iter_input.setPlaceholderText("Ej: 100, 50, 200")
        # Aumentar tamaño para mejor visibilidad
        self.max_iter_input.setMaximumSize(180, 35)
        self.max_iter_input.setMinimumSize(150, 30)
        self.max_iter_input.setStyleSheet("font-size: 14px; padding: 5px;")
        tolerance_layout.addWidget(QLabel("Máx iter:"))
        tolerance_layout.addWidget(self.max_iter_input)

        self.input_layout.addLayout(tolerance_layout)

        # Botón resolver
        self.solve_button = QPushButton("Encontrar Raíz")
        from gui.themes import DarkTheme
        self.solve_button.setStyleSheet(DarkTheme.get_button_style("warning") + "padding: 12px;")
        self.input_layout.addWidget(self.solve_button)

        # Área de resultados
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        self.input_layout.addWidget(QLabel("Resultados:"))
        self.input_layout.addWidget(self.results_text)

        self.input_panel.setLayout(self.input_layout)
        self.input_panel.setMaximumWidth(420)
        self.input_panel.setMinimumWidth(380)

        self.left_layout.addWidget(self.input_panel)
        self.left_panel.setLayout(self.left_layout)

        # Panel derecho: Tabla y gráfico
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout()

        # Tabla de resultados detallados
        table_panel = QGroupBox("Tabla de Iteraciones")
        table_layout = QVBoxLayout()
        self.results_table = QTableWidget()
        self.results_table.setMaximumHeight(400)  # Aumentar altura para mejor visibilidad
        table_layout.addWidget(self.results_table)
        table_panel.setLayout(table_layout)

        self.right_layout.addWidget(table_panel)
        self.right_layout.addWidget(self.plot_widget)

        self.right_panel.setLayout(self.right_layout)

        # Agregar paneles al splitter
        self.main_splitter.addWidget(self.left_panel)
        self.main_splitter.addWidget(self.right_panel)
        self.main_splitter.setSizes([400, 800])  # Tamaños iniciales

        # Inicializar parámetros del método
        self.on_method_changed()

    def on_method_changed(self):
        """Actualiza la UI según el método seleccionado"""
        # Limpiar layout anterior
        for i in reversed(range(self.params_layout.count())):
            self.params_layout.itemAt(i).widget().setParent(None)

        method = self.method_combo.currentText()

        if method == "Bisección":
            # Intervalo [a, b]
            interval_layout = QHBoxLayout()

            self.a_input = QLineEdit("-5")
            self.a_input.setPlaceholderText("Ej: -5, -2.5, 0")
            # Aumentar tamaño para mejor visibilidad
            self.a_input.setMaximumSize(140, 35)
            self.a_input.setMinimumSize(120, 30)
            self.a_input.setStyleSheet("font-size: 14px; padding: 5px;")
            interval_layout.addWidget(QLabel("a:"))
            interval_layout.addWidget(self.a_input)

            self.b_input = QLineEdit("5")
            self.b_input.setPlaceholderText("Ej: 5, 2.5, 10")
            # Aumentar tamaño para mejor visibilidad
            self.b_input.setMaximumSize(140, 35)
            self.b_input.setMinimumSize(120, 30)
            self.b_input.setStyleSheet("font-size: 14px; padding: 5px;")
            interval_layout.addWidget(QLabel("b:"))
            interval_layout.addWidget(self.b_input)

            interval_widget = QWidget()
            interval_widget.setLayout(interval_layout)
            self.params_layout.addWidget(QLabel("Intervalo [a, b]:"))
            self.params_layout.addWidget(interval_widget)

        elif method == "Newton-Raphson":
            # Aproximación inicial y derivada
            self.x0_input = QLineEdit("1")
            self.x0_input.setPlaceholderText("Ej: 1, 0.5, -2")
            # Aumentar tamaño para mejor visibilidad
            self.x0_input.setMaximumSize(200, 35)
            self.x0_input.setMinimumSize(180, 30)
            self.x0_input.setStyleSheet("font-size: 14px; padding: 5px;")
            self.params_layout.addWidget(QLabel("Aproximación inicial x₀:"))
            self.params_layout.addWidget(self.x0_input)

            self.derivative_input = QLineEdit()
            self.derivative_input.setPlaceholderText("Ej: 2*x, cos(x)")
            self.derivative_input.focusInEvent = lambda e: self.keyboard.set_target(self.derivative_input)
            # Aumentar tamaño para mejor visibilidad
            self.derivative_input.setMaximumSize(200, 35)
            self.derivative_input.setMinimumSize(180, 30)
            self.derivative_input.setStyleSheet("font-size: 14px; padding: 5px;")
            self.params_layout.addWidget(QLabel("Derivada f'(x):"))
            self.params_layout.addWidget(self.derivative_input)

        elif method == "Punto Fijo":
            # Función de iteración g(x)
            self.x0_input = QLineEdit("1")
            self.x0_input.setPlaceholderText("Ej: 1, 0.5, -2")
            # Aumentar tamaño para mejor visibilidad
            self.x0_input.setMaximumSize(200, 35)
            self.x0_input.setMinimumSize(180, 30)
            self.x0_input.setStyleSheet("font-size: 14px; padding: 5px;")
            self.params_layout.addWidget(QLabel("Aproximación inicial x₀:"))
            self.params_layout.addWidget(self.x0_input)

            self.g_function_input = QLineEdit()
            self.g_function_input.setPlaceholderText("Ej: sqrt(4 + x), (x + 4/x)/2")
            self.g_function_input.focusInEvent = lambda e: self.keyboard.set_target(self.g_function_input)
            # Aumentar tamaño para mejor visibilidad
            self.g_function_input.setMaximumSize(200, 35)
            self.g_function_input.setMinimumSize(180, 30)
            self.g_function_input.setStyleSheet("font-size: 14px; padding: 5px;")
            self.params_layout.addWidget(QLabel("Función g(x) para x = g(x):"))
            self.params_layout.addWidget(self.g_function_input)

        elif method == "Aitken":
            # Función de iteración g(x) para método de Aitken
            self.x0_input = QLineEdit("1")
            self.x0_input.setPlaceholderText("Ej: 1, 0.5, -2")
            # Aumentar tamaño para mejor visibilidad
            self.x0_input.setMaximumSize(200, 35)
            self.x0_input.setMinimumSize(180, 30)
            self.x0_input.setStyleSheet("font-size: 14px; padding: 5px;")
            self.params_layout.addWidget(QLabel("Aproximación inicial x₀:"))
            self.params_layout.addWidget(self.x0_input)

            self.g_function_input = QLineEdit()
            self.g_function_input.setPlaceholderText("Ej: sqrt(4 + x), (x + 4/x)/2")
            self.g_function_input.focusInEvent = lambda e: self.keyboard.set_target(self.g_function_input)
            # Aumentar tamaño para mejor visibilidad
            self.g_function_input.setMaximumSize(200, 35)
            self.g_function_input.setMinimumSize(180, 30)
            self.g_function_input.setStyleSheet("font-size: 14px; padding: 5px;")
            self.params_layout.addWidget(QLabel("Función g(x) para x = g(x):"))
            self.params_layout.addWidget(self.g_function_input)

    def get_main_widget(self):
        """Retorna el widget principal de la interfaz"""
        return self.main_splitter
