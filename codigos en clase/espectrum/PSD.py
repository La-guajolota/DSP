import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# Parámetros de la señal
f0 = 100      # Frecuencia de la señal (Hz)
fs = 1000     # Frecuencia de muestreo (Hz)
N = 1024      # Número de muestras
n = np.arange(N)
x = np.cos(2 * np.pi * f0 * n / fs)

# 1) Periodograma simple (FFT + escalado)
Nfft = 2048   # Zero-padding para mejor densidad de bins
X = np.fft.fft(x, Nfft)
f = np.fft.fftfreq(Nfft, 1/fs)
Sxx_period = (1/(fs*N)) * np.abs(X)**2
f_pos = f[:Nfft//2]
Sxx_period = Sxx_period[:Nfft//2]

# 2) Método de Welch
#    Segmentos de 256 muestras, 50% overlap, ventana Hann
f_welch, Sxx_welch = welch(x, fs=fs, window='hann', nperseg=256, noverlap=128, nfft=Nfft, scaling='density')

# 3) Cálculo de potencia: integrar PSD
power_period = np.trapz(Sxx_period, f_pos)
power_welch = np.trapz(Sxx_welch, f_welch)
power_time = np.mean(x**2)

print(f"Potencia vía promedio en tiempo: {power_time:.4f}")
print(f"Potencia integrando PSD (Periodograma): {power_period:.4f}")
print(f"Potencia integrando PSD (Welch):      {power_welch:.4f}")

# —— Gráficas ——————————————————————————————————————————

plt.figure(figsize=(10, 5))
plt.semilogy(f_pos, Sxx_period, label='Periodograma')
plt.semilogy(f_welch, Sxx_welch, label='Welch (Hann, 256, 50%)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('PSD [V²/Hz]')
plt.title('Comparación de PSD: Periodograma vs. Welch')
plt.grid(True, which='both', ls='--')
plt.legend()
plt.tight_layout()
plt.show()
