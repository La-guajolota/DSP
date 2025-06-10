# Importación de librerías necesarias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

# Rutas de los archivos CSV
file_paths = [
    '/media/adrian/sd_linux/sem8/DSP/parcial_3/practica_4/PART1/sampled_signals/Senoidal_100Hz.csv',
    '/media/adrian/sd_linux/sem8/DSP/parcial_3/practica_4/PART1/sampled_signals/Barrido_10-500Hz.csv',
    '/media/adrian/sd_linux/sem8/DSP/parcial_3/practica_4/PART1/sampled_signals/Senoidal_Ruido_100Hz.csv'
]

# Parámetros del filtro
fs = 10000  # Frecuencia de muestreo (Hz)
fc_low = 100   # Frecuencia de corte baja (Hz)
fc_high = 200  # Frecuencia de corte alta (Hz)
nyq = fs / 2  # Frecuencia de Nyquist
M = 11     # Orden del filtro (impar para simetría)

# Definir diferentes ventanas
ventanas = {
    'Rectangular': 'boxcar',
    'Hanning': 'hann',
    'Hamming': 'hamming',
    'Blackman': 'blackman',
    'Kaiser (β=4.0)': ('kaiser', 4.0)
}

# Función para diseñar filtros FIR con diferentes ventanas
def diseñar_filtros_fir(ventanas, M, fc_low, fc_high, fs):
    """
    Diseña filtros FIR con diferentes ventanas.

    Parámetros:
    - ventanas: Diccionario con los nombres y tipos de ventanas.
    - M: Orden del filtro (número de coeficientes).
    - fc_low: Frecuencia de corte baja (Hz).
    - fc_high: Frecuencia de corte alta (Hz).
    - fs: Frecuencia de muestreo (Hz).

    Retorna:
    - filtros: Diccionario con los coeficientes de los filtros diseñados.
    """
    filtros = {'Pasa-Bajas': {}, 'Pasa-Altas': {}, 'Pasa-Bandas': {}}
    nyq = fs / 2

    # Diseñar filtros pasa-bajas
    for nombre, ventana in ventanas.items():
        h = signal.firwin(M, fc_low / nyq, window=ventana)
        filtros['Pasa-Bajas'][nombre] = h

    # Diseñar filtros pasa-altas
    for nombre, ventana in ventanas.items():
        h = signal.firwin(M, fc_low / nyq, window=ventana, pass_zero=False)
        filtros['Pasa-Altas'][nombre] = h

    # Diseñar filtros pasa-bandas
    for nombre, ventana in ventanas.items():
        h = signal.firwin(M, [fc_low / nyq, fc_high / nyq], window=ventana, pass_zero=False)
        filtros['Pasa-Bandas'][nombre] = h

    return filtros

# Diseñar filtros FIR con diferentes ventanas
filtros = diseñar_filtros_fir(ventanas, M, fc_low, fc_high, fs)

# Iterar sobre los archivos y aplicar los filtros
for i, file_path in enumerate(file_paths):
    # Cargar los datos del archivo CSV
    data = pd.read_csv(file_path)
    
    # Extraer las columnas de muestra y valor
    n_samples = data['Muestra'].values  # Índices de las muestras
    signal_values = data['Valor'].values  # Valores de la señal

    # Crear mosaico para señales originales y filtradas
    num_filtros = max(len(filtros['Pasa-Bajas']), len(filtros['Pasa-Altas']), len(filtros['Pasa-Bandas']))
    fig, axs = plt.subplots(4, num_filtros, figsize=(15, 10))
    fig.suptitle(f'Señal Original y Filtrada ({file_path.split("/")[-1]})', fontsize=16)

    # Graficar señal original
    axs[0, 0].plot(n_samples, signal_values, label='Original', color='blue')
    axs[0, 0].set_title('Señal Original')
    axs[0, 0].set_xlabel('Muestras')
    axs[0, 0].set_ylabel('Amplitud')
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    # Aplicar filtros y graficar señales filtradas
    for j, (tipo, filtros_tipo) in enumerate(filtros.items()):
        for k, (nombre, h) in enumerate(filtros_tipo.items()):
            filtered_signal = signal.lfilter(h, 1, signal_values)
            axs[j + 1, k].plot(n_samples, filtered_signal, label=f'{tipo} con {nombre}', alpha=0.7)
            axs[j + 1, k].set_title(f'{tipo} ({nombre})')
            axs[j + 1, k].set_xlabel('Muestras')
            axs[j + 1, k].set_ylabel('Amplitud')
            axs[j + 1, k].grid(True)
            axs[j + 1, k].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    # Crear mosaico para espectros
    fig, axs = plt.subplots(4, num_filtros, figsize=(15, 10))
    fig.suptitle(f'Espectros de Señal Original y Filtrada ({file_path.split("/")[-1]})', fontsize=16)

    # FFT de la señal original
    X = np.fft.fft(signal_values)
    freq = np.fft.fftfreq(len(signal_values), 1/fs)
    axs[0, 0].plot(freq[:len(freq)//2], 20 * np.log10(np.abs(X[:len(X)//2]) + 1e-10), label='Original', color='blue')
    axs[0, 0].set_title('Espectro Original (dB)')
    axs[0, 0].set_xlabel('Frecuencia (Hz)')
    axs[0, 0].set_ylabel('Magnitud (dB)')
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    # FFT de las señales filtradas
    for j, (tipo, filtros_tipo) in enumerate(filtros.items()):
        for k, (nombre, h) in enumerate(filtros_tipo.items()):
            filtered_signal = signal.lfilter(h, 1, signal_values)
            Y = np.fft.fft(filtered_signal)
            axs[j + 1, k].plot(freq[:len(freq)//2], 20 * np.log10(np.abs(Y[:len(Y)//2]) + 1e-10), label=f'{tipo} con {nombre}', alpha=0.7)
            axs[j + 1, k].set_title(f'{tipo} ({nombre})')
            axs[j + 1, k].set_xlabel('Frecuencia (Hz)')
            axs[j + 1, k].set_ylabel('Magnitud (dB)')
            axs[j + 1, k].grid(True)
            axs[j + 1, k].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()