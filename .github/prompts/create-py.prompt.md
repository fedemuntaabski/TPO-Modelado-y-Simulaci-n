---
mode: agent
---

## 🎯 Objetivos del Prompt

Crear un simulador matemático avanzado que integre métodos numéricos con una interfaz gráfica moderna y funcional. El proyecto debe ser modular, extensible y fácil de mantener, proporcionando herramientas para resolver ecuaciones diferenciales, búsqueda de raíces, integración numérica, interpolación y derivadas numéricas.

### Objetivos Específicos:
- Implementar algoritmos numéricos precisos y eficientes
- Desarrollar una GUI intuitiva con PyQt6
- Crear una arquitectura modular para facilitar extensiones
- Incluir validaciones robustas y manejo de errores
- Proporcionar visualizaciones interactivas con matplotlib
- Mantener documentación completa y actualizada

## 🔧 Requerimientos Técnicos

### Lenguaje y Framework:
- **Python 3.8+** como lenguaje principal
- **PyQt6** para la interfaz gráfica
- **NumPy, SciPy, Matplotlib, SymPy** para computación científica

### Arquitectura:
- Estructura modular con directorios separados (core/, gui/, utils/, numerics/, tests/)
- Separación clara entre lógica de negocio y presentación
- Uso de clases y funciones reutilizables
- Manejo de excepciones y validaciones de entrada

### Funcionalidades Obligatorias:
- Resolución de EDOs (Euler, Runge-Kutta 2/4, SciPy)
- Búsqueda de raíces (Bisección, Newton-Raphson, Punto Fijo)
- Integración numérica (Trapecio, Simpson)
- Interpolación (Lagrange, diferencias finitas)
- Derivadas numéricas (diferencias finitas, Richardson)
- Teclado virtual para ingreso de funciones
- Visualización gráfica de resultados
- Sistema de créditos e información del equipo

### Calidad de Código:
- Comentarios descriptivos en español
- Nombres de variables y funciones en inglés
- Uso de type hints
- Pruebas unitarias con pytest
- Linting con flake8 y formateo con black

## ⚠️ Limitaciones

### Restricciones Técnicas:
- No usar bibliotecas externas no listadas en requirements.txt
- Mantener compatibilidad con Python 3.8+
- Limitar el uso de memoria para datasets grandes
- Evitar dependencias del sistema operativo específicas

### Restricciones de Diseño:
- Mantener la interfaz en español
- Usar tema oscuro profesional
- Limitar el número de botones en el teclado virtual
- Optimizar para pantallas de resolución estándar

### Restricciones de Alcance:
- Enfocarse en métodos numéricos básicos y avanzados
- No incluir funcionalidades no relacionadas con simulación matemática
- Mantener el proyecto autocontenido

## ✅ Criterios de Éxito

### Funcionalidad:
- [ ] Todos los métodos numéricos implementados correctamente
- [ ] GUI funcional y responsiva
- [ ] Validaciones de entrada robustas
- [ ] Visualizaciones precisas y útiles
- [ ] Teclado virtual operativo

### Calidad:
- [ ] Código modular y bien documentado
- [ ] Pruebas unitarias pasando
- [ ] Sin errores de linting
- [ ] Rendimiento aceptable en cálculos complejos

### Usabilidad:
- [ ] Interfaz intuitiva y moderna
- [ ] Mensajes de error claros
- [ ] Documentación completa
- [ ] Instalación automática de dependencias

### Mantenibilidad:
- [ ] Arquitectura extensible
- [ ] Código reutilizable
- [ ] Configuración centralizada
- [ ] Reportes de estado de implementación
