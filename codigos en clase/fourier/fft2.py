import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift

a = 0.8
N = 100
fft_size = 1024

omega = np.linspace(-np.pi, np.pi, fft_size)

# Generamos la señal Exponecial
n = np.arange(N)
signal = a ** n

X = fftshift(fft(signal, fft_size)) # Señal en el dominio de la frecuencia
X_cal = 1/(1 - a * np.exp(-1j * omega)) # Calculo de la transformada de Fourier a mano

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
# Graficamos la señal en el dominio del tiempo
ax1.stem(n, signal, basefmt="b-")
ax1.set_title("Señal en el dominio del tiempo")
ax1.set_xlabel("Tiempo (n)")
ax1.set_ylabel("Amplitud")
# Graficamos la transformada de Fourier analítica
ax2.plot(omega, np.abs(X_cal), color="r", label="Calculada")
ax2.plot(omega, np.abs(X)/np.max(np.abs(X)), color="g", label="FFT Normalizada")
ax2.set_title("Transformada de Fourier")
ax2.set_xlabel("Frecuencia (rad)")
ax2.set_ylabel("Amplitud")
plt.legend()
plt.tight_layout()
plt.show()