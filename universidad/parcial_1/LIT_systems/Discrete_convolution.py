"""
Autor: Adrian Silva Palafox
Fecha: MArzo 9 2025

Este script realiza la convolución discreta de dos señales utilizando dos métodos: uno manual y otro nativo de numpy. 
Además, grafica las señales de entrada, la respuesta al impulso y el resultado de la convolución.

Funciones:
-----------
conv(hn, xn):
    Realiza la convolución discreta de dos señales de manera manual.
    Parámetros:
        hn (numpy array): Respuesta al impulso del sistema.
        xn (numpy array): Señal de entrada.
    Retorno:
        None

conv_nativo(hn, xn):
    Realiza la convolución discreta de dos señales utilizando la función nativa de numpy.
    Parámetros:
        hn (numpy array): Respuesta al impulso del sistema.
        xn (numpy array): Señal de entrada.
    Retorno:
        None

Uso:
----
Al ejecutar el script, se graficarán las señales de entrada, la respuesta al impulso y el resultado de la convolución.
"""

import numpy as np
import matplotlib.pyplot as plt

def conv(hn, xn):
    """
    Realiza la convolución discreta de dos señales de manera manual.
    """
    # Inicializamos la señal de salida con ceros
    yn = np.zeros(len(xn) + len(hn) - 1)

    # Realizamos la convolución discreta de manera manual
    for n in range(len(yn)):  # Para cada término de yn
        for i in range(len(hn)):  # Suma-sigma de i=0 a i=n
            if n - i >= 0 and n - i < len(hn):  # Verificamos que los índices sean válidos
                yn[n] += hn[n - i] * xn[i]

    # Graficamos la señal de salida
    plt.stem(yn)
    plt.title('Convolución Discreta')
    plt.xlabel('n')
    plt.ylabel('y[n]')
    plt.show()

def conv_nativo(hn, xn):
    """
    Realiza la convolución discreta de dos señales utilizando la función nativa de numpy.
    """
    # Utilizamos la función de convolución nativa de numpy
    yn = np.convolve(hn, xn)

    print(yn)

    # Graficamos la señal de salida
    plt.stem(yn)
    plt.title('Convolución Discreta (Nativa)')
    plt.xlabel('n')
    plt.ylabel('y[n]')
    plt.show()

if __name__ == "__main__":
    # Respuesta al impulso de algún sistema LIT
    #hn = np.array([1, -2, 3, -1, 2])
    hn = np.array([1,1,1])
    # Señal de entrada
    #xn = np.array([-2, 2, 1, 0, 3])
    xn = np.array([0.5,2,0])

    conv(hn, xn)

    conv_nativo(hn, xn)