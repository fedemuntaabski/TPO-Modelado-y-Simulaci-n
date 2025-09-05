"""
Módulo de Graficación Auxiliar
Contiene métodos de respaldo para visualización simplificada y fallback
"""

import numpy as np

def plot_simplified(plot_widget, f, function_str, history, root, method, a=None, b=None, x0=None, g_function=None):
    """Grafica versión simplificada en caso de error"""
    # Crear layout con 2 subplots para versión simplificada
    ax1 = plot_widget.figure.add_subplot(211)
    ax2 = plot_widget.figure.add_subplot(212)

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

    plot_widget.figure.tight_layout()
    plot_widget.canvas.draw()

def plot_fallback(plot_widget, root, method, history):
    """Último recurso: mostrar solo texto informativo"""
    ax = plot_widget.figure.add_subplot(111)
    ax.text(0.5, 0.5,
           '📊 RESULTADOS DEL MÉTODO ' + method.upper() + '\n\n' +
           f'Raíz encontrada: {root:.6f}\n' +
           f'Iteraciones realizadas: {len(history)}\n' +
           f'Última aproximación: {history[-1]:.6f}\n\n' +
           'Error en graficación: Revisa la función f(x)',
           ha='center', va='center', transform=ax.transAxes,
           fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
    ax.set_title('Resultado del Cálculo', fontsize=14, fontweight='bold')
    ax.axis('off')
    plot_widget.figure.tight_layout()
    plot_widget.canvas.draw()
