"""
Información del Equipo y Créditos - Información del Equipo
Simulador Matemático Avanzado v3.0

Equipo TPO Modelado y Simulación - 2025
"""

class TeamInfo:
    """
    Clase estática con información del equipo
    """
    
    PROJECT_NAME = "Simulador Matemático Avanzado"
    VERSION = "3.0"
    YEAR = "2025"
    ORGANIZATION = "TPO Modelado y Simulación"
    
    TEAM_MEMBERS = [
        {
            "name": "[Nombre del Líder]",
            "role": "Líder del Proyecto",
            "email": "lider@universidad.edu"
        },
        {
            "name": "[Nombre del Desarrollador Backend]",
            "role": "Desarrollador Backend",
            "email": "backend@universidad.edu"
        },
        {
            "name": "[Nombre del Desarrollador Frontend]",
            "role": "Desarrollador Frontend",
            "email": "frontend@universidad.edu"
        },
        {
            "name": "[Nombre del Especialista]",
            "role": "Especialista en Matemáticas",
            "email": "matematicas@universidad.edu"
        },
        {
            "name": "[Nombre del Tester]",
            "role": "Tester y QA",
            "email": "testing@universidad.edu"
        }
    ]
    
    TECHNOLOGIES = {
        "language": "Python 3.8+",
        "gui": "PyQt6",
        "math": ["NumPy", "SciPy", "SymPy"],
        "visualization": "Matplotlib",
        "testing": ["pytest", "pytest-cov"]
    }
    
    CONTACT_INFO = {
        "email": "equipo.tpo@universidad.edu",
        "github": "https://github.com/equipo-tpo/simulador-matematico",
        "documentation": "https://simulador-matematico.readthedocs.io"
    }
    
    @staticmethod
    def get_banner() -> str:
        """Retorna el banner de información del equipo"""
        return f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                 {TeamInfo.PROJECT_NAME} v{TeamInfo.VERSION}                   ║
║                      {TeamInfo.ORGANIZATION}                      ║
║                               {TeamInfo.YEAR}                                 ║
╚══════════════════════════════════════════════════════════════════════════╝
        """
    
    @staticmethod
    def get_copyright() -> str:
        """Retorna el texto de copyright"""
        return f"© {TeamInfo.YEAR} {TeamInfo.ORGANIZATION}. Todos los derechos reservados."
