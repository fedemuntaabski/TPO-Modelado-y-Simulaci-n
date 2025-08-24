"""
Pestaña de Comparación de Métodos Numéricos
Permite comparar diferentes métodos lado a lado y analizar su convergencia
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QCheckBox, QTableWidget, QTableWidgetItem, QMessageBox, QSplitter,
    QTabWidget
)
from PyQt6.QtCore import Qt

from numerics.methods import NumericalMethods, MathParser
from numerics.advanced import InterpolationMethods, AdvancedNumericalMethods, ErrorAnalysis

class ComparisonTab(QWidget):
    """
    Pestaña principal para comparación de métodos numéricos
    """
    
    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        
        # Panel izquierdo: Configuración
        config_panel = QWidget()
        config_layout = QVBoxLayout()
        
        # Selección de tipo de comparación
        comparison_group = QGroupBox("Tipo de Comparación")
        comparison_layout = QVBoxLayout()
        
        self.comparison_type = QComboBox()
        self.comparison_type.addItems([
            "Métodos de Raíces",
            "Aceleración de Aitken",
            "Precisión de Derivadas",
            "Convergencia de Integrales"
        ])
        self.comparison_type.currentTextChanged.connect(self.on_comparison_type_changed)
        comparison_layout.addWidget(self.comparison_type)
        
        comparison_group.setLayout(comparison_layout)
        config_layout.addWidget(comparison_group)
        
        # Contenedor dinámico para parámetros específicos
        self.dynamic_params = QWidget()
        self.dynamic_layout = QVBoxLayout()
        self.dynamic_params.setLayout(self.dynamic_layout)
        config_layout.addWidget(self.dynamic_params)
        
        # Botón para ejecutar comparación
        self.compare_button = QPushButton("🔄 Ejecutar Comparación")
        from gui.themes import DarkTheme
        self.compare_button.setStyleSheet(DarkTheme.get_button_style("primary") + "padding: 15px; font-size: 14px;")
        self.compare_button.clicked.connect(self.execute_comparison)
        config_layout.addWidget(self.compare_button)
        
        # Área de resultados
        results_group = QGroupBox("Resultados de Comparación")
        results_layout = QVBoxLayout()
        
        self.results_table = QTableWidget()
        self.results_table.setMaximumHeight(200)
        results_layout.addWidget(self.results_table)
        
        self.summary_text = QTextEdit()
        self.summary_text.setMaximumHeight(150)
        results_layout.addWidget(self.summary_text)
        
        results_group.setLayout(results_layout)
        config_layout.addWidget(results_group)
        
        config_panel.setLayout(config_layout)
        config_panel.setMaximumWidth(400)
        
        # Panel derecho: Gráficos
        layout.addWidget(config_panel)
        layout.addWidget(self.plot_widget)
        
        self.setLayout(layout)
        
        # Inicializar con el primer tipo
        self.on_comparison_type_changed()
    
    def on_comparison_type_changed(self):
        """Actualiza la interfaz según el tipo de comparación seleccionado"""
        # Limpiar layout anterior
        for i in reversed(range(self.dynamic_layout.count())):
            item = self.dynamic_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
        
        comparison_type = self.comparison_type.currentText()
        
        if comparison_type == "Métodos de Raíces":
            self.setup_root_methods_comparison()
        elif comparison_type == "Aceleración de Aitken":
            self.setup_aitken_comparison()
        elif comparison_type == "Precisión de Derivadas":
            self.setup_derivatives_comparison()
        elif comparison_type == "Convergencia de Integrales":
            self.setup_integration_comparison()
    
    def setup_root_methods_comparison(self):
        """Configura la interfaz para comparar métodos de búsqueda de raíces"""
        # Función
        func_group = QGroupBox("Función f(x)")
        func_layout = QVBoxLayout()
        
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: x**2 - 4, sin(x) - 0.5")
        self.function_input.setText("x**2 - 4")  # Valor por defecto
        self.function_input.focusInEvent = lambda e: self.keyboard.set_target(self.function_input)
        func_layout.addWidget(self.function_input)
        
        func_group.setLayout(func_layout)
        self.dynamic_layout.addWidget(func_group)
        
        # Métodos a comparar
        methods_group = QGroupBox("Métodos a Comparar")
        methods_layout = QVBoxLayout()
        
        self.bisection_check = QCheckBox("Bisección")
        self.bisection_check.setChecked(True)
        self.newton_check = QCheckBox("Newton-Raphson")
        self.newton_check.setChecked(True)
        self.fixed_point_check = QCheckBox("Punto Fijo")
        
        methods_layout.addWidget(self.bisection_check)
        methods_layout.addWidget(self.newton_check)
        methods_layout.addWidget(self.fixed_point_check)
        
        methods_group.setLayout(methods_layout)
        self.dynamic_layout.addWidget(methods_group)
        
        # Parámetros específicos
        params_group = QGroupBox("Parámetros")
        params_layout = QVBoxLayout()
        
        # Para bisección
        bisection_layout = QHBoxLayout()
        self.a_input = QDoubleSpinBox()
        self.a_input.setRange(-100, 100)
        self.a_input.setValue(-5)
        self.b_input = QDoubleSpinBox()
        self.b_input.setRange(-100, 100)
        self.b_input.setValue(5)
        
        bisection_layout.addWidget(QLabel("Intervalo [a,b]:"))
        bisection_layout.addWidget(self.a_input)
        bisection_layout.addWidget(self.b_input)
        params_layout.addLayout(bisection_layout)
        
        # Para Newton-Raphson
        newton_layout = QHBoxLayout()
        self.derivative_input = QLineEdit()
        self.derivative_input.setPlaceholderText("Derivada f'(x)")
        self.derivative_input.setText("2*x")  # Derivada por defecto
        self.derivative_input.focusInEvent = lambda e: self.keyboard.set_target(self.derivative_input)
        
        self.x0_newton = QDoubleSpinBox()
        self.x0_newton.setRange(-100, 100)
        self.x0_newton.setValue(1)
        
        newton_layout.addWidget(QLabel("f'(x):"))
        newton_layout.addWidget(self.derivative_input)
        newton_layout.addWidget(QLabel("x₀:"))
        newton_layout.addWidget(self.x0_newton)
        params_layout.addLayout(newton_layout)
        
        # Para punto fijo
        fixed_layout = QHBoxLayout()
        self.g_function_input = QLineEdit()
        self.g_function_input.setPlaceholderText("g(x) para x = g(x)")
        self.g_function_input.setText("sqrt(4)")  # Función g por defecto
        self.g_function_input.focusInEvent = lambda e: self.keyboard.set_target(self.g_function_input)
        
        self.x0_fixed = QDoubleSpinBox()
        self.x0_fixed.setRange(-100, 100)
        self.x0_fixed.setValue(1)
        
        fixed_layout.addWidget(QLabel("g(x):"))
        fixed_layout.addWidget(self.g_function_input)
        fixed_layout.addWidget(QLabel("x₀:"))
        fixed_layout.addWidget(self.x0_fixed)
        params_layout.addLayout(fixed_layout)
        
        # Tolerancia
        tol_layout = QHBoxLayout()
        self.tolerance = QDoubleSpinBox()
        self.tolerance.setRange(1e-12, 1e-2)
        self.tolerance.setValue(1e-6)
        self.tolerance.setDecimals(10)
        
        self.max_iterations = QSpinBox()
        self.max_iterations.setRange(10, 500)
        self.max_iterations.setValue(100)
        
        tol_layout.addWidget(QLabel("Tolerancia:"))
        tol_layout.addWidget(self.tolerance)
        tol_layout.addWidget(QLabel("Máx iter:"))
        tol_layout.addWidget(self.max_iterations)
        params_layout.addLayout(tol_layout)
        
        params_group.setLayout(params_layout)
        self.dynamic_layout.addWidget(params_group)
    
    def setup_aitken_comparison(self):
        """Configura la interfaz para comparar con y sin aceleración de Aitken"""
        # Método base
        method_group = QGroupBox("Método Base")
        method_layout = QVBoxLayout()
        
        self.base_method = QComboBox()
        self.base_method.addItems(["Punto Fijo", "Newton-Raphson"])
        method_layout.addWidget(self.base_method)
        
        method_group.setLayout(method_layout)
        self.dynamic_layout.addWidget(method_group)
        
        # Función y parámetros similares a los anteriores
        # ... (implementar según necesidad)
    
    def setup_derivatives_comparison(self):
        """Configura la comparación de precisión en derivadas"""
        # Implementar configuración para derivadas
        pass
    
    def setup_integration_comparison(self):
        """Configura la comparación de convergencia en integrales"""
        # Implementar configuración para integrales
        pass
    
    def execute_comparison(self):
        """Ejecuta la comparación seleccionada"""
        comparison_type = self.comparison_type.currentText()
        
        if comparison_type == "Métodos de Raíces":
            self.compare_root_methods()
        elif comparison_type == "Aceleración de Aitken":
            self.compare_aitken_acceleration()
        # ... otros tipos
    
    def compare_root_methods(self):
        """Compara métodos de búsqueda de raíces"""
        try:
            function_str = self.function_input.text().strip()
            if not function_str:
                QMessageBox.warning(self, "Error", "Ingrese una función")
                return
            
            f = MathParser.parse_function(function_str)
            tol = self.tolerance.value()
            max_iter = self.max_iterations.value()
            
            results = {}
            histories = {}
            
            # Ejecutar métodos seleccionados
            if self.bisection_check.isChecked():
                try:
                    a, b = self.a_input.value(), self.b_input.value()
                    root, iterations, history = NumericalMethods.bisection_method(f, a, b, tol, max_iter)
                    results['Bisección'] = {
                        'root': root,
                        'iterations': iterations,
                        'final_error': abs(f(root))
                    }
                    histories['Bisección'] = history
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Error en bisección: {str(e)}")
            
            if self.newton_check.isChecked():
                try:
                    derivative_str = self.derivative_input.text().strip()
                    if derivative_str:
                        df = MathParser.parse_function(derivative_str)
                        x0 = self.x0_newton.value()
                        root, iterations, history = NumericalMethods.newton_raphson_method(f, df, x0, tol, max_iter)
                        results['Newton-Raphson'] = {
                            'root': root,
                            'iterations': iterations,
                            'final_error': abs(f(root))
                        }
                        histories['Newton-Raphson'] = history
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Error en Newton-Raphson: {str(e)}")
            
            if self.fixed_point_check.isChecked():
                try:
                    g_str = self.g_function_input.text().strip()
                    if g_str:
                        g = MathParser.parse_function(g_str)
                        x0 = self.x0_fixed.value()
                        root, iterations, history = NumericalMethods.fixed_point_method(g, x0, tol, max_iter)
                        results['Punto Fijo'] = {
                            'root': root,
                            'iterations': iterations,
                            'final_error': abs(f(root))  # Error en f, no en g
                        }
                        histories['Punto Fijo'] = history
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Error en punto fijo: {str(e)}")
            
            # Mostrar resultados
            self.display_comparison_results(results, histories)
            self.plot_convergence_comparison(histories)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en comparación: {str(e)}")
    
    def display_comparison_results(self, results: Dict, histories: Dict):
        """Muestra los resultados en la tabla"""
        if not results:
            return
        
        # Configurar tabla
        methods = list(results.keys())
        self.results_table.setRowCount(len(methods))
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(['Método', 'Raíz', 'Iteraciones', 'Error Final'])
        
        # Llenar tabla
        for i, method in enumerate(methods):
            data = results[method]
            self.results_table.setItem(i, 0, QTableWidgetItem(method))
            self.results_table.setItem(i, 1, QTableWidgetItem(f"{data['root']:.8f}"))
            self.results_table.setItem(i, 2, QTableWidgetItem(str(data['iterations'])))
            self.results_table.setItem(i, 3, QTableWidgetItem(f"{data['final_error']:.2e}"))
        
        # Ajustar columnas
        self.results_table.resizeColumnsToContents()
        
        # Crear resumen
        summary = "COMPARACIÓN DE MÉTODOS\\n" + "="*40 + "\\n\\n"
        
        # Encontrar el mejor método por criterio
        best_iterations = min(results.items(), key=lambda x: x[1]['iterations'])
        best_precision = min(results.items(), key=lambda x: x[1]['final_error'])
        
        summary += f"🏆 Menos iteraciones: {best_iterations[0]} ({best_iterations[1]['iterations']} iter)\\n"
        summary += f"🎯 Mayor precisión: {best_precision[0]} (error: {best_precision[1]['final_error']:.2e})\\n\\n"
        
        summary += "Análisis detallado:\\n"
        for method, data in results.items():
            summary += f"• {method}: {data['iterations']} iter, error {data['final_error']:.2e}\\n"
        
        self.summary_text.setText(summary)
    
    def plot_convergence_comparison(self, histories: Dict):
        """Grafica la comparación de convergencia"""
        if not histories:
            return
        
        self.plot_widget.figure.clear()
        ax = self.plot_widget.figure.add_subplot(111)
        
        colors = ['#3498db', '#e74c3c', '#27ae60', '#f39c12', '#9b59b6']
        
        for i, (method, history) in enumerate(histories.items()):
            iterations = range(len(history))
            color = colors[i % len(colors)]
            ax.plot(iterations, history, 'o-', color=color, label=method, 
                   linewidth=2, markersize=6)
        
        ax.set_xlabel('Iteración')
        ax.set_ylabel('Aproximación')
        ax.set_title('Comparación de Convergencia de Métodos')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        self.plot_widget.canvas.draw()
    
    def compare_aitken_acceleration(self):
        """Compara método con y sin aceleración de Aitken"""
        # Implementar comparación de Aitken
        pass
