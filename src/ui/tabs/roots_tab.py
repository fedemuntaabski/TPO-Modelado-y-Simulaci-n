"""
Pestaña de búsqueda de raíces de ecuaciones no lineales.

Implementa la interfaz gráfica para los métodos numéricos de búsqueda de raíces
siguiendo principios SOLID y DRY.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional

from src.ui.components.base_tab import BaseTab
from src.ui.components.mixins import InputValidationMixin, ResultDisplayMixin, PlottingMixin
from src.ui.components.constants import VALIDATION, DEFAULT_CONFIGS
from src.core.root_finding import RootFinder, create_function_from_string
from config.settings import NUMERICAL_CONFIG


class RootsTab(BaseTab, InputValidationMixin, ResultDisplayMixin, PlottingMixin):
    """
    Pestaña para búsqueda de raíces.
    Hereda funcionalidad común de BaseTab y usa mixins para reducir duplicación.
    """
    
    def __init__(self, parent):
        # Inicializar mixins primero
        InputValidationMixin.__init__(self)
        
        super().__init__(parent, "🎯 Búsqueda de Raíces")
        
        # Inicializar atributos de validación manualmente
        self._validation_states = {}
        self._validation_callbacks = {}
        self._field_validators = {}
        
        config = DEFAULT_CONFIGS["root_finding"]
        self.root_finder = RootFinder(
            tolerance=config["tolerance"],
            max_iterations=config["max_iterations"]
        )
    
    def setup_validation_for_tab(self, entries, validation_config):
        """Configura validación para la pestaña de raíces (implementación simplificada)"""
        # Por ahora, solo guardar referencias básicas
        self.entries = entries
        self.validation_config = validation_config
        # No configurar validación en tiempo real por simplicidad
    
    def is_form_valid(self):
        """Validación simplificada del formulario"""
        errors = {}
        
        # Validar función
        entry_func = self.entries.get("función_fx")
        if entry_func is None:
            errors["función_fx"] = "Campo de función no encontrado"
        else:
            func_text = entry_func.get().strip()
            if not func_text:
                errors["función_fx"] = "La función no puede estar vacía"
        
        # Validar intervalo a
        entry_a = self.entries.get("intervalo_a")
        if entry_a is None:
            errors["intervalo_a"] = "Campo de intervalo a no encontrado"
        else:
            a_text = entry_a.get().strip()
            if not a_text:
                errors["intervalo_a"] = "El intervalo a no puede estar vacío"
            else:
                try:
                    float(a_text)
                except ValueError:
                    errors["intervalo_a"] = "El intervalo a debe ser un número"
        
        # Validar intervalo b
        entry_b = self.entries.get("intervalo_b")
        if entry_b is None:
            errors["intervalo_b"] = "Campo de intervalo b no encontrado"
        else:
            b_text = entry_b.get().strip()
            if not b_text:
                errors["intervalo_b"] = "El intervalo b no puede estar vacío"
            else:
                try:
                    float(b_text)
                except ValueError:
                    errors["intervalo_b"] = "El intervalo b debe ser un número"
        
        # Validar tolerancia
        entry_tol = self.entries.get("tolerancia")
        if entry_tol is None:
            errors["tolerancia"] = "Campo de tolerancia no encontrado"
        else:
            tol_text = entry_tol.get().strip()
            if not tol_text:
                errors["tolerancia"] = "La tolerancia no puede estar vacía"
            else:
                try:
                    tol_val = float(tol_text)
                    if tol_val <= 0:
                        errors["tolerancia"] = "La tolerancia debe ser positiva"
                except ValueError:
                    errors["tolerancia"] = "La tolerancia debe ser un número"
        
        return len(errors) == 0, errors
    
    def get_validated_values(self):
        """Obtener valores validados del formulario"""
        return {
            "función_fx": self.entries["función_fx"].get().strip(),
            "intervalo_a": float(self.entries["intervalo_a"].get().strip()),
            "intervalo_b": float(self.entries["intervalo_b"].get().strip()),
            "tolerancia": float(self.entries["tolerancia"].get().strip())
        }
    
    def validate_range(self, a_str, b_str):
        """Validar que el rango sea válido para bisección"""
        try:
            a = float(a_str)
            b = float(b_str)
            if a >= b:
                return False, "El intervalo a debe ser menor que b"
            return True, ""
        except ValueError:
            return False, "Los intervalos deben ser números válidos"
    
    def create_content(self):
        """Crear contenido específico para raíces (Template Method)"""
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Métodos numéricos para encontrar raíces de ecuaciones no lineales",
            font=ctk.CTkFont(size=14)
        )
        desc_label.grid(row=0, column=0, pady=10, padx=20, sticky="ew")
        
        # Crear sección de entrada
        input_data = {
            "Función f(x):": "x**2 - 4",
            "Intervalo a:": "1",
            "Intervalo b:": "3",
            "Tolerancia:": str(VALIDATION.DEFAULT_TOLERANCE)
        }
        self.entries = self.create_input_section(input_data)
        
        # Configurar validación en tiempo real
        validation_config = {
            "función_fx": {"type": "function"},
            "intervalo_a": {"type": "numeric"},
            "intervalo_b": {"type": "numeric"},
            "tolerancia": {"type": "tolerance"}
        }
        self.setup_validation_for_tab(self.entries, validation_config)
        
        # Crear sección de métodos
        methods = [
            ("Bisección", self.bisection_method),
            ("Newton-Raphson", self.newton_raphson_method),
            ("Punto Fijo", self.fixed_point_method),
            ("Aitken", self.aitken_method)
        ]
        self.create_methods_section(methods)
        
        # Crear sección de resultados
        self.results_frame, self.results_text, self.plot_frame = self.create_results_section()
    
    def bisection_method(self):
        """Ejecutar método de bisección con validación mejorada"""
        # Verificar que el formulario sea válido
        is_valid, errors = self.is_form_valid()
        if not is_valid:
            error_msg = "; ".join(errors.values())
            self.show_error(f"Por favor corrija los siguientes errores: {error_msg}")
            return

        try:
            # Obtener valores validados
            values = self.get_validated_values()
            function_str = values["función_fx"]

            # Validar rango específico para bisección
            is_valid_range, range_error = self.validate_range(
                str(values["intervalo_a"]), str(values["intervalo_b"])
            )
            if not is_valid_range:
                self.show_error(range_error)
                return

            # Crear función
            f = create_function_from_string(function_str)

            # Ejecutar método
            result = self.root_finder.bisection_method(
                f, values["intervalo_a"], values["intervalo_b"]
            )

            # Mostrar resultados
            self._display_results(result, "MÉTODO DE BISECCIÓN")

            # Crear gráfico
            self._plot_function_and_root(f, values["intervalo_a"], values["intervalo_b"], result.root)

        except Exception as e:
            self.show_error(f"Error en bisección: {str(e)}")
    
    def newton_raphson_method(self):
        """Ejecutar método de Newton-Raphson usando mixins"""
        try:
            # Validar función usando mixin
            is_valid_func, function_str, func_error = self.validate_function_input(
                self.entries, "función_fx"
            )
            if not is_valid_func:
                self.show_error(func_error)
                return

            # Validar entradas numéricas usando mixin
            is_valid_num, values, num_error = self.validate_numeric_inputs(
                self.entries,
                ["intervalo_a", "tolerancia"]
            )
            if not is_valid_num:
                self.show_error(num_error)
                return

            # Crear función
            f = create_function_from_string(function_str)

            # Ejecutar método (derivada se calcula numéricamente)
            result = self.root_finder.newton_raphson_method(
                f, None, values["intervalo_a"]  # None = derivada numérica
            )

            # Mostrar resultados usando mixin
            self._display_results(result, "MÉTODO DE NEWTON-RAPHSON")

            # Crear gráfico usando mixin
            self._plot_newton_raphson(f, values["intervalo_a"], result.root)

        except Exception as e:
            self.show_error(f"Error en Newton-Raphson: {e}")
    
    def fixed_point_method(self):
        """Ejecutar método de punto fijo usando mixins"""
        try:
            # Validar función usando mixin
            is_valid_func, function_str, func_error = self.validate_function_input(
                self.entries, "función_fx"
            )
            if not is_valid_func:
                self.show_error(func_error)
                return

            # Validar entradas numéricas usando mixin
            is_valid_num, values, num_error = self.validate_numeric_inputs(
                self.entries,
                ["intervalo_a", "tolerancia"]
            )
            if not is_valid_num:
                self.show_error(num_error)
                return

            # Crear función original
            f = create_function_from_string(function_str)

            # Convertir a función de punto fijo: g(x) = x + f(x)
            g = lambda x: x + f(x)

            # Ejecutar método
            result = self.root_finder.fixed_point_method(g, values["intervalo_a"])

            # Mostrar resultados usando mixin
            self._display_results(result, "MÉTODO DE PUNTO FIJO")

            # Crear gráfico usando mixin
            self._plot_fixed_point(f, g, values["intervalo_a"], result.root)

        except Exception as e:
            self.show_error(f"Error en punto fijo: {e}")
    
    def aitken_method(self):
        """Ejecutar método de aceleración de Aitken usando mixins"""
        try:
            # Validar función usando mixin
            is_valid_func, function_str, func_error = self.validate_function_input(
                self.entries, "función_fx"
            )
            if not is_valid_func:
                self.show_error(func_error)
                return

            # Validar entradas numéricas usando mixin
            is_valid_num, values, num_error = self.validate_numeric_inputs(
                self.entries,
                ["intervalo_a", "tolerancia"]
            )
            if not is_valid_num:
                self.show_error(num_error)
                return

            # Crear función original
            f = create_function_from_string(function_str)

            # Convertir a función de punto fijo: g(x) = x + f(x)
            g = lambda x: x + f(x)

            # Ejecutar método de Aitken
            result = self.root_finder.aitken_acceleration(g, values["intervalo_a"])

            # Mostrar resultados usando mixin
            self._display_results(result, "MÉTODO DE AITKEN")

            # Crear gráfico usando mixin
            self._plot_aitken(f, g, values["intervalo_a"], result.root)

        except Exception as e:
            self.show_error(f"Error en Aitken: {e}")
    
    def _display_results(self, result, method_name: str):
        """Mostrar resultados usando mixin ResultDisplayMixin"""
        # Datos principales
        main_data = {
            "Función": self.entries["función_fx"].get(),
            "Método": result.method if hasattr(result, 'method') else method_name,
            "Raíz encontrada": f"{result.root:.8f}",
            "Valor de función": f"{result.function_value:.2e}",
            "Iteraciones": result.iterations,
            "Convergió": "Sí" if result.converged else "No",
            "Error final": f"{result.error:.2e}"
        }

        # Secciones adicionales
        sections = {}

        # Tabla de iteraciones usando mixin
        if result.iteration_data:
            self.display_iteration_table(self.results_text, result.iteration_data, method_name)

        # Información del método
        method_info = []
        if "bisección" in method_name.lower():
            method_info = [
                "Requiere cambio de signo en el intervalo",
                "Convergencia garantizada",
                "Convergencia lineal",
                "Error se reduce a la mitad en cada iteración"
            ]
        elif "newton" in method_name.lower():
            method_info = [
                "Requiere punto inicial cerca de la raíz",
                "Convergencia cuadrática cerca de la raíz",
                "Puede diverger si la derivada es pequeña",
                "Usa derivada numérica automáticamente"
            ]
        elif "punto fijo" in method_name.lower():
            method_info = [
                "Convierte f(x)=0 a x=g(x)",
                "Convergencia depende de |g'(x)| < 1",
                "Transformación: g(x) = x + f(x)",
                "Puede requerir diferentes transformaciones"
            ]
        elif "aitken" in method_name.lower():
            method_info = [
                "Acelera la convergencia de métodos iterativos",
                "Usa extrapolación de Aitken (Δ²)",
                "Mejora convergencia de punto fijo",
                "Requiere 3 iteraciones por paso",
                "Puede fallar si denominador es cercano a cero"
            ]

        if method_info:
            sections["CARACTERÍSTICAS DEL MÉTODO"] = method_info

        # Usar mixin para mostrar resultados
        self.display_calculation_results(self.results_text, method_name, main_data, sections)
    
    def _plot_function_and_root(self, f, a: float, b: float, root: float):
        """Crear gráfico de la función y la raíz encontrada usando mixin"""
        fig, canvas = self.setup_plot_area(self.plot_frame)
        ax = fig.add_subplot(111)

        # Usar mixin para graficar función
        x_range = (a - 0.5*(b-a), b + 0.5*(b-a))
        points = [(root, f(root))]
        point_labels = [f'Raíz: x = {root:.6f}']

        self.plot_function_with_points(fig, ax, f, x_range, points, point_labels)

        # Línea de y=0
        ax.axhline(y=0, color='white', linestyle='--', alpha=0.7, label='y = 0')

        # Marcar intervalo inicial (para bisección)
        if abs(b - a) > 1e-10:
            ax.axvline(x=a, color='yellow', linestyle=':', alpha=0.7, label=f'a = {a}')
            ax.axvline(x=b, color='yellow', linestyle=':', alpha=0.7, label=f'b = {b}')

        self.apply_standard_plot_styling(
            ax,
            title="Función y Raíz Encontrada",
            xlabel="x",
            ylabel="f(x)"
        )

        # Actualizar canvas
        canvas.draw()

    def _plot_newton_raphson(self, f, x0: float, root: float):
        """Crear gráfico mostrando el proceso de Newton-Raphson usando mixin"""
        fig, canvas = self.setup_plot_area(self.plot_frame)
        ax = fig.add_subplot(111)
        
        # Usar mixin para graficar función con puntos
        range_size = max(abs(root - x0), 1)
        x_range = (x0 - range_size, root + range_size)
        points = [(x0, f(x0)), (root, f(root))]
        point_labels = [f'Inicio: x₀ = {x0:.6f}', f'Raíz: x = {root:.6f}']
        
        self.plot_function_with_points(fig, ax, f, x_range, points, point_labels)
        
        # Línea de y=0
        ax.axhline(y=0, color='white', linestyle='--', alpha=0.7, label='y = 0')
        
        self.apply_standard_plot_styling(
            ax,
            title="Método de Newton-Raphson",
            xlabel="x",
            ylabel="f(x)"
        )
        
        # Actualizar canvas
        canvas.draw()
    
    def _plot_fixed_point(self, f, g, x0: float, root: float):
        """Crear gráfico para punto fijo mostrando f(x), g(x) y y=x usando mixin"""
        fig, canvas = self.setup_plot_area(self.plot_frame)
        ax = fig.add_subplot(111)
        
        # Usar mixin para graficar múltiples funciones
        range_size = max(abs(root - x0), 1)
        x_range = (x0 - range_size, root + range_size)
        
        functions = [
            (f, 'cyan', 'f(x)'),
            (g, 'orange', 'g(x) = x + f(x)'),
            (lambda x: x, 'white', 'y = x')  # línea y=x
        ]
        
        self.plot_multiple_functions(fig, ax, functions, x_range)
        
        # Línea de y=0
        ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
        
        # Puntos importantes
        points = [(x0, g(x0)), (root, root)]
        point_labels = [f'Inicio: x₀ = {x0:.6f}', f'Punto fijo: x = {root:.6f}']
        
        for point, label in zip(points, point_labels):
            ax.plot(point[0], point[1], 'o', markersize=8 if 'Inicio' in label else 10,
                   color='green' if 'Inicio' in label else 'red', label=label)
        
        self.apply_standard_plot_styling(
            ax,
            title="Método de Punto Fijo",
            xlabel="x",
            ylabel="y"
        )
        
        # Actualizar canvas
        canvas.draw()
    
    def _plot_aitken(self, f, g, x0: float, root: float):
        """Crear gráfico para método de Aitken mostrando el proceso de aceleración"""
        fig, canvas = self.setup_plot_area(self.plot_frame)
        ax = fig.add_subplot(111)
        
        # Usar mixin para graficar múltiples funciones
        range_size = max(abs(root - x0), 1)
        x_range = (x0 - range_size, root + range_size)
        
        functions = [
            (f, 'cyan', 'f(x)'),
            (g, 'orange', 'g(x) = x + f(x)'),
            (lambda x: x, 'white', 'y = x')  # línea y=x
        ]
        
        self.plot_multiple_functions(fig, ax, functions, x_range)
        
        # Línea de y=0
        ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
        
        # Puntos importantes
        points = [(x0, g(x0)), (root, root)]
        point_labels = [f'Inicio: x₀ = {x0:.6f}', f'Raíz (Aitken): x = {root:.6f}']
        
        for point, label in zip(points, point_labels):
            ax.plot(point[0], point[1], 'o', markersize=8 if 'Inicio' in label else 10,
                   color='green' if 'Inicio' in label else 'red', label=label)
        
        self.apply_standard_plot_styling(
            ax,
            title="Método de Aceleración de Aitken",
            xlabel="x",
            ylabel="y"
        )
        
        # Actualizar canvas
        canvas.draw()
