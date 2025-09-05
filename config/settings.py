"""
Configuración del Simulador Matemático
"""

import matplotlib.pyplot as plt
import customtkinter as ctk

# Configuración de la interfaz
UI_CONFIG = {
    "appearance_mode": "dark",
    "color_theme": "blue",
    "default_font_size": 12,
    "title_font_size": 24,
    "window_geometry": "1400x800",
    "window_title": "🧮 Simulador Matemático Avanzado v4.0"
}

# Configuración de matplotlib
PLOT_CONFIG = {
    "style": "dark_background",
    "figure_size": (10, 6),
    "dpi": 100,
    "grid": True,
    "legend": True
}

# Configuración numérica
NUMERICAL_CONFIG = {
    "default_tolerance": 1e-6,
    "max_iterations": 1000,
    "default_step_size": 0.1,
    "precision_digits": 8
}

def configure_ui():
    """Configura la interfaz de usuario"""
    ctk.set_appearance_mode(UI_CONFIG["appearance_mode"])
    ctk.set_default_color_theme(UI_CONFIG["color_theme"])

def configure_matplotlib():
    """Configura matplotlib para el tema oscuro"""
    plt.style.use(PLOT_CONFIG["style"])

# Alias para compatibilidad
UI_SETTINGS = UI_CONFIG
NUMERICAL_SETTINGS = NUMERICAL_CONFIG
