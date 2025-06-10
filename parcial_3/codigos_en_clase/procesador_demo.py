#pip install sounddevice
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy import signal
from scipy.io import wavfile
import time

class DemoFiltros:
    def __init__(self, fs=8000):
        self.fs = fs
        self.nyquist = fs / 2
    
    def cargar_audio(self, archivo):
        try:
            fs_original, audio = wavfile.read(archivo)
            if audio.ndim > 1:
                audio = audio.mean(axis=1)  # Convertir a mono si es estéreo
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            if fs_original != self.fs:
                num_muestras = int(len(audio)) * self.fs / fs_original
                audio =  signal.resample(audio, num_muestras)
            
            max_muestra = self.fs * 5
            if len(audio) > max_muestra:
                audio = audio[:max_muestra]
            elif len(audio) < max_muestra:
                repeticiones = int(np.ceil(max_muestra / len(audio)))
                audio = np.tile(audio, repeticiones)[:max_muestra]
            
            duracion_final = len(audio) / self.fs
            return audio
        except Exception as e:
            print(f"Error al cargar el archivo de audio: {e}")
            return None
            
    def diseñar_filtro(self):
        fc = 800 / self.nyquist
        print("Diseño del filtro FIR:")
        h_fir = signal.firwin(41, fc, window='hamming')
        print("Diseñando un filtro IIR")
        b_iir, a_iir = signal.butter(5, fc, btype='low')
        return h_fir, b_iir, a_iir
    
    def aplicar_filtros(self, audio, h_fir, iir_coefs):
        b_iir, a_iir = iir_coefs

        audio_fir = signal.lfilter(h_fir, 1.0, audio)

        audio_iir = signal.lfilter(b_iir, a_iir, audio)

        return audio_fir, audio_iir

    def reproducir_comparacion (self, audio, audio_fir, audio_iir):
        
        #Normalizar audio para evitar clipping
        def normalizar(audio):
            max_val = np.max(np.abs(audio))
            if max_val > 0:
                return audio / max_val * 0.8
            return audio

        orig_norm = normalizar(audio)
        fir_norm = normalizar(audio_fir)
        iir_norm = normalizar(audio_iir)

        duracion = len(orig_norm) / self.fs

        try:
            input("Presione Enter para reproducir el audio original...")
            print("Reproduciendo audio original...")
            sd.play(orig_norm, self.fs)
            sd.wait()
            time.sleep(1)  # Esperar a que termine la reproducción
            
            input("Presione Enter para reproducir el audio filtrado FIR...")
            print("Reproduciendo audio filtrado FIR...")
            sd.play(fir_norm, self.fs)
            sd.wait()
            
            input("Presione Enter para reproducir el audio filtrado IIR...")
            print("Reproduciendo audio filtrado IIR...")
            sd.play(iir_norm, self.fs)
            sd.wait()
        except Exception as e:
            print(f"Error durante la reproducción: {e}")

    def analizar_espectros(self, audio_orig, audio_fir, audio_iir, h_fir, iir_coefs):
        b_iir, a_iir = iir_coefs

        # Limitar a 2 segundos de audio
        max_samples = int(self.fs * 2)
        audio_orig = audio_orig[:max_samples]
        audio_fir = audio_fir[:max_samples]
        audio_iir = audio_iir[:max_samples]

        # Calcular espectros
        f_orig, Pxx_orig = signal.welch(audio_orig, fs=self.fs, nperseg=1024)
        f_fir, Pxx_fir = signal.welch(audio_fir, fs=self.fs, nperseg=1024)
        f_iir, Pxx_iir = signal.welch(audio_iir, fs=self.fs, nperseg=1024)

        # Graficar espectros
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1)
        plt.semilogy(f_orig, Pxx_orig, label='Original', color='blue')
        plt.title('Espectro Original')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Densidad Espectral de Potencia (PSD)')
        plt.grid()
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.semilogy(f_fir, Pxx_fir, label='Filtrado FIR', color='orange')
        plt.title('Espectro Filtrado FIR')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Densidad Espectral de Potencia (PSD)')
        plt.grid()
        plt.legend()

        plt.subplot(2, 2, 3)
        plt.semilogy(f_iir, Pxx_iir, label='Filtrado IIR', color='green')
        plt.title('Espectro Filtrado IIR')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Densidad Espectral de Potencia (PSD)')
        plt.grid()
        plt.legend()

        # Resumen de diferencias
        plt.subplot(2, 2, 4)
        diff_fir = np.abs(Pxx_orig - Pxx_fir)
        diff_iir = np.abs(Pxx_orig - Pxx_iir)
        plt.plot(f_orig, diff_fir, label='Diferencia FIR', color='orange')
        plt.plot(f_orig, diff_iir, label='Diferencia IIR', color='green')
        plt.title('Diferencias entre Original y Filtrados')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Diferencia de PSD')
        plt.grid()
        plt.legend()

        plt.tight_layout()
        plt.show()
