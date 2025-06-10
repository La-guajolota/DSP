#!/usr/bin/env python3

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def generar_archivos_prueba():
    """Genera archivos de audio de prueba MEJORADOS para demostración clara"""
    
    fs = 8000  # Frecuencia de muestreo
    duracion = 5  # 5 segundos para mejor demo
    t = np.linspace(0, duracion, int(fs * duracion))
    
    print("Generando archivos de audio MEJORADOS para demo clara...")
    
    # 1. Señal de voz sintética con más ruido de alta frecuencia
    print("  Creando voz_con_ruido.wav...")
    frecuencias_voz = [200, 400, 600, 800]  # Frecuencias de voz
    amplitudes = [0.4, 0.35, 0.25, 0.15]
    
    voz = np.zeros_like(t)
    for f, a in zip(frecuencias_voz, amplitudes):
        voz += a * np.sin(2*np.pi*f*t)
    
    # Añadir modulación de voz más realista
    modulacion = 1 + 0.4*np.sin(2*np.pi*2*t) + 0.2*np.sin(2*np.pi*5*t)
    voz = voz * modulacion
    
    # Añadir MUCHO ruido de alta frecuencia para hacer evidente el filtrado
    ruido_hf = (0.15 * np.sin(2*np.pi*1500*t) +     # Ruido a 1500 Hz
                0.12 * np.sin(2*np.pi*2000*t) +     # Ruido a 2000 Hz
                0.10 * np.sin(2*np.pi*2500*t) +     # Ruido a 2500 Hz
                0.08 * np.random.randn(len(t)))     # Ruido blanco
    
    voz_con_ruido = voz + ruido_hf
    
    # Normalizar y guardar
    voz_normalizada = np.int16(voz_con_ruido / np.max(np.abs(voz_con_ruido)) * 32767 * 0.85)
    wavfile.write('voz_con_ruido.wav', fs, voz_normalizada)
    
    # 2. Señal multi-frecuencia para probar selectividad
    print("  Creando multifrecuencia_test.wav...")
    f_bajas = [300, 500, 700]      # Deben pasar (< 800 Hz)
    f_altas = [1200, 1800, 2400]   # Deben atenuarse (> 800 Hz)
    
    señal_bajas = sum(0.2 * np.sin(2*np.pi*f*t) for f in f_bajas)
    señal_altas = sum(0.2 * np.sin(2*np.pi*f*t) for f in f_altas)
    
    # Combinar con modulación temporal para hacer más interesante
    envelope = 0.5 + 0.5 * np.sin(2*np.pi*0.5*t)  # Modulación lenta
    multifrecuencia = (señal_bajas + señal_altas) * envelope
    
    # Añadir ruido para hacer más realista
    ruido = 0.08 * np.random.randn(len(t))
    multifrecuencia_final = multifrecuencia + ruido
    
    multi_norm = np.int16(multifrecuencia_final / np.max(np.abs(multifrecuencia_final)) * 32767 * 0.85)
    wavfile.write('multifrecuencia_test.wav', fs, multi_norm)
    
    # 3. Música sintética con armónicos
    print("  Creando musica_sintetica.wav...")
    # Notas musicales con armónicos
    notas = [261.63, 293.66, 329.63, 349.23]  # Do, Re, Mi, Fa
    
    musica = np.zeros_like(t)
    for i, nota in enumerate(notas):
        inicio = i * len(t) // 4
        fin = (i + 1) * len(t) // 4
        t_nota = t[inicio:fin]
        
        # Fundamental + armónicos
        nota_completa = (0.5 * np.sin(2*np.pi*nota*t_nota) +           # Fundamental
                        0.3 * np.sin(2*np.pi*nota*2*t_nota) +          # 2do armónico
                        0.2 * np.sin(2*np.pi*nota*3*t_nota) +          # 3er armónico
                        0.1 * np.sin(2*np.pi*nota*4*t_nota))           # 4to armónico
        
        musica[inicio:fin] = nota_completa
    
    # Añadir ruido de alta frecuencia para demostrar filtrado
    ruido_musical = 0.12 * np.sin(2*np.pi*3000*t) + 0.08 * np.random.randn(len(t))
    musica_con_ruido = musica + ruido_musical
    
    musica_norm = np.int16(musica_con_ruido / np.max(np.abs(musica_con_ruido)) * 32767 * 0.85)
    wavfile.write('musica_sintetica.wav', fs, musica_norm)
    
    print("Archivos de audio MEJORADOS creados:")
    print("  - voz_con_ruido.wav (5s - voz con ruido de alta freq)")
    print("  - multifrecuencia_test.wav (5s - frecuencias bajas y altas)")
    print("  - musica_sintetica.wav (5s - notas musicales con armónicos)")
    print("  Todos optimizados para demostrar diferencias claras entre filtros")
    
    # Mostrar espectro de las señales
    mostrar_espectros(voz_con_ruido, multifrecuencia_final, musica_con_ruido, fs)
    
    return ['voz_con_ruido.wav', 'multifrecuencia_test.wav', 'musica_sintetica.wav']

