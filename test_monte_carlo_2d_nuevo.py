#!/usr/bin/env python3
"""
Script de prueba para verificar la nueva implementación de Monte Carlo 2D
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.monte_carlo_engine import MonteCarloEngine
from src.core.function_parser import parse_function
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def test_monte_carlo_2d_nuevo():
    """
    Prueba específica para la nueva implementación del Monte Carlo 2D
    con visualización mejorada y optimizada
    """
    print("=== Prueba de la Nueva Implementación Monte Carlo 2D ===\n")
    
    # Crear instancia del motor Monte Carlo
    mc_engine = MonteCarloEngine()
    
    # Probar varias funciones para verificar que la visualización funciona bien
    test_functions = [
        ("x*y", ["x", "y"], "Producto x×y (valor exacto: 0.25)"),
        ("sin(x)*cos(y)", ["x", "y"], "sin(x)×cos(y)"),
        ("x**2 + y**2", ["x", "y"], "Paraboloide x²+y²")
    ]
    
    for func_str, vars, description in test_functions:
        print(f"\n>>> Probando función: {description} <<<")
        
        # Parsear la función
        func = parse_function(func_str, vars)
        print(f"✓ Función {func_str} parseada correctamente")
        
        # Configurar parámetros de simulación
        n_samples = 3000  # Más puntos para mejor visualización
        x_range = (0, 1)
        y_range = (0, 1)
        
        # Ejecutar simulación
        results = mc_engine.simulate(
            func=func,
            n_samples=n_samples,
            seed=42,  # Semilla fija para reproducibilidad
            dimensions=2,
            x_range=x_range,
            y_range=y_range
        )
        
        print("✓ Simulación completada")
        print(f"  Valor estimado: {results['resultado_integracion']:.6f}")
        
        # Generar nombre de archivo para la visualización
        filename = f"monte_carlo_2d_{func_str.replace('*', '').replace('(', '').replace(')', '').replace(' ', '_')}.png"
        
        # Crear visualización 3D mejorada
        fig = plt.figure(figsize=(14, 10))
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#2b2b2b')
        
        # Configurar elementos 3D
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('white')
        ax.yaxis.pane.set_edgecolor('white')
        ax.zaxis.pane.set_edgecolor('white')
        ax.tick_params(colors='white')
        
        # Crear malla para la superficie con resolución óptima
        x_surf = np.linspace(x_range[0], x_range[1], 40)  # Mayor resolución
        y_surf = np.linspace(y_range[0], y_range[1], 40)
        X, Y = np.meshgrid(x_surf, y_surf)
        
        # Evaluar función en la malla de manera optimizada
        Z = np.zeros_like(X)
        for i in range(len(x_surf)):
            for j in range(len(y_surf)):
                Z[j, i] = func(X[j, i], Y[j, i])
        
        # Graficar superficie con colores vivos
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, 
                              linewidth=0, antialiased=True)
        
        # Obtener puntos de la simulación
        points_inside = results['puntos_dentro']
        points_outside = results['puntos_fuera']
        
        # Graficar puntos clasificados con mejor visibilidad
        if len(points_inside) > 0:
            # Calcular valores de la función para cada punto interno
            z_max_per_point = np.array([func(x, y) for x, y in points_inside])
            
            # Usar valores aleatorios entre 0 y el valor real de la función en ese punto
            z_inside = np.random.uniform(0, z_max_per_point, size=len(points_inside))
            
            # Dibujar puntos de éxito como esferas verdes
            ax.scatter(points_inside[:, 0], points_inside[:, 1], z_inside,
                      color='lime', s=40, alpha=0.9, label='Puntos de éxito', 
                      marker='o', edgecolors='darkgreen')
        
        if len(points_outside) > 0:
            # Calcular altura máxima para puntos externos
            z_max = np.max(Z)
            
            # Generar posiciones por encima de la superficie
            z_outside = np.random.uniform(z_max * 1.1, z_max * 1.5, size=len(points_outside))
            
            # Dibujar puntos de fracaso como cruces rojas
            ax.scatter(points_outside[:, 0], points_outside[:, 1], z_outside,
                      color='red', s=40, alpha=0.9, label='Puntos de fracaso', 
                      marker='x', linewidths=2)
        
        # Configurar gráfico 3D con etiquetas claras
        ax.set_xlabel('t', fontsize=14, labelpad=10, color='white')
        ax.set_ylabel('y', fontsize=14, labelpad=10, color='white')
        ax.set_zlabel('f(t,y)', fontsize=14, labelpad=10, color='white')
        ax.set_title(f'Integración Monte Carlo 2D: {description}', 
                    fontsize=16, fontweight='bold', color='white')
        
        # Agregar leyenda con mejor visibilidad
        ax.legend(loc='upper right', fontsize=12, framealpha=0.8)
        
        # Ajustar vista para mejor visualización (probar diferentes ángulos)
        ax.view_init(elev=30, azim=45)
        
        # Agregar barra de color
        cbar = fig.colorbar(surf, ax=ax, shrink=0.7, aspect=10, pad=0.1)
        cbar.set_label('f(t,y)', fontsize=12, color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        cbar.outline.set_edgecolor('white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        
        # Agregar anotaciones con resultados
        integral_val = results['resultado_integracion']
        ci_lower, ci_upper = results['intervalo_confianza']
        ax.text2D(0.02, 0.98, f'Integral: {integral_val:.6f}\nIC: [{ci_lower:.6f}, {ci_upper:.6f}]', 
                 transform=ax.transAxes, fontsize=12, weight='bold', color='white',
                 bbox=dict(boxstyle='round', facecolor='#444444', alpha=0.9))
        
        # Guardar imagen
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ Visualización 2D guardada como '{filename}'")
        plt.close()

    print("\n=== Prueba de visualización completa ===")
    print("✓ Pruebas completadas con éxito")
    print("Archivos generados:")
    for func_str, _, _ in test_functions:
        filename = f"monte_carlo_2d_{func_str.replace('*', '').replace('(', '').replace(')', '').replace(' ', '_')}.png"
        print(f"- {filename}")

if __name__ == "__main__":
    test_monte_carlo_2d_nuevo()
