"""
Módulo de Graficación para la Pestaña de Raíces
Contiene la lógica de visualización y plotting de resultados
"""

import numpy as np
from PyQt6.QtWidgets import QTableWidgetItem

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
            self._plot_simplified(f, function_str, history, root, method, a, b, x0, g_function)

    def _plot_simplified(self, f, function_str, history, root, method, a=None, b=None, x0=None, g_function=None):
        """Grafica versión simplificada en caso de error"""
        try:
            self.plot_widget.figure.clear()

            # Crear layout con 2 subplots para versión simplificada
            ax1 = self.plot_widget.figure.add_subplot(211)
            ax2 = self.plot_widget.figure.add_subplot(212)

            # Subplot 1: Función básica
            if method == "Bisección" and a is not None and b is not None:
                x_vals = np.linspace(a - 1, b + 1, 500)
            else:
                x_range = 4
                x_vals = np.linspace(x0 - x_range, x0 + x_range, 500) if x0 is not None else np.linspace(-5, 5, 500)

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
            try:
                f_root = f(root)
                info_text += f'\nf(raíz): {f_root:.2e}'
            except:
                pass

            ax2.text(0.02, 0.98, info_text, transform=ax2.transAxes,
                    fontsize=9, verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))

            self.plot_widget.figure.tight_layout()
            self.plot_widget.canvas.draw()

        except Exception as e2:
            print(f"Error incluso en graficación simplificada: {e2}")
            self._plot_fallback(root, method, history)

    def _plot_fallback(self, root, method, history):
        """Último recurso: mostrar solo texto informativo"""
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
