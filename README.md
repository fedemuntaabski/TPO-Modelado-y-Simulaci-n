# 🎨 Simulador Matemático Avanzado v2.0

## Versión Mejorada con Interfaz Moderna

Sistema integrado para resolución de métodos numéricos con interfaz gráfica completamente renovada y nuevas funcionalidades avanzadas.

## 🆕 NOVEDADES DE LA VERSIÓN 2.0

### 🎨 **Mejoras Visuales Principales**
- ✅ **Tema Oscuro Moderno**: Fondo gris profesional con excelente contraste
- ✅ **Título Reformateado**: "SIMULADOR MATEMÁTICO AVANZADO" con mejor espaciado
- ✅ **Teclado Virtual Simplificado**: Solo funciones matemáticas esenciales
- ✅ **Paleta de Colores Consistente**: Diseño profesional y moderno

### 🔄 **Nueva Pestaña de Comparación**
- ✅ **Comparación de Métodos de Raíces**: Bisección vs Newton-Raphson vs Punto Fijo
- ✅ **Análisis de Convergencia**: Gráficos comparativos lado a lado
- ✅ **Métricas Cuantitativas**: Iteraciones, precisión y velocidad
- ✅ **Aceleración de Aitken**: Comparación con y sin aceleración

### ✨ **Animaciones y Efectos**
- ✅ **Efectos de Hover**: Botones con respuesta visual suave
- ✅ **Indicadores de Progreso**: Animaciones durante cálculos largos
- ✅ **Mensajes de Estado**: Notificaciones animadas de éxito/error
- ✅ **Transiciones Suaves**: Cambios de estado fluidos

### 🔧 **Mejoras de Usabilidad**
- ✅ **Teclado Optimizado**: Sin números ni variables, solo funciones
- ✅ **Mejor Contraste**: Texto claro sobre fondo oscuro
- ✅ **Interfaz Intuitiva**: Navegación simplificada
- ✅ **Retroalimentación Visual**: Estados claros en tiempo real

## 📊 COMPARACIÓN DE VERSIONES

| Característica | Versión 1.0 | Versión 2.0 |
|----------------|--------------|--------------|
| **Tema Visual** | Fondo blanco básico | Tema oscuro profesional |
| **Teclado Virtual** | 26 botones (números + funciones) | 16 botones (solo funciones) |
| **Título** | Texto comprimido | Espaciado elegante |
| **Comparación de Métodos** | ❌ No disponible | ✅ Pestaña dedicada |
| **Animaciones** | ❌ Estático | ✅ Efectos suaves |
| **Indicadores de Progreso** | ❌ Sin feedback | ✅ Animaciones de progreso |
| **Contraste** | Medio | Alto (optimizado) |
| **Referencias Académicas** | Incluidas en UI | Eliminadas (solo en docs) |

## 🚀 EJECUCIÓN RÁPIDA

### Versión Mejorada (Recomendada)
```bash
python main_v2.py
```

### Versión Original (Compatibilidad)
```bash
python main.py
```

## 🎯 Características Principales

### Métodos Numéricos Implementados

#### 📈 Ecuaciones Diferenciales Ordinarias
- **Runge-Kutta de 4to orden** (implementación propia)
- **Runge-Kutta usando SciPy** (solve_ivp)
- Soporte para ecuaciones de la forma: `dy/dt = f(t, y)`
- Visualización gráfica de soluciones

#### 🎯 Búsqueda de Raíces
- **Método de Bisección** con análisis de convergencia
- **Newton-Raphson** con cálculo automático de derivadas
- **Punto Fijo** para ecuaciones de la forma `x = g(x)`
- Visualización de convergencia paso a paso

#### ∫ Integración Numérica
- **Reglas de Newton-Cotes** (Simpson 1/3)
- Visualización del área bajo la curva
- Análisis de precisión

#### 📊 Interpolación
- **Interpolación de Lagrange** con múltiples puntos
- **Tabla de diferencias finitas**
- Visualización de polinomios interpoladores

