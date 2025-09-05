"""
Módulo de Graficación para Método de Bisección
Contiene la lógica específica de visualización para el método de bisección
"""

import numpy as np

def plot_bisection(plot_widget, f, function_str, history, root, a, b):
    """Grafica la función y análisis para el método de bisección"""
    # Crear figura con 3 subplots para análisis completo
    gs = plot_widget.figure.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    # Subplot 1: Función con intervalo y raíz detallada (ocupa fila completa superior)
    ax1 = plot_widget.figure.add_subplot(gs[0, :])
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
    f_root = f(root)
    ax1.scatter([root], [f_root], color='red', s=120, zorder=7,
               marker='*', edgecolors='darkred', linewidth=2,
               label=f'Raíz Final\nx = {root:.6f}\nf(x) = {f_root:.2e}')

    # Línea vertical de la raíz
    ax1.axvline(x=root, color='red', linestyle='--', linewidth=2, alpha=0.7)

    ax1.set_xlabel('x', fontsize=11, fontweight='bold')
    ax1.set_ylabel('f(x)', fontsize=11, fontweight='bold')
    ax1.set_title('📊 Función y Raíz Final - Método Bisección', fontsize=12, fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.3)
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)

    # Subplot 2: Convergencia de aproximaciones
    ax2 = plot_widget.figure.add_subplot(gs[1, 0])
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
    ax3 = plot_widget.figure.add_subplot(gs[1, 1])
    errors = [abs(x - root) for x in history]
    ax3.semilogy(range(len(errors)), errors, 'bo-', linewidth=2, markersize=6,
                markerfacecolor='blue', markeredgecolor='navy', markeredgewidth=1,
                label='Error absoluto')
    ax3.set_xlabel('Iteración', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Error |x - x*|', fontsize=10, fontweight='bold')
    ax3.set_title('🔍 Análisis de Errores', fontsize=11, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=8)

    # Información detallada en el subplot de errores
    error_info = '📊 ANÁLISIS COMPLETO\n\n'
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
