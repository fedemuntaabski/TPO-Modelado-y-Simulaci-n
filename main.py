#!/usr/bin/env python3
"""
Simulador Matemático Avanzado - Versión 3.0
Sistema integrado para métodos numéricos con interfaz gráfica moderna

Características:
- Interfaz PyQt6 con tema oscuro profesional
- Métodos numéricos completos (raíces, integración, EDO, etc.)
- Teclado virtual optimizado para funciones matemáticas
- Visualización avanzada y análisis detallado
- Arquitectura modular y extensible

Autores: Equipo TPO Modelado y Simulación
Fecha: 2025
Versión: 3.0
"""

import sys
import subprocess
import importlib
import logging
import os
from pathlib import Path
from typing import List, Optional

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simulator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Dependencias requeridas con versiones mínimas
REQUIRED_PACKAGES = {
    'PyQt6': '6.0.0',
    'numpy': '1.21.0', 
    'scipy': '1.7.0',
    'matplotlib': '3.5.0',
    'sympy': '1.9.0'
}

def show_startup_banner() -> None:
    """Muestra el banner de inicio optimizado."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════╗
║                 🧮 Análisis Avanzado y Simulación Numérica               ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

🚀 CARACTERÍSTICAS PRINCIPALES:
   ✨ Interfaz PyQt6 con tema oscuro profesional
   🎯 Teclado virtual optimizado (funciones matemáticas)
   📊 Análisis detallado y visualización avanzada
   🔄 Animaciones suaves y efectos visuales
   📈 Visualización interactiva con matplotlib
   🔧 Arquitectura modular y extensible

🔧 MÉTODOS DISPONIBLES:
   • Búsqueda de raíces: Bisección, Newton-Raphson, Secante
   • Integración numérica: Trapezoidal, Simpson
   • Ecuaciones diferenciales: Euler, Runge-Kutta
   • Interpolación: Lagrange, Newton
   • Sistemas lineales: Gauss, Jacobi, Gauss-Seidel
"""
    print(banner)

def check_and_install_dependencies() -> bool:
    """
    Verifica e instala las dependencias necesarias.
    
    Returns:
        bool: True si todas las dependencias están disponibles, False si hay errores.
    """
    print("🔍 Verificando dependencias del sistema...")
    logger.info("Iniciando verificación de dependencias")
    
    missing_packages = []
    
    for package, min_version in REQUIRED_PACKAGES.items():
        try:
            if package == 'PyQt6':
                import PyQt6.QtWidgets
                logger.info(f"PyQt6 encontrado")
            else:
                module = importlib.import_module(package)
                version = getattr(module, '__version__', 'unknown')
                logger.info(f"{package} {version} encontrado")
            
            print(f"✅ {package} - OK")
            
        except ImportError as e:
            missing_packages.append(package)
            print(f"❌ {package} - FALTANTE")
            logger.warning(f"Dependencia faltante: {package} - {e}")
    
    if missing_packages:
        print(f"\n📦 Instalando dependencias faltantes: {', '.join(missing_packages)}")
        
        for package in missing_packages:
            try:
                print(f"   📥 Instalando {package}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package,
                    "--quiet", "--upgrade"
                ])
                print(f"   ✅ {package} instalado correctamente")
                logger.info(f"Dependencia {package} instalada exitosamente")
                
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Error instalando {package}: {e}")
                logger.error(f"Falló la instalación de {package}: {e}")
                return False
    
    print("✅ Todas las dependencias están disponibles!")
    logger.info("Verificación de dependencias completada exitosamente")
    return True

def validate_python_version() -> bool:
    """
    Valida que la versión de Python sea compatible.
    
    Returns:
        bool: True si la versión es compatible, False en caso contrario.
    """
    min_python = (3, 8)
    current_python = sys.version_info[:2]
    
    if current_python < min_python:
        print(f"❌ Python {min_python[0]}.{min_python[1]}+ requerido. "
              f"Versión actual: {current_python[0]}.{current_python[1]}")
        logger.error(f"Versión de Python incompatible: {current_python}")
        return False
    
    print(f"✅ Python {current_python[0]}.{current_python[1]} - Compatible")
    logger.info(f"Versión de Python validada: {current_python}")
    return True

def setup_environment() -> bool:
    """
    Configura el entorno de ejecución.
    
    Returns:
        bool: True si el setup es exitoso, False en caso contrario.
    """
    try:
        # Verificar estructura de directorios
        required_dirs = ['gui', 'numerics']
        for dir_name in required_dirs:
            if not Path(dir_name).exists():
                logger.error(f"Directorio requerido no encontrado: {dir_name}")
                print(f"❌ Directorio faltante: {dir_name}")
                return False
        
        # Configurar paths
        sys.path.insert(0, str(Path(__file__).parent))
        
        # Configurar matplotlib backend
        import matplotlib
        matplotlib.use('Qt5Agg')
        
        logger.info("Entorno configurado correctamente")
        return True
        
    except Exception as e:
        logger.error(f"Error configurando entorno: {e}")
        print(f"❌ Error en configuración: {e}")
        return False

def launch_application() -> int:
    """
    Lanza la aplicación principal.
    
    Returns:
        int: Código de salida de la aplicación.
    """
    try:
        print("🎨 Inicializando interfaz gráfica...")
        logger.info("Iniciando aplicación GUI")
        
        from PyQt6.QtWidgets import QApplication
        from gui.main_window import MathSimulatorApp
        
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        app.setApplicationName("Simulador Matemático Avanzado")
        app.setApplicationVersion("3.0")
        app.setOrganizationName("TPO Modelado y Simulación")
        
        # Crear y mostrar ventana principal
        main_window = MathSimulatorApp()
        main_window.show()
        
        print("🚀 Aplicación iniciada correctamente!")
        print("📱 Interfaz gráfica disponible en ventana principal")
        
        # Mostrar instrucciones de uso
        print("\n" + "="*50)
        print("INSTRUCCIONES DE USO:")
        print("• Use el teclado virtual para ingresar funciones")
        print("• Explore las pestañas para diferentes métodos")
        print("• Utilice las herramientas de análisis en cada pestaña")
        print("• Disfrute del tema oscuro profesional")
        print("="*50)
        
        logger.info("Interfaz gráfica mostrada exitosamente")
        
        # Ejecutar loop principal
        return app.exec()
        
    except ImportError as e:
        logger.error(f"Error importando módulos GUI: {e}")
        print(f"❌ Error importando componentes: {e}")
        print("💡 Verifique que los módulos gui/ estén disponibles")
        return 1
        
    except Exception as e:
        logger.error(f"Error inesperado en aplicación: {e}")
        print(f"❌ Error inesperado: {e}")
        return 1

def main() -> int:
    """
    Función principal del simulador.
    
    Returns:
        int: Código de salida del programa.
    """
    try:
        # Mostrar banner de inicio
        show_startup_banner()
        
        # Validar versión de Python
        if not validate_python_version():
            return 1
        
        # Verificar e instalar dependencias
        if not check_and_install_dependencies():
            return 1
        
        # Configurar entorno
        if not setup_environment():
            return 1
        
        # Lanzar aplicación
        return launch_application()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Aplicación interrumpida por el usuario")
        logger.info("Aplicación interrumpida por KeyboardInterrupt")
        return 0
        
    except Exception as e:
        logger.error(f"Error crítico en main: {e}")
        print(f"\n❌ Error crítico: {e}")
        print("📋 Revise el archivo simulator.log para más detalles")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
