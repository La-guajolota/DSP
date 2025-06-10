#!/usr/bin/env python3


import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import sounddevice as sd
import time

class DemoFiltrosSimple:
    def __init__(self, fs=8000):
        self.fs = fs
        self.nyquist = fs / 2
        
    def cargar_audio(self, archivo):
        """Carga archivo de audio y lo prepara para 5 segundos"""
        try:
            fs_orig, audio = wavfile.read(archivo)
            print(f"Cargando {archivo}...")
            print(f"   Fs original: {fs_orig} Hz")
            print(f"   Muestras: {len(audio)}")
            
            # Convertir a mono si es estéreo
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1)
                print("   Convertido a mono")
            
            # Convertir a float
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            
            # Remuestrear si es necesario
            if fs_orig != self.fs:
                num_samples = int(len(audio) * self.fs / fs_orig)
                audio = signal.resample(audio, num_samples)
                print(f"   Remuestreado a {self.fs} Hz")
            
            # Mantener 5 segundos completos
            max_samples = self.fs * 5  # 5 segundos exactos
            if len(audio) > max_samples:
                audio = audio[:max_samples]
                print(f"   Mantenido en 5 segundos exactos")
            elif len(audio) < max_samples:
                # Si es muy corto, extender
                repeticiones = int(np.ceil(max_samples / len(audio)))
                audio = np.tile(audio, repeticiones)[:max_samples]
                print(f"   Audio extendido a 5 segundos")
            
            duracion_final = len(audio) / self.fs
            print(f"Audio listo: {len(audio)} muestras, {duracion_final:.1f} segundos")
            return audio
            
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")
            return None
    
    def diseñar_filtros(self):
        """Diseña filtros optimizados para diferencias audibles claras"""
        
        # Frecuencia de corte más baja para diferencias más evidentes
        fc = 800 / self.nyquist  # 800 Hz en lugar de 1000 Hz
        
        # Filtro FIR - Orden mayor para mejor selectividad
        print("Diseñando filtro FIR...")
        h_fir = signal.firwin(41, fc, window='hamming')  # Orden 40
        print(f"   Orden: {len(h_fir)-1}")
        print(f"   Frecuencia de corte: 800 Hz")
        
        # Filtro IIR - Butterworth orden mayor para corte más abrupto
        print("Diseñando filtro IIR...")
        b_iir, a_iir = signal.butter(6, fc, btype='low')  # Orden 6
        print(f"   Orden: {len(b_iir)-1}")
        print(f"   Frecuencia de corte: 800 Hz")
        
        return h_fir, (b_iir, a_iir)
    
    def aplicar_filtros(self, audio, h_fir, iir_coeffs):
        """Aplica filtros FIR e IIR al audio de 5 segundos"""
        
        b_iir, a_iir = iir_coeffs
        
        print("Aplicando filtros a audio de 5 segundos...")
        
        # Aplicar FIR
        print("   Procesando con FIR...")
        audio_fir = signal.lfilter(h_fir, 1, audio)
        
        # Aplicar IIR  
        print("   Procesando con IIR...")
        audio_iir = signal.lfilter(b_iir, a_iir, audio)
        
        print("Filtrado completado - 5 segundos cada señal")
        
        return audio_fir, audio_iir
    
    def reproducir_comparacion(self, audio_orig, audio_fir, audio_iir):
        """Reproduce audio completo de 5 segundos para comparación clara"""
        
        # Normalizar conservando diferencias
        def normalizar_conservando_diferencias(audio):
            max_val = np.max(np.abs(audio))
            if max_val > 0:
                return audio / max_val * 0.8  # 80% del máximo para claridad
            return audio
        
        orig_norm = normalizar_conservando_diferencias(audio_orig)
        fir_norm = normalizar_conservando_diferencias(audio_fir)
        iir_norm = normalizar_conservando_diferencias(audio_iir)
        
        duracion = len(orig_norm) / self.fs
        
        print(f"\nCOMPARACIÓN AUDITIVA EXTENDIDA:")
        print(f"   Duración de cada audio: {duracion:.1f} segundos")
        print("=" * 60)
        
        try:
            # Audio original
            print("1. AUDIO ORIGINAL (con ruido de alta frecuencia)")
            print("   Escucha atentamente el ruido y los tonos agudos...")
            input("   Presiona Enter para reproducir...")
            sd.play(orig_norm, self.fs)
            sd.wait()
            time.sleep(1)
            
            # Audio FIR
            print("\n2. FILTRO FIR (suavizado gradual)")
            print("   Nota cómo se reduce el ruido pero conserva naturalidad...")
            input("   Presiona Enter para reproducir...")
            sd.play(fir_norm, self.fs)
            sd.wait()
            time.sleep(1)
            
            # Audio IIR
            print("\n3. FILTRO IIR (corte más abrupto)")
            print("   Escucha el corte más pronunciado de frecuencias altas...")
            input("   Presiona Enter para reproducir...")
            sd.play(iir_norm, self.fs)
            sd.wait()
            time.sleep(1)
            
            # Reproducción comparativa rápida
            print("\nCOMPARACIÓN RÁPIDA (sin pausas):")
            print("Original → FIR → IIR")
            time.sleep(2)
            
            print("Audio Original...")
            sd.play(orig_norm, self.fs)
            sd.wait()
            time.sleep(0.5)
            
            print("Audio FIR...")
            sd.play(fir_norm, self.fs)
            sd.wait()
            time.sleep(0.5)
            
            print("Audio IIR...")
            sd.play(iir_norm, self.fs)
            sd.wait()
            
            print("\nDIFERENCIAS CLAVE:")
            print("    Original: Más ruido, sonido 'áspero'")
            print("    FIR: Suavizado gradual, mantiene naturalidad")
            print("    IIR: Corte abrupto, puede sonar 'apagado'")
            print("    Para música: FIR es mejor")
            print("    Para telecomunicaciones: IIR es más eficiente")
            
        except Exception as e:
            print(f"Error en reproducción: {e}")
            print("   Verifica configuración de audio del sistema")
    
    def analizar_espectros(self, audio_orig, audio_fir, audio_iir, h_fir, iir_coeffs):
        """Muestra análisis espectral comparativo de audio de 5 segundos"""
        
        print("Generando análisis espectral de 5 segundos...")
        
        b_iir, a_iir = iir_coeffs
        
        # Calcular espectros con mayor resolución
        f, Pxx_orig = signal.welch(audio_orig, self.fs, nperseg=1024)
        f, Pxx_fir = signal.welch(audio_fir, self.fs, nperseg=1024)
        f, Pxx_iir = signal.welch(audio_iir, self.fs, nperseg=1024)
        
        # Crear gráficas
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('Análisis Comparativo de Filtros Digitales - Audio 5 segundos', fontsize=16)
        
        # Señales en tiempo - mostrar primeros 2 segundos
        t = np.arange(len(audio_orig)) / self.fs
        muestras_mostrar = self.fs * 2  # 2 segundos
        axes[0, 0].plot(t[:muestras_mostrar], audio_orig[:muestras_mostrar], 'b-', alpha=0.7, label='Original')
        axes[0, 0].plot(t[:muestras_mostrar], audio_fir[:muestras_mostrar], 'g-', linewidth=2, label='FIR')
        axes[0, 0].plot(t[:muestras_mostrar], audio_iir[:muestras_mostrar], 'r-', linewidth=2, label='IIR')
        axes[0, 0].set_title('Señales en el Dominio del Tiempo (primeros 2s)')
        axes[0, 0].set_xlabel('Tiempo (s)')
        axes[0, 0].set_ylabel('Amplitud')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Espectros comparativos
        axes[0, 1].semilogy(f, Pxx_orig, 'b-', alpha=0.7, label='Original')
        axes[0, 1].semilogy(f, Pxx_fir, 'g-', linewidth=2, label='FIR')
        axes[0, 1].semilogy(f, Pxx_iir, 'r-', linewidth=2, label='IIR')
        axes[0, 1].set_title('Espectros de Potencia')
        axes[0, 1].set_xlabel('Frecuencia (Hz)')
        axes[0, 1].set_ylabel('PSD (V²/Hz)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_xlim([0, self.fs/2])
        axes[0, 1].axvline(800, color='k', linestyle='--', alpha=0.5, linewidth=2, label='fc=800Hz')
        
        # Respuesta en frecuencia de los filtros
        w_fir, H_fir = signal.freqz(h_fir, 1, worN=1024, fs=self.fs)
        w_iir, H_iir = signal.freqz(b_iir, a_iir, worN=1024, fs=self.fs)
        
        axes[1, 0].plot(w_fir, 20*np.log10(np.abs(H_fir)), 'g-', linewidth=3, label='FIR')
        axes[1, 0].plot(w_iir, 20*np.log10(np.abs(H_iir)), 'r-', linewidth=3, label='IIR')
        axes[1, 0].set_title('Respuesta en Frecuencia de los Filtros')
        axes[1, 0].set_xlabel('Frecuencia (Hz)')
        axes[1, 0].set_ylabel('Magnitud (dB)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_xlim([0, self.fs/2])
        axes[1, 0].axhline(-3, color='k', linestyle=':', alpha=0.5, linewidth=2, label='-3dB')
        axes[1, 0].axvline(800, color='k', linestyle='--', alpha=0.5, linewidth=2)
        
        # Métricas comparativas
        axes[1, 1].axis('off')
        
        # Calcular métricas
        snr_orig = self.calcular_snr(audio_orig)
        snr_fir = self.calcular_snr(audio_fir)
        snr_iir = self.calcular_snr(audio_iir)
        
        # Buscar atenuación en 800 Hz
        idx_800_fir = np.argmin(np.abs(w_fir - 800))
        idx_800_iir = np.argmin(np.abs(w_iir - 800))
        atenuacion_800_fir = 20*np.log10(np.abs(H_fir[idx_800_fir]))
        atenuacion_800_iir = 20*np.log10(np.abs(H_iir[idx_800_iir]))
        
        # Calcular reducción de ruido
        potencia_orig = np.var(audio_orig)
        potencia_fir = np.var(audio_fir)
        potencia_iir = np.var(audio_iir)
        
        reduccion_fir = 10 * np.log10(potencia_orig / potencia_fir) if potencia_fir > 0 else 0
        reduccion_iir = 10 * np.log10(potencia_orig / potencia_iir) if potencia_iir > 0 else 0
        
        metricas_texto = f"""
MÉTRICAS DE AUDIO DE 5 SEGUNDOS:

SNR (Relación Señal/Ruido):
• Original: {snr_orig:.1f} dB
• FIR:      {snr_fir:.1f} dB
• IIR:      {snr_iir:.1f} dB

Atenuación @ fc=800Hz:
• FIR: {atenuacion_800_fir:.1f} dB
• IIR: {atenuacion_800_iir:.1f} dB

Reducción de Potencia:
• FIR: {reduccion_fir:.1f} dB
• IIR: {reduccion_iir:.1f} dB

Características:
• FIR: Fase lineal, estable
• IIR: Más eficiente, corte abrupto

Ganador SNR: {'FIR' if snr_fir > snr_iir else 'IIR'}

DURACIÓN PROCESADA: 5.0 segundos
        """
        
        axes[1, 1].text(0.1, 0.9, metricas_texto, transform=axes[1, 1].transAxes,
                        fontsize=11, verticalalignment='top', fontfamily='monospace',
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        return snr_orig, snr_fir, snr_iir
    
    def calcular_snr(self, audio):
        """Calcula SNR estimado para audio de 5 segundos"""
        try:
            # Filtro paso-bajas muy suave para separar señal de ruido
            b_smooth, a_smooth = signal.butter(2, 0.1, btype='low')
            señal_estimada = signal.filtfilt(b_smooth, a_smooth, audio)
            ruido_estimado = audio - señal_estimada
            
            potencia_señal = np.var(señal_estimada)
            potencia_ruido = np.var(ruido_estimado)
            
            if potencia_ruido > 0:
                return 10 * np.log10(potencia_señal / potencia_ruido)
            else:
                return float('inf')
        except:
            return 20.0  # Valor por defecto
    
    def demo_completa(self, archivo):
        """Ejecuta demostración completa con audio de 5 segundos"""
        
        print("INICIANDO DEMOSTRACIÓN DE FILTROS DIGITALES")
        print("Audio optimizado de 5 segundos para diferencias claras")
        print("=" * 65)
        
        # 1. Cargar audio
        audio_orig = self.cargar_audio(archivo)
        if audio_orig is None:
            return
        
        # 2. Diseñar filtros
        h_fir, iir_coeffs = self.diseñar_filtros()
        
        # 3. Aplicar filtros
        audio_fir, audio_iir = self.aplicar_filtros(audio_orig, h_fir, iir_coeffs)
        
        # 4. Análisis visual
        snr_orig, snr_fir, snr_iir = self.analizar_espectros(audio_orig, audio_fir, audio_iir, h_fir, iir_coeffs)
        
        # 5. Comparación auditiva
        respuesta = input("\n¿Reproducir comparación auditiva de 5 segundos? (s/n): ")
        if respuesta.lower() in ['s', 'si', 'y', 'yes', '']:
            self.reproducir_comparacion(audio_orig, audio_fir, audio_iir)
        
        # 6. Resumen final detallado
        print("\nRESUMEN DETALLADO DE LA DEMOSTRACIÓN:")
        print("=" * 65)
        print(f"Archivo procesado: {archivo}")
        print(f"Duración procesada: {len(audio_orig)/self.fs:.1f} segundos")
        print(f"Frecuencia de corte: 800 Hz")
        print(f"")
        print(f"MÉTRICAS DE CALIDAD:")
        print(f"   SNR Original: {snr_orig:.1f} dB")
        print(f"   SNR FIR:      {snr_fir:.1f} dB (mejora: {snr_fir-snr_orig:+.1f} dB)")
        print(f"   SNR IIR:      {snr_iir:.1f} dB (mejora: {snr_iir-snr_orig:+.1f} dB)")
        print(f"   Mejor SNR: {'FIR' if snr_fir > snr_iir else 'IIR'}")
        print(f"")
        print(f"CONCLUSIONES PARA ESTUDIANTES:")
        print(f"   • FILTRO FIR:")
        print(f"     - Fase lineal (no distorsiona forma de onda)")
        print(f"     - Siempre estable")
        print(f"     - Mejor para audio y música")
        print(f"     - Mayor carga computacional")
        print(f"   • FILTRO IIR:")
        print(f"     - Más eficiente computacionalmente")
        print(f"     - Corte más selectivo y abrupto")
        print(f"     - Mejor para telecomunicaciones")
        print(f"     - Puede introducir distorsión de fase")
        print(f"")
        print(f"APLICACIONES REALES:")
        print(f"   • Spotify/Apple Music: Usan FIR (calidad)")
        print(f"   • WhatsApp/Zoom: Usan IIR (eficiencia)")
        print(f"   • Sistemas embebidos: IIR (memoria limitada)")
        print(f"   • Audio profesional: FIR (fidelidad)")
        
        print(f"\nDEMOSTRACIÓN EXITOSA - LISTO PARA CLASE")

def main():
    """Función principal para ejecutar la demostración MEJORADA"""
    
    print("DEMOSTRACIÓN DE FILTROS DIGITALES - VERSIÓN MEJORADA")
    print("Optimizada para audio de 5 segundos con diferencias claras")
    print("Compatible con bocinas de laptop y auriculares")
    print("=" * 65)
    
    # Crear instancia del demo
    demo = DemoFiltrosSimple()
    
    # Verificar archivos disponibles
    import os
    archivos_disponibles = [f for f in os.listdir('.') if f.endswith('.wav')]
    
    if not archivos_disponibles:
        print("No se encontraron archivos .wav")
        print("SOLUCION:")
        print("   1. Ejecuta: python generador_audio_mejorado.py")
        print("   2. Esto creará 3 archivos de 5 segundos optimizados")
        print("   3. Luego ejecuta este programa nuevamente")
        return
    
    print("Archivos de audio disponibles:")
    for i, archivo in enumerate(archivos_disponibles):
        try:
            from scipy.io import wavfile
            fs, audio = wavfile.read(archivo)
            duracion = len(audio) / fs
            print(f"   {i+1}. {archivo} ({duracion:.1f}s, {fs}Hz)")
        except:
            print(f"   {i+1}. {archivo} (error al leer)")
    
    # Seleccionar archivo
    print(f"\nRECOMENDACION PARA DEMO EN CLASE:")
    print(f"   - voz_con_ruido.wav: Mejor para demostrar filtrado de voz")
    print(f"   - multifrecuencia_test.wav: Mejor para mostrar selectividad")
    print(f"   - musica_sintetica.wav: Mejor para calidad musical")
    
    try:
        opcion = int(input(f"\nSelecciona archivo (1-{len(archivos_disponibles)}): ")) - 1
        archivo_seleccionado = archivos_disponibles[opcion]
    except:
        print("Selección inválida, usando primer archivo disponible")
        archivo_seleccionado = archivos_disponibles[0]
    
    print(f"\nINICIANDO DEMO CON: {archivo_seleccionado}")
    print("=" * 65)
    
    # Ejecutar demostración
    try:
        demo.demo_completa(archivo_seleccionado)
        
        print("\n¡DEMOSTRACIÓN COMPLETADA EXITOSAMENTE!")
        print("=" * 65)
        print("Audio de 5 segundos procesado")
        print("Diferencias claras entre FIR e IIR")
        print("Gráficas comparativas generadas")
        print("Métricas de calidad calculadas")
        print("Lista para presentar en clase")
        
        print(f"\nTIPS PARA LA CLASE:")
        print(f"   • Enfatiza las diferencias auditivas")
        print(f"   • Muestra las gráficas espectrales")
        print(f"   • Pregunta cuál prefieren para música vs telecom")
        print(f"   • Destaca las aplicaciones reales (Spotify vs WhatsApp)")
        
    except Exception as e:
        print(f"\nError durante la demostración: {e}")
        print("Posibles soluciones:")
        print("   1. Verifica que todas las librerías estén instaladas")
        print("   2. Asegúrate de que el audio funcione en tu sistema")
        print("   3. Intenta con un archivo diferente")

if __name__ == "__main__":
    main()
