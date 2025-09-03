"""
Interfaz Gráfica Principal del Simulador Matemático
Implementa la ventana principal y todos los componentes de la GUI

Características:
- Interfaz moderna con PyQt6
- Teclado virtual para funciones matemáticas
- Pestañas para diferentes métodos numéricos
- Visualización de resultados con matplotlib
- Créditos e información del equipo
"""

import sys
from typing import Optional, Callable
import numpy as np
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
        
        # Botones de funciones matemáticas organizados en 1 columna
        buttons = [
            'sin', 'cos', 'tan', 'log', 'exp', 'sqrt', 'pi', 'e'
        ]
        
        for row, text in enumerate(buttons):
            button = QPushButton(text)
            button.setMinimumSize(26, 18)  # Botones 20% más pequeños
            button.setMaximumSize(38, 22)  # Límite máximo reducido
            button.clicked.connect(lambda checked, t=text: self.button_clicked(t))
            
            # Aplicar estilos para funciones matemáticas y constantes
            button.setStyleSheet(DarkTheme.get_keyboard_button_style("function"))
            
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

class ODETab(QWidget):
    """
    Pestaña para resolver ecuaciones diferenciales ordinarias
    """
    
    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        
        # Panel de entrada
        input_panel = QGroupBox("Ecuación Diferencial dy/dt = f(t, y)")
        input_layout = QVBoxLayout()
        
        # Función f(t, y)
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: t + y, -y + t**2, sin(t)*y")
        self.function_input.focusInEvent = lambda e: self.keyboard.set_target(self.function_input)
        input_layout.addWidget(QLabel("f(t, y):"))
        input_layout.addWidget(self.function_input)
        
        # Condiciones iniciales
        conditions_layout = QHBoxLayout()
        
        self.t0_input = QDoubleSpinBox()
        self.t0_input.setRange(-100, 100)
        self.t0_input.setValue(0)
        conditions_layout.addWidget(QLabel("t₀:"))
        conditions_layout.addWidget(self.t0_input)
        
        self.y0_input = QDoubleSpinBox()
        self.y0_input.setRange(-100, 100)
        self.y0_input.setValue(1)
        conditions_layout.addWidget(QLabel("y₀:"))
        conditions_layout.addWidget(self.y0_input)
        
        self.tf_input = QDoubleSpinBox()
        self.tf_input.setRange(-100, 100)
        self.tf_input.setValue(5)
        conditions_layout.addWidget(QLabel("tf:"))
        conditions_layout.addWidget(self.tf_input)
        
        input_layout.addLayout(conditions_layout)
        
        # Número de puntos
        self.n_points = QSpinBox()
        self.n_points.setRange(10, 1000)
        self.n_points.setValue(100)
        input_layout.addWidget(QLabel("Número de puntos:"))
        input_layout.addWidget(self.n_points)
        
        # Método
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Runge-Kutta 4 (Implementación propia)", "Runge-Kutta (SciPy)"])
        input_layout.addWidget(QLabel("Método:"))
        input_layout.addWidget(self.method_combo)
        
        # Botón resolver
        solve_button = QPushButton("Resolver EDO")
        from gui.themes import DarkTheme
        from gui.animations import ButtonHoverEffect, StatusAnimation
        solve_button.setStyleSheet(DarkTheme.get_button_style("success") + "padding: 12px;")
        solve_button.clicked.connect(self.solve_ode)
        
        # Agregar efecto de hover
        self.solve_hover_effect = ButtonHoverEffect(solve_button)
        
        input_layout.addWidget(solve_button)
        
        # Área de resultados
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        input_layout.addWidget(QLabel("Resultados:"))
        input_layout.addWidget(self.results_text)
        
        input_panel.setLayout(input_layout)
        input_panel.setMaximumWidth(350)
        
        layout.addWidget(input_panel)
        layout.addWidget(self.plot_widget)
        
        self.setLayout(layout)
    
    def solve_ode(self):
        """Resuelve la ecuación diferencial con indicadores de progreso"""
        try:
            # Iniciar indicador de progreso
            from gui.animations import ProgressIndicator, StatusAnimation
            progress = ProgressIndicator(self.parent())
            progress.start("Resolviendo EDO")
            
            # Obtener parámetros
            function_str = self.function_input.text().strip()
            if not function_str:
                progress.stop()
                QMessageBox.warning(self, "Error", "Ingrese la función f(t, y)")
                return
            
            t0 = self.t0_input.value()
            tf = self.tf_input.value()
            y0 = self.y0_input.value()
            n_points = self.n_points.value()
            
            if tf <= t0:
                progress.stop()
                QMessageBox.warning(self, "Error", "tf debe ser mayor que t0")
                return
            
            # Parsear función
            f = MathParser.parse_ode_function(function_str)
            
            # Resolver según el método seleccionado
            method = self.method_combo.currentIndex()
            
            if method == 0:  # Runge-Kutta propio
                t, y = NumericalMethods.runge_kutta_4(f, (t0, tf), y0, n_points)
                method_name = "Runge-Kutta 4 (Implementación propia)"
            else:  # SciPy
                t, y = NumericalMethods.runge_kutta_scipy(f, (t0, tf), y0, n_points)
                method_name = "Runge-Kutta (SciPy)"
            
            # Detener progreso
            progress.stop()
            
            # Mostrar resultados
            self.plot_widget.plot_ode_solution(t, y, f"Solución EDO: dy/dt = {function_str}")
            
            # Mostrar información en el área de texto
            results = f"""
Método: {method_name}
Ecuación: dy/dt = {function_str}
Condiciones: t₀={t0}, y₀={y0}, tf={tf}
Puntos calculados: {len(t)}
Valor final: y({tf:.2f}) ≈ {y[-1]:.6f}
            """.strip()
            
            self.results_text.setText(results)
            
            # Mostrar mensaje de éxito con animación
            if hasattr(self, 'parent') and hasattr(self.parent(), 'statusBar'):
                StatusAnimation.flash_success(self.parent().statusBar(), "EDO resuelta correctamente")
            
        except Exception as e:
            # Detener progreso en caso de error
            if 'progress' in locals():
                progress.stop()
            
            # Mostrar error con animación
            if hasattr(self, 'parent') and hasattr(self.parent(), 'statusBar'):
                StatusAnimation.flash_error(self.parent().statusBar(), f"Error: {str(e)}")
            
            QMessageBox.critical(self, "Error", f"Error resolviendo EDO: {str(e)}")

