#!/usr/bin/env python3
"""
Simulador Matemático Avanzado
Sistema integrado para métodos numéricos con interfaz gráfica moderna

Autores: Equipo TPO Modelado y Simulación
Fecha: 2025
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

# Lista de dependencias requeridas
REQUIRED_PACKAGES = [
    'PyQt6',
    'numpy',
    'scipy',
    'matplotlib',
    'sympy'
]

def check_and_install_dependencies():
    """
    Verifica e instala las dependencias necesarias si no están disponibles
    """
    print("🔍 Verificando dependencias...")
    
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        try:
            if package == 'PyQt6':
                importlib.import_module('PyQt6.QtWidgets')
            else:
                importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - FALTANTE")
    
    if missing_packages:
        print(f"\n📦 Instalando paquetes faltantes: {', '.join(missing_packages)}")
        for package in missing_packages:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ])
                print(f"✅ {package} instalado correctamente")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error instalando {package}: {e}")
                return False
    
    print("🎉 Todas las dependencias están disponibles!\n")
    return True

def main():
    """
    Función principal del programa
    """
    print("=" * 60)
    print("🧮 SIMULADOR MATEMÁTICO AVANZADO")
    print("   Métodos Numéricos con Interfaz Gráfica")
    print("=" * 60)
    
    # Verificar e instalar dependencias
    if not check_and_install_dependencies():
        print("❌ Error en la instalación de dependencias. Abortando...")
        sys.exit(1)
    
    # Importar módulos después de verificar dependencias
    try:
        from gui.main_window import MathSimulatorApp
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QIcon
        
        # Crear la aplicación Qt
        app = QApplication(sys.argv)
        app.setApplicationName("Simulador Matemático Avanzado")
        app.setApplicationVersion("1.0")
        app.setOrganizationName("TPO Modelado y Simulación")
        
        # Configurar estilo moderno
        app.setStyle('Fusion')
        
        # Crear y mostrar la ventana principal
        window = MathSimulatorApp()
        window.show()
        
        print("🚀 Aplicación iniciada correctamente!")
        print("📱 Interfaz gráfica disponible en ventana principal\n")
        
        # Ejecutar el bucle de eventos
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"❌ Error importando módulos de la GUI: {e}")
        print("🔧 Asegúrate de que todos los archivos estén en su lugar")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
