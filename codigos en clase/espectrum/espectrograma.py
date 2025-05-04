import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy import signal

fs = 20
f0 = 1
f1 = 5

n = np.arange(0, 199)
n2 = np.arrange(0, 99)

seno0 = np.sin(2*np.pi*(f0/fs)*n)
seno1 = np.sin(2*np.pi*(f1/fs)*n)
x1 = seno0 + seno1
x2 = np.concatenate(seno0,seno1)

X = 1000
f=np.arange((-N/2,N/2)*fs/N)
Y1 = np.fft.fftshift(np.fft.fft(x1, X))
Y2 = np.fft.fftshift(np.fft.fft(x2, X))
