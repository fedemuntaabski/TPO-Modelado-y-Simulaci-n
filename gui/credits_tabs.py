"""
Información del Equipo y Créditos - Pestañas del Diálogo
Simulador Matemático Avanzado v3.0

Equipo TPO Modelado y Simulación - 2025
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class CreditsTabs:
    """
    Clase con métodos para crear las pestañas del diálogo de créditos
    """
    
    @staticmethod
    def create_team_tab() -> QWidget:
        """Crea la pestaña de información del equipo"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        team_info = QTextEdit()
        team_info.setReadOnly(True)
        team_info.setHtml("""
        <h2 style="color: #2c3e50; text-align: center;">Equipo de Desarrollo</h2>
        
        <h3 style="color: #3498db;">🎓 TPO Modelado y Simulación</h3>
        <p><strong>Proyecto:</strong> Simulador Matemático Avanzado</p>
        <p><strong>Versión:</strong> 3.0</p>
        <p><strong>Año:</strong> 2025</p>
        <p><strong>Institución:</strong> Universidad [Nombre de la Universidad]</p>
        
        <h3 style="color: #3498db;">👨‍💻 Desarrolladores</h3>
        <ul>
            <li><strong>Líder del Proyecto:</strong> [Nombre del Líder]</li>
            <li><strong>Desarrollador Backend:</strong> [Nombre del Desarrollador]</li>
            <li><strong>Desarrollador Frontend:</strong> [Nombre del Desarrollador]</li>
            <li><strong>Especialista en Matemáticas:</strong> [Nombre del Especialista]</li>
            <li><strong>Tester y QA:</strong> [Nombre del Tester]</li>
        </ul>
        
        <h3 style="color: #3498db;">📧 Contacto</h3>
        <p><strong>Email:</strong> equipo.tpo@universidad.edu</p>
        <p><strong>GitHub:</strong> https://github.com/equipo-tpo/simulador-matematico</p>
        
        <h3 style="color: #3498db;">📜 Licencia</h3>
        <p>Este proyecto está bajo la Licencia MIT</p>
        <p>© 2025 Equipo TPO Modelado y Simulación</p>
        """)
        
        layout.addWidget(team_info)
        widget.setLayout(layout)
        return widget
    
    @staticmethod
    def create_tech_tab() -> QWidget:
        """Crea la pestaña de tecnologías utilizadas"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        tech_info = QTextEdit()
        tech_info.setReadOnly(True)
        tech_info.setHtml("""
        <h2 style="color: #2c3e50; text-align: center;">Stack Tecnológico</h2>
        
        <h3 style="color: #3498db;">🐍 Lenguaje Principal</h3>
        <ul>
            <li><strong>Python 3.8+</strong> - Lenguaje de programación principal</li>
        </ul>
        
        <h3 style="color: #3498db;">🖥️ Interfaz Gráfica</h3>
        <ul>
            <li><strong>PyQt6</strong> - Framework moderno para interfaces gráficas</li>
            <li><strong>Matplotlib</strong> - Visualización de gráficos y plots</li>
        </ul>
        
        <h3 style="color: #3498db;">🔢 Bibliotecas Matemáticas</h3>
        <ul>
            <li><strong>NumPy</strong> - Operaciones numéricas eficientes</li>
            <li><strong>SciPy</strong> - Métodos numéricos avanzados</li>
            <li><strong>SymPy</strong> - Cálculo simbólico y parsing de funciones</li>
        </ul>
        
        <h3 style="color: #3498db;">🧪 Testing y Calidad</h3>
        <ul>
            <li><strong>pytest</strong> - Framework de testing</li>
            <li><strong>pytest-cov</strong> - Cobertura de código</li>
            <li><strong>black</strong> - Formateo de código</li>
            <li><strong>flake8</strong> - Linting</li>
            <li><strong>mypy</strong> - Verificación de tipos</li>
        </ul>
        
        <h3 style="color: #3498db;">📚 Documentación</h3>
        <ul>
            <li><strong>Sphinx</strong> - Generación de documentación</li>
            <li><strong>sphinx-rtd-theme</strong> - Tema Read the Docs</li>
        </ul>
        
        <h3 style="color: #3498db;">⚡ Optimización</h3>
        <ul>
            <li><strong>Vectorización NumPy</strong> - Operaciones eficientes en arrays</li>
            <li><strong>Threading</strong> - Cálculos en hilos separados</li>
            <li><strong>Caching</strong> - Cache de resultados frecuentes</li>
        </ul>
        """)
        
        layout.addWidget(tech_info)
        widget.setLayout(layout)
        return widget
    
    @staticmethod
    def create_features_tab() -> QWidget:
        """Crea la pestaña de características principales"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        features_info = QTextEdit()
        features_info.setReadOnly(True)
        features_info.setHtml("""
        <h2 style="color: #2c3e50; text-align: center;">Características Principales</h2>
        
        <h3 style="color: #3498db;">📈 Ecuaciones Diferenciales</h3>
        <ul>
            <li>Método de Euler</li>
            <li>Runge-Kutta de 2do orden (RK2)</li>
            <li>Runge-Kutta de 4to orden (RK4)</li>
            <li>Runge-Kutta-Fehlberg (RK45)</li>
        </ul>
        
        <h3 style="color: #3498db;">∫ Integración Numérica</h3>
        <ul>
            <li>Regla del Trapecio</li>
            <li>Regla de Simpson 1/3</li>
            <li>Regla de Simpson 3/8</li>
            <li>Cuadratura de Gauss</li>
            <li>Integración adaptativa</li>
        </ul>
        
        <h3 style="color: #3498db;">🔢 Diferencias Finitas</h3>
        <ul>
            <li>Diferencias hacia adelante</li>
            <li>Diferencias hacia atrás</li>
            <li>Diferencias centrales</li>
            <li>Derivadas de orden superior</li>
            <li>Extrapolación de Richardson</li>
        </ul>
        
        <h3 style="color: #3498db;">🎯 Búsqueda de Raíces</h3>
        <ul>
            <li>Método de Bisección</li>
            <li>Newton-Raphson</li>
            <li>Método de la Secante</li>
            <li>Punto Fijo</li>
        </ul>
        
        <h3 style="color: #3498db;">📊 Interpolación</h3>
        <ul>
            <li>Interpolación de Lagrange</li>
            <li>Interpolación de Newton</li>
            <li>Splines cúbicos</li>
            <li>Tabla de diferencias finitas</li>
        </ul>
        
        <h3 style="color: #3498db;">🎨 Interfaz y Usabilidad</h3>
        <ul>
            <li>Teclado virtual matemático</li>
            <li>Tema oscuro profesional</li>
            <li>Visualización interactiva</li>
            <li>Animaciones suaves</li>
            <li>Exportación de resultados</li>
        </ul>
        """)
        
        layout.addWidget(features_info)
        widget.setLayout(layout)
        return widget
    
    @staticmethod
    def create_thanks_tab() -> QWidget:
        """Crea la pestaña de agradecimientos"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        thanks_info = QTextEdit()
        thanks_info.setReadOnly(True)
        thanks_info.setHtml("""
        <h2 style="color: #2c3e50; text-align: center;">Agradecimientos</h2>
        
        <h3 style="color: #3498db;">🎓 Institución Educativa</h3>
        <p>Agradecemos a nuestra universidad por proporcionar el marco académico 
        y los recursos necesarios para el desarrollo de este proyecto.</p>
        
        <h3 style="color: #3498db;">👨‍🏫 Profesores y Mentores</h3>
        <p>Especial reconocimiento a nuestros profesores de la cátedra de 
        Modelado y Simulación por su guía, conocimiento y apoyo constante 
        durante todo el proceso de desarrollo.</p>
        
        <h3 style="color: #3498db;">🌟 Comunidad Open Source</h3>
        <p>Gratitud a la comunidad de desarrolladores de Python y especialmente 
        a los mantenedores de las bibliotecas utilizadas:</p>
        <ul>
            <li>NumPy y SciPy community</li>
            <li>Matplotlib developers</li>
            <li>PyQt6 team</li>
            <li>SymPy developers</li>
        </ul>
        
        <h3 style="color: #3498db;">📚 Referencias Académicas</h3>
        <p>Este proyecto se basa en métodos y algoritmos fundamentales de 
        análisis numérico desarrollados por matemáticos y científicos a lo 
        largo de la historia. Agradecemos a todos los académicos que han 
        contribuido al campo del análisis numérico.</p>
        
        <h3 style="color: #3498db;">🤝 Testers y Usuarios</h3>
        <p>Agradecemos a todos los que han probado versiones previas del 
        simulador y han proporcionado feedback valioso para mejorarlo.</p>
        
        <h3 style="color: #3498db;">💝 Dedicatoria</h3>
        <p style="font-style: italic; text-align: center; color: #7f8c8d;">
        "Dedicado a todos los estudiantes y profesionales que encuentran 
        en las matemáticas una herramienta poderosa para comprender y 
        transformar el mundo."
        </p>
        """)
        
        layout.addWidget(thanks_info)
        widget.setLayout(layout)
        return widget
