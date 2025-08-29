"""
Temas y estilos para el Simulador Matemático Avanzado
Define colores, fuentes y estilos consistentes para toda la aplicación
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

class DarkTheme:
    """
    Tema oscuro moderno con colores profesionales
    """
    
    # Colores principales
    BACKGROUND_PRIMARY = "#2c3e50"      # Gris oscuro principal
    BACKGROUND_SECONDARY = "#34495e"    # Gris medio
    BACKGROUND_LIGHT = "#455a75"        # Gris claro
    
    # Colores de texto
    TEXT_PRIMARY = "#ecf0f1"            # Blanco suave
    TEXT_SECONDARY = "#bdc3c7"          # Gris claro
    TEXT_ACCENT = "#3498db"             # Azul de acento
    
    # Colores de botones y controles
    BUTTON_PRIMARY = "#3498db"          # Azul principal
    BUTTON_SUCCESS = "#27ae60"          # Verde éxito
    BUTTON_WARNING = "#f39c12"          # Naranja advertencia
    BUTTON_DANGER = "#e74c3c"           # Rojo peligro
    BUTTON_INFO = "#9b59b6"             # Púrpura información
    
    # Colores de bordes
    BORDER_LIGHT = "#556b83"            # Borde claro
    BORDER_DARK = "#1e2a38"             # Borde oscuro
    
    # Colores de hover
    HOVER_LIGHT = "#4a6580"             # Hover claro
    HOVER_ACCENT = "#2980b9"            # Hover azul
    
    @staticmethod
    def get_main_stylesheet():
        """Retorna el stylesheet principal para la aplicación"""
        return f"""
        /* Estilos principales */
        QMainWindow {{
            background-color: {DarkTheme.BACKGROUND_PRIMARY};
            color: {DarkTheme.TEXT_PRIMARY};
        }}
        
        QWidget {{
            background-color: {DarkTheme.BACKGROUND_PRIMARY};
            color: {DarkTheme.TEXT_PRIMARY};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        /* Pestañas */
        QTabWidget::pane {{
            border: 2px solid {DarkTheme.BORDER_LIGHT};
            background-color: {DarkTheme.BACKGROUND_SECONDARY};
            border-radius: 8px;
        }}
        
        QTabBar::tab {{
            background-color: {DarkTheme.BACKGROUND_LIGHT};
            color: {DarkTheme.TEXT_SECONDARY};
            padding: 12px 20px;
            margin-right: 3px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border: 1px solid {DarkTheme.BORDER_LIGHT};
            font-weight: bold;
            min-width: 120px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {DarkTheme.BACKGROUND_SECONDARY};
            color: {DarkTheme.TEXT_PRIMARY};
            border-bottom: 3px solid {DarkTheme.BUTTON_PRIMARY};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {DarkTheme.HOVER_LIGHT};
            color: {DarkTheme.TEXT_PRIMARY};
        }}
        
        /* Grupos de controles */
        QGroupBox {{
            font-weight: bold;
            font-size: 14px;
            border: 2px solid {DarkTheme.BORDER_LIGHT};
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 15px;
            background-color: {DarkTheme.BACKGROUND_SECONDARY};
            color: {DarkTheme.TEXT_PRIMARY};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 8px 0 8px;
            color: {DarkTheme.TEXT_ACCENT};
            font-weight: bold;
        }}
        
        /* Controles de entrada */
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
            padding: 10px;
            border: 2px solid {DarkTheme.BORDER_LIGHT};
            border-radius: 6px;
            font-size: 12px;
            background-color: {DarkTheme.BACKGROUND_LIGHT};
            color: {DarkTheme.TEXT_PRIMARY};
        }}
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
            border-color: {DarkTheme.BUTTON_PRIMARY};
            background-color: {DarkTheme.BACKGROUND_SECONDARY};
        }}
        
        /* Botones */
        QPushButton {{
            padding: 10px 16px;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 12px;
            min-height: 20px;
        }}
        
        QPushButton:hover {{
            opacity: 0.9;
        }}
        
        QPushButton:pressed {{
            opacity: 0.7;
        }}
        
        /* Área de texto */
        QTextEdit {{
            border: 2px solid {DarkTheme.BORDER_LIGHT};
            border-radius: 6px;
            background-color: {DarkTheme.BACKGROUND_LIGHT};
            color: {DarkTheme.TEXT_PRIMARY};
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 11px;
            padding: 8px;
        }}
        
        /* Etiquetas */
        QLabel {{
            color: {DarkTheme.TEXT_PRIMARY};
            font-size: 12px;
        }}
        
        /* Barras de scroll */
        QScrollBar:vertical {{
            background-color: {DarkTheme.BACKGROUND_LIGHT};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {DarkTheme.BORDER_LIGHT};
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {DarkTheme.BUTTON_PRIMARY};
        }}
        
        /* Tabla */
        QTableWidget {{
            background-color: {DarkTheme.BACKGROUND_SECONDARY};
            alternate-background-color: {DarkTheme.BACKGROUND_LIGHT};
            color: {DarkTheme.TEXT_PRIMARY};
            gridline-color: {DarkTheme.BORDER_LIGHT};
            border: 2px solid {DarkTheme.BORDER_LIGHT};
            border-radius: 6px;
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background-color: {DarkTheme.BUTTON_PRIMARY};
            color: {DarkTheme.TEXT_PRIMARY};
        }}
        
        QHeaderView::section {{
            background-color: {DarkTheme.BACKGROUND_LIGHT};
            color: {DarkTheme.TEXT_PRIMARY};
            padding: 8px;
            border: 1px solid {DarkTheme.BORDER_LIGHT};
            font-weight: bold;
        }}
        
        /* Barra de estado */
        QStatusBar {{
            background-color: {DarkTheme.BACKGROUND_LIGHT};
            color: {DarkTheme.TEXT_SECONDARY};
            border-top: 1px solid {DarkTheme.BORDER_LIGHT};
        }}
        
        /* Splitter */
        QSplitter::handle {{
            background-color: {DarkTheme.BORDER_LIGHT};
        }}
        
        QSplitter::handle:horizontal {{
            width: 3px;
        }}
        
        QSplitter::handle:vertical {{
            height: 3px;
        }}
        
        /* Frames */
        QFrame {{
            border-radius: 8px;
        }}
        """
    
    @staticmethod
    def get_button_style(button_type="primary"):
        """Retorna estilos específicos para botones"""
        color_map = {
            "primary": DarkTheme.BUTTON_PRIMARY,
            "success": DarkTheme.BUTTON_SUCCESS,
            "warning": DarkTheme.BUTTON_WARNING,
            "danger": DarkTheme.BUTTON_DANGER,
            "info": DarkTheme.BUTTON_INFO
        }
        
        base_color = color_map.get(button_type, DarkTheme.BUTTON_PRIMARY)
        
        return f"""
        QPushButton {{
            background-color: {base_color};
            color: {DarkTheme.TEXT_PRIMARY};
        }}
        
        QPushButton:hover {{
            background-color: {DarkTheme.HOVER_ACCENT};
        }}
        
        QPushButton:pressed {{
            background-color: {DarkTheme.BORDER_DARK};
        }}
        """
    
    @staticmethod
    def get_keyboard_button_style(button_type="function"):
        """Estilos específicos para botones del teclado virtual con mejor contraste"""
        base_style = f"""
            QPushButton {{
                border: 2px solid transparent;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
                min-width: 51px;
                min-height: 34px;
                max-width: 77px;
                max-height: 43px;
                margin: 2px;
            }}
        """
        
        if button_type == "function":
            return base_style + f"""
            QPushButton {{
                background-color: {DarkTheme.BUTTON_INFO};
                color: {DarkTheme.TEXT_PRIMARY};
                border-color: #2980b9;
            }}
            
            QPushButton:hover {{
                background-color: #2980b9;
                border-color: {DarkTheme.BUTTON_PRIMARY};
            }}
            
            QPushButton:pressed {{
                background-color: #1f618d;
            }}
            """
        elif button_type == "clear":
            return base_style + f"""
            QPushButton {{
                background-color: {DarkTheme.BUTTON_DANGER};
                color: {DarkTheme.TEXT_PRIMARY};
                border-color: #c0392b;
                font-size: 11px;
            }}
            
            QPushButton:hover {{
                background-color: #c0392b;
                border-color: #e74c3c;
            }}
            
            QPushButton:pressed {{
                background-color: #a93226;
            }}
            """
        elif button_type == "operator":
            return base_style + f"""
            QPushButton {{
                background-color: {DarkTheme.BUTTON_WARNING};
                color: {DarkTheme.TEXT_PRIMARY};
                border-color: #d68910;
                font-size: 14px;
                font-weight: 900;
            }}
            
            QPushButton:hover {{
                background-color: #d68910;
                border-color: #f39c12;
            }}
            
            QPushButton:pressed {{
                background-color: #b7950b;
            }}
            """
        
        return base_style

class AnimationUtils:
    """
    Utilidades para animaciones suaves en la interfaz
    """
    
    @staticmethod
    def get_fade_duration():
        """Duración estándar para animaciones de fade"""
        return 250  # milliseconds
    
    @staticmethod
    def get_hover_duration():
        """Duración para efectos de hover"""
        return 150  # milliseconds
