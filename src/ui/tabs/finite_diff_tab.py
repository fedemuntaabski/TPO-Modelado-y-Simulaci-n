"""
Pestaña de diferencias finitas.

Implementa la interfaz gráfica para los métodos de diferencias finitas
siguiendo principios SOLID y DRY.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional

from src.ui.components.base_tab import BaseTab
from src.core.finite_differences import FiniteDifferenceCalculator, create_function_from_string
from config.settings import NUMERICAL_CONFIG


class FiniteDiffTab(BaseTab):
    """
    Pestaña para diferencias finitas.
    Hereda funcionalidad común de BaseTab (principio DRY).
    """
    
    def __init__(self, parent):
        super().__init__(parent, "🔢 Diferencias Finitas")
        self.calculator = FiniteDifferenceCalculator()
    
    def create_content(self):
        """Crear contenido específico para diferencias finitas (Template Method)"""
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Métodos de diferencias finitas para calcular derivadas numéricas",
            font=ctk.CTkFont(size=14)
        )
        desc_label.grid(row=0, column=0, pady=10, padx=20, sticky="ew")
        
        # Crear sección de entrada
        input_data = {
            "Función f(x):": "x**3 + 2*x**2 - x + 1",
            "Punto x₀:": "1",
            "Paso h:": "0.1"
        }
        self.entries = self.create_input_section(input_data)
        
        # Agregar selector de orden de derivada
        input_frame = self.content_frame.winfo_children()[1]  # Frame de entrada
        
        ctk.CTkLabel(input_frame, text="Orden de derivada:").grid(
            row=len(input_data), column=0, padx=10, pady=5, sticky="w"
        )
        self.order_combobox = ctk.CTkComboBox(
            input_frame, 
            values=["1", "2", "3"], 
            state="readonly"
        )
        self.order_combobox.grid(row=len(input_data), column=1, padx=10, pady=5, sticky="w")
        self.order_combobox.set("1")
        
        # Crear sección de métodos
        methods = [
            ("Hacia Adelante", self.forward_difference),
            ("Hacia Atrás", self.backward_difference),
            ("Central", self.central_difference),
            ("Análisis Completo", self.complete_analysis)
        ]
        self.create_methods_section(methods)
        
        # Crear sección de resultados
        self.results_frame, self.results_text, self.plot_frame = self.create_results_section()
    
    def forward_difference(self):
        """Ejecutar diferencias hacia adelante"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries,
                ["función_fx", "punto_x₀", "paso_h"]
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función
            f = create_function_from_string(values["función_fx"])
            order = int(self.order_combobox.get())
            
            # Ejecutar método
            result = self.calculator.forward_difference(
                f, values["punto_x₀"], values["paso_h"], order
            )
            
            # Mostrar resultados
            self._display_results(result)
            
            # Crear gráfico
            self._plot_derivative_analysis(f, result, "Hacia Adelante")
            
        except Exception as e:
            self.show_error(f"Error en diferencias hacia adelante: {e}")
    
    def backward_difference(self):
        """Ejecutar diferencias hacia atrás"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries,
                ["función_fx", "punto_x₀", "paso_h"]
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función
            f = create_function_from_string(values["función_fx"])
            order = int(self.order_combobox.get())
            
            # Ejecutar método
            result = self.calculator.backward_difference(
                f, values["punto_x₀"], values["paso_h"], order
            )
            
            # Mostrar resultados
            self._display_results(result)
            
            # Crear gráfico
            self._plot_derivative_analysis(f, result, "Hacia Atrás")
            
        except Exception as e:
            self.show_error(f"Error en diferencias hacia atrás: {e}")
    
    def central_difference(self):
        """Ejecutar diferencias centrales"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries,
                ["función_fx", "punto_x₀", "paso_h"]
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función
            f = create_function_from_string(values["función_fx"])
            order = int(self.order_combobox.get())
            
            # Ejecutar método
            result = self.calculator.central_difference(
                f, values["punto_x₀"], values["paso_h"], order
            )
            
            # Mostrar resultados
            self._display_results(result)
            
            # Crear gráfico
            self._plot_derivative_analysis(f, result, "Central")
            
        except Exception as e:
            self.show_error(f"Error en diferencias centrales: {e}")
    
    def complete_analysis(self):
        """Análisis completo comparando todos los métodos"""
        try:
            # Validar entradas
            is_valid, values, error_msg = self.validate_inputs(
                self.entries,
                ["función_fx", "punto_x₀", "paso_h"]
            )
            
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Crear función
            f = create_function_from_string(values["función_fx"])
            order = int(self.order_combobox.get())
            
            # Ejecutar todos los métodos
            results = self.calculator.compare_all_methods(
                f, values["punto_x₀"], values["paso_h"], order
            )
            
            # Mostrar comparación
            self._display_comparison(results, order)
            
            # Crear gráfico comparativo
            self._plot_comparison(f, results, values["punto_x₀"], values["paso_h"])
            
        except Exception as e:
            self.show_error(f"Error en análisis completo: {e}")
    
    def _display_results(self, result):
        """Mostrar resultados de un método específico"""
        # Datos principales
        main_data = {
            "Función": self.entries["función_fx"].get(),
            "Punto": f"x₀ = {result.point}",
            "Método": result.method,
            "Orden de derivada": result.order,
            "Paso (h)": f"{result.step_size:.6f}",
            "Derivada aproximada": f"{result.value:.10f}"
        }
        
        # Agregar información exacta si está disponible
        if result.exact_value is not None:
            main_data["Valor exacto"] = f"{result.exact_value:.10f}"
            main_data["Error absoluto"] = f"{result.absolute_error:.2e}"
            main_data["Error relativo"] = f"{result.relative_error:.6f}%"
        
        # Secciones adicionales
        sections = {}
        
        # Fórmula utilizada
        if result.formula:
            sections["FÓRMULA UTILIZADA"] = [
                result.formula,
                f"Orden de error: {result.error_order}"
            ]
        
        # Información del método
        method_info = []
        if "adelante" in result.method.lower():
            method_info = [
                "Usa puntos hacia adelante desde x₀",
                "Error: O(h) - convergencia lineal",
                "Útil en bordes izquierdos del dominio",
                "Requiere menos puntos hacia atrás"
            ]
        elif "atrás" in result.method.lower():
            method_info = [
                "Usa puntos hacia atrás desde x₀",
                "Error: O(h) - convergencia lineal", 
                "Útil en bordes derechos del dominio",
                "Requiere menos puntos hacia adelante"
            ]
        elif "central" in result.method.lower():
            method_info = [
                "Usa puntos en ambas direcciones desde x₀",
                "Error: O(h²) - convergencia cuadrática (orden 1)",
                "Generalmente más preciso que forward/backward",
                "Requiere puntos en ambas direcciones"
            ]
        
        if method_info:
            sections["CARACTERÍSTICAS DEL MÉTODO"] = method_info
        
        # Datos de computación
        if result.computation_data:
            comp_data = result.computation_data
            if 'points_used' in comp_data and 'function_evaluations' in comp_data:
                points = comp_data['points_used']
                values = comp_data['function_evaluations']
                
                computation_lines = []
                computation_lines.append("Puntos utilizados en el cálculo:")
                computation_lines.append(f"{'Punto':<12} {'f(x)':<15}")
                computation_lines.append("-" * 30)
                
                for point, value in zip(points, values):
                    computation_lines.append(f"{point:<12.6f} {value:<15.8f}")
                
                sections["DATOS DE COMPUTACIÓN"] = computation_lines
        
        # Recomendaciones
        recommendations = []
        if result.absolute_error is not None:
            if result.absolute_error < 1e-8:
                recommendations.append("✅ Excelente precisión obtenida")
            elif result.absolute_error < 1e-6:
                recommendations.append("✅ Buena precisión")
            elif result.absolute_error < 1e-4:
                recommendations.append("⚠️ Precisión moderada - considere reducir h")
            else:
                recommendations.append("❌ Baja precisión - reduzca h significativamente")
        
        recommendations.extend([
            "• Para mayor precisión, use diferencias centrales",
            "• Reduzca h para mejorar la precisión",
            "• Para funciones suaves, central es generalmente mejor",
            "• Considere métodos de alta precisión (5-puntos) para mayor exactitud"
        ])
        
        sections["RECOMENDACIONES"] = recommendations
        
        # Formatear y mostrar
        formatted_text = self.format_result_text(
            f"{result.method} - DERIVADA DE ORDEN {result.order}", 
            main_data, sections
        )
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", formatted_text)
    
    def _display_comparison(self, results, order):
        """Mostrar comparación de todos los métodos"""
        main_data = {
            "Función": self.entries["función_fx"].get(),
            "Punto": f"x₀ = {self.entries['punto_x₀'].get()}",
            "Paso": f"h = {self.entries['paso_h'].get()}",
            "Orden de derivada": order
        }
        
        # Obtener valor exacto de referencia
        exact_value = None
        for result in results.values():
            if result.exact_value is not None:
                exact_value = result.exact_value
                break
        
        if exact_value is not None:
            main_data["Valor exacto"] = f"{exact_value:.10f}"
        
        # Tabla comparativa
        comparison_lines = []
        comparison_lines.append(f"{'Método':<20} {'Aproximación':<15} {'Error':<15} {'Error Rel.':<12} {'Orden':<8}")
        comparison_lines.append("-" * 80)
        
        # Encontrar el mejor método
        best_method = None
        best_error = float('inf')
        
        for name, result in results.items():
            error_str = f"{result.absolute_error:.2e}" if result.absolute_error is not None else "N/A"
            rel_error_str = f"{result.relative_error:.4f}%" if result.relative_error is not None else "N/A"
            
            comparison_lines.append(
                f"{result.method:<20} {result.value:<15.8f} {error_str:<15} {rel_error_str:<12} {result.error_order:<8}"
            )
            
            # Actualizar mejor método
            if result.absolute_error is not None and result.absolute_error < best_error:
                best_error = result.absolute_error
                best_method = result.method
        
        sections = {
            "COMPARACIÓN DE MÉTODOS": comparison_lines
        }
        
        # Análisis de los resultados
        if best_method:
            analysis = []
            analysis.append(f"✅ Mejor método: {best_method}")
            analysis.append(f"   Error mínimo: {best_error:.2e}")
            analysis.append("")
            analysis.extend([
                "📊 Características teóricas:",
                "   • Hacia Adelante: Error O(h), 1 dirección",
                "   • Hacia Atrás: Error O(h), 1 dirección",
                "   • Central: Error O(h²), 2 direcciones",
                "",
                "🎯 Cuándo usar cada método:",
                "   • Adelante: borde izquierdo, datos limitados hacia atrás",
                "   • Atrás: borde derecho, datos limitados hacia adelante",
                "   • Central: interior del dominio, mejor precisión general",
                "",
                "💡 Para mejorar precisión:",
                "   • Reducir h (pero cuidado con errores de redondeo)",
                "   • Usar métodos de mayor orden (5-puntos)",
                "   • Aplicar extrapolación de Richardson"
            ])
            
            sections["ANÁLISIS"] = analysis
        
        # Formatear y mostrar
        formatted_text = self.format_result_text(
            f"ANÁLISIS COMPLETO - DERIVADA DE ORDEN {order}", 
            main_data, sections
        )
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", formatted_text)
    
    def _plot_derivative_analysis(self, f, result, method_name):
        """Crear gráfico para análisis de derivadas"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='#2b2b2b')
        
        for ax in [ax1, ax2]:
            ax.set_facecolor('#2b2b2b')
        
        x0 = result.point
        h = result.step_size
        
        # Gráfico 1: Función original y puntos usados
        x_range = np.linspace(x0 - 3*h, x0 + 3*h, 1000)
        y_values = [f(x) for x in x_range]
        
        ax1.plot(x_range, y_values, 'cyan', linewidth=2, label='f(x)')
        
        # Marcar punto de evaluación
        ax1.plot(x0, f(x0), 'ro', markersize=10, label=f'x₀ = {x0}')
        
        # Marcar puntos usados en el cálculo
        if result.computation_data and 'points_used' in result.computation_data:
            points = result.computation_data['points_used']
            values = result.computation_data['function_evaluations']
            
            for point, value in zip(points, values):
                if point != x0:  # No remarcar el punto central
                    ax1.plot(point, value, 'go', markersize=6, alpha=0.7)
        
        self.apply_plot_styling(
            ax1,
            title="Función y Puntos de Evaluación",
            xlabel="x",
            ylabel="f(x)"
        )
        
        # Gráfico 2: Análisis de convergencia con h
        h_values = [h * (2**i) for i in range(-3, 4)]  # h/8 a 8h
        errors = []
        derivatives = []
        
        for h_test in h_values:
            try:
                if "adelante" in method_name.lower():
                    test_result = self.calculator.forward_difference(f, x0, h_test, result.order)
                elif "atrás" in method_name.lower():
                    test_result = self.calculator.backward_difference(f, x0, h_test, result.order)
                else:  # central
                    test_result = self.calculator.central_difference(f, x0, h_test, result.order)
                
                derivatives.append(test_result.value)
                if test_result.absolute_error is not None:
                    errors.append(test_result.absolute_error)
                else:
                    errors.append(np.nan)
            except:
                derivatives.append(np.nan)
                errors.append(np.nan)
        
        # Graficar convergencia
        valid_indices = [i for i, e in enumerate(errors) if not np.isnan(e) and e > 0]
        if valid_indices:
            valid_h = [h_values[i] for i in valid_indices]
            valid_errors = [errors[i] for i in valid_indices]
            
            ax2.loglog(valid_h, valid_errors, 'o-', color='orange', linewidth=2, 
                      markersize=6, label='Error vs h')
            
            # Marcar h actual
            current_error = result.absolute_error
            if current_error is not None and current_error > 0:
                ax2.loglog(h, current_error, 'ro', markersize=10, 
                          label=f'h actual = {h:.3f}')
        
        self.apply_plot_styling(
            ax2,
            title="Convergencia del Error",
            xlabel="Paso h",
            ylabel="Error absoluto"
        )
        
        plt.tight_layout()
        canvas = fig.canvas
        canvas.draw()
    
    def _plot_comparison(self, f, results, x0, h):
        """Crear gráfico comparativo de los métodos"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), facecolor='#2b2b2b')
        
        for ax in [ax1, ax2]:
            ax.set_facecolor('#2b2b2b')
        
        # Gráfico 1: Función y esquemas de diferencias
        x_range = np.linspace(x0 - 3*h, x0 + 3*h, 1000)
        y_values = [f(x) for x in x_range]
        
        ax1.plot(x_range, y_values, 'cyan', linewidth=2, label='f(x)')
        ax1.plot(x0, f(x0), 'ro', markersize=10, label=f'x₀ = {x0}')
        
        # Mostrar puntos de cada método
        colors = {'forward': 'orange', 'backward': 'green', 'central': 'yellow'}
        for name, result in results.items():
            if result.computation_data and 'points_used' in result.computation_data:
                points = result.computation_data['points_used']
                values = result.computation_data['function_evaluations']
                
                color = colors.get(name, 'white')
                for point, value in zip(points, values):
                    if abs(point - x0) > 1e-10:  # No remarcar el punto central
                        ax1.plot(point, value, 'o', color=color, 
                                markersize=6, alpha=0.7)
        
        self.apply_plot_styling(
            ax1,
            title="Función y Puntos de Evaluación",
            xlabel="x",
            ylabel="f(x)"
        )
        
        # Gráfico 2: Comparación de precisión
        methods = [result.method for result in results.values()]
        values_computed = [result.value for result in results.values()]
        errors = [result.absolute_error if result.absolute_error is not None else 0 
                 for result in results.values()]
        
        # Gráfico de barras para los valores
        x_pos = np.arange(len(methods))
        bars1 = ax2.bar(x_pos - 0.2, values_computed, 0.4, 
                       color=['orange', 'green', 'yellow'], alpha=0.7, 
                       label='Aproximaciones')
        
        # Línea del valor exacto si está disponible
        exact_value = None
        for result in results.values():
            if result.exact_value is not None:
                exact_value = result.exact_value
                break
        
        if exact_value is not None:
            ax2.axhline(y=exact_value, color='white', linestyle='--', 
                       linewidth=2, label=f'Exacto: {exact_value:.8f}')
        
        # Añadir valores en las barras
        for bar, value in zip(bars1, values_computed):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.001*abs(height),
                    f'{value:.6f}', ha='center', va='bottom', color='white', fontsize=9)
        
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels([m.replace('Diferencias ', '') for m in methods], rotation=45)
        
        self.apply_plot_styling(
            ax2,
            title="Comparación de Aproximaciones",
            xlabel="Método",
            ylabel="Valor de la Derivada"
        )
        
        plt.tight_layout()
        canvas = fig.canvas
        canvas.draw()
