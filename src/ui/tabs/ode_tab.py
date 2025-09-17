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
from src.ui.components.constants import VALIDATION, DEFAULT_CONFIGS, UI, PLOT, COLORS
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
        
        # Función hardcodeada por ahora (temporal)
        def func(t, y):
            return y - t**2 + 1
        
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
            
            if method == "rk4" and res.k1_values is not None:
                # Tabla extendida para RK4 con k1, k2, k3, k4, y n+1
                self.table.insert("end", f"{'t':>10} {'y':>12} {'k1':>12} {'k2':>12} {'k3':>12} {'k4':>12} {'y n+1':>12}\n")
                self.table.insert("end", "-"*82+"\n")
                
                # Mostrar filas con los valores k1, k2, k3, k4, y n+1
                for i in range(len(res.k1_values)):
                    # Los valores k1, k2, k3, k4 del paso i se calculan en t[i], y[i] para obtener y[i+1]
                    ti, yi = res.t[i], res.y[i].squeeze()
                    k1i = res.k1_values[i].squeeze()
                    k2i = res.k2_values[i].squeeze()
                    k3i = res.k3_values[i].squeeze()
                    k4i = res.k4_values[i].squeeze()
                    y_nexti = res.y_next_values[i].squeeze()
                    self.table.insert("end", f"{ti:>10.6f} {yi:>12.6f} {k1i:>12.6f} {k2i:>12.6f} {k3i:>12.6f} {k4i:>12.6f} {y_nexti:>12.6f}\n")
                
                # Última fila (resultado final sin k values)
                if len(res.t) > len(res.k1_values):
                    final_t, final_y = res.t[-1], res.y[-1].squeeze()
                    self.table.insert("end", f"{final_t:>10.6f} {final_y:>12.6f} {'-':>12} {'-':>12} {'-':>12} {'-':>12} {'-':>12}\n")
            elif method == "euler" and res.y_next_values is not None:
                # Tabla extendida para Euler con y n+1
                self.table.insert("end", f"{'t':>12} {'y':>15} {'y n+1':>15}\n")
                self.table.insert("end", "-"*44+"\n")
                
                # Mostrar filas con los valores y n+1
                for i in range(len(res.y_next_values)):
                    # El valor y_next del paso i se calcula en t[i], y[i] para obtener y[i+1]
                    ti, yi = res.t[i], res.y[i].squeeze()
                    y_nexti = res.y_next_values[i].squeeze()
                    self.table.insert("end", f"{ti:>12.6f} {yi:>15.6f} {y_nexti:>15.6f}\n")
                
                # Última fila (resultado final sin y_next)
                if len(res.t) > len(res.y_next_values):
                    final_t, final_y = res.t[-1], res.y[-1].squeeze()
                    self.table.insert("end", f"{final_t:>12.6f} {final_y:>15.6f} {'-':>15}\n")
            else:
                # Tabla simple para otros métodos (Heun)
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
        self.tol_entry = self._labeled_entry(left, "Tolerancia =", "1e-6")
        
        # Selector de método
        self.method_var = ctk.StringVar(value="rk4")
        ctk.CTkLabel(left, text="Método").pack(pady=(10,0))
        ctk.CTkOptionMenu(left, variable=self.method_var, values=["euler","heun","rk4"]).pack(pady=(0,10), fill="x")
        
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
