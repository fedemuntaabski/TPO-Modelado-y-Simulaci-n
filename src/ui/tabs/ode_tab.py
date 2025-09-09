import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config.settings import NUMERICAL_CONFIG, configure_matplotlib
from src.core.function_parser import validate_function_2d, create_function_evaluator_2d
from src.core.ode_runge_kutta import RungeKuttaSolver

class ODETab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master); configure_matplotlib(); self._build_layout()

    def _parse_inputs(self):
        func_str = self.func_entry.get().strip()
        ok, msg = validate_function_2d(func_str)
        if not ok: raise ValueError(f"Función inválida: {msg}")
        f = create_function_evaluator_2d(func_str)
        t0 = float(self.t0_entry.get().strip()); tf = float(self.tf_entry.get().strip()); y0 = float(self.y0_entry.get().strip())
        method = self.method_var.get().strip().lower()
        step_text = self.step_entry.get().strip(); step = float(step_text) if step_text else None
        tol = float(self.tol_entry.get().strip())
        return f, t0, tf, y0, method, step, tol, func_str

    def _run(self):
        try:
            f, t0, tf, y0, method, step, tol, func_str = self._parse_inputs()
            
            # Crear wrapper para convertir entre escalar y array
            def f_array(t, y):
                return np.array([f(t, y[0])])
            
            solver = RungeKuttaSolver(method=method, step=step, tol=tol)
            res = solver.solve(f_array, t0, tf, [y0], step=step)
            
            self.ax.clear()
            self.ax.plot(res.t, res.y.squeeze())
            self.ax.set_xlabel("t")
            self.ax.set_ylabel("y")
            self.ax.set_title(f"Método: {res.method} • pasos: {res.steps_taken}")
            self.canvas.draw()
            
            self.table.delete("0.0","end")
            self.table.insert("end", f"{'t':>12} {'y':>18}\n")
            self.table.insert("end","-"*32+"\n")
            for ti, yi in zip(res.t, res.y.squeeze()):
                self.table.insert("end", f"{ti:>12.6f} {yi:>18.10f}\n")
            
            extra = f" • error máx. estimado ≈ {res.max_error_estimate:.2e}" if res.max_error_estimate is not None else ""
            self.msg.configure(text=f"Listo en {res.computation_time:.3f}s{extra}")
        except Exception as e:
            self.msg.configure(text=f"Error: {e}")

    def _labeled_entry(self, parent, label, default=""):
        frame = ctk.CTkFrame(parent); frame.pack(fill="x", pady=4)
        ctk.CTkLabel(frame, text=label, width=140, anchor="w").pack(side="left", padx=(4,4))
        entry = ctk.CTkEntry(frame); entry.insert(0, default); entry.pack(side="left", fill="x", expand=True); return entry

    def _build_layout(self):
        left = ctk.CTkFrame(self, width=300); left.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkLabel(left, text="EDOs • Runge–Kutta", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0,10))
        self.func_entry = self._labeled_entry(left, "f(t,y) =", "y - t**2 + 1"); self.t0_entry = self._labeled_entry(left, "t0 =", "0.0")
        self.tf_entry = self._labeled_entry(left, "tf =", "2.0"); self.y0_entry = self._labeled_entry(left, "y0 =", "0.5")
        self.step_entry = self._labeled_entry(left, "Paso h (p/ fijos) =", str(NUMERICAL_CONFIG.get("ode_default_step", 0.1)))
        self.tol_entry = self._labeled_entry(left, "Tolerancia (RK45) =", "1e-6")
        self.method_var = ctk.StringVar(value="rk4"); ctk.CTkLabel(left, text="Método").pack(pady=(10,0))
        ctk.CTkOptionMenu(left, variable=self.method_var, values=["euler","heun","rk2","rk4","rk45"]).pack(pady=(0,10), fill="x")
        ctk.CTkButton(left, text="Ejecutar", command=self._run).pack(pady=10, fill="x")
        self.msg = ctk.CTkLabel(left, text="", wraplength=280, anchor="w", justify="left"); self.msg.pack(pady=(4,10), fill="x")
        right = ctk.CTkFrame(self); right.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.fig = plt.Figure(figsize=(6,4)); self.ax = self.fig.add_subplot(111); self.ax.set_xlabel("t"); self.ax.set_ylabel("y")
        self.canvas = FigureCanvasTkAgg(self.fig, master=right); self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.table = ctk.CTkTextbox(right, height=180); self.table.configure(font=("Consolas", 11)); self.table.pack(fill="x", expand=False, pady=(10,0))
