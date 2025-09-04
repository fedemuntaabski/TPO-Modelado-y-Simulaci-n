"""
Módulo de Métodos Numéricos para la Pestaña de Raíces
Contiene la lógica de cálculo para cada método numérico
"""

import numpy as np
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

from numerics.methods import NumericalMethods, MathParser

class RootsTabMethods:
    """
    Clase que maneja la lógica de cálculo de los métodos numéricos
    """

    def __init__(self, ui_instance):
        self.ui = ui_instance

    def find_root(self):
        """Encuentra la raíz usando el método seleccionado"""
        try:
            function_str = self.ui.function_input.text().strip()
            if not function_str:
                QMessageBox.warning(None, "Error", "Ingrese la función f(x)")
                return

            f = MathParser.parse_function(function_str)
            method = self.ui.method_combo.currentText()

            # Convertir valores de texto a números
            try:
                tol = float(self.ui.tolerance_input.text())
                max_iter = int(self.ui.max_iter_input.text())
            except ValueError:
                QMessageBox.warning(None, "Error", "Tolerancia y máximo de iteraciones deben ser números válidos")
                return

            if method == "Bisección":
                return self._solve_bisection(f, function_str, tol, max_iter)
            elif method == "Newton-Raphson":
                return self._solve_newton_raphson(f, function_str, tol, max_iter)
            elif method == "Punto Fijo":
                return self._solve_fixed_point(f, function_str, tol, max_iter)
            elif method == "Aitken":
                return self._solve_aitken(f, function_str, tol, max_iter)

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error encontrando raíz: {str(e)}")

    def _solve_bisection(self, f, function_str, tol, max_iter):
        """Resuelve usando método de bisección"""
        try:
            a = float(self.ui.a_input.text())
            b = float(self.ui.b_input.text())
        except ValueError:
            QMessageBox.warning(None, "Error", "Los valores de a y b deben ser números válidos")
            return

        if a >= b:
            QMessageBox.warning(None, "Error", "a debe ser menor que b")
            return

        root, iterations, history = NumericalMethods.bisection_method(f, a, b, tol, max_iter)

        # Graficar función y convergencia
        from .roots_tab_plotting import RootsTabPlotting
        plotting = RootsTabPlotting(self.ui.plot_widget)
        plotting.plot_function_and_convergence(f, function_str, history, root, "Bisección", a=a, b=b)

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
        self._populate_results_table(history, root, f, "Bisección")
        self.ui.results_text.setText(results)

        return root, iterations, history

    def _solve_newton_raphson(self, f, function_str, tol, max_iter):
        """Resuelve usando método de Newton-Raphson"""
        derivative_str = self.ui.derivative_input.text().strip()
        if not derivative_str:
            QMessageBox.warning(None, "Error", "Ingrese la derivada f'(x)")
            return

        df = MathParser.parse_function(derivative_str)
        try:
            x0 = float(self.ui.x0_input.text())
        except ValueError:
            QMessageBox.warning(None, "Error", "La aproximación inicial debe ser un número válido")
            return

        root, iterations, history = NumericalMethods.newton_raphson_method(f, df, x0, tol, max_iter)

        # Graficar función y convergencia
        from .roots_tab_plotting import RootsTabPlotting
        plotting = RootsTabPlotting(self.ui.plot_widget)
        plotting.plot_function_and_convergence(f, function_str, history, root, "Newton-Raphson", x0=x0, g_function=derivative_str)

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
        self._populate_results_table(history, root, f, "Newton-Raphson")
        self.ui.results_text.setText(results)

        return root, iterations, history

    def _solve_fixed_point(self, f, function_str, tol, max_iter):
        """Resuelve usando método de punto fijo"""
        g_str = self.ui.g_function_input.text().strip()
        if not g_str:
            QMessageBox.warning(None, "Error", "Ingrese la función g(x)")
            return

        g = MathParser.parse_function(g_str)
        try:
            x0 = float(self.ui.x0_input.text())
        except ValueError:
            QMessageBox.warning(None, "Error", "La aproximación inicial debe ser un número válido")
            return

        root, iterations, history = NumericalMethods.fixed_point_method(g, x0, tol, max_iter)

        # Graficar función y convergencia
        from .roots_tab_plotting import RootsTabPlotting
        plotting = RootsTabPlotting(self.ui.plot_widget)
        plotting.plot_function_and_convergence(f, function_str, history, root, "Punto Fijo", x0=x0, g_function=g_str)

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
        self._populate_results_table(history, root, f, "Punto Fijo")
        self.ui.results_text.setText(results)

        return root, iterations, history

    def _solve_aitken(self, f, function_str, tol, max_iter):
        """Resuelve usando método de Aitken"""
        g_str = self.ui.g_function_input.text().strip()
        if not g_str:
            QMessageBox.warning(None, "Error", "Ingrese la función g(x)")
            return

        g = MathParser.parse_function(g_str)
        try:
            x0 = float(self.ui.x0_input.text())
        except ValueError:
            QMessageBox.warning(None, "Error", "La aproximación inicial debe ser un número válido")
            return

        root, iterations, history, accelerated_history, detailed_steps = NumericalMethods.aitken_method(g, x0, tol, max_iter)

        # Graficar función y convergencia
        from .roots_tab_plotting import RootsTabPlotting
        plotting = RootsTabPlotting(self.ui.plot_widget)
        plotting.plot_function_and_convergence(f, function_str, history, root, "Aitken", x0=x0, g_function=g_str)

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
        self._populate_results_table(history, root, f, "Aitken", detailed_steps=detailed_steps)
        self.ui.results_text.setText(results)

        return root, iterations, history

    def _populate_results_table(self, history, root, f, method, detailed_steps=None):
        """Llena la tabla con los detalles de las iteraciones"""
        if not history:
            return

        # Para Aitken, usar información detallada si está disponible
        if method == "Aitken" and detailed_steps:
            self._populate_aitken_table(detailed_steps, root, f)
            return

        # Configuración normal para otros métodos
        num_rows = len(history)
        self.ui.results_table.setRowCount(num_rows)
        self.ui.results_table.setColumnCount(5)
        self.ui.results_table.setHorizontalHeaderLabels([
            'Iteración', 'xᵢ', 'f(xᵢ)', 'Error Absoluto', 'Error Relativo (%)'
        ])

        # Llenar tabla con datos de cada iteración
        for i, x_i in enumerate(history):
            f_x_i = f(x_i)
            abs_error = abs(x_i - root) if i < len(history) - 1 else abs(f_x_i)  # Error absoluto
            rel_error = abs_error / abs(root) if root != 0 else abs_error  # Error relativo

            self.ui.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.ui.results_table.setItem(i, 1, QTableWidgetItem(f"{x_i:.8f}"))
            self.ui.results_table.setItem(i, 2, QTableWidgetItem(f"{f_x_i:.6f}"))
            self.ui.results_table.setItem(i, 3, QTableWidgetItem(self._format_error(abs_error, False)))
            self.ui.results_table.setItem(i, 4, QTableWidgetItem(self._format_error(rel_error, True)))

        # Ajustar columnas al contenido
        self.ui.results_table.resizeColumnsToContents()
        self.ui.results_table.setMaximumHeight(400)  # Aumentar altura para mejor visibilidad

    def _populate_aitken_table(self, detailed_steps, root, f):
        """Llena la tabla con información detallada del método de Aitken"""
        if not detailed_steps:
            return

        # Configurar tabla para Aitken con más columnas
        num_rows = len(detailed_steps)
        self.ui.results_table.setRowCount(num_rows)
        self.ui.results_table.setColumnCount(7)
        self.ui.results_table.setHorizontalHeaderLabels([
            'Iter', 'x₍ᵢ₋₁₎', 'g(x₍ᵢ₋₁₎)', 'x0,x1,x2', 'x*_acelerado', 'Error Abs', 'Error Rel'
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

            self.ui.results_table.setItem(i, 0, QTableWidgetItem(str(iter_num)))
            self.ui.results_table.setItem(i, 1, QTableWidgetItem(f"{x_anterior:.8f}"))
            self.ui.results_table.setItem(i, 2, QTableWidgetItem(f"{g_x_anterior:.8f}"))
            self.ui.results_table.setItem(i, 3, QTableWidgetItem(x0_x1_x2))
            self.ui.results_table.setItem(i, 4, QTableWidgetItem(x_acelerado))
            self.ui.results_table.setItem(i, 5, QTableWidgetItem(error_abs))
            self.ui.results_table.setItem(i, 6, QTableWidgetItem(error_rel))

        # Ajustar columnas al contenido
        self.ui.results_table.resizeColumnsToContents()
        self.ui.results_table.setMaximumHeight(400)

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
