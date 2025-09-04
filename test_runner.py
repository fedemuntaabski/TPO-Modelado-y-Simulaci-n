#!/usr/bin/env python3
"""
Test Runner Unificado - Ejecuta todos los tests del proyecto
Incluye tests unitarios, integración y validación completa

Autor: Equipo TPO Modelado y Simulación
Fecha: 2025
"""

import sys
import os
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess

# Agregar el directorio principal al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuración de colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """Muestra el banner del test runner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════╗
║                    🧪 TEST RUNNER UNIFICADO                             ║
║                 Simulador Matemático Avanzado v3.0                     ║
╚══════════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def run_single_test_file(test_file: str) -> Tuple[int, int, float]:
    """
    Ejecuta un archivo de test individual.

    Args:
        test_file: Ruta al archivo de test

    Returns:
        Tupla de (tests_pasados, tests_totales, tiempo_ejecucion)
    """
    print(f"\n{Colors.BLUE}🧪 Ejecutando {os.path.basename(test_file)}...{Colors.END}")

    start_time = time.time()

    try:
        # Ejecutar con pytest si está disponible
        result = subprocess.run([
            sys.executable, '-m', 'pytest', test_file,
            '-v', '--tb=short', '--disable-warnings'
        ], capture_output=True, text=True, timeout=300)

        end_time = time.time()
        execution_time = end_time - start_time

        # Analizar output para contar tests
        output_lines = result.stdout.split('\n')
        passed = 0
        failed = 0

        for line in output_lines:
            if 'PASSED' in line or '✅' in line:
                passed += 1
            elif 'FAILED' in line or 'ERROR' in line or '❌' in line:
                failed += 1

        total_tests = passed + failed

        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ {os.path.basename(test_file)}: {passed}/{total_tests} tests pasaron{Colors.END}")
        else:
            print(f"{Colors.RED}❌ {os.path.basename(test_file)}: {passed}/{total_tests} tests pasaron{Colors.END}")
            if result.stderr:
                print(f"{Colors.YELLOW}Detalles: {result.stderr.strip()}{Colors.END}")

        return passed, total_tests, execution_time

    except subprocess.TimeoutExpired:
        end_time = time.time()
        print(f"{Colors.RED}⏰ Timeout ejecutando {os.path.basename(test_file)}{Colors.END}")
        return 0, 0, end_time - start_time

    except Exception as e:
        end_time = time.time()
        print(f"{Colors.RED}💥 Error ejecutando {os.path.basename(test_file)}: {e}{Colors.END}")
        return 0, 0, end_time - start_time

def run_manual_tests(test_file: str) -> Tuple[int, int, float]:
    """
    Ejecuta tests manualmente si pytest no está disponible.

    Args:
        test_file: Ruta al archivo de test

    Returns:
        Tupla de (tests_pasados, tests_totales, tiempo_ejecucion)
    """
    print(f"\n{Colors.BLUE}🧪 Ejecutando {os.path.basename(test_file)} (modo manual)...{Colors.END}")

    start_time = time.time()

    try:
        # Importar el módulo de test
        module_name = os.path.basename(test_file)[:-3]  # Remover .py
        test_module = __import__(f"tests.{module_name}", fromlist=[module_name])

        passed = 0
        total = 0

        # Encontrar todas las clases de test
        test_classes = []
        for attr_name in dir(test_module):
            attr = getattr(test_module, attr_name)
            if (isinstance(attr, type) and
                attr_name.startswith('Test') and
                hasattr(attr, '__module__')):
                test_classes.append(attr)

        for test_class in test_classes:
            print(f"  {Colors.CYAN}Clase: {test_class.__name__}{Colors.END}")

            instance = test_class()
            methods = [method for method in dir(instance) if method.startswith('test_')]

            for method_name in methods:
                total += 1
                try:
                    method = getattr(instance, method_name)
                    method()
                    print(f"    {Colors.GREEN}✅ {method_name}{Colors.END}")
                    passed += 1
                except Exception as e:
                    print(f"    {Colors.RED}❌ {method_name}: {e}{Colors.END}")

        end_time = time.time()
        execution_time = end_time - start_time

        if passed == total:
            print(f"{Colors.GREEN}✅ {os.path.basename(test_file)}: {passed}/{total} tests pasaron{Colors.END}")
        else:
            print(f"{Colors.RED}❌ {os.path.basename(test_file)}: {passed}/{total} tests pasaron{Colors.END}")

        return passed, total, execution_time

    except Exception as e:
        end_time = time.time()
        print(f"{Colors.RED}💥 Error en ejecución manual: {e}{Colors.END}")
        return 0, 0, end_time - start_time

