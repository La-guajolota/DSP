# 📊 Biblioteca de custom tools de Procesamiento de Señales Digitales

![Banner](https://via.placeholder.com/800x200/4b6584/ffffff?text=Procesamiento+de+Se%C3%B1ales+Digitales)

<div align="center">
  
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20%2B-green.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.4%2B-orange.svg)](https://matplotlib.org/)

</div>

## 📝 Descripción General

Esta biblioteca implementa conceptos fundamentales del procesamiento de señales digitales:

- **Convolución Discreta** (dconv.py)
- **Transformada Discreta de Fourier** (dft.py)
- **Generación y Análisis de Señales** (dft_signal.py)

## 🧰 Módulos Disponibles

### 🔹 `dconv.py` - Convolución Discreta

<details open>
<summary><b>Detalles</b></summary>

Este módulo implementa la convolución discreta entre dos señales:
- **Filtro** (`h_filter`): Coeficientes que modelan el comportamiento del sistema.
- **Señal de entrada** (`x_signal`): Datos que queremos filtrar.

#### Algoritmo Implementado:

```python
def dconv(h, x):
    """
    Calcula la convolución discreta entre h (filtro) y x (señal).
    
    Parámetros:
    h (array): Coeficientes del filtro
    x (array): Señal de entrada
    
    Retorna:
    y (array): Señal convolucionada
    """
    # Longitud de la señal resultante
    M = len(h)
    N = len(x)
    y_length = M + N - 1
    
    # Inicializar array de salida con ceros
    y = np.zeros(y_length)
    
    # Realizar la convolución
    for n in range(y_length):
        for k in range(M):
            if n - k >= 0 and n - k < N:
                y[n] += h[k] * x[n - k]
                
    return y
```

#### Conceptualmente:
La convolución recorre todos los solapamientos posibles del filtro sobre la señal, multiplicando y sumando los valores para generar cada muestra de salida.

</details>

---

### 🔹 `dft.py` - Transformada Discreta de Fourier

<details open>
<summary><b>Detalles</b></summary>

Este módulo implementa la **Transformada Discreta de Fourier (DFT)**, una herramienta fundamental para transformar señales del dominio del tiempo al dominio de la frecuencia.

#### Algoritmo Implementado:

```python
def dft(x, padding=None):
    """
    Calcula la Transformada Discreta de Fourier.
    
    Parámetros:
    x (array): Señal de entrada en el dominio del tiempo
    padding (int, opcional): Longitud deseada para padding con ceros
    
    Retorna:
    X (array complejo): Coeficientes de la DFT
    """
    # Aplicar padding si es necesario
    if padding is not None:
        if isinstance(padding, int):
            N = padding
        else:
            N = 2**math.ceil(math.log2(len(x)))
        x_padded = np.zeros(N, dtype=complex)
        x_padded[:len(x)] = x
    else:
        x_padded = x
        N = len(x)
    
    # Inicializar array de salida
    X = np.zeros(N, dtype=complex)
    
    # Calcular la DFT
    for k in range(N):
        for n in range(N):
            X[k] += x_padded[n] * np.exp(-2j * np.pi * k * n / N)
            
    return X
```

#### Visualización Incluida:
La función `plot_dft(X, fs=1)` genera dos subplots:
- Gráfica de magnitud: `|X[k]|`
- Gráfica de fase: `∠X[k]`

</details>

---

### 🔹 `dft_signal.py` - Análisis de Señal Mediante DFT

<details open>
<summary><b>Detalles</b></summary>

Este módulo genera y analiza una señal compuesta sumando:
- Una **sinusoidal** con frecuencia `freq` (1 Hz por defecto)
- Una **cosenoidal** con frecuencia `freq/3` (≈0.33 Hz)

#### Generación de la Señal:

```python
# Parámetros de la señal
freq = 1.0                 # Frecuencia base (Hz)
signal_duration = 5.0      # Duración en segundos
fs = 10 * freq             # Frecuencia de muestreo
Ts = np.arange(0, signal_duration, 1/fs)  # Vector de tiempos

# Construcción de la señal compuesta
x = np.array([
    np.sin(2*np.pi*freq*t) + np.cos(2*np.pi*(freq/3)*t)
    for t in Ts
])
```

#### Análisis Mediante DFT:
1. Se calcula la DFT de la señal usando `dft(x)`
2. Se generan tres gráficas:
   - Señal en el dominio del tiempo
   - Magnitud de la DFT
   - Fase de la DFT

</details>

## 🚀 Uso Rápido

```python
# Ejemplo de convolución discreta
import numpy as np
from dconv import dconv

# Definir un filtro y una señal
h = np.array([0.2, 0.5, 0.3])  # Filtro de suavizado
x = np.array([1, 2, 3, 4, 5])  # Señal de entrada

# Calcular la convolución
y = dconv(h, x)
print("Señal convolucionada:", y)

# Ejemplo de DFT
from dft import dft, plot_dft

# Calcular la DFT
X = dft(x)
plot_dft(X, fs=1)
```

## 📈 Visualización de Resultados

![Ejemplo de Visualización](https://via.placeholder.com/800x400/8854d0/ffffff?text=Gr%C3%A1ficas+de+Se%C3%B1al+y+DFT)

## 📚 Fundamentos Teóricos

### Convolución Discreta
La convolución discreta entre dos señales `h` y `x` se define como:

$$y[n] = \sum_{k=0}^{M-1} h[k] \cdot x[n-k]$$

donde `M` es la longitud del filtro.

### Transformada Discreta de Fourier
La DFT de una secuencia `x` de longitud `N` se define como:

$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j2\pi kn/N}$$

para `k = 0, 1, ..., N-1`.

## 🛠️ Requisitos

- Python 3.8+
- NumPy
- Matplotlib

## 📄 Licencia

[MIT](LICENSE)

---

<div align="center">
  
Desarrollado con ❤️ para el análisis y procesamiento de señales digitales

</div>