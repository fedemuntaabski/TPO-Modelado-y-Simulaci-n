#!/usr/bin/env python3
"""
Demostración de las mejoras en la refactorización de UI.

Este script muestra las nuevas funcionalidades implementadas:
1. Constantes centralizadas
2. Gestor de errores unificado
3. Validación en tiempo real
4. Mensajes de error amigables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.components.constants import (
    VALIDATION, UI, PLOT, COLORS,
    ERROR_MESSAGES, ValidationErrorCodes
)
from src.ui.components.error_handler import handle_error, handle_validation_error, ErrorSeverity
from src.ui.components.validation_mixins import AdvancedValidationMixin


def demo_constants():
    """Demostrar el uso de constantes centralizadas"""
    print("=== DEMO: Constantes Centralizadas ===")
    print(f"Tolerancia por defecto: {VALIDATION.DEFAULT_TOLERANCE}")
    print(f"Ancho de ventana: {UI.WINDOW_WIDTH}")
    print(f"Alto de ventana: {UI.WINDOW_HEIGHT}")
    print(f"Color de éxito: {COLORS.SUCCESS}")
    print(f"Ancho de figura de plot: {PLOT.FIGURE_WIDTH}")
    print()


def demo_error_handling():
    """Demostrar el gestor de errores unificado"""
    print("=== DEMO: Gestor de Errores Unificado ===")

    # Error de validación
    print("1. Error de validación:")
    error_msg = handle_validation_error(ValidationErrorCodes.INVALID_FUNCTION, "función")
    print(f"   Mensaje: {error_msg}")

    # Error técnico convertido a mensaje amigable
    print("\n2. Error técnico convertido:")
    try:
        1 / 0  # Provocar error
    except ZeroDivisionError as e:
        handle_error(e, "cálculo matemático", ErrorSeverity.ERROR, show_dialog=False)
        print("   Error manejado y convertido a mensaje amigable")

    print()


def demo_validation():
    """Demostrar validadores avanzados"""
    print("=== DEMO: Validadores Avanzados ===")

    validator = AdvancedValidationMixin()

    # Validar función
    print("1. Validación de función:")
    is_valid, msg = validator.validate_function("x**2 + 2*x + 1")
    print(f"   'x**2 + 2*x + 1' -> Válida: {is_valid}")

    is_valid, msg = validator.validate_function("x**2 + ;")
    print(f"   'x**2 + ;' -> Válida: {is_valid}, Mensaje: {msg}")

    # Validar números
    print("\n2. Validación numérica:")
    is_valid, msg = validator.validate_numeric("3.14")
    print(f"   '3.14' -> Válida: {is_valid}")

    is_valid, msg = validator.validate_numeric("abc")
    print(f"   'abc' -> Válida: {is_valid}, Mensaje: {msg}")

    # Validar rango
    print("\n3. Validación de rango:")
    is_valid, msg = validator.validate_range("0", "5")
    print(f"   Rango [0, 5] -> Válido: {is_valid}")

    is_valid, msg = validator.validate_range("5", "0")
    print(f"   Rango [5, 0] -> Válido: {is_valid}, Mensaje: {msg}")

    print()


def demo_tab_refactoring():
    """Demostrar las refactorizaciones específicas de las pestañas"""
    print("=== DEMO: Refactorización de Pestañas ===")

    # Probar importación de pestañas refactorizadas
    try:
        from src.ui.tabs.integration_tab import IntegrationTab
        from src.ui.tabs.ode_tab import ODETab
        from src.ui.tabs.finite_diff_tab import FiniteDiffTab
        from src.ui.tabs.newton_cotes_tab import NewtonCotesTab
        from src.ui.tabs.roots_tab import RootsTab
        print("✅ Todas las pestañas se importan correctamente")
    except ImportError as e:
        print(f"❌ Error importando pestañas: {e}")
        return

    # Verificar métodos refactorizados
    print("\n1. Verificando métodos de IntegrationTab:")
    integration_methods = ['trapezoid_method', 'simpson_13_method', 'simpson_38_method', 'compare_all_methods']
    for method in integration_methods:
        if hasattr(IntegrationTab, method):
            print(f"   ✅ {method}")
        else:
            print(f"   ❌ {method} no encontrado")

    print("\n2. Verificando métodos de ODETab:")
    ode_methods = ['euler_method', 'rk2_method', 'rk4_method', 'compare_all_methods']
    for method in ode_methods:
        if hasattr(ODETab, method):
            print(f"   ✅ {method}")
        else:
            print(f"   ❌ {method} no encontrado")

    print("\n3. Verificando constantes en FiniteDiffTab:")
    # Verificar que usa las constantes correctas
    try:
        from src.ui.tabs.finite_diff_tab import VALIDATION
        print(f"   ✅ VALIDATION.MIN_POINTS: {VALIDATION.MIN_POINTS}")
        print(f"   ✅ VALIDATION.MAX_X_VALUE: {VALIDATION.MAX_X_VALUE}")
    except:
        print("   ❌ Constantes no accesibles en FiniteDiffTab")

    print("\n4. Verificando configuración de validación en NewtonCotesTab:")
    try:
        from src.ui.tabs.newton_cotes_tab import VALIDATION
        print(f"   ✅ VALIDATION.MIN_SUBDIVISIONS: {VALIDATION.MIN_SUBDIVISIONS}")
        print(f"   ✅ VALIDATION.MAX_SUBDIVISIONS: {VALIDATION.MAX_SUBDIVISIONS}")
    except:
        print("   ❌ Constantes no accesibles en NewtonCotesTab")

    print()


def demo_configurations():
    """Demostrar configuraciones por defecto"""
    print("=== DEMO: Configuraciones por Defecto ===")

    from src.ui.components.constants import DEFAULT_CONFIGS

    for method, config in DEFAULT_CONFIGS.items():
        print(f"{method}:")
        for key, value in config.items():
            print(f"  {key}: {value}")
        print()


def main():
    """Función principal de demostración"""
    print("🚀 DEMOSTRACIÓN DE REFACTORIZACIÓN DE UI")
    print("=" * 50)
    print()

    demo_constants()
    demo_error_handling()
    demo_validation()
    demo_tab_refactoring()
    demo_configurations()

    print("✅ Demostración completada exitosamente!")
    print("\nLas mejoras implementadas incluyen:")
    print("• Constantes centralizadas para fácil mantenimiento")
    print("• Gestor de errores unificado con mensajes amigables")
    print("• Validadores avanzados reutilizables")
    print("• Configuraciones por defecto organizadas")
    print("• Arquitectura preparada para validación en tiempo real")


if __name__ == "__main__":
    main()
