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
import logging

# Importar módulos modulares
from gui.initializer import (
    show_startup_banner,
    check_and_install_dependencies,
    validate_python_version,
    setup_environment
)
from gui.app_launcher import launch_application

logger = logging.getLogger(__name__)

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
