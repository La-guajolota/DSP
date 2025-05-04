import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ffshift

fs = 1
N = 100
x1 = signal.windows.blackman(N)
x2 = signal.windows.hamming(N)
x3 = signal.windows.hann(N)
x4 = np.ones(N)

plt.figure(1)
plt.plot(x1, label='Blackman')
plt.plot(x2, label='Hamming')
plt.plot(x3, label='Hann')
plt.plot(x4, label='Rectangular')
plt.title('Ventanas')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.legend()
plt.grid()
plt.show()

N1 = 10000
f = np.arange(-N1//2, N1//2, 1) * fs/N1
X1 = fftshift(fft(x1, N1))
X2 = fftshift(fft(x2, N1))
X3 = fftshift(fft(x3, N1))
X4 = fftshift(fft(x4, N1))

plt.figure(2)
plt.plot(f,20*np.log10(np.abs(x1)/np.max(x1)),label='')
plt.plot(f,20*np.log10(np.abs(x1)/np.max(x1)),label='')
plt.plot(f,20*np.log10(np.abs(x1)/np.max(x1)),label='')
plt.plot(f,20*np.log10(np.abs(x1)/np.max(x1)),label='')
plt.plot(f,20*np.log10(np.abs(x1)/np.max(x1)),label='')
plt.show()
