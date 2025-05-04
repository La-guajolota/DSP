import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
Fs = 1000          # Frecuencia de muestreo en Hz
T = 1 / Fs         # Intervalo de muestreo
t = np.arange(0, 1, T)  # Vector de tiempo de 1 segundo

# Generamos una señal: por ejemplo, una onda sinusoidal de 50 Hz
f = 50             # Frecuencia de la señal en Hz
signal = np.cos(2 * np.pi * f * t)

# Calculamos la transformada de Fourier de la señal
fft_signal = np.fft.fft(signal)

# Generamos el eje de frecuencias
N = len(signal)
freq = np.fft.fftfreq(N, d=T)

# Solo se muestran las frecuencias positivas
half_N = N // 2

# Graficamos la señal original y su transformada de Fourier
plt.figure(figsize=(12, 5))

# Señal en el dominio del tiempo
plt.subplot(1, 2, 1)
plt.plot(t, signal)
plt.title("Señal en el dominio del tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")

# Magnitud de la transformada de Fourier
plt.subplot(1, 2, 2)
plt.plot(freq[:half_N], np.abs(fft_signal)[:half_N])
plt.title("Transformada de Fourier")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")

plt.tight_layout()
plt.show()
