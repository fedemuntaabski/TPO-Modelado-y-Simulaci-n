# 🧮 Simulador Matemático Avanzado 

## 🚀 Características Principales

### ✅ **Funcionalidades Completas**
- 🎯 **Búsqueda de Raíces**: Bisección, Newton-Raphson, Punto Fijo
- ∫ **Integración Numérica**: Trapecio, Simpson 1/3, Simpson 3/8, Newton-Cotes completo
- 📊 **Newton-Cotes Avanzado**: 8 métodos con tabla de iteraciones detallada
- 📈 **EDOs**: Euler, Runge-Kutta (2º y 4º orden), Heun, RK45 adaptativo
- 🔢 **Diferencias Finitas**: Adelante, atrás, central, 5 puntos, Richardson
- 🎲 **Monte Carlo**: Simulación estocástica para integración 1D y 2D con análisis estadístico
- 📋 **Tabla de Iteraciones**: Vista paso a paso de todos los cálculos
- 🎨 **Interfaz Moderna**: CustomTkinter con diseño responsivo y oscuro
- 📊 **Visualización**: Gráficos interactivos con Matplotlib
- ✅ **Tests Completos**: Suite de pruebas unitarias para validación

## 📁 Estructura del Proyecto

```
├── main_simple.py                 # 🚀 Punto de entrada principal (recomendado)
├── README.md                      # 📖 Documentación del proyecto
├── requirements_minimal.txt       # 📦 Dependencias mínimas
├── config/
│   └── settings.py               # ⚙️ Configuración global
├── src/
│   ├── core/                     # 🧮 Algoritmos matemáticos
│   │   ├── newton_cotes.py       # ✨ Newton-Cotes completo
│   │   ├── function_parser.py    # 🔒 Parser seguro de funciones
│   │   ├── integration_validators.py # ✅ Validaciones de integración
│   │   ├── monte_carlo_engine.py # 🎲 Motor de simulación Monte Carlo
│   │   ├── root_finding.py       # 🎯 Búsqueda de raíces
│   │   ├── integration.py        # ∫ Integración básica
│   │   ├── ode_solver.py         # 📈 Resolución de EDOs
│   │   ├── ode_runge_kutta.py    # 📈 Métodos Runge-Kutta para EDOs
│   │   ├── finite_differences.py # 🔢 Diferencias finitas
│   │   └── __init__.py
│   └── ui/                       # 🎨 Interfaz gráfica
│       ├── main_app.py           # 🏠 Aplicación principal
│       ├── components/
│       │   ├── base_tab.py       # 🏗️ Componente base para pestañas
│       │   ├── constants.py      # 📊 Constantes de la aplicación
│       │   ├── error_handler.py  # ⚠️ Manejo de errores
│       │   ├── mixins.py         # 🔧 Mixins reutilizables
│       │   ├── tab_factory.py    # 🏭 Factory para creación de pestañas
│       │   ├── validation_mixins.py # ✅ Validaciones mixtas
│       │   └── __init__.py
│       └── tabs/                 # 📑 Pestañas específicas
│           ├── newton_cotes_tab.py    # ✨ Newton-Cotes UI
│           ├── roots_tab.py           # 🎯 Raíces UI
│           ├── integration_tab.py     # ∫ Integración UI
│           ├── ode_tab.py            # 📈 EDOs UI
│           ├── ode_tab_new.py       # 📈 EDOs UI (versión nueva)
│           ├── finite_diff_tab.py    # 🔢 Diferencias UI
│           ├── monte_carlo_tab.py    # 🎲 Monte Carlo UI
│           └── __init__.py
└── tests/                        # 🧪 Tests unitarios
    ├── test_newton_cotes.py     # ✨ Tests Newton-Cotes
    ├── test_root_finding.py     # 🎯 Tests raíces
    ├── test_ode_solver.py       # 📈 Tests EDOs
    ├── test_finite_differences.py # 🔢 Tests diferencias
    ├── test_monte_carlo.py      # 🎲 Tests Monte Carlo
    ├── check_types.py           # 🔍 Verificación de tipos
    ├── run_tests.py            # ▶️ Ejecutor de tests
    └── __init__.py
```

## 🛠️ Instalación y Ejecución

### 📋 Requisitos Previos
- **Python 3.8+**
- **pip** (viene con Python)

### 🚀 Instalación Rápida

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/fedemuntaabski/TPO-Modelado-y-Simulaci-n.git
   cd TPO-Modelado-y-Simulaci-n
   ```

2. **Ejecutar la aplicación** (automático):
   ```bash
   python main_simple.py
   ```

   > **Nota**: `main_simple.py` instala automáticamente todas las dependencias y ejecuta la aplicación. No requiere instalación manual de paquetes.

### 🔧 Instalación Manual (opcional)

```bash
# Instalar dependencias
pip install -r requirements_minimal.txt

