# Convolución discreta algoritmo
# Autor: Adrián Silva Palafox
# Fecha: 2025-4-4

import matplotlib.pyplot as plt

# Señales de entrada
h_filter = [0.5,1,0.5]  
x_signal = [2,1,0,1,2]

# Convolución discreta
def dconv(h, x):
    """
    Realiza la convolución discreta entre dos señales.
    
    Parámetros:
    h (list): Primer señal (filtro).
    x (list): Segunda señal (entrada).
    
    Retorna:
    list: Resultado de la convolución.
    """
    # Longitudes de las señales
    len_h = len(h)
    len_x = len(x)
    
    # Longitud de la señal resultante
    len_y = len_h + len_x - 1
    
    # Inicializar la señal resultante
    y = [0] * len_y
    
    # Realizar la convolución
    for n in range(len_y):
        for k in range(len_h):
            if n - k >= 0 and n - k < len_x:
                y[n] += h[k] * x[n - k]
    
    return y

def main():
    # Realizar la convolución
    y = dconv(h_filter, x_signal)
    
    # Imprimir el resultado
    print("Resultado de la convolución:", y)

    # Graficar las señales
    plt.figure(figsize=(10, 5))
    plt.subplot(3, 1, 1)
    plt.stem(h_filter)
    plt.title("Filtro")
    plt.subplot(3, 1, 2)
    plt.stem(x_signal)
    plt.title("Señal de entrada")
    plt.subplot(3, 1, 3)
    plt.stem(y)
    plt.title("Resultado de la convolución")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
# Resultado esperado: [1.0, 2.0, 2.0, 2.0, 1.0]