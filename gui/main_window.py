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
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLineEdit, QLabel, QTextEdit, QGridLayout,
    QGroupBox, QSpinBox, QDoubleSpinBox, QComboBox, QSplitter,
    QMessageBox, QProgressBar, QStatusBar, QScrollArea,
    QFrame, QApplication
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
        layout.setSpacing(6)  # Espaciado entre botones
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Importar tema una vez para eficiencia
        from gui.themes import DarkTheme
        
        # Botones de funciones matemáticas únicamente con mejor organización
        buttons = [
            # Fila 1: Funciones trigonométricas básicas
            ['sin', 'cos', 'tan', 'Clear'],
            # Fila 2: Funciones exponenciales y logarítmicas  
            ['exp', 'log', 'sqrt', '+'],
            # Fila 3: Constantes matemáticas y operadores
            ['pi', 'e', '^', '-'],
            # Fila 4: Operadores aritméticos básicos
            ['*', '/', '.', '='],
        ]
        
        for row, button_row in enumerate(buttons):
            for col, text in enumerate(button_row):
                button = QPushButton(text)
                button.setMinimumSize(80, 50)  # Botones más grandes
                button.setMaximumSize(120, 60)  # Límite máximo
                button.clicked.connect(lambda checked, t=text: self.button_clicked(t))
                
                # Aplicar estilos según el tipo de botón (optimizado)
                if text == 'Clear':
                    button.setStyleSheet(DarkTheme.get_keyboard_button_style("clear"))
                elif text in ['+', '-', '*', '/', '^', '=', '.']:
                    button.setStyleSheet(DarkTheme.get_keyboard_button_style("operator"))
                else:  # Funciones matemáticas y constantes
                    button.setStyleSheet(DarkTheme.get_keyboard_button_style("function"))
                
                layout.addWidget(button, row, col)
        
        self.setLayout(layout)
    
    def set_target(self, target_widget):
        """Establece el widget de destino para el teclado"""
        self.current_target = target_widget
    
    def button_clicked(self, text):
        """Maneja los clics en los botones del teclado"""
        if not self.current_target:
            return
        
        if text == 'Clear':
            self.current_target.clear()
        else:
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
        layout = QHBoxLayout()
        
        # Panel de entrada
        input_panel = QGroupBox("Búsqueda de Raíces")
        input_layout = QVBoxLayout()
        
        # Función
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: x**2 - 4, sin(x) - 0.5")
        self.function_input.focusInEvent = lambda e: self.keyboard.set_target(self.function_input)
        input_layout.addWidget(QLabel("Función f(x):"))
        input_layout.addWidget(self.function_input)
        
        # Método
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Bisección", "Newton-Raphson", "Punto Fijo"])
        self.method_combo.currentTextChanged.connect(self.on_method_changed)
        input_layout.addWidget(QLabel("Método:"))
        input_layout.addWidget(self.method_combo)
        
        # Parámetros específicos del método
        self.params_widget = QWidget()
        self.params_layout = QVBoxLayout()
        self.params_widget.setLayout(self.params_layout)
        input_layout.addWidget(self.params_widget)
        
        # Tolerancia e iteraciones
        tolerance_layout = QHBoxLayout()
        self.tolerance_input = QDoubleSpinBox()
        self.tolerance_input.setRange(1e-12, 1e-2)
        self.tolerance_input.setValue(1e-6)
        self.tolerance_input.setDecimals(10)
        tolerance_layout.addWidget(QLabel("Tolerancia:"))
        tolerance_layout.addWidget(self.tolerance_input)
        
        self.max_iter_input = QSpinBox()
        self.max_iter_input.setRange(10, 1000)
        self.max_iter_input.setValue(100)
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
        self.results_text.setMaximumHeight(200)
        input_layout.addWidget(QLabel("Resultados:"))
        input_layout.addWidget(self.results_text)
        
        input_panel.setLayout(input_layout)
        input_panel.setMaximumWidth(350)
        
        layout.addWidget(input_panel)
        layout.addWidget(self.plot_widget)
        
        self.setLayout(layout)
        
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
            
            self.a_input = QDoubleSpinBox()
            self.a_input.setRange(-100, 100)
            self.a_input.setValue(-5)
            interval_layout.addWidget(QLabel("a:"))
            interval_layout.addWidget(self.a_input)
            
            self.b_input = QDoubleSpinBox()
            self.b_input.setRange(-100, 100)
            self.b_input.setValue(5)
            interval_layout.addWidget(QLabel("b:"))
            interval_layout.addWidget(self.b_input)
            
            interval_widget = QWidget()
            interval_widget.setLayout(interval_layout)
            self.params_layout.addWidget(QLabel("Intervalo [a, b]:"))
            self.params_layout.addWidget(interval_widget)
            
        elif method == "Newton-Raphson":
            # Aproximación inicial y derivada
            self.x0_input = QDoubleSpinBox()
            self.x0_input.setRange(-100, 100)
            self.x0_input.setValue(1)
            self.params_layout.addWidget(QLabel("Aproximación inicial x₀:"))
            self.params_layout.addWidget(self.x0_input)
            
            self.derivative_input = QLineEdit()
            self.derivative_input.setPlaceholderText("Ej: 2*x, cos(x)")
            self.derivative_input.focusInEvent = lambda e: self.keyboard.set_target(self.derivative_input)
            self.params_layout.addWidget(QLabel("Derivada f'(x):"))
            self.params_layout.addWidget(self.derivative_input)
            
        elif method == "Punto Fijo":
            # Función de iteración g(x)
            self.x0_input = QDoubleSpinBox()
            self.x0_input.setRange(-100, 100)
            self.x0_input.setValue(1)
            self.params_layout.addWidget(QLabel("Aproximación inicial x₀:"))
            self.params_layout.addWidget(self.x0_input)
            
            self.g_function_input = QLineEdit()
            self.g_function_input.setPlaceholderText("Ej: sqrt(4 + x), (x + 4/x)/2")
            self.g_function_input.focusInEvent = lambda e: self.keyboard.set_target(self.g_function_input)
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
            tol = self.tolerance_input.value()
            max_iter = self.max_iter_input.value()
            
            if method == "Bisección":
                a = self.a_input.value()
                b = self.b_input.value()
                
                if a >= b:
                    QMessageBox.warning(self, "Error", "a debe ser menor que b")
                    return
                
                root, iterations, history = NumericalMethods.bisection_method(f, a, b, tol, max_iter)
                
                # Graficar convergencia
                self.plot_widget.plot_convergence(range(len(history)), history, "Convergencia - Bisección")
                
                results = f"""
Método: Bisección
Función: f(x) = {function_str}
Intervalo inicial: [{a}, {b}]
Raíz encontrada: x ≈ {root:.8f}
f(x) ≈ {f(root):.2e}
Iteraciones: {iterations}
Tolerancia: {tol:.2e}
                """.strip()
            
            elif method == "Newton-Raphson":
                derivative_str = self.derivative_input.text().strip()
                if not derivative_str:
                    QMessageBox.warning(self, "Error", "Ingrese la derivada f'(x)")
                    return
                
                df = MathParser.parse_function(derivative_str)
                x0 = self.x0_input.value()
                
                root, iterations, history = NumericalMethods.newton_raphson_method(f, df, x0, tol, max_iter)
                
                # Graficar convergencia
                self.plot_widget.plot_convergence(range(len(history)), history, "Convergencia - Newton-Raphson")
                
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
            
            elif method == "Punto Fijo":
                g_str = self.g_function_input.text().strip()
                if not g_str:
                    QMessageBox.warning(self, "Error", "Ingrese la función g(x)")
                    return
                
                g = MathParser.parse_function(g_str)
                x0 = self.x0_input.value()
                
                root, iterations, history = NumericalMethods.fixed_point_method(g, x0, tol, max_iter)
                
                # Graficar convergencia
                self.plot_widget.plot_convergence(range(len(history)), history, "Convergencia - Punto Fijo")
                
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
            
            self.results_text.setText(results)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error encontrando raíz: {str(e)}")

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
        left_panel = QGroupBox("🔢 Teclado Virtual")
        left_layout = QVBoxLayout()
        
        self.keyboard = MathKeyboard()
        left_layout.addWidget(self.keyboard)
        
        # Información de uso
        info_label = QLabel("""
        💡 <b>Instrucciones:</b>
        • Haga clic en una caja de texto
        • Use el teclado virtual para funciones matemáticas
        • Funciones disponibles: sin, cos, tan, exp, log, sqrt
        • Constantes: π (pi), e
        • Ingrese números y variables directamente desde el teclado
        """)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #bdc3c7; font-size: 11px; padding: 10px; background-color: #34495e; border-radius: 6px; margin: 5px;")
        left_layout.addWidget(info_label)
        
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(350)
        
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
            from gui.comparison_tab import ComparisonTab
            
            self.interpolation_tab = InterpolationTab(self.keyboard, self.plot_widget)
            self.derivatives_tab = DerivativesTab(self.keyboard, self.plot_widget)
            self.comparison_tab = ComparisonTab(self.keyboard, self.plot_widget)
            
            self.tab_widget.addTab(self.ode_tab, "📈 Ecuaciones Diferenciales")
            self.tab_widget.addTab(self.roots_tab, "🎯 Búsqueda de Raíces")
            self.tab_widget.addTab(self.integration_tab, "∫ Integración")
            self.tab_widget.addTab(self.interpolation_tab, "📊 Interpolación")
            self.tab_widget.addTab(self.derivatives_tab, "🔢 Derivadas")
            self.tab_widget.addTab(self.comparison_tab, "🔄 Comparación")
        except ImportError as e:
            # Si no se pueden importar las pestañas avanzadas, usar solo las básicas
            print(f"Warning: No se pudieron cargar pestañas avanzadas: {e}")
            self.tab_widget.addTab(self.ode_tab, "📈 Ecuaciones Diferenciales")
            self.tab_widget.addTab(self.roots_tab, "🎯 Búsqueda de Raíces")
            self.tab_widget.addTab(self.integration_tab, "∫ Integración")
        
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
            font-size: 26px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
            letter-spacing: 1px;
            margin: 0px;
            padding: 8px 0px;
        """)
        
        # Subtítulo con información técnica
        subtitle_label = QLabel("Métodos Numéricos • Interfaz Gráfica Moderna • Versión 3.0")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("""
            color: #95a5a6;
            font-size: 13px;
            font-weight: normal;
            font-style: italic;
            letter-spacing: 0.5px;
            margin: 0px;
            padding: 4px 0px;
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        
        frame.setLayout(layout)
        frame.setMaximumHeight(140)
        frame.setMinimumHeight(140)
        
        return frame
    
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
