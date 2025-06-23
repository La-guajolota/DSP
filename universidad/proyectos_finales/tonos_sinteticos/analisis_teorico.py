import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.io.wavfile import write

# -- Parámetros de la simulación --
fs = 8000  # Frecuencia de muestreo en Hz (estándar para telefonía)
duracion = 0.225  # Duración del tono en segundos
amplitud = 0.5  # Amplitud de la señal

# -- Frecuencias estándar DTMF --
freq_bajas = {'1': 697, '2': 697, '3': 697, 'A': 697,
              '4': 770, '5': 770, '6': 770, 'B': 770,
              '7': 852, '8': 852, '9': 852, 'C': 852,
              '*': 941, '0': 941, '#': 941, 'D': 941}

freq_altas = {'1': 1209, '4': 1209, '7': 1209, '*': 1209,
              '2': 1336, '5': 1336, '8': 1336, '0': 1336,
              '3': 1477, '6': 1477, '9': 1477, '#': 1477,
              'A': 1633, 'B': 1633, 'C': 1633, 'D': 1633}

def generar_tono_dtmf(tecla, duracion, fs, amplitud):
    """
    Genera una señal DTMF para una tecla dada.
    La señal es la suma de dos ondas sinusoidales.
    """
    if tecla not in freq_bajas or tecla not in freq_altas:
        raise ValueError("Tecla no válida. Use '0'-'9', '*', '#', 'A'-'D'.")

    # Vector de tiempo
    t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)

    # Frecuencias para la tecla seleccionada
    f1 = freq_bajas[tecla]
    f2 = freq_altas[tecla]

    # Generación de las dos ondas sinusoidales
    onda1 = amplitud * np.sin(2 * np.pi * f1 * t)
    onda2 = amplitud * np.sin(2 * np.pi * f2 * t)

    # Suma de las ondas para formar el tono DTMF
    tono_dtmf = onda1 + onda2

    # Normalización para evitar clipping al guardar en 16 bits
    tono_dtmf_normalizado = np.int16((tono_dtmf / tono_dtmf.max()) * 32767)
    
    return t, tono_dtmf, tono_dtmf_normalizado, f1, f2

def graficar_mosaico_tiempo(teclas, tiempos, señales, fs):
    """
    Crea un mosaico de gráficos en el dominio del tiempo para todas las teclas.
    """
    num_teclas = len(teclas)
    cols = 4
    rows = (num_teclas + cols - 1) // cols

    plt.figure(figsize=(16, 10))
    for i, tecla in enumerate(teclas):
        plt.subplot(rows, cols, i + 1)
        plt.plot(tiempos[i][:int(fs * 0.05)], señales[i][:int(fs * 0.05)])  # Mostrar solo los primeros 50 ms
        plt.title(f"Tecla: {tecla}")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Amplitud")
        plt.grid(True)
    plt.tight_layout()
    plt.show()

def graficar_mosaico_frecuencia(teclas, señales, fs):
    """
    Crea un mosaico de gráficos en el dominio de la frecuencia para todas las teclas.
    """
    num_teclas = len(teclas)
    cols = 4
    rows = (num_teclas + cols - 1) // cols

    plt.figure(figsize=(16, 10))
    for i, tecla in enumerate(teclas):
        N = len(señales[i])
        yf = fft(señales[i])
        xf = fftfreq(N, 1 / fs)[:N // 2]
        plt.subplot(rows, cols, i + 1)
        plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
        plt.title(f"Tecla: {tecla}")
        plt.xlabel("Frecuencia [Hz]")
        plt.ylabel("Amplitud")
        plt.grid(True)
    plt.tight_layout()
    plt.show()

# --- Ejecución Principal ---
if __name__ == "__main__":
    teclas = list(freq_bajas.keys())
    tiempos = []
    señales = []
    señales_normalizadas = []

    for tecla in teclas:
        # Generar el tono
        t, tono, tono_normalizado, f1, f2 = generar_tono_dtmf(tecla, duracion, fs, amplitud)
        tiempos.append(t)
        señales.append(tono)
        señales_normalizadas.append(tono_normalizado)

        # Guardar en archivo .wav
        nombre_archivo = f'./tonos_sinteticos/tonos_teclas/tono_dtmf_{tecla}.wav'
        write(nombre_archivo, fs, tono_normalizado)
        print(f"Tono para la tecla '{tecla}' generado y guardado como '{nombre_archivo}'")

    # Graficar mosaico en el dominio del tiempo
    graficar_mosaico_tiempo(teclas, tiempos, señales, fs)

    # Graficar mosaico en el dominio de la frecuencia
    graficar_mosaico_frecuencia(teclas, señales, fs)