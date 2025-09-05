"""
Componentes GUI principales del Simulador Matemático
Implementa los widgets básicos: teclado virtual, widget de gráficos y aplicación principal

Características:
- Teclado virtual para f            self.tab_widget.addTab(self.credits_tab, "👨‍🎓 Créditos")           self.tab_widget.addTab(self.credits_tab, "👨‍🎓 Créditos")           self.tab_widget.addTab(self.credits_tab, "👥 Créditos")           self.tab_widget.addTab(self.credits_tab, "👥 Créditos")nciones matemáticas
- Widget para mostrar gráficos con matplotlib
- Ventana principal de la aplicación
"""

import sys
from typing import Optional, Callable
import numpy as np
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLineEdit, QLabel, QTextEdit, QGridLayout,
    QGroupBox, QSpinBox, QDoubleSpinBox, QComboBox, QSplitter,
    QMessageBox, QProgressBar, QStatusBar, QScrollArea,
    QFrame, QApplication, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon

from numerics.methods import NumericalMethods, MathParser

class MathKeyboard(QWidget):
    """
    Teclado virtual para ingresar funciones matemáticas
    """

    function_entered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_target = None
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(8)  # Espaciado mayor entre botones para mejor separación
        layout.setContentsMargins(8, 8, 8, 8)

        # Importar tema una vez para eficiencia
        from gui.themes import DarkTheme

        self.function_buttons = []

        # Botones de funciones matemáticas
        functions = ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt', 'pi', 'e']
        for row, text in enumerate(functions):
            button = QPushButton(text)
            button.setMinimumSize(26, 18)
            button.setMaximumSize(38, 22)
            button.clicked.connect(lambda checked, t=text: self.button_clicked(t))
            button.setStyleSheet(DarkTheme.get_keyboard_button_style("function"))
            self.function_buttons.append(button)
            layout.addWidget(button, row, 0)

        self.setLayout(layout)

    def set_target(self, target_widget):
        """Establece el widget de destino para el teclado"""
        self.current_target = target_widget

    def button_clicked(self, text):
        """Maneja los clics en los botones del teclado"""
        if not self.current_target:
            return

        current_text = self.current_target.text()
        new_text = current_text + text
        self.current_target.setText(new_text)

class PlotWidget(QWidget):
    """
    Widget para mostrar gráficos con matplotlib
    """

    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.figure.patch.set_facecolor('white')

    def clear_plot(self):
        """Limpia el gráfico actual"""
        self.figure.clear()
        self.canvas.draw()

    def plot_function(self, x_data, y_data, title="Gráfico", xlabel="x", ylabel="y", label="Función"):
        """Grafica una función"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_data, y_data, 'b-', label=label, linewidth=2)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        ax.legend()
        self.canvas.draw()

    def plot_ode_solution(self, t_data, y_data, title="Solución EDO"):
        """Grafica la solución de una ecuación diferencial"""
        self.plot_function(t_data, y_data, title, "t", "y(t)", "Solución")

    def plot_convergence(self, iterations, values, title="Convergencia"):
        """Grafica la convergencia de un método iterativo"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(iterations, values, 'ro-', linewidth=2, markersize=6)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel("Iteración")
        ax.set_ylabel("Valor")
        ax.grid(True, alpha=0.3)
        self.canvas.draw()

