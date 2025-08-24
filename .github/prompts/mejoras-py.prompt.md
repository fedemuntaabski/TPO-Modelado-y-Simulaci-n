---
mode: agent
---

# 🎨 MEJORAS AL SIMULADOR MATEMÁTICO AVANZADO

## 📋 TAREA PRINCIPAL
Mejorar la interfaz gráfica y funcionalidades del simulador matemático para una experiencia de usuario más profesional, moderna y comparativa entre métodos numéricos.

## 🎯 REQUISITOS ESPECÍFICOS

### 1. 🎨 MEJORAS VISUALES Y DE DISEÑO

#### A. Esquema de Colores y Contraste
- **CAMBIAR** el fondo blanco por un esquema gris moderno
- **APLICAR** colores de fondo: `#2c3e50` (gris oscuro principal) y `#34495e` (gris medio)
- **CONFIGURAR** texto en colores claros para buen contraste: `#ecf0f1` (blanco suave)
- **USAR** paleta de colores consistente en toda la aplicación

#### B. Rediseño del Header/Título
- **ELIMINAR** completamente la referencia "TPO Modelado y Simulación 2025"
- **REFORMATEAR** el título "SIMULADOR MATEMÁTICO AVANZADO" para que no se vea "aplastado"
- **APLICAR** tipografía más espaciada y elegante
- **CENTRAR** correctamente el título con mejor proporción visual

#### C. Limpieza del Teclado Virtual
- **REMOVER** los botones numéricos: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
- **REMOVER** los botones de paréntesis: ( )
- **REMOVER** las variables: "x", "t", "y" del teclado virtual
- **MANTENER** solo funciones matemáticas: sin, cos, tan, exp, log, sqrt, pi, e
- **REORGANIZAR** el layout del teclado para mejor usabilidad

### 2. ✨ ANIMACIONES E INTERACTIVIDAD

#### A. Animaciones de Transición
- **AGREGAR** efectos de fade-in cuando se cambia entre pestañas
- **IMPLEMENTAR** animaciones suaves en botones al hacer hover
- **CREAR** transiciones suaves en gráficos al actualizar datos
- **AÑADIR** indicadores de progreso animados durante cálculos

#### B. Feedback Visual
- **IMPLEMENTAR** efectos de pulsación en botones
- **AGREGAR** colores de estado (éxito/error) con transiciones
- **CREAR** tooltips informativos con animaciones

### 3. 📊 COMPARACIÓN DE MÉTODOS NUMÉRICOS

#### A. Pestaña de Comparación de Métodos de Raíces
- **CREAR** nueva pestaña "🔄 Comparación de Métodos"
- **IMPLEMENTAR** comparación lado a lado de:
  - Punto Fijo vs Bisección
  - Newton-Raphson vs Bisección
  - Los tres métodos simultáneamente
- **MOSTRAR** gráficos comparativos de convergencia
- **INCLUIR** tabla de comparación de iteraciones, errores y velocidad

#### B. Visualización Avanzada de Convergencia
- **AGREGAR** gráficos de convergencia con múltiples curvas
- **IMPLEMENTAR** zoom interactivo en gráficos
- **CREAR** leyendas dinámicas y personalizables
- **MOSTRAR** análisis estadístico de cada método

#### C. Comparación de Aceleración
- **IMPLEMENTAR** comparación Aitken vs método original
- **MOSTRAR** mejora en velocidad de convergencia
- **GRAFICAR** ambas secuencias en el mismo plot
- **CALCULAR** factor de aceleración obtenido

## 🚫 LIMITACIONES Y RESTRICCIONES

### Restricciones Técnicas
1. **MANTENER** la compatibilidad con PyQt6
2. **PRESERVAR** toda la funcionalidad matemática existente
3. **NO ROMPER** la estructura modular del código
4. **MANTENER** la instalación automática de dependencias

### Restricciones de Diseño
1. **NO CAMBIAR** la funcionalidad core de los métodos numéricos
2. **PRESERVAR** la facilidad de uso para usuarios no técnicos
3. **MANTENER** la responsividad de la interfaz
4. **NO EXCEDER** 1400x900 píxeles como tamaño base de ventana

### Restricciones de Rendimiento
1. **GARANTIZAR** que las animaciones no afecten los cálculos
2. **MANTENER** tiempo de startup < 3 segundos
3. **ASEGURAR** que las comparaciones no consuman memoria excesiva

## ✅ CRITERIOS DE ÉXITO

### 1. 🎨 Criterios Visuales
- [ ] El fondo es gris moderno con buen contraste
- [ ] El título se ve proporcionado y elegante
- [ ] No aparece "TPO Modelado y Simulación 2025" en ningún lugar
- [ ] El teclado virtual contiene solo funciones matemáticas
- [ ] Los colores son consistentes en toda la aplicación

### 2. ✨ Criterios de Animación
- [ ] Las transiciones entre pestañas son suaves (< 300ms)
- [ ] Los botones responden visualmente al hover
- [ ] Los gráficos se actualizan con animaciones fluidas
- [ ] Hay indicadores de progreso durante cálculos largos

### 3. 📊 Criterios de Comparación
- [ ] Existe una pestaña dedicada a comparación de métodos
- [ ] Se pueden comparar al menos 2 métodos simultáneamente
- [ ] Los gráficos muestran claramente las diferencias de convergencia
- [ ] Hay métricas cuantitativas de comparación (iteraciones, errores, tiempo)

### 4. 🔧 Criterios Técnicos
- [ ] Toda la funcionalidad original sigue funcionando
- [ ] La aplicación inicia sin errores
- [ ] Las animaciones no causan lag o bloqueos
- [ ] El código mantiene la estructura modular

### 5. 👤 Criterios de Usabilidad
- [ ] La interfaz es más intuitiva que la versión anterior
- [ ] Los usuarios pueden entender fácilmente las comparaciones
- [ ] El contraste mejora la legibilidad
- [ ] Los tooltips proporcionan información útil

## 🔧 IMPLEMENTACIÓN SUGERIDA

### Archivos a Modificar:
1. **gui/main_window.py** - Rediseño visual y animaciones
2. **gui/advanced_tabs.py** - Nueva pestaña de comparación
3. **main.py** - Aplicar tema oscuro globalmente

### Nuevos Archivos a Crear:
1. **gui/comparison_tab.py** - Pestaña de comparación de métodos
2. **gui/animations.py** - Utilidades para animaciones
3. **gui/themes.py** - Definición de temas y colores

### Tecnologías Adicionales:
- **QPropertyAnimation** (PyQt6) para animaciones suaves
- **QGraphicsEffect** para efectos visuales
- **QTimer** para actualizaciones progresivas

## 📝 NOTAS DE IMPLEMENTACIÓN

### Prioridad Alta (Crítico):
1. Cambio de esquema de colores
2. Rediseño del título
3. Limpieza del teclado virtual

### Prioridad Media (Importante):
1. Animaciones básicas
2. Pestaña de comparación de métodos

### Prioridad Baja (Deseable):
1. Animaciones avanzadas
2. Tooltips interactivos
3. Efectos visuales adicionales

### Testing:
- **Verificar** que todas las mejoras funcionan en Windows, macOS y Linux
- **Comprobar** rendimiento con diferentes tamaños de datasets
- **Validar** que las animaciones no interfieren con los cálculos numéricos