class RootsTab(QWidget):
    """
    Pestaña para encontrar raíces de ecuaciones
    """
    
    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()
    
    def init_ui(self):
        # Layout principal con splitter para mejor organización
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo: Controles de entrada
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Panel de entrada
        input_panel = QGroupBox("Búsqueda de Raíces")
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Función
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: x**2 - 4, sin(x) - 0.5")
        self.function_input.focusInEvent = lambda e: self.keyboard.set_target(self.function_input)
        # Aumentar tamaño para mejor visibilidad
        self.function_input.setMaximumSize(280, 35)
        self.function_input.setMinimumSize(250, 30)
        self.function_input.setStyleSheet("font-size: 14px; padding: 5px;")
        input_layout.addWidget(QLabel("Función f(x):"))
        input_layout.addWidget(self.function_input)
        
        # Método
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Bisección", "Newton-Raphson", "Punto Fijo", "Aitken"])
        self.method_combo.currentTextChanged.connect(self.on_method_changed)
        # Aumentar tamaño para mejor visibilidad
        self.method_combo.setMaximumSize(280, 35)
        self.method_combo.setMinimumSize(250, 30)
        self.method_combo.setStyleSheet("font-size: 14px; padding: 5px;")
        input_layout.addWidget(QLabel("Método:"))
        input_layout.addWidget(self.method_combo)
        
        # Parámetros específicos del método
        self.params_widget = QWidget()
        self.params_layout = QVBoxLayout()
        self.params_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.params_widget.setLayout(self.params_layout)
        input_layout.addWidget(self.params_widget)
        
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
        
        input_layout.addLayout(tolerance_layout)
        
        # Botón resolver
        solve_button = QPushButton("Encontrar Raíz")
        from gui.themes import DarkTheme
        solve_button.setStyleSheet(DarkTheme.get_button_style("warning") + "padding: 12px;")
        solve_button.clicked.connect(self.find_root)
        input_layout.addWidget(solve_button)
        
        # Área de resultados
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        input_layout.addWidget(QLabel("Resultados:"))
        input_layout.addWidget(self.results_text)
        
        input_panel.setLayout(input_layout)
        input_panel.setMaximumWidth(420)
        input_panel.setMinimumWidth(380)
        
        left_layout.addWidget(input_panel)
        left_panel.setLayout(left_layout)
        
        # Panel derecho: Tabla y gráfico
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Tabla de resultados detallados
        table_panel = QGroupBox("Tabla de Iteraciones")
        table_layout = QVBoxLayout()
        self.results_table = QTableWidget()
        self.results_table.setMaximumHeight(400)  # Aumentar altura para mejor visibilidad
        table_layout.addWidget(self.results_table)
        table_panel.setLayout(table_layout)
        
        right_layout.addWidget(table_panel)
        right_layout.addWidget(self.plot_widget)
        
        right_panel.setLayout(right_layout)
        
        # Agregar paneles al splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([400, 800])  # Tamaños iniciales
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)
        
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
    
    def find_root(self):
        """Encuentra la raíz usando el método seleccionado"""
        try:
            function_str = self.function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese la función f(x)")
                return
            
            f = MathParser.parse_function(function_str)
            method = self.method_combo.currentText()
            
            # Convertir valores de texto a números
            try:
                tol = float(self.tolerance_input.text())
                max_iter = int(self.max_iter_input.text())
            except ValueError:
                QMessageBox.warning(self, "Error", "Tolerancia y máximo de iteraciones deben ser números válidos")
                return
            
            if method == "Bisección":
                try:
                    a = float(self.a_input.text())
                    b = float(self.b_input.text())
                except ValueError:
                    QMessageBox.warning(self, "Error", "Los valores de a y b deben ser números válidos")
                    return
                
                if a >= b:
                    QMessageBox.warning(self, "Error", "a debe ser menor que b")
                    return
                
                root, iterations, history = NumericalMethods.bisection_method(f, a, b, tol, max_iter)
                
                # Graficar función y convergencia
                self.plot_function_and_convergence(f, function_str, history, root, method, a, b)
                
                results = f"""
Método: Bisección
Función: f(x) = {function_str}
Intervalo inicial: [{a}, {b}]
Raíz encontrada: x ≈ {root:.8f}
f(x) ≈ {f(root):.2e}
Iteraciones: {iterations}
Tolerancia: {tol:.2e}
                """.strip()
                
                # Llenar tabla con detalles de iteraciones
                self.populate_results_table(history, root, f, method)
                self.results_text.setText(results)
                
            elif method == "Newton-Raphson":
                derivative_str = self.derivative_input.text().strip()
                if not derivative_str:
                    QMessageBox.warning(self, "Error", "Ingrese la derivada f'(x)")
                    return
                
                df = MathParser.parse_function(derivative_str)
                try:
                    x0 = float(self.x0_input.text())
                except ValueError:
                    QMessageBox.warning(self, "Error", "La aproximación inicial debe ser un número válido")
                    return
                
                root, iterations, history = NumericalMethods.newton_raphson_method(f, df, x0, tol, max_iter)
                
                # Graficar función y convergencia
                self.plot_function_and_convergence(f, function_str, history, root, method, x0=x0)
                
                results = f"""
Método: Newton-Raphson
Función: f(x) = {function_str}
Derivada: f'(x) = {derivative_str}
Aproximación inicial: x₀ = {x0}
Raíz encontrada: x ≈ {root:.8f}
f(x) ≈ {f(root):.2e}
Iteraciones: {iterations}
Tolerancia: {tol:.2e}
                """.strip()
                
                # Llenar tabla con detalles de iteraciones
                self.populate_results_table(history, root, f, method)
                self.results_text.setText(results)
                
            elif method == "Punto Fijo":
                g_str = self.g_function_input.text().strip()
                if not g_str:
                    QMessageBox.warning(self, "Error", "Ingrese la función g(x)")
                    return
                
                g = MathParser.parse_function(g_str)
                try:
                    x0 = float(self.x0_input.text())
                except ValueError:
                    QMessageBox.warning(self, "Error", "La aproximación inicial debe ser un número válido")
                    return
                
                root, iterations, history = NumericalMethods.fixed_point_method(g, x0, tol, max_iter)
                
                # Graficar función y convergencia
                self.plot_function_and_convergence(f, function_str, history, root, method, x0=x0, g_function=g_str)
                
                results = f"""
Método: Punto Fijo
Función original: f(x) = {function_str}
Función de iteración: g(x) = {g_str}
Aproximación inicial: x₀ = {x0}
Punto fijo encontrado: x ≈ {root:.8f}
g(x) ≈ {g(root):.8f}
Iteraciones: {iterations}
Tolerancia: {tol:.2e}
                """.strip()
                
                # Llenar tabla con detalles de iteraciones
                self.populate_results_table(history, root, f, method)
                self.results_text.setText(results)
                
            elif method == "Aitken":
                g_str = self.g_function_input.text().strip()
                if not g_str:
                    QMessageBox.warning(self, "Error", "Ingrese la función g(x)")
                    return
                
                g = MathParser.parse_function(g_str)
                try:
                    x0 = float(self.x0_input.text())
                except ValueError:
                    QMessageBox.warning(self, "Error", "La aproximación inicial debe ser un número válido")
                    return
                
                root, iterations, history, accelerated_history, detailed_steps = NumericalMethods.aitken_method(g, x0, tol, max_iter)

                # Graficar función y convergencia
                self.plot_function_and_convergence(f, function_str, history, root, method, x0=x0, g_function=g_str)
                
                results = f"""
Método: Aitken (Acelerado)
Función original: f(x) = {function_str}
Función de iteración: g(x) = {g_str}
Aproximación inicial: x₀ = {x0}
Raíz encontrada: x ≈ {root:.8f}
g(x) ≈ {g(root):.8f}
Iteraciones: {iterations}
Tolerancia: {tol:.2e}
Nota: Método con aceleración de convergencia
                """.strip()
                
                # Llenar tabla con detalles de iteraciones
                self.populate_results_table(history, root, f, method, detailed_steps=detailed_steps)
                self.results_text.setText(results)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error encontrando raíz: {str(e)}")
    
    def populate_results_table(self, history, root, f, method, detailed_steps=None):
        """Llena la tabla con los detalles de las iteraciones"""
        if not history:
            return

        # Para Aitken, usar información detallada si está disponible
        if method == "Aitken" and detailed_steps:
            self._populate_aitken_table(detailed_steps, root, f)
            return

        # Configuración normal para otros métodos
        num_rows = len(history)
        self.results_table.setRowCount(num_rows)
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            'Iteración', 'xᵢ', 'f(xᵢ)', 'Error Absoluto', 'Error Relativo (%)'
        ])
        
        # Llenar tabla con datos de cada iteración
        for i, x_i in enumerate(history):
            f_x_i = f(x_i)
            abs_error = abs(x_i - root) if i < len(history) - 1 else abs(f_x_i)  # Error absoluto
            rel_error = abs_error / abs(root) if root != 0 else abs_error  # Error relativo
            
            self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.results_table.setItem(i, 1, QTableWidgetItem(f"{x_i:.8f}"))
            self.results_table.setItem(i, 2, QTableWidgetItem(f"{f_x_i:.6f}"))
            self.results_table.setItem(i, 3, QTableWidgetItem(self._format_error(abs_error, False)))
            self.results_table.setItem(i, 4, QTableWidgetItem(self._format_error(rel_error, True)))
        
        # Ajustar columnas al contenido
        self.results_table.resizeColumnsToContents()
        self.results_table.setMaximumHeight(400)  # Aumentar altura para mejor visibilidad
    
    def _format_error(self, error_value, is_relative=False):
        """
        Formatea un error para que sea más fácil de entender
        
        Args:
            error_value: Valor del error
            is_relative: Si es error relativo (se multiplica por 100)
            
        Returns:
            str: Error formateado de manera amigable
        """
        if error_value is None:
            return "-"
        
        # Convertir a porcentaje si es error relativo
        if is_relative:
            error_value = error_value * 100
        
        # Casos especiales para errores muy pequeños
        if abs(error_value) < 1e-12:
            return "≈ 0 (Convergente)" if not is_relative else "≈ 0% (Convergente)"
        elif abs(error_value) < 1e-8:
            return f"{error_value:.2e}" if not is_relative else f"{error_value:.2e}%"
        elif abs(error_value) < 1e-4:
            return f"{error_value:.6f}" if not is_relative else f"{error_value:.4f}%"
        elif abs(error_value) < 1e-2:
            return f"{error_value:.4f}" if not is_relative else f"{error_value:.2f}%"
        else:
            # Para errores grandes, usar notación científica
            return f"{error_value:.2e}" if not is_relative else f"{error_value:.2e}%"
    
    def _populate_aitken_table(self, detailed_steps, root, f):
        """Llena la tabla con información detallada del método de Aitken"""
        if not detailed_steps:
            return
        
        # Configurar tabla para Aitken con más columnas
        num_rows = len(detailed_steps)
        self.results_table.setRowCount(num_rows)
        self.results_table.setColumnCount(7)
        self.results_table.setHorizontalHeaderLabels([
            'Iter', 'x₍ᵢ₋₁₎', 'g(x₍ᵢ₋₁₎)', 'x₀,x₁,x₂', 'x*_acelerado', 'Error Abs', 'Error Rel'
        ])
        
        # Llenar tabla con datos detallados de cada paso
        for i, step in enumerate(detailed_steps):
            iter_num = step['iteracion']
            x_anterior = step['x_anterior']
            g_x_anterior = step['g_x_anterior']
            
            # Formatear x0,x1,x2 si existe
            x0_x1_x2 = ""
            if step['x0_x1_x2']:
                x0_x1_x2 = f"[{step['x0_x1_x2'][0]:.4f}, {step['x0_x1_x2'][1]:.4f}, {step['x0_x1_x2'][2]:.4f}]"
            
            # Valor acelerado
            x_acelerado = f"{step['x_acelerado']:.8f}" if step['x_acelerado'] is not None else "-"
            
            # Errores
            error_abs = self._format_error(step['error_abs'], False) if step['error_abs'] is not None else "-"
            error_rel = self._format_error(step['error_rel'], True) if step['error_rel'] is not None else "-"
            
            self.results_table.setItem(i, 0, QTableWidgetItem(str(iter_num)))
            self.results_table.setItem(i, 1, QTableWidgetItem(f"{x_anterior:.8f}"))
            self.results_table.setItem(i, 2, QTableWidgetItem(f"{g_x_anterior:.8f}"))
            self.results_table.setItem(i, 3, QTableWidgetItem(x0_x1_x2))
            self.results_table.setItem(i, 4, QTableWidgetItem(x_acelerado))
            self.results_table.setItem(i, 5, QTableWidgetItem(error_abs))
            self.results_table.setItem(i, 6, QTableWidgetItem(error_rel))
        
        # Ajustar columnas al contenido
        self.results_table.resizeColumnsToContents()
        self.results_table.setMaximumHeight(400)
    
    def plot_function_and_convergence(self, f, function_str, history, root, method, a=None, b=None, x0=None, g_function=None):
        """Grafica la función, el proceso de convergencia y elementos visuales mejorados con raíces finales detalladas"""
        try:
            # Crear figura con subplots mejorados
            self.plot_widget.figure.clear()

            # Calcular estadísticas de convergencia
            f_root = f(root)
            convergence_rate = 0
            if len(history) > 2:
                errors = [abs(x - root) for x in history[:-1]]  # Errores de las aproximaciones
                if len(errors) > 1:
                    convergence_rate = errors[-1] / errors[-2] if errors[-2] != 0 else 0

            if method == "Bisección":
                # Crear figura con 3 subplots para análisis completo
                gs = self.plot_widget.figure.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
                
                # Subplot 1: Función con intervalo y raíz detallada (ocupa fila completa superior)
                ax1 = self.plot_widget.figure.add_subplot(gs[0, :])
                x_vals = np.linspace(a - 2, b + 2, 1500)
                y_vals = [f(x) for x in x_vals]

                # Graficar función
                ax1.plot(x_vals, y_vals, 'b-', linewidth=2.5, label=f'f(x) = {function_str}')

                # Ejes de referencia
                ax1.axhline(y=0, color='k', linestyle='-', alpha=0.8, linewidth=1.5, label='Eje X')
                ax1.axvline(x=0, color='k', linestyle='--', alpha=0.5, label='Eje Y')

                # Área del intervalo inicial
                ax1.fill_betweenx([-max(abs(y) for y in y_vals)*1.5, max(abs(y) for y in y_vals)*1.5],
                                 a, b, alpha=0.15, color='lightblue', label='Intervalo inicial [a,b]')

                # Puntos iniciales
                ax1.scatter([a, b], [f(a), f(b)], color='darkorange', s=80, zorder=6,
                           marker='s', label=f'Puntos iniciales\na={a:.3f}, b={b:.3f}')

                # Raíz final con detalles
                ax1.scatter([root], [f_root], color='red', s=120, zorder=7,
                           marker='*', edgecolors='darkred', linewidth=2,
                           label=f'Raíz Final\nx = {root:.6f}\nf(x) = {f_root:.2e}')

                # Línea vertical de la raíz
                ax1.axvline(x=root, color='red', linestyle='--', linewidth=2, alpha=0.7)

                ax1.set_xlabel('x', fontsize=11, fontweight='bold')
                ax1.set_ylabel('f(x)', fontsize=11, fontweight='bold')
                ax1.set_title(f'📊 Función y Raíz Final - Método {method}', fontsize=12, fontweight='bold', pad=20)
                ax1.grid(True, alpha=0.3)
                ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)

                # Subplot 2: Convergencia de aproximaciones
                ax2 = self.plot_widget.figure.add_subplot(gs[1, 0])
                ax2.plot(range(len(history)), history, 'ro-', linewidth=2.5, markersize=8,
                        markerfacecolor='red', markeredgecolor='darkred', markeredgewidth=1.5,
                        label='Aproximaciones del método')
                ax2.axhline(y=root, color='green', linestyle='-', linewidth=2.5,
                           label=f'Raíz exacta: {root:.6f}')
                ax2.scatter(range(len(history)), history, color='red', s=60, zorder=5, alpha=0.8)
                ax2.set_xlabel('Iteración', fontsize=10, fontweight='bold')
                ax2.set_ylabel('Valor de x', fontsize=10, fontweight='bold')
                ax2.set_title('📈 Convergencia', fontsize=11, fontweight='bold')
                ax2.grid(True, alpha=0.3)
                ax2.legend(fontsize=8)

                # Subplot 3: Análisis de errores
                ax3 = self.plot_widget.figure.add_subplot(gs[1, 1])
                errors = [abs(x - root) for x in history]
                ax3.semilogy(range(len(errors)), errors, 'bo-', linewidth=2, markersize=6,
                            markerfacecolor='blue', markeredgecolor='navy', markeredgewidth=1,
                            label='Error absoluto')
                ax3.set_xlabel('Iteración', fontsize=10, fontweight='bold')
                ax3.set_ylabel('Error |x - x*|', fontsize=10, fontweight='bold')
                ax3.set_title('� Análisis de Errores', fontsize=11, fontweight='bold')
                ax3.grid(True, alpha=0.3)
                ax3.legend(fontsize=8)

                # Información detallada en el subplot de errores
                error_info = f'📊 ANÁLISIS COMPLETO\n\n'
                error_info += f'Iteraciones: {len(history)}\n'
                error_info += f'Raíz: {root:.8f}\n'
                error_info += f'Error final: {errors[-1]:.2e}\n'
                if len(errors) > 1 and errors[0] != 0:
                    reduction_factor = errors[-1] / errors[0]
                    error_info += f'Reducción total: {reduction_factor:.2e}\n'
                error_info += f'f(raíz): {f_root:.2e}'

                ax3.text(0.02, 0.98, error_info, transform=ax3.transAxes,
                        fontsize=8, verticalalignment='top',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.9))
                
            else:  # Newton-Raphson, Punto Fijo o Aitken
                # Crear figura con 3 subplots para análisis completo
                gs = self.plot_widget.figure.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
                
                # Subplot 1: Función con aproximaciones detalladas (ocupa fila completa superior)
                ax1 = self.plot_widget.figure.add_subplot(gs[0, :])
                x_range = 6 if method == "Aitken" else 4
                x_vals = np.linspace(x0 - x_range, x0 + x_range, 1500)
                y_vals = [f(x) for x in x_vals]

                # Graficar función con mejor estilo
                ax1.plot(x_vals, y_vals, 'b-', linewidth=2.5, label=f'f(x) = {function_str}')

                # Ejes de referencia
                ax1.axhline(y=0, color='k', linestyle='-', alpha=0.8, linewidth=1.5, label='Eje X')
                ax1.axvline(x=0, color='k', linestyle='--', alpha=0.5, label='Eje Y')

                # Raíz final con detalles mejorados
                ax1.scatter([root], [f_root], color='red', s=150, zorder=7,
                           marker='*', edgecolors='darkred', linewidth=3,
                           label=f'Raíz Final\nx = {root:.6f}\nf(x) = {f_root:.2e}')

                # Línea vertical de la raíz
                ax1.axvline(x=root, color='red', linestyle='--', linewidth=2.5, alpha=0.8)

                # Punto inicial
                ax1.scatter([x0], [f(x0)], color='purple', s=120, marker='D', zorder=6,
                           edgecolors='darkviolet', linewidth=2,
                           label=f'Punto Inicial\nx₀ = {x0:.3f}\nf(x₀) = {f(x0):.2e}')

                # Mostrar trayectoria de aproximaciones
                if len(history) > 1:
                    # Conectar aproximaciones con líneas curvas
                    ax1.plot(history, [f(x) for x in history], 'go-', alpha=0.7,
                            linewidth=2, markersize=8, markerfacecolor='green',
                            markeredgecolor='darkgreen', markeredgewidth=1.5,
                            label='Trayectoria de aproximaciones')

                    # Agregar flechas para mostrar dirección (máximo 6 para no sobrecargar)
                    for i in range(min(len(history)-1, 6)):
                        if i < len(history)-1:
                            dx = history[i+1] - history[i]
                            dy = f(history[i+1]) - f(history[i])
                            if abs(dx) > 1e-10:  # Evitar flechas demasiado pequeñas
                                ax1.arrow(history[i], f(history[i]), dx*0.8, dy*0.8,
                                         head_width=0.15, head_length=0.15, fc='green', ec='green',
                                         alpha=0.6, linewidth=1)

                ax1.set_xlabel('x', fontsize=11, fontweight='bold')
                ax1.set_ylabel('f(x)', fontsize=11, fontweight='bold')

                # Título específico por método
                if method == "Aitken":
                    title = f'🚀 Función y Raíz Final - Método {method} (Acelerado)'
                    if g_function:
                        title += f'\nFunción g(x): {g_function}'
                    ax1.text(0.02, 0.98, '⚡ ACELERACIÓN AITKEN ACTIVA',
                            transform=ax1.transAxes, fontsize=10, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
                elif method == "Newton-Raphson":
                    title = f'🎯 Función y Raíz Final - Método {method}'
                    if g_function:
                        title += f'\nDerivada f\'(x): {g_function}'
                else:  # Punto Fijo
                    title = f'🔄 Función y Raíz Final - Método {method}'
                    if g_function:
                        title += f'\nFunción g(x): {g_function}'

                ax1.set_title(title, fontsize=12, fontweight='bold', pad=20)
                ax1.grid(True, alpha=0.3)
                ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)

                # Subplot 2: Análisis de convergencia mejorado
                ax2 = self.plot_widget.figure.add_subplot(gs[1, 0])

                # Graficar aproximaciones con mejor estilo
                ax2.plot(range(len(history)), history, 'ro-', linewidth=2.5, markersize=8,
                        markerfacecolor='red', markeredgecolor='darkred', markeredgewidth=1.5,
                        label='Aproximaciones del método')

                # Línea de la raíz exacta
                ax2.axhline(y=root, color='green', linestyle='-', linewidth=2.5,
                           label=f'Raíz exacta: {root:.6f}')

                # Agregar puntos destacados
                ax2.scatter(range(len(history)), history, color='red', s=60, zorder=5, alpha=0.8)

                ax2.set_xlabel('Iteración', fontsize=10, fontweight='bold')
                ax2.set_ylabel('Valor de x', fontsize=10, fontweight='bold')
                ax2.set_title('📈 Convergencia', fontsize=11, fontweight='bold')
                ax2.grid(True, alpha=0.3)
                ax2.legend(fontsize=8)

                # Subplot 3: Análisis detallado de errores y estadísticas
                ax3 = self.plot_widget.figure.add_subplot(gs[1, 1])

                # Calcular errores
                errors = [abs(x - root) for x in history]
                
                # Graficar errores en escala logarítmica
                if len(errors) > 0 and max(errors) > 0:
                    ax3.semilogy(range(len(errors)), errors, 'bo-', linewidth=2, markersize=6,
                                markerfacecolor='blue', markeredgecolor='navy', markeredgewidth=1,
                                label='Error absoluto')
                
                ax3.set_xlabel('Iteración', fontsize=10, fontweight='bold')
                ax3.set_ylabel('Error |x - x*|', fontsize=10, fontweight='bold')
                ax3.set_title('🔍 Análisis de Errores', fontsize=11, fontweight='bold')
                ax3.grid(True, alpha=0.3)
                ax3.legend(fontsize=8)

                # Calcular y mostrar estadísticas detalladas de convergencia
                convergence_info = f'📊 ANÁLISIS COMPLETO\n\n'
                convergence_info += f'Iteraciones: {len(history)}\n'
                convergence_info += f'Raíz: {root:.8f}\n'
                convergence_info += f'f(raíz): {f_root:.2e}\n'
                
                if len(errors) > 0:
                    convergence_info += f'Error final: {errors[-1]:.2e}\n'
                
                # Calcular tasa de convergencia promedio
                if len(errors) > 2:
                    rates = []
                    for i in range(1, len(errors)):
                        if errors[i-1] != 0:
                            rate = errors[i] / errors[i-1]
                            if rate > 0:  # Solo tasas positivas
                                rates.append(rate)
                    
                    if rates:
                        avg_rate = np.mean(rates)
                        convergence_info += f'Tasa prom.: {avg_rate:.4f}\n'
                        
                        if avg_rate < 0.5:
                            convergence_info += '🚀 Convergencia rápida\n'
                        elif avg_rate < 1:
                            convergence_info += '✅ Convergencia lineal\n'
                        else:
                            convergence_info += '⚠️  Posible divergencia\n'
                    
                    # Calcular orden de convergencia aproximado
                    if len(rates) > 2:
                        order = -np.log(rates[-1]) / np.log(rates[-2]) if rates[-2] > 0 else 0
                        if 0 < order < 5:  # Rango razonable
                            convergence_info += f'Orden ≈ {order:.2f}\n'

                # Agregar información específica del método
                if method == "Newton-Raphson":
                    convergence_info += '\n🎯 Método cuadrático teórico'
                    if len(errors) > 2:
                        convergence_info += '\n(Orden 2 esperado)'
                elif method == "Aitken":
                    convergence_info += '\n🚀 Con aceleración Δ²'
                    if len(errors) > 2:
                        convergence_info += '\n(Mayor velocidad)'
                elif method == "Punto Fijo":
                    convergence_info += '\n🔄 Método iterativo'
                    if g_function:
                        convergence_info += '\n(g(x) definida)'

                ax3.text(0.02, 0.98, convergence_info, transform=ax3.transAxes,
                        fontsize=7.5, verticalalignment='top', fontfamily='monospace',
                        bbox=dict(boxstyle='round,pad=0.6', facecolor='lightcyan', alpha=0.9))

            # Ajustar layout y mostrar
            self.plot_widget.figure.tight_layout()
            self.plot_widget.canvas.draw()

        except Exception as e:
            # Si hay error en la graficación avanzada, mostrar versión simplificada pero informativa
            print(f"Error en graficación avanzada: {e}")
            try:
                self.plot_widget.figure.clear()
                
                # Crear layout con 2 subplots para versión simplificada
                ax1 = self.plot_widget.figure.add_subplot(211)
                ax2 = self.plot_widget.figure.add_subplot(212)
                
                # Subplot 1: Función básica
                if method == "Bisección" and 'a' in locals() and 'b' in locals():
                    x_vals = np.linspace(a - 1, b + 1, 500)
                else:
                    x_range = 4
                    x_vals = np.linspace(x0 - x_range, x0 + x_range, 500) if 'x0' in locals() else np.linspace(-5, 5, 500)
                
                try:
                    y_vals = [f(x) for x in x_vals]
                    ax1.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {function_str}')
                    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.7)
                    ax1.scatter([root], [f(root)], color='red', s=100, marker='*', 
                               label=f'Raíz: {root:.4f}')
                    ax1.set_title(f'Función y Raíz - {method}', fontsize=12, fontweight='bold')
                    ax1.grid(True, alpha=0.3)
                    ax1.legend()
                except:
                    ax1.text(0.5, 0.5, f'Error al graficar función\nRaíz aproximada: {root:.4f}', 
                            ha='center', va='center', transform=ax1.transAxes,
                            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
                    ax1.set_title(f'Resultado - {method}', fontsize=12, fontweight='bold')
                
                # Subplot 2: Convergencia simplificada
                ax2.plot(range(len(history)), history, 'ro-', linewidth=2, markersize=6, 
                        label='Aproximaciones')
                ax2.axhline(y=root, color='g', linestyle='--', linewidth=2, 
                           label=f'Raíz: {root:.4f}')
                ax2.set_xlabel('Iteración')
                ax2.set_ylabel('Valor de x')
                ax2.set_title(f'Convergencia - {method}', fontsize=12, fontweight='bold')
                ax2.grid(True, alpha=0.3)
                ax2.legend()
                
                # Agregar información básica
                info_text = f'Método: {method}\nIteraciones: {len(history)}\nRaíz: {root:.6f}'
                if 'f_root' in locals():
                    info_text += f'\nf(raíz): {f_root:.2e}'
                
                ax2.text(0.02, 0.98, info_text, transform=ax2.transAxes,
                        fontsize=9, verticalalignment='top',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))
                
                self.plot_widget.figure.tight_layout()
                self.plot_widget.canvas.draw()
                
            except Exception as e2:
                print(f"Error incluso en graficación simplificada: {e2}")
                # Último recurso: mostrar solo texto informativo
                try:
                    self.plot_widget.figure.clear()
                    ax = self.plot_widget.figure.add_subplot(111)
                    ax.text(0.5, 0.5, 
                           f'📊 RESULTADOS DEL MÉTODO {method.upper()}\n\n' +
                           f'Raíz encontrada: {root:.6f}\n' +
                           f'Iteraciones realizadas: {len(history)}\n' +
                           f'Última aproximación: {history[-1]:.6f}\n\n' +
                           f'Error en graficación: Revisa la función f(x)',
                           ha='center', va='center', transform=ax.transAxes,
                           fontsize=12, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
                    ax.set_title('Resultado del Cálculo', fontsize=14, fontweight='bold')
                    ax.axis('off')
                    self.plot_widget.figure.tight_layout()
                    self.plot_widget.canvas.draw()
                except Exception as e3:
                    print(f"Error crítico en visualización: {e3}")
                    # Si todo falla, al menos mostrar en consola
                    print(f"\n{'='*50}")
                    print(f"RESULTADO DEL MÉTODO {method.upper()}")
                    print(f"{'='*50}")
                    print(f"Raíz encontrada: {root:.6f}")
                    print(f"Iteraciones: {len(history)}")
                    print(f"Historial: {history}")
                    print(f"{'='*50}\n")

class IntegrationTab(QWidget):
    """
    Pestaña para integración numérica
    """
    
    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        
        # Panel de entrada
        input_panel = QGroupBox("Integración Numérica")
        input_layout = QVBoxLayout()
        
        # Función
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: x**2, sin(x), exp(-x**2)")
        self.function_input.focusInEvent = lambda e: self.keyboard.set_target(self.function_input)
        input_layout.addWidget(QLabel("Función f(x):"))
        input_layout.addWidget(self.function_input)
        
        # Límites de integración
        limits_layout = QHBoxLayout()
        
        self.a_input = QDoubleSpinBox()
        self.a_input.setRange(-100, 100)
        self.a_input.setValue(0)
        limits_layout.addWidget(QLabel("a:"))
        limits_layout.addWidget(self.a_input)
        
        self.b_input = QDoubleSpinBox()
        self.b_input.setRange(-100, 100)
        self.b_input.setValue(1)
        limits_layout.addWidget(QLabel("b:"))
        limits_layout.addWidget(self.b_input)
        
        input_layout.addLayout(limits_layout)
        
        # Número de subdivisiones
        self.n_input = QSpinBox()
        self.n_input.setRange(2, 1000)
        self.n_input.setValue(100)
        input_layout.addWidget(QLabel("Subdivisiones (n):"))
        input_layout.addWidget(self.n_input)
        
        # Botón calcular
        calc_button = QPushButton("Calcular Integral")
        from gui.themes import DarkTheme
        calc_button.setStyleSheet(DarkTheme.get_button_style("info") + "padding: 12px;")
        calc_button.clicked.connect(self.calculate_integral)
        input_layout.addWidget(calc_button)
        
        # Área de resultados
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        input_layout.addWidget(QLabel("Resultados:"))
        input_layout.addWidget(self.results_text)
        
        input_panel.setLayout(input_layout)
        input_panel.setMaximumWidth(350)
        
        layout.addWidget(input_panel)
        layout.addWidget(self.plot_widget)
        
        self.setLayout(layout)
    
    def calculate_integral(self):
        """Calcula la integral numérica"""
        try:
            function_str = self.function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese la función f(x)")
                return
            
            f = MathParser.parse_function(function_str)
            a = self.a_input.value()
            b = self.b_input.value()
            n = self.n_input.value()
            
            if a >= b:
                QMessageBox.warning(self, "Error", "a debe ser menor que b")
                return
            
            # Calcular integral
            integral_value = NumericalMethods.newton_cotes_integration(f, a, b, n)
            
            # Graficar la función y el área bajo la curva
            x = np.linspace(a, b, 200)
            y = [f(xi) for xi in x]
            
            self.plot_widget.figure.clear()
            ax = self.plot_widget.figure.add_subplot(111)
            ax.plot(x, y, 'b-', linewidth=2, label=f'f(x) = {function_str}')
            ax.fill_between(x, y, alpha=0.3, label=f'Área = {integral_value:.6f}')
            ax.set_title(f'Integración Numérica: ∫ {function_str} dx')
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.grid(True, alpha=0.3)
            ax.legend()
            self.plot_widget.canvas.draw()
            
            # Mostrar resultados
            results = f"""
Método: Newton-Cotes (Simpson 1/3)
Función: f(x) = {function_str}
Límites: [{a}, {b}]
Subdivisiones: {n}
Integral ≈ {integral_value:.8f}
            """.strip()
            
            self.results_text.setText(results)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error calculando integral: {str(e)}")

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
        self.ode_tab = ODETab(self.keyboard, self.plot_widget)
        self.roots_tab = RootsTab(self.keyboard, self.plot_widget)
        self.integration_tab = IntegrationTab(self.keyboard, self.plot_widget)
        
        # Importar pestañas avanzadas
        try:
            from gui.advanced_tabs import InterpolationTab, DerivativesTab
            
            self.interpolation_tab = InterpolationTab(self.keyboard, self.plot_widget)
            self.derivatives_tab = DerivativesTab(self.keyboard, self.plot_widget)
            
            self.tab_widget.addTab(self.roots_tab, "🎯 Búsqueda de Raíces")
            self.tab_widget.addTab(self.ode_tab, "📈 Ecuaciones Diferenciales")
            self.tab_widget.addTab(self.integration_tab, "∫ Integración")
            self.tab_widget.addTab(self.interpolation_tab, "📊 Interpolación")
            self.tab_widget.addTab(self.derivatives_tab, "🔢 Derivadas")
        except ImportError as e:
            # Si no se pueden importar las pestañas avanzadas, usar solo las básicas
            print(f"Warning: No se pudieron cargar pestañas avanzadas: {e}")
            self.tab_widget.addTab(self.roots_tab, "🎯 Búsqueda de Raíces")
            self.tab_widget.addTab(self.ode_tab, "📈 Ecuaciones Diferenciales")
            self.tab_widget.addTab(self.integration_tab, "∫ Integración")
            
            # Intentar cargar interpolación y derivadas por separado
            try:
                from gui.advanced_tabs import InterpolationTab
                self.interpolation_tab = InterpolationTab(self.keyboard, self.plot_widget)
                self.tab_widget.addTab(self.interpolation_tab, "📊 Interpolación")
            except ImportError:
                pass
                
            try:
                from gui.advanced_tabs import DerivativesTab
                self.derivatives_tab = DerivativesTab(self.keyboard, self.plot_widget)
                self.tab_widget.addTab(self.derivatives_tab, "🔢 Derivadas")
            except ImportError:
                pass
        
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MathSimulatorApp()
    window.show()
    sys.exit(app.exec())
