import numpy as np 
import matplotlib.pyplot as plt 
from scipy import signal 
 
def design_bandpass_filter(center_freq, bandwidth, fs, order=101): 
    """ 
    Diseña un filtro pasabanda FIR para una frecuencia central específica 
     
    Parámetros: 
    center_freq: Frecuencia central del filtro en Hz 
    bandwidth: Ancho de banda del filtro en Hz 
    fs: Frecuencia de muestreo en Hz 
    order: Orden del filtro (debe ser impar) 
     
    Retorna: 
    b: Coeficientes del filtro FIR 
    """ 
    if order % 2 == 0: 
        order += 1  # Asegurar que el orden sea impar 
     
    # Normalizar frecuencias 
    nyquist = fs / 2 
    low_cutoff = (center_freq - bandwidth/2) / nyquist 
    high_cutoff = (center_freq + bandwidth/2) / nyquist 
     
    # Limitar a rango válido 
    low_cutoff = max(0.001, min(0.999, low_cutoff)) 
    high_cutoff = max(0.001, min(0.999, high_cutoff)) 
     
    # Diseñar filtro usando ventana Hamming 
    b = signal.firwin(order, [low_cutoff, high_cutoff], window='hamming', 
pass_zero=False) 
     
    return b 
 
def analyze_filter(b, fs, center_freq): 
    """ 
    Analiza y muestra la respuesta en frecuencia del filtro 
    """ 
    # Calcular respuesta en frecuencia 
    w, h = signal.freqz(b, 1, worN=8000) 
    f = w * fs / (2 * np.pi) 
     
    # Graficar respuesta en magnitud 
    plt.figure(figsize=(10, 6)) 
    plt.subplot(2, 1, 1) 
    plt.plot(f, np.abs(h)) 
    plt.title(f'Respuesta en magnitud del filtro para {center_freq} Hz') 
    plt.xlabel('Frecuencia (Hz)') 
    plt.ylabel('Ganancia') 
    plt.grid(True) 
    plt.axvline(center_freq, color='r', linestyle='--', alpha=0.5) 
    plt.xlim(0, 2000) 
     
    # Respuesta en dB 
    plt.subplot(2, 1, 2) 
    plt.plot(f, 20 * np.log10(np.abs(h) + 1e-10)) 
    plt.title(f'Respuesta en dB del filtro para {center_freq} Hz') 
    plt.xlabel('Frecuencia (Hz)') 
    plt.ylabel('Ganancia (dB)') 
    plt.grid(True) 
    plt.axvline(center_freq, color='r', linestyle='--', alpha=0.5) 
    plt.xlim(0, 2000) 
    plt.ylim(-80, 5) 
     
    plt.tight_layout() 
    plt.savefig(f'filter_response_{center_freq}Hz.png') 
    plt.show() 
 
# Parámetros 
fs = 8000  # Frecuencia de muestreo 
bandwidth = 30  # Ancho de banda de 30 Hz 
filter_order = 251  # Orden del filtro 
 
# Diseñar y analizar filtros para frecuencias bajas 
for freq in [697, 770, 852, 941]: 
    b = design_bandpass_filter(freq, bandwidth, fs, filter_order) 
    analyze_filter(b, fs, freq) 
    np.savetxt(f'dtmf_filter_coef_{freq}Hz.csv', b, delimiter=',') 
 
# Diseñar y analizar filtros para frecuencias altas 
for freq in [1209, 1336, 1477, 1633]: 
    b = design_bandpass_filter(freq, bandwidth, fs, filter_order) 
    analyze_filter(b, fs, freq) 
    np.savetxt(f'dtmf_filter_coef_{freq}Hz.csv', b, delimiter=',')