# Prompt para Proyecto de Simulador Matemático Avanzado

## 📋 OBJETIVOS DEL PROYECTO

### Objetivo Principal
Desarrollar un simulador matemático avanzado en Python con interfaz gráfica intuitiva que permita realizar cálculos complejos de métodos numéricos de manera eficiente y visualmente atractiva.

### Objetivos Específicos
1. **Funcionalidad Matemática**: Implementar módulos para ecuaciones diferenciales ordinarias, integración numérica y diferenciación numérica
2. **Interfaz de Usuario**: Crear una GUI moderna, responsiva y fácil de usar
3. **Eficiencia**: Garantizar rendimiento óptimo en cálculos complejos
4. **Usabilidad**: Proporcionar herramientas intuitivas para entrada de funciones matemáticas
5. **Documentación**: Incluir identificación del equipo y créditos apropiados

---

## 🛠️ REQUERIMIENTOS TÉCNICOS

### Stack Tecnológico Principal
- **Lenguaje**: Python 3.8+
- **GUI Framework**: Tkinter (nativo) o PyQt5/6 para interfaces avanzadas
- **Bibliotecas Matemáticas**:
  - `numpy` - Operaciones numéricas eficientes
  - `scipy` - Métodos numéricos avanzados
  - `matplotlib` - Visualización de gráficos
  - `sympy` - Cálculo simbólico y parsing de funciones
- **Bibliotecas Adicionales**:
  - `pandas` - Manejo de datos (opcional)
  - `numba` - Optimización de rendimiento (opcional)

### Arquitectura del Sistema
```
proyecto/
├── main.py                 # Punto de entrada principal
├── gui/
│   ├── __init__.py
│   ├── main_window.py      # Ventana principal
│   ├── calculator_widget.py # Teclado matemático
│   └── results_display.py  # Visualización de resultados
├── core/
│   ├── __init__.py
│   ├── differential_equations.py  # Runge-Kutta
│   ├── numerical_integration.py   # Newton-Cotes
│   └── finite_differences.py      # Derivación numérica
├── utils/
│   ├── __init__.py
│   ├── function_parser.py  # Parser de funciones matemáticas
│   └── validators.py       # Validaciones de entrada
├── tests/
│   └── [archivos de testing]
└── requirements.txt
```

### Módulos Matemáticos Requeridos

#### 1. Ecuaciones Diferenciales Ordinarias (EDO)
- **Método de Euler**
- **Runge-Kutta de 2do orden (RK2)**
- **Runge-Kutta de 4to orden (RK4)**
- **Runge-Kutta-Fehlberg (RK45)** para control de error

#### 2. Integración Numérica
- **Regla del Trapecio**
- **Regla de Simpson 1/3**
- **Regla de Simpson 3/8**
- **Cuadratura de Gauss** (opcional avanzado)

#### 3. Diferencias Finitas
- **Diferencias hacia adelante**
- **Diferencias hacia atrás**
- **Diferencias centrales**
- **Derivadas de orden superior**

### Especificaciones de Interfaz
- **Teclado Virtual**: Botones para funciones matemáticas comunes (sin, cos, exp, log, etc.)
- **Editor de Funciones**: Campo de texto con syntax highlighting básico
- **Área de Resultados**: Gráficos y tablas de resultados
- **Panel de Configuración**: Parámetros para cada método numérico
- **Menú de Créditos**: Información del equipo desarrollador

---

## ⚠️ LIMITACIONES Y RESTRICCIONES

### Limitaciones Técnicas
1. **Rendimiento**: Los cálculos deben completarse en < 5 segundos para funciones estándar
2. **Memoria**: Uso máximo de 512MB RAM para operaciones normales
3. **Compatibilidad**: Debe funcionar en Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
4. **Dependencias**: Minimizar dependencias externas, priorizar bibliotecas estándar

### Restricciones de Funcionalidad
1. **Entrada**: Solo funciones de una variable real
2. **Dominio**: Funciones definidas en intervalos finitos
3. **Precisión**: Máximo 15 dígitos significativos (limitación de float64)
4. **Complejidad**: Funciones con máximo 100 operaciones anidadas

