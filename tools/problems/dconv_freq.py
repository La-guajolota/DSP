# Autor: Adrián Silva Palafox
# Fecha: 2025-4-4
"""
Dado el problema:
Dada una señal discreta x[n] = {2,1,0,1,2} y un filtro h[n] = {0.5,1,0.5}:

Calcule manualmente la convolución discreta y[n] = x[n] * h[n].
Calcule la DFT de x[n], h[n] y y[n] verificando la propiedad de convolución en el dominio temporal y
multiplicación en el dominio frecuencia
"""

from tools.dconv import dconv
from tools.dft import dft
import numpy as np
import matplotlib.pyplot as plt

# señal de entrada
x = [2, 1, 0, 1, 2]
# filtro
h = [0.5, 1, 0.5]

def main():
    # Realizar la convolución
    y = dconv(h, x)

    # Realizar la DFT
    Y = dft(y)
    padding = len(Y) # Longitud de la señal de salida
    X = dft(x, padding)
    H = dft(h, padding)
    
    # Imprimir el resultado de la convolución
    print("Resultado de la convolución:")
    print(np.array_str(np.array(y), precision=1, suppress_small=True))
    
    # Imprimir el resultado de la DFT
    print("\nResultado de la DFT de la señal de entrada:")
    print(np.array_str(np.array(X), precision=1, suppress_small=True))
    
    # Imprimir el resultado de la DFT del filtro
    print("\nResultado de la DFT del filtro:")
    print(np.array_str(np.array(H), precision=1, suppress_small=True))
    
    # Imprimir el resultado de la DFT de la convolución
    print("\nResultado de la DFT de la convolución:")
    print(np.array_str(np.array(Y), precision=1, suppress_small=True))

    # Propiedad de la convolución en el dominio temporal y multiplicación en el dominio de la frecuencia
    print("\nPropiedad de la convolución en el dominio temporal y multiplicación en el dominio de la frecuencia:")
    Y_check = np.multiply(X, H)
    print(np.array_str(np.array(Y_check), precision=1, suppress_small=True))

if __name__ == "__main__":
    main()