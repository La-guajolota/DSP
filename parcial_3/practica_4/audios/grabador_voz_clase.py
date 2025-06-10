#!/usr/bin/env python3
"""
GRABADOR DE VOZ PARA CLASE
Graba conteo, frase técnica y silbido en vivo
Compatible con procesador_arduino_optimizado.py
"""

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import time
import os

class GrabadorVozClase:
    def __init__(self, fs=8000):
        self.fs = fs
        print("GRABADOR DE VOZ PARA CLASE DE FILTROS DIGITALES")
        print("=" * 55)
        print(f"Frecuencia de muestreo: {fs} Hz")
        print("Optimizado para procesamiento con Arduino Mega")
        print("=" * 55)
    
    def verificar_audio(self):
        """Verifica que el sistema de audio funcione"""
        print("\nVERIFICANDO SISTEMA DE AUDIO...")
        try:
            # Obtener dispositivos
            dispositivos = sd.query_devices()
            print(f"Dispositivos encontrados: {len(dispositivos)}")
            
            # Mostrar dispositivo de entrada por defecto
            entrada_default = sd.query_devices(kind='input')
            print(f"Micrófono por defecto: {entrada_default['name']}")
            
            # Test de grabación corta
            print("Realizando test de 2 segundos...")
            test_audio = sd.rec(int(2 * self.fs), samplerate=self.fs, channels=1)
            sd.wait()
            
            nivel = np.max(np.abs(test_audio))
            print(f"Nivel detectado: {nivel:.4f}")
            
            if nivel < 0.001:
                print("ADVERTENCIA: Nivel muy bajo")
                print("   - Verifica que el micrófono esté conectado")
                print("   - Aumenta el volumen de grabación")
                print("   - Acércate más al micrófono")
                return False
            else:
                print("Sistema de audio funcionando correctamente")
                return True
                
        except Exception as e:
            print(f"Error en sistema de audio: {e}")
            return False
    
    def grabar_conteo_1_5(self):
        """Graba conteo del 1 al 5 (5 segundos)"""
        
        print("\n" + "="*50)
        print("GRABACIÓN 1: CONTEO DEL 1 AL 5")
        print("="*50)
        print("INSTRUCCIONES:")
        print("• Cuenta del 1 al 5 claramente")
        print("• Pausa de 1 segundo entre números")
        print("• Mantén volumen constante")
        print("• Duración total: 5 segundos")
        print("")
        print("EJEMPLO: 'Uno... dos... tres... cuatro... cinco'")
        print("")
        
        input("Presiona ENTER cuando estés listo para grabar...")
        
        return self._grabar_con_countdown("voz_conteo.wav", 5, 
                                        "Cuenta ahora: 1... 2... 3... 4... 5")
    
    def grabar_frase_tecnica(self):
        """Graba frase técnica (3 segundos)"""
        
        print("\n" + "="*50)
        print("GRABACIÓN 2: FRASE TÉCNICA")
        print("="*50)
        print("INSTRUCCIONES:")
        print("• Di la frase rápido pero claro")
        print("• Pronuncia cada palabra distintamente")
        print("• Duración total: 3 segundos")
        print("")
        print("FRASE: 'Filtros digitales FIR e IIR'")
        print("")
        
        input("Presiona ENTER cuando estés listo para grabar...")
        
        return self._grabar_con_countdown("frase_tecnica.wav", 3,
                                        "Di ahora: Filtros digitales FIR e IIR")
    
    def grabar_silbido_tonal(self):
        """Graba silbido tonal (2 segundos)"""
        
        print("\n" + "="*50)
        print("GRABACIÓN 3: SILBIDO TONAL")
        print("="*50)
        print("INSTRUCCIONES:")
        print("• Mantén un silbido constante")
        print("• Frecuencia estable (aprox 1000-1500 Hz)")
        print("• Sin variaciones de tono")
        print("• Duración total: 2 segundos")
        print("")
        print("OBJETIVO: Probar selectividad del filtro")
        print("")
        
        input("Presiona ENTER cuando estés listo para grabar...")
        
        return self._grabar_con_countdown("silbido_tonal.wav", 2,
                                        "Silba ahora de forma constante")
    
    def _grabar_con_countdown(self, nombre_archivo, duracion, instruccion):
        """Graba audio con countdown y instrucciones"""
        
        print(f"\nGRABANDO: {nombre_archivo}")
        print(f"Duración: {duracion} segundos")
        print("")
        
        # Countdown
        print("Preparándose...")
        for i in range(3, 0, -1):
            print(f"   {i}...")
            time.sleep(1)
        
        print(f"{instruccion}")
        
        try:
            # Grabar
            audio = sd.rec(int(duracion * self.fs), 
                          samplerate=self.fs, 
                          channels=1, 
                          dtype='float64')
            
            # Mostrar progreso en tiempo real
            for i in range(duracion):
                time.sleep(1)
                puntos = "." * (i + 1)
                espacios = " " * (duracion - i - 1)
                print(f"   Grabando{puntos}{espacios}[{i+1}/{duracion}s]")
            
            sd.wait()
            print(" Grabación completada")
            
            # Procesar audio
            audio = audio.flatten()
            
            # Verificar nivel
            nivel_max = np.max(np.abs(audio))
            nivel_rms = np.sqrt(np.mean(audio**2))
            
            print(f"\nANÁLISIS DE LA GRABACIÓN:")
            print(f"• Nivel máximo: {nivel_max:.4f}")
            print(f"• Nivel RMS: {nivel_rms:.4f}")
            
            if nivel_max < 0.01:
                print("ADVERTENCIA: Nivel muy bajo")
                respuesta = input("¿Intentar nuevamente? (s/n): ")
                if respuesta.lower() == 's':
                    return self._grabar_con_countdown(nombre_archivo, duracion, instruccion)
            
            # Normalizar audio
            if nivel_max > 0:
                audio_normalizado = audio / nivel_max * 0.8
            else:
                audio_normalizado = audio
            
            # Convertir a int16 y guardar
            audio_int16 = (audio_normalizado * 32767).astype(np.int16)
            wavfile.write(nombre_archivo, self.fs, audio_int16)
            
            print(f"💾 Guuaacaouardadaoamaoa:   0nombre_archivo}")
            
            # Análisis espectral rápido
            self._analizar_grabacion(audio_normalizado, nombre_archivo)
            
            # Reproducir para verificar
            respuesta = input("\n¿Reproducir para verificar? (s/n): ")
            if respuesta.lower() == 's':
                print("Reproduciendo...")
                sd.play(audio_normalizado, self.fs)
                sd.wait()
                
                respuesta2 = input("¿Está bien la grabación? (s/n): ")
                if respuesta2.lower() != 's':
                    respuesta3 = input("¿Grabar nuevamente? (s/n): ")
                    if respuesta3.lower() == 's':
                        return self._grabar_con_countdown(nombre_archivo, duracion, instruccion)
            
            return nombre_archivo
            
        except Exception as e:
            print(f" Error durante grabación: {e}")
            return None
    
    def _analizar_grabacion(self, audio, nombre):
        """Análisis espectral rápido de la grabación"""
        
        try:
            # Calcular espectro
            f, Pxx = signal.welch(audio, self.fs, nperseg=512)
            
            # Encontrar pico principal
            idx_max = np.argmax(Pxx)
            freq_pico = f[idx_max]
            
            # Energía en bandas
            energia_baja = np.sum(Pxx[(f < 800)])
            energia_alta = np.sum(Pxx[(f >= 800)])
            ratio_energia = energia_baja / (energia_alta + 1e-10)
            
            print(f"\nANÁLISIS ESPECTRAL:")
            print(f"• Frecuencia pico: {freq_pico:.0f} Hz")
            print(f"• Energía < 800 Hz: {energia_baja:.2e}")
            print(f"• Energía ≥ 800 Hz: {energia_alta:.2e}")
            print(f"• Ratio baja/alta: {ratio_energia:.1f}")
            
            # Interpretación según tipo
            if "conteo" in nombre:
                if 200 <= freq_pico <= 600:
                    print(" Frecuencias de voz detectadas correctamente")
                else:
                    print("️ Frecuencias inusuales para voz")
                    
            elif "silbido" in nombre:
                if 800 <= freq_pico <= 2000:
                    print(" Frecuencia de silbido adecuada para filtros")
                else:
                    print("⚠️ Silbido fuera del rango óptimo")
                    
            elif "frase" in nombre:
                if ratio_energia > 2:
                    print(" Buena distribución espectral para análisis")
                else:
                    print("️ Poco contenido en frecuencias bajas")
                    
        except Exception as e:
            print(f"️ No se pudo analizar espectro: {e}")
    
    def crear_set_completo_clase(self):
        """Crea set completo de grabaciones para la clase"""
        
        print("\n" + "="*60)
        print("CREACIÓN DE SET COMPLETO PARA CLASE")
        print("="*60)
        print("Se crearán 3 grabaciones optimizadas para Arduino:")
        print("1. Conteo 1-5 (5 segundos) - Análisis de voz")
        print("2. Frase técnica (3 segundos) - Calidad de filtrado")
        print("3. Silbido tonal (2 segundos) - Selectividad")
        print("")
        
        # Verificar audio primero
        if not self.verificar_audio():
            print(" Problema con sistema de audio. Corrige antes de continuar.")
            return []
        
        archivos_creados = []
        
        try:
            # Grabación 1: Conteo
            print(f"\n{'='*20} GRABACIÓN 1/3 {'='*20}")
            archivo1 = self.grabar_conteo_1_5()
            if archivo1:
                archivos_creados.append(archivo1)
            
            # Pausa entre grabaciones
            time.sleep(1)
            
            # Grabación 2: Frase técnica
            print(f"\n{'='*20} GRABACIÓN 2/3 {'='*20}")
            archivo2 = self.grabar_frase_tecnica()
            if archivo2:
                archivos_creados.append(archivo2)
            
            # Pausa entre grabaciones
            time.sleep(1)
            
            # Grabación 3: Silbido
            print(f"\n{'='*20} GRABACIÓN 3/3 {'='*20}")
            archivo3 = self.grabar_silbido_tonal()
            if archivo3:
                archivos_creados.append(archivo3)
            
            # Resumen final
            print(f"\n" + "="*60)
            print("RESUMEN DE GRABACIONES CREADAS")
            print("="*60)
            
            if len(archivos_creados) == 3:
                print("¡TODAS LAS GRABACIONES COMPLETADAS EXITOSAMENTE!")
                for i, archivo in enumerate(archivos_creados, 1):
                    print(f"   {i}. {archivo} ")
                
                print(f"\nPRÓXIMOS PASOS:")
                print("1. Ejecutar: python procesador_arduino_optimizado.py")
                print("2. Seleccionar estos archivos para procesar")
                print("3. Comparar filtros FIR vs IIR")
                print("4. Escuchar diferencias en tu propia voz")
                
            else:
                print(f"⚠️ Se completaron {len(archivos_creados)}/3 grabaciones")
                for archivo in archivos_creados:
                    print(f"   • {archivo} ")
                
                faltantes = 3 - len(archivos_creados)
                print(f"   Faltan {faltantes} grabaciones")
            
            return archivos_creados
            
        except KeyboardInterrupt:
            print("\n\n️ Grabación interrumpida por usuario")
            return archivos_creados
            
        except Exception as e:
            print(f"\n Error durante grabaciones: {e}")
            return archivos_creados
    
    def mostrar_espectros(self, archivos):
        """Muestra análisis espectral de todos los archivos grabados"""
        
        if not archivos:
            print("No hay archivos para analizar")
            return
        
        fig, axes = plt.subplots(len(archivos), 2, figsize=(15, 4*len(archivos)))
        if len(archivos) == 1:
            axes = axes.reshape(1, -1)
        
        fig.suptitle('Análisis Espectral de Grabaciones para Clase', fontsize=14)
        
        nombres = ['Conteo 1-5', 'Frase Técnica', 'Silbido Tonal']
        
        for i, archivo in enumerate(archivos):
            try:
                # Leer archivo
                fs, audio = wavfile.read(archivo)
                if audio.dtype == np.int16:
                    audio = audio.astype(np.float32) / 32768.0
                
                # Tiempo
                t = np.arange(len(audio)) / fs
                
                # Gráfica temporal
                axes[i, 0].plot(t, audio)
                axes[i, 0].set_title(f'{nombres[i]} - Señal Temporal')
                axes[i, 0].set_xlabel('Tiempo (s)')
                axes[i, 0].set_ylabel('Amplitud')
                axes[i, 0].grid(True, alpha=0.3)
                
                # Espectro
                f, Pxx = signal.welch(audio, fs, nperseg=512)
                axes[i, 1].semilogy(f, Pxx)
                axes[i, 1].set_title(f'{nombres[i]} - Espectro de Potencia')
                axes[i, 1].set_xlabel('Frecuencia (Hz)')
                axes[i, 1].set_ylabel('PSD (V²/Hz)')
                axes[i, 1].grid(True, alpha=0.3)
                axes[i, 1].set_xlim([0, fs/2])
                
                # Marcar frecuencia de corte
                axes[i, 1].axvline(800, color='red', linestyle='--', 
                                 alpha=0.7, label='fc = 800 Hz')
                axes[i, 1].legend()
                
            except Exception as e:
                print(f"Error analizando {archivo}: {e}")
        
        plt.tight_layout()
        plt.show()