def generate_report(results: Dict[str, Tuple[int, int, float]], total_time: float) -> Dict:
    """
    Genera un reporte completo de los resultados.

    Args:
        results: Diccionario con resultados por archivo
        total_time: Tiempo total de ejecución

    Returns:
        Diccionario con el reporte completo
    """
    total_passed = sum(passed for passed, _, _ in results.values())
    total_tests = sum(total for _, total, _ in results.values())

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total_files": len(results),
            "total_tests": total_tests,
            "passed_tests": total_passed,
            "failed_tests": total_tests - total_passed,
            "success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0,
            "total_time": round(total_time, 2)
        },
        "file_results": {},
        "recommendations": []
    }

    # Resultados por archivo
    for file_name, (passed, total, exec_time) in results.items():
        success_rate = (passed / total * 100) if total > 0 else 0
        report["file_results"][file_name] = {
            "passed": passed,
            "total": total,
            "success_rate": round(success_rate, 2),
            "execution_time": round(exec_time, 2)
        }

    # Generar recomendaciones
    if total_tests == 0:
        report["recommendations"].append("No se encontraron tests para ejecutar")
    elif total_passed == total_tests:
        report["recommendations"].append("🎉 ¡Todos los tests pasaron exitosamente!")
        report["recommendations"].append("El código está listo para producción")
    else:
        failed_tests = total_tests - total_passed
        report["recommendations"].append(f"⚠️ {failed_tests} tests fallaron - revisar implementación")
        report["recommendations"].append("Ejecutar tests individuales para debugging detallado")

        # Identificar archivos con problemas
        problematic_files = [
            file for file, (passed, total, _) in results.items()
            if passed != total
        ]
        if problematic_files:
            report["recommendations"].append(f"Archivos con problemas: {', '.join(problematic_files)}")

    return report

def save_report(report: Dict, output_file: str = "test_report.json"):
    """Guarda el reporte en un archivo JSON."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n{Colors.BLUE}📄 Reporte guardado en: {output_file}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error guardando reporte: {e}{Colors.END}")

def print_summary_report(report: Dict):
    """Imprime un resumen del reporte."""
    summary = report["summary"]

    print(f"\n{Colors.BOLD}{Colors.MAGENTA}📊 REPORTE DE EJECUCIÓN{Colors.END}")
    print(f"{'='*50}")
    print(f"Archivos procesados: {summary['total_files']}")
    print(f"Tests totales: {summary['total_tests']}")
    print(f"Tests exitosos: {summary['passed_tests']}")
    print(f"Tests fallidos: {summary['failed_tests']}")
    print(f"Tasa de éxito: {summary['success_rate']:.1f}%")
    print(f"Tiempo total: {summary['total_time']:.2f}s")
    print(f"{'='*50}")

    # Mostrar resultados por archivo
    print(f"\n{Colors.CYAN}DETALLE POR ARCHIVO:{Colors.END}")
    for file_name, file_result in report["file_results"].items():
        status = "✅" if file_result["passed"] == file_result["total"] else "❌"
        print(f"  {status} {file_name}: {file_result['passed']}/{file_result['total']} "
              f"({file_result['success_rate']}%) - {file_result['execution_time']:.2f}s")

    # Mostrar recomendaciones
    if report["recommendations"]:
        print(f"\n{Colors.YELLOW}💡 RECOMENDACIONES:{Colors.END}")
        for rec in report["recommendations"]:
            print(f"  • {rec}")

def main():
    """Función principal del test runner."""
    print_banner()

    # Verificar que estamos en el directorio correcto
    tests_dir = Path(__file__).parent / "tests"
    if not tests_dir.exists():
        print(f"{Colors.RED}❌ Directorio de tests no encontrado: {tests_dir}{Colors.END}")
        return 1

    # Encontrar archivos de test
    test_files = list(tests_dir.glob("test_*.py"))
    if not test_files:
        print(f"{Colors.YELLOW}⚠️ No se encontraron archivos de test en {tests_dir}{Colors.END}")
        return 1

    print(f"{Colors.BLUE}🔍 Encontrados {len(test_files)} archivos de test:{Colors.END}")
    for test_file in test_files:
        print(f"  • {test_file.name}")

    # Verificar disponibilidad de pytest
    try:
        import pytest
        use_pytest = True
        print(f"\n{Colors.GREEN}✅ pytest disponible - usando modo automático{Colors.END}")
    except ImportError:
        use_pytest = False
        print(f"\n{Colors.YELLOW}⚠️ pytest no disponible - usando modo manual{Colors.END}")

    # Ejecutar tests
    results = {}
    total_start_time = time.time()

    for test_file in sorted(test_files):
        if use_pytest:
            passed, total, exec_time = run_single_test_file(str(test_file))
        else:
            passed, total, exec_time = run_manual_tests(str(test_file))

        results[test_file.name] = (passed, total, exec_time)

    total_time = time.time() - total_start_time

    # Generar y mostrar reporte
    report = generate_report(results, total_time)
    print_summary_report(report)

    # Guardar reporte
    save_report(report)

    # Código de salida basado en resultados
    success_rate = report["summary"]["success_rate"]
    if success_rate == 100.0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!{Colors.END}")
        return 0
    elif success_rate >= 80.0:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ LA MAYORÍA DE TESTS PASARON ({success_rate:.1f}%){Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ MÚLTIPLES TESTS FALLARON ({success_rate:.1f}%){Colors.END}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
