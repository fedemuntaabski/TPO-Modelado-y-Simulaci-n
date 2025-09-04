# 🧮 Simulador Matemático Avanzado v3.0

Un simulador interactivo para métodos numéricos con interfaz gráfica moderna, desarrollado en Python con PyQt6.

## ✨ Características Principales

### 📊 Métodos Numéricos Implementados
- **Ecuaciones Diferenciales**: Runge-Kutta (2do y 4to orden), Euler, integración con SciPy
- **Búsqueda de Raíces**: Bisección, Newton-Raphson, Punto Fijo
- **Integración Numérica**: Regla del Trapecio, Simpson 1/3
- **Interpolación**: Método de Lagrange, diferencias finitas
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
- Tests de integración para componentes GUI
- Tests de validación y utilidades
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

### 4. Interpolación
1. Ir a la pestaña "📊 Interpolación"
2. Ingresar puntos (x, y) en la tabla
3. Especificar punto de evaluación

### 5. Derivadas Numéricas
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
│   └── settings.json      # Configuración
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
│   ├── initializer.py
│   ├── integration_tab.py
│   ├── ode_tab.py
│   ├── roots_tab.py
│   ├── tabs.py
│   └── themes.py
├── numerics/
│   ├── __init__.py
│   ├── advanced.py
│   ├── core_methods.py
│   ├── methods.py
│   ├── parser_utils.py
│   └── root_methods.py
├── tests/
│   ├── test_advanced_methods.py
│   ├── test_config.py
│   ├── test_finite_differences.py
│   ├── test_gui.py
│   ├── test_main.py
│   ├── test_numerical_methods.py
│   └── test_utils.py
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