### Limitaciones de Interfaz
1. **Resolución**: Optimizado para pantallas 1920x1080 mínimo
2. **Navegadores**: No requiere compatibilidad web (aplicación desktop)
3. **Idioma**: Interfaz en español (con opción de inglés como mejora futura)

---

## ✅ CRITERIOS DE ÉXITO

### Criterios Funcionales
- [ ] **Métodos Numéricos**: Todos los métodos implementados y validados con casos de prueba conocidos
- [ ] **Precisión**: Error relativo < 1e-6 para funciones de prueba estándar
- [ ] **Interfaz Completa**: Todos los elementos de UI funcionando correctamente
- [ ] **Entrada de Funciones**: Parser robusto que maneja sintaxis matemática estándar
- [ ] **Visualización**: Gráficos claros y exportables en formato PNG/PDF

### Criterios de Rendimiento
- [ ] **Tiempo de Respuesta**: Cálculos completados en < 3 segundos promedio
- [ ] **Estabilidad**: 0 crashes en 100 operaciones consecutivas
- [ ] **Escalabilidad**: Manejo eficiente de hasta 10,000 puntos de evaluación

### Criterios de Calidad
- [ ] **Código Limpio**: Cobertura de tests > 80%
- [ ] **Documentación**: Docstrings en todas las funciones principales
- [ ] **Usabilidad**: Usuario puede realizar cálculo completo en < 2 minutos sin documentación
- [ ] **Estética**: Interfaz moderna y profesional con feedback visual apropiado

### Criterios de Entrega
- [ ] **Créditos**: Pantalla de créditos con información completa del equipo
- [ ] **Manual**: Documentación de usuario en español
- [ ] **Instalación**: Script de instalación automatizada
- [ ] **Ejemplos**: Al menos 5 casos de uso documentados con resultados esperados

---

## 🔍 CHECKLIST DE VERIFICACIÓN PARA MEJORAS

### Funcionalidades Core
```python
# Verificar que estos métodos estén implementados:
- [ ] RungeKutta.euler()
- [ ] RungeKutta.rk2()
- [ ] RungeKutta.rk4()
- [ ] Integration.trapezoid()
- [ ] Integration.simpson_13()
- [ ] Integration.simpson_38()
- [ ] FiniteDifferences.forward()
- [ ] FiniteDifferences.backward()
- [ ] FiniteDifferences.central()
```

### Elementos de Interfaz
- [ ] Ventana principal redimensionable
- [ ] Teclado virtual matemático completo
- [ ] Campo de entrada con validación en tiempo real
- [ ] Área de gráficos integrada
- [ ] Panel de parámetros configurables
- [ ] Botones de exportación de resultados
- [ ] Menú de ayuda contextual

### Optimizaciones Sugeridas
1. **Vectorización**: Usar operaciones numpy para arrays grandes
2. **Caching**: Implementar cache de resultados para funciones repetidas
3. **Threading**: Cálculos pesados en hilos separados para mantener UI responsiva
4. **Validación**: Verificación robusta de entrada de funciones
5. **Error Handling**: Manejo elegante de errores matemáticos (división por cero, overflow, etc.)

---

## 📝 NOTAS PARA DESARROLLO

### Convenciones de Código
- **Estilo**: Seguir PEP 8
- **Naming**: Funciones en snake_case, clases en PascalCase
- **Comentarios**: Docstrings en español, comentarios técnicos en inglés
- **Testing**: Usar pytest para pruebas unitarias

### Estructura de Commits
```
feat: nueva funcionalidad
fix: corrección de bug
refactor: refactorización de código
docs: actualización de documentación
test: añadir o modificar tests
style: cambios de formato/estilo
perf: mejoras de rendimiento
```

### Entorno de Desarrollo Recomendado
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest tests/

# Ejecutar aplicación
python main.py
```

---

## 🎯 PRÓXIMOS PASOS

1. **Auditoría del Código Actual**: Revisar implementación existente contra estos criterios
2. **Gap Analysis**: Identificar funcionalidades faltantes
3. **Priorización**: Ordenar mejoras por impacto y complejidad
4. **Plan de Desarrollo**: Crear roadmap de implementación
5. **Testing**: Establecer suite de pruebas completa

---

*Este prompt debe ser usado como guía principal para el desarrollo y mejora del simulador matemático. Todos los criterios deben ser verificados antes de considerar el proyecto como completado.*