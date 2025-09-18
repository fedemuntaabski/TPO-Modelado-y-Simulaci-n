#!/usr/bin/env python3
"""
Ejecutor para la aplicación de Aitken desde la carpeta principal.

Uso desde la carpeta principal:
    python run_aitken.py

Este script permite ejecutar la aplicación de Aitken sin necesidad
de cambiar al directorio aitken/.
"""

import sys
import os

def show_banner():
    """Mostrar banner de inicio."""
    banner = """
🚀 EJECUTANDO AITKEN DESDE CARPETA PRINCIPAL
═══════════════════════════════════════════════
"""
    print(banner)

def main():
    """Ejecutar la aplicación de Aitken desde la carpeta principal."""
    
    show_banner()
    
    # Obtener la ruta del directorio aitken
    current_dir = os.path.dirname(os.path.abspath(__file__))
    aitken_dir = os.path.join(current_dir, 'aitken')
    
    print(f"📁 Directorio principal: {current_dir}")
    print(f"📁 Directorio aitken:    {aitken_dir}")
    
    # Verificar que el directorio aitken existe
    if not os.path.exists(aitken_dir):
        print("\n❌ Error: No se encuentra el directorio 'aitken/'")
        print("   Asegúrate de ejecutar este script desde la carpeta principal del proyecto.")
        return 1
    
    # Verificar que main_aitken.py existe
    main_aitken_path = os.path.join(aitken_dir, 'main_aitken.py')
    if not os.path.exists(main_aitken_path):
        print("\n❌ Error: No se encuentra 'aitken/main_aitken.py'")
        return 1
    
    print("✅ Archivos encontrados correctamente")
    
    # Agregar el directorio aitken al path
    sys.path.insert(0, aitken_dir)
    
    print("\n� Cargando aplicación de Aitken...")
    
    try:
        # Importar y ejecutar la aplicación
        import main_aitken
        print("✅ Módulos importados correctamente")
        print("🎯 Iniciando interfaz gráfica...")
        print("   (Cierra la ventana gráfica para terminar)")
        print("=" * 50)
        
        # Ejecutar la aplicación principal
        main_aitken.main()
        
        print("\n👋 Aplicación cerrada.")
        
    except ImportError as e:
        print(f"\n❌ Error de importación: {e}")
        print("   Verifica que todos los archivos estén en aitken/")
        return 1
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación interrumpida por el usuario.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error ejecutando la aplicación: {e}")
        print("   Verifica que las dependencias estén instaladas:")
        print("   • customtkinter")
        print("   • matplotlib")
        print("   • numpy")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except KeyboardInterrupt:
        print("\n👋 Programa interrumpido.")
        exit_code = 0
    sys.exit(exit_code)