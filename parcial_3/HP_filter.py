"""
Diseño de un filtro FIR pasa-altas utilizando:
1. Respuesta al impulso ideal de un filtro pasa-altas.
2. Ventana de Blackman para suavizar la respuesta en frecuencia.
3. Cálculo de la respuesta en frecuencia del filtro diseñado.

El filtro se diseña con los siguientes parámetros:
- Longitud del filtro (M): Debe ser impar para garantizar simetría.
- Frecuencia de corte (wc): Normalizada a π rad/muestra.

Se grafican:
1. La respuesta al impulso del filtro.
2. La respuesta en frecuencia en escala logarítmica (dB).

Finalmente, se guarda la gráfica de la respuesta en frecuencia como una imagen.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parámetros del filtro
M = 61  # Longitud del filtro (debe ser impar para garantizar simetría)
wc = 0.5 * np.pi  # Frecuencia de corte en radianes (normalizada a π rad/muestra)

# Generación del vector de índices 'n'
n = np.arange(-(M-1)//2, (M-1)//2 + 1)

# Cálculo de la respuesta al impulso ideal del filtro pasa-altas
h_ideal = -(wc / np.pi) * np.sinc(wc / np.pi * n)  # Filtro pasa-bajas invertido
h_ideal[(M-1)//2] += 1  # Ajuste en el centro para convertirlo en pasa-altas

# Aplicación de la ventana de Blackman para suavizar la respuesta
black_window = np.blackman(M)  # Ventana de Blackman
h_trunc = h_ideal * black_window  # Respuesta al impulso truncada

# Cálculo de la respuesta en frecuencia del filtro
w, H = signal.freqz(h_trunc, 1, worN=1024)  # Respuesta en frecuencia
w_norm = w / np.pi  # Frecuencia normalizada (0 a 1)
h_mag = np.abs(H)  # Magnitud de la respuesta en frecuencia
h_db = 20 * np.log10(h_mag + 1e-10)  # Magnitud en dB (evitando log(0) con un offset pequeño)

# Gráfica de la respuesta al impulso
plt.figure(figsize=(10, 6))
plt.stem(n, h_trunc, basefmt=" ")
plt.title('Respuesta al Impulso del Filtro Pasa-Altas', fontsize=14)
plt.xlabel('Índice (n)', fontsize=12)
plt.ylabel('Amplitud', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Gráfica de la respuesta en frecuencia
plt.figure(figsize=(10, 6))
plt.plot(w_norm, h_db, label='Respuesta en Frecuencia', color='blue', linewidth=1.5)
plt.title('Respuesta en Frecuencia del Filtro Pasa-Altas', fontsize=14)
plt.xlabel('Frecuencia Normalizada (×π rad/muestra)', fontsize=12)
plt.ylabel('Magnitud (dB)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(0, color='black', lw=0.5, ls='--', label='Referencia 0 dB')  # Línea de referencia en 0 dB
plt.axvline(0.5, color='red', lw=0.8, ls='--', label='Frecuencia de Corte (0.5π)')
plt.legend(fontsize=10)
plt.xlim(0, 1)  # Limitar el eje x de 0 a 1 (frecuencia normalizada)
plt.ylim(-100, 5)  # Limitar el eje y de -100 dB a 5 dB
plt.xticks(np.arange(0, 1.1, 0.1))  # Marcas en el eje x cada 0.1
plt.yticks(np.arange(-100, 6, 10))  # Marcas en el eje y cada 10 dB
plt.tight_layout()
plt.show()

# Información adicional
print("Filtro diseñado con los siguientes parámetros:")
print(f"- Longitud del filtro (M): {M}")
print(f"- Frecuencia de corte (wc): {wc/np.pi:.2f}π rad/muestra")
print(f"- Ventana utilizada: Blackman")

#Crear una señal de prueba
n1 = np.arange(0, 300)
w0 = 0.2 * np.pi
xn = np.cos(w0 * n1) 

# Filtrar la señal convolución
yn = np.convolve(xn, h_trunc, mode='full')
yn = yn[:len(xn)]  # Ajustar la longitud de la señal filtrada

# Graficar la señal original y la señal filtrada
plt.figure(figsize=(10, 6))
plt.plot(n1, xn, label='Señal Original', color='blue', linewidth=1.5)
plt.plot(n1, yn, label='Señal Filtrada', color='red', linewidth=1.5)
plt.title('Señal Original y Filtrada', fontsize=14)
plt.xlabel('Índice (n)', fontsize=12)
plt.ylabel('Amplitud', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()
# Información sobre la señal filtrada
print("Señal filtrada con el filtro pasa-altas:")
print(f"- Longitud de la señal original: {len(xn)}")
print(f"- Longitud de la señal filtrada: {len(yn)}")
print(f"- Frecuencia de muestreo: 1 muestra por unidad de tiempo")
print(f"- Frecuencia de corte del filtro: {wc/np.pi:.2f}π rad/muestra")
print(f"- Frecuencia de la señal original: {w0/np.pi:.2f}π rad/muestra")

# FIltrar con la funcion filtf de scipy
yn1 = signal.lfilter(h_trunc, 1, xn)  # Filtrar la señal utilizando la función filtf
yn1 = yn1[:len(xn)]  # Ajustar la longitud de la señal filtrada
# Graficar la señal original y la señal filtrada
plt.figure(figsize=(10, 6))
plt.plot(n1, xn, label='Señal Original', color='blue', linewidth=1.5)
plt.plot(n1, yn1, label='Señal Filtrada', color='red', linewidth=1.5)
plt.title('Señal Original y Filtrada (con filtf)', fontsize=14)
plt.xlabel('Índice (n)', fontsize=12)
plt.ylabel('Amplitud', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()
# Información sobre la señal filtrada
print("Señal filtrada con el filtro pasa-altas (con filtf):")
print(f"- Longitud de la señal original: {len(xn)}")
print(f"- Longitud de la señal filtrada: {len(yn1)}")
print(f"- Frecuencia de muestreo: 1 muestra por unidad de tiempo")
print(f"- Frecuencia de corte del filtro: {wc/np.pi:.2f}π rad/muestra")
print(f"- Frecuencia de la señal original: {w0/np.pi:.2f}π rad/muestra")
