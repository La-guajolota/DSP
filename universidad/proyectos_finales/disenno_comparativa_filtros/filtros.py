import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def comparar_filtros_pasabanda(f_central, ancho_banda, fs):
    """
    Diseña, analiza y compara un filtro FIR y un IIR para una frecuencia dada.
    """
    # --- Parámetros comunes ---
    nyq_rate = fs / 2.0
    borde_bajo = (f_central - ancho_banda / 2) / nyq_rate
    borde_alto = (f_central + ancho_banda / 2) / nyq_rate
    
    # --- 1. Diseño del Filtro FIR (Respuesta Finita al Impulso) ---
    # Orden del filtro: un orden más alto da una transición más abrupta.
    fir_orden = 11 
    # Diseño usando el método de la ventana (Hamming en este caso)
    fir_coeffs = signal.firwin(fir_orden, [borde_bajo, borde_alto], pass_zero=False, window='hamming')
    w_fir, h_fir = signal.freqz(fir_coeffs, worN=8000)
    
    # --- 2. Diseño del Filtro IIR (Respuesta Infinita al Impulso) ---
    # Orden del filtro: bajo orden para eficiencia computacional
    iir_orden = 11
    # Diseño usando la aproximación de Butterworth
    # 'b, a' son los coeficientes del numerador y denominador del filtro
    b, a = signal.butter(iir_orden, [borde_bajo, borde_alto], btype='band')
    w_iir, h_iir = signal.freqz(b, a, worN=8000)

    # --- 3. Visualización y Comparativa ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axs = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle(f'Comparativa de Filtros PasaBanda para {f_central} Hz', fontsize=16)

    # -- Gráfico de Respuesta en Magnitud --
    axs[0].plot((w_fir/np.pi)*nyq_rate, 20 * np.log10(abs(h_fir)), 'b', label=f'FIR (Orden {fir_orden})')
    axs[0].plot((w_iir/np.pi)*nyq_rate, 20 * np.log10(abs(h_iir)), 'r--', label=f'IIR Butterworth (Orden {iir_orden})')
    axs[0].set_title("Respuesta en Magnitud")
    axs[0].set_ylabel("Magnitud [dB]")
    axs[0].set_xlabel("Frecuencia [Hz]")
    axs[0].axvline(f_central, color='k', linestyle=':', alpha=0.7, label=f'Frecuencia Central ({f_central} Hz)')
    axs[0].set_xlim(f_central - 200, f_central + 200) # Zoom alrededor de la frecuencia de interés
    axs[0].set_ylim(-60, 5)
    axs[0].legend()
    axs[0].grid(True)
    
    # -- Gráfico de Respuesta de Fase --
    angles_fir = np.unwrap(np.angle(h_fir))
    angles_iir = np.unwrap(np.angle(h_iir))
    
    axs[1].plot((w_fir/np.pi)*nyq_rate, angles_fir, 'b', label='FIR (Fase Lineal)')
    axs[1].plot((w_iir/np.pi)*nyq_rate, angles_iir, 'r--', label='IIR (Fase No Lineal)')
    axs[1].set_title("Respuesta de Fase")
    axs[1].set_ylabel("Ángulo (radianes)")
    axs[1].set_xlabel("Frecuencia [Hz]")
    axs[1].set_xlim(f_central - 200, f_central + 200) # Mismo zoom que en magnitud
    axs[1].grid(True)
    axs[1].legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# --- Ejecución Principal ---
if __name__ == "__main__":
    # Parámetros para el diseño del filtro
    fs = 8000  # Frecuencia de muestreo en Hz
    frecuencia_objetivo = 697 # <--- Puede cambiar esta por otra frecuencia DTMF (e.g., 770, 1336)
    ancho_banda_hz = 30 # Ancho de banda del filtro en Hz

    print(f"Diseñando y comparando filtros para la frecuencia {frecuencia_objetivo} Hz...")
    comparar_filtros_pasabanda(frecuencia_objetivo, ancho_banda_hz, fs)