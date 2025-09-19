"""
Archivo principal para ejecutar la aplicación de interpolación de Lagrange.
"""

import os
import sys
import customtkinter as ctk

# Añadir el directorio raíz al path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importar la aplicación
from lagrange_app import LagrangeApp

if __name__ == "__main__":
    # Crear la ventana principal
    root = ctk.CTk()
    app = LagrangeApp(root)
    
    # Iniciar el bucle principal
    root.mainloop()