def menu_grabador():
    """Menú principal del grabador"""
    
    grabador = GrabadorVozClase()
    
    while True:
        print("\n" + "="*50)
        print("MENÚ GRABADOR DE VOZ PARA CLASE")
        print("="*50)
        print("1. Crear set completo (3 grabaciones)")
        print("2. Grabar solo conteo (5s)")
        print("3. Grabar solo frase técnica (3s)")
        print("4. Grabar solo silbido (2s)")
        print("5. Verificar sistema de audio")
        print("6. Mostrar análisis espectral")
        print("7. Reproducir archivos existentes")
        print("8. Salir")
        
        try:
            opcion = input("\nSelecciona opción (1-8): ").strip()
            
            if opcion == '1':
                archivos = grabador.crear_set_completo_clase()
                if len(archivos) == 3:
                    respuesta = input("\n¿Mostrar análisis espectral? (s/n): ")
                    if respuesta.lower() == 's':
                        grabador.mostrar_espectros(archivos)
                
            elif opcion == '2':
                grabador.grabar_conteo_1_5()
                
            elif opcion == '3':
                grabador.grabar_frase_tecnica()
                
            elif opcion == '4':
                grabador.grabar_silbido_tonal()
                
            elif opcion == '5':
                grabador.verificar_audio()
                
            elif opcion == '6':
                archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
                if archivos_wav:
                    grabador.mostrar_espectros(archivos_wav[:3])
                else:
                    print("No hay archivos WAV para analizar")
                
            elif opcion == '7':
                reproducir_archivos_existentes(grabador)
                
            elif opcion == '8':
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción no válida")
                
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def reproducir_archivos_existentes(grabador):
    """Reproduce archivos WAV existentes"""
    
    archivos = [f for f in os.listdir('.') if f.endswith('.wav')]
    
    if not archivos:
        print("No hay archivos WAV para reproducir")
        return
    
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos):
        try:
            fs, audio = wavfile.read(archivo)
            duracion = len(audio) / fs
            print(f"   {i+1}. {archivo} ({duracion:.1f}s)")
        except:
            print(f"   {i+1}. {archivo} (error)")
    
    try:
        seleccion = int(input(f"\nSelecciona archivo (1-{len(archivos)}): ")) - 1
        archivo_seleccionado = archivos[seleccion]
        
        # Cargar y reproducir
        fs, audio = wavfile.read(archivo_seleccionado)
        if audio.dtype == np.int16:
            audio = audio.astype(np.float32) / 32768.0
        
        print(f"Reproduciendo {archivo_seleccionado}...")
        sd.play(audio, fs)
        sd.wait()
        print(" Reproducción completada")
        
    except (ValueError, IndexError):
        print(" Selección inválida")
    except Exception as e:
        print(f" Error reproduciendo: {e}")

def main():
    """Función principal"""
    
    print("GRABADOR DE VOZ PARA CLASE DE FILTROS DIGITALES")
    print("Optimizado para Arduino Mega y procesamiento en tiempo real")
    print("=" * 65)
    
    try:
        menu_grabador()
    except Exception as e:
        print(f"Error en programa principal: {e}")

if __name__ == "__main__":
    main()
