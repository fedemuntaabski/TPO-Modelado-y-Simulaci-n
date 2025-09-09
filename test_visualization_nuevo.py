#!/usr/bin/env python3
"""
Script de prueba para verificar la visualización corregida de Monte Carlo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.monte_carlo_engine import MonteCarloEngine
from src.core.function_parser import parse_function
import numpy as np
import matplotlib.pyplot as plt

def test_visualization_1d():
    """Probar visualización 1D con exp(x)"""
    print("=== Prueba de Visualización 1D ===")

    mc_engine = MonteCarloEngine()

    # Parsear función exp(x)
    func = parse_function("exp(x)", ["x"])
    print("✓ Función exp(x) parseada correctamente")

    # Parámetros de simulación
    n_samples = 2000
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

    # Crear visualización similar a la UI
    fig, ax = plt.subplots(figsize=(10, 6))

    # Graficar la función original
    x_vals = np.linspace(x_range[0], x_range[1], 1000)
    y_vals = np.array([func(x) for x in x_vals])

    ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x) = exp(x)', alpha=0.8)
    ax.fill_between(x_vals, 0, y_vals, alpha=0.3, color='blue', label='Área bajo la curva')

    # Graficar puntos clasificados
    points_inside = results['puntos_dentro']
    points_outside = results['puntos_fuera']

    if len(points_inside) > 0:
        ax.scatter(points_inside[:, 0], np.zeros_like(points_inside[:, 0]),
                   color='green', s=50, alpha=0.7, label='Puntos de éxito', marker='o', edgecolors='darkgreen')

    if len(points_outside) > 0:
        ax.scatter(points_outside[:, 0], np.full_like(points_outside[:, 0], np.max(y_vals) * 1.1),
                   color='red', s=50, alpha=0.7, label='Puntos de fracaso', marker='x')

    # Configurar gráfico
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title('Integración Monte Carlo 1D - exp(x)', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.5)

    # Ajustar límites
    y_max = np.max(y_vals)
    ax.set_ylim(-0.1 * y_max, y_max * 1.2)

    # Agregar anotaciones
    integral_val = results['resultado_integracion']
    ci_lower, ci_upper = results['intervalo_confianza']
    ax.annotate(f'Integral: {integral_val:.3f}\nIC: [{ci_lower:.3f}, {ci_upper:.3f}]',
                xy=(0.02, 0.98), xycoords='axes fraction',
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig('test_visualization_1d.png', dpi=150, bbox_inches='tight')
    print("✓ Visualización guardada como 'test_visualization_1d.png'")
    plt.close()

def test_visualization_2d():
    """Probar visualización 2D con x*y"""
    print("\n=== Prueba de Visualización 2D ===")

    mc_engine = MonteCarloEngine()

    # Parsear función x*y
    func = parse_function("x*y", ["x", "y"])
    print("✓ Función x*y parseada correctamente")

    # Parámetros de simulación
    n_samples = 3000
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

    # Crear visualización 3D
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Crear malla para la superficie
    x_surf = np.linspace(x_range[0], x_range[1], 30)
    y_surf = np.linspace(y_range[0], y_range[1], 30)
    X, Y = np.meshgrid(x_surf, y_surf)
    
    # Función wrapper para visualización
    def func_vis(x, y):
        return func(x, y)  # func ya está definido para x,y
    
    Z = np.array([[func_vis(x, y) for x in x_surf] for y in y_surf])

    # Graficar superficie
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, linewidth=0, antialiased=True)

    # Graficar puntos clasificados
    points_inside = results['puntos_dentro']
    points_outside = results['puntos_fuera']

    if len(points_inside) > 0:
        ax.scatter(points_inside[:, 0], points_inside[:, 1], np.zeros_like(points_inside[:, 0]),
                   color='green', s=30, alpha=0.8, label='Puntos de éxito')

    if len(points_outside) > 0:
        ax.scatter(points_outside[:, 0], points_outside[:, 1], np.full_like(points_outside[:, 0], np.max(Z) * 1.1),
                   color='red', s=30, alpha=0.8, label='Puntos de fracaso', marker='x')

    # Configurar gráfico 3D
    ax.set_xlabel('x', fontsize=10)
    ax.set_ylabel('y', fontsize=10)
    ax.set_zlabel('f(x,y)', fontsize=10)
    ax.set_title('Integración Monte Carlo 2D - x*y', fontsize=12, fontweight='bold')

    # Ajustar vista
    ax.view_init(elev=20, azim=45)

    # Agregar barra de color
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='f(x,y)')

    # Agregar anotaciones
    integral_val = results['resultado_integracion']
    ci_lower, ci_upper = results['intervalo_confianza']
    ax.text2D(0.02, 0.98, f'Integral: {integral_val:.3f}\nIC: [{ci_lower:.3f}, {ci_upper:.3f}]',
              transform=ax.transAxes, fontsize=8,
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig('test_visualization_2d.png', dpi=150, bbox_inches='tight')
    print("✓ Visualización guardada como 'test_visualization_2d.png'")
    plt.close()

if __name__ == "__main__":
    test_visualization_1d()
    test_visualization_2d()
    print("\n=== Pruebas completadas ===")
    print("Archivos generados:")
    print("- test_visualization_1d.png")
    print("- test_visualization_2d.png")
