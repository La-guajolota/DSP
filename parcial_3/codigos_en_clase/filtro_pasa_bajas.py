import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

M = 27
wc = 0.45* np.pi

n = np.arange(-(M-1)//2, (M-1)//2 + 1)
#paso 2: Calcular la respuesta al impulso ideal
h_ideal = (wc/np.pi) * np.sinc(wc * n / np.pi)

#paso 3: Aplicar la ventana de Hanning
window = np.hanning(M)
h_truncada = h_ideal * window

# Calcular la respuesta en frecuencia
w, H = signal.freqz(h_truncada, 1, worN=1024)
w_normalizada = w / np.pi
H_magnitud = np.abs(H)
H_db = 20 * np.log10(H_magnitud + 1e-10)

plt.figure(1)
plt.stem(n, h_ideal, 'b', markerfmt='bo', label='Ideal')
plt.stem(n, h_truncada, 'r', markerfmt='ro', label='Truncada con ventana')
plt.xlabel('n [muestras]')
plt.ylabel('h[n]')
plt.title('Respuesta al impulso')
plt.legend()
plt.grid(True)

plt.figure(2)
plt.plot(w_normalizada, H_magnitud)
plt.xlabel('w/$\pi$ [rad/s]')
plt.ylabel('|H(e^jw)|')
plt.title('Respuesta en frecuencia (magnitud)')
plt.grid(True)

plt.figure(3)
plt.plot(w_normalizada, H_db)
plt.xlabel('w/$\pi$ [rad/s]')
plt.ylabel('|H(e^jw)| [dB]')
plt.title('Respuesta en frecuencia (dB)')
plt.ylim(-80, 5)
plt.grid(True)

plt.figure(4)
plt.plot(w_normalizada, H_magnitud)
plt.axvline(x=0.3, color='g', linestyle='--', label='wp = 0.3$\pi$')
plt.axvline(x=0.6, color='r', linestyle='--', label='ws = 0.6$\pi$')
plt.axhline(y=0.99, color='b', linestyle=':', label='1-$\delta_1$ = 0.99')
plt.axhline(y=0.01, color='m', linestyle=':', label='$\delta_2$ = 0.01')
plt.xlabel('w/$\pi$ [rad/s]')
plt.ylabel('|H(e^jw)|')
plt.title('Verificación de especificaciones')
plt.legend(loc='best')
plt.grid(True)

plt.tight_layout()
plt.show()
