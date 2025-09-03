# 🧮 Simulador Matemático Avanzado

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
- Python 3.8 o superior
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
├── config/
│   └── settings.json      # Configuración
├── core/
│   ├── differential_equations.py
│   ├── finite_differences.py
│   └── numerical_integration.py
├── gui/
│   ├── main_window.py
│   ├── advanced_tabs.py
│   ├── themes.py
│   ├── animations.py
│   └── credits.py
├── numerics/
│   ├── methods.py
│   └── advanced.py
├── utils/
│   ├── function_parser.py
│   └── validators.py
└── tests/
    └── test_main.py
```

## 🎓 Información Académica

**Materia**: Modelado y Simulación  
**Año**: 2025  
**Institución**: Universidad

### Equipo de Desarrollo
- Implementación de algoritmos numéricos
- Desarrollo de interfaz gráfica
- Testing y validación

## 📚 Referencias

- Burden & Faires: "Numerical Analysis"
- Press et al.: "Numerical Recipes"
- Documentación oficial de SciPy y NumPy

---
