"""
Módulo para la lógica de interpolación y diferencias finitas
"""

import numpy as np
from PyQt6.QtWidgets import QMessageBox

from numerics.interpolation_methods import InterpolationMethods


class InterpolationLogic:
    """
    Clase que contiene la lógica de cálculo para interpolación
    """

    def __init__(self, data_table, eval_point, results_text, plot_widget):
        self.data_table = data_table
        self.eval_point = eval_point
        self.results_text = results_text
        self.plot_widget = plot_widget

    def get_data_points(self):
        """Extrae los puntos de datos de la tabla"""
        x_points = []
        y_points = []

        for i in range(self.data_table.rowCount()):
            x_item = self.data_table.item(i, 0)
            y_item = self.data_table.item(i, 1)

            if x_item and y_item and x_item.text().strip() and y_item.text().strip():
                try:
                    x = float(x_item.text())
                    y = float(y_item.text())
                    x_points.append(x)
                    y_points.append(y)
                except ValueError:
                    continue

        return np.array(x_points), np.array(y_points)

    def interpolate_lagrange(self):
        """Realiza interpolación de Lagrange"""
        try:
            x_points, y_points = self.get_data_points()

            if len(x_points) < 2:
                QMessageBox.warning(None, "Error", "Se necesitan al menos 2 puntos")
                return

            # Verificar que no hay puntos x repetidos
            if len(np.unique(x_points)) != len(x_points):
                QMessageBox.warning(None, "Error", "Los puntos x deben ser únicos")
                return

            # Ordenar puntos por x
            sorted_indices = np.argsort(x_points)
            x_points = x_points[sorted_indices]
            y_points = y_points[sorted_indices]

            # Punto de evaluación
            x_eval_point = self.eval_point.value()

            # Crear rango para graficar
            x_min, x_max = x_points.min(), x_points.max()
            x_range = x_max - x_min
            x_plot = np.linspace(x_min - 0.2*x_range, x_max + 0.2*x_range, 200)

            # Interpolar
            y_plot, polynomial = InterpolationMethods.lagrange_interpolation_detailed(
                x_points, y_points, x_plot
            )

            # Evaluar en el punto específico
            y_eval = polynomial(x_eval_point)

            # Graficar
            self.plot_widget.figure.clear()
            ax = self.plot_widget.figure.add_subplot(111)

            # Puntos originales
            ax.plot(x_points, y_points, 'ro', markersize=8, label='Puntos dados')

            # Polinomio interpolador
            ax.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio de Lagrange')

            # Punto evaluado
            ax.plot(x_eval_point, y_eval, 'gs', markersize=10, label=f'Evaluación en x={x_eval_point}')

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Interpolación de Lagrange')
            ax.grid(True, alpha=0.3)
            ax.legend()

            self.plot_widget.canvas.draw()

            # Mostrar resultados
            results = f"""
Interpolación de Lagrange
------------------------
Puntos utilizados: {len(x_points)}
Grado del polinomio: {len(x_points) - 1}

Evaluación:
x = {x_eval_point}
y = {y_eval:.8f}

Puntos dados:
"""
            for i, (x, y) in enumerate(zip(x_points, y_points)):
                results += f"  P{i+1}: ({x}, {y})\n"

            self.results_text.setText(results)

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error en interpolación: {str(e)}")

    def calculate_differences(self):
        """Calcula la tabla de diferencias finitas"""
        try:
            x_points, y_points = self.get_data_points()

            if len(x_points) < 2:
                QMessageBox.warning(None, "Error", "Se necesitan al menos 2 puntos")
                return

            # Ordenar puntos
            sorted_indices = np.argsort(x_points)
            x_points = x_points[sorted_indices]
            y_points = y_points[sorted_indices]

            # Calcular tabla de diferencias
            diff_table = InterpolationMethods.finite_differences_table(x_points, y_points)

            # Formatear resultados
            results = "Tabla de Diferencias Finitas\n"
            results += "=" * 40 + "\n\n"
            results += f"{'i':>3} {'x':>8} {'f(x)':>12}"

            n = len(x_points)
            for j in range(1, n):
                results += f"{'Δ^' + str(j) + 'f':>12}"
            results += "\n"
            results += "-" * (15 + 12 * n) + "\n"

            for i in range(n):
                results += f"{i:>3} {x_points[i]:>8.3f} {y_points[i]:>12.6f}"
                for j in range(1, n - i):
                    if i + j <= n:
                        results += f"{diff_table[i, j]:>12.6f}"
                results += "\n"

            # Verificar si las diferencias son constantes (polinomio)
            last_col = n - 1
            if n > 2:
                last_diffs = diff_table[:n-last_col, last_col]
                if len(last_diffs) > 1 and np.allclose(last_diffs, last_diffs[0], rtol=1e-10):
                    results += f"\n📊 Los datos parecen seguir un polinomio de grado {last_col}\n"
                    results += f"   (diferencia constante en la columna {last_col})\n"

            self.results_text.setText(results)

            # Graficar solo los puntos
            self.plot_widget.figure.clear()
            ax = self.plot_widget.figure.add_subplot(111)
            ax.plot(x_points, y_points, 'ro-', markersize=8, linewidth=2)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title('Puntos de Datos para Diferencias Finitas')
            ax.grid(True, alpha=0.3)
            self.plot_widget.canvas.draw()

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error calculando diferencias: {str(e)}")
