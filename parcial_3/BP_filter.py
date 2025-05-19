import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parámetros del filtro de la imagen
fs = 5000  # Frecuencia de muestreo en Hz
M = 67     # Longitud del filtro (elegimos un número impar grande para mejor resolución)

# Bandas de transición
f1_1 = 300   # Hz - Primera banda de transición, inicio
f1_2 = 600   # Hz - Primera banda de transición, fin
f2_1 = 1500  # Hz - Segunda banda de transición, inicio
f2_2 = 1800  # Hz - Segunda banda de transición, fin (calculado como f2_1 + 300Hz)

# Atenuaciones
delta_1 = 0.1   # Rizado en banda de paso (amplitud)
delta_2 = 0.01  # Atenuación en banda de rechazo (amplitud)

# Convertir frecuencias a frecuencias normalizadas (0 a 1, donde 1 es fs/2)
w1_1 = f1_1 / (fs/2)
w1_2 = f1_2 / (fs/2)
w2_1 = f2_1 / (fs/2)
w2_2 = f2_2 / (fs/2)

# Frecuencias de corte para el diseño del filtro (centro de las bandas de transición)
wc1 = (w1_1 + w1_2) / 2  # Primera frecuencia de corte normalizada
wc2 = (w2_1 + w2_2) / 2  # Segunda frecuencia de corte normalizada

