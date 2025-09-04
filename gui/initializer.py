#!/usr/bin/env python3
"""
Módulo de Inicialización - Simulador Matemático Avanzado
Contiene funciones para inicializar el entorno de la aplicación

Características:
- Verificación e instalación de dependencias
- Validación de versión de Python
- Configuración del entorno
- Banner de inicio

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
