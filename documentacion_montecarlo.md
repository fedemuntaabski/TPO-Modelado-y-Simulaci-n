# Documentación del Método Monte Carlo

## Descripción General

El método de Monte Carlo es una técnica estocástica para estimar integrales y resolver problemas numéricos mediante números aleatorios. La base matemática de este método para estimar una integral es:

$$ I = \int_a^b f(x) dx \approx (b-a) \cdot \frac{1}{N} \sum_{i=1}^{N} f(x_i) $$

Donde:
- $I$ es el valor de la integral
- $[a,b]$ es el intervalo de integración
- $N$ es el número de muestras aleatorias
- $x_i$ son puntos aleatorios distribuidos uniformemente en $[a,b]$

Para integrales bidimensionales, la fórmula se extiende a:

$$ I = \int_a^b \int_c^d f(x,y) dy dx \approx (b-a)(d-c) \cdot \frac{1}{N} \sum_{i=1}^{N} f(x_i, y_i) $$

## Estimación del Error

El error estándar en las estimaciones Monte Carlo se calcula como:

$$ \sigma = \frac{s}{\sqrt{N}} $$

Donde $s$ es la desviación estándar de los valores de la función evaluados en los puntos aleatorios. El intervalo de confianza al 95% se calcula como:

$$ IC_{95\%} = \hat{I} \pm 1.96 \cdot \sigma $$

Donde $\hat{I}$ es la estimación de la integral.

## Métodos Principales

### `simular(func: Callable, n_samples: int, seed: Optional[int], error_maximo: float, dimensions: int, x_range: Tuple[float, float], y_range: Optional[Tuple[float, float]]) -> Dict`
- **Descripción**: Ejecuta una simulación Monte Carlo para estimar una integral
- **Parámetros**:
  - `func`: Función a integrar
  - `n_samples`: Número de muestras aleatorias
  - `semilla`: Semilla para reproducibilidad (opcional)
  - `error_maximo`: Error máximo aceptable para IC
  - `dimensiones`: Dimensiones de integración (1 o 2)
  - `rango_x`: Rango en eje x (a, b)
  - `rango_y`: Rango en eje y (c, d) para integrales 2D
- **Retorna**: Diccionario con resultados, estadísticas y datos para visualización
- **Método**: Genera puntos aleatorios, evalúa la función y estima la integral
- **Complejidad**: O(N) donde N es el número de muestras

### `_generar_puntos(func: Callable, n_samples: int, dimensions: int, x_range: Tuple[float, float], y_range: Optional[Tuple[float, float]]) -> Tuple[np.ndarray, np.ndarray]`
- **Descripción**: Genera puntos aleatorios y evalúa la función en ellos
- **Parámetros**:
  - `func`: Función a evaluar
  - `n_samples`: Número de puntos aleatorios
  - `dimensions`: Dimensiones (1 o 2)
  - `x_range`: Rango en eje x
  - `y_range`: Rango en eje y (solo para 2D)
- **Retorna**: Tupla (puntos, valores) con los puntos generados y las evaluaciones de la función

### `_calcular_volumen(dimensions: int, x_range: Tuple[float, float], y_range: Optional[Tuple[float, float]]) -> float`
- **Descripción**: Calcula el volumen del dominio de integración
- **Parámetros**:
  - `dimensions`: Dimensiones (1 o 2)
  - `x_range`: Rango en eje x
  - `y_range`: Rango en eje y (solo para 2D)
- **Retorna**: Volumen del dominio
- **Fórmula**: Para 1D: b-a, Para 2D: (b-a)*(d-c)

### `_calcular_integracion(values: np.ndarray, volume: float) -> float`
- **Descripción**: Calcula el resultado de la integración Monte Carlo
- **Parámetros**:
  - `values`: Valores de la función evaluada en puntos aleatorios
  - `volume`: Volumen del dominio
- **Retorna**: Resultado de la integración
- **Fórmula**: volume * np.mean(values)

