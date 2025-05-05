import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy import signal

# Parámetros de las señales
f0 = 2   # Frecuencia de la primera señal (Hz)
f1 = 20   # Frecuencia de la segunda señal (Hz)
fs = f1*10 # Frecuencia de muestreo (Hz)

# Vector de tiempo discreto
n = np.arange(0, 3, 1/fs)  # 3 segundos de duración con pasos de 1/fs

# Generar las señales seno
seno0 = np.sin(2 * np.pi * f0 * n)
seno1 = np.sin(2 * np.pi * f1 * n)

# Señal sumada
x1 = seno0 + seno1

# Señal concatenada
x2 = np.concatenate((seno0, seno1))
n2 = np.arange(0, len(x2)) / fs  # Nuevo vector de tiempo para la señal concatenada

# FFT de las señales
X = 1024  # Número de puntos para la FFT
Y1 = np.fft.fftshift(np.fft.fft(x1, X))
Y2 = np.fft.fftshift(np.fft.fft(x2, X))
freqs = np.fft.fftshift(np.fft.fftfreq(X, 1/fs))  # Vector de frecuencias

# Gráfica de la señal sumada
plt.figure(figsize=(10, 5))
plt.plot(n, x1, label="Señal Sumada")
plt.title("Señal Sumada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()
plt.show()

# Gráfica de la señal concatenada
plt.figure(figsize=(10, 5))
plt.plot(n2, x2, label="Señal Concatenada")
plt.title("Señal Concatenada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()
plt.show()

# Gráfica de la FFT de la señal sumada
plt.figure(figsize=(10, 5))
plt.plot(freqs, np.abs(Y1) / np.max(np.abs(Y1)), label="FFT Señal Sumada")  # Normalizada
plt.title("FFT de la Señal Sumada")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud Normalizada")
plt.grid()
plt.legend()
plt.show()

# Gráfica de la FFT de la señal concatenada
plt.figure(figsize=(10, 5))
plt.plot(freqs, np.abs(Y2) / np.max(np.abs(Y2)), label="FFT Señal Concatenada")  # Normalizada
plt.title("FFT de la Señal Concatenada")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud Normalizada")
plt.grid()
plt.legend()
plt.show()

# Gráfica del espectrograma de la señal sumada
plt.figure(figsize=(10, 5))
plt.specgram(x1, Fs=fs, NFFT=256, noverlap=128, cmap=cm.viridis)  # Ajuste de NFFT y noverlap
plt.title("Espectrograma de la Señal Sumada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Frecuencia (Hz)")
plt.colorbar(label="Magnitud")
plt.grid()
plt.show()

# Gráfica del espectrograma de la señal concatenada
plt.figure(figsize=(10, 5))
plt.specgram(x2, Fs=fs, NFFT=256, noverlap=128, cmap=cm.viridis)  # Ajuste de NFFT y noverlap
plt.title("Espectrograma de la Señal Concatenada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Frecuencia (Hz)")
plt.colorbar(label="Magnitud")
plt.grid()
plt.show()