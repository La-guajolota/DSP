"""
Este script realiza el análisis espectral de una señal senoidal mediante:
1. Cálculo de la Transformada Discreta de Fourier (TDF) utilizando la FFT.
2. Normalización de la magnitud del espectro.
3. Cálculo de la Densidad Espectral de Potencia (PSD) en escala lineal.
4. Representación de la PSD en escala logarítmica (decibeles).

Se generan gráficas para visualizar:
- La magnitud del espectro.
- La magnitud normalizada del espectro.
- La PSD en escala lineal.
- La PSD en escala logarítmica.

Herramientas utilizadas:
- `numpy` para cálculos matemáticos.
- `matplotlib` para visualización de datos.
"""

import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
f0 = 100  # Frecuencia de oscilación (Hz)
fs = 1000  # Frecuencia de muestreo (Hz)
N = 1000  # Número de muestras

# Generación de la señal senoidal
n = np.arange(0, N)  # Vector de tiempo discreto
x = np.cos(2 * np.pi * (f0 / fs) * n)  # Señal senoidal

# Parámetros de la FFT
N1 = 1000  # Número de puntos para la TDF (puede incluir zero-padding)

# Cálculo de la Transformada Discreta de Fourier (TDF)
X = np.fft.fft(x, N1)  # FFT de la señal
Xshift = np.fft.fftshift(X)  # Centrar la FFT
f = np.arange(-N1 / 2, N1 / 2) * (fs / N1)  # Vector de frecuencias

# Gráfica 1: Magnitud del espectro
plt.figure(1)
plt.plot(f, np.abs(Xshift), label="|X(k)|")
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud |X(k)|')
plt.title('Magnitud del Espectro')
plt.grid(True)
plt.legend()

# Gráfica 2: Magnitud normalizada del espectro
plt.figure(2)
plt.plot(f, (1 / N) * np.abs(Xshift), label="|X(k)| Normalizada")
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud Normalizada |X(k)|')
plt.title('Magnitud Normalizada del Espectro')
plt.grid(True)
plt.legend()

# Cálculo de la Densidad Espectral de Potencia (PSD)
Sxx = (1 / N) * np.abs(X)**2  # PSD en escala lineal
Sxx_shift = np.fft.fftshift(Sxx)  # Centrar la PSD

# Gráfica 3: PSD en escala lineal
plt.figure(3)
plt.plot(f, Sxx_shift, label="PSD")
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Densidad Espectral de Potencia (V²/Hz)')
plt.title('Densidad Espectral de Potencia (PSD)')
plt.grid(True)
plt.legend()

# Cálculo de la PSD en escala logarítmica (decibeles)
Sxx_db = 10 * np.log10(Sxx_shift + 1e-12)  # Evitar log10(0) añadiendo un pequeño valor

# Gráfica 4: PSD en escala logarítmica
plt.figure(4)
plt.plot(f, Sxx_db, label="PSD (dB)")
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Densidad Espectral de Potencia (dB)')
plt.title('Densidad Espectral de Potencia (PSD) en dB')
plt.grid(True)
plt.legend()

# Mostrar todas las gráficas
plt.tight_layout()
plt.show()