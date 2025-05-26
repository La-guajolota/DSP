# Importación de librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parámetros de simulación
fs = 1000  # Frecuencia de muestreo (Hz)
fc = 100   # Frecuencia de corte (Hz)
nyq = fs / 2  # Frecuencia de Nyquist
M = 51     # Orden del filtro (impar para simetría)

# Definir diferentes ventanas
ventanas = {
    'Rectangular': 'boxcar',
    'Hanning': 'hann',
    'Hamming': 'hamming',
    'Blackman': 'blackman',
    'Kaiser (β=4.0)': ('kaiser', 4.0)
}

# Función para mostrar ventanas en el dominio del tiempo
def mostrar_ventanas(ventanas, M):
    """
    Muestra las ventanas en el dominio del tiempo.

    Parámetros:
    - ventanas: Diccionario con los nombres y tipos de ventanas.
    - M: Orden del filtro (número de coeficientes).
    """
    plt.figure(figsize=(10, 6))
    n = np.arange(M)
    for nombre, ventana in ventanas.items():
        if isinstance(ventana, tuple):
            window = signal.get_window(ventana, M)
        else:
            window = signal.get_window(ventana, M)
        plt.plot(n, window, label=nombre)
    plt.title('Ventanas en el Dominio del Tiempo')
    plt.xlabel('n [muestras]')
    plt.ylabel('Amplitud')
    plt.legend()
    plt.grid(True)
    plt.show()

# Función para diseñar y analizar filtros FIR con diferentes ventanas
def analizar_filtros_fir(ventanas, M, fc, fs):
    """
    Diseña y analiza filtros FIR con diferentes ventanas.

    Parámetros:
    - ventanas: Diccionario con los nombres y tipos de ventanas.
    - M: Orden del filtro (número de coeficientes).
    - fc: Frecuencia de corte (Hz).
    - fs: Frecuencia de muestreo (Hz).

    Retorna:
    - filtros: Diccionario con los coeficientes de los filtros diseñados.
    """
    nyq = fs / 2
    filtros = {}

    # Diseñar filtros con diferentes ventanas
    for nombre, ventana in ventanas.items():
        if isinstance(ventana, tuple):
            h = signal.firwin(M, fc/nyq, window=ventana)
        else:
            h = signal.firwin(M, fc/nyq, window=ventana)
        filtros[nombre] = h

    # Calcular y graficar respuestas en frecuencia
    plt.figure(figsize=(12, 10))
    for i, (nombre, h) in enumerate(filtros.items(), 1):
        w, H = signal.freqz(h, 1, worN=1000)
        f = w * fs / (2 * np.pi)

        # Magnitud en escala lineal
        plt.subplot(len(filtros), 2, 2*i-1)
        plt.plot(f, np.abs(H))
        plt.title(f'Filtro FIR con Ventana {nombre}')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud')
        plt.grid(True)
        plt.xlim([0, fs/2])

        # Magnitud en dB
        plt.subplot(len(filtros), 2, 2*i)
        plt.plot(f, 20 * np.log10(np.abs(H) + 1e-10))  # Evitar log(0)
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud (dB)')
        plt.grid(True)
        plt.xlim([0, fs/2])
        plt.ylim([-100, 5])

    plt.tight_layout()
    plt.show()

    return filtros

# Mostrar ventanas en el dominio del tiempo
mostrar_ventanas(ventanas, M)

# Diseñar y analizar filtros FIR con diferentes ventanas
filtros = analizar_filtros_fir(ventanas, M, fc, fs)

# Crear una señal de prueba con múltiples componentes frecuenciales
t = np.arange(0, 1, 1/fs)
f1, f2, f3 = 50, 150, 300  # Frecuencias de componentes (Hz)
x = np.sin(2*np.pi*f1*t) + 0.5*np.sin(2*np.pi*f2*t) + 0.25*np.sin(2*np.pi*f3*t)

# Graficar la señal original en el dominio del tiempo
plt.figure(figsize=(12, 6))
plt.subplot(3, 1, 1)
plt.plot(t[:200], x[:200])
plt.title('Señal Original (Primeras 200 muestras)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)

# Aplicar diferentes filtros y comparar resultados en el dominio del tiempo
for i, (nombre, h) in enumerate(filtros.items(), 2):
    if i > 3:  # Mostrar solo dos filtros por claridad
        break
    y = signal.lfilter(h, 1, x)
    plt.subplot(3, 1, i)
    plt.plot(t[:200], y[:200])
    plt.title(f'Señal Filtrada con Ventana {nombre}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True)

plt.tight_layout()
plt.show()

# Análisis en el dominio de la frecuencia
plt.figure(figsize=(12, 6))

# FFT de la señal original
X = np.fft.fft(x)
freq = np.fft.fftfreq(len(x), 1/fs)
plt.subplot(3, 1, 1)
plt.plot(freq[:len(freq)//2], np.abs(X[:len(X)//2])/len(X))
plt.title('Espectro de la Señal Original')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.grid(True)
plt.xlim([0, fs/2])

# FFT de las señales filtradas
for i, (nombre, h) in enumerate(filtros.items(), 2):
    if i > 3:  # Mostrar solo dos filtros por claridad
        break
    y = signal.lfilter(h, 1, x)
    Y = np.fft.fft(y)
    plt.subplot(3, 1, i)
    plt.plot(freq[:len(freq)//2], np.abs(Y[:len(Y)//2])/len(Y))
    plt.title(f'Espectro de la Señal Filtrada con Ventana {nombre}')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True)
    plt.xlim([0, fs/2])

plt.tight_layout()
plt.show()

# Guardar coeficientes del filtro Hamming para usarlo más adelante
np.save('coef_fir_hamming.npy', filtros['Hamming'])
print("Coeficientes del filtro FIR con ventana Hamming guardados en 'coef_fir_hamming.npy'")