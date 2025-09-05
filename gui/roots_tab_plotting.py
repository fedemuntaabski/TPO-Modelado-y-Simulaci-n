"""
Módulo de Graficación para la Pestaña de Raíces
Contiene la lógica de visualización y plotting de resultados
"""

import numpy as np
from PyQt6.QtWidgets import QTableWidgetItem
from .roots_tab_plotting_bisection import plot_bisection
from .roots_tab_plotting_iterative import plot_iterative
from .roots_tab_plotting_helpers import plot_simplified, plot_fallback

class RootsTabPlotting:
    """
    Clase que maneja la graficación y visualización de resultados
    """

    def __init__(self, plot_widget):
        self.plot_widget = plot_widget

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
                plot_bisection(self.plot_widget, f, function_str, history, root, a, b)
            else:  # Newton-Raphson, Punto Fijo o Aitken
                plot_iterative(self.plot_widget, f, function_str, history, root, method, x0, g_function)

            # Ajustar layout y mostrar
            self.plot_widget.figure.tight_layout()
            self.plot_widget.canvas.draw()

        except Exception as e:
            # Si hay error en la graficación avanzada, mostrar versión simplificada pero informativa
            print(f"Error en graficación avanzada: {e}")
            plot_simplified(self.plot_widget, f, function_str, history, root, method, a, b, x0, g_function)

    def _plot_simplified(self, f, function_str, history, root, method, a=None, b=None, x0=None, g_function=None):
        """Grafica versión simplificada en caso de error"""
        plot_simplified(self.plot_widget, f, function_str, history, root, method, a, b, x0, g_function)

    def _plot_fallback(self, root, method, history):
        """Último recurso: mostrar solo texto informativo"""
        plot_fallback(self.plot_widget, root, method, history)
