# Documentación de Métodos Core - Simulador Matemático

Este documento proporciona una descripción detallada de los métodos principales implementados en los módulos core del Simulador Matemático.

## Índice
1. [Function Parser](#function-parse#### `simular(func: Callable, n_samples: int, seed: Optional[int], error_maximo: float, dimensions: int, x_range: Tuple[float, float], y_range: Optional[Tuple[float, float]] = None) -> Dict`
- **Descripción**: Ejecuta una simulación Monte Carlo para estimar una integral
- **Parámetros**:
  - `func`: Función a integrar
  - `n_samples`: Número de muestras aleatorias
  - `seed`: Semilla para reproducibilidad (opcional)
  - `error_maximo`: Error máximo aceptable para el nivel de confianza (e.g., 0.05 para 95% de confianza)
  - `dimensions`: Dimensiones de integración (1 o 2)
  - `x_range`: Rango en eje x (a, b)
  - `y_range`: Rango en eje y (c, d) para integrales 2D
- **Retorna**: Diccionario con resultados, estadísticas y datos para visualización
- **Método**: Genera puntos aleatorios, evalúa la función y estima la integral
- **Complejidad**: O(N) donde N es el número de muestrasFinding (Búsqueda de Raíces)](#root-finding)
3. [Newton-Cotes (Integración Numérica)](#newton-cotes)
4. [Monte Carlo Engine](#monte-carlo-engine)
5. [ODE Solver (Ecuaciones Diferenciales)](#ode-solver)
6. [Finite Differences (Diferencias Finitas)](#finite-differences)
7. [Integration (Integración Básica)](#integration)
8. [Integration Validators](#integration-validators)

---

## Function Parser

Módulo: `src/core/function_parser.py`

El parser de funciones permite convertir cadenas de texto que representan funciones matemáticas en funciones ejecutables de Python, manteniendo un entorno seguro.

### Métodos Principales

#### `parse_function(func_str: str, variables: list) -> Callable`
- **Descripción**: Crea una función Python a partir de una cadena de texto.
- **Parámetros**:
  - `func_str`: Cadena con la expresión matemática (ej. "x**2 + sin(x)")
  - `variables`: Lista de nombres de variables utilizadas en la función
- **Retorna**: Función callable que acepta los valores de las variables definidas
- **Seguridad**: Utiliza un diccionario restringido para prevenir ejecución de código malicioso

#### `FunctionParser.parse(func_str: str) -> Callable`
- **Descripción**: Método simplificado que parsea una función con una variable "x"
- **Parámetros**:
  - `func_str`: Cadena con la expresión matemática
- **Retorna**: Función ejecutable que acepta un valor para x

#### `FunctionParser.parse_and_evaluate(func_str: str, x_value) -> float`
- **Descripción**: Parsea y evalúa una función en un valor dado
- **Parámetros**:
  - `func_str`: Cadena con la expresión matemática
  - `x_value`: Valor donde evaluar la función
- **Retorna**: Resultado numérico de evaluar la función en x_value

#### `FunctionParser.validate_function(func_str: str) -> (bool, str)`
- **Descripción**: Verifica si una cadena representa una función válida
- **Parámetros**:
  - `func_str`: Cadena a validar
- **Retorna**: Tupla (es_válida, mensaje_error)

---

## Root Finding

Módulo: `src/core/root_finding.py`

Implementa métodos numéricos para encontrar raíces de funciones (valores de x donde f(x)=0).

### Métodos Principales

#### `bisection(func: Callable, a: float, b: float, tol: float, max_iter: int) -> dict`
- **Descripción**: Encuentra una raíz usando el método de bisección
- **Parámetros**:
  - `func`: Función a evaluar
  - `a, b`: Intervalo inicial donde f(a) y f(b) tienen signos opuestos
  - `tol`: Tolerancia para convergencia
  - `max_iter`: Número máximo de iteraciones
- **Retorna**: Diccionario con la raíz, iteraciones y otros detalles
- **Convergencia**: Garantizada pero lenta (lineal)

#### `newton_raphson(func: Callable, deriv: Callable, x0: float, tol: float, max_iter: int) -> dict`
- **Descripción**: Implementa el método de Newton-Raphson (tangente)
- **Parámetros**:
  - `func`: Función objetivo
  - `deriv`: Derivada de la función
  - `x0`: Aproximación inicial
  - `tol`: Tolerancia
  - `max_iter`: Iteraciones máximas
- **Retorna**: Diccionario con la raíz y detalles de convergencia
- **Convergencia**: Cuadrática cerca de la raíz si la derivada no es cero

#### `fixed_point(g: Callable, x0: float, tol: float, max_iter: int) -> dict`
- **Descripción**: Implementa el método de punto fijo
- **Parámetros**:
  - `g`: Función de iteración
  - `x0`: Punto inicial
  - `tol`: Tolerancia
  - `max_iter`: Iteraciones máximas
- **Retorna**: Diccionario con el punto fijo y detalles de convergencia
- **Convergencia**: Depende de si |g'(x)| < 1 cerca del punto fijo

#### `secant(func: Callable, x0: float, x1: float, tol: float, max_iter: int) -> dict`
- **Descripción**: Implementa el método de la secante
- **Parámetros**:
  - `func`: Función objetivo
  - `x0, x1`: Dos aproximaciones iniciales
  - `tol`: Tolerancia
  - `max_iter`: Iteraciones máximas
- **Retorna**: Diccionario con la raíz y detalles
- **Convergencia**: Superlineal (orden ~1.618)

---

## Newton-Cotes

Módulo: `src/core/newton_cotes.py`

Implementa métodos de integración numérica basados en las fórmulas de Newton-Cotes.

### Métodos Principales

#### `rectangle_simple(func_str: str, a: float, b: float) -> NewtonCotesResult`
- **Descripción**: Implementa la regla del rectángulo simple (punto medio)
- **Fórmula**: I ≈ (b-a) * f((a+b)/2)
- **Parámetros**:
  - `func_str`: Cadena con la función a integrar
  - `a, b`: Límites de integración
- **Retorna**: Objeto resultado con valor de la integral y detalles
- **Orden de Error**: O(h²)

#### `rectangle_composite(func_str: str, a: float, b: float, n: int) -> NewtonCotesResult`
- **Descripción**: Implementa la regla del rectángulo compuesta (punto medio)
- **Fórmula**: I ≈ h * Σf(xi) donde h = (b-a)/n, xi = a + (i-0.5)*h
- **Parámetros**:
  - `func_str`: Cadena con la función
  - `a, b`: Límites de integración
  - `n`: Número de subdivisiones
- **Retorna**: Objeto resultado
- **Orden de Error**: O(h²)

#### `trapezoid_simple(func_str: str, a: float, b: float) -> NewtonCotesResult`
- **Descripción**: Implementa la regla del trapecio simple
- **Fórmula**: I ≈ (b-a)/2 * [f(a) + f(b)]
- **Parámetros**:
  - `func_str`: Cadena con la función
  - `a, b`: Límites de integración
- **Retorna**: Objeto resultado
- **Orden de Error**: O(h²)

#### `trapezoid_composite(func_str: str, a: float, b: float, n: int) -> NewtonCotesResult`
- **Descripción**: Implementa la regla del trapecio compuesta
- **Fórmula**: I ≈ h/2 * [f(a) + 2*Σf(xi) + f(b)] donde h = (b-a)/n
- **Parámetros**:
  - `func_str`: Cadena con la función
  - `a, b`: Límites de integración
  - `n`: Número de subdivisiones
- **Retorna**: Objeto resultado
- **Orden de Error**: O(h²)

#### `simpson_13_simple(func_str: str, a: float, b: float) -> NewtonCotesResult`
- **Descripción**: Implementa la regla de Simpson 1/3 simple
- **Fórmula**: I ≈ (b-a)/6 * [f(a) + 4*f((a+b)/2) + f(b)]
- **Parámetros**:
  - `func_str`: Cadena con la función
  - `a, b`: Límites de integración
- **Retorna**: Objeto resultado
- **Orden de Error**: O(h⁴)

#### `simpson_13_composite(func_str: str, a: float, b: float, n: int) -> NewtonCotesResult`
- **Descripción**: Implementa la regla de Simpson 1/3 compuesta
- **Fórmula**: I ≈ h/3 * [f(a) + 4*Σf(x_impares) + 2*Σf(x_pares) + f(b)]
- **Parámetros**:
  - `func_str`: Cadena con la función
  - `a, b`: Límites de integración
  - `n`: Número de subdivisiones (debe ser par)
- **Retorna**: Objeto resultado
- **Orden de Error**: O(h⁴)

#### `simpson_38_simple(func_str: str, a: float, b: float) -> NewtonCotesResult`
- **Descripción**: Implementa la regla de Simpson 3/8 simple
- **Fórmula**: I ≈ (b-a)/8 * [f(a) + 3*f(a+h) + 3*f(a+2h) + f(b)] donde h=(b-a)/3
- **Parámetros**:
  - `func_str`: Cadena con la función
  - `a, b`: Límites de integración
- **Retorna**: Objeto resultado
- **Orden de Error**: O(h⁴)

#### `simpson_38_composite(func_str: str, a: float, b: float, n: int) -> NewtonCotesResult`
- **Descripción**: Implementa la regla de Simpson 3/8 compuesta
- **Fórmula**: I ≈ 3h/8 * [f(a) + 3*Σf(...) + f(b)]
- **Parámetros**:
  - `func_str`: Cadena con la función
  - `a, b`: Límites de integración
  - `n`: Número de subdivisiones (debe ser múltiplo de 3)
- **Retorna**: Objeto resultado
- **Orden de Error**: O(h⁴)

### Implementación en la UI (SimpleNewtonCotes)

En la interfaz de usuario (`src/ui/tabs/newton_cotes_tab.py`), se implementa una versión simplificada de los métodos Newton-Cotes a través de la clase `SimpleNewtonCotes`. Esta implementación:

- Proporciona los mismos métodos que el módulo core
- Incluye evaluación de funciones a través de numpy para cálculos vectorizados
- Usa una técnica de evaluación punto por punto para funciones como `sin(x)` para evitar problemas con arrays

#### Notas de implementación importantes:

Para los métodos compuestos (rectangle_composite, trapezoid_composite, simpson_13_composite, simpson_38_composite), la evaluación de funciones se realiza individualmente para cada punto, evitando errores con funciones matemáticas aplicadas a arrays:

```python
# Implementación optimizada para evitar errores con funciones matemáticas
x = np.linspace(a, b, n + 1)
y = np.array([f(float(xi)) for xi in x])  # Evaluación punto por punto
```

Este enfoque garantiza compatibilidad con todas las funciones matemáticas, incluyendo funciones trigonométricas como `sin(x)`, `cos(x)`, etc.

---

## Monte Carlo Engine

Módulo: `src/core/monte_carlo_engine.py`

Implementa métodos de integración y simulación estocástica mediante técnicas de Monte Carlo.

### Fundamentos Teóricos

El método de Monte Carlo es una técnica estocástica para estimar integrales y resolver problemas numéricos mediante números aleatorios. La base matemática de este método para estimar una integral es:

$$ I = \int_a^b f(x) dx \approx (b-a) \cdot \frac{1}{N} \sum_{i=1}^{N} f(x_i) $$

Donde:
- $I$ es el valor de la integral
- $[a,b]$ es el intervalo de integración
- $N$ es el número de muestras aleatorias
- $x_i$ son puntos aleatorios distribuidos uniformemente en $[a,b]$

Para integrales bidimensionales, la fórmula se extiende a:

$$ I = \int_a^b \int_c^d f(x,y) dy dx \approx (b-a)(d-c) \cdot \frac{1}{N} \sum_{i=1}^{N} f(x_i, y_i) $$

La convergencia del método es del orden $O(1/\sqrt{N})$, lo que significa que para reducir el error a la mitad, se necesita cuadruplicar el número de muestras.

### Estimación del Error

El error estándar en las estimaciones Monte Carlo se calcula como:

$$ \sigma = \frac{s}{\sqrt{N}} $$

Donde $s$ es la desviación estándar de los valores de la función evaluados en los puntos aleatorios. El intervalo de confianza al 95% se calcula como:

$$ IC_{95\%} = \hat{I} \pm 1.96 \cdot \sigma $$

Donde $\hat{I}$ es la estimación de la integral.

### Métodos Principales

#### `simular(func: Callable, n_samples: int, seed: Optional[int], max_error: float, dimensions: int, x_range: Tuple[float, float], y_range: Optional[Tuple[float, float]]) -> Dict`
- **Descripción**: Ejecuta una simulación Monte Carlo para estimar una integral
- **Parámetros**:
  - `func`: Función a integrar
  - `n_samples`: Número de muestras aleatorias
  - `seed`: Semilla para reproducibilidad (opcional)
  - `max_error`: Error máximo aceptable para IC
  - `dimensions`: Dimensiones de integración (1 o 2)
  - `x_range`: Rango en eje x (a, b)
  - `y_range`: Rango en eje y (c, d) para integrales 2D
- **Retorna**: Diccionario con resultados, estadísticas y datos para visualización
- **Método**: Genera puntos aleatorios, evalúa la función y estima la integral
- **Complejidad**: O(N) donde N es el número de muestras

#### `_generar_puntos(func: Callable, n_samples: int, dimensions: int, x_range: Tuple[float, float], y_range: Optional[Tuple[float, float]]) -> Tuple[np.ndarray, np.ndarray]`
- **Descripción**: Genera puntos aleatorios y evalúa la función en ellos
- **Parámetros**:
  - `func`: Función a evaluar
  - `n_samples`: Número de puntos aleatorios
  - `dimensions`: Dimensiones (1 o 2)
  - `x_range`: Rango en eje x
  - `y_range`: Rango en eje y (solo para 2D)
- **Retorna**: Tupla (puntos, valores) con los puntos generados y las evaluaciones de la función

#### `_calcular_volumen(dimensions: int, x_range: Tuple[float, float], y_range: Optional[Tuple[float, float]]) -> float`
- **Descripción**: Calcula el volumen del dominio de integración
- **Parámetros**:
  - `dimensions`: Dimensiones (1 o 2)
  - `x_range`: Rango en eje x
  - `y_range`: Rango en eje y (solo para 2D)
- **Retorna**: Volumen del dominio
- **Fórmula**: Para 1D: b-a, Para 2D: (b-a)*(d-c)

#### `_calcular_integracion(values: np.ndarray, volume: float) -> float`
- **Descripción**: Calcula el resultado de la integración Monte Carlo
- **Parámetros**:
  - `values`: Valores de la función evaluada en puntos aleatorios
  - `volume`: Volumen del dominio
- **Retorna**: Resultado de la integración
- **Fórmula**: volume * np.mean(values)

#### `_calcular_estadisticas(values: np.ndarray, volume: float, error_maximo: float) -> Tuple[float, float, Tuple[float, float]]`
- **Descripción**: Calcula estadísticas de la simulación
- **Parámetros**:
  - `values`: Valores de las evaluaciones
  - `volume`: Volumen del dominio
  - `error_maximo`: Error máximo aceptable (determina el nivel de confianza)
- **Retorna**: Tupla (desviación estándar, error estándar, intervalo de confianza)
- **Intervalo de Confianza**: Utiliza distribución normal con z calculado dinámicamente usando `error_maximo`
- **Nota importante**: Un valor mayor de `error_maximo` produce intervalos de confianza más estrechos, ya que representa una menor exigencia de confianza estadística

#### `_calculate_convergence(func: Callable, n_samples: int, dimensions: int, x_range: Tuple[float, float], volume: float, y_range: Optional[Tuple[float, float]]) -> np.ndarray`
- **Descripción**: Genera datos para visualizar la convergencia del método
- **Parámetros**: Similar a `simular`
- **Retorna**: Array con datos de convergencia para diferentes tamaños de muestra
- **Método**: Toma puntos logarítmicamente espaciados para mostrar la evolución de la convergencia

#### `_classify_points(points: np.ndarray, values: np.ndarray, dimensions: int) -> Tuple[np.ndarray, np.ndarray]`
- **Descripción**: Clasifica puntos para visualización según valores positivos/negativos
- **Parámetros**:
  - `points`: Coordenadas de los puntos generados
  - `values`: Valores de la función en esos puntos
  - `dimensions`: Dimensiones (1 o 2)
- **Retorna**: Tupla (puntos_dentro, puntos_fuera) para visualización

### Funciones Predeterminadas

El módulo incluye un conjunto de funciones predefinidas para pruebas y demostraciones:

#### Funciones 1D
- `sin(x)`: Función seno
- `x²`: Función cuadrática
- `e^(-x²)`: Función gaussiana
- `sqrt(1-x²)`: Semicircunferencia (útil para aproximar π/4)

#### Funciones 2D
- `x² + y²`: Función cuadrática bidimensional
- `sin(x)cos(y)`: Producto de funciones trigonométricas
- `e^(-(x²+y²))`: Función gaussiana bidimensional

### Interfaz de Usuario

El módulo `monte_carlo_tab.py` implementa una interfaz gráfica completa que permite:

1. **Seleccionar dimensionalidad**: 1D o 2D
2. **Ingresar función**: Mediante expresión matemática personalizada
3. **Configurar parámetros**:
   - Número de muestras
   - Semilla para reproducibilidad
   - Error máximo aceptable
   - Rangos de integración
4. **Visualizar resultados**:
   - Valor estimado de la integral
   - Estadísticas de error
   - Intervalos de confianza
   - Gráficos de puntos y convergencia

### Ejemplo de Uso desde Código

```python
from src.core.monte_carlo_engine import MonteCarloEngine
import numpy as np

# Crear instancia del motor
mc_engine = MonteCarloEngine()

# Definir función a integrar
def my_function(x):
    return x**2 * np.sin(x)

# Ejecutar simulación con un 95% de confianza (error_maximo = 0.05)
results = mc_engine.simular(
    func=my_function,
    n_samples=100000,
    semilla=42,
    error_maximo=0.05,  # 95% de confianza
    dimensiones=1,
    rango_x=(0, np.pi)
)

# Acceder a resultados
valor_integral = results['resultado_integracion']
intervalo_confianza = results['intervalo_confianza']
error_estandar = results['error_estandar']

print(f"Valor estimado: {valor_integral}")
print(f"Intervalo de confianza (95%): {intervalo_confianza}")
print(f"Error estándar: {error_estandar}")

# Ejemplo con otro nivel de confianza (99%)
results_high_conf = mc_engine.simular(
    func=my_function,
    n_samples=100000,
    semilla=42,
    error_maximo=0.01,  # 99% de confianza
    dimensiones=1,
    rango_x=(0, np.pi)
)

print(f"Intervalo de confianza (99%): {results_high_conf['intervalo_confianza']}")
```

### Limitaciones y Consideraciones

- La convergencia es del orden O(1/√N), relativamente lenta
- El número de muestras debe ser suficientemente grande para resultados precisos
- El método es sensible a la calidad del generador de números aleatorios
- Para funciones muy oscilatorias, puede requerir un número muy alto de muestras
- Se recomienda usar una semilla para garantizar reproducibilidad en pruebas
- El parámetro `error_maximo` controla el nivel de confianza: valores más pequeños (por ejemplo, 0.01) producen intervalos de confianza más amplios pero con mayor confianza estadística

---

## ODE Solver

Módulo: `src/core/ode_solver.py`

Implementa métodos para resolver ecuaciones diferenciales ordinarias (EDOs).

### Métodos Principales

#### `euler(f: Callable, y0: float, t_span: Tuple[float, float], h: float) -> Dict`
- **Descripción**: Implementa el método de Euler para resolver EDOs
- **Ecuación**: y_{n+1} = y_n + h*f(t_n, y_n)
- **Parámetros**:
  - `f`: Función f(t, y) que define la EDO dy/dt = f(t, y)
  - `y0`: Valor inicial y(t0)
  - `t_span`: Tupla (t0, tf) con intervalo de tiempo
  - `h`: Tamaño de paso
- **Retorna**: Diccionario con la solución y detalles
- **Orden de Error**: O(h)

#### `heun(f: Callable, y0: float, t_span: Tuple[float, float], h: float) -> Dict`
- **Descripción**: Implementa el método de Heun (Runge-Kutta de orden 2)
- **Ecuación**: Predictor-Corrector basado en Euler
- **Parámetros**: Similares a `euler`
- **Retorna**: Diccionario con la solución y detalles
- **Orden de Error**: O(h²)

#### `rk4(f: Callable, y0: float, t_span: Tuple[float, float], h: float) -> Dict`
- **Descripción**: Implementa el método de Runge-Kutta de 4º orden
- **Ecuación**: Usa 4 evaluaciones por paso para mayor precisión
- **Parámetros**: Similares a `euler`
- **Retorna**: Diccionario con la solución y detalles
- **Orden de Error**: O(h⁴)

#### `rk45_adaptive(f: Callable, y0: float, t_span: Tuple[float, float], tol: float, h_init: float, h_max: float) -> Dict`
- **Descripción**: Implementa Runge-Kutta-Fehlberg (RK45) con paso adaptativo
- **Ecuación**: Combina evaluaciones de 4º y 5º orden para estimar error
- **Parámetros**:
  - Similares a los anteriores, más:
  - `tol`: Tolerancia para control de error
  - `h_init`: Tamaño de paso inicial
  - `h_max`: Tamaño máximo de paso permitido
- **Retorna**: Diccionario con solución, pasos adaptados y detalles
- **Característica**: Ajusta automáticamente el tamaño de paso según el error

---

## Finite Differences

Módulo: `src/core/finite_differences.py`

Implementa métodos de diferencias finitas para aproximar derivadas.

### Métodos Principales

#### `forward_difference(f: Callable, x: float, h: float, order: int = 1) -> Dict`
- **Descripción**: Implementa diferencia finita hacia adelante
- **Fórmula**: f'(x) ≈ [f(x+h) - f(x)]/h
- **Parámetros**:
  - `f`: Función a derivar
  - `x`: Punto donde calcular la derivada
  - `h`: Tamaño de paso
  - `order`: Orden de la derivada (1 o 2)
- **Retorna**: Diccionario con valor de derivada y detalles
- **Orden de Error**: O(h)

#### `backward_difference(f: Callable, x: float, h: float, order: int = 1) -> Dict`
- **Descripción**: Implementa diferencia finita hacia atrás
- **Fórmula**: f'(x) ≈ [f(x) - f(x-h)]/h
- **Parámetros**: Similares a `forward_difference`
- **Retorna**: Diccionario con valor de derivada y detalles
- **Orden de Error**: O(h)

#### `central_difference(f: Callable, x: float, h: float, order: int = 1) -> Dict`
- **Descripción**: Implementa diferencia finita central
- **Fórmula**: f'(x) ≈ [f(x+h) - f(x-h)]/(2h)
- **Parámetros**: Similares a `forward_difference`
- **Retorna**: Diccionario con valor de derivada y detalles
- **Orden de Error**: O(h²)

#### `five_point_difference(f: Callable, x: float, h: float, order: int = 1) -> Dict`
- **Descripción**: Implementa fórmula de 5 puntos para mayor precisión
- **Fórmula**: Usa puntos x-2h, x-h, x, x+h, x+2h
- **Parámetros**: Similares a `forward_difference`
- **Retorna**: Diccionario con valor de derivada y detalles
- **Orden de Error**: O(h⁴)

#### `richardson_extrapolation(f: Callable, x: float, h: float, method_func: Callable, order: int = 1) -> Dict`
- **Descripción**: Implementa extrapolación de Richardson para mejorar precisión
- **Método**: Combina aproximaciones con diferentes h para cancelar términos de error
- **Parámetros**:
  - Similares a los anteriores, más:
  - `method_func`: Función del método base a mejorar
- **Retorna**: Diccionario con valor mejorado y detalles
- **Orden de Error**: Depende del método base, generalmente mejora 2 órdenes

---

## Integration

Módulo: `src/core/integration.py`

Implementa métodos básicos de integración numérica.

### Métodos Principales

#### `trapezoid(f: Callable, a: float, b: float, n: int) -> Dict`
- **Descripción**: Implementa la regla del trapecio para integración
- **Fórmula**: I ≈ (b-a)/n * [f(a)/2 + Σf(xi) + f(b)/2]
- **Parámetros**:
  - `f`: Función a integrar
  - `a, b`: Límites de integración
  - `n`: Número de subdivisiones
- **Retorna**: Diccionario con valor de la integral y detalles
- **Orden de Error**: O(h²)

#### `simpson13(f: Callable, a: float, b: float, n: int) -> Dict`
- **Descripción**: Implementa la regla de Simpson 1/3
- **Fórmula**: I ≈ h/3 * [f(a) + 4*Σf(x_impares) + 2*Σf(x_pares) + f(b)]
- **Parámetros**: Similares a `trapezoid`
- **Retorna**: Diccionario con valor de la integral y detalles
- **Orden de Error**: O(h⁴)
- **Requisito**: n debe ser par

#### `simpson38(f: Callable, a: float, b: float, n: int) -> Dict`
- **Descripción**: Implementa la regla de Simpson 3/8
- **Fórmula**: I ≈ 3h/8 * [f(a) + 3*Σf(...) + f(b)]
- **Parámetros**: Similares a `trapezoid`
- **Retorna**: Diccionario con valor de la integral y detalles
- **Orden de Error**: O(h⁴)
- **Requisito**: n debe ser múltiplo de 3

---

## Integration Validators

Módulo: `src/core/integration_validators.py`

Proporciona validaciones para los métodos de integración numérica.

### Métodos Principales

#### `validate_interval(a: float, b: float) -> None`
- **Descripción**: Valida que el intervalo de integración sea válido
- **Parámetros**:
  - `a, b`: Límites del intervalo
- **Valida**:
  - Que a y b sean números válidos (no NaN, no infinitos)
  - Que a < b
- **Retorna**: None o lanza IntegrationValidationError

#### `validate_subdivisions(n: int, min_n: int = 1, max_n: int = 1_000_000) -> None`
- **Descripción**: Valida el número de subdivisiones
- **Parámetros**:
  - `n`: Número de subdivisiones
  - `min_n`: Mínimo permitido
  - `max_n`: Máximo permitido
- **Valida**:
  - Que n sea un entero
  - Que min_n ≤ n ≤ max_n
- **Retorna**: None o lanza IntegrationValidationError

#### `validate_simpson_13_n(n: int) -> None`
- **Descripción**: Valida que n sea par para Simpson 1/3
- **Parámetros**:
  - `n`: Número de subdivisiones
- **Valida**:
  - Que n sea par
- **Retorna**: None o lanza IntegrationValidationError

#### `validate_simpson_38_n(n: int) -> None`
- **Descripción**: Valida que n sea múltiplo de 3 para Simpson 3/8
- **Parámetros**:
  - `n`: Número de subdivisiones
- **Valida**:
  - Que n sea múltiplo de 3
- **Retorna**: None o lanza IntegrationValidationError

---

Este documento proporciona una referencia completa de los métodos principales del core del Simulador Matemático, detallando sus parámetros, funcionamiento y características para facilitar su comprensión y uso.
