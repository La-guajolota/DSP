# Importación de librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parámetros generales
fs = 1000  # Frecuencia de muestreo (Hz)
T = 1      # Duración de la señal (segundos)
N = T * fs # Número de muestras
t = np.arange(0, T, 1/fs)  # Vector de tiempo

# Función para mostrar la respuesta al impulso de un filtro
def mostrar_respuesta_impulso(b, a, titulo, N_imp=100):
    """
    Muestra la respuesta al impulso de un filtro dado.

    Parámetros:
    - b, a: Coeficientes del filtro (numerador y denominador).
    - titulo: Título del gráfico.
    - N_imp: Número de muestras del impulso (por defecto 100).
    """
    # Generar impulso unitario
    impulso = np.zeros(N_imp)
    impulso[0] = 1

    # Calcular respuesta al impulso
    respuesta = signal.lfilter(b, a, impulso)

    # Graficar la respuesta al impulso
    plt.figure(figsize=(10, 6))
    plt.stem(np.arange(N_imp), respuesta)  # Corregido: use_line_collection=True
    plt.title(f'Respuesta al Impulso - {titulo}')
    plt.xlabel('n [muestras]')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()

    return respuesta

# Función para mostrar la respuesta en frecuencia de un filtro
def mostrar_respuesta_frecuencia(b, a, titulo, fs=1000):
    """
    Muestra la respuesta en frecuencia de un filtro dado.

    Parámetros:
    - b, a: Coeficientes del filtro (numerador y denominador).
    - titulo: Título del gráfico.
    - fs: Frecuencia de muestreo (por defecto 1000 Hz).
    """
    # Calcular respuesta en frecuencia
    w, h = signal.freqz(b, a, worN=8000)
    f = w * fs / (2 * np.pi)  # Convertir a Hz

    # Graficar la magnitud de la respuesta en frecuencia
    plt.figure(figsize=(12, 8))

    # Magnitud en escala lineal
    plt.subplot(2, 1, 1)
    plt.plot(f, np.abs(h))
    plt.title(f'Respuesta en Frecuencia - {titulo}')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True)
    plt.xlim([0, fs/2])

    # Magnitud en escala logarítmica (dB)
    plt.subplot(2, 1, 2)
    plt.plot(f, 20 * np.log10(np.abs(h) + 1e-10))  # Evitar log(0)
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud (dB)')
    plt.grid(True)
    plt.xlim([0, fs/2])
    plt.ylim([-80, 5])
    plt.tight_layout()
    plt.show()

# Diseño de filtros

# 1. Filtro FIR Paso-Bajas (ventana rectangular)
fc = 100  # Frecuencia de corte (Hz)
nyq = fs / 2  # Frecuencia de Nyquist
M = 31  # Orden del filtro (M impar para simetría)

# Diseño del filtro FIR usando una ventana rectangular
h_fir = signal.firwin(M, fc/nyq, window='boxcar')
print(f"Coeficientes del filtro FIR (Rectangular, Orden {M-1}):")
print(h_fir)

# 2. Filtro IIR Paso-Bajas (Butterworth)
orden_iir = 4  # Orden del filtro
b_iir, a_iir = signal.butter(orden_iir, fc/nyq, 'low')
print(f"\nCoeficientes del filtro IIR (Butterworth, Orden {orden_iir}):")
print(f"Numerador: {b_iir}")
print(f"Denominador: {a_iir}")

# Mostrar respuestas al impulso
resp_fir = mostrar_respuesta_impulso(h_fir, 1, f'Filtro FIR Orden {M-1}')
resp_iir = mostrar_respuesta_impulso(b_iir, a_iir, f'Filtro IIR Orden {orden_iir}')

# Mostrar respuestas en frecuencia
mostrar_respuesta_frecuencia(h_fir, 1, f'Filtro FIR Paso-Bajas (Rectangular, Orden {M-1})', fs)
mostrar_respuesta_frecuencia(b_iir, a_iir, f'Filtro IIR Paso-Bajas (Butterworth, Orden {orden_iir})', fs)