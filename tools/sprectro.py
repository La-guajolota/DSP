from dft import dft
import matplotlib.pyplot as plt
import numpy as np

# signal
freq = 1  # Frecuencia de la onda sinusoidal
signal_duration = 10  # Duración de la señal en segundos
fs = freq * 10  # Frecuencia de muestreo (Hz)
Ts = np.arange(0, signal_duration, 1/fs)  # Vector de tiempo

x = np.array([np.sin(2 * np.pi * freq * t) + np.cos(2 * np.pi * freq/3 * t) for t in Ts])  # Genera una onda sinusoidal como array
#x = 0.8 ** Ts # Genera una señal exponencial

def main():
    """
    Este programa genera una señal compuesta por una suma de una onda sinusoidal y una cosenoidal,
    calcula su Transformada Discreta de Fourier (DFT) y grafica la magnitud y la fase de la DFT.
    """
    # Calcula la DFT de la señal
    X = dft(list(x))
    
    # Magnitud y fase
    magnitude = np.abs(X)
    phase = np.angle(X)

    # Vector de frecuencias
    freqs = [0] * len(X)
    for k in range(len(X)):
        freqs[k] = (k * fs) / len(X)

    # Grafica la señal original
    plt.figure(figsize=(10, 5))
    plt.plot(Ts, x, label="Señal Original")
    plt.title("Señal Original")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid()
    plt.legend()
    plt.show()

    # Grafica la magnitud
    plt.figure(figsize=(10, 5))
    plt.plot(freqs[:len(freqs)//2], magnitude[:len(magnitude)//2])
    plt.title("Magnitud de la DFT")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Magnitud")
    plt.show()

    # Grafica la fase
    plt.figure(figsize=(10, 5))
    plt.plot(freqs[:len(freqs)//2], phase[:len(phase)//2])
    plt.title("Fase de la DFT")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Fase (radianes)")
    plt.show()

if __name__ == "__main__":
    main()
