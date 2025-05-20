import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.fftpack as fft

# Limpieza (equivalente a 'clear all' en MATLAB)
plt.close('all')

# Parámetros del filtro
M_1 = 60  # Orden del filtro M-1
n = np.arange(-M_1//2, M_1//2+1)  # Vector de índices centrado en cero

# Respuesta al impulso de un filtro paso-altas ideal
wc = 0.5 * np.pi  # Frecuencia de corte
# Fórmula del paso-altas (invirtiendo el signo del paso-bajas)
hn = -(wc/np.pi) * np.sinc(wc * n / np.pi)
# Suma del impulso en cero (añadir 1 en el centro para el paso-altas)
hn[M_1//2] = hn[M_1//2] + 1

# Aplicación de la ventana de Blackman
# (En el código original se usa hanning pero el título menciona Blackman)
hn1 = hn * np.blackman(M_1+1)

# Graficar la respuesta al impulso
plt.figure(1)
plt.stem(n, hn1, use_line_collection=True)
plt.title('Respuesta al impulso truncada x ventana')
plt.xlabel('n [muestra]')
plt.grid(True)

# Calcular la respuesta en frecuencia H(w)
N1 = 10000
# Calcular la FFT y centrarla
H1jw = np.fft.fftshift(np.abs(np.fft.fft(hn1, N1)))
w = np.linspace(-np.pi, np.pi, N1, endpoint=False)

# Graficar la respuesta en frecuencia (escala lineal)
plt.figure(2)
plt.plot(w/np.pi, H1jw)
plt.grid(True)
plt.title('Respuesta en frecuencia')
plt.xlabel('w/pi [rad/s]')

# Graficar la respuesta en frecuencia (escala en dB)
plt.figure(3)
plt.plot(w/np.pi, 20*np.log10(H1jw))
plt.grid(True)
plt.title('Respuesta en frecuencia en dB')
plt.xlabel('w/pi [rad/s]')

# Crear señal senoidal de prueba
n1 = np.arange(0, 300)
w0 = 0.2 * np.pi
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

# Filtrar la señal utilizando la función filter (implementación directa)
yn1 = signal.lfilter(hn1, 1, xn)

# Graficar la señal filtrada con filter
plt.figure(5)
plt.plot(yn1, 'b')
plt.title('señal senoidal filtrada con filter')
plt.xlabel('n [muestra]')

plt.show()
