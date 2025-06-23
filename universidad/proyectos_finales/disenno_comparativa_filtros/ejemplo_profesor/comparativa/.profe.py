import numpy as np 
import matplotlib.pyplot as plt 
from scipy import signal 
 
def design_fir_bandpass(center_freq, bandwidth, fs, order=101): 
    """Diseña filtro FIR pasabanda usando método de la ventana""" 
    nyquist = fs / 2 
    low_cutoff = (center_freq - bandwidth/2) / nyquist 
    high_cutoff = (center_freq + bandwidth/2) / nyquist 
     
    # Limitar a rango válido 
    low_cutoff = max(0.001, min(0.999, low_cutoff)) 
    high_cutoff = max(0.001, min(0.999, high_cutoff)) 
     
    b = signal.firwin(order, [low_cutoff, high_cutoff], window='hamming', 
pass_zero=False) 
    return b, [1.0]  # b, a para formato compatible con IIR 
 
def design_iir_bandpass(center_freq, bandwidth, fs, order=2): 
    """Diseña filtro IIR pasabanda usando Butterworth""" 
    nyquist = fs / 2 
    low_cutoff = (center_freq - bandwidth/2) / nyquist 
    high_cutoff = (center_freq + bandwidth/2) / nyquist 
     
    # Limitar a rango válido 
    low_cutoff = max(0.001, min(0.999, low_cutoff)) 
    high_cutoff = max(0.001, min(0.999, high_cutoff)) 
     
    b, a = signal.butter(order, [low_cutoff, high_cutoff], btype='band') 
    return b, a 
 
def compare_filters(center_freq, bandwidth, fs): 
    """Compara filtros FIR e IIR para una frecuencia dada""" 
    # Diseñar filtros 
    b_fir, a_fir = design_fir_bandpass(center_freq, bandwidth, fs, 
order=101) 
    b_iir, a_iir = design_iir_bandpass(center_freq, bandwidth, fs, 
order=2) 
     
    # Calcular respuestas en frecuencia 
    w, h_fir = signal.freqz(b_fir, a_fir, worN=8000) 
    _, h_iir = signal.freqz(b_iir, a_iir, worN=8000) 
    f = w * fs / (2 * np.pi) 
     
    # Graficar respuestas en magnitud 
    plt.figure(figsize=(12, 10)) 
     
    # Respuesta en magnitud 
    plt.subplot(2, 1, 1) 
    plt.plot(f, np.abs(h_fir), 'b-', label='FIR (Orden 101)') 
    plt.plot(f, np.abs(h_iir), 'r--', label='IIR (Orden 2)') 
    plt.title(f'Comparación de filtros para {center_freq} Hz') 
    plt.xlabel('Frecuencia (Hz)') 
    plt.ylabel('Ganancia') 
    plt.grid(True) 
    plt.axvline(center_freq, color='g', linestyle='--', alpha=0.5) 
    plt.legend() 
    plt.xlim(center_freq - 200, center_freq + 200) 
     
    # Respuesta en dB 
    plt.subplot(2, 1, 2) 
    plt.plot(f, 20 * np.log10(np.abs(h_fir) + 1e-10), 'b-', label='FIR  (Orden 101)') 
    plt.plot(f, 20 * np.log10(np.abs(h_iir) + 1e-10), 'r--', label='IIR (Orden 2)') 
    plt.title(f'Respuesta en dB para {center_freq} Hz') 
    plt.xlabel('Frecuencia (Hz)') 
    plt.ylabel('Ganancia (dB)') 
    plt.grid(True) 
    plt.axvline(center_freq, color='g', linestyle='--', alpha=0.5) 
    plt.legend() 
    plt.xlim(0, 2000) 
    plt.ylim(-80, 5) 
     
    plt.tight_layout() 
    plt.savefig(f'filter_comparison_{center_freq}Hz.png') 
    plt.show() 
     
    # Analizar fase 
    plt.figure(figsize=(10, 6)) 
    plt.plot(f, np.unwrap(np.angle(h_fir)), 'b-', label='FIR (Orden 101)') 
    plt.plot(f, np.unwrap(np.angle(h_iir)), 'r--', label='IIR (Orden 2)') 
    plt.title(f'Comparación de fase para {center_freq} Hz') 
    plt.xlabel('Frecuencia (Hz)') 
    plt.ylabel('Fase (radianes)') 
    plt.grid(True) 
    plt.axvline(center_freq, color='g', linestyle='--', alpha=0.5) 
    plt.legend() 
    plt.xlim(center_freq - 200, center_freq + 200) 
    plt.savefig(f'phase_comparison_{center_freq}Hz.png') 
    plt.show() 
 
# Comparar filtros para una frecuencia baja y una alta 
fs = 8000 
bandwidth = 30 
compare_filters(697, bandwidth, fs)  # Frecuencia baja 
compare_filters(1209, bandwidth, fs)  # Frecuencia alta 