# Generación del vector de índices 'n'
n = np.arange(-(M-1)//2, (M-1)//2 + 1)

# Cálculo de la respuesta al impulso ideal del filtro pasa-banda
h_ideal = (wc2 * np.sinc(wc2 * n)) - (wc1 * np.sinc(wc1 * n))

# Aplicación de la ventana de hanning para suavizar la respuesta
hanning_window = np.hanning(M)  # Ventana de hanning
h_trunc = h_ideal * hanning_window

# Cálculo de la respuesta en frecuencia del filtro
w, H = signal.freqz(h_trunc, 1, worN=4096)
w_norm = w / np.pi      # Frecuencia normalizada (0 a 1)
w_hz = w_norm * (fs/2)  # Convertir a Hz para la visualización
h_mag = np.abs(H)
h_db = 20 * np.log10(h_mag + 1e-10)  # Magnitud en dB (evitando log(0))

# Gráfica de la respuesta al impulso
plt.figure(figsize=(10, 6))
plt.stem(n, h_trunc, basefmt=" ")
plt.title('Respuesta al Impulso del Filtro Pasa-Banda', fontsize=14)
plt.xlabel('Índice (n)', fontsize=12)
plt.ylabel('Amplitud', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Gráfica de la respuesta en frecuencia en Hz
plt.figure(figsize=(12, 8))
plt.plot(w_hz, h_db, label='Respuesta en Frecuencia', color='blue', linewidth=1.5)
plt.title('Respuesta en Frecuencia del Filtro Pasa-Banda', fontsize=14)
plt.xlabel('Frecuencia (Hz)', fontsize=12)
plt.ylabel('Magnitud (dB)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Añadir líneas para las bandas de transición
plt.axvline(f1_1, color='red', lw=0.8, ls='--', label='Banda de Transición 1')
plt.axvline(f1_2, color='red', lw=0.8, ls='--')
plt.axvline(f2_1, color='green', lw=0.8, ls='--', label='Banda de Transición 2')
plt.axvline(f2_2, color='green', lw=0.8, ls='--')

# Añadir líneas para las atenuaciones
plt.axhline(20*np.log10(1-delta_1), color='purple', lw=0.8, ls=':', label=f'Banda de Paso (1-δ1): {1-delta_1}')
plt.axhline(20*np.log10(1+delta_1), color='purple', lw=0.8, ls=':')
plt.axhline(20*np.log10(delta_2), color='orange', lw=0.8, ls=':', label=f'Banda de Rechazo (δ2): {delta_2}')

plt.legend(fontsize=10, loc='lower center')
plt.xlim(0, fs/2)  # Limitar el eje x de 0 a fs/2
plt.ylim(-60, 5)  # Limitar el eje y
plt.tight_layout()
plt.show()

# Gráfica de la respuesta en frecuencia normalizada (como en la imagen)
plt.figure(figsize=(12, 8))
plt.plot(w_norm, h_mag, label='Respuesta en Frecuencia', color='blue', linewidth=1.5)
plt.title('Respuesta en Frecuencia del Filtro Pasa-Banda (Normalizada)', fontsize=14)
plt.xlabel('Frecuencia Normalizada (×π rad/muestra)', fontsize=12)
plt.ylabel('Magnitud', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Añadir líneas para las bandas de transición
plt.axvline(w1_1, color='red', lw=0.8, ls='--', label='Banda de Transición 1')
plt.axvline(w1_2, color='red', lw=0.8, ls='--')
plt.axvline(w2_1, color='green', lw=0.8, ls='--', label='Banda de Transición 2')
plt.axvline(w2_2, color='green', lw=0.8, ls='--')

# Añadir líneas para las atenuaciones
plt.axhline(1-delta_1, color='purple', lw=0.8, ls=':', label=f'Banda de Paso (1-δ1): {1-delta_1}')
plt.axhline(1+delta_1, color='purple', lw=0.8, ls=':')
plt.axhline(delta_2, color='orange', lw=0.8, ls=':', label=f'Banda de Rechazo (δ2): {delta_2}')

plt.legend(fontsize=10, loc='upper right')
plt.xlim(0, 1)  # Limitar el eje x de 0 a 1
plt.ylim(0, 1.2)  # Limitar el eje y
plt.tight_layout()
plt.show()

# Crear una señal de prueba con componentes en diferentes frecuencias
t = np.arange(0, 1, 1/fs)  # 1 segundo de duración
# Crear señal con componentes en banda de rechazo y en banda de paso
x = (np.sin(2*np.pi*200*t) +  # componente en banda de rechazo
     np.sin(2*np.pi*1000*t) +  # componente en banda de paso
     np.sin(2*np.pi*2000*t))   # componente en banda de rechazo

# Filtrar la señal 
y = signal.lfilter(h_trunc, 1, x)

# Graficar las señales en el tiempo
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(t[:500], x[:500], label='Señal Original')
plt.title('Señal Original (Primeras 500 muestras)', fontsize=14)
plt.xlabel('Tiempo (s)', fontsize=12)
plt.ylabel('Amplitud', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t[:500], y[:500], label='Señal Filtrada', color='red')
plt.title('Señal Filtrada (Primeras 500 muestras)', fontsize=14)
plt.xlabel('Tiempo (s)', fontsize=12)
plt.ylabel('Amplitud', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# Calcular y mostrar los espectros
N_fft = 8192
freq = np.fft.rfftfreq(N_fft, 1/fs)
X = np.fft.rfft(x, N_fft)
Y = np.fft.rfft(y, N_fft)

plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(freq, 20*np.log10(np.abs(X) + 1e-10))
plt.title('Espectro de la Señal Original', fontsize=14)
plt.xlabel('Frecuencia (Hz)', fontsize=12)
plt.ylabel('Magnitud (dB)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.axvline(f1_1, color='red', lw=0.8, ls='--')
plt.axvline(f1_2, color='red', lw=0.8, ls='--')
plt.axvline(f2_1, color='green', lw=0.8, ls='--')
plt.axvline(f2_2, color='green', lw=0.8, ls='--')
plt.xlim(0, fs/2)
plt.ylim(-60, 60)

plt.subplot(2, 1, 2)
plt.plot(freq, 20*np.log10(np.abs(Y) + 1e-10), color='red')
plt.title('Espectro de la Señal Filtrada', fontsize=14)
plt.xlabel('Frecuencia (Hz)', fontsize=12)
plt.ylabel('Magnitud (dB)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.axvline(f1_1, color='red', lw=0.8, ls='--')
plt.axvline(f1_2, color='red', lw=0.8, ls='--')
plt.axvline(f2_1, color='green', lw=0.8, ls='--')
plt.axvline(f2_2, color='green', lw=0.8, ls='--')
plt.xlim(0, fs/2)
plt.ylim(-60, 60)
plt.tight_layout()
plt.show()

# Información adicional del filtro diseñado
print("Filtro FIR pasa-banda diseñado con los siguientes parámetros:")
print(f"- Longitud del filtro (M): {M}")
print(f"- Frecuencia de muestreo (fs): {fs} Hz")
print(f"- Primera banda de transición: {f1_1} Hz - {f1_2} Hz")
print(f"- Segunda banda de transición: {f2_1} Hz - {f2_2} Hz")
print(f"- Rizado en banda de paso (δ1): {delta_1}")
print(f"- Atenuación en banda de rechazo (δ2): {delta_2}")
print(f"- Ventana utilizada: Blackman")