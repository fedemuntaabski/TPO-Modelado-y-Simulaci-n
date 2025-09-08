#!/usr/bin/env python3
"""
Script para verificación de type hints usando mypy.

Ejecuta verificación de tipos en el código fuente.
"""

import subprocess
import sys
from pathlib import Path

def run_mypy_check():
    """Ejecuta mypy en los módulos principales"""
    print("🔍 Verificando type hints con mypy...")

    # Directorios a verificar
    source_dirs = [
        "src/core",
        "src/ui/components",
        "src/ui/tabs"
    ]

    # Configuración de mypy
    mypy_args = [
        "mypy",
        "--ignore-missing-imports",
        "--no-strict-optional",
        "--show-error-codes"
    ] + source_dirs

    try:
        result = subprocess.run(mypy_args, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Todos los type hints son correctos!")
            return True
        else:
            print("❌ Se encontraron errores de type hints:")
            print(result.stdout)
            if result.stderr:
                print("Errores adicionales:")
                print(result.stderr)
            return False

    except FileNotFoundError:
        print("❌ mypy no está instalado. Instale con: pip install mypy")
        return False

if __name__ == "__main__":
    success = run_mypy_check()
    sys.exit(0 if success else 1)