### `_calcular_estadisticas(values: np.ndarray, volume: float, error_maximo: float) -> Tuple[float, float, Tuple[float, float]]`
- **Descripción**: Calcula estadísticas de la simulación
- **Parámetros**:
  - `values`: Valores de las evaluaciones
  - `volume`: Volumen del dominio
  - `error_maximo`: Error máximo aceptable (determina el nivel de confianza)
- **Retorna**: Tupla (desviación estándar, error estándar, intervalo de confianza)
- **Intervalo de Confianza**: Utiliza distribución normal con z calculado dinámicamente usando `error_maximo`
- **Nota importante**: Un valor mayor de `error_maximo` produce intervalos de confianza más estrechos, ya que representa una menor exigencia de confianza estadística

### `_calcular_convergencia(func: Callable, n_samples: int, dimensions: int, x_range: Tuple[float, float], volume: float, y_range: Optional[Tuple[float, float]]) -> np.ndarray`
- **Descripción**: Genera datos para visualizar la convergencia del método
- **Parámetros**: Similar a `simular`
- **Retorna**: Array con datos de convergencia para diferentes tamaños de muestra
- **Método**: Toma puntos logarítmicamente espaciados para mostrar la evolución de la convergencia

### `_clasificar_puntos_exito_fracaso(points: np.ndarray, values: np.ndarray, dimensions: int) -> Tuple[np.ndarray, np.ndarray]`
- **Descripción**: Clasifica puntos para visualización según valores positivos/negativos
- **Parámetros**:
  - `points`: Coordenadas de los puntos generados
  - `values`: Valores de la función en esos puntos
  - `dimensions`: Dimensiones (1 o 2)
- **Retorna**: Tupla (puntos_dentro, puntos_fuera) para visualización

## Funciones Predeterminadas

El módulo incluye un conjunto de funciones predefinidas para pruebas y demostraciones:

### Funciones 1D
- `sin(x)`: Función seno
- `x²`: Función cuadrática
- `e^(-x²)`: Función gaussiana
- `sqrt(1-x²)`: Semicircunferencia (útil para aproximar π/4)

### Funciones 2D
- `x² + y²`: Función cuadrática bidimensional
- `sin(x)cos(y)`: Producto de funciones trigonométricas
- `e^(-(x²+y²))`: Función gaussiana bidimensional

## Interfaz de Usuario

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

## Ejemplo de Uso desde Código

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

## Verificación del Efecto del Parámetro error_maximo

Para verificar el efecto del parámetro `error_maximo` en la aplicación:

1. **Ejecuta la aplicación principal**:
   ```
   python main_simple.py
   ```

2. **Navega a la pestaña Monte Carlo**

3. **Configura la simulación con estos parámetros**:
   - Dimensión: 1D
   - Función: x^2
   - Número de muestras: 10000
   - Semilla: 42 (para reproducibilidad)
   - Error máximo: 0.05 (5%, nivel de confianza del 95%)
   - Rango X: 0 a 1

4. **Ejecuta la simulación y observa el resultado**
   - Anota el intervalo de confianza

5. **Cambia el Error máximo y vuelve a ejecutar**:
   - Prueba con error_maximo = 0.01 (99% de confianza)
   - Prueba con error_maximo = 0.2 (80% de confianza)

6. **Observa cómo varía el intervalo de confianza**:
   - Con error_maximo más pequeño (0.01): Intervalo más amplio
   - Con error_maximo más grande (0.2): Intervalo más estrecho

## Limitaciones y Consideraciones

- El número de muestras debe ser suficientemente grande para resultados precisos
- El método es sensible a la calidad del generador de números aleatorios
- Para funciones muy oscilatorias, puede requerir un número muy alto de muestras
- Se recomienda usar una semilla para garantizar reproducibilidad en pruebas
- El parámetro `error_maximo` controla el nivel de confianza: valores más pequeños (por ejemplo, 0.01) producen intervalos de confianza más amplios pero con mayor confianza estadística