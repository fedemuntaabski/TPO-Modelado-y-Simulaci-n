"""
Pestaña para encontrar raíces de ecuaciones
Implementa la clase RootsTab para el simulador matemático
Módulo principal que coordina UI, métodos y graficación
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from .roots_tab_ui import RootsTabUI
from .roots_tab_methods import RootsTabMethods

class RootsTab(QWidget):
    """
    Pestaña para encontrar raíces de ecuaciones
    Coordina entre la interfaz, métodos numéricos y graficación
    """

    def __init__(self, keyboard, plot_widget):
        super().__init__()
        self.keyboard = keyboard
        self.plot_widget = plot_widget

        # Crear instancia de UI
        self.ui = RootsTabUI(keyboard, plot_widget)

        # Crear instancia de métodos
        self.methods = RootsTabMethods(self.ui)

        # Conectar el botón de resolver
        self.ui.solve_button.clicked.connect(self.methods.find_root)

        # Configurar layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.ui.get_main_widget())
        self.setLayout(layout)

    def clear_results(self):
        """Limpia los resultados de la pestaña"""
        self.ui.results_text.clear()
        self.ui.results_table.setRowCount(0)
        self.plot_widget.clear_plot()
