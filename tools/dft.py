# Transformada discreta de fourier algoritmo
# Autor: Adrián Silva Palafox
# Fecha: 2025-4-4

import numpy as np
import matplotlib.pyplot as plt

# señal
x = [2,1,0,1,2]
#x = [.5,1,.5]

def dft(x, padding=None):
    """
    Realiza la transformada discreta de Fourier (DFT) de una señal.
    
    Parámetros:
    x (list): Señal de entrada.
    padding (int): Longitud deseada de la señal. Si es None, se ajusta a la longitud de la señal.

    Retorna:
    list: Resultado de la DFT.
    """

    # Longitud de la señal
    N = len(x)
    if padding is None:
        if N & (N - 1) != 0:  # Verifica si N no es potencia de 2
            next_pow2 = 1 << (N - 1).bit_length()
    else:
        next_pow2 = padding

    # Padding para que la longitud sea una potencia de 2
    x += [0] * (next_pow2 - N)
    N = len(x)

    # Inicializar la señal resultante
    X = [0] * N

    # Realizar la DFT
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * (np.e ** (-2j * np.pi * k * n / N))
    
    return X

def main():
    # Realizar la DFT
    X = dft(x, padding=2**4)
    
    # Imprimir el resultado
    print("Resultado de la DFT:", X)
    # Graficar la magnitud de la DFT
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.stem(np.abs(X))
    plt.title("Magnitud de la DFT")
    plt.subplot(2, 1, 2)
    plt.plot(np.angle(X))
    plt.title("Fase de la DFT")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
# Convolución discreta algoritmo