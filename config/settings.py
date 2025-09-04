"""
Configuración del sistema
Manejo de configuraciones de la aplicación
"""

import json
import os
from typing import Dict, Any


class Settings:
    """
    Clase para manejar configuraciones del sistema
    """

    def __init__(self):
        self.config_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config', 'settings.json'
        )

    def load_settings(self) -> Dict[str, Any]:
        """
        Carga configuraciones desde archivo JSON

        Returns:
            Diccionario con configuraciones
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.get_default_settings()
        except Exception:
            return self.get_default_settings()

    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Guarda configuraciones en archivo JSON

        Args:
            settings: Configuraciones a guardar

        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def get_default_settings(self) -> Dict[str, Any]:
        """
        Retorna configuraciones por defecto

        Returns:
            Diccionario con configuraciones por defecto
        """
        return {
            "theme": "dark",
            "language": "es",
            "precision": 6,
            "max_iterations": 1000,
            "plot_resolution": 100
        }

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Valida una configuración

        Args:
            config: Configuración a validar

        Returns:
            True si es válida, False en caso contrario
        """
        required_fields = ['theme', 'language', 'precision', 'max_iterations']

        # Verificar campos requeridos
        for field in required_fields:
            if field not in config:
                return False

        # Verificar tipos y rangos
        if not isinstance(config.get('precision', 0), int) or config['precision'] < 1:
            return False

        if not isinstance(config.get('max_iterations', 0), int) or config['max_iterations'] < 1:
            return False

        if config.get('theme', '') not in ['dark', 'light']:
            return False

        if config.get('language', '') not in ['es', 'en']:
            return False

        return True
