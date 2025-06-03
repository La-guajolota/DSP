import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

# Funciones para diseño de filtros FIR
def ideal_lp_filter(cutoff, M):
    """
    Diseña un filtro paso-bajas ideal de orden M
    cutoff: frecuencia de corte normalizada (0 a 1, donde 1 es pi rad/muestra)
    M: orden del filtro (M+1 coeficientes)
    """
    n = np.arange(M+1)
    # Calcular la respuesta al impulso ideal del filtro paso-bajas
    h = np.zeros(M+1)
    # Caso especial para evitar división por cero
    h[M//2] = cutoff
    # Calcular para el resto de los valores
    mask = np.ones(M+1, dtype=bool)
    mask[M//2] = False
    n_masked = n[mask] - M//2
    h[mask] = np.sin(np.pi * cutoff * n_masked) / (np.pi * n_masked)
    return h

def apply_window(h, window_type='rectangular'):
    """
    Aplica una ventana específica a los coeficientes del filtro
    """
    M = len(h) - 1
    if window_type.lower() == 'rectangular':
        window = np.ones(M+1)
    elif window_type.lower() == 'hanning':
        window = signal.windows.hann(M+1)
    elif window_type.lower() == 'hamming':
        window = signal.windows.hamming(M+1)
    elif window_type.lower() == 'blackman':
        window = signal.windows.blackman(M+1)
    else:
        raise ValueError(f"Tipo de ventana '{window_type}' no reconocido")
    
    return h * window

def freqz_normalized(h, fs=1.0, nfft=4096):
    """
    Calcula la respuesta en frecuencia normalizada del filtro
    """
    w, H = signal.freqz(h, worN=nfft)
    f = w * fs / (2 * np.pi)  # Convertir a Hz si se proporciona fs
    return f, H

def plot_filter_response(h, title="Respuesta del Filtro", fs=1.0):
    """
    Grafica la respuesta en el tiempo y en frecuencia del filtro
    """
    M = len(h) - 1
    n = np.arange(M+1)
    
    # Obtener respuesta en frecuencia
    f, H = freqz_normalized(h, fs)
    H_mag = np.abs(H)
    H_phase = np.angle(H)
    H_db = 20 * np.log10(H_mag + 1e-10)  # Agregar pequeño valor para evitar log(0)
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    
    # Respuesta al impulso
    axs[0].stem(n, h, use_line_collection=True)
    axs[0].set_title(f"Respuesta al Impulso ({title})")
    axs[0].set_xlabel('Muestra (n)')
    axs[0].set_ylabel('Amplitud')
    axs[0].grid(True)
    
    # Respuesta en magnitud
    axs[1].plot(f, H_mag)
    axs[1].set_title(f"Respuesta en Magnitud ({title})")
    axs[1].set_xlabel('Frecuencia Normalizada')
    axs[1].set_ylabel('Magnitud')
    axs[1].grid(True)
    
    # Respuesta en dB
    axs[2].plot(f, H_db)
    axs[2].set_title(f"Respuesta en dB ({title})")
    axs[2].set_xlabel('Frecuencia Normalizada')
    axs[2].set_ylabel('Magnitud (dB)')
    axs[2].set_ylim([-80, 5])
    axs[2].grid(True)
    
    plt.tight_layout()
    return fig

def filter_signal(x, h):
    """
    Filtra la señal x con los coeficientes del filtro h
    """
    return np.convolve(x, h, mode='same')

def generate_test_signal(fs=1000, duration=1.0, frequencies=[10, 50, 100, 200]):
    """
    Genera una señal de prueba con múltiples frecuencias
    """
    t = np.arange(0, duration, 1/fs)
    x = np.zeros_like(t)
    for f in frequencies:
        x += np.sin(2 * np.pi * f * t)
    return t, x

def design_filter(filter_type, cutoff, order, window='hamming', fs=1.0):
    """
    Diseña un filtro FIR con los parámetros especificados
    filter_type: 'lowpass', 'highpass', 'bandpass', 'bandstop'
    cutoff: frecuencia de corte normalizada o tupla para bandpass/bandstop
    order: orden del filtro (debe ser par para HP, BP, BS)
    window: tipo de ventana
    fs: frecuencia de muestreo (para visualización)
    """
    if order % 2 == 0:
        order += 1  # Asegurarse de que el orden sea impar para fase lineal
    
    if filter_type.lower() == 'lowpass':
        h_ideal = ideal_lp_filter(cutoff, order)
    
    elif filter_type.lower() == 'highpass':
        # Diseñar paso-bajas y convertir a paso-altas
        h_lp = ideal_lp_filter(cutoff, order)
        h_ideal = -h_lp  # Invertir
        h_ideal[order//2] += 1  # Agregar impulso en el centro
    
    elif filter_type.lower() == 'bandpass':
        # Asegurarse de que cutoff es una tupla
        if not isinstance(cutoff, (list, tuple)) or len(cutoff) != 2:
            raise ValueError("Para filtro bandpass, cutoff debe ser una tupla (f_low, f_high)")
        
        f_low, f_high = cutoff
        # Diseñar dos filtros paso-bajas y restar
        h_lp1 = ideal_lp_filter(f_high, order)
        h_lp2 = ideal_lp_filter(f_low, order)
        h_ideal = h_lp1 - h_lp2
    
    elif filter_type.lower() == 'bandstop':
        # Asegurarse de que cutoff es una tupla
        if not isinstance(cutoff, (list, tuple)) or len(cutoff) != 2:
            raise ValueError("Para filtro bandstop, cutoff debe ser una tupla (f_low, f_high)")
        
        f_low, f_high = cutoff
        # Diseñar dos filtros paso-bajas y combinar
        h_lp1 = ideal_lp_filter(f_low, order)
        h_lp2 = ideal_lp_filter(f_high, order)
        h_ideal = h_lp1 + (np.ones(order+1) - h_lp2)
    
    else:
        raise ValueError(f"Tipo de filtro '{filter_type}' no reconocido")
    
    # Aplicar ventana
    h = apply_window(h_ideal, window)
    
    return h

def export_filter_coeffs(h, filename="filter_coeffs.csv"):
    """
    Exporta los coeficientes del filtro a un archivo CSV y formato Arduino
    """
    # Guardar en CSV
    pd.DataFrame({'coeff': h}).to_csv(filename, index=False)
    
    # Formato para Arduino
    arduino_code = "const float filter_coeffs[] = {\n"
    for i, coeff in enumerate(h):
        arduino_code += f"  {coeff:.10f}"
        if i < len(h) - 1:
            arduino_code += ","
        if (i + 1) % 4 == 0:
            arduino_code += "\n"
    if (len(h) % 4) != 0:
        arduino_code += "\n"
    arduino_code += "};\n\n"
    arduino_code += f"const int FILTER_ORDER = {len(h) - 1};\n"
    arduino_code += f"const int FILTER_LENGTH = {len(h)};\n"
    
    # Guardar el código Arduino
    with open(filename.replace('.csv', '.h'), 'w') as f:
        f.write(arduino_code)
    
    print(f"Coeficientes guardados en {filename} y formato Arduino en {filename.replace('.csv', '.h')}")
    return arduino_code

# Ejemplo 1: Diseño de Filtro Paso-Bajas
def ejemplo_paso_bajas():
    # Parámetros
    fs = 1000  # Hz
    cutoff = 100 / (fs/2)  # Normalizada (100 Hz)
    order = 30  # Orden del filtro
    
    # Comparar diferentes ventanas
    windows = ['rectangular', 'hanning', 'hamming', 'blackman']
    plt.figure(figsize=(12, 8))
    
    for i, window in enumerate(windows, 1):
        h = design_filter('lowpass', cutoff, order, window, fs)
        f, H = freqz_normalized(h, fs)
        H_db = 20 * np.log10(np.abs(H) + 1e-10)
        
        plt.subplot(2, 2, i)
        plt.plot(f, H_db)
        plt.title(f"Paso-Bajas, Ventana {window.capitalize()}")
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud (dB)')
        plt.grid(True)
        plt.xlim([0, fs/2])
        plt.ylim([-100, 5])
    
    plt.tight_layout()
    plt.savefig("ejemplo_paso_bajas.png")
    plt.show()
    
    # Para la ventana Hamming, exportar coeficientes
    h_hamming = design_filter('lowpass', cutoff, order, 'hamming', fs)
    fig = plot_filter_response(h_hamming, "Paso-Bajas Hamming", fs)
    fig.savefig("paso_bajas_hamming.png")
    export_filter_coeffs(h_hamming, "lowpass_coeffs.csv")
    
    # Probar con señal de prueba
    t, x = generate_test_signal(fs, 1.0, [10, 50, 100, 200, 300])
    y = filter_signal(x, h_hamming)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, x)
    plt.title("Señal Original")
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(t, y)
    plt.title("Señal Filtrada (Paso-Bajas)")
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig("ejemplo_paso_bajas_senal.png")
    plt.show()

# Ejemplo 2: Diseño de Filtro Paso-Altas
def ejemplo_paso_altas():
    # Parámetros
    fs = 1000  # Hz
    cutoff = 150 / (fs/2)  # Normalizada (150 Hz)
    order = 30  # Orden del filtro
    
    # Comparar diferentes ventanas
    windows = ['rectangular', 'hanning', 'hamming', 'blackman']
    plt.figure(figsize=(12, 8))
    
    for i, window in enumerate(windows, 1):
        h = design_filter('highpass', cutoff, order, window, fs)
        f, H = freqz_normalized(h, fs)
        H_db = 20 * np.log10(np.abs(H) + 1e-10)
        
        plt.subplot(2, 2, i)
        plt.plot(f, H_db)
        plt.title(f"Paso-Altas, Ventana {window.capitalize()}")
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud (dB)')
        plt.grid(True)
        plt.xlim([0, fs/2])
        plt.ylim([-100, 5])
    
    plt.tight_layout()
    plt.savefig("ejemplo_paso_altas.png")
    plt.show()
    
    # Para la ventana Hamming, exportar coeficientes
    h_hamming = design_filter('highpass', cutoff, order, 'hamming', fs)
    fig = plot_filter_response(h_hamming, "Paso-Altas Hamming", fs)
    fig.savefig("paso_altas_hamming.png")
    export_filter_coeffs(h_hamming, "highpass_coeffs.csv")
    
    # Probar con señal de prueba
    t, x = generate_test_signal(fs, 1.0, [10, 50, 100, 200, 300])
    y = filter_signal(x, h_hamming)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, x)
    plt.title("Señal Original")
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(t, y)
    plt.title("Señal Filtrada (Paso-Altas)")
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig("ejemplo_paso_altas_senal.png")
    plt.show()

# Ejemplo 3: Diseño de Filtro Paso-Banda
def ejemplo_paso_banda():
    # Parámetros
    fs = 1000  # Hz
    cutoff = (100/(fs/2), 250/(fs/2))  # Normalizada (100-250 Hz)
    order = 50  # Orden del filtro
    
    # Comparar diferentes ventanas
    windows = ['rectangular', 'hanning', 'hamming', 'blackman']
    plt.figure(figsize=(12, 8))
    
    for i, window in enumerate(windows, 1):
        h = design_filter('bandpass', cutoff, order, window, fs)
        f, H = freqz_normalized(h, fs)
        H_db = 20 * np.log10(np.abs(H) + 1e-10)
        
        plt.subplot(2, 2, i)
        plt.plot(f, H_db)
        plt.title(f"Paso-Banda, Ventana {window.capitalize()}")
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud (dB)')
        plt.grid(True)
        plt.xlim([0, fs/2])
        plt.ylim([-100, 5])
    
    plt.tight_layout()
    plt.savefig("ejemplo_paso_banda.png")
    plt.show()
    
    # Para la ventana Hamming, exportar coeficientes
    h_hamming = design_filter('bandpass', cutoff, order, 'hamming', fs)
    fig = plot_filter_response(h_hamming, "Paso-Banda Hamming", fs)
    fig.savefig("paso_banda_hamming.png")
    export_filter_coeffs(h_hamming, "bandpass_coeffs.csv")
    
    # Probar con señal de prueba
    t, x = generate_test_signal(fs, 1.0, [10, 50, 150, 300, 400])
    y = filter_signal(x, h_hamming)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, x)
    plt.title("Señal Original")
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(t, y)
    plt.title("Señal Filtrada (Paso-Banda)")
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig("ejemplo_paso_banda_senal.png")
    plt.show()

