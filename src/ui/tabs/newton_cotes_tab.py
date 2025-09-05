"""
Pestaña de integración Newton-Cotes.

Implementa la interfaz gráfica para los métodos de integración Newton-Cotes
con selector de métodos, validaciones en tiempo real y visualización de resultados.
"""

import customtkinter as ctk
import logging
from typing import Optional, Dict, Any

from src.ui.components.base_tab import BaseTab
from src.core.newton_cotes import NewtonCotes, NewtonCotesError
from src.core.integration_validators import IntegrationValidationError

logger = logging.getLogger(__name__)


class NewtonCotesTab(BaseTab):
    """
    Pestaña para integración Newton-Cotes.
    Hereda funcionalidad común de BaseTab siguiendo principio DRY.
    """
    
    def __init__(self, parent):
        self.newton_cotes = NewtonCotes()
        self.current_result = None
        self.entries = {}
        self.method_buttons = []
        self.method_var = None
        self.results_text = None
        self.info_labels = {}
        super().__init__(parent, "📊 Newton-Cotes")
        
    def create_content(self):
        """Crear contenido específico para Newton-Cotes"""
        # Configurar el tamaño del frame principal
        self.content_frame.configure(width=1200, height=700)
        
        # Título principal
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="🧮 Integración Newton-Cotes",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        
        # Crear secciones principales
        self.create_input_panel()
        self.create_results_panel()
        
        # Configurar grid principal
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
    def create_input_panel(self):
        """Crear panel de entrada de parámetros"""
        # Frame para inputs
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Título del panel
        input_title = ctk.CTkLabel(
            input_frame,
            text="📝 Parámetros",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        input_title.grid(row=0, column=0, columnspan=2, pady=15, padx=20, sticky="w")
        
        # Campos de entrada
        input_fields = [
            ("Función f(x):", "x**2"),
            ("Límite inferior (a):", "0"),
            ("Límite superior (b):", "1"),
            ("Subdivisiones (n):", "10")
        ]
        
        for i, (label_text, default_value) in enumerate(input_fields):
            # Label
            label = ctk.CTkLabel(
                input_frame,
                text=label_text,
                font=ctk.CTkFont(size=12)
            )
            label.grid(row=i+1, column=0, pady=8, padx=20, sticky="w")
            
            # Entry
            entry = ctk.CTkEntry(
                input_frame,
                placeholder_text=default_value,
                width=180
            )
            entry.grid(row=i+1, column=1, pady=8, padx=(10, 20), sticky="ew")
            entry.insert(0, default_value)
            
            # Guardar referencia usando el texto del label como clave
            key = label_text.replace(":", "").strip()
            self.entries[key] = entry
        
        # Configurar grid del input frame
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Sección de métodos
        self.create_method_selection(input_frame)
        
        # Botones de control
        self.create_control_buttons(input_frame)
        
    def create_method_selection(self, parent_frame):
        """Crear selector de métodos"""
        method_label = ctk.CTkLabel(
            parent_frame,
            text="🔧 Método de Integración",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        method_label.grid(row=6, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="w")
        
        # Variable para el método seleccionado
        self.method_var = ctk.StringVar(value="simpson_13_composite")
        
        # Métodos disponibles
        methods = [
            ("rectangle_simple", "Rectángulo Simple"),
            ("rectangle_composite", "Rectángulo Compuesto"),
            ("trapezoid_simple", "Trapecio Simple"),
            ("trapezoid_composite", "Trapecio Compuesto"),
            ("simpson_13_simple", "Simpson 1/3 Simple"),
            ("simpson_13_composite", "Simpson 1/3 Compuesto"),
            ("simpson_38_simple", "Simpson 3/8 Simple"),
            ("simpson_38_composite", "Simpson 3/8 Compuesto")
        ]
        
        # Crear radio buttons
        for i, (method_key, method_name) in enumerate(methods):
            radio = ctk.CTkRadioButton(
                parent_frame,
                text=method_name,
                variable=self.method_var,
                value=method_key,
                font=ctk.CTkFont(size=11),
                command=self.on_method_change
            )
            radio.grid(row=7+i, column=0, columnspan=2, pady=3, padx=30, sticky="w")
            self.method_buttons.append(radio)
        
        # Información del método
        self.method_info_label = ctk.CTkLabel(
            parent_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=["gray60", "gray40"],
            wraplength=300
        )
        self.method_info_label.grid(row=15, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        # Actualizar info inicial
        self.on_method_change()
        
    def create_control_buttons(self, parent_frame):
        """Crear botones de control"""
        button_frame = ctk.CTkFrame(parent_frame)
        button_frame.grid(row=16, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        
        # Botón calcular
        calc_button = ctk.CTkButton(
            button_frame,
            text="🚀 Calcular",
            command=self.calculate_integration,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        calc_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        
        # Botón ejemplos
        example_button = ctk.CTkButton(
            button_frame,
            text="📝 Ejemplos",
            command=self.show_examples_menu,
            height=40
        )
        example_button.grid(row=0, column=1, pady=10, padx=10, sticky="ew")
        
        # Botón limpiar
        clear_button = ctk.CTkButton(
            button_frame,
            text="🧹 Limpiar",
            command=self.clear_results,
            height=40
        )
        clear_button.grid(row=0, column=2, pady=10, padx=10, sticky="ew")
        
        # Configurar grid
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
    def create_results_panel(self):
        """Crear panel de resultados"""
        # Frame para resultados
        results_frame = ctk.CTkFrame(self.content_frame)
        results_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        
        # Título del panel
        results_title = ctk.CTkLabel(
            results_frame,
            text="📊 Resultados",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_title.grid(row=0, column=0, pady=15, padx=20, sticky="w")
        
        # Área de texto para resultados
        self.results_text = ctk.CTkTextbox(
            results_frame,
            height=400,
            width=500,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.results_text.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
        
        # Frame para información rápida
        info_frame = ctk.CTkFrame(results_frame)
        info_frame.grid(row=2, column=0, pady=15, padx=20, sticky="ew")
        
        # Labels de información
        info_items = ["Resultado", "Tiempo", "Evaluaciones", "Error"]
        for i, item in enumerate(info_items):
            label = ctk.CTkLabel(
                info_frame,
                text=f"{item}: --",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            label.grid(row=i//2, column=i%2, pady=8, padx=15, sticky="w")
            self.info_labels[item] = label
        
        # Configurar grids
        results_frame.grid_rowconfigure(1, weight=1)
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        
        # Mensaje inicial
        self.clear_results()
        
    def on_method_change(self):
        """Manejar cambio de método seleccionado"""
        if not hasattr(self, 'newton_cotes') or not self.method_var:
            return
            
        method = self.method_var.get()
        try:
            method_info = self.newton_cotes.get_method_info(method)
            
            info_text = f"📋 {method_info['description']}"
            if method_info['formula']:
                info_text += f"\n📐 {method_info['formula']}"
            info_text += f"\n⚡ {method_info['error_order']}"
            
            if method_info['n_constraint']:
                info_text += f"\n⚠️ n debe ser {method_info['n_constraint']}"
            
            self.method_info_label.configure(text=info_text)
            
            # Habilitar/deshabilitar campo n
            n_entry = self.entries.get("Subdivisiones (n)")
            if n_entry:
                if method_info['requires_n']:
                    n_entry.configure(state="normal")
                else:
                    n_entry.configure(state="disabled")
                    
        except Exception as e:
            logger.error(f"Error actualizando info del método: {e}")
            if self.method_info_label:
                self.method_info_label.configure(text=f"Error: {e}")
                
    def calculate_integration(self):
        """Calcular integración usando Newton-Cotes"""
        try:
            # Limpiar resultados anteriores
            if self.results_text:
                self.results_text.delete("1.0", "end")
            
            # Obtener parámetros
            func_str = self.entries["Función f(x)"].get().strip()
            a = float(self.entries["Límite inferior (a)"].get())
            b = float(self.entries["Límite superior (b)"].get())
            method = self.method_var.get()
            
            # Obtener n si es necesario
            n = None
            method_info = self.newton_cotes.get_method_info(method)
            if method_info['requires_n']:
                n_str = self.entries["Subdivisiones (n)"].get().strip()
                if n_str:
                    n = int(n_str)
            
            # Mostrar estado de cálculo
            if self.results_text:
                self.results_text.insert("end", "⏳ Calculando...\n")
                self.results_text.update()
            
            # Realizar integración
            result = self.newton_cotes.integrate(func_str, a, b, method, n)
            self.current_result = result
            
            # Mostrar resultados
            self.display_results(result)
            
            # Actualizar labels de información
            self.update_info_labels(result)
            
        except ValueError as e:
            self.show_error(f"Error en parámetros: {e}")
        except (NewtonCotesError, IntegrationValidationError) as e:
            self.show_error(f"Error de integración: {e}")
        except Exception as e:
            self.show_error(f"Error inesperado: {e}")
            logger.error(f"Error en cálculo de Newton-Cotes: {e}", exc_info=True)
            
    def display_results(self, result):
        """Mostrar resultados detallados"""
        if not self.results_text:
            return
            
        self.results_text.delete("1.0", "end")
        
        # Encabezado
        output = "=" * 50 + "\n"
        output += "📊 RESULTADO INTEGRACIÓN NEWTON-COTES\n"
        output += "=" * 50 + "\n\n"
        
        # Información del problema
        output += f"📝 Función: {result.function}\n"
        output += f"📐 Intervalo: [{result.interval[0]}, {result.interval[1]}]\n"
        output += f"🔧 Método: {result.method}\n\n"
        
        # Resultado principal
        output += f"🎯 RESULTADO: {result.result:.10f}\n\n"
        
        # Detalles del cálculo
        output += "📋 DETALLES DEL CÁLCULO:\n"
        output += "-" * 25 + "\n"
        if result.n_subdivisions:
            output += f"🔢 Subdivisiones (n): {result.n_subdivisions}\n"
        if result.h:
            output += f"📏 Paso (h): {result.h:.8f}\n"
        output += f"⚡ Evaluaciones: {result.evaluations}\n"
        output += f"⏱️ Tiempo: {result.computation_time:.6f} segundos\n"
        output += f"�� Orden de error: {result.error_order}\n\n"
        
        # Fórmula utilizada
        if result.formula:
            output += "📐 FÓRMULA UTILIZADA:\n"
            output += f"{result.formula}\n\n"
        
        # Estimación de precisión
        output += "📈 ESTIMACIÓN DE PRECISIÓN:\n"
        output += "-" * 25 + "\n"
        output += f"�� {result.accuracy_estimate}\n"
        
        # Mostrar en el textbox
        self.results_text.insert("1.0", output)
        
    def update_info_labels(self, result):
        """Actualizar labels de información rápida"""
        if not self.info_labels:
            return
            
        self.info_labels["Resultado"].configure(
            text=f"Resultado: {result.result:.8f}"
        )
        self.info_labels["Tiempo"].configure(
            text=f"Tiempo: {result.computation_time:.4f}s"
        )
        self.info_labels["Evaluaciones"].configure(
            text=f"Evaluaciones: {result.evaluations}"
        )
        self.info_labels["Error"].configure(
            text=f"Error: {result.error_order}"
        )
        
    def show_error(self, message: str):
        """Mostrar mensaje de error"""
        if self.results_text:
            self.results_text.delete("1.0", "end")
            error_text = f"❌ ERROR\n{'='*30}\n\n{message}\n\n"
            error_text += "💡 SUGERENCIAS:\n"
            error_text += "• Verifique la sintaxis de la función\n"
            error_text += "• Asegúrese de que a < b\n"
            error_text += "• Para Simpson 1/3: use n par\n"
            error_text += "• Para Simpson 3/8: use n múltiplo de 3\n"
            self.results_text.insert("1.0", error_text)
        
        # Limpiar labels de información
        if self.info_labels:
            for label in self.info_labels.values():
                label.configure(text=label.cget("text").split(":")[0] + ": --")
                
    def clear_results(self):
        """Limpiar resultados y resetear campos"""
        if self.results_text:
            self.results_text.delete("1.0", "end")
            
            # Mensaje de bienvenida
            welcome_text = "🎯 INTEGRACIÓN NEWTON-COTES\n\n"
            welcome_text += "Seleccione una función, intervalo y método,\n"
            welcome_text += "luego presione 'Calcular'.\n\n"
            welcome_text += "📚 MÉTODOS DISPONIBLES:\n"
            welcome_text += "• Rectángulo: O(h²) - Rápido\n"
            welcome_text += "• Trapecio: O(h²) - Confiable\n"
            welcome_text += "• Simpson 1/3: O(h⁴) - Alta precisión\n"
            welcome_text += "• Simpson 3/8: O(h⁴) - Muy preciso\n"
            self.results_text.insert("1.0", welcome_text)
        
        # Limpiar labels de información
        if self.info_labels:
            for label in self.info_labels.values():
                text = label.cget("text").split(":")[0] + ": --"
                label.configure(text=text)
                
    def show_examples_menu(self):
        """Mostrar menú de ejemplos específicos por método"""
        # Crear ventana de ejemplos
        examples_window = ctk.CTkToplevel(self.content_frame)
        examples_window.title("📝 Ejemplos Newton-Cotes")
        examples_window.geometry("600x500")
        examples_window.grab_set()
        
        # Título
        title_label = ctk.CTkLabel(
            examples_window,
            text="📚 Ejemplos por Método",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame con scroll para ejemplos
        scroll_frame = ctk.CTkScrollableFrame(examples_window, height=350)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Ejemplos organizados por método
        examples_by_method = {
            "Rectángulo Simple": [
                ("x", "0", "1", "rectangle_simple", "1", "Área bajo y=x"),
                ("2*x + 1", "0", "2", "rectangle_simple", "1", "Función lineal"),
            ],
            "Rectángulo Compuesto": [
                ("x**2", "0", "2", "rectangle_composite", "20", "Parábola básica"),
                ("sin(x)", "0", "1.5708", "rectangle_composite", "50", "Seno de 0 a π/2"),
            ],
            "Trapecio Simple": [
                ("x**2 + 1", "0", "1", "trapezoid_simple", "1", "Parábola desplazada"),
                ("exp(x)", "0", "0.5", "trapezoid_simple", "1", "Exponencial pequeña"),
            ],
            "Trapecio Compuesto": [
                ("1/x", "1", "2", "trapezoid_composite", "30", "Función recíproca"),
                ("cos(x)", "0", "1.5708", "trapezoid_composite", "40", "Coseno de 0 a π/2"),
            ],
            "Simpson 1/3 Simple": [
                ("x**3", "0", "1", "simpson_13_simple", "2", "Cúbica exacta"),
                ("x**2 + x + 1", "0", "2", "simpson_13_simple", "2", "Polinomio cuadrático"),
            ],
            "Simpson 1/3 Compuesto": [
                ("x**4", "0", "1", "simpson_13_composite", "10", "Cuártica"),
                ("sqrt(x)", "0", "4", "simpson_13_composite", "20", "Raíz cuadrada"),
                ("1/(1+x**2)", "-1", "1", "simpson_13_composite", "30", "Arctangente (π/2)"),
            ],
            "Simpson 3/8 Simple": [
                ("x**3 + x", "0", "1", "simpson_38_simple", "3", "Cúbica exacta"),
                ("sin(x) + cos(x)", "0", "1", "simpson_38_simple", "3", "Trigonométrica"),
            ],
            "Simpson 3/8 Compuesto": [
                ("x**5", "0", "1", "simpson_38_composite", "12", "Quinta potencia"),
                ("log(x+1)", "0", "1", "simpson_38_composite", "15", "Logaritmo natural"),
                ("exp(-x**2)", "-1", "1", "simpson_38_composite", "18", "Gaussiana"),
            ]
        }
        
        row = 0
        for method_name, examples in examples_by_method.items():
            # Título del método
            method_title = ctk.CTkLabel(
                scroll_frame,
                text=f"🔧 {method_name}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=["#1f538d", "#3d8bff"]
            )
            method_title.grid(row=row, column=0, columnspan=3, pady=(15, 5), padx=10, sticky="w")
            row += 1
            
            # Ejemplos del método
            for func, a, b, method_key, n, description in examples:
                # Botón para cargar ejemplo
                example_btn = ctk.CTkButton(
                    scroll_frame,
                    text=f"📝 {description}",
                    command=lambda f=func, a_val=a, b_val=b, m=method_key, n_val=n: 
                           self.load_specific_example(f, a_val, b_val, m, n_val, examples_window),
                    width=180,
                    height=30
                )
                example_btn.grid(row=row, column=0, pady=2, padx=(20, 5), sticky="w")
                
                # Información del ejemplo
                info_text = f"f(x) = {func}, [{a}, {b}], n = {n}"
                info_label = ctk.CTkLabel(
                    scroll_frame,
                    text=info_text,
                    font=ctk.CTkFont(size=10),
                    text_color=["gray60", "gray40"]
                )
                info_label.grid(row=row, column=1, pady=2, padx=5, sticky="w")
                
                row += 1
        
        # Botón cerrar
        close_btn = ctk.CTkButton(
            examples_window,
            text="Cerrar",
            command=examples_window.destroy
        )
        close_btn.pack(pady=10)
        
    def load_specific_example(self, func, a, b, method, n, window):
        """Cargar ejemplo específico y cerrar ventana"""
        try:
            # Limpiar campos primero
            self.entries["Función f(x)"].delete(0, "end")
            self.entries["Límite inferior (a)"].delete(0, "end")
            self.entries["Límite superior (b)"].delete(0, "end")
            self.entries["Subdivisiones (n)"].delete(0, "end")
            
            # Configurar nuevos valores
            self.entries["Función f(x)"].insert(0, str(func))
            self.entries["Límite inferior (a)"].insert(0, str(a))
            self.entries["Límite superior (b)"].insert(0, str(b))
            self.entries["Subdivisiones (n)"].insert(0, str(n))
            
            # Configurar método y actualizar interfaz
            self.method_var.set(method)
            
            # Forzar actualización de la interfaz
            self.update_idletasks()
            self.on_method_change()
            
            # Actualizar radio buttons visualmente
            for button in self.method_buttons:
                if button.cget("value") == method:
                    button.select()
                else:
                    button.deselect()
            
            # Cerrar ventana
            window.destroy()
            
            # Obtener nombre del método para mostrar
            method_names = {
                "rectangle_simple": "Rectángulo Simple",
                "rectangle_composite": "Rectángulo Compuesto",
                "trapezoid_simple": "Trapecio Simple",
                "trapezoid_composite": "Trapecio Compuesto",
                "simpson_13_simple": "Simpson 1/3 Simple",
                "simpson_13_composite": "Simpson 1/3 Compuesto",
                "simpson_38_simple": "Simpson 3/8 Simple",
                "simpson_38_composite": "Simpson 3/8 Compuesto"
            }
            
            method_display = method_names.get(method, method)
            
            # Mostrar mensaje actualizado
            if self.results_text:
                self.results_text.delete("1.0", "end")
                example_text = f"✅ EJEMPLO CARGADO EXITOSAMENTE\n\n"
                example_text += f"📝 Función: {func}\n"
                example_text += f"📐 Intervalo: [{a}, {b}]\n"
                example_text += f"🔧 Método: {method_display}\n"
                example_text += f"🔢 Subdivisiones: {n}\n\n"
                example_text += "💡 Todos los campos han sido actualizados.\n"
                example_text += "🚀 Presione 'Calcular' para ver el resultado."
                self.results_text.insert("1.0", example_text)
                
        except Exception as e:
            print(f"Error cargando ejemplo: {e}")
            # Mostrar mensaje de error más detallado
            if self.results_text:
                self.results_text.delete("1.0", "end")
                error_text = f"❌ ERROR AL CARGAR EJEMPLO\n\n"
                error_text += f"Detalles del error: {str(e)}\n\n"
                error_text += f"Claves disponibles: {list(self.entries.keys())}\n\n"
                error_text += "💡 Reportar este error al desarrollador."
                self.results_text.insert("1.0", error_text)
