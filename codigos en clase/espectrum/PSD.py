import numpy as np
import matplotlib.pyplot as plt

f0 = 100
fs = 1000
N = 1000
n = np.arange(0, N)
x = np.cos(2 * np.pi * f0 * n / fs)

N1 = 1000 # Numero de puntos para la TDF
X = np.fft.fft(x, N1) # TDF
Xshift = np.fft.fftshift(X) # Desplazamiento de la TDF
f = np.arange(-N1/2, N1/2) * fs / N1 # Frecuencias  

# Graficar la TDF
plt.figure()
plt.plot(f, np.abs(Xshift))
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud |X(k)|')
plt.title('Magnitud de X(k)')
plt.grid()

#PSP
Sxx = (1/N) * np.abs(Xshift)**2 # PSD
Sxxshift = np.fft.fftshift(Sxx) # Desplazamiento de la PSD
f = np.arange(-N1/2, N1/2) * fs / N1 # Frecuencias
# Graficar la PSD
plt.figure()
plt.plot(f, Sxxshift)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('PSD')
plt.title('Densidad espectral de potencia Sxx(f)')
plt.grid()
plt.show()

# PSD en decibelios
Sxx_dB = 10 * np.log10(Sxxshift)
# Graficar la PSD en decibelios
plt.figure()
plt.plot(f, Sxx_dB)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('PSD (dB)')
plt.title('Densidad espectral de potencia Sxx(f) en dB')
plt.grid()
plt.show()