# Ejecutar aplicación
python main_simple.py
```

## 📊 Funcionalidades Detalladas

### ✨ **Newton-Cotes Avanzado**
- **8 Métodos Completos**:
  - 📐 Rectángulo Simple y Compuesto
  - 📏 Trapecio Simple y Compuesto
  - 🎯 Simpson 1/3 Simple y Compuesto
  - 🎯 Simpson 3/8 Simple y Compuesto

- **Características Especiales**:
  - 📋 **Tabla de Iteraciones**: Muestra i, xi, f(xi) para cada paso
  - 🔢 **Coeficientes**: Visualización de coeficientes en Simpson
  - 📊 **Información Detallada**: Fórmulas, órdenes de error, estadísticas
  - 🎯 **Ejemplos Interactivos**: Biblioteca completa de casos de prueba
  - ✅ **Validaciones**: Verificación de restricciones (n par para Simpson 1/3, etc.)

### � **Monte Carlo Avanzado**
- **Integración 1D y 2D**: Simulación estocástica completa
- **Análisis Estadístico**: Desviación estándar, intervalos de confianza (95%)
- **Visualización Interactiva**: Puntos dentro/fuera del dominio
- **Análisis de Convergencia**: Gráficos de convergencia del método
- **Reproducibilidad**: Control de semillas para resultados consistentes
- **Validaciones Automáticas**: Verificación de parámetros y rangos

### ∫ **Integración Numérica**
- Métodos: Trapecio, Simpson 1/3, Simpson 3/8
- Integración simple y compuesta
- Comparación de precisión entre métodos

### 📈 **Resolución de EDOs**
- Métodos: Euler, Runge-Kutta 2º y 4º orden, Heun
- RK45 adaptativo para máxima precisión
- Visualización gráfica de soluciones

### 🔢 **Diferencias Finitas**
- Tipos: Adelante, atrás, central, 5 puntos
- Extrapolación de Richardson para mayor precisión
- Análisis de precisión y convergencia
- Cálculo de errores absolutos y relativos
- Derivadas de primer y segundo orden

### ✅ **Características Adicionales**
- **Instalación Automática**: `main_simple.py` instala dependencias automáticamente
- **Manejo de Errores**: Sistema robusto de validaciones y manejo de excepciones
- **Interfaz Responsiva**: Diseño moderno con tema oscuro
- **Parser Seguro de Funciones**: Evaluación segura de expresiones matemáticas
- **Suite de Tests Completa**: Cobertura de pruebas unitarias para todas las funcionalidades
- **Configuración Centralizada**: Sistema de configuración modular
- **Logging Integrado**: Sistema de logging para debugging y monitoreo


## 🔧 Tecnologías Utilizadas

- **🐍 Python 3.8+**: Lenguaje principal
- **🎨 CustomTkinter**: Interfaz gráfica moderna
- **🔢 NumPy**: Cálculos numéricos eficientes
- **📊 Matplotlib**: Visualización de gráficos
- **🔬 SciPy**: Funciones científicas avanzadas
- **🖼️ Pillow**: Manejo de imágenes

## 🎯 Principios de Diseño

### SOLID Principles
- **S**ingle Responsibility: Cada módulo tiene una responsabilidad clara
- **O**pen/Closed: Extensible sin modificar código existente
- **L**iskov Substitution: Subclases intercambiables
- **I**nterface Segregation: Interfaces específicas y cohesivas
- **D**ependency Inversion: Dependencias hacia abstracciones

### Otros Principios
- **DRY** (Don't Repeat Yourself): Código reutilizable
- **KISS** (Keep It Simple): Soluciones simples y claras
- **Separation of Concerns**: UI, lógica y datos separados
- **Fail-Fast**: Detección temprana de errores
### 📝 Agregar Nuevos Métodos
1. Implementar lógica en `src/core/`
2. Crear interfaz en `src/ui/tabs/`
3. Agregar tests en `tests/`
4. Actualizar documentación

## 🏗️ Arquitectura del Proyecto

### **Separación de Responsabilidades**
- **`src/core/`**: Lógica matemática pura, algoritmos numéricos
- **`src/ui/`**: Interfaz gráfica, componentes reutilizables
- **`tests/`**: Pruebas unitarias y de integración
- **`config/`**: Configuraciones centralizadas

### **Patrones de Diseño Implementados**
- **Factory Pattern**: Creación de pestañas (`TabFactory`)
- **Template Method**: Estructura base de pestañas (`BaseTab`)
- **Mixin Pattern**: Funcionalidades reutilizables (`InputValidationMixin`, `PlottingMixin`)
- **Strategy Pattern**: Diferentes algoritmos para el mismo problema

### **Principios SOLID Aplicados**
- ✅ **Single Responsibility**: Cada clase tiene una responsabilidad clara
- ✅ **Open/Closed**: Extensible sin modificar código existente
- ✅ **Liskov Substitution**: Subclases intercambiables
- ✅ **Interface Segregation**: Interfaces específicas y cohesivas
- ✅ **Dependency Inversion**: Dependencias hacia abstracciones

