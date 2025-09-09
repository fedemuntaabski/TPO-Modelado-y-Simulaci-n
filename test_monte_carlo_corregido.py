#!/usr/bin/env python3
"""
Script de prueba para visualización de Monte Carlo con posicionamiento correcto de puntos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.monte_carlo_engine import MonteCarloEngine
from src.core.function_parser import parse_function
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def test_monte_carlo_1d():
    """Probar visualización Monte Carlo 1D con distribución correcta de puntos"""
    print("=== Prueba de Visualización Monte Carlo 1D con puntos distribuidos correctamente ===")

    mc_engine = MonteCarloEngine()

    # Parsear función exp(x)
    func = parse_function("exp(x)", ["x"])
    print("✓ Función exp(x) parseada correctamente")

    # Parámetros de simulación
    n_samples = 1000
    x_range = (0, 1)

    # Ejecutar simulación
    results = mc_engine.simulate(
        func=func,
        n_samples=n_samples,
        seed=42,
        dimensions=1,
        x_range=x_range
    )

    print("✓ Simulación completada")
    print(f"Valor estimado: {results['resultado_integracion']:.6f}")
    print(f"Valor real (e-1): {np.exp(1) - 1:.6f}")

    # Crear visualización
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#2b2b2b')
    ax.set_facecolor('#2b2b2b')

    # Crear puntos para graficar la función
    x_vals = np.linspace(x_range[0], x_range[1], 1000)
    y_vals = np.array([func(x) for x in x_vals])

    # Graficar la función original con mayor visibilidad
    ax.plot(x_vals, y_vals, 'cyan', linewidth=2.5, label='f(x) = exp(x)', alpha=0.9)

    # Rellenar el área bajo la curva
    y_fill = np.maximum(y_vals, 0)
    ax.fill_between(x_vals, 0, y_fill, alpha=0.3, color='cyan', label='Área bajo la curva')

    # Obtener puntos de la simulación
    points_inside = results['puntos_dentro']
    points_outside = results['puntos_fuera']

    # Generar coordenadas y aleatorias entre 0 y f(x) para puntos dentro
    y_max_per_point = np.array([func(x) for x in points_inside[:, 0]])
    y_inside = np.random.uniform(0, y_max_per_point, size=len(points_inside))

    # Graficar puntos clasificados
    if len(points_inside) > 0:
        ax.scatter(points_inside[:, 0], y_inside, 
                   color='lime', s=60, alpha=0.8, label='Puntos de éxito', 
                   marker='o', edgecolors='darkgreen')

    if len(points_outside) > 0:
        y_max = np.max(y_vals)
        y_outside = np.random.uniform(y_max * 1.0, y_max * 1.5, size=len(points_outside))
        ax.scatter(points_outside[:, 0], y_outside, 
                   color='red', s=60, alpha=0.8, label='Puntos de fracaso', 
                   marker='x', linewidths=2)

    # Configurar gráfico
    ax.set_xlabel('x', fontsize=14, color='white')
    ax.set_ylabel('f(x)', fontsize=14, color='white')
    ax.set_title('Integración Monte Carlo 1D - Puntos correctamente distribuidos', fontsize=14, fontweight='bold', color='white')
    ax.legend(loc='upper right', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)

    # Ajustar colores para tema oscuro
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    # Ajustar límites
    y_max = np.max(y_vals)
    ax.set_ylim(-0.1 * y_max, y_max * 1.6)

    # Agregar anotaciones
    integral_val = results['resultado_integracion']
    ci_lower, ci_upper = results['intervalo_confianza']
    ax.annotate(f'Integral: {integral_val:.3f}\nIC: [{ci_lower:.3f}, {ci_upper:.3f}]',
                xy=(0.02, 0.98), xycoords='axes fraction',
                fontsize=12, verticalalignment='top', color='white',
                bbox=dict(boxstyle='round', facecolor='#444444', alpha=0.9))

    plt.tight_layout()
    plt.savefig('monte_carlo_1d_corrected.png', dpi=150, bbox_inches='tight')
    print("✓ Visualización 1D corregida guardada como 'monte_carlo_1d_corrected.png'")
    plt.close()

def test_monte_carlo_2d():
    """Probar visualización Monte Carlo 2D con distribución correcta de puntos"""
    print("\n=== Prueba de Visualización Monte Carlo 2D con puntos distribuidos correctamente ===")

    mc_engine = MonteCarloEngine()

    # Parsear función x*y
    func = parse_function("x*y", ["x", "y"])
    print("✓ Función x*y parseada correctamente")

    # Parámetros de simulación
    n_samples = 2000
    x_range = (0, 1)
    y_range = (0, 1)

    # Ejecutar simulación
    results = mc_engine.simulate(
        func=func,
        n_samples=n_samples,
        seed=42,
        dimensions=2,
        x_range=x_range,
        y_range=y_range
    )

    print("✓ Simulación completada")
    print(f"Valor estimado: {results['resultado_integracion']:.6f}")
    print(f"Valor real (1/4): {0.25:.6f}")

    # Crear visualización 3D con figura grande
    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor('#2b2b2b')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#2b2b2b')

    # Crear malla para la superficie
    x_surf = np.linspace(x_range[0], x_range[1], 30)
    y_surf = np.linspace(y_range[0], y_range[1], 30)
    X, Y = np.meshgrid(x_surf, y_surf)

    # Evaluar función en la malla
    Z = np.array([[func(x, y) for x in x_surf] for y in y_surf])

    # Graficar superficie con colores vivos
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, linewidth=0, antialiased=True)

    # Obtener puntos de la simulación
    points_inside = results['puntos_dentro']
    points_outside = results['puntos_fuera']

    # Generar alturas aleatorias para puntos dentro
    if len(points_inside) > 0:
        z_max_per_point = np.array([func(x, y) for x, y in points_inside])
        z_inside = np.random.uniform(0, z_max_per_point, size=len(points_inside))
        ax.scatter(points_inside[:, 0], points_inside[:, 1], z_inside,
                   color='lime', s=40, alpha=0.9, label='Puntos de éxito', 
                   marker='o', edgecolors='darkgreen')

    # Puntos fuera por encima de la superficie
    if len(points_outside) > 0:
        z_max = np.max(Z)
        z_outside = np.random.uniform(z_max * 1.1, z_max * 1.5, size=len(points_outside))
        ax.scatter(points_outside[:, 0], points_outside[:, 1], z_outside,
                   color='red', s=40, alpha=0.9, label='Puntos de fracaso', 
                   marker='x', linewidths=2)

    # Configurar gráfico 3D con etiquetas grandes y claras
    ax.set_xlabel('t', fontsize=14, labelpad=10, color='white')
    ax.set_ylabel('y', fontsize=14, labelpad=10, color='white')
    ax.set_zlabel('f(t,y)', fontsize=14, labelpad=10, color='white')
    ax.set_title('Integración Monte Carlo 2D - Puntos correctamente distribuidos', fontsize=14, fontweight='bold', color='white')

    # Ajustar colores para tema oscuro
    ax.tick_params(colors='white')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('white')
    ax.yaxis.pane.set_edgecolor('white')
    ax.zaxis.pane.set_edgecolor('white')

    # Ajustar vista y márgenes
    ax.view_init(elev=30, azim=45)
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)

    # Agregar leyenda con mayor visibilidad
    ax.legend(loc='upper right', fontsize=12)

    # Agregar barra de color mejorada
    cbar = fig.colorbar(surf, ax=ax, shrink=0.7, aspect=10, pad=0.1)
    cbar.set_label('f(t,y)', fontsize=12, color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    cbar.outline.set_edgecolor('white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    # Agregar anotaciones
    integral_val = results['resultado_integracion']
    ci_lower, ci_upper = results['intervalo_confianza']
    ax.text2D(0.02, 0.98, f'Integral: {integral_val:.4f}\nIC: [{ci_lower:.4f}, {ci_upper:.4f}]',
              transform=ax.transAxes, fontsize=12, weight='bold', color='white',
              bbox=dict(boxstyle='round', facecolor='#444444', alpha=0.9))

    plt.savefig('monte_carlo_2d_corrected.png', dpi=150, bbox_inches='tight')
    print("✓ Visualización 2D corregida guardada como 'monte_carlo_2d_corrected.png'")
    plt.close()

if __name__ == "__main__":
    test_monte_carlo_1d()
    test_monte_carlo_2d()
    print("\n=== Pruebas completadas ===")
    print("Archivos generados:")
    print("- monte_carlo_1d_corrected.png")
    print("- monte_carlo_2d_corrected.png")
