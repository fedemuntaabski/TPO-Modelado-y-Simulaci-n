#!/usr/bin/env python3
"""
Demo extremadamente simplificada para mostrar la resolución de EDOs usando Runge-Kutta.
"""

import subprocess
import sys

# Instalar dependencias necesarias
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'customtkinter', 'matplotlib', 'numpy', 'scipy'])
    print("Dependencias instaladas correctamente.")
except subprocess.CalledProcessError as e:
    print(f"Error instalando dependencias: {e}")
    sys.exit(1)

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.integrate import solve_ivp
import time


class SimpleDemoApp(ctk.CTk):
    """Aplicación demo extremadamente simplificada para EDOs"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("🧮 Demo Simple de EDOs")
        self.geometry("1000x650")
        self.minsize(800, 600)
        
        # Construir interfaz
        self._build_layout()
    
    def _run(self):
        """Ejecutar la solución de la EDO"""
        try:
            # Ejemplo predefinido: y' = y - t^2 + 1, y(0) = 0.5
            def f(t, y):
                return [y[0] - t**2 + 1]
            
            # Parámetros
            t0 = 0.0
            tf = 2.0
            y0 = [0.5]
            method = self.method_var.get().lower()
            
            # Mapear métodos a los disponibles en scipy
            method_map = {
                "euler": "RK23",  # Scipy no tiene Euler, usamos RK23 como aproximación
                "heun": "RK23",   # Scipy no tiene Heun, usamos RK23 como aproximación
                "rk2": "RK23",    # RK23 es una variante de RK2
                "rk4": "RK45",    # RK45 es una variante de RK4
                "rk45": "RK45"    # RK45 es el método adaptativo
            }
            
            # Resolver EDO
            start_time = time.time()
            sol = solve_ivp(f, [t0, tf], y0, method=method_map[method], dense_output=True)
            computation_time = time.time() - start_time
            
            # Crear puntos para graficar
            t_points = np.linspace(t0, tf, 100)
            y_points = sol.sol(t_points)[0]
            
            # Mostrar resultados gráficamente
            self.ax.clear()
            self.ax.plot(t_points, y_points)
            self.ax.set_xlabel("t")
            self.ax.set_ylabel("y")
            self.ax.set_title(f"Método: {method} • EDO: y' = y - t² + 1")
            self.canvas.draw()
            
            # Mostrar resultados en tabla
            self.table.delete("0.0", "end")
            self.table.insert("end", f"{'t':>12} {'y':>18}\n")
            self.table.insert("end", "-"*32+"\n")
            for t, y in zip(t_points[::5], y_points[::5]):  # Mostrar solo algunos puntos
                self.table.insert("end", f"{t:>12.6f} {y:>18.10f}\n")
            
            # Mostrar mensaje con resultados
            self.msg.configure(text=f"Listo en {computation_time:.3f}s • Pasos: {len(sol.t)}")
        except Exception as e:
            self.msg.configure(text=f"Error: {e}")
            print(f"Error: {e}")
    
    def _build_layout(self):
        """Construir la interfaz de usuario"""
        # Crear contenedor principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel izquierdo para controles
        left = ctk.CTkFrame(main_frame, width=300)
        left.pack(side="left", fill="y", padx=10, pady=10)
        
        # Título
        ctk.CTkLabel(left, text="EDOs • Runge–Kutta", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0,10))
        
        # Información sobre el ejemplo
        info_text = "Este es un ejemplo predefinido:\n\ny' = y - t² + 1\ny(0) = 0.5"
        ctk.CTkLabel(left, text=info_text, wraplength=280, justify="left").pack(pady=10)
        
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
        right = ctk.CTkFrame(main_frame)
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


def run_simple_demo():
    """Ejecuta la aplicación demo simplificada"""
    try:
        print("🚀 Iniciando Demo Simple de EDOs")
        app = SimpleDemoApp()
        print("✅ Aplicación inicializada correctamente")
        app.mainloop()
        return 0
    except Exception as e:
        print(f"❌ Error en aplicación demo: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run_simple_demo())
