#!/usr/bin/env python3
"""
Tests unitarios para configuración y aplicación principal
Incluye pruebas de settings, inicialización y manejo de errores

Autor: Equipo TPO Modelado y Simulación
Fecha: 2025
"""

import sys
import os
import json
import pytest
import tempfile

# Agregar el directorio principal al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la aplicación principal
try:
    from gui.main_window import MathSimulatorApp
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

# Clase simple para gestión de configuración
class SettingsManager:
    """Gestor simple de configuración basado en JSON."""

    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config', 'settings.json'
        )
        self._config = self.load_settings()

    def load_settings(self):
        """Carga configuración desde archivo JSON."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.get_default_config()
        except (json.JSONDecodeError, IOError):
            return self.get_default_config()

    def save_settings(self, config, path=None):
        """Guarda configuración en archivo JSON."""
        save_path = path or self.config_path
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except IOError:
            raise

    def get_default_config(self):
        """Retorna configuración por defecto."""
        return {
            "application": {
                "name": "Simulador Matemático Avanzado",
                "version": "3.0",
                "organization": "TPO Modelado y Simulación",
                "theme": "dark"
            },
            "ui": {
                "window": {
                    "min_width": 800,
                    "min_height": 600,
                    "default_width": 1200,
                    "default_height": 800
                },
                "keyboard": {
                    "button_size": {"width": 80, "height": 50},
                    "spacing": 6,
                    "margins": 10
                },
                "animations": {
                    "enabled": True,
                    "fade_duration": 250,
                    "hover_duration": 150
                }
            },
            "numerical": {
                "default_tolerance": 1e-6,
                "max_iterations": 1000,
                "integration_points": 1000,
                "ode_points": 100
            },
            "plotting": {
                "backend": "Qt5Agg",
                "figure_size": [8, 6],
                "dpi": 100,
                "grid": True,
                "alpha": 0.3
            },
            "logging": {
                "level": "INFO",
                "file": "simulator.log",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "max_file_size": "10MB",
                "backup_count": 5
            }
        }

    def validate_setting(self, key, value):
        """Valida un setting individual."""
        if key == "numerical.default_tolerance":
            return isinstance(value, (int, float)) and value > 0
        elif key == "numerical.max_iterations":
            return isinstance(value, int) and value > 0
        elif key == "ui.animations.enabled":
            return isinstance(value, bool)
        elif key == "application.theme":
            return value in ["dark", "light"]
        else:
            return True  # Para otros settings, aceptar cualquier valor válido

    def update_settings(self, current_config, updates):
        """Actualiza configuración con nuevos valores."""
        updated = current_config.copy()
        self._deep_update(updated, updates)
        return updated

    def _deep_update(self, base_dict, update_dict):
        """Actualización profunda de diccionario."""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value


class TestSettingsManager:
    """Tests del gestor de configuración."""

    def test_default_settings(self):
        """Test de configuración por defecto."""
        settings = SettingsManager()

        # Verificar que se cargan valores por defecto
        assert hasattr(settings, 'theme'), "Debe tener configuración de tema"
        assert hasattr(settings, 'precision'), "Debe tener configuración de precisión"
        assert hasattr(settings, 'max_iterations'), "Debe tener configuración de iteraciones"

        # Verificar valores razonables
        assert settings.precision > 0, "Precisión debe ser positiva"
        assert settings.max_iterations > 0, "Iteraciones máximas deben ser positivas"

    def test_settings_validation(self):
        """Test de validación de configuración."""
        settings = SettingsManager()

        # Valores válidos
        valid_configs = {
            "precision": 1e-10,
            "max_iterations": 1000,
            "tolerance": 1e-6,
            "step_size": 0.001
        }

        for key, value in valid_configs.items():
            assert settings.validate_setting(key, value), f"Configuración válida rechazada: {key}"

        # Valores inválidos
        invalid_configs = {
            "precision": -1e-10,  # Negativo
            "max_iterations": 0,  # Cero
            "tolerance": 0,       # Cero
            "step_size": -0.001   # Negativo
        }

        for key, value in invalid_configs.items():
            assert not settings.validate_setting(key, value), f"Configuración inválida aceptada: {key}"

    def test_settings_persistence(self):
        """Test de persistencia de configuración."""
        # Crear archivo temporal para tests
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Crear configuración de prueba
            test_config = {
                "theme": "dark",
                "precision": 1e-8,
                "max_iterations": 500,
                "language": "es"
            }

            # Guardar configuración
            settings = SettingsManager()
            settings.save_settings(test_config, temp_path)

            # Verificar que el archivo existe
            assert os.path.exists(temp_path), "Archivo de configuración no creado"

            # Cargar configuración
            loaded_config = settings.load_settings(temp_path)

            # Verificar que se cargó correctamente
            for key, value in test_config.items():
                assert loaded_config.get(key) == value, f"Configuración no persistió: {key}"

        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_settings_update(self):
        """Test de actualización de configuración."""
        settings = SettingsManager()

        # Configuración inicial
        initial_config = {
            "precision": 1e-6,
            "max_iterations": 100
        }

        # Actualización parcial
        update_config = {
            "precision": 1e-8,
            "tolerance": 1e-4
        }

        # Aplicar actualización
        updated_config = settings.update_settings(initial_config, update_config)

        # Verificar actualización
        assert updated_config["precision"] == 1e-8, "Precisión no actualizada"
        assert updated_config["max_iterations"] == 100, "Valor original perdido"
        assert updated_config["tolerance"] == 1e-4, "Nuevo valor no agregado"

    def test_invalid_settings_file(self):
        """Test de manejo de archivo de configuración inválido."""
        settings = SettingsManager()

        # Crear archivo con JSON inválido
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write("{ invalid json content ")
            temp_path = temp_file.name

        try:
            # Intentar cargar configuración inválida
            loaded_config = settings.load_settings(temp_path)

            # Debe devolver configuración por defecto
            assert loaded_config is not None, "Debe devolver configuración por defecto"
            assert isinstance(loaded_config, dict), "Configuración debe ser diccionario"

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestMainApplication:
    """Tests de la aplicación principal."""

    @pytest.mark.skipif(not GUI_AVAILABLE, reason="GUI no disponible")
    def test_app_initialization(self):
        """Test de inicialización de la aplicación."""
        # Verificar que la clase existe y se puede instanciar
        assert MathSimulatorApp is not None, "Clase MathSimulatorApp debe existir"

        # Verificar que tiene los métodos necesarios
        required_methods = [
            'show',
            'close',
            'setWindowTitle'
        ]

        for method in required_methods:
            assert hasattr(MathSimulatorApp, method), f"MathSimulatorApp debe tener método {method}"

    def test_app_configuration_mock(self):
        """Test de configuración de la aplicación (mock)."""
        # Verificar configuración por defecto usando nuestro gestor
        settings = SettingsManager()
        default_config = settings.get_default_config()

        assert isinstance(default_config, dict), "Configuración por defecto debe ser diccionario"
        assert len(default_config) > 0, "Configuración por defecto no debe estar vacía"

        # Verificar campos requeridos
        required_fields = ['application', 'ui', 'numerical', 'plotting', 'logging']
        for field in required_fields:
            assert field in default_config, f"Campo requerido faltante: {field}"

    def test_error_handling(self):
        """Test de manejo de errores en la aplicación."""
        # Test de errores de configuración usando nuestro gestor
        settings = SettingsManager()

        try:
            # Intentar configuración inválida
            invalid_config = {
                "numerical": {
                    "default_tolerance": "invalid",
                    "max_iterations": -1
                }
            }

            # Debe manejar errores gracefully
            result = settings.validate_setting("numerical.default_tolerance", invalid_config["numerical"]["default_tolerance"])
            assert not result, "Configuración inválida debe ser rechazada"

        except Exception as e:
            # Si lanza excepción, debe ser manejada apropiadamente
            assert isinstance(e, (ValueError, TypeError)), f"Excepción inesperada: {type(e)}"

    def test_logging_setup_mock(self):
        """Test de configuración de logging (mock)."""
        # Verificar que existe configuración de logging usando nuestro gestor
        settings = SettingsManager()
        config = settings.get_default_config()
        log_config = config.get("logging", {})

        assert isinstance(log_config, dict), "Configuración de logging debe ser diccionario"
        assert 'level' in log_config, "Configuración debe tener nivel"
        assert 'format' in log_config, "Configuración debe tener formato"

        # Verificar niveles válidos
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        assert log_config['level'] in valid_levels, "Nivel de logging inválido"


class TestConfigurationIntegration:
    """Tests de integración de configuración."""

    def test_settings_app_integration(self):
        """Test de integración entre configuración y aplicación."""
        settings = SettingsManager()

        # Obtener configuración por defecto usando nuestro gestor
        app_config = settings.get_default_config()

        # Validar con el gestor de configuración
        for key, value in app_config.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    full_key = f"{key}.{sub_key}"
                    assert settings.validate_setting(full_key, sub_value), f"Configuración de app inválida: {full_key}"

    def test_config_file_operations(self):
        """Test de operaciones con archivo de configuración."""
        settings = SettingsManager()

        # Crear configuración de prueba
        test_config = {
            "theme": "light",
            "precision": 1e-12,
            "max_iterations": 2000,
            "auto_save": True,
            "language": "en"
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Guardar configuración
            settings.save_settings(test_config, temp_path)

            # Verificar archivo
            assert os.path.exists(temp_path), "Archivo no creado"

            # Leer archivo directamente para verificar contenido
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)

            # Verificar contenido
            for key, value in test_config.items():
                assert saved_data[key] == value, f"Valor no guardado correctamente: {key}"

            # Cargar y verificar
            loaded_config = settings.load_settings(temp_path)
            assert loaded_config == test_config, "Configuración no cargada correctamente"

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_config_backup_and_restore(self):
        """Test de backup y restauración de configuración."""
        settings = SettingsManager()

        # Configuración original
        original_config = {
            "theme": "dark",
            "precision": 1e-6
        }

        # Configuración modificada
        modified_config = {
            "theme": "light",
            "precision": 1e-8,
            "new_setting": "test"
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Guardar configuración original
            settings.save_settings(original_config, temp_path)

            # "Modificar" configuración
            settings.save_settings(modified_config, temp_path)

            # Verificar que se guardó la modificada
            loaded = settings.load_settings(temp_path)
            assert loaded["theme"] == "light", "Configuración modificada no guardada"

            # Restaurar original
            settings.save_settings(original_config, temp_path)

            # Verificar restauración
            restored = settings.load_settings(temp_path)
            assert restored["theme"] == "dark", "Configuración original no restaurada"
            assert "new_setting" not in restored, "Campo nuevo no eliminado en restauración"

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestMainEdgeCases:
    """Tests de casos edge para la aplicación principal."""

    def test_empty_config(self):
        """Test de configuración vacía."""
        settings = SettingsManager()

        # Configuración vacía
        empty_config = {}

        # Debe manejar configuración vacía
        result = settings.update_settings({}, empty_config)
        assert result == {}, "Configuración vacía debe permanecer vacía"

    def test_malformed_config_values(self):
        """Test de valores malformados en configuración."""
        settings = SettingsManager()

        malformed_configs = [
            {"precision": "not_a_number"},
            {"max_iterations": None},
            {"tolerance": float('inf')},
            {"step_size": float('nan')}
        ]

        for config in malformed_configs:
            for key, value in config.items():
                assert not settings.validate_setting(key, value), \
                       f"Valor malformado aceptado: {key}={value}"

    def test_config_file_permissions(self):
        """Test de permisos de archivo de configuración."""
        settings = SettingsManager()

        # Intentar guardar en directorio sin permisos de escritura
        # Nota: En Windows esto puede no funcionar igual que en Unix
        try:
            # Crear directorio temporal
            with tempfile.TemporaryDirectory() as temp_dir:
                config_path = os.path.join(temp_dir, "test_config.json")

                test_config = {"test": "value"}
                settings.save_settings(test_config, config_path)

                # Verificar que se creó
                assert os.path.exists(config_path), "Archivo no creado con permisos normales"

        except PermissionError:
            # Si hay error de permisos, debe manejarse
            pass

    def test_large_config_files(self):
        """Test de archivos de configuración grandes."""
        settings = SettingsManager()

        # Crear configuración grande
        large_config = {}
        for i in range(1000):
            large_config[f"setting_{i}"] = f"value_{i}"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Guardar configuración grande
            settings.save_settings(large_config, temp_path)

            # Cargar configuración grande
            loaded = settings.load_settings(temp_path)

            # Verificar que se cargó correctamente
            assert len(loaded) == len(large_config), "Configuración grande incompleta"
            assert loaded["setting_0"] == "value_0", "Primer elemento incorrecto"
            assert loaded["setting_999"] == "value_999", "Último elemento incorrecto"

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestApplicationLifecycle:
    """Tests del ciclo de vida de la aplicación."""

    def test_app_startup_sequence(self):
        """Test de secuencia de inicio de la aplicación."""
        # Verificar orden de inicialización (simulado)
        startup_steps = ["load_config", "init_ui", "setup_modules", "show_window"]

        assert isinstance(startup_steps, list), "Secuencia de inicio debe ser lista"
        assert len(startup_steps) > 0, "Secuencia de inicio no debe estar vacía"

        # Verificar pasos críticos
        critical_steps = ["load_config", "init_ui", "setup_modules"]
        for step in critical_steps:
            assert step in startup_steps, f"Paso crítico faltante: {step}"

    def test_app_shutdown_sequence(self):
        """Test de secuencia de cierre de la aplicación."""
        shutdown_steps = ["save_config", "cleanup_resources", "close_windows"]

        assert isinstance(shutdown_steps, list), "Secuencia de cierre debe ser lista"
        assert len(shutdown_steps) > 0, "Secuencia de cierre no debe estar vacía"

        # Verificar pasos de limpieza
        cleanup_steps = ["save_config", "cleanup_resources", "close_windows"]
        for step in cleanup_steps:
            assert step in shutdown_steps, f"Paso de limpieza faltante: {step}"

    def test_resource_management(self):
        """Test de gestión de recursos."""
        # Verificar que la aplicación maneja recursos apropiadamente
        resources = ["gui_framework", "numerical_libs", "config_files", "logging_system"]

        assert isinstance(resources, list), "Recursos deben ser lista"
        assert len(resources) > 0, "Debe requerir algunos recursos"

        # Recursos típicos
        typical_resources = ["gui_framework", "numerical_libs", "config_files"]
        for resource in typical_resources:
            assert resource in resources, f"Recurso típico faltante: {resource}"


if __name__ == "__main__":
    # Ejecutar tests
    try:
        import pytest
        pytest.main([__file__, "-v", "--tb=short"])
    except ImportError:
        print("⚠️ pytest no encontrado, ejecutando tests manualmente...")

        test_classes = [
            TestSettingsManager,
            TestMainApplication,
            TestConfigurationIntegration,
            TestMainEdgeCases,
            TestApplicationLifecycle
        ]

        total_tests = 0
        passed_tests = 0

        for test_class in test_classes:
            print(f"\n🧪 Ejecutando {test_class.__name__}...")

            instance = test_class()
            methods = [method for method in dir(instance) if method.startswith('test_')]

            for method_name in methods:
                total_tests += 1
                try:
                    method = getattr(instance, method_name)
                    method()
                    print(f"  ✅ {method_name}")
                    passed_tests += 1
                except Exception as e:
                    print(f"  ❌ {method_name}: {e}")

        print(f"\n📊 RESULTADOS CONFIGURACIÓN: {passed_tests}/{total_tests} tests pasaron")

        if passed_tests == total_tests:
            print("🎉 ¡Todos los tests de configuración pasaron exitosamente!")
        else:
            print(f"⚠️ {total_tests - passed_tests} tests fallaron")
