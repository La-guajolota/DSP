import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parámetros del filtro
M = 27  # Longitud del filtro (debe ser impar para garantizar simetría)
wc = 0.45 * np.pi  # Frecuencia de corte en radianes (normalizada a π rad/muestra)

# Generación del vector de índices 'n'
n = np.arange(-(M-1)//2, (M-1)//2 + 1)

# Cálculo de la respuesta al impulso ideal del filtro pasa-bajas
h_ideal = (wc / np.pi) * np.sinc(wc / np.pi * n)

# Aplicación de la ventana de Hamming para suavizar la respuesta
hamming_window = np.hamming(M)
h_trunc = h_ideal * hamming_window

# Cálculo de la respuesta en frecuencia del filtro
w, H = signal.freqz(h_trunc, 1, worN=1024)  # Respuesta en frecuencia
w_norm = w / np.pi  # Frecuencia normalizada (0 a 1)
h_mag = np.abs(H)  # Magnitud de la respuesta en frecuencia
h_db = 20 * np.log10(h_mag + 1e-10)  # Magnitud en dB (evitando log(0) con un offset pequeño)

# Configuración de la gráfica de la respuesta en frecuencia
plt.figure(figsize=(10, 6))
plt.plot(w_norm, h_db, label='Respuesta en Frecuencia', color='blue', linewidth=1.5)
plt.title('Respuesta en Frecuencia del Filtro Pasa-Bajas', fontsize=14)
plt.xlabel('Frecuencia Normalizada (×π rad/muestra)', fontsize=12)
plt.ylabel('Magnitud (dB)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(0, color='black', lw=0.5, ls='--')  # Línea de referencia en 0 dB
plt.axvline(0.45, color='red', lw=0.8, ls='--', label='Frecuencia de Corte (0.45π)')
plt.axvline(0.55, color='green', lw=0.8, ls='--', label='Frecuencia de Banda de Rechazo (0.55π)')
plt.legend(fontsize=10)
plt.xlim(0, 1)  # Limitar el eje x de 0 a 1 (frecuencia normalizada)
plt.ylim(-100, 5)  # Limitar el eje y de -100 dB a 5 dB
plt.xticks(np.arange(0, 1.1, 0.1))  # Marcas en el eje x cada 0.1
plt.yticks(np.arange(-100, 6, 10))  # Marcas en el eje y cada 10 dB
plt.tight_layout()

# Guardar la gráfica como imagen
plt.savefig('PB_filter_response.png', dpi=300)  # Guardar con alta resolución
plt.show()

# Información adicional
print("Filtro diseñado con los siguientes parámetros:")
print(f"- Longitud del filtro (M): {M}")
print(f"- Frecuencia de corte (wc): {wc/np.pi:.2f}π rad/muestra")
print(f"- Ventana utilizada: Hamming")

