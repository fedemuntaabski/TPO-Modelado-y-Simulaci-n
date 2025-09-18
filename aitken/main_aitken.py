#!/usr/bin/env python3
"""
Main ejecutable para la aplicación de Aceleración de Aitken

Uso:
    python main_aitken.py

Funcionalidades:
- Interfaz gráfica moderna con CustomTkinter
- Tabla detallada mostrando 8 decimales
- Gráficos de convergencia
- Ejemplos predefinidos
"""

import sys
import os

# Agregar el directorio de aitken al path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from aitken_app import AitkenGUI


def print_banner():
    """Mostrar banner de bienvenida."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                MÉTODO DE ACELERACIÓN DE AITKEN               ║
    ║                                                              ║
    ║  Acelera la convergencia de métodos iterativos de punto fijo ║
    ║  Fórmula: x_new = x - (x₁ - x)² / (x₂ - 2x₁ + x)             ║
    ║                                                              ║
    ║  Características:                                            ║
    ║  • Tabla con 8 decimales de precisión                        ║
    ║  • Gráficos de convergencia                                  ║
    ║  • Interfaz moderna con tema oscuro                          ║
    ║  • Ejemplos matemáticos predefinidos                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_examples():
    """Mostrar ejemplos de uso."""
    examples = """
    📋 EJEMPLOS DE FUNCIONES PARA PROBAR:
    
    1. cos(x)           - Encuentra x = cos(x) ≈ 0.739085133
    2. sqrt(x + 1)      - Encuentra la proporción áurea φ ≈ 1.618033989
    3. (x + 2/x) / 2    - Encuentra √2 ≈ 1.414213562
    4. exp(-x)          - Encuentra la intersección x = e^(-x) ≈ 0.567143290
    5. (x + 1) / 2      - Función lineal simple
    
    💡 SUGERENCIAS:
    • Usa valores iniciales cercanos a la solución
    • Para cos(x), prueba x₀ = 0.5
    • Para sqrt(x+1), prueba x₀ = 1.0
    • Tolerancia recomendada: 1e-8
    """
    print(examples)


def main():
    """Función principal del programa."""
    
    print_banner()
    print_examples()
    
    print("🚀 Iniciando aplicación gráfica...")
    print("   Cierra esta ventana de consola para terminar el programa.")
    print("=" * 70)
    
    try:
        # Crear y ejecutar la aplicación
        app = AitkenGUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario.")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando la aplicación: {e}")
        print("   Verifica que todas las dependencias estén instaladas:")
        print("   • customtkinter")
        print("   • matplotlib") 
        print("   • numpy")
        
    finally:
        print("\n✅ Programa terminado.")


if __name__ == "__main__":
    main()