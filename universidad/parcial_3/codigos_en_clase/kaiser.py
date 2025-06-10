"""
Diseño de un filtro FIR pasa-bajas utilizando la ventana de Kaiser.
1. Se calcula la respuesta al impulso ideal del filtro pasa-bajas.
2. Se aplica la ventana de Kaiser para suavizar la respuesta en frecuencia.
3. Se calcula la respuesta en frecuencia del filtro diseñado.
4. Se filtra una señal senoidal de prueba utilizando dos métodos:
   - Convolución directa.
   - Función `lfilter` de SciPy.

Se grafican:
1. La respuesta al impulso truncada por la ventana.
2. La respuesta en frecuencia en escala lineal y en decibeles.
3. La señal filtrada utilizando ambos métodos.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.fftpack as fft

# Parámetros del filtro
M = 14  # Longitud del filtro (debe ser impar para garantizar simetría)
beta = 3.3  # Parámetro de la ventana de Kaiser
wc = 0.45 * np.pi  # Frecuencia de corte normalizada (en radianes)

# Generación del vector de índices 'n'
n = np.arange(-M//2, M//2+1)

# Cálculo de la respuesta al impulso ideal del filtro pasa-bajas
hn = (wc / np.pi) * np.sinc(wc * n / np.pi)

# Aplicar la ventana de Kaiser
kaiser_window = signal.windows.kaiser(M+1, beta)  # Ventana de Kaiser
hn1 = hn * kaiser_window  # Respuesta al impulso truncada

# Gráfica de la respuesta al impulso truncada
plt.figure(1)
plt.stem(n, hn1, basefmt=" ")
plt.title('Respuesta al Impulso Truncada por Ventana de Kaiser')
plt.xlabel('Índice (n)')
plt.ylabel('Amplitud')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Cálculo de la respuesta en frecuencia del filtro
N1 = 10000  # Número de puntos para la FFT
H1jw = np.fft.fftshift(np.abs(np.fft.fft(hn1, N1)))
w = np.linspace(-np.pi, np.pi, N1, endpoint=False)

# Gráfica de la respuesta en frecuencia (escala lineal)
plt.figure(2)
plt.plot(w / np.pi, H1jw, label='Escala Lineal')
plt.title('Respuesta en Frecuencia (Escala Lineal)')
plt.xlabel('Frecuencia Normalizada (×π rad/muestra)')
plt.ylabel('Magnitud')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Gráfica de la respuesta en frecuencia (escala en dB)
plt.figure(3)
plt.plot(w / np.pi, 20 * np.log10(H1jw + 1e-10), label='Escala en dB', color='red')
plt.title('Respuesta en Frecuencia (Escala en dB)')
plt.xlabel('Frecuencia Normalizada (×π rad/muestra)')
plt.ylabel('Magnitud (dB)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Creación de la señal de prueba
n1 = np.arange(0, 300)  # Vector de tiempo discreto
w0 = 0.7 * np.pi  # Frecuencia de la señal de prueba
xn = np.cos(w0 * n1)  # Señal senoidal

# Filtrar la señal utilizando convolución directa
yn = np.convolve(xn, hn1, mode='full')
yn = yn[:len(xn)]  # Ajustar la longitud de la señal filtrada

# Gráfica de la señal filtrada con convolución
plt.figure(4)
plt.plot(yn, 'r', label='Filtrada con Convolución')
plt.title('Señal Filtrada con Convolución')
plt.xlabel('Índice (n)')
plt.ylabel('Amplitud')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Filtrar la señal utilizando lfilter
yn1 = signal.lfilter(hn1, 1, xn)

# Gráfica de la señal filtrada con lfilter
plt.figure(5)
plt.plot(yn1, 'b', label='Filtrada con lfilter')
plt.title('Señal Filtrada con lfilter')
plt.xlabel('Índice (n)')
plt.ylabel('Amplitud')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar todas las gráficas
plt.show()