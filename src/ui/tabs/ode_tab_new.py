"""
Pestaña para resolver ecuaciones diferenciales ordinarias (EDOs).

Implementa la interfaz gráfica para varios métodos de Runge-Kutta
siguiendo principios SOLID y DRY.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Optional, Dict, Any, Tuple, Callable

from src.ui.components.base_tab import BaseTab
from src.ui.components.mixins import InputValidationMixin, ResultDisplayMixin
from src.ui.components.constants import VALIDATION, DEFAULT_CONFIGS, UI, PLOT, COLORS
from src.core.function_parser import parse_function
from src.core.ode_runge_kutta import RungeKuttaSolver
from config.settings import NUMERICAL_CONFIG


class ODETab(BaseTab):
    """
    Pestaña para resolver ecuaciones diferenciales ordinarias.
    Hereda funcionalidad común de BaseTab.
    """
    
    def __init__(self, parent):
        super().__init__(parent, "🔄 Ecuaciones Diferenciales")
        self._build_layout()
    
    def _parse_inputs(self):
        """Parsear entradas del usuario"""
        func_str = self.func_entry.get().strip()
        
        # Validar y crear función
        func = parse_function(func_str, ["t", "y"])
        
        # Parsear parámetros numéricos
        t0 = float(self.t0_entry.get().strip())
        tf = float(self.tf_entry.get().strip())
        y0 = float(self.y0_entry.get().strip())
        method = self.method_var.get().strip().lower()
        
        # Paso (opcional)
        step_text = self.step_entry.get().strip()
        step = float(step_text) if step_text else None
        
        # Tolerancia
        tol = float(self.tol_entry.get().strip())
        
        return func, t0, tf, y0, method, step, tol, func_str
    
    def _run(self):
        """Ejecutar la solución de la EDO"""
        try:
            # Obtener parámetros
            f, t0, tf, y0, method, step, tol, func_str = self._parse_inputs()
            
            # Crear wrapper para convertir entre escalar y array
            def f_array(t, y):
                return np.array([f(t, y[0])])
            
            # Resolver la EDO
            solver = RungeKuttaSolver(method=method, step=step, tol=tol)
            res = solver.solve(f_array, t0, tf, [y0], step=step)
            
            # Mostrar resultados gráficamente
            self.ax.clear()
            self.ax.plot(res.t, res.y.squeeze())
            self.ax.set_xlabel("t")
            self.ax.set_ylabel("y")
            self.ax.set_title(f"Método: {res.method} • pasos: {res.steps_taken}")
            self.canvas.draw()
            
            # Mostrar resultados en tabla
            self.table.delete("0.0", "end")
            self.table.insert("end", f"{'t':>12} {'y':>18}\n")
            self.table.insert("end", "-"*32+"\n")
            for ti, yi in zip(res.t, res.y.squeeze()):
                self.table.insert("end", f"{ti:>12.6f} {yi:>18.10f}\n")
            
            # Mostrar mensaje con resultados
            extra = f" • error máx. estimado ≈ {res.max_error_estimate:.2e}" if res.max_error_estimate is not None else ""
            self.msg.configure(text=f"Listo en {res.computation_time:.3f}s{extra}")
        except Exception as e:
            self.msg.configure(text=f"Error: {e}")
    
    def _labeled_entry(self, parent, label, default=""):
        """Crear un entry con etiqueta"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=4)
        ctk.CTkLabel(frame, text=label, width=140, anchor="w").pack(side="left", padx=(4,4))
        entry = ctk.CTkEntry(frame)
        entry.insert(0, default)
        entry.pack(side="left", fill="x", expand=True)
        return entry
    
    def _build_layout(self):
        """Construir la interfaz de usuario"""
        # Usar el scroll_frame que proporciona BaseTab
        container = self.scroll_frame
        
        # Panel izquierdo para controles
        left = ctk.CTkFrame(container, width=300)
        left.pack(side="left", fill="y", padx=10, pady=10)
        
        # Título
        ctk.CTkLabel(left, text="EDOs • Runge–Kutta", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0,10))
        
        # Entradas de usuario
        self.func_entry = self._labeled_entry(left, "f(t,y) =", "y - t**2 + 1")
        self.t0_entry = self._labeled_entry(left, "t0 =", "0.0")
        self.tf_entry = self._labeled_entry(left, "tf =", "2.0")
        self.y0_entry = self._labeled_entry(left, "y0 =", "0.5")
        self.step_entry = self._labeled_entry(left, "Paso h (p/ fijos) =", str(NUMERICAL_CONFIG.get("ode_default_step", 0.1)))
        self.tol_entry = self._labeled_entry(left, "Tolerancia (RK45) =", "1e-6")
        
        # Selector de método
        self.method_var = ctk.StringVar(value="rk4")
        ctk.CTkLabel(left, text="Método").pack(pady=(10,0))
        ctk.CTkOptionMenu(left, variable=self.method_var, values=["euler","heun","rk2","rk4","rk45"]).pack(pady=(0,10), fill="x")
        
        # Botón de ejecución
        ctk.CTkButton(left, text="Ejecutar", command=self._run).pack(pady=10, fill="x")
        
        # Mensaje de estado
        self.msg = ctk.CTkLabel(left, text="", wraplength=280, anchor="w", justify="left")
        self.msg.pack(pady=(4,10), fill="x")
        
        # Panel derecho para visualización
        right = ctk.CTkFrame(container)
        right.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Gráfico
        self.fig = plt.Figure(figsize=(6,4))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("t")
        self.ax.set_ylabel("y")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Tabla de resultados
        self.table = ctk.CTkTextbox(right, height=180)
        self.table.configure(font=("Consolas", 11))
        self.table.pack(fill="x", expand=False, pady=(10,0))
