import numpy as np 
import matplotlib.pyplot as plt

# Señales
fs = 512
t = np.arange(0, 1, 1/fs)  # Vector de tiempo
x = np.sin(2 * np.pi * 100 * t) + np.sin(2 * np.pi * 104 * t)  # Señal compuesta

# Ventanas
n = len(x)
hamming_window = np.hamming(n)
hanning_window = np.hanning(n)
blackman_window = np.blackman(n)

# Aplicar ventanas
x_hamming = x * hamming_window
x_hanning = x * hanning_window
x_blackman = x * blackman_window

# FFT
X_hamming = np.fft.fft(x_hamming)
X_hanning = np.fft.fft(x_hanning)
X_blackman = np.fft.fft(x_blackman)

# Frecuencias
f = np.fft.fftfreq(n, 1/fs)
f = np.fft.fftshift(f)  # Desplazar el cero al centro
X_hamming = np.fft.fftshift(X_hamming)
X_hanning = np.fft.fftshift(X_hanning)
X_blackman = np.fft.fftshift(X_blackman)

# Graficar resultados 
# Graficar la señal original
plt.figure(figsize=(12, 8))
plt.subplot(4, 1, 1)
plt.plot(t, x)
plt.title("Señal Original")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.tight_layout()

## Ventanas
# Graficar la señal con ventana Hamming
plt.subplot(4, 1, 2)
plt.plot(t, x_hamming)
plt.title("Señal con Ventana Hamming")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.tight_layout()
# Graficar la señal con ventana Hanning
plt.subplot(4, 1, 3)
plt.plot(t, x_hanning)
plt.title("Señal con Ventana Hanning")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.tight_layout()
# Graficar la señal con ventana Blackman
plt.subplot(4, 1, 4)
plt.plot(t, x_blackman)
plt.title("Señal con Ventana Blackman")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.tight_layout()
plt.show()

## Graficar la FFT
# Graficar la magnitud de la FFT Hamming
plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(f, np.abs(X_hamming))
plt.title("FFT con Ventana Hamming")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.grid()
plt.tight_layout()
# Graficar la magnitud de la FFT Hanning
plt.subplot(3, 1, 2)
plt.plot(f, np.abs(X_hanning))
plt.title("FFT con Ventana Hanning")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.grid()
plt.tight_layout()
# Graficar la magnitud de la FFT Blackman
plt.subplot(3, 1, 3)
plt.plot(f, np.abs(X_blackman))
plt.title("FFT con Ventana Blackman")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.grid()
plt.tight_layout()
plt.show()


