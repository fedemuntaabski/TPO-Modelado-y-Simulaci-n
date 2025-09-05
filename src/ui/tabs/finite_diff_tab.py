"""
Pestaña de diferencias finitas - Versión simplificada.

Solo entrada por lista de puntos con área de resultados expandible.
"""

import customtkinter as ctk
import numpy as np
from typing import Optional, List, Dict

from src.ui.components.base_tab import BaseTab
from src.core.finite_differences import FiniteDifferences
from config.settings import NUMERICAL_CONFIG


class FiniteDiffTab(BaseTab):
    """
    Pestaña para diferencias finitas simplificada.
    Solo entrada por lista con área de resultados grande.
    """
    
    def __init__(self, parent):
        super().__init__(parent, "🔢 Diferencias Finitas")
        self.calculator = FiniteDifferences()
        self.data_points = []
    
    def create_content(self):
        """Crear contenido específico para diferencias finitas"""
        # Configurar el grid principal para que se expanda
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=0)  # Input section
        self.content_frame.grid_rowconfigure(2, weight=1)  # Results section (expandible)
        
        # Descripción
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Diferencias Finitas - Entrada directa de puntos (x, f(x))",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        desc_label.grid(row=0, column=0, pady=10, padx=20, sticky="ew")
        
        # Sección de entrada (más compacta)
        self.create_input_section()
        
        # Sección de resultados (expandible)
        self.create_large_results_section()

    def create_input_section(self):
        """Crear sección de entrada compacta solo para lista de puntos"""
        # Frame para la entrada
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Paso h común para todos los puntos
        ctk.CTkLabel(input_frame, text="Paso h (común):").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.h_entry = ctk.CTkEntry(input_frame, width=100)
        self.h_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.h_entry.insert(0, "0.1")
        
        # Tabla para entrada de puntos
        table_label = ctk.CTkLabel(
            input_frame,
            text="Puntos (x, f(x)):",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        table_label.grid(row=1, column=0, columnspan=3, pady=(10,5), padx=10, sticky="w")
        
        # Frame para la tabla
        self.table_frame = ctk.CTkFrame(input_frame)
        self.table_frame.grid(row=2, column=0, columnspan=3, pady=5, padx=10, sticky="ew")
        
        # Headers
        ctk.CTkLabel(self.table_frame, text="x", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=5, pady=2
        )
        ctk.CTkLabel(self.table_frame, text="f(x)", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=1, padx=5, pady=2
        )
        
        # Crear entradas para puntos
        self.point_entries = []
        for i in range(6):  # 6 filas por defecto
            x_entry = ctk.CTkEntry(self.table_frame, width=80)
            fx_entry = ctk.CTkEntry(self.table_frame, width=80)
            
            x_entry.grid(row=i+1, column=0, padx=5, pady=2)
            fx_entry.grid(row=i+1, column=1, padx=5, pady=2)
            
            self.point_entries.append((x_entry, fx_entry))
        
        # Valores por defecto
        default_points = [
            ("1.0", "3.0"),
            ("1.1", "3.651"),
            ("1.2", "4.448"),
            ("1.3", "5.403")
        ]
        
        for i, (x_val, fx_val) in enumerate(default_points):
            if i < len(self.point_entries):
                self.point_entries[i][0].insert(0, x_val)
                self.point_entries[i][1].insert(0, fx_val)
        
        # Botón de cálculo
        calculate_btn = ctk.CTkButton(
            input_frame,
            text="🧮 Calcular Diferencias Finitas",
            command=self.calculate_list_mode,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=250
        )
        calculate_btn.grid(row=3, column=0, columnspan=3, pady=15, padx=10)

    def create_large_results_section(self):
        """Crear sección de resultados expandible y grande"""
        # Frame principal para resultados que se expande
        self.results_frame = ctk.CTkFrame(self.content_frame)
        self.results_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)
        
        # Título de resultados
        results_title = ctk.CTkLabel(
            self.results_frame,
            text="📊 Resultados",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_title.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        
        # Área de texto expandible para resultados
        self.results_text = ctk.CTkTextbox(
            self.results_frame,
            height=400,  # Altura inicial grande
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.results_text.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
        
        # Mensaje inicial
        initial_message = """🔢 Diferencias Finitas - Listo para calcular

📝 Instrucciones:
1. Ingrese el paso h común para todos los puntos
2. Complete la tabla con los puntos (x, f(x))
3. Haga clic en "Calcular Diferencias Finitas"

ℹ️ El sistema seleccionará automáticamente:
• Método Progresivo: para el primer punto
• Método Central: para puntos intermedios (mayor precisión)
• Método Regresivo: para el último punto

Los resultados mostrarán explicaciones paso a paso del proceso de cálculo."""
        
        self.results_text.insert("0.0", initial_message)

    def calculate_list_mode(self):
        """Ejecutar cálculo en modo lista"""
        try:
            # Validar paso h
            try:
                h = float(self.h_entry.get())
                if h <= 0:
                    raise ValueError("El paso h debe ser positivo")
            except ValueError:
                self.show_error("Paso h inválido. Ingrese un número positivo.")
                return
            
            # Recopilar puntos válidos
            data_points = []
            for i, (x_entry, fx_entry) in enumerate(self.point_entries):
                x_text = x_entry.get().strip()
                fx_text = fx_entry.get().strip()
                
                if x_text and fx_text:  # Solo procesar si ambos campos tienen datos
                    try:
                        x = float(x_text)
                        fx = float(fx_text)
                        data_points.append({
                            "x": x,
                            "h": h,
                            "fx": fx
                        })
                    except ValueError:
                        self.show_error(f"Error en fila {i+1}: valores numéricos inválidos")
                        return
            
            if len(data_points) < 2:
                self.show_error("Se necesitan al menos 2 puntos para calcular diferencias finitas")
                return
            
            # Calcular usando auto_calculate_list
            results = self.calculator.auto_calculate_list(data_points)
            
            # Mostrar resultados mejorados
            self._display_improved_results(results, h, manual_mode=False)
            
        except Exception as e:
            self.show_error(f"Error en cálculo: {e}")

    # Métodos heredados de BaseTab - mantener para compatibilidad
    def progressive_method(self):
        """Método progresivo - ahora redirige al cálculo principal"""
        self.calculate_list_mode()
    
    def regressive_method(self):
        """Método regresivo - ahora redirige al cálculo principal"""
        self.calculate_list_mode()
    
    def central_method(self):
        """Método central - ahora redirige al cálculo principal"""
        self.calculate_list_mode()
    
    def auto_calculate(self):
        """Cálculo automático - ahora redirige al cálculo principal"""
        self.calculate_list_mode()
    
    def complete_analysis(self):
        """Análisis completo - ahora redirige al cálculo principal"""
        self.calculate_list_mode()

    def _display_improved_results(self, results, h, manual_mode=False, function_str=None):
        """Mostrar resultados mejorados con explicaciones paso a paso"""
        self.results_text.delete("1.0", "end")
        
        output = []
        output.append("🎯 RESULTADOS DIFERENCIAS FINITAS")
        output.append("=" * 60)
        output.append("")
        
        if manual_mode and function_str:
            output.append(f"📝 Función: f(x) = {function_str}")
        
        output.append(f"📐 Paso común: h = {h}")
        output.append(f"📊 Total de puntos procesados: {len(results)}")
        output.append("")
        
        # Estadísticas de métodos
        methods_count = {}
        for result in results:
            method = result.get('auto_selected_method', result.get('method', 'unknown'))
            methods_count[method] = methods_count.get(method, 0) + 1
        
        output.append("🔧 MÉTODOS UTILIZADOS:")
        for method, count in methods_count.items():
            output.append(f"   • {method.title()}: {count} vez(es)")
        output.append("")
        
        # Resultados detallados para cada punto
        for i, result in enumerate(results, 1):
            output.append(f"{'='*50}")
            output.append(f"📍 PUNTO {i}: x = {result['x']}")
            output.append(f"{'='*50}")
            
            # Información del método
            method = result.get('auto_selected_method', result.get('method', 'unknown'))
            output.append(f"🔸 Método seleccionado: {method.title()}")
            output.append(f"   Fórmula: {result.get('formula', 'N/A')}")
            output.append(f"   Error de truncamiento: {result.get('error_order', 'N/A')}")
            
            # Justificación de selección automática
            if 'position_in_list' in result:
                pos = result['position_in_list'] + 1
                total = result['total_points']
                if pos == 1:
                    justification = "Primer punto → Método progresivo"
                elif pos == total:
                    justification = "Último punto → Método regresivo"
                else:
                    justification = "Punto intermedio → Método central (mayor precisión)"
                output.append(f"   Justificación: {justification}")
            
            output.append("")
            
            # Proceso de cálculo
            output.append("📝 PROCESO DE CÁLCULO:")
            output.append("-" * 30)
            
            # Evaluaciones de función
            if 'fx_minus_h' in result:
                output.append(f"   f({result['x'] - h:.3f}) = {result['fx_minus_h']:.6f}")
            if 'fx' in result:
                output.append(f"   f({result['x']:.3f}) = {result['fx']:.6f}")
            if 'fx_plus_h' in result:
                output.append(f"   f({result['x'] + h:.3f}) = {result['fx_plus_h']:.6f}")
            
            output.append("")
            
            # Sustitución en fórmula
            output.append("🧮 SUSTITUCIÓN EN FÓRMULA:")
            if method == 'progressive':
                output.append(f"   f'({result['x']}) ≈ [{result['fx_plus_h']:.6f} - {result['fx']:.6f}] / {h}")
                output.append(f"   f'({result['x']}) ≈ {result['fx_plus_h'] - result['fx']:.6f} / {h}")
            elif method == 'regressive':
                output.append(f"   f'({result['x']}) ≈ [{result['fx']:.6f} - {result['fx_minus_h']:.6f}] / {h}")
                output.append(f"   f'({result['x']}) ≈ {result['fx'] - result['fx_minus_h']:.6f} / {h}")
            elif method == 'central':
                output.append(f"   f'({result['x']}) ≈ [{result['fx_plus_h']:.6f} - {result['fx_minus_h']:.6f}] / (2 × {h})")
                output.append(f"   f'({result['x']}) ≈ {result['fx_plus_h'] - result['fx_minus_h']:.6f} / {2 * h}")
            
            output.append("")
            
            # Resultado final
            output.append("🎯 RESULTADO FINAL:")
            output.append(f"   f'({result['x']}) ≈ {result['derivative']:.8f}")
            
            # Análisis de error
            output.append("")
            output.append("📊 ANÁLISIS DE ERROR:")
            error_order = result.get('error_order', 'N/A')
            if error_order == 'O(h²)':
                precision = "ALTA (error cuadrático)"
                estimated_error = h**2
            else:
                precision = "MEDIA (error lineal)"
                estimated_error = h
            
            output.append(f"   Error de truncamiento: {error_order}")
            output.append(f"   Precisión: {precision}")
            output.append(f"   Error local estimado: ≈ {estimated_error:.6f}")
            output.append("")
        
        # Resumen final
        output.append("="*60)
        output.append("📈 RESUMEN GENERAL")
        output.append("="*60)
        output.append(f"✅ Procesamiento completado exitosamente")
        output.append(f"📊 {len(results)} derivadas calculadas")
        output.append(f"🎯 Paso común utilizado: h = {h}")
        
        # Recomendaciones
        output.append("")
        output.append("💡 RECOMENDACIONES:")
        if any(result.get('error_order') == 'O(h²)' for result in results):
            output.append("   • Excelente: Se utilizó método central para máxima precisión")
        output.append("   • Para mayor precisión, reduzca el valor de h")
        output.append("   • Para puntos extremos, considere agregar más datos")
        
        # Mostrar en el widget de texto
        result_text = "\n".join(output)
        self.results_text.insert("1.0", result_text)

    def show_error(self, message):
        """Mostrar mensaje de error en el área de resultados"""
        self.results_text.delete("1.0", "end")
        error_msg = f"❌ ERROR\n\n{message}\n\nPor favor, corrija los datos e intente nuevamente."
        self.results_text.insert("1.0", error_msg)