#### 🔢 Derivadas Numéricas
- **Diferencias finitas centrales** (1ra, 2da, 3ra y 4ta derivada)
- **Análisis de convergencia** con diferentes pasos h
- **Extrapolación de Richardson** para mayor precisión
- Comparación con derivadas exactas

#### ⚡ Métodos Avanzados
- **Aceleración de Aitken** para mejorar convergencia
- **Cuadratura adaptativa** con control de error
- **Análisis de errores** (absoluto y relativo)

## 🖥️ Interfaz Gráfica

### Características de la GUI
- **Teclado virtual matemático** para ingreso de funciones
- **Pestañas organizadas** por tipo de método
- **Visualización interactiva** con matplotlib
- **Diseño moderno** con PyQt6
- **Créditos e información del equipo**

### Componentes Principales
- 🔢 **Teclado Virtual**: Botones para funciones matemáticas comunes
- 📊 **Área de Gráficos**: Visualización en tiempo real de resultados
- ⚙️ **Paneles de Control**: Configuración de parámetros por método
- 📝 **Área de Resultados**: Salida detallada de cálculos

## 🚀 Instalación y Ejecución

### Requisitos del Sistema
- Python 3.8 o superior
- Windows, macOS o Linux

### Instalación Automática

El programa incluye **instalación automática de dependencias**. Simplemente ejecute:

```bash
python main.py
```

### Instalación Manual

Si prefiere instalar las dependencias manualmente:

```bash
pip install -r requirements.txt
```

**Dependencias incluidas:**
- PyQt6 >= 6.5.0
- NumPy >= 1.24.0
- SciPy >= 1.10.0
- Matplotlib >= 3.7.0
- SymPy >= 1.12

### Verificación de Instalación

Ejecute las pruebas para verificar que todo funciona correctamente:

```bash
python test_simulator.py
```

## 📁 Estructura del Proyecto

```
TPO-Modelado-y-Simulación/
├── main.py                    # Archivo principal de ejecución
├── requirements.txt           # Dependencias del proyecto
├── test_simulator.py         # Pruebas de verificación
├── README.md                 # Documentación principal
├── numerics/                 # Módulos de métodos numéricos
│   ├── __init__.py
│   ├── methods.py           # Métodos numéricos principales
│   └── advanced.py          # Métodos avanzados e interpolación
└── gui/                     # Módulos de interfaz gráfica
    ├── __init__.py
    ├── main_window.py       # Ventana principal y pestañas básicas
    └── advanced_tabs.py     # Pestañas avanzadas
```

## 💡 Guía de Uso

### 1. Iniciar la Aplicación
```bash
cd TPO-Modelado-y-Simulación
python main.py
```

### 2. Usar el Teclado Virtual
- Haga clic en cualquier campo de entrada de función
- Use los botones del teclado virtual para construir expresiones matemáticas
- Funciones disponibles: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, etc.

### 3. Resolver una Ecuación Diferencial
1. Vaya a la pestaña "📈 Ecuaciones Diferenciales"
2. Ingrese `f(t, y)` (ej: `t + y`, `-y + sin(t)`)
3. Configure condiciones iniciales: `t₀`, `y₀`, `tf`
4. Seleccione el método (Runge-Kutta propio o SciPy)
5. Haga clic en "Resolver EDO"

### 4. Encontrar Raíces
1. Vaya a la pestaña "🎯 Búsqueda de Raíces"
2. Ingrese la función `f(x)` (ej: `x**2 - 4`)
3. Seleccione el método (Bisección, Newton-Raphson, Punto Fijo)
4. Configure parámetros según el método
5. Haga clic en "Encontrar Raíz"

### 5. Calcular Integrales
1. Vaya a la pestaña "∫ Integración"
2. Ingrese la función `f(x)`
3. Configure límites de integración `a` y `b`
4. Ajuste el número de subdivisiones
5. Haga clic en "Calcular Integral"

### 6. Interpolación de Lagrange
1. Vaya a la pestaña "📊 Interpolación"
2. Ingrese puntos en la tabla (x, y)
3. Configure el punto de evaluación
4. Haga clic en "Interpolar con Lagrange"

