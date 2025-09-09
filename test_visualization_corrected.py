#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones en la visualización de Monte Carlo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.monte_carlo_engine import MonteCarloEngine
from src.core.function_parser import parse_function
import numpy as np
import matplotlib.pyplot as plt

def test_1d_visualization():
    """Probar visualización 1D corregida"""
    print("=== Prueba de Visualización 1D Corregida ===")

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

    # Crear visualización corregida
    fig, ax = plt.subplots(figsize=(12, 8))

    # Crear puntos para graficar la función
    x_vals = np.linspace(x_range[0], x_range[1], 1000)
    y_vals = np.array([func(x) for x in x_vals])

    # Graficar la función original
    ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x) = exp(x)', alpha=0.8)

    # Rellenar el área bajo la curva
    y_fill = np.maximum(y_vals, 0)
    ax.fill_between(x_vals, 0, y_fill, alpha=0.3, color='blue', label='Área bajo la curva')

    # Obtener puntos de la simulación
    points_inside = results['puntos_dentro']
    points_outside = results['puntos_fuera']

    # Graficar puntos clasificados CORREGIDOS
    if len(points_inside) > 0:
        # Para puntos dentro: mostrar en verde en sus posiciones correctas (x, f(x))
        y_inside = np.array([func(x) for x in points_inside[:, 0]])
        ax.scatter(points_inside[:, 0], y_inside,
                   color='green', s=50, alpha=0.7, label='Puntos de éxito', marker='o', edgecolors='darkgreen')

    if len(points_outside) > 0:
        # Para puntos fuera: generar posiciones aleatorias por encima de la curva
        y_max = np.max(y_vals)
        y_outside = np.random.uniform(y_max * 1.1, y_max * 1.5, size=len(points_outside))
        ax.scatter(points_outside[:, 0], y_outside,
                   color='red', s=50, alpha=0.7, label='Puntos de fracaso', marker='x')

    # Configurar gráfico
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title('Integración Monte Carlo 1D - CORREGIDA', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.5)

    # Ajustar límites
    y_max = np.max(y_vals)
    ax.set_ylim(-0.1 * y_max, y_max * 1.6)

    # Agregar anotaciones
    integral_val = results['resultado_integracion']
    ci_lower, ci_upper = results['intervalo_confianza']
    ax.annotate(f'Integral: {integral_val:.3f}\nIC: [{ci_lower:.3f}, {ci_upper:.3f}]',
                xy=(0.02, 0.98), xycoords='axes fraction',
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig('test_1d_corrected.png', dpi=150, bbox_inches='tight')
    print("✓ Visualización 1D corregida guardada como 'test_1d_corrected.png'")
    plt.close()

def test_2d_visualization():
    """Probar visualización 2D corregida"""
    print("\n=== Prueba de Visualización 2D Corregida ===")

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

    # Crear visualización 3D corregida
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Crear malla para la superficie
    x_surf = np.linspace(x_range[0], x_range[1], 30)
    y_surf = np.linspace(y_range[0], y_range[1], 30)
    X, Y = np.meshgrid(x_surf, y_surf)

    # Evaluar función en la malla
    Z = np.array([[func(x, y) for x in x_surf] for y in y_surf])

    # Graficar superficie
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, linewidth=0, antialiased=True)

    # Obtener puntos de la simulación
    points_inside = results['puntos_dentro']
    points_outside = results['puntos_fuera']

    # Graficar puntos clasificados CORREGIDOS
    if len(points_inside) > 0:
        # Para puntos dentro: mostrar en verde en sus posiciones correctas (x, y, f(x,y))
        z_inside = np.array([func(x, y) for x, y in points_inside])
        ax.scatter(points_inside[:, 0], points_inside[:, 1], z_inside,
                   color='green', s=30, alpha=0.8, label='Puntos de éxito')

    if len(points_outside) > 0:
        # Para puntos fuera: generar posiciones aleatorias por encima de la superficie
        z_max = np.max(Z)
        z_outside = np.random.uniform(z_max * 1.1, z_max * 1.5, size=len(points_outside))
        ax.scatter(points_outside[:, 0], points_outside[:, 1], z_outside,
                   color='red', s=30, alpha=0.8, label='Puntos de fracaso', marker='x')

    # Configurar gráfico 3D
    ax.set_xlabel('t', fontsize=10)
    ax.set_ylabel('y', fontsize=10)
    ax.set_zlabel('f(t,y)', fontsize=10)
    ax.set_title('Integración Monte Carlo 2D - CORREGIDA', fontsize=12, fontweight='bold')

    # Ajustar vista
    ax.view_init(elev=20, azim=45)

    # Agregar barra de color
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='f(t,y)')

    # Agregar anotaciones
    integral_val = results['resultado_integracion']
    ci_lower, ci_upper = results['intervalo_confianza']
    ax.text2D(0.02, 0.98, f'Integral: {integral_val:.3f}\nIC: [{ci_lower:.3f}, {ci_upper:.3f}]',
              transform=ax.transAxes, fontsize=8,
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig('test_2d_corrected.png', dpi=150, bbox_inches='tight')
    print("✓ Visualización 2D corregida guardada como 'test_2d_corrected.png'")
    plt.close()

if __name__ == "__main__":
    test_1d_visualization()
    test_2d_visualization()
    print("\n=== Pruebas completadas ===")
    print("Archivos generados:")
    print("- test_1d_corrected.png")
    print("- test_2d_corrected.png")
