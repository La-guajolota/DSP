"""
Este script realiza el análisis espectral de señales senoidales mediante:
1. Generación de señales:
   - Una señal compuesta por la suma de dos senoidales.
   - Una señal formada por la concatenación de dos senoidales.
2. Cálculo del espectro de las señales utilizando la Transformada Rápida de Fourier (FFT).
3. Generación de espectrogramas para analizar la distribución de frecuencia en el tiempo.
4. Visualización en 3D del espectrograma de la señal concatenada.

Se utilizan herramientas de `numpy`, `matplotlib` y `scipy` para realizar los cálculos y las visualizaciones.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib.cm as cm

# Parámetros de las señales
fs = 20  # Frecuencia de muestreo (Hz)
f0 = 1   # Frecuencia de la primera señal (Hz)
f1 = 5   # Frecuencia de la segunda señal (Hz)

# Generación de señales
n = np.arange(0, 199)  # Vector de tiempo discreto para la señal completa
n2 = np.arange(0, 199)  # Vector de tiempo discreto para la señal concatenada

# Señal 1: Suma de dos senoidales
x1 = np.sin(2 * np.pi * (f0 / fs) * n) + np.sin(2 * np.pi * (f1 / fs) * n)

# Señal 2: Concatenación de dos senoidales
x2 = np.concatenate([np.sin(2 * np.pi * (f0 / fs) * n), np.sin(2 * np.pi * (f1 / fs) * n2)])

# Gráfica de las señales en el dominio del tiempo
plt.figure(1)
plt.plot(n, x1, label="Suma de senoidales")
plt.title("Señal: Suma de dos senoidales")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")
plt.grid(True)
plt.legend()

plt.figure(2)
plt.plot(np.arange(len(x2)), x2, label="Concatenación de senoidales")
plt.title("Señal: Concatenación de dos senoidales")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")
plt.grid(True)
plt.legend()

# Cálculo del espectro de las señales
N = 1000  # Número de puntos para la FFT
f = np.arange(-N / 2, N / 2) * (fs / N)  # Vector de frecuencias

# Espectro de la señal 1 (suma de senoidales)
X1 = np.fft.fftshift(np.fft.fft(x1, N))
plt.figure(3)
plt.plot(f, np.abs(X1), label="Espectro de la suma de senoidales")
plt.title("Espectro: Suma de senoidales")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.grid(True)
plt.legend()

# Espectro de la señal 2 (concatenación de senoidales)
X2 = np.fft.fftshift(np.fft.fft(x2, N))
plt.figure(4)
plt.plot(f, np.abs(X2), label="Espectro de las senoidales concatenadas")
plt.title("Espectro: Señales concatenadas")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.grid(True)
plt.legend()

# Espectrograma de la señal 1 (suma de senoidales)
plt.figure(5)
f_spec, t_spec, Sxx = signal.spectrogram(x1, fs=fs, nperseg=20)
plt.pcolormesh(t_spec, f_spec, Sxx, shading='gouraud', cmap=cm.viridis)
plt.title("Espectrograma: Suma de senoidales")
plt.ylabel("Frecuencia (Hz)")
plt.xlabel("Tiempo (s)")
plt.colorbar(label="Densidad de potencia")
plt.grid(True)

# Espectrograma de la señal 2 (concatenación de senoidales)
plt.figure(6)
f_spec2, t_spec2, Sxx2 = signal.spectrogram(x2, fs=fs, nperseg=20)
plt.pcolormesh(t_spec2, f_spec2, Sxx2, shading='gouraud', cmap=cm.viridis)
plt.title("Espectrograma: Señales concatenadas")
plt.ylabel("Frecuencia (Hz)")
plt.xlabel("Tiempo (s)")
plt.colorbar(label="Densidad de potencia")
plt.grid(True)

# Visualización 3D del espectrograma de la señal concatenada
fig = plt.figure(7)
ax = fig.add_subplot(111, projection='3d')
T, F = np.meshgrid(t_spec2, f_spec2)
surf = ax.plot_surface(T, F, Sxx2, cmap=cm.coolwarm)
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Frecuencia (Hz)")
ax.set_zlabel("Densidad de potencia")
fig.colorbar(surf, ax=ax, aspect=5)
plt.title("Espectrograma 3D: Señales concatenadas")

# Mostrar todas las gráficas
plt.show()