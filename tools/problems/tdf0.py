"""
Dada la secuencia exponencial x[n] = 0.5ⁿ para n = 0,1,2 (3 puntos):
1. Calcule manualmente la Transformada Discreta de Fourier (DFT) de x[n] aplicando 
directamente la definición: X[k] = Σ(n=0 a N-1) x[n]e^(-j2πkn/N) para k = 0,1,2.
"""

from tools.dft import dft
from tools.dconv import dconv
import numpy as np
import matplotlib.pyplot as plt

x = [0.5**n for n in range(3)]  # x[n] = 0.5^n para n = 0,1,2

def main():
    # Calcular la DFT de x[n]
    X = dft(x)
    
    # Imprimir el resultado de la DFT
    print("Resultado de la DFT de x[n]:")
    print(np.array_str(np.array(X), precision=3, suppress_small=True))
    
    # Graficar la magnitud y fase de la DFT
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.title("Magnitud de la DFT")
    plt.stem(range(len(X)), np.abs(X))
    plt.xlabel("k")
    plt.ylabel("|X[k]|")
    
    plt.subplot(2, 1, 2)
    plt.title("Fase de la DFT")
    plt.stem(range(len(X)), np.angle(X))
    plt.xlabel("k")
    plt.ylabel("∠X[k]")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
"""
Dada la secuencia exponencial x[n] = 0.5ⁿ para n = 0,1,2 (3 puntos):
1. Calcule manualmente la Transformada Discreta de Fourier (DFT) de x[n] aplicando
directamente la definición: X[k] = Σ(n=0 a N-1) x[n]e^(-j2πkn/N) para k = 0,1,2.
2. Calcule la DFT de x[n] utilizando la función dft() y compare los resultados.
3. Grafique la magnitud y fase de la DFT.
"""