def mostrar_espectros(voz, multifrecuencia, musica, fs):
    """Muestra espectros de las señales generadas MEJORADAS"""
    
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    fig.suptitle('Señales de Prueba MEJORADAS - Optimizadas para Demo', fontsize=14)
    
    señales = [voz, multifrecuencia, musica]
    nombres = ['Voz con Ruido HF', 'Multi-Frecuencia', 'Música Sintética']
    
    for i, (señal, nombre) in enumerate(zip(señales, nombres)):
        # Dominio del tiempo - mostrar más tiempo para audio de 5s
        t = np.arange(len(señal)) / fs
        muestras_mostrar = min(4000, len(señal))  # Primeros 0.5 segundos
        axes[i, 0].plot(t[:muestras_mostrar], señal[:muestras_mostrar])
        axes[i, 0].set_title(f'{nombre} - Dominio Temporal')
        axes[i, 0].set_xlabel('Tiempo (s)')
        axes[i, 0].set_ylabel('Amplitud')
        axes[i, 0].grid(True, alpha=0.3)
        
        # Dominio de la frecuencia
        from scipy import signal as sig
        f, Pxx = sig.welch(señal, fs, nperseg=2048)  # Mayor resolución
        axes[i, 1].semilogy(f, Pxx, linewidth=2)
        axes[i, 1].set_title(f'{nombre} - Espectro de Potencia')
        axes[i, 1].set_xlabel('Frecuencia (Hz)')
        axes[i, 1].set_ylabel('PSD (V²/Hz)')
        axes[i, 1].grid(True, alpha=0.3)
        axes[i, 1].set_xlim([0, fs/2])
        
        # Marcar frecuencia de corte del filtro (800 Hz)
        axes[i, 1].axvline(800, color='red', linestyle='--', alpha=0.7, 
                          linewidth=2, label='Fc filtro = 800 Hz')
        axes[i, 1].legend()
    
    plt.tight_layout()
    plt.show()
    
    print("\nCARACTERÍSTICAS DE LAS SEÑALES:")
    print("=" * 50)
    print("1. VOZ CON RUIDO HF:")
    print("   - Frecuencias de voz: 200-800 Hz (deben pasar)")
    print("   - Ruido agregado: 1500-2500 Hz (debe eliminarse)")
    print("   - Duración: 5 segundos")
    
    print("\n2. MULTI-FRECUENCIA:")
    print("   - Frecuencias bajas: 300, 500, 700 Hz (deben pasar)")
    print("   - Frecuencias altas: 1200, 1800, 2400 Hz (deben eliminarse)")
    print("   - Ideal para probar selectividad")
    
    print("\n3. MÚSICA SINTÉTICA:")
    print("   - Notas musicales con armónicos")
    print("   - Ruido de alta frecuencia añadido")
    print("   - Perfecto para demostrar preservación de calidad musical")

def reproducir_archivos_generados():
    """Reproduce los archivos para verificar que suenan bien y duran 5 segundos"""
    
    import sounddevice as sd
    from scipy.io import wavfile
    
    archivos = ['voz_con_ruido.wav', 'multifrecuencia_test.wav', 'musica_sintetica.wav']
    
    print("\nREPRODUCIENDO ARCHIVOS GENERADOS:")
    print("=" * 50)
    
    for i, archivo in enumerate(archivos):
        try:
            fs, audio = wavfile.read(archivo)
            duracion = len(audio) / fs
            print(f"\n{i+1}. Reproduciendo {archivo}")
            print(f"   Duración: {duracion:.1f} segundos")
            print(f"   Frecuencia: {fs} Hz")
            
            # Normalizar para reproducción
            audio_float = audio.astype(np.float32) / 32768.0
            
            input("   Presiona Enter para reproducir...")
            sd.play(audio_float, fs)
            sd.wait()  # Esperar hasta que termine
            
            print(f"   {archivo} reproducido correctamente")
            
        except Exception as e:
            print(f"   Error reproduciendo {archivo}: {e}")
    
    print(f"\nTODOS LOS ARCHIVOS VERIFICADOS")
    print(f"Cada archivo dura 5 segundos y tiene características específicas")
    print(f"para demostrar claramente las diferencias entre filtros FIR e IIR")

if __name__ == "__main__":
    print("=== GENERADOR DE ARCHIVOS DE PRUEBA MEJORADO ===")
    print("Creando señales de 5 segundos optimizadas para demo clara...\n")
    
    try:
        archivos = generar_archivos_prueba()
        
        respuesta = input("\n¿Reproducir archivos para verificar calidad? (s/n): ")
        if respuesta.lower() in ['s', 'si', 'y', 'yes', '']:
            reproducir_archivos_generados()
        
        print("\nARCHIVOS LISTOS PARA DEMOSTRACION EN CLASE")
        print("=" * 50)
        print("Duración: 5 segundos cada uno")
        print("Frecuencia de corte: 800 Hz (optimizada)")
        print("Diferencias audibles claras entre original/FIR/IIR")
        print("Ruido de alta frecuencia añadido para demostrar filtrado")
        print("\nAhora ejecuta: python procesador_demo_simple.py")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Verifica que tengas instaladas todas las librerías necesarias.")
