import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift
from scipy import signal

# Parámetros
fs = 1  # Frecuencia de muestreo (arbitraria para ventanas)
N = 100  # Número de muestras de las ventanas

# Generación de ventanas
x1 = signal.windows.blackman(N)
x2 = signal.windows.hamming(N)
x3 = signal.windows.hann(N)
x4 = np.ones(N)  # Ventana rectangular

# Gráfica de las ventanas en el dominio del tiempo
plt.figure(1)
plt.plot(x1, label='Blackman')
plt.plot(x2, label='Hamming')
plt.plot(x3, label='Hann')
plt.plot(x4, label='Rectangular')
plt.title('Ventanas en el dominio del tiempo')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.legend()
plt.grid()
plt.show()

# FFT de las ventanas
N1 = 10000  # Número de puntos para la FFT (zero-padding para mayor resolución)
f = np.arange(-N1//2, N1//2) * fs / N1  # Vector de frecuencias
X1 = fftshift(fft(x1, N1))
X2 = fftshift(fft(x2, N1))
X3 = fftshift(fft(x3, N1))
X4 = fftshift(fft(x4, N1))

# Gráfica de los espectros de las ventanas en dB
plt.figure(2)
plt.plot(f, 20 * np.log10(np.abs(X1) / np.max(np.abs(X1))), label='Blackman')
plt.plot(f, 20 * np.log10(np.abs(X2) / np.max(np.abs(X2))), label='Hamming')
plt.plot(f, 20 * np.log10(np.abs(X3) / np.max(np.abs(X3))), label='Hann')
plt.plot(f, 20 * np.log10(np.abs(X4) / np.max(np.abs(X4))), label='Rectangular')
plt.title('Espectros de las ventanas (dB)')
plt.xlabel('Frecuencia normalizada')
plt.ylabel('Magnitud (dB)')
plt.legend()
plt.grid()
plt.show()