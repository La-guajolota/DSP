import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os
from datetime import datetime

class DTMFFilterGenerator:
    """Generador de filtros digitales para detección DTMF en PlatformIO"""
    
    def __init__(self):
        self.fs = 8000  # Frecuencia de muestreo por defecto
        self.dtmf_frequencies = {
            'low': [697, 770, 852, 941],      # Frecuencias bajas
            'high': [1209, 1336, 1477, 1633] # Frecuencias altas
        }
    
    def design_fir_bandpass(self, center_freq, bandwidth, order=101, window='hamming'):
        """
        Diseña un filtro FIR pasabanda
        
        Args:
            center_freq: Frecuencia central en Hz
            bandwidth: Ancho de banda en Hz
            order: Orden del filtro (número de coeficientes)
            window: Tipo de ventana ('hamming', 'hanning', 'blackman', 'kaiser')
        
        Returns:
            tuple: (coeficientes_b, respuesta_frecuencia)
        """
        # Asegurar orden impar para filtros FIR
        if order % 2 == 0:
            order += 1
            
        # Calcular frecuencias de corte normalizadas
        nyquist = self.fs / 2
        low_cutoff = (center_freq - bandwidth/2) / nyquist
        high_cutoff = (center_freq + bandwidth/2) / nyquist
        
        # Limitar al rango válido [0.001, 0.999]
        low_cutoff = max(0.001, min(0.999, low_cutoff))
        high_cutoff = max(0.001, min(0.999, high_cutoff))
        
        # Diseñar filtro
        b = signal.firwin(order, [low_cutoff, high_cutoff], 
                         window=window, pass_zero=False)
        
        # Calcular respuesta en frecuencia
        w, h = signal.freqz(b, 1, worN=8000, fs=self.fs)
        
        return b, (w, h)
    
    def design_iir_bandpass(self, center_freq, bandwidth, order=2, filter_type='butter'):
        """
        Diseña un filtro IIR pasabanda
        
        Args:
            center_freq: Frecuencia central en Hz
            bandwidth: Ancho de banda en Hz
            order: Orden del filtro
            filter_type: Tipo de filtro ('butter', 'cheby1', 'cheby2', 'ellip')
        
        Returns:
            tuple: (coeficientes_b, coeficientes_a, respuesta_frecuencia)
        """
        # Calcular frecuencias de corte normalizadas
        nyquist = self.fs / 2
        low_cutoff = (center_freq - bandwidth/2) / nyquist
        high_cutoff = (center_freq + bandwidth/2) / nyquist
        
        # Limitar al rango válido
        low_cutoff = max(0.001, min(0.999, low_cutoff))
        high_cutoff = max(0.001, min(0.999, high_cutoff))
        
        # Diseñar filtro según el tipo
        if filter_type == 'butter':
            b, a = signal.butter(order, [low_cutoff, high_cutoff], btype='band')
        elif filter_type == 'cheby1':
            b, a = signal.cheby1(order, 1, [low_cutoff, high_cutoff], btype='band')
        elif filter_type == 'cheby2':
            b, a = signal.cheby2(order, 40, [low_cutoff, high_cutoff], btype='band')
        elif filter_type == 'ellip':
            b, a = signal.ellip(order, 1, 40, [low_cutoff, high_cutoff], btype='band')
        else:
            raise ValueError("Tipo de filtro no válido. Use: 'butter', 'cheby1', 'cheby2', 'ellip'")
        
        # Calcular respuesta en frecuencia
        w, h = signal.freqz(b, a, worN=8000, fs=self.fs)
        
        return b, a, (w, h)
    
    def analyze_filter_response(self, freq_response, center_freq, title="Filtro"):
        """Analiza y grafica la respuesta en frecuencia del filtro"""
        w, h = freq_response
        
        # Crear figura con subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        # Respuesta en magnitud (lineal)
        ax1.plot(w, np.abs(h), 'b-', linewidth=2)
        ax1.set_title(f'{title} - Respuesta en Magnitud')
        ax1.set_xlabel('Frecuencia (Hz)')
        ax1.set_ylabel('Ganancia')
        ax1.grid(True, alpha=0.3)
        ax1.axvline(center_freq, color='r', linestyle='--', alpha=0.7, label=f'{center_freq} Hz')
        ax1.legend()
        ax1.set_xlim(0, 2000)
        
        # Respuesta en magnitud (dB)
        ax2.plot(w, 20 * np.log10(np.abs(h) + 1e-10), 'b-', linewidth=2)
        ax2.set_title(f'{title} - Respuesta en dB')
        ax2.set_xlabel('Frecuencia (Hz)')
        ax2.set_ylabel('Ganancia (dB)')
        ax2.grid(True, alpha=0.3)
        ax2.axvline(center_freq, color='r', linestyle='--', alpha=0.7, label=f'{center_freq} Hz')
        ax2.legend()
        ax2.set_xlim(0, 2000)
        ax2.set_ylim(-80, 5)
        
        # Respuesta en fase
        ax3.plot(w, np.unwrap(np.angle(h)), 'g-', linewidth=2)
        ax3.set_title(f'{title} - Respuesta en Fase')
        ax3.set_xlabel('Frecuencia (Hz)')
        ax3.set_ylabel('Fase (radianes)')
        ax3.grid(True, alpha=0.3)
        ax3.axvline(center_freq, color='r', linestyle='--', alpha=0.7, label=f'{center_freq} Hz')
        ax3.legend()
        ax3.set_xlim(center_freq - 200, center_freq + 200)
        
        plt.tight_layout()
        return fig
    
    def generate_fir_header(self, coeffs, frequency, order, window='hamming'):
        """Genera archivo .h para filtro FIR"""
        header_content = f"""#ifndef FIR_{frequency}HZ_H
#define FIR_{frequency}HZ_H

//==============================================================================
// FILTRO FIR PASABANDA PARA {frequency} Hz
//==============================================================================
// Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Frecuencia de muestreo: {self.fs} Hz
// Orden del filtro: {order}
// Ventana utilizada: {window}
// Número de coeficientes: {len(coeffs)}

#define FILTER_FREQUENCY {frequency}
#define FILTER_LENGTH {len(coeffs)}
#define FILTER_ORDER {order}

// Coeficientes del filtro FIR
const float filter_coeffs[FILTER_LENGTH] = {{
"""
        
        # Agregar coeficientes con formato de 8 por línea
        for i, coeff in enumerate(coeffs):
            if i % 8 == 0:
                header_content += "    "
            header_content += f"{coeff:12.8f}f"
            if i < len(coeffs) - 1:
                header_content += ", "
            if (i + 1) % 8 == 0 or i == len(coeffs) - 1:
                header_content += "\n"
        
        header_content += f"""
}};

#endif // FIR_{frequency}HZ_H
"""
        return header_content
    
    def generate_iir_header(self, b_coeffs, a_coeffs, frequency, order, filter_type='butter'):
        """Genera archivo .h para filtro IIR"""
        header_content = f"""#ifndef IIR_{frequency}HZ_H
#define IIR_{frequency}HZ_H

//==============================================================================
// FILTRO IIR PASABANDA PARA {frequency} Hz
//==============================================================================
// Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Frecuencia de muestreo: {self.fs} Hz
// Orden del filtro: {order}
// Tipo de filtro: {filter_type}

#define FILTER_FREQUENCY {frequency}
#define IIR_ORDER {order}

// Coeficientes del denominador (feedback) - polos
const float a_coeffs[IIR_ORDER + 1] = {{
"""
        
        # Agregar coeficientes a
        for i, coeff in enumerate(a_coeffs):
            header_content += f"    {coeff:12.8f}f"
            if i < len(a_coeffs) - 1:
                header_content += ","
            header_content += f"    // a[{i}]\n"
        
        header_content += """};

// Coeficientes del numerador (feedforward) - zeros
const float b_coeffs[IIR_ORDER + 1] = {
"""
        
        # Agregar coeficientes b
        for i, coeff in enumerate(b_coeffs):
            header_content += f"    {coeff:12.8f}f"
            if i < len(b_coeffs) - 1:
                header_content += ","
            header_content += f"    // b[{i}]\n"
        
        header_content += f"""
}};

#endif // IIR_{frequency}HZ_H
"""
        return header_content
    
    def generate_single_filter(self, center_freq, bandwidth, filter_type='fir', 
                             order=101, window='hamming', iir_type='butter', 
                             output_dir='filters', show_plot=True):
        """
        Genera un filtro individual
        
        Args:
            center_freq: Frecuencia central en Hz
            bandwidth: Ancho de banda en Hz
            filter_type: 'fir' o 'iir'
            order: Orden del filtro
            window: Ventana para FIR ('hamming', 'hanning', 'blackman', 'kaiser')
            iir_type: Tipo de filtro IIR ('butter', 'cheby1', 'cheby2', 'ellip')
            output_dir: Directorio de salida
            show_plot: Mostrar gráficas
        """
        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        if filter_type.lower() == 'fir':
            # Generar filtro FIR
            coeffs, freq_resp = self.design_fir_bandpass(center_freq, bandwidth, order, window)
            
            # Generar archivo header
            header_content = self.generate_fir_header(coeffs, center_freq, order, window)
            filename = f"fir_{center_freq}hz.h"
            
            # Título para gráficas
            title = f"Filtro FIR {center_freq} Hz (Orden {order}, {window})"
            
        elif filter_type.lower() == 'iir':
            # Generar filtro IIR
            b_coeffs, a_coeffs, freq_resp = self.design_iir_bandpass(center_freq, bandwidth, order, iir_type)
            
            # Generar archivo header
            header_content = self.generate_iir_header(b_coeffs, a_coeffs, center_freq, order, iir_type)
            filename = f"iir_{center_freq}hz.h"
            
            # Título para gráficas
            title = f"Filtro IIR {center_freq} Hz (Orden {order}, {iir_type})"
            
        else:
            raise ValueError("filter_type debe ser 'fir' o 'iir'")
        
        # Guardar archivo header
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(header_content)
        
        print(f"✓ Generado: {filepath}")
        
        # Mostrar análisis si se solicita
        if show_plot:
            fig = self.analyze_filter_response(freq_resp, center_freq, title)
            plot_filename = os.path.join(output_dir, f"{filter_type}_{center_freq}hz_response.png")
            fig.savefig(plot_filename, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfica guardada: {plot_filename}")
            plt.show()
        
        return filepath
    
    def generate_dtmf_filter_set(self, bandwidth=30, filter_type='fir', order=101, 
                               window='hamming', iir_type='butter', output_dir='dtmf_filters'):
        """
        Genera el conjunto completo de filtros DTMF
        
        Args:
            bandwidth: Ancho de banda en Hz
            filter_type: 'fir', 'iir', o 'both'
            order: Orden del filtro
            window: Ventana para FIR
            iir_type: Tipo de filtro IIR
            output_dir: Directorio de salida
        """
        print(f"=== Generando filtros DTMF ===")
        print(f"Tipo: {filter_type.upper()}")
        print(f"Ancho de banda: {bandwidth} Hz")
        print(f"Orden: {order}")
        if filter_type in ['fir', 'both']:
            print(f"Ventana FIR: {window}")
        if filter_type in ['iir', 'both']:
            print(f"Tipo IIR: {iir_type}")
        print(f"Directorio: {output_dir}")
        print("-" * 50)
        
        # Crear directorio
        os.makedirs(output_dir, exist_ok=True)
        
        # Generar filtros para todas las frecuencias DTMF
        all_frequencies = self.dtmf_frequencies['low'] + self.dtmf_frequencies['high']
        generated_files = []
        
        for freq in all_frequencies:
            print(f"Procesando {freq} Hz...")
            
            if filter_type in ['fir', 'both']:
                filepath = self.generate_single_filter(
                    freq, bandwidth, 'fir', order, window, 
                    output_dir=output_dir, show_plot=False
                )
                generated_files.append(filepath)
            
            if filter_type in ['iir', 'both']:
                filepath = self.generate_single_filter(
                    freq, bandwidth, 'iir', order, window, iir_type,
                    output_dir=output_dir, show_plot=False
                )
                generated_files.append(filepath)
        
        # Generar archivo de configuración
        config_file = self.generate_config_file(all_frequencies, filter_type, output_dir)
        generated_files.append(config_file)
        
        print(f"\n✓ Generación completada!")
        print(f"✓ {len(generated_files)} archivos generados en '{output_dir}'")
        
        return generated_files
    
    def generate_config_file(self, frequencies, filter_type, output_dir):
        """Genera archivo de configuración con todas las inclusiones"""
        config_content = f"""#ifndef DTMF_FILTERS_CONFIG_H
#define DTMF_FILTERS_CONFIG_H

//==============================================================================
// CONFIGURACIÓN DE FILTROS DTMF
//==============================================================================
// Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Frecuencias DTMF disponibles: {', '.join(map(str, frequencies))} Hz

// Para usar un filtro específico, descomenta UNA de las siguientes líneas:

"""
        
        for freq in frequencies:
            if filter_type in ['fir', 'both']:
                config_content += f'// #include "fir_{freq}hz.h"     // Filtro FIR para {freq} Hz\n'
            if filter_type in ['iir', 'both']:
                config_content += f'// #include "iir_{freq}hz.h"     // Filtro IIR para {freq} Hz\n'
        
        config_content += """
// Ejemplo de uso en main.cpp:
// 1. Incluye este archivo: #include "dtmf_filters_config.h"
// 2. Descomenta el filtro que desees usar arriba
// 3. Compila y carga a tu ESP32

#endif // DTMF_FILTERS_CONFIG_H
"""
        
        config_filepath = os.path.join(output_dir, 'dtmf_filters_config.h')
        with open(config_filepath, 'w') as f:
            f.write(config_content)
        
        print(f"✓ Configuración generada: {config_filepath}")
        return config_filepath
    
    def compare_filters(self, center_freq, bandwidth, fir_order=101, iir_order=2, 
                       window='hamming', iir_type='butter'):
        """Compara filtros FIR e IIR para una frecuencia dada"""
        print(f"Comparando filtros para {center_freq} Hz...")
        
        # Generar ambos filtros
        fir_coeffs, fir_resp = self.design_fir_bandpass(center_freq, bandwidth, fir_order, window)
        iir_b, iir_a, iir_resp = self.design_iir_bandpass(center_freq, bandwidth, iir_order, iir_type)
        
        # Crear gráfica comparativa
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Respuesta en magnitud
        ax1.plot(fir_resp[0], np.abs(fir_resp[1]), 'b-', linewidth=2, label=f'FIR (Orden {fir_order})')
        ax1.plot(iir_resp[0], np.abs(iir_resp[1]), 'r--', linewidth=2, label=f'IIR (Orden {iir_order})')
        ax1.set_title(f'Respuesta en Magnitud - {center_freq} Hz')
        ax1.set_xlabel('Frecuencia (Hz)')
        ax1.set_ylabel('Ganancia')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.set_xlim(center_freq - 200, center_freq + 200)
        
        # Respuesta en dB
        ax2.plot(fir_resp[0], 20*np.log10(np.abs(fir_resp[1]) + 1e-10), 'b-', linewidth=2, label=f'FIR (Orden {fir_order})')
        ax2.plot(iir_resp[0], 20*np.log10(np.abs(iir_resp[1]) + 1e-10), 'r--', linewidth=2, label=f'IIR (Orden {iir_order})')
        ax2.set_title(f'Respuesta en dB - {center_freq} Hz')
        ax2.set_xlabel('Frecuencia (Hz)')
        ax2.set_ylabel('Ganancia (dB)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_xlim(0, 2000)
        ax2.set_ylim(-80, 5)
        
        # Respuesta en fase
        ax3.plot(fir_resp[0], np.unwrap(np.angle(fir_resp[1])), 'b-', linewidth=2, label=f'FIR (Orden {fir_order})')
        ax3.plot(iir_resp[0], np.unwrap(np.angle(iir_resp[1])), 'r--', linewidth=2, label=f'IIR (Orden {iir_order})')
        ax3.set_title(f'Respuesta en Fase - {center_freq} Hz')
        ax3.set_xlabel('Frecuencia (Hz)')
        ax3.set_ylabel('Fase (radianes)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        ax3.set_xlim(center_freq - 200, center_freq + 200)
        
        # Respuesta al impulso
        ax4.stem(range(len(fir_coeffs)), fir_coeffs, linefmt='b-', markerfmt='bo', label=f'FIR (Orden {fir_order})')
        
        # Para IIR, calculamos respuesta al impulso
        impulse = np.zeros(50)
        impulse[0] = 1
        iir_impulse_resp = signal.lfilter(iir_b, iir_a, impulse)
        ax4.stem(range(len(iir_impulse_resp)), iir_impulse_resp, linefmt='r--', markerfmt='r^', label=f'IIR (Orden {iir_order})')
        
        ax4.set_title('Respuesta al Impulso')
        ax4.set_xlabel('Muestras')
        ax4.set_ylabel('Amplitud')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plt.tight_layout()
        plt.show()
        
        return fig

# =============================================================================
# FUNCIONES DE UTILIDAD PARA USO INTERACTIVO
# =============================================================================

def generate_interactive():
    """Función interactiva para generar filtros"""
    generator = DTMFFilterGenerator()
    
    print("=== Generador Interactivo de Filtros DTMF ===\n")
    
    # Selección de modo
    print("Selecciona el modo:")
    print("1. Generar filtro individual")
    print("2. Generar conjunto completo DTMF")
    print("3. Comparar filtros FIR vs IIR")
    
    mode = input("\nOpción (1-3): ").strip()
    
    if mode == '1':
        # Filtro individual
        freq = float(input("Frecuencia central (Hz): "))
        bandwidth = float(input("Ancho de banda (Hz) [30]: ") or "30")
        filter_type = input("Tipo de filtro (fir/iir) [fir]: ").lower() or "fir"
        order = int(input("Orden del filtro [101 para FIR, 2 para IIR]: ") or ("101" if filter_type == "fir" else "2"))
        
        if filter_type == 'fir':
            window = input("Ventana (hamming/hanning/blackman/kaiser) [hamming]: ") or "hamming"
            generator.generate_single_filter(freq, bandwidth, filter_type, order, window)
        else:
            iir_type = input("Tipo IIR (butter/cheby1/cheby2/ellip) [butter]: ") or "butter"
            generator.generate_single_filter(freq, bandwidth, filter_type, order, iir_type=iir_type)
    
    elif mode == '2':
        # Conjunto completo
        bandwidth = float(input("Ancho de banda (Hz) [30]: ") or "30")
        filter_type = input("Tipo de filtro (fir/iir/both) [fir]: ").lower() or "fir"
        order = int(input("Orden del filtro [101 para FIR, 2 para IIR]: ") or ("101" if filter_type == "fir" else "2"))
        
        generator.generate_dtmf_filter_set(bandwidth, filter_type, order)
    
    elif mode == '3':
        # Comparación
        freq = float(input("Frecuencia para comparar (Hz): "))
        bandwidth = float(input("Ancho de banda (Hz) [30]: ") or "30")
        fir_order = int(input("Orden FIR [101]: ") or "101")
        iir_order = int(input("Orden IIR [2]: ") or "2")
        
        generator.compare_filters(freq, bandwidth, fir_order, iir_order)

# =============================================================================
# EJEMPLOS DE USO
# =============================================================================

if __name__ == "__main__":
    # Crear instancia del generador
    generator = DTMFFilterGenerator()
    
    # Ejemplo 1: Generar un filtro FIR individual
    print("Ejemplo 1: Filtro FIR para 697 Hz")
    generator.generate_single_filter(
        center_freq=697,
        bandwidth=30,
        filter_type='fir',
        order=101,
        window='hamming'
    )
    
    # Ejemplo 2: Generar un filtro IIR individual
    print("\nEjemplo 2: Filtro IIR para 1209 Hz")
    generator.generate_single_filter(
        center_freq=1209,
        bandwidth=30,
        filter_type='iir',
        order=2,
        iir_type='butter'
    )
    
    # Ejemplo 3: Generar conjunto completo DTMF
    print("\nEjemplo 3: Conjunto completo de filtros FIR")
    generator.generate_dtmf_filter_set(
        bandwidth=30,
        filter_type='fir',
        order=101,
        window='hamming'
    )
    
    # Ejemplo 4: Comparar filtros
    print("\nEjemplo 4: Comparación FIR vs IIR para 697 Hz")
    generator.compare_filters(697, 30, fir_order=101, iir_order=2)
    
    # Descomentar para modo interactivo
    generate_interactive()