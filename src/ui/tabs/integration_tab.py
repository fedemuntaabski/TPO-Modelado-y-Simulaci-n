"""
Pestaña de integración numérica.

Implementa la interfaz gráfica para los métodos de integración numérica
siguiendo principios SOLID y DRY.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional

from src.ui.components.base_tab import BaseTab
from src.core.integration import NumericalIntegrator, create_function_from_string
from config.settings import NUMERICAL_CONFIG


class IntegrationTab(BaseTab):
    """
    Pestaña para integración numérica.
    Hereda funcionalidad común de BaseTab (principio DRY).
    """
    
    def __init__(self, parent):
        super().__init__(parent, "∫ Integración Numérica")
        self.integrator = NumericalIntegrator(use_scipy=True)
    
    def create_content(self):
        """Crear contenido específico para integración (Template Method)"""
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Métodos numéricos para calcular integrales definidas",
            font=ctk.CTkFont(size=14)
        )
        desc_label.grid(row=0, column=0, pady=10, padx=20, sticky="ew")
        
        # Crear sección de entrada
        input_data = {
            "Función f(x):": "x**2",
            "Límite inferior (a):": "0",
            "Límite superior (b):": "2",
            "Subdivisiones (n):": "10"
        }
        self.entries = self.create_input_section(input_data)
        
        # Crear sección de métodos
        methods = [
            ("Trapecio", self.trapezoid_method),
            ("Simpson 1/3", self.simpson_13_method),
            ("Simpson 3/8", self.simpson_38_method),
            ("Comparar Todos", self.compare_all_methods)
        ]
        self.create_methods_section(methods)
        
        # Crear sección de resultados
        self.results_frame, self.results_text, self.plot_frame = self.create_results_section()
    
    def trapezoid_method(self):
        """Ejecutar regla del trapecio"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries,
                ["función_fx", "límite_inferior_a", "límite_superior_b", "subdivisiones_n"]
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función
            f = create_function_from_string(values["función_fx"])
            
            # Ejecutar método
            result = self.integrator.trapezoid_rule(
                f, values["límite_inferior_a"], values["límite_superior_b"], values["subdivisiones_n"]
            )
            
            # Mostrar resultados
            self._display_results(result)
            
            # Crear gráfico
            self._plot_integration(f, result)
            
        except Exception as e:
            self.show_error(f"Error en trapecio: {e}")
    
    def simpson_13_method(self):
        """Ejecutar regla de Simpson 1/3"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries,
                ["función_fx", "límite_inferior_a", "límite_superior_b", "subdivisiones_n"]
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función
            f = create_function_from_string(values["función_fx"])
            
            # Ejecutar método
            result = self.integrator.simpson_13_rule(
                f, values["límite_inferior_a"], values["límite_superior_b"], values["subdivisiones_n"]
            )
            
            # Mostrar resultados
            self._display_results(result)
            
            # Crear gráfico
            self._plot_integration(f, result)
            
        except Exception as e:
            self.show_error(f"Error en Simpson 1/3: {e}")
    
    def simpson_38_method(self):
        """Ejecutar regla de Simpson 3/8"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries,
                ["función_fx", "límite_inferior_a", "límite_superior_b", "subdivisiones_n"]
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función
            f = create_function_from_string(values["función_fx"])
            
            # Ejecutar método
            result = self.integrator.simpson_38_rule(
                f, values["límite_inferior_a"], values["límite_superior_b"], values["subdivisiones_n"]
            )
            
            # Mostrar resultados
            self._display_results(result)
            
            # Crear gráfico
            self._plot_integration(f, result)
            
        except Exception as e:
            self.show_error(f"Error en Simpson 3/8: {e}")
    
    def compare_all_methods(self):
        """Comparar todos los métodos de integración"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries,
                ["función_fx", "límite_inferior_a", "límite_superior_b", "subdivisiones_n"]
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función
            f = create_function_from_string(values["función_fx"])
            
            # Ejecutar todos los métodos
            results = {}
            results['trapezoid'] = self.integrator.trapezoid_rule(
                f, values["límite_inferior_a"], values["límite_superior_b"], values["subdivisiones_n"]
            )
            results['simpson_13'] = self.integrator.simpson_13_rule(
                f, values["límite_inferior_a"], values["límite_superior_b"], values["subdivisiones_n"]
            )
            results['simpson_38'] = self.integrator.simpson_38_rule(
                f, values["límite_inferior_a"], values["límite_superior_b"], values["subdivisiones_n"]
            )
            
            # Mostrar comparación
            self._display_comparison(results)
            
            # Crear gráfico comparativo
            self._plot_comparison(f, results)
            
        except Exception as e:
            self.show_error(f"Error en comparación: {e}")
    
    def _display_results(self, result):
        """Mostrar resultados de un método específico"""
        # Datos principales
        main_data = {
            "Función": self.entries["función_fx"].get(),
            "Límites": f"[{self.entries['límite_inferior_a'].get()}, {self.entries['límite_superior_b'].get()}]",
            "Método": result.method,
            "Subdivisiones": result.subdivisions,
            "Paso (h)": f"{result.step_size:.6f}",
            "Integral aproximada": f"{result.value:.8f}"
        }
        
        # Agregar información exacta si está disponible
        if result.exact_value is not None:
            main_data["Valor exacto"] = f"{result.exact_value:.8f}"
            main_data["Error absoluto"] = f"{result.error:.2e}"
            main_data["Error relativo"] = f"{result.relative_error:.4f}%"
        
        # Secciones adicionales
        sections = {}
        
        # Información del método
        method_info = []
        if "trapecio" in result.method.lower():
            method_info = [
                "Aproxima el área usando trapecios",
                "Error: O(h²) donde h = (b-a)/n",
                "Fórmula: h[f(a)/2 + f(a+h) + ... + f(b)/2]",
                "Funciona bien para funciones suaves"
            ]
        elif "simpson 1/3" in result.method.lower():
            method_info = [
                "Aproxima usando parábolas (polinomios de grado 2)",
                "Error: O(h⁴) donde h = (b-a)/n",
                "Requiere n par (número de subdivisiones)",
                "Mayor precisión que trapecio para funciones suaves"
            ]
        elif "simpson 3/8" in result.method.lower():
            method_info = [
                "Aproxima usando polinomios cúbicos",
                "Error: O(h⁴) donde h = (b-a)/n",
                "Requiere n múltiplo de 3",
                "Similar precisión a Simpson 1/3"
            ]
        
        if method_info:
            sections["CARACTERÍSTICAS DEL MÉTODO"] = method_info
        
        # Datos de computación si están disponibles
        if result.computation_data:
            comp_data = result.computation_data
            if 'formula' in comp_data:
                sections["FÓRMULA UTILIZADA"] = [comp_data['formula']]
        
        # Recomendaciones
        recommendations = []
        if result.error is not None:
            if result.error < 1e-8:
                recommendations.append("✅ Excelente precisión obtenida")
            elif result.error < 1e-6:
                recommendations.append("✅ Buena precisión")
            elif result.error < 1e-4:
                recommendations.append("⚠️ Precisión moderada - considere aumentar n")
            else:
                recommendations.append("❌ Baja precisión - aumente n significativamente")
        
        recommendations.extend([
            "• Para mayor precisión, use Simpson 1/3 en lugar de trapecio",
            "• Duplique n para reducir el error aproximadamente 4 veces (Simpson)",
            "• Duplique n para reducir el error aproximadamente 4 veces (trapecio)"
        ])
        
        sections["RECOMENDACIONES"] = recommendations
        
        # Formatear y mostrar
        formatted_text = self.format_result_text(result.method, main_data, sections)
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", formatted_text)
    
    def _display_comparison(self, results):
        """Mostrar comparación de todos los métodos"""
        main_data = {
            "Función": self.entries["función_fx"].get(),
            "Límites": f"[{self.entries['límite_inferior_a'].get()}, {self.entries['límite_superior_b'].get()}]",
            "Subdivisiones originales": self.entries['subdivisiones_n'].get()
        }
        
        # Tabla comparativa
        comparison_lines = []
        comparison_lines.append(f"{'Método':<20} {'Aproximación':<15} {'Error':<15} {'Error Rel.':<12}")
        comparison_lines.append("-" * 70)
        
        # Obtener valor exacto de referencia
        exact_value = None
        for result in results.values():
            if result.exact_value is not None:
                exact_value = result.exact_value
                break
        
        if exact_value is not None:
            main_data["Valor exacto"] = f"{exact_value:.8f}"
        
        # Encontrar el mejor método
        best_method = None
        best_error = float('inf')
        
        for name, result in results.items():
            error_str = f"{result.error:.2e}" if result.error is not None else "N/A"
            rel_error_str = f"{result.relative_error:.4f}%" if result.relative_error is not None else "N/A"
            
            comparison_lines.append(
                f"{result.method:<20} {result.value:<15.8f} {error_str:<15} {rel_error_str:<12}"
            )
            
            # Actualizar mejor método
            if result.error is not None and result.error < best_error:
                best_error = result.error
                best_method = result.method
        
        sections = {
            "COMPARACIÓN DE MÉTODOS": comparison_lines
        }
        
        if best_method:
            sections["ANÁLISIS"] = [
                f"✅ Mejor método: {best_method}",
                f"   Error mínimo: {best_error:.2e}",
                "",
                "📊 Orden de precisión teórico:",
                "   • Trapecio: O(h²)",
                "   • Simpson 1/3: O(h⁴)",
                "   • Simpson 3/8: O(h⁴)",
                "",
                "💡 Para funciones suaves, Simpson suele ser superior",
                "💡 Para funciones con discontinuidades, trapecio puede ser más robusto"
            ]
        
        # Formatear y mostrar
        formatted_text = self.format_result_text("COMPARACIÓN DE MÉTODOS DE INTEGRACIÓN", main_data, sections)
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", formatted_text)
    
    def _plot_integration(self, f, result):
        """Crear gráfico de la integración"""
        fig, canvas = self.create_matplotlib_plot(self.plot_frame)
        ax = fig.add_subplot(111)
        
        # Obtener límites
        a = float(self.entries['límite_inferior_a'].get())
        b = float(self.entries['límite_superior_b'].get())
        n = result.subdivisions
        
        # Rango de x para la función suave
        x_smooth = np.linspace(a - 0.1*(b-a), b + 0.1*(b-a), 1000)
        y_smooth = [f(x) for x in x_smooth]
        
        # Graficar función
        ax.plot(x_smooth, y_smooth, 'cyan', linewidth=2, label='f(x)')
        
        # Puntos de integración
        x_points = np.linspace(a, b, n + 1)
        y_points = [f(x) for x in x_points]
        
        # Rellenar área bajo la curva
        ax.fill_between(x_smooth[(x_smooth >= a) & (x_smooth <= b)], 
                       [f(x) for x in x_smooth[(x_smooth >= a) & (x_smooth <= b)]], 
                       alpha=0.3, color='cyan', label='Área a integrar')
        
        # Mostrar aproximación según el método
        if "trapecio" in result.method.lower():
            # Mostrar trapecios
            for i in range(n):
                x_trap = [x_points[i], x_points[i+1], x_points[i+1], x_points[i]]
                y_trap = [0, 0, y_points[i+1], y_points[i]]
                ax.plot(x_trap, y_trap, 'orange', alpha=0.7, linewidth=1)
        
        elif "simpson" in result.method.lower():
            # Mostrar puntos de evaluación
            ax.plot(x_points, y_points, 'ro', markersize=4, label='Puntos de evaluación')
        
        # Líneas verticales en los límites
        ax.axvline(x=a, color='white', linestyle='--', alpha=0.7, label=f'a = {a}')
        ax.axvline(x=b, color='white', linestyle='--', alpha=0.7, label=f'b = {b}')
        
        self.apply_plot_styling(
            ax,
            title=f"{result.method} (n={n})",
            xlabel="x",
            ylabel="f(x)"
        )
        
        # Agregar texto con el resultado
        ax.text(0.05, 0.95, f"∫f(x)dx ≈ {result.value:.6f}", 
                transform=ax.transAxes, fontsize=12, color='white',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        canvas.draw()
    
    def _plot_comparison(self, f, results):
        """Crear gráfico comparativo de los métodos"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='#2b2b2b')
        
        for ax in [ax1, ax2]:
            ax.set_facecolor('#2b2b2b')
        
        # Obtener límites
        a = float(self.entries['límite_inferior_a'].get())
        b = float(self.entries['límite_superior_b'].get())
        
        # Gráfico 1: Función y métodos
        x_smooth = np.linspace(a - 0.1*(b-a), b + 0.1*(b-a), 1000)
        y_smooth = [f(x) for x in x_smooth]
        
        ax1.plot(x_smooth, y_smooth, 'cyan', linewidth=2, label='f(x)')
        ax1.fill_between(x_smooth[(x_smooth >= a) & (x_smooth <= b)], 
                        [f(x) for x in x_smooth[(x_smooth >= a) & (x_smooth <= b)]], 
                        alpha=0.3, color='cyan')
        
        self.apply_plot_styling(ax1, title="Función a Integrar", xlabel="x", ylabel="f(x)")
        
        # Gráfico 2: Comparación de resultados
        methods = list(results.keys())
        values = [results[method].value for method in methods]
        colors = ['orange', 'green', 'red']
        
        bars = ax2.bar(range(len(methods)), values, color=colors[:len(methods)], alpha=0.7)
        ax2.set_xticks(range(len(methods)))
        ax2.set_xticklabels([results[method].method for method in methods], rotation=45)
        
        # Añadir valor exacto si está disponible
        exact_value = None
        for result in results.values():
            if result.exact_value is not None:
                exact_value = result.exact_value
                break
        
        if exact_value is not None:
            ax2.axhline(y=exact_value, color='white', linestyle='--', 
                       linewidth=2, label=f'Exacto: {exact_value:.6f}')
        
        # Añadir valores en las barras
        for i, (bar, value) in enumerate(zip(bars, values)):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01*abs(height),
                    f'{value:.6f}', ha='center', va='bottom', color='white', fontsize=10)
        
        self.apply_plot_styling(ax2, title="Comparación de Resultados", 
                               xlabel="Método", ylabel="Valor de la Integral")
        
        plt.tight_layout()
        canvas.draw()
