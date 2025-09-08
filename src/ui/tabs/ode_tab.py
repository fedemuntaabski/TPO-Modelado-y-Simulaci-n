"""
Pestaña de ecuaciones diferenciales ordinarias (EDO).

Implementa la interfaz gráfica para los métodos de resolución de EDO
siguiendo principios SOLID y DRY.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional

from src.ui.components.base_tab import BaseTab
from src.ui.components.mixins import InputValidationMixin, ResultDisplayMixin, PlottingMixin
from src.ui.components.constants import VALIDATION, DEFAULT_CONFIGS
from src.core.ode_solver import ODESolver
from src.core.root_finding import create_function_from_string
from config.settings import NUMERICAL_CONFIG


class ODETab(BaseTab, InputValidationMixin, ResultDisplayMixin, PlottingMixin):
    """
    Pestaña para ecuaciones diferenciales ordinarias.
    Hereda funcionalidad común de BaseTab y usa mixins para reducir duplicación.
    """
    
    def __init__(self, parent):
        # Inicializar mixins primero
        InputValidationMixin.__init__(self)
        
        super().__init__(parent, "📈 Ecuaciones Diferenciales")
        self.ode_solver = ODESolver(use_scipy=True)
    
    def setup_validation_for_tab(self, entries, validation_config):
        """Configura validación para la pestaña de ODE (implementación simplificada)"""
        # Por ahora, solo guardar referencias básicas
        self.entries = entries
        self.validation_config = validation_config
        # No configurar validación en tiempo real por simplicidad
    
    def create_content(self):
        """Crear contenido específico para EDO (Template Method)"""
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Métodos numéricos para resolver ecuaciones diferenciales ordinarias: dy/dt = f(t, y)",
            font=ctk.CTkFont(size=14)
        )
        desc_label.grid(row=0, column=0, pady=10, padx=20, sticky="ew")
        
        # Crear sección de entrada
        input_data = {
            "Función f(t,y):": "-2*y + t",
            "Tiempo inicial (t₀):": "0",
            "Tiempo final (tₓ):": "2",
            "Condición inicial y₀:": "1",
            "Número de puntos (n):": "21"
        }
        self.entries = self.create_input_section(input_data)

        # Configurar validación en tiempo real
        validation_config = {
            "función_fty": {"type": "function"},
            "tiempo_inicial_t₀": {"type": "numeric"},
            "tiempo_final_tₓ": {"type": "numeric"},
            "condición_inicial_y₀": {"type": "numeric"},
            "número_de_puntos_n": {"type": "integer", "params": {"min_val": VALIDATION.MIN_SUBDIVISIONS, "max_val": VALIDATION.MAX_SUBDIVISIONS}}
        }
        self.setup_validation_for_tab(self.entries, validation_config)
        
        # Crear sección de métodos
        methods = [
            ("Euler", self.euler_method),
            ("Runge-Kutta 2", self.rk2_method),
            ("Runge-Kutta 4", self.rk4_method),
            ("Comparar Todos", self.compare_all_methods)
        ]
        self.create_methods_section(methods)
        
        # Crear sección de resultados
        self.results_frame, self.results_text, self.plot_frame = self.create_results_section()
    
    def euler_method(self):
        """Ejecutar método de Euler"""
        try:
            # Validar formulario completo
            if not self.is_form_valid():
                return
            
            # Obtener valores validados
            values = self.get_validated_values()
            
            # Validar rangos específicos
            if not self.validate_range(values["tiempo_inicial_t₀"], values["tiempo_final_tₓ"], "tiempo inicial", "tiempo final"):
                return
            
            # Crear función f(t, y)
            f = create_function_from_string(values["función_fty"])
            
            # Ejecutar método
            result = self.ode_solver.euler_method(
                f, 
                values["tiempo_inicial_t₀"], 
                values["tiempo_final_tₓ"], 
                values["condición_inicial_y₀"], 
                values["número_de_puntos_n"]
            )
            
            # Mostrar resultados
            self._display_results(result)
            
            # Crear gráfico
            self._plot_ode_solution(result)
            
        except Exception as e:
            self.show_error(f"Error en Euler: {e}")
    
    def rk2_method(self):
        """Ejecutar método de Runge-Kutta de 2do orden"""
        try:
            # Validar formulario completo
            if not self.is_form_valid():
                return
            
            # Obtener valores validados
            values = self.get_validated_values()
            
            # Validar rangos específicos
            if not self.validate_range(values["tiempo_inicial_t₀"], values["tiempo_final_tₓ"], "tiempo inicial", "tiempo final"):
                return
            
            # Crear función f(t, y)
            f = create_function_from_string(values["función_fty"])
            
            # Ejecutar método
            result = self.ode_solver.runge_kutta_2(
                f,
                values["tiempo_inicial_t₀"],
                values["tiempo_final_tₓ"],
                values["condición_inicial_y₀"],
                values["número_de_puntos_n"]
            )
            
            # Mostrar resultados
            self._display_results(result)
            
            # Crear gráfico
            self._plot_ode_solution(result)
            
        except Exception as e:
            self.show_error(f"Error en RK2: {e}")
    
    def rk4_method(self):
        """Ejecutar método de Runge-Kutta de 4to orden"""
        try:
            # Validar formulario completo
            if not self.is_form_valid():
                return
            
            # Obtener valores validados
            values = self.get_validated_values()
            
            # Validar rangos específicos
            if not self.validate_range(values["tiempo_inicial_t₀"], values["tiempo_final_tₓ"], "tiempo inicial", "tiempo final"):
                return
            
            # Crear función f(t, y)
            f = create_function_from_string(values["función_fty"])
            
            # Ejecutar método
            result = self.ode_solver.runge_kutta_4(
                f,
                values["tiempo_inicial_t₀"],
                values["tiempo_final_tₓ"],
                values["condición_inicial_y₀"],
                values["número_de_puntos_n"]
            )
            
            # Mostrar resultados
            self._display_results(result)
            
            # Crear gráfico
            self._plot_ode_solution(result)
            
        except Exception as e:
            self.show_error(f"Error en RK4: {e}")
    
    def compare_all_methods(self):
        """Comparar todos los métodos de EDO"""
        try:
            # Validar formulario completo
            if not self.is_form_valid():
                return
            
            # Obtener valores validados
            values = self.get_validated_values()
            
            # Validar rangos específicos
            if not self.validate_range(values["tiempo_inicial_t₀"], values["tiempo_final_tₓ"], "tiempo inicial", "tiempo final"):
                return
            
            # Crear función f(t, y)
            f = create_function_from_string(values["función_fty"])
            
            # Ejecutar todos los métodos
            results = {}
            results['euler'] = self.ode_solver.euler_method(
                f, values["tiempo_inicial_t₀"], values["tiempo_final_tₓ"], 
                values["condición_inicial_y₀"], values["número_de_puntos_n"]
            )
            results['rk2'] = self.ode_solver.runge_kutta_2(
                f, values["tiempo_inicial_t₀"], values["tiempo_final_tₓ"], 
                values["condición_inicial_y₀"], values["número_de_puntos_n"]
            )
            results['rk4'] = self.ode_solver.runge_kutta_4(
                f, values["tiempo_inicial_t₀"], values["tiempo_final_tₓ"], 
                values["condición_inicial_y₀"], values["número_de_puntos_n"]
            )
            
            # Mostrar comparación
            self._display_comparison(results)
            
            # Crear gráfico comparativo
            self._plot_comparison(results)
            
        except Exception as e:
            self.show_error(f"Error en comparación: {e}")
    
    def _display_results(self, result):
        """Mostrar resultados de un método específico"""
        # Datos principales
        main_data = {
            "Ecuación": f"dy/dt = {self.entries['función_fty'].get()}",
            "Condición inicial": f"y({self.entries['tiempo_inicial_t₀'].get()}) = {self.entries['condición_inicial_y₀'].get()}",
            "Intervalo": f"[{self.entries['tiempo_inicial_t₀'].get()}, {self.entries['tiempo_final_tₓ'].get()}]",
            "Método": result.method,
            "Paso (h)": f"{result.step_size:.6f}",
            "Puntos evaluados": len(result.t),
            "Solución final": f"y({result.t[-1]:.3f}) = {result.y[-1]:.8f}"
        }
        
        # Agregar información exacta si está disponible
        if result.exact_solution is not None:
            exact_final = result.exact_solution[-1]
            main_data["Valor exacto final"] = f"{exact_final:.8f}"
            main_data["Error máximo"] = f"{result.max_error:.2e}"
            main_data["Error promedio"] = f"{result.avg_error:.2e}"
            main_data["Error final"] = f"{result.final_error:.2e}"
        
        # Secciones adicionales
        sections = {}
        
        # Información del método
        method_info = []
        if "euler" in result.method.lower():
            method_info = [
                "Método explícito de primer orden",
                "Fórmula: y_{i+1} = y_i + h·f(t_i, y_i)",
                "Error global: O(h) - convergencia lineal",
                "Simple pero puede ser inestable con h grande",
                "Requiere h pequeño para buena precisión"
            ]
        elif "runge-kutta 2" in result.method.lower():
            method_info = [
                "Método explícito de segundo orden",
                "Usa dos evaluaciones de f por paso",
                "Error global: O(h²) - convergencia cuadrática",
                "Mejor precisión que Euler para el mismo h",
                "Compromiso entre precisión y eficiencia"
            ]
        elif "runge-kutta 4" in result.method.lower():
            method_info = [
                "Método explícito de cuarto orden (estándar)",
                "Usa cuatro evaluaciones de f por paso",
                "Error global: O(h⁴) - convergencia muy rápida",
                "Excelente precisión para funciones suaves",
                "Más caro computacionalmente pero muy preciso"
            ]
        
        if method_info:
            sections["CARACTERÍSTICAS DEL MÉTODO"] = method_info
        
        # Fórmulas del método
        if result.computation_data and 'formula' in result.computation_data:
            formulas = result.computation_data['formula']
            if isinstance(formulas, list):
                sections["FÓRMULAS UTILIZADAS"] = formulas
            else:
                sections["FÓRMULA UTILIZADA"] = [formulas]
        
        # Tabla de primeros pasos
        if result.computation_data and 'step_data' in result.computation_data:
            step_data = result.computation_data['step_data']
            if step_data:
                step_lines = []
                step_lines.append("Primeros pasos del método:")
                step_lines.append(f"{'i':<3} {'t_i':<10} {'y_i':<12} {'Info adicional':<30}")
                step_lines.append("-" * 60)
                
                for data in step_data[:8]:  # Mostrar solo primeros 8 pasos
                    i = data['i']
                    t_i = data['t_i']
                    y_i = data['y_i']
                    
                    if 'f_ti_yi' in data:  # Euler
                        info = f"f(t_i,y_i) = {data['f_ti_yi']:.6f}"
                    elif 'k1' in data:  # Runge-Kutta
                        if 'k2' in data and 'k3' not in data:  # RK2
                            info = f"k1={data['k1']:.4f}, k2={data['k2']:.4f}"
                        elif 'k4' in data:  # RK4
                            info = f"k1={data['k1']:.4f}, k4={data['k4']:.4f}"
                        else:
                            info = "Runge-Kutta step"
                    else:
                        info = "Step computed"
                    
                    step_lines.append(f"{i:<3} {t_i:<10.4f} {y_i:<12.6f} {info:<30}")
                
                if len(result.computation_data['step_data']) > 8:
                    step_lines.append("... (mostrando solo los primeros 8 pasos)")
                
                sections["TABLA DE PASOS"] = step_lines
        
        # Recomendaciones
        recommendations = []
        if result.exact_solution is not None:
            if result.max_error < 1e-8:
                recommendations.append("✅ Excelente precisión obtenida")
            elif result.max_error < 1e-6:
                recommendations.append("✅ Buena precisión")
            elif result.max_error < 1e-4:
                recommendations.append("⚠️ Precisión moderada - considere reducir h")
            else:
                recommendations.append("❌ Baja precisión - reduzca h significativamente")
        
        recommendations.extend([
            "• Para mayor precisión, use RK4 en lugar de Euler",
            "• Reduzca h (aumente n) si necesita mayor precisión",
            "• RK4 es generalmente la mejor opción para funciones suaves",
            "• Para problemas stiff, considere métodos implícitos"
        ])
        
        sections["RECOMENDACIONES"] = recommendations
        
        # Formatear y mostrar
        formatted_text = self.format_result_text(result.method.upper(), main_data, sections)
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", formatted_text)
    
    def _display_comparison(self, results):
        """Mostrar comparación de todos los métodos"""
        main_data = {
            "Ecuación": f"dy/dt = {self.entries['función_fty'].get()}",
            "Condición inicial": f"y({self.entries['tiempo_inicial_t₀'].get()}) = {self.entries['condición_inicial_y₀'].get()}",
            "Intervalo": f"[{self.entries['tiempo_inicial_t₀'].get()}, {self.entries['tiempo_final_tₓ'].get()}]",
            "Puntos": self.entries['número_de_puntos_n'].get()
        }
        
        # Tabla comparativa
        comparison_lines = []
        comparison_lines.append(f"{'Método':<15} {'Solución Final':<15} {'Error Max':<12} {'Error Prom':<12} {'Orden':<6}")
        comparison_lines.append("-" * 70)
        
        # Obtener valor exacto de referencia
        exact_value = None
        for result in results.values():
            if result.exact_solution is not None:
                exact_value = result.exact_solution[-1]
                break
        
        if exact_value is not None:
            main_data["Valor exacto final"] = f"{exact_value:.8f}"
        
        # Encontrar el mejor método
        best_method = None
        best_error = float('inf')
        
        for name, result in results.items():
            final_value = result.y[-1]
            max_error_str = f"{result.max_error:.2e}" if result.max_error is not None else "N/A"
            avg_error_str = f"{result.avg_error:.2e}" if result.avg_error is not None else "N/A"
            
            # Determinar orden teórico
            if "euler" in result.method.lower():
                order = "O(h)"
            elif "runge-kutta 2" in result.method.lower():
                order = "O(h²)"
            elif "runge-kutta 4" in result.method.lower():
                order = "O(h⁴)"
            else:
                order = "N/A"
            
            comparison_lines.append(
                f"{result.method:<15} {final_value:<15.8f} {max_error_str:<12} {avg_error_str:<12} {order:<6}"
            )
            
            # Actualizar mejor método
            if result.max_error is not None and result.max_error < best_error:
                best_error = result.max_error
                best_method = result.method
        
        sections = {
            "COMPARACIÓN DE MÉTODOS": comparison_lines
        }
        
        # Análisis de eficiencia
        efficiency_analysis = []
        if best_method:
            efficiency_analysis.append(f"✅ Mejor precisión: {best_method}")
            efficiency_analysis.append(f"   Error máximo: {best_error:.2e}")
            efficiency_analysis.append("")
        
        efficiency_analysis.extend([
            "📊 Comparación de eficiencia:",
            "   • Euler: 1 evaluación/paso, O(h) error",
            "   • RK2: 2 evaluaciones/paso, O(h²) error", 
            "   • RK4: 4 evaluaciones/paso, O(h⁴) error",
            "",
            "💡 Recomendaciones:",
            "   • Para cálculos rápidos: Euler con h pequeño",
            "   • Para precisión moderada: RK2",
            "   • Para alta precisión: RK4 (opción estándar)",
            "   • RK4 suele ser la mejor opción global"
        ])
        
        sections["ANÁLISIS DE EFICIENCIA"] = efficiency_analysis
        
        # Formatear y mostrar
        formatted_text = self.format_result_text("COMPARACIÓN DE MÉTODOS EDO", main_data, sections)
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", formatted_text)
    
    def _plot_ode_solution(self, result):
        """Crear gráfico de la solución de EDO"""
        fig, canvas = self.create_matplotlib_plot(self.plot_frame)
        ax = fig.add_subplot(111)
        
        # Graficar solución numérica
        ax.plot(result.t, result.y, 'o-', color='cyan', linewidth=2, 
                markersize=4, label=f'{result.method}')
        
        # Graficar solución exacta si está disponible
        if result.exact_solution is not None:
            ax.plot(result.t, result.exact_solution, '--', color='orange', 
                    linewidth=2, label='Solución exacta')
        
        # Marcar condición inicial
        t0 = result.t[0]
        y0 = result.y[0]
        ax.plot(t0, y0, 'go', markersize=8, label=f'Condición inicial: y({t0}) = {y0}')
        
        # Marcar solución final
        tf = result.t[-1]
        yf = result.y[-1]
        ax.plot(tf, yf, 'ro', markersize=8, label=f'Solución final: y({tf:.3f}) = {yf:.6f}')
        
        self.apply_plot_styling(
            ax,
            title=f"{result.method} - h = {result.step_size:.4f}",
            xlabel="t",
            ylabel="y(t)"
        )
        
        # Agregar información del error si está disponible
        if result.max_error is not None:
            ax.text(0.05, 0.95, f"Error máximo: {result.max_error:.2e}", 
                    transform=ax.transAxes, fontsize=10, color='white',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        canvas.draw()
    
    def _plot_comparison(self, results):
        """Crear gráfico comparativo de los métodos EDO"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), facecolor='#2b2b2b')
        
        for ax in [ax1, ax2]:
            ax.set_facecolor('#2b2b2b')
        
        # Colores para cada método
        colors = {'euler': 'orange', 'rk2': 'green', 'rk4': 'cyan'}
        linestyles = {'euler': '-', 'rk2': '--', 'rk4': '-.'}
        
        # Gráfico 1: Soluciones
        for name, result in results.items():
            ax1.plot(result.t, result.y, linestyles[name], color=colors[name], 
                    linewidth=2, label=result.method, alpha=0.8)
        
        # Solución exacta si está disponible
        exact_solution = None
        for result in results.values():
            if result.exact_solution is not None:
                exact_solution = result.exact_solution
                ax1.plot(result.t, exact_solution, 'w:', linewidth=3, 
                        label='Solución exacta', alpha=0.9)
                break
        
        # Condición inicial
        first_result = list(results.values())[0]
        t0, y0 = first_result.t[0], first_result.y[0]
        ax1.plot(t0, y0, 'go', markersize=8, label=f'y({t0}) = {y0}')
        
        self.apply_plot_styling(ax1, title="Comparación de Soluciones", 
                               xlabel="t", ylabel="y(t)")
        
        # Gráfico 2: Errores (si hay solución exacta)
        if exact_solution is not None:
            for name, result in results.items():
                if result.error is not None:
                    ax2.plot(result.t, result.error, linestyles[name], 
                            color=colors[name], linewidth=2, 
                            label=f'Error {result.method}')
            
            ax2.set_yscale('log')
            self.apply_plot_styling(ax2, title="Errores Absolutos (escala log)", 
                                   xlabel="t", ylabel="Error absoluto")
        else:
            # Si no hay solución exacta, mostrar comparación de valores finales
            methods = [result.method for result in results.values()]
            final_values = [result.y[-1] for result in results.values()]
            
            bars = ax2.bar(range(len(methods)), final_values, 
                          color=list(colors.values())[:len(methods)], alpha=0.7)
            ax2.set_xticks(range(len(methods)))
            ax2.set_xticklabels(methods, rotation=45)
            
            # Añadir valores en las barras
            for bar, value in zip(bars, final_values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01*abs(height),
                        f'{value:.6f}', ha='center', va='bottom', color='white', fontsize=10)
            
            self.apply_plot_styling(ax2, title="Valores Finales de la Solución", 
                                   xlabel="Método", ylabel="y(t_final)")
        
        plt.tight_layout()
        
        # Crear canvas y dibujar
        canvas = fig.canvas
        canvas.draw()