class MathSimulatorApp(QMainWindow):
    """
    Ventana principal del simulador matemático
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("🧮 Simulador Matemático Avanzado - TPO Modelado y Simulación")
        self.setGeometry(100, 100, 1400, 900)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()

        # Título y créditos
        title_frame = self.create_title_frame()
        main_layout.addWidget(title_frame)

        # Splitter principal (horizontal)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Panel izquierdo: Teclado virtual
        left_panel = QGroupBox("")
        left_layout = QVBoxLayout()

        self.keyboard = MathKeyboard()
        left_layout.addWidget(self.keyboard)

        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(120)  # Reducido para layout de 1 columna más compacto

        # Panel derecho: Pestañas y gráficos
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        # Widget de gráficos
        self.plot_widget = PlotWidget()

        # Pestañas de métodos
        self.tab_widget = QTabWidget()

        # Crear pestañas
        from gui.tabs import ODETab, RootsTab, IntegrationTab, NewtonCotesTab
        self.ode_tab = ODETab(self.keyboard, self.plot_widget)
        self.roots_tab = RootsTab(self.keyboard, self.plot_widget)
        self.integration_tab = IntegrationTab(self.keyboard, self.plot_widget)
        self.newton_cotes_tab = NewtonCotesTab(self.keyboard, self.plot_widget)

        # Crear pestaña de créditos simplificada
        self.credits_tab = self.create_credits_tab()

        # Importar pestañas avanzadas
        try:
            from gui.advanced_tabs import FiniteDifferencesTab

            self.finite_differences_tab = FiniteDifferencesTab(self.keyboard, self.plot_widget)

            self.tab_widget.addTab(self.roots_tab, "🎯 Búsqueda de Raíces")
            self.tab_widget.addTab(self.newton_cotes_tab, "📊 Newton-Cotes")
            self.tab_widget.addTab(self.finite_differences_tab, "� Diferencias Finitas")
            self.tab_widget.addTab(self.ode_tab, "📈 Ecuaciones Diferenciales")
            self.tab_widget.addTab(self.integration_tab, "∫ Integración")
            self.tab_widget.addTab(self.credits_tab, "� Créditos")
        except ImportError as e:
            # Si no se pueden importar las pestañas avanzadas, usar solo las básicas
            print(f"Warning: No se pudieron cargar pestañas avanzadas: {e}")
            self.tab_widget.addTab(self.roots_tab, "🎯 Búsqueda de Raíces")
            self.tab_widget.addTab(self.newton_cotes_tab, "📊 Newton-Cotes")
            self.tab_widget.addTab(self.ode_tab, "📈 Ecuaciones Diferenciales")
            self.tab_widget.addTab(self.integration_tab, "∫ Integración")
            self.tab_widget.addTab(self.credits_tab, "� Créditos")

        right_layout.addWidget(self.tab_widget)
        right_panel.setLayout(right_layout)

        # Agregar paneles al splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([350, 1050])

        main_layout.addWidget(main_splitter)
        central_widget.setLayout(main_layout)

        # Barra de estado
        self.statusBar().showMessage("Sistema listo • Seleccione un método numérico para comenzar")

        # Aplicar estilo
        self.apply_style()

    def create_title_frame(self):
        """Crea el frame del título con diseño moderno y optimizado"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #34495e, stop:1 #2c3e50);
                border: 1px solid #34495e;
                border-radius: 8px;
                margin: 5px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(20, 15, 20, 15)

        # Título principal con espaciado optimizado
        title_label = QLabel("🧮 SIMULADOR MATEMÁTICO AVANZADO")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            color: #ecf0f1;
            font-size: 22px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
            letter-spacing: 1px;
            margin: 0px;
            padding: 6px 0px;
        """)

        layout.addWidget(title_label)

        frame.setLayout(layout)
        frame.setMaximumHeight(80)
        frame.setMinimumHeight(80)

        return frame

    def keyPressEvent(self, event):
        """Maneja atajos de teclado para mejorar la usabilidad"""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                # Ctrl+Enter: Ejecutar cálculo en la pestaña actual
                current_tab = self.tab_widget.currentWidget()
                if hasattr(current_tab, 'solve'):
                    current_tab.solve()
                event.accept()
            elif event.key() == Qt.Key.Key_R:
                # Ctrl+R: Limpiar resultados
                current_tab = self.tab_widget.currentWidget()
                if hasattr(current_tab, 'clear_results'):
                    current_tab.clear_results()
                event.accept()
        else:
            super().keyPressEvent(event)

    def apply_style(self):
        """Aplica el tema oscuro moderno a la aplicación"""
        from gui.themes import DarkTheme

        # Aplicar el stylesheet principal
        self.setStyleSheet(DarkTheme.get_main_stylesheet())

        # Configurar la paleta de colores para elementos nativos
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(DarkTheme.BACKGROUND_PRIMARY))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(DarkTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Base, QColor(DarkTheme.BACKGROUND_SECONDARY))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(DarkTheme.BACKGROUND_LIGHT))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(DarkTheme.BACKGROUND_LIGHT))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(DarkTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Text, QColor(DarkTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Button, QColor(DarkTheme.BACKGROUND_LIGHT))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(DarkTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(DarkTheme.TEXT_ACCENT))
        palette.setColor(QPalette.ColorRole.Link, QColor(DarkTheme.BUTTON_PRIMARY))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(DarkTheme.BUTTON_PRIMARY))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(DarkTheme.TEXT_PRIMARY))

        self.setPalette(palette)

    def create_credits_tab(self):
        """Crea una pestaña de créditos simplificada"""
        from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont

        credits_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        title = QLabel("📚 CRÉDITOS")
        title_font = QFont("Arial", 30, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #3498db; margin: 36px;")
        layout.addWidget(title)

        # Materia
        subject = QLabel("Materia: Modelado y Simulación")
        subject_font = QFont("Arial", 22, QFont.Weight.Bold)
        subject.setFont(subject_font)
        subject.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subject.setStyleSheet("margin: 26px;")
        layout.addWidget(subject)

        # Estudiantes
        students_title = QLabel("Estudiantes:")
        students_title_font = QFont("Arial", 22)
        students_title.setFont(students_title_font)
        students_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        students_title.setStyleSheet("margin: 31px 0 21px 0;")
        layout.addWidget(students_title)

        students = [
            "Federico Muntaabski",
            "Nicolas Llousas",
            "Santiago Oteiza"
        ]

        for student in students:
            student_label = QLabel(f"• {student}")
            student_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            student_label.setStyleSheet("margin: 14px; font-size: 21px; font-weight: bold;")
            layout.addWidget(student_label)

        # Año
        year = QLabel("2025")
        year.setAlignment(Qt.AlignmentFlag.AlignCenter)
        year.setStyleSheet("margin: 36px; color: #7f8c8d; font-size: 20px; font-weight: bold;")
        layout.addWidget(year)

        credits_widget.setLayout(layout)
        return credits_widget
