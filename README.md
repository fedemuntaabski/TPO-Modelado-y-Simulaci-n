# Simulador de Métodos Numéricos 

Un simulador interactivo para métodos numéricos con interfaz gráfica moderna, completamente modularizado siguiendo principios de ingeniería de software.

## 🚀 Características

- **Búsqueda de Raíces**: Bisección, Newton-Raphson, Punto Fijo
- **Integración Numérica**: Trapecio, Simpson 1/3, Simpson 3/8, métodos adaptativos
- **Resolución de ODEs**: Euler, Runge-Kutta (2º y 4º orden), Heun, RK45 adaptativo
- **Diferencias Finitas**: Adelante, atrás, central, 5 puntos, Richardson, paso adaptativo
- **Interfaz Moderna**: CustomTkinter con diseño responsivo
- **Visualización**: Gráficos interactivos con Matplotlib
- **Tests Completos**: Suite de pruebas unitarias para todos los módulos

## 📁 Estructura del Proyecto

```
├── main.py                 # Punto de entrada principal
├── src/
│   ├── core/              # Algoritmos matemáticos
│   │   ├── root_finding.py
│   │   ├── integration.py
│   │   ├── ode_solver.py
│   │   └── finite_differences.py
│   └── ui/                # Interfaz gráfica
│       ├── main_app.py    # Aplicación principal
│       ├── components/    # Componentes base
│       │   └── base_tab.py
│       └── tabs/          # Pestañas específicas
│           ├── roots_tab.py
│           ├── integration_tab.py
│           ├── ode_tab.py
│           └── finite_diff_tab.py
├── config/
│   └── settings.py        # Configuración global
├── tests/                 # Tests unitarios
│   ├── test_root_finding.py
│   ├── test_integration.py
│   ├── test_ode_solver.py
│   ├── test_finite_differences.py
│   └── run_tests.py      # Ejecutor de tests
└── requirements_minimal.txt
```

## 🛠️ Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd TPO-Modelado-y-Simulaci-n
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements_minimal.txt
   ```

3. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

## 🧪 Testing

### Ejecutar todos los tests:
```bash
python tests/run_tests.py
```

### Ejecutar tests de un módulo específico:
```bash
python tests/run_tests.py root_finding
python tests/run_tests.py integration
python tests/run_tests.py ode_solver
python tests/run_tests.py finite_differences
```

### Ejecutar tests individuales:
```bash
python -m unittest tests.test_root_finding -v
python -m unittest tests.test_integration -v
python -m unittest tests.test_ode_solver -v
python -m unittest tests.test_finite_differences -v
```

## 📊 Uso de la Aplicación

### Búsqueda de Raíces
1. Selecciona el método (Bisección, Newton-Raphson, Punto Fijo)
2. Ingresa la función como string (ej: `x**2 - 4`)
3. Define el intervalo o valor inicial
4. Ajusta tolerancia e iteraciones máximas
5. Ejecuta y visualiza los resultados

### Integración Numérica
1. Elige el método de integración
2. Ingresa la función a integrar
3. Define los límites de integración
4. Especifica el número de subdivisiones
5. Compara resultados con diferentes métodos

### Resolución de ODEs
1. Selecciona el método de integración
2. Define la ecuación diferencial
3. Establece condiciones iniciales
4. Configura el paso y rango de solución
5. Visualiza la solución gráficamente

### Diferencias Finitas
1. Elige el tipo de diferencia finita
2. Ingresa la función a derivar
3. Especifica el punto y tamaño de paso
4. Compara precisión entre métodos
5. Analiza convergencia

## 🎯 Principios de Diseño Implementados

### SOLID
- **S**ingle Responsibility: Cada clase tiene una responsabilidad específica
- **O**pen/Closed: Extensible sin modificar código existente
- **L**iskov Substitution: Las subclases son intercambiables
- **I**nterface Segregation: Interfaces específicas y cohesivas
- **D**ependency Inversion: Dependencias hacia abstracciones

### Otros Principios
- **DRY** (Don't Repeat Yourself): Código reutilizable y modular
- **KISS** (Keep It Simple, Stupid): Soluciones simples y claras
- **Separation of Concerns**: UI, lógica y datos separados

## 🔧 Configuración

Modifica `config/settings.py` para personalizar:

```python
# Configuración de UI
UI_SETTINGS = {
    'theme': 'dark',
    'color_theme': 'blue',
    'window_size': (1200, 800)
}

# Configuración de gráficos
PLOT_SETTINGS = {
    'figure_size': (8, 6),
    'dpi': 100,
    'style': 'default'
}

# Configuración numérica
NUMERICAL_SETTINGS = {
    'default_tolerance': 1e-10,
    'max_iterations': 1000,
    'default_step_size': 0.01
}
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Notas de Desarrollo

### Agregar Nuevos Métodos
1. Implementa la lógica en el módulo correspondiente en `src/core/`
2. Actualiza la interfaz en `src/ui/tabs/`
3. Agrega tests en `tests/`
4. Actualiza la configuración si es necesario

### Estructura de Tests
- Tests básicos: Funcionalidad core
- Tests avanzados: Casos complejos
- Tests de casos límite: Manejo de errores

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.
