#!/usr/bin/env python3
"""
Módulo de Lanzamiento de Aplicación - Simulador Matemático Avanzado
Contiene funciones para inicializar y lanzar la interfaz gráfica

Características:
- Inicialización de QApplication
- Creación de la ventana principal
- Configuración de la aplicación Qt
- Manejo de errores de importación

Autores: Equipo TPO Modelado y Simulación
Fecha: 2025
Versión: 3.0
"""

import sys
import logging

logger = logging.getLogger(__name__)

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
        from gui.components import MathSimulatorApp

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