# Función principal que ejecuta los ejemplos
def main():
    print("=== DISEÑO DE FILTROS FIR MEDIANTE EL MÉTODO DE LA VENTANA ===")
    print("1. Filtro Paso-Bajas")
    print("2. Filtro Paso-Altas")
    print("3. Filtro Paso-Banda")
    print("4. Diseñar filtro personalizado")
    print("5. Ejecutar todos los ejemplos")
    print("0. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == '1':
        ejemplo_paso_bajas()
    elif opcion == '2':
        ejemplo_paso_altas()
    elif opcion == '3':
        ejemplo_paso_banda()
    elif opcion == '4':
        # Diseño personalizado
        tipo = input("Tipo de filtro (lowpass, highpass, bandpass, bandstop): ")
        fs = float(input("Frecuencia de muestreo (Hz): "))
        
        if tipo.lower() in ['bandpass', 'bandstop']:
            f_low = float(input("Frecuencia de corte inferior (Hz): "))
            f_high = float(input("Frecuencia de corte superior (Hz): "))
            cutoff = (f_low/(fs/2), f_high/(fs/2))
        else:
            f_c = float(input("Frecuencia de corte (Hz): "))
            cutoff = f_c/(fs/2)
        
        order = int(input("Orden del filtro: "))
        window = input("Tipo de ventana (rectangular, hanning, hamming, blackman): ")
        
        h = design_filter(tipo, cutoff, order, window, fs)
        fig = plot_filter_response(h, f"{tipo.capitalize()} {window.capitalize()}", fs)
        plt.show()
        
        exportar = input("¿Desea exportar los coeficientes? (s/n): ")
        if exportar.lower() == 's':
            nombre = input("Nombre del archivo (sin extensión): ") or f"{tipo}_filter"
            export_filter_coeffs(h, f"{nombre}.csv")
    
    elif opcion == '5':
        ejemplo_paso_bajas()
        ejemplo_paso_altas()
        ejemplo_paso_banda()
    elif opcion == '0':
        print("¡Gracias por utilizar el diseñador de filtros FIR!")
    else:
        print("Opción no válida")

if __name__ == "__main__":
    main()
