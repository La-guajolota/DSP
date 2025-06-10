import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.fftpack as fft

# Limpieza (equivalente a 'clear all' en MATLAB)
plt.close('all')

# Respuesta al impulso del primer filtro paso-bajas ideal (wc1)
M = 66
n = np.arange(-M//2, M//2+1)
wc1 = 0.24 * np.pi
hn1 = (wc1/np.pi) * np.sinc(wc1 * n / np.pi)

# Respuesta al impulso del segundo filtro paso-bajas ideal (wc2)
wc2 = 0.6 * np.pi
hn2 = (wc2/np.pi) * np.sinc(wc2 * n / np.pi)

# Respuesta al impulso del filtro paso-banda (resta de los dos filtros paso-bajas)
hn = hn2 - hn1  # Paso-banda = Paso-bajas(wc2) - Paso-bajas(wc1)
hn3 = hn * np.hanning(M+1)  # Aplicar ventana de Hanning

# Graficar la respuesta al impulso
plt.figure(1)
plt.stem(n, hn3, use_line_collection=True)
plt.title('Respuesta al impulso truncada x ventana')
plt.xlabel('n [muestra]')
plt.grid(True)

# Calcular la respuesta en frecuencia H(w)
N1 = 10000
# Calcular la FFT y centrarla
H1jw = np.fft.fftshift(np.abs(np.fft.fft(hn3, N1)))
w = np.linspace(-np.pi, np.pi, N1, endpoint=False)

# Graficar la respuesta en frecuencia (escala lineal)
plt.figure(2)
plt.plot(w/np.pi, H1jw)
plt.grid(True)
plt.title('Respuesta en frecuencia')
plt.xlabel('w/pi [rad/s]')

# Graficar la respuesta en frecuencia (escala en dB)
plt.figure(3)
plt.plot(w/np.pi, 20*np.log10(H1jw + 1e-10))  # Añadir pequeña constante para evitar log(0)
plt.grid(True)
plt.title('Respuesta en frecuencia en dB')
plt.xlabel('w/pi [rad/s]')

# Crear señal senoidal de prueba
n1 = np.arange(0, 300)
w0 = 0.7 * np.pi
xn = np.cos(w0 * n1)

# Filtrar la señal senoidal utilizando convolución
yn = np.convolve(xn, hn1, mode='full')
# Recortar la salida para que tenga la misma longitud que la entrada
yn = yn[:len(xn)]

# Graficar la señal filtrada con convolución
plt.figure(4)
plt.plot(yn, 'r')
plt.title('señal senoidal filtrada con conv')
plt.xlabel('n [muestra]')

# Filtrar la señal utilizando la función filter
yn1 = signal.lfilter(hn1, 1, xn)

# Graficar la señal filtrada con filter
plt.figure(5)
plt.plot(yn1, 'b')
plt.title('señal senoidal filtrada con filter')
plt.xlabel('n [muestra]')

plt.show()
