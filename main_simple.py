#!/usr/bin/env python3
"""
Simulador Matemático Avanzado 
"""

# Instalar dependencias mínimas desde requirements_minimal.txt
import subprocess
import sys

try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_minimal.txt'])
    print("Dependencias instaladas correctamente.")
except subprocess.CalledProcessError as e:
    print(f"Error instalando dependencias: {e}")
    sys.exit(1)

import logging

logger = logging.getLogger(__name__)

# Importar componentes modulares
try:
    from src.ui.main_app import MathSimulatorApp
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Advertencia: No se pudieron importar los módulos modulares: {e}")
    print("Asegúrese de que la estructura modular esté disponible")
    MODULES_AVAILABLE = False


def run_simple_app():
    """Ejecuta la aplicación simplificada"""
    try:
        print("🚀 Iniciando Simulador Matemático")
        app = MathSimulatorApp()
        app.mainloop()
        return 0
    except Exception as e:
        logger.error(f"Error en aplicación simplificada: {e}")
        print(f"❌ Error en interfaz simplificada: {e}")
        return 1


if __name__ == "__main__":
    exit_code = run_simple_app()
    sys.exit(exit_code)