### 7. Derivadas Numéricas
1. Vaya a la pestaña "🔢 Derivadas"
2. Ingrese la función `f(x)`
3. Configure punto de evaluación y paso `h`
4. Seleccione orden de derivada (1-4)
5. Use "Análisis de Convergencia" para estudiar precisión

## 🔧 Elecciones Tecnológicas

### GUI: PyQt6
**Razones de elección:**
- ✅ **Modernidad**: Widgets actualizados y soporte para Python 3.8+
- ✅ **Riqueza funcional**: Amplia gama de componentes avanzados
- ✅ **Rendimiento**: Excelente para aplicaciones matemáticas
- ✅ **Soporte profesional**: Documentación extensa y comunidad activa

### Cálculos: SciPy + NumPy
**Ventajas:**
- ✅ **Precisión**: Algoritmos optimizados y validados
- ✅ **Eficiencia**: Implementaciones en C/Fortran
- ✅ **Compatibilidad**: Estándar en computación científica

### Arquitectura Modular
- 📦 **Separación clara**: GUI independiente de lógica matemática
- 🔄 **Reutilización**: Módulos pueden usarse independientemente
- 🛠️ **Mantenibilidad**: Código organizado y documentado

## 📊 Ejemplos de Uso

### Ecuación Diferencial: Crecimiento Poblacional
```
Función: 0.1*y*(1 - y/100)
Condiciones: t₀=0, y₀=5, tf=50
Resultado: Curva logística de crecimiento
```

### Raíz de Función Trigonométrica
```
Función: sin(x) - 0.5
Método: Bisección con intervalo [0, π]
Resultado: x ≈ 0.5236 (π/6)
```

### Integral Definida
```
Función: x**2 * exp(-x)
Límites: [0, 5]
Resultado: Integral ≈ 2.0000
```

## 🎓 Créditos Académicos

**Materia:** Modelado y Simulación  
**Año:** 2025  
**Institución:** [Nombre de la Universidad]  

### Equipo de Desarrollo
- **Análisis numérico:** Implementación de algoritmos matemáticos
- **Desarrollo GUI:** Interfaz gráfica moderna y funcional
- **Testing y validación:** Pruebas de precisión y rendimiento

## 📝 Notas Técnicas

### Precisión Numérica
- **Tolerancias por defecto:** 1e-6 para métodos iterativos
- **Pasos adaptativos:** Configurables para análisis de convergencia
- **Validación:** Comparación con soluciones analíticas cuando es posible

### Rendimiento
- **Optimización:** Uso de NumPy para operaciones vectoriales
- **Memoria:** Gestión eficiente para datasets grandes
- **Responsividad:** GUI no bloqueante durante cálculos

### Extensibilidad
- **Nuevos métodos:** Fácil adición de algoritmos
- **Personalización:** Parámetros configurables
- **Exportación:** Resultados guardables (futuras versiones)

## 🔍 Resolución de Problemas

### Error de Dependencias
Si aparecen errores de importación:
```bash
pip install --upgrade PyQt6 numpy scipy matplotlib sympy
```

### Error de Display (Linux)
Para sistemas sin display gráfico:
```bash
export QT_QPA_PLATFORM=offscreen
```

### Problemas de Convergencia
- Ajuste la tolerancia para métodos iterativos
- Verifique las condiciones iniciales
- Use el análisis de convergencia para diagnosticar problemas

## 📚 Referencias y Algoritmos

### Bibliografía Numérica
1. **Burden & Faires** - "Numerical Analysis"
2. **Press et al.** - "Numerical Recipes"
3. **Quarteroni et al.** - "Scientific Computing with MATLAB and Octave"

### Implementaciones de Referencia
- SciPy documentation: https://docs.scipy.org/
- NumPy user guide: https://numpy.org/doc/
- PyQt6 documentation: https://doc.qt.io/qtforpython/

---

## 🚀 ¡Comenzar Ahora!

```bash
git clone [url-del-repositorio]
cd TPO-Modelado-y-Simulación
python main.py
```

**¡El simulador se encargará del resto!** 🎉