import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# Generación de señal discreta en el tiempo
f0 = 100
f1 = 110
fs = 1000
N = 1000 # Número de muestras FFT
n = np.arange(N)

#Señales
x = np.cos(2*np.pi*f0/fs*n) + 0.05*np.cos(2*np.pi*f1/fs*n)
#Obtención de la FFT
Xk = fft(x)
f = (n/N)*fs

plt.plot(f, np.abs(Xk))     
plt.title('FFT de la señal')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud $|X\(omega)\|$')
plt.grid()
plt.show()

