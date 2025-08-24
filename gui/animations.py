"""
Utilidades para animaciones y efectos visuales
Proporciona animaciones suaves para mejorar la experiencia de usuario
"""

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, pyqtSignal, QTimer
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget
from PyQt6.QtGui import QColor
import time

class FadeAnimation:
    """
    Maneja animaciones de fade in/out para widgets
    """
    
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 300):
        """
        Aplica efecto de fade in a un widget
        
        Args:
            widget: Widget a animar
            duration: Duración en milliseconds
        """
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        animation.start()
        return animation
    
    @staticmethod
    def fade_out(widget: QWidget, duration: int = 300):
        """
        Aplica efecto de fade out a un widget
        
        Args:
            widget: Widget a animar
            duration: Duración en milliseconds
        """
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        animation.start()
        return animation

class ButtonHoverEffect:
    """
    Efectos de hover para botones
    """
    
    def __init__(self, button):
        self.button = button
        self.original_style = button.styleSheet()
        self.setup_events()
    
    def setup_events(self):
        """Configura los eventos de hover"""
        self.button.enterEvent = self.on_enter
        self.button.leaveEvent = self.on_leave
    
    def on_enter(self, event):
        """Efecto al pasar el mouse por encima"""
        from gui.themes import DarkTheme
        
        # Crear efecto de brillo
        current_style = self.button.styleSheet()
        hover_style = current_style + f"""
        QPushButton {{
            border: 2px solid {DarkTheme.BUTTON_PRIMARY};
            transform: scale(1.02);
        }}
        """
        self.button.setStyleSheet(hover_style)
    
    def on_leave(self, event):
        """Efecto al quitar el mouse"""
        # Restaurar estilo original
        self.button.setStyleSheet(self.original_style)

class ProgressIndicator:
    """
    Indicador de progreso animado para operaciones largas
    """
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.timer = QTimer()
        self.dots = 0
        self.base_text = ""
        
    def start(self, text: str = "Calculando"):
        """
        Inicia la animación de progreso
        
        Args:
            text: Texto base a mostrar
        """
        self.base_text = text
        self.dots = 0
        self.timer.timeout.connect(self.update_text)
        self.timer.start(500)  # Actualizar cada 500ms
    
    def stop(self):
        """Detiene la animación de progreso"""
        self.timer.stop()
        if hasattr(self.parent, 'statusBar'):
            self.parent.statusBar().showMessage("Listo")
    
    def update_text(self):
        """Actualiza el texto con puntos animados"""
        self.dots = (self.dots + 1) % 4
        animated_text = self.base_text + "." * self.dots
        
        if hasattr(self.parent, 'statusBar'):
            self.parent.statusBar().showMessage(animated_text)

class SlideAnimation:
    """
    Animaciones de deslizamiento para transiciones suaves
    """
    
    @staticmethod
    def slide_in_from_right(widget: QWidget, duration: int = 400):
        """
        Desliza un widget desde la derecha
        
        Args:
            widget: Widget a animar
            duration: Duración en milliseconds
        """
        # Obtener posición final
        final_pos = widget.pos()
        
        # Posición inicial (fuera de la pantalla a la derecha)
        start_pos = final_pos
        start_pos.setX(final_pos.x() + widget.width())
        
        # Configurar animación
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(final_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        widget.move(start_pos)
        animation.start()
        return animation
    
    @staticmethod
    def slide_in_from_left(widget: QWidget, duration: int = 400):
        """
        Desliza un widget desde la izquierda
        
        Args:
            widget: Widget a animar
            duration: Duración en milliseconds
        """
        # Obtener posición final
        final_pos = widget.pos()
        
        # Posición inicial (fuera de la pantalla a la izquierda)
        start_pos = final_pos
        start_pos.setX(final_pos.x() - widget.width())
        
        # Configurar animación
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(final_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        widget.move(start_pos)
        animation.start()
        return animation

class PlotAnimation:
    """
    Animaciones para gráficos y visualizaciones
    """
    
    @staticmethod
    def animate_plot_update(plot_widget, update_function, duration: int = 1000):
        """
        Anima la actualización de un gráfico
        
        Args:
            plot_widget: Widget del gráfico
            update_function: Función que actualiza el gráfico
            duration: Duración de la animación
        """
        # Implementar animación progresiva del gráfico
        steps = 20
        step_duration = duration // steps
        
        timer = QTimer()
        current_step = [0]  # Usar lista para poder modificar en closure
        
        def update_step():
            if current_step[0] < steps:
                # Calcular progreso (0.0 a 1.0)
                progress = current_step[0] / steps
                
                # Llamar función de actualización con progreso
                update_function(progress)
                
                current_step[0] += 1
            else:
                timer.stop()
                # Actualización final
                update_function(1.0)
        
        timer.timeout.connect(update_step)
        timer.start(step_duration)
        
        return timer

class StatusAnimation:
    """
    Animaciones para mensajes de estado
    """
    
    @staticmethod
    def flash_success(status_bar, message: str, duration: int = 3000):
        """
        Muestra un mensaje de éxito con efecto flash
        
        Args:
            status_bar: Barra de estado
            message: Mensaje a mostrar
            duration: Duración del mensaje
        """
        # Cambiar estilo temporalmente
        original_style = status_bar.styleSheet()
        success_style = original_style + """
        QStatusBar {
            background-color: #27ae60;
            color: white;
            font-weight: bold;
        }
        """
        
        status_bar.setStyleSheet(success_style)
        status_bar.showMessage(f"✅ {message}")
        
        # Restaurar estilo original después del tiempo especificado
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: status_bar.setStyleSheet(original_style))
        timer.timeout.connect(lambda: status_bar.showMessage("Listo"))
        timer.start(duration)
        
        return timer
    
    @staticmethod
    def flash_error(status_bar, message: str, duration: int = 4000):
        """
        Muestra un mensaje de error con efecto flash
        
        Args:
            status_bar: Barra de estado
            message: Mensaje a mostrar
            duration: Duración del mensaje
        """
        # Cambiar estilo temporalmente
        original_style = status_bar.styleSheet()
        error_style = original_style + """
        QStatusBar {
            background-color: #e74c3c;
            color: white;
            font-weight: bold;
        }
        """
        
        status_bar.setStyleSheet(error_style)
        status_bar.showMessage(f"❌ {message}")
        
        # Restaurar estilo original después del tiempo especificado
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: status_bar.setStyleSheet(original_style))
        timer.timeout.connect(lambda: status_bar.showMessage("Listo"))
        timer.start(duration)
        
        return timer

class LoadingSpinner:
    """
    Spinner de carga animado
    """
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.timer = QTimer()
        self.angle = 0
        
    def start(self):
        """Inicia la animación del spinner"""
        self.timer.timeout.connect(self.rotate)
        self.timer.start(100)  # Actualizar cada 100ms
        
    def stop(self):
        """Detiene la animación del spinner"""
        self.timer.stop()
        
    def rotate(self):
        """Rota el spinner"""
        self.angle = (self.angle + 30) % 360
        # Aquí se implementaría la rotación visual del spinner
        # (requiere implementación específica según el widget)
