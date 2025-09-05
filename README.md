# 🧮 Simulador Matemático Avanzado v3.0

Un simulador interactivo para métodos numéricos con interfaz gráfica moderna, desarrollado en Python con PyQt6. Incluye métodos especializados de Newton-Cotes para integración numérica.

## ✨ Características Principales

### 📊 Métodos Numéricos Implementados
- **Ecuaciones Diferenciales**: Runge-Kutta (2do y 4to orden), Euler, integración con SciPy
- **Búsqueda de Raíces**: Bisección, Newton-Raphson, Punto Fijo
- **Integración Numérica**: Newton-Cotes (Rectángulo, Trapecio, Simpson 1/3, Simpson 3/8)
- **Diferencias Finitas**: Derivadas e interpolación numérica
- **Interpolación**: Método de Lagrange
- **Derivadas Numéricas**: Diferencias finitas centrales, extrapolación de Richardson

### 🎨 Interfaz Gráfica
- Tema oscuro profesional
- Teclado virtual para funciones matemáticas
- Visualización interactiva con matplotlib
- Pestañas organizadas por método
- Animaciones y efectos visuales

### 🏗️ Arquitectura Modular
- `core/`: Algoritmos numéricos fundamentales
- `gui/`: Componentes de interfaz gráfica
- `numerics/`: Implementaciones de métodos
- `utils/`: Utilidades y validaciones
- `tests/`: Suite de pruebas

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.13 o superior
- Sistema operativo: Windows, macOS o Linux

### Instalación Automática
```bash
python main.py
```
El programa instala automáticamente todas las dependencias necesarias.

### Instalación Manual
```bash
pip install -r requirements.txt
```

### Ejecución
```bash
python main.py
```

## 🧪 Testing

### Ejecutar Tests
```bash
python -m pytest tests/
```

### Ejecutar Tests con Reporte
```bash
python test_runner.py
```

### Cobertura de Tests
- Tests unitarios para métodos numéricos
- Tests de ecuaciones diferenciales
- Tests de diferencias finitas
- Tests de integración numérica
- Tests de validadores
- Reporte JSON generado automáticamente

## 📖 Guía de Uso

### 1. Ecuaciones Diferenciales
1. Ir a la pestaña "📈 Ecuaciones Diferenciales"
2. Ingresar la función `f(t,y)` (ej: `t + y`)
3. Configurar condiciones iniciales y parámetros
4. Seleccionar método y ejecutar

### 2. Búsqueda de Raíces
1. Ir a la pestaña "🎯 Búsqueda de Raíces"
2. Ingresar la función `f(x)` (ej: `x**2 - 4`)
3. Configurar intervalo o punto inicial
4. Seleccionar método y ejecutar

### 3. Integración Numérica
1. Ir a la pestaña "∫ Integración"
2. Ingresar la función `f(x)`
3. Definir límites de integración
4. Configurar número de subdivisiones

### 4. Newton-Cotes
1. Ir a la pestaña "📊 Newton-Cotes"
2. Ingresar la función `f(x)`
3. Definir límites de integración `a` y `b`
4. Configurar número de subdivisiones `n`
5. Seleccionar método: Rectángulo, Trapecio, Simpson 1/3, Simpson 3/8 (simple o compuesto)

### 5. Diferencias Finitas
1. Ir a la pestaña "� Diferencias Finitas"
2. Ingresar la función `f(x)`
3. Configurar parámetros según el análisis requerido

### 6. Interpolación
1. Ir a la pestaña "📊 Interpolación"
2. Ingresar puntos (x, y) en la tabla
3. Especificar punto de evaluación

### 7. Derivadas Numéricas
1. Ir a la pestaña "🔢 Derivadas"
2. Ingresar la función `f(x)`
3. Configurar punto y paso `h`
4. Seleccionar orden de derivada

## 🛠️ Tecnologías Utilizadas

- **PyQt6**: Interfaz gráfica moderna
- **NumPy**: Computación numérica eficiente
- **SciPy**: Algoritmos científicos avanzados
- **Matplotlib**: Visualización de datos
- **SymPy**: Matemática simbólica

## 📁 Estructura del Proyecto

```
TPO-Modelado-y-Simulaci-n/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── README.md              # Esta documentación
├── simulator.log          # Log de ejecución
├── test_report.json       # Reporte de tests
├── test_runner.py         # Ejecutor de tests
├── config/
│   ├── settings.json      # Configuración
│   └── settings.py        # Configuración adicional
├── core/
│   ├── __init__.py
│   ├── differential_equations.py
│   ├── finite_differences.py
│   └── numerical_integration.py
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── advanced_tabs.py
│   ├── animations.py
│   ├── app_launcher.py
│   ├── components.py
│   ├── credits.py
│   ├── credits_dialog.py
│   ├── credits_tabs.py
│   ├── derivatives_tab.py
│   ├── finite_differences_analysis.py
│   ├── finite_differences_derivatives.py
│   ├── finite_differences_interpolation.py
│   ├── finite_differences_tab.py
│   ├── initializer.py
│   ├── integration_tab.py
│   ├── interpolation_logic.py
│   ├── interpolation_tab.py
│   ├── interpolation_ui.py
│   ├── main_window.py
│   ├── newton_cotes_tab.py
│   ├── ode_tab.py
│   ├── roots_tab.py
│   ├── roots_tab_methods.py
│   ├── roots_tab_plotting.py
│   ├── roots_tab_plotting_bisection.py
│   ├── roots_tab_plotting_helpers.py
│   ├── roots_tab_plotting_iterative.py
│   ├── roots_tab_ui.py
│   ├── tabs.py
│   ├── team_info.py
│   └── themes.py
├── numerics/
│   ├── __init__.py
│   ├── advanced_numerical_methods.py
│   ├── core_methods.py
│   ├── error_analysis.py
│   ├── interpolation_methods.py
│   ├── methods.py
│   ├── parser_utils.py
│   ├── root_acceleration_methods.py
│   ├── root_basic_methods.py
│   ├── root_interpolation_methods.py
│   └── root_methods.py
├── tests/
│   ├── test_differential_equations.py
│   ├── test_finite_differences.py
│   ├── test_numerical_integration.py
│   └── test_validators.py
└── utils/
    ├── __init__.py
    ├── function_parser.py
    └── validators.py
```

## 🎓 Información Académica

**Materia**: Modelado y Simulación  
**Año**: 2025  
**Institución**: Universidad  
**Repositorio**: TPO-Modelado-y-Simulaci-n

### Equipo de Desarrollo
- Implementación de algoritmos numéricos
- Desarrollo de interfaz gráfica
- Testing y validación

## 📚 Referencias

- Burden & Faires: "Numerical Analysis"
- Press et al.: "Numerical Recipes"
- Documentación oficial de SciPy y NumPy

---
