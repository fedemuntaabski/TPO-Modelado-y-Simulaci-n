#!/usr/bin/env python3
"""
Lanzador mejorado del Simulador Matemático Avanzado
Versión 2.0 con mejoras visuales y funcionalidades avanzadas
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

# Lista de dependencias requeridas (mismas que antes)
REQUIRED_PACKAGES = [
    'PyQt6',
    'numpy',
    'scipy',
    'matplotlib',
    'sympy'
]

def show_startup_banner():
    """Muestra el banner de inicio mejorado"""
    print("=" * 70)
    print("🎨 SIMULADOR MATEMÁTICO AVANZADO - VERSIÓN 2.0")
    print("   Interfaz Renovada • Nuevas Funcionalidades • Mejor Rendimiento")
    print("=" * 70)
    print()
    print("🆕 NUEVAS CARACTERÍSTICAS:")
    print("   ✨ Tema oscuro moderno con mejor contraste")
    print("   🎯 Teclado virtual simplificado (solo funciones matemáticas)")
    print("   📊 Comparación avanzada entre métodos numéricos")
    print("   🔄 Animaciones suaves y efectos visuales")
    print("   🚀 Interfaz más intuitiva y profesional")
    print()

def check_and_install_dependencies():
    """Verifica e instala las dependencias necesarias"""
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
                    sys.executable, "-m", "pip", "install", package, "--quiet"
                ])
                print(f"✅ {package} instalado correctamente")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error instalando {package}: {e}")
                return False
    
    print("🎉 Todas las dependencias están disponibles!\n")
    return True

def main():
    """Función principal mejorada"""
    show_startup_banner()
    
    # Verificar e instalar dependencias
    if not check_and_install_dependencies():
        print("❌ Error en la instalación de dependencias. Abortando...")
        input("Presione Enter para salir...")
        sys.exit(1)
    
    # Importar módulos después de verificar dependencias
    try:
        from gui.main_window import MathSimulatorApp
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QIcon, QFont
        
        # Crear la aplicación Qt
        app = QApplication(sys.argv)
        app.setApplicationName("Simulador Matemático Avanzado v2.0")
        app.setApplicationVersion("2.0")
        app.setOrganizationName("Simulador Matemático")
        
        # Configurar fuente global para mejor legibilidad
        font = QFont("Segoe UI", 9)
        app.setFont(font)
        
        # Configurar estilo moderno
        app.setStyle('Fusion')
        
        # Crear y mostrar la ventana principal
        print("🎨 Inicializando interfaz gráfica moderna...")
        window = MathSimulatorApp()
        window.show()
        
        print("🚀 Aplicación iniciada correctamente!")
        print("📱 Interfaz gráfica disponible en ventana principal")
        print("🎯 Nuevas funciones disponibles en todas las pestañas")
        print("\n" + "=" * 50)
        print("INSTRUCCIONES DE USO:")
        print("• Use el teclado virtual simplificado para funciones")
        print("• Explore la nueva pestaña '🔄 Comparación'")
        print("• Disfrute del tema oscuro profesional")
        print("• Observe las nuevas animaciones y efectos")
        print("=" * 50 + "\n")
        
        # Ejecutar el bucle de eventos
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"❌ Error importando módulos de la GUI: {e}")
        print("🔧 Verifique que todos los archivos estén en su lugar")
        input("Presione Enter para salir...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        input("Presione Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    main()
