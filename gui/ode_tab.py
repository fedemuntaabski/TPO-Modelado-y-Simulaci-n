"""
Pestaña para resolver ecuaciones diferenciales ordinarias
Implementa la clase ODETab para el simulador matemático
"""

import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QMessageBox
)
from PyQt6.QtCore import Qt

from numerics.methods import NumericalMethods, MathParser

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
