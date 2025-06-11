#!/usr/bin/env python3
"""
SISTEMA PARA CLASE - ESP32 FILTROS DIGITALES CORREGIDO
Corrección de sincronización y manejo de buffers
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import sounddevice as sd
import serial
import time
import os

class SistemaCompletoClaseESP32:
    def __init__(self, puerto='COM4', fs=8000):
        self.puerto = puerto
        self.fs = fs
        self.esp32 = None
        self.conectado = False
        
        print("=" * 60)
        print("SISTEMA PARA CLASE DE FILTROS DIGITALES - ESP32")
        print("Version corregida con mejor sincronización")
        print("=" * 60)
        print(f"Puerto ESP32: {puerto}")
        print(f"Frecuencia: {fs} Hz")
        print("=" * 60)
    
    def menu_principal_clase(self):
        """Menú principal simplificado"""
        
        while True:
            print(f"\n{'='*60}")
            print("MENU PRINCIPAL - CLASE FILTROS DIGITALES ESP32")
            print(f"{'='*60}")
            print("PREPARACION:")
            print("1. Verificar sistema completo")
            print("2. Grabar voz del estudiante")
            print("3. Test de comunicación ESP32")
            print("")
            print("PROCESAMIENTO:")
            print("4. Demo completa con ESP32")
            print("5. Procesar archivo específico")
            print("6. Comparar FIR vs IIR")
            print("")
            print("ANALISIS:")
            print("7. Mostrar espectros de grabaciones")
            print("8. Reproducir archivos existentes")
            print("9. Salir")
            
            try:
                opcion = input(f"\nSelecciona opción (1-9): ").strip()
                
                if opcion == '1':
                    self.verificar_sistema_completo()
                elif opcion == '2':
                    self.realizar_grabaciones_clase()
                elif opcion == '3':
                    self.test_esp32()
                elif opcion == '4':
                    self.demo_completa_simple()
                elif opcion == '5':
                    self.procesar_archivo_especifico()
                elif opcion == '6':
                    self.comparar_fir_vs_iir()
                elif opcion == '7':
                    self.mostrar_analisis_grabaciones()
                elif opcion == '8':
                    self.reproducir_archivos()
                elif opcion == '9':
                    print("Clase completada exitosamente!")
                    break
                else:
                    print("Opción no válida")
                    
            except KeyboardInterrupt:
                print("\n\nSistema interrumpido")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def verificar_sistema_completo(self):
        """Verificación simplificada del sistema"""
        
        print(f"\n{'='*50}")
        print("VERIFICACION COMPLETA DEL SISTEMA ESP32")
        print(f"{'='*50}")
        
        # Verificar audio
        print("1. SISTEMA DE AUDIO:")
        try:
            test_audio = sd.rec(int(0.5 * self.fs), samplerate=self.fs, channels=1)
            sd.wait()
            if len(test_audio) > 0:
                print("   Audio funcionando correctamente")
                audio_ok = True
            else:
                print("   Problema con audio")
                audio_ok = False
        except Exception as e:
            print(f"   Error en audio: {e}")
            audio_ok = False
        
        # Verificar ESP32
        print("\n2. COMUNICACION ESP32:")
        esp32_ok = self.conectar_esp32()
        if esp32_ok:
            self.esp32.write(b't\n')
            time.sleep(2)
            self.cerrar_esp32()
        
        # Verificar archivos existentes
        print("\n3. ARCHIVOS DE AUDIO:")
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        print(f"Archivos WAV encontrados: {len(archivos_wav)}")
        for archivo in archivos_wav:
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   {archivo}: {duracion:.1f}s, {fs}Hz")
            except:
                print(f"   {archivo}: Error al leer")
        
        print(f"\n{'='*50}")
        print("RESUMEN DEL SISTEMA:")
        print(f"   Audio: {'OK' if audio_ok else 'ERROR'}")
        print(f"   ESP32: {'OK' if esp32_ok else 'ERROR'}")
        print(f"   Archivos: {'OK' if len(archivos_wav) > 0 else 'SIN ARCHIVOS'}")
        
        if audio_ok and esp32_ok:
            print("\nSISTEMA LISTO PARA LA CLASE")
        else:
            print("\nCORREGIR PROBLEMAS ANTES DE LA CLASE")
        
        return audio_ok and esp32_ok
    
    def realizar_grabaciones_clase(self):
        """Realiza grabaciones específicas para la clase"""
        
        print(f"\n{'='*50}")
        print("GRABACIONES PARA LA CLASE ESP32")
        print(f"{'='*50}")
        
        continuar = input("\nCrear grabaciones de prueba? (s/n): ")
        if continuar.lower() != 's':
            return
        
        archivos = []
        
        # Grabación 1: Conteo
        print(f"\nGRABACION 1: Conteo 1-5")
        print("Di claramente: 'Uno, dos, tres, cuatro, cinco'")
        input("Presiona Enter cuando estés listo...")
        print("GRABANDO... (5 segundos)")
        
        audio1 = sd.rec(int(5 * self.fs), samplerate=self.fs, channels=1, dtype='float32')
        sd.wait()
        
        archivo1 = "conteo_1_5_esp32.wav"
        wavfile.write(archivo1, self.fs, (audio1 * 32767).astype(np.int16))
        archivos.append(archivo1)
        print(f"Guardado: {archivo1}")
        
        # Grabación 2: Frase técnica
        print(f"\nGRABACION 2: Frase técnica")
        print("Di: 'El ESP32 procesa filtros digitales eficientemente'")
        input("Presiona Enter cuando estés listo...")
        print("GRABANDO... (5 segundos)")
        
        audio2 = sd.rec(int(5 * self.fs), samplerate=self.fs, channels=1, dtype='float32')
        sd.wait()
        
        archivo2 = "frase_tecnica_esp32.wav"
        wavfile.write(archivo2, self.fs, (audio2 * 32767).astype(np.int16))
        archivos.append(archivo2)
        print(f"Guardado: {archivo2}")
        
        print(f"\nGRABACIONES COMPLETADAS!")
        return archivos
    
    def conectar_esp32(self):
        """Conecta con ESP32 de forma más robusta"""
        try:
            print(f"Conectando ESP32 en {self.puerto}...")
            self.esp32 = serial.Serial(self.puerto, 115200, timeout=5)
            time.sleep(3)
            
            # Limpiar buffers
            self.esp32.reset_input_buffer()
            self.esp32.reset_output_buffer()
            
            # Test básico
            self.esp32.write(b't\n')
            time.sleep(3)
            
            # Leer respuesta
            respuestas = []
            for _ in range(15):
                if self.esp32.in_waiting:
                    respuesta = self.esp32.readline().decode('utf-8', errors='ignore').strip()
                    if respuesta:
                        respuestas.append(respuesta)
                        print(f"   ESP32: {respuesta}")
                        if "ESP32" in respuesta or "TEST" in respuesta:
                            self.conectado = True
                            print("ESP32 conectado exitosamente")
                            return True
                time.sleep(0.3)
            
            # Si llegamos aquí, hay comunicación
            if len(respuestas) > 0:
                self.conectado = True
                print("ESP32 conectado (comunicación básica)")
                return True
            else:
                print("Sin respuesta del ESP32")
                return False
            
        except Exception as e:
            print(f"Error conectando ESP32: {e}")
            return False
    
    def cerrar_esp32(self):
        """Cierra conexión ESP32"""
        if self.esp32 and self.esp32.is_open:
            self.esp32.close()
            self.conectado = False
    
    def test_esp32(self):
        """Test de comunicación ESP32"""
        
        print(f"\n{'='*40}")
        print("TEST DE COMUNICACION ESP32")
        print(f"{'='*40}")
        
        if self.conectar_esp32():
            try:
                # Test de filtros
                print(f"\nProbando configuración de filtros...")
                for filtro in [0, 1, 2]:
                    print(f"\nConfigurando filtro {filtro}...")
                    self.esp32.write(f"{filtro}\n".encode())
                    time.sleep(2)
                    
                    # Leer respuesta
                    for _ in range(5):
                        if self.esp32.in_waiting:
                            resp = self.esp32.readline().decode('utf-8', errors='ignore').strip()
                            if resp:
                                print(f"   Filtro {filtro}: {resp}")
                                break
                        time.sleep(0.5)
                
                print("\nTest de comunicación exitoso")
                
            except Exception as e:
                print(f"Error en test: {e}")
            finally:
                self.cerrar_esp32()
        else:
            print("No se pudo conectar para el test")
    
    def demo_completa_simple(self):
        """Demostración simplificada con archivos completos"""
        
        print(f"\n{'='*60}")
        print("DEMOSTRACION COMPLETA PARA CLASE ESP32")
        print("Procesando archivos de audio completos")
        print(f"{'='*60}")
        
        # Verificar archivos
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos de audio disponibles")
            respuesta = input("¿Crear grabaciones ahora? (s/n): ")
            if respuesta.lower() == 's':
                archivos_wav = self.realizar_grabaciones_clase()
            else:
                print("Se necesitan archivos de audio para continuar")
                return
        
        # Seleccionar archivo
        print(f"\nArchivos disponibles:")
        for i, archivo in enumerate(archivos_wav):
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   {i+1}. {archivo} ({duracion:.1f}s)")
            except:
                print(f"   {i+1}. {archivo} (error)")
        
        try:
            seleccion = int(input(f"\nSelecciona archivo (1-{len(archivos_wav)}): ")) - 1
            archivo_seleccionado = archivos_wav[seleccion]
        except:
            archivo_seleccionado = archivos_wav[0]
            print(f"Usando: {archivo_seleccionado}")
        
        # Mostrar duración del archivo seleccionado
        try:
            fs, audio = wavfile.read(archivo_seleccionado)
            duracion_real = len(audio) / fs
            muestras_totales = int(duracion_real * self.fs)
            print(f"Archivo seleccionado: {duracion_real:.1f}s ({muestras_totales} muestras a {self.fs}Hz)")
        except:
            print("Error leyendo archivo")
            return
        
        # Conectar ESP32
        if not self.conectar_esp32():
            print("No se puede continuar sin ESP32")
            return
        
        try:
            # Seleccionar método de procesamiento
            print(f"\nMétodos de procesamiento disponibles:")
            print("1. Streaming (muestra por muestra) - Más lento pero completo")
            print("2. Buffer múltiple (chunks de 2048) - Más rápido")
            
            metodo = input("Selecciona método (1/2, por defecto 2): ").strip()
            if metodo == "1":
                usar_streaming = True
                print("Usando método streaming para archivo completo")
            else:
                usar_streaming = False
                print("Usando método de buffer múltiple")
            
            # Procesar con FIR
            print(f"\n{'='*50}")
            print("PROCESANDO CON FILTRO FIR")
            print(f"{'='*50}")
            
            if usar_streaming:
                entrada_fir, salida_fir = self.procesar_con_esp32_corregido(archivo_seleccionado, 1)
            else:
                entrada_fir, salida_fir = self.procesar_con_buffer_multiple(archivo_seleccionado, 1)
            
            if entrada_fir is not None and salida_fir is not None:
                self.generar_analisis_simple(archivo_seleccionado, entrada_fir, salida_fir, "FIR")
                self.reproducir_comparacion_simple(entrada_fir, salida_fir, "FIR")
            else:
                print("Error procesando con FIR")
            
            # Procesar con IIR
            print(f"\n{'='*50}")
            print("PROCESANDO CON FILTRO IIR")
            print(f"{'='*50}")
            
            if usar_streaming:
                entrada_iir, salida_iir = self.procesar_con_esp32_corregido(archivo_seleccionado, 2)
            else:
                entrada_iir, salida_iir = self.procesar_con_buffer_multiple(archivo_seleccionado, 2)
            
            if entrada_iir is not None and salida_iir is not None:
                self.generar_analisis_simple(archivo_seleccionado, entrada_iir, salida_iir, "IIR")
                self.reproducir_comparacion_simple(entrada_iir, salida_iir, "IIR")
                
                # Comparación final
                if entrada_fir is not None:
                    self.comparar_resultados_finales(archivo_seleccionado, 
                                                   entrada_fir, salida_fir, 
                                                   entrada_iir, salida_iir)
            else:
                print("Error procesando con IIR")
        
        finally:
            self.cerrar_esp32()
        
        print(f"\nDEMOSTRACION COMPLETA")
    
    def procesar_con_buffer_multiple(self, archivo, tipo_filtro):
        """Procesa archivo completo usando múltiples buffers de 2048"""
        
        try:
            # Cargar audio
            fs_orig, audio = wavfile.read(archivo)
            print(f"Procesando {archivo} COMPLETO con filtro tipo {tipo_filtro}")
            
            # Preparar audio
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1)
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            
            if fs_orig != self.fs:
                num_samples = int(len(audio) * self.fs / fs_orig)
                audio = signal.resample(audio, num_samples)
            
            # Convertir a ADC (0-1023)
            audio_normalizado = np.clip(audio, -1, 1)
            audio_adc = ((audio_normalizado + 1) * 511.5).astype(int)
            
            duracion_total = len(audio_adc) / self.fs
            print(f"Audio completo: {duracion_total:.1f}s, {len(audio_adc)} muestras")
            
            # Reset y configurar filtro
            print("Reseteando ESP32...")
            self.esp32.write(b"r\n")
            time.sleep(3)
            self.esp32.reset_input_buffer()
            
            print(f"Configurando filtro {tipo_filtro}...")
            self.esp32.write(f"{tipo_filtro}\n".encode())
            time.sleep(3)
            
            # Verificar configuración
            configurado = False
            for _ in range(8):
                if self.esp32.in_waiting:
                    resp = self.esp32.readline().decode('utf-8', errors='ignore').strip()
                    print(f"   ESP32: {resp}")
                    if "FILTRO" in resp or "activado" in resp:
                        configurado = True
                        break
                time.sleep(0.5)
            
            if not configurado:
                print("ADVERTENCIA: Sin confirmación de filtro")
            
            # Procesar en buffers de 2048 muestras
            buffer_size = 2048
            total_buffers = (len(audio_adc) + buffer_size - 1) // buffer_size
            
            entrada_completa = []
            salida_completa = []
            buffers_exitosos = 0
            
            print(f"Procesando en {total_buffers} buffers de {buffer_size} muestras")
            
            for i in range(total_buffers):
                inicio = i * buffer_size
                fin = min(inicio + buffer_size, len(audio_adc))
                buffer_data = audio_adc[inicio:fin]
                
                print(f"\nBuffer {i+1}/{total_buffers}: {len(buffer_data)} muestras")
                
                # Procesar buffer pasando el tipo_filtro
                entrada_buffer, salida_buffer = self.procesar_buffer_unico(buffer_data, tipo_filtro)
                
                if entrada_buffer is not None and salida_buffer is not None:
                    entrada_completa.extend(entrada_buffer)
                    salida_completa.extend(salida_buffer)
                    buffers_exitosos += 1
                    
                    progreso = (i + 1) / total_buffers * 100
                    print(f"  Buffer {i+1}: {progreso:.1f}% - EXITOSO")
                else:
                    print(f"  Buffer {i+1}: ERROR - usando datos sin filtrar")
                    # Usar datos sin filtrar para mantener sincronización
                    entrada_completa.extend(buffer_data)
                    salida_completa.extend(buffer_data)
            
            print(f"\nProcesamiento completo:")
            print(f"  Buffers exitosos: {buffers_exitosos}/{total_buffers}")
            print(f"  Muestras totales: {len(entrada_completa)}")
            print(f"  Duración final: {len(entrada_completa)/self.fs:.1f}s")
            
            if len(entrada_completa) > 0:
                return np.array(entrada_completa), np.array(salida_completa)
            else:
                return None, None
                
        except Exception as e:
            print(f"Error en procesamiento múltiple: {e}")
            return None, None
    
    def procesar_buffer_unico(self, buffer_data, tipo_filtro):
        """Procesa un solo buffer de hasta 2048 muestras"""
        
        try:
            # Limpiar buffer
            self.esp32.reset_input_buffer()
            
            # NUEVO: Debug del filtro antes de procesar
            print("  Verificando estado del filtro...")
            self.esp32.write(b"df\n")
            time.sleep(2)
            
            # Leer respuestas del debug
            debug_responses = []
            for _ in range(15):
                if self.esp32.in_waiting:
                    resp = self.esp32.readline().decode('utf-8', errors='ignore').strip()
                    if resp and ("Tipo de filtro" in resp or "diferencia:" in resp or "Estado" in resp):
                        debug_responses.append(resp)
                        print(f"    {resp}")
                time.sleep(0.1)
            
            # Verificar que el filtro está configurado correctamente
            tipo_correcto = any(f"Tipo de filtro actual: {tipo_filtro}" in resp for resp in debug_responses)
            if tipo_correcto:
                print("  Tipo de filtro CORRECTO")
            else:
                print(f"  ERROR: Tipo de filtro incorrecto - esperado {tipo_filtro}")
            
            # Verificar que el filtro funciona
            diferencia_detectada = any("diferencia:" in resp and not "diferencia: 0)" in resp for resp in debug_responses)
            if diferencia_detectada:
                print("  Filtro FUNCIONA correctamente")
            else:
                print("  PROBLEMA: Filtro no modifica las muestras")
            
            # Iniciar captura
            self.esp32.write(b"c\n")
            time.sleep(1)
            
            # Enviar muestras del buffer
            print(f"  Enviando {len(buffer_data)} muestras...")
            for i, muestra in enumerate(buffer_data):
                self.esp32.write(f"DATA:{int(muestra)}\n".encode())
                time.sleep(0.003)
                
                if (i + 1) % 500 == 0:
                    print(f"    {i+1}/{len(buffer_data)} muestras enviadas")
            
            # Esperar procesamiento
            print("  Esperando procesamiento...")
            time.sleep(5)
            
            # Verificar completado
            procesamiento_ok = False
            for _ in range(15):
                if self.esp32.in_waiting:
                    msg = self.esp32.readline().decode('utf-8', errors='ignore').strip()
                    if msg:
                        print(f"    ESP32: {msg}")
                        if "PROCESAMIENTO COMPLETADO" in msg or "BUFFER COMPLETO" in msg:
                            procesamiento_ok = True
                            break
                time.sleep(0.3)
            
            if not procesamiento_ok:
                print("  ADVERTENCIA: Sin confirmación de procesamiento")
            
            # Solicitar datos
            print("  Solicitando datos...")
            self.esp32.write(b"s\n")
            time.sleep(3)
            
            # Leer datos
            entrada, salida = self.leer_datos_esp32_rapido(len(buffer_data))
            
            # Verificar que el filtro se aplicó
            if entrada and salida:
                diferencias = [abs(int(e) - int(s)) for e, s in zip(entrada[:100], salida[:100])]
                num_diferentes = sum(1 for d in diferencias if d > 0)
                porcentaje_filtrado = (num_diferentes / len(diferencias)) * 100
                
                print(f"  Verificación: {porcentaje_filtrado:.1f}% de muestras fueron filtradas")
                
                if porcentaje_filtrado > 10:  # Al menos 10% de las muestras deben cambiar
                    print("  FILTRO APLICADO CORRECTAMENTE")
                else:
                    print("  ADVERTENCIA: Filtro no parece haberse aplicado")
            
            return entrada, salida
            
        except Exception as e:
            print(f"Error en buffer único: {e}")
            return None, None
    
    def leer_datos_esp32_rapido(self, muestras_esperadas):
        """Lectura rápida de datos del ESP32"""
        
        entrada = []
        salida = []
        leyendo_datos = False
        timeout_inicio = time.time()
        
        while (time.time() - timeout_inicio) < 15:  # 15 segundos max
            if self.esp32.in_waiting:
                try:
                    linea = self.esp32.readline().decode('utf-8', errors='ignore').strip()
                    if not linea:
                        continue
                    
                    if "INICIO_DATOS_ESP32" in linea:
                        leyendo_datos = False
                        continue
                    
                    if "index,input,output" in linea:
                        leyendo_datos = True
                        continue
                    
                    if "FIN_DATOS_ESP32" in linea:
                        break
                    
                    if leyendo_datos and "," in linea:
                        partes = linea.split(',')
                        if len(partes) >= 3:
                            try:
                                entrada.append(int(partes[1]))
                                salida.append(int(partes[2]))
                            except ValueError:
                                continue
                                
                except Exception:
                    continue
            else:
                time.sleep(0.05)
        
        # Verificar datos recibidos
        if len(entrada) >= muestras_esperadas * 0.7:  # Al menos 70%
            # Ajustar tamaño
            entrada = entrada[:muestras_esperadas]
            salida = salida[:muestras_esperadas]
            
            # Rellenar si faltan
            while len(entrada) < muestras_esperadas:
                entrada.append(entrada[-1] if entrada else 512)
                salida.append(salida[-1] if salida else 512)
            
            return entrada, salida
        else:
            return None, None
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   {i+1}. {archivo} ({duracion:.1f}s)")
            except:
                print(f"   {i+1}. {archivo} (error)")
        
        try:
            seleccion = int(input(f"\nSelecciona archivo (1-{len(archivos_wav)}): ")) - 1
            archivo_seleccionado = archivos_wav[seleccion]
        except:
            archivo_seleccionado = archivos_wav[0]
            print(f"Usando: {archivo_seleccionado}")
        
        # Mostrar duración del archivo seleccionado
        try:
            fs, audio = wavfile.read(archivo_seleccionado)
            duracion_real = len(audio) / fs
            muestras_totales = int(duracion_real * self.fs)
            print(f"Archivo seleccionado: {duracion_real:.1f}s ({muestras_totales} muestras a {self.fs}Hz)")
        except:
            print("Error leyendo archivo")
            return
        
        # Conectar ESP32
        if not self.conectar_esp32():
            print("No se puede continuar sin ESP32")
            return
        
        try:
            # Seleccionar método de procesamiento
            print(f"\nMétodos de procesamiento disponibles:")
            print("1. Streaming (muestra por muestra) - Más lento pero completo")
            print("2. Buffer múltiple (chunks de 2048) - Más rápido")
            
            metodo = input("Selecciona método (1/2, por defecto 2): ").strip()
            if metodo == "1":
                usar_streaming = True
                print("Usando método streaming para archivo completo")
            else:
                usar_streaming = False
                print("Usando método de buffer múltiple")
            
            # Procesar con FIR
            print(f"\n{'='*50}")
            print("PROCESANDO CON FILTRO FIR")
            print(f"{'='*50}")
            
            if usar_streaming:
                entrada_fir, salida_fir = self.procesar_con_esp32_corregido(archivo_seleccionado, 1)
            else:
                entrada_fir, salida_fir = self.procesar_con_buffer_multiple(archivo_seleccionado, 1)
            
            if entrada_fir is not None and salida_fir is not None:
                self.generar_analisis_simple(archivo_seleccionado, entrada_fir, salida_fir, "FIR")
                self.reproducir_comparacion_simple(entrada_fir, salida_fir, "FIR")
            else:
                print("Error procesando con FIR")
            
            # Procesar con IIR
            print(f"\n{'='*50}")
            print("PROCESANDO CON FILTRO IIR")
            print(f"{'='*50}")
            
            if usar_streaming:
                entrada_iir, salida_iir = self.procesar_con_esp32_corregido(archivo_seleccionado, 2)
            else:
                entrada_iir, salida_iir = self.procesar_con_buffer_multiple(archivo_seleccionado, 2)
            
            if entrada_iir is not None and salida_iir is not None:
                self.generar_analisis_simple(archivo_seleccionado, entrada_iir, salida_iir, "IIR")
                self.reproducir_comparacion_simple(entrada_iir, salida_iir, "IIR")
                
                # Comparación final
                if entrada_fir is not None:
                    self.comparar_resultados_finales(archivo_seleccionado, 
                                                   entrada_fir, salida_fir, 
                                                   entrada_iir, salida_iir)
            else:
                print("Error procesando con IIR")
        
        finally:
            self.cerrar_esp32()
        
        print(f"\nDEMOSTRACION COMPLETA")
    
    def procesar_archivo_especifico(self):
        """Procesa un archivo específico completo"""
        
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos WAV disponibles")
            return
        
        print(f"\nArchivos disponibles:")
        for i, archivo in enumerate(archivos_wav):
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   {i+1}. {archivo} ({duracion:.1f}s)")
            except:
                print(f"   {i+1}. {archivo} (error)")
        
        try:
            seleccion = int(input(f"\nSelecciona archivo (1-{len(archivos_wav)}): ")) - 1
            archivo = archivos_wav[seleccion]
            
            # Mostrar duración completa
            fs, audio = wavfile.read(archivo)
            duracion_real = len(audio) / fs
            print(f"Archivo: {duracion_real:.1f}s completos")
            
            print(f"\nFiltros disponibles:")
            print("1. FIR (preserva fase)")
            print("2. IIR (más eficiente)")
            
            filtro_sel = int(input("Selecciona filtro (1/2): "))
            nombres = ["", "FIR", "IIR"]
            nombre_filtro = nombres[filtro_sel]
            
            # Seleccionar método
            print(f"\nMétodos de procesamiento:")
            print("1. Streaming completo")
            print("2. Buffer múltiple (recomendado)")
            
            metodo = input("Método (1/2, por defecto 2): ").strip()
            usar_streaming = (metodo == "1")
            
            if self.conectar_esp32():
                if usar_streaming:
                    entrada, salida = self.procesar_con_esp32_corregido(archivo, filtro_sel)
                else:
                    entrada, salida = self.procesar_con_buffer_multiple(archivo, filtro_sel)
                
                if entrada is not None and salida is not None:
                    self.generar_analisis_simple(archivo, entrada, salida, nombre_filtro)
                    self.reproducir_comparacion_simple(entrada, salida, nombre_filtro)
                else:
                    print("Error en procesamiento")
                
                self.cerrar_esp32()
            
        except (ValueError, IndexError):
            print("Selección inválida")
        except Exception as e:
            print(f"Error: {e}")
    
    def comparar_fir_vs_iir(self):
        """Compara FIR vs IIR con archivo completo"""
        
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos WAV disponibles")
            return
        
        print(f"\nSelecciona archivo para comparar FIR vs IIR:")
        for i, archivo in enumerate(archivos_wav):
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   {i+1}. {archivo} ({duracion:.1f}s)")
            except:
                print(f"   {i+1}. {archivo} (error)")
        
        try:
            seleccion = int(input(f"\nArchivo (1-{len(archivos_wav)}): ")) - 1
            archivo = archivos_wav[seleccion]
            
            # Mostrar duración
            fs, audio = wavfile.read(archivo)
            duracion_real = len(audio) / fs
            print(f"Procesando {duracion_real:.1f}s completos")
            
            # Seleccionar método
            print(f"\nMétodo de procesamiento:")
            print("1. Streaming completo")
            print("2. Buffer múltiple (recomendado para archivos largos)")
            
            metodo = input("Método (1/2, por defecto 2): ").strip()
            usar_streaming = (metodo == "1")
            
            if self.conectar_esp32():
                
                # Procesar con FIR
                print(f"\n{'='*50}")
                print("PROCESANDO CON FIR - ARCHIVO COMPLETO")
                print(f"{'='*50}")
                
                if usar_streaming:
                    entrada_fir, salida_fir = self.procesar_con_esp32_corregido(archivo, 1)
                else:
                    entrada_fir, salida_fir = self.procesar_con_buffer_multiple(archivo, 1)
                
                if entrada_fir is not None:
                    self.generar_analisis_simple(archivo, entrada_fir, salida_fir, "FIR")
                
                # Procesar con IIR
                print(f"\n{'='*50}")
                print("PROCESANDO CON IIR - ARCHIVO COMPLETO")
                print(f"{'='*50}")
                
                if usar_streaming:
                    entrada_iir, salida_iir = self.procesar_con_esp32_corregido(archivo, 2)
                else:
                    entrada_iir, salida_iir = self.procesar_con_buffer_multiple(archivo, 2)
                
                if entrada_iir is not None:
                    self.generar_analisis_simple(archivo, entrada_iir, salida_iir, "IIR")
                
                # Comparación final
                if entrada_fir is not None and entrada_iir is not None:
                    self.comparar_resultados_finales(archivo, entrada_fir, salida_fir, entrada_iir, salida_iir)
                
                self.cerrar_esp32()
            
        except Exception as e:
            print(f"Error: {e}")
    
    def procesar_con_esp32_corregido(self, archivo, tipo_filtro):
        """Procesa archivo COMPLETO con ESP32 usando método streaming"""
        
        try:
            # Cargar audio
            fs_orig, audio = wavfile.read(archivo)
            print(f"Procesando {archivo} con filtro tipo {tipo_filtro}")
            
            # Preparar audio
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1)
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            
            if fs_orig != self.fs:
                num_samples = int(len(audio) * self.fs / fs_orig)
                audio = signal.resample(audio, num_samples)
            
            # Convertir a ADC (0-1023)
            audio_normalizado = np.clip(audio, -1, 1)
            audio_adc = ((audio_normalizado + 1) * 511.5).astype(int)
            
            duracion_total = len(audio_adc) / self.fs
            print(f"Audio completo: {duracion_total:.1f}s, {len(audio_adc)} muestras")
            
            # Reset y configurar filtro
            print("Reseteando ESP32...")
            self.esp32.write(b"r\n")
            time.sleep(3)
            self.esp32.reset_input_buffer()
            
            print(f"Configurando filtro {tipo_filtro}...")
            self.esp32.write(f"{tipo_filtro}\n".encode())
            time.sleep(3)
            
            # Verificar configuración
            configurado = False
            for _ in range(8):
                if self.esp32.in_waiting:
                    resp = self.esp32.readline().decode('utf-8', errors='ignore').strip()
                    print(f"   ESP32: {resp}")
                    if "FILTRO" in resp or "activado" in resp:
                        configurado = True
                        break
                time.sleep(0.5)
            
            if not configurado:
                print("ADVERTENCIA: Sin confirmación de filtro")
            
            # NUEVO: Procesar usando método streaming (muestra por muestra)
            print("Iniciando procesamiento streaming...")
            
            entrada_completa = []
            salida_completa = []
            
            # Procesar en chunks pequeños para evitar overflow del buffer serie
            chunk_size = 100  # Procesar de 100 en 100 muestras
            total_chunks = (len(audio_adc) + chunk_size - 1) // chunk_size
            
            for chunk_idx in range(total_chunks):
                inicio = chunk_idx * chunk_size
                fin = min(inicio + chunk_size, len(audio_adc))
                chunk_muestras = audio_adc[inicio:fin]
                
                print(f"Chunk {chunk_idx + 1}/{total_chunks}: {len(chunk_muestras)} muestras")
                
                # Procesar chunk
                entrada_chunk, salida_chunk = self.procesar_chunk_streaming(chunk_muestras)
                
                if entrada_chunk and salida_chunk:
                    entrada_completa.extend(entrada_chunk)
                    salida_completa.extend(salida_chunk)
                    
                    progreso = (chunk_idx + 1) / total_chunks * 100
                    print(f"  Progreso: {progreso:.1f}%")
                else:
                    print(f"  ERROR en chunk {chunk_idx + 1}")
                    # Agregar datos por defecto para mantener sincronización
                    for muestra in chunk_muestras:
                        entrada_completa.append(int(muestra))
                        salida_completa.append(int(muestra))  # Sin filtrar
            
            print(f"Procesamiento completo: {len(entrada_completa)} muestras")
            
            if len(entrada_completa) > 0:
                return np.array(entrada_completa), np.array(salida_completa)
            else:
                return None, None
                
        except Exception as e:
            print(f"Error en procesamiento: {e}")
            return None, None
    
    def procesar_chunk_streaming(self, chunk_muestras):
        """Procesa un chunk de muestras usando método streaming"""
        
        entrada_chunk = []
        salida_chunk = []
        
        try:
            # Limpiar buffer antes de empezar
            self.esp32.reset_input_buffer()
            
            for i, muestra in enumerate(chunk_muestras):
                # Enviar muestra para procesamiento directo
                self.esp32.write(f"PROCESS:{int(muestra)}\n".encode())
                
                # Esperar respuesta (con timeout corto)
                timeout_inicio = time.time()
                respuesta_recibida = False
                
                while (time.time() - timeout_inicio) < 0.1:  # 100ms timeout por muestra
                    if self.esp32.in_waiting:
                        try:
                            linea = self.esp32.readline().decode('utf-8', errors='ignore').strip()
                            if linea.startswith("SAMPLE_RESULT:"):
                                # Formato: SAMPLE_RESULT:entrada,salida
                                datos = linea.split(':')[1].split(',')
                                if len(datos) == 2:
                                    entrada_chunk.append(int(datos[0]))
                                    salida_chunk.append(int(datos[1]))
                                    respuesta_recibida = True
                                    break
                        except:
                            continue
                    time.sleep(0.01)
                
                if not respuesta_recibida:
                    # Si no hay respuesta, usar valor original
                    entrada_chunk.append(int(muestra))
                    salida_chunk.append(int(muestra))
                
                # Pequeña pausa cada 10 muestras
                if (i + 1) % 10 == 0:
                    time.sleep(0.01)
            
            return entrada_chunk, salida_chunk
            
        except Exception as e:
            print(f"Error en chunk streaming: {e}")
            return None, None
    
    def leer_datos_esp32_corregido(self, muestras_esperadas):
        """Lee datos del ESP32 con método corregido"""
        
        entrada = []
        salida = []
        leyendo_datos = False
        timeout_inicio = time.time()
        
        print(f"Esperando datos del ESP32 (máximo 30 segundos)...")
        
        while (time.time() - timeout_inicio) < 30:
            if self.esp32.in_waiting:
                try:
                    linea = self.esp32.readline().decode('utf-8', errors='ignore').strip()
                    if not linea:
                        continue
                    
                    if "INICIO_DATOS_ESP32" in linea:
                        print("   Inicio de datos detectado")
                        leyendo_datos = False  # Esperar header
                        continue
                    
                    if "index,input,output" in linea:
                        print("   Leyendo datos CSV...")
                        leyendo_datos = True
                        continue
                    
                    if "FIN_DATOS_ESP32" in linea or "ENVIO COMPLETADO" in linea:
                        print("   Fin de datos detectado")
                        break
                    
                    if leyendo_datos and "," in linea:
                        partes = linea.split(',')
                        if len(partes) >= 3:
                            try:
                                val_entrada = int(partes[1])
                                val_salida = int(partes[2])
                                entrada.append(val_entrada)
                                salida.append(val_salida)
                                
                                if len(entrada) % 200 == 0:
                                    print(f"   Recibidas {len(entrada)} muestras")
                                    
                            except ValueError:
                                continue
                                
                except Exception as e:
                    print(f"   Error leyendo línea: {e}")
                    continue
            else:
                time.sleep(0.1)
        
        print(f"Datos recibidos: {len(entrada)} entradas, {len(salida)} salidas")
        print(f"Datos esperados: {muestras_esperadas}")
        
        # Verificar si tenemos suficientes datos
        if len(entrada) >= muestras_esperadas * 0.5:  # Al menos 50%
            # Ajustar tamaño
            entrada = entrada[:muestras_esperadas]
            salida = salida[:muestras_esperadas]
            
            # Rellenar si faltan datos
            while len(entrada) < muestras_esperadas:
                entrada.append(entrada[-1] if entrada else 512)
                salida.append(salida[-1] if salida else 512)
            
            print("   Datos procesados correctamente")
            return entrada, salida
        else:
            print(f"   Datos insuficientes ({len(entrada)}/{muestras_esperadas})")
            return None, None
    
    def generar_analisis_simple(self, archivo, entrada, salida, nombre_filtro):
        """Genera análisis visual simple"""
        
        # Convertir a voltajes
        entrada_volt = np.array(entrada) * 5.0 / 1023.0
        salida_volt = np.array(salida) * 5.0 / 1023.0
        
        # Crear gráficas
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'Análisis ESP32 - {archivo} - Filtro {nombre_filtro}', fontsize=14)
        
        # Señales temporales
        t = np.arange(len(entrada)) / self.fs
        axes[0, 0].plot(t, entrada_volt, 'b-', alpha=0.7, label='Original')
        axes[0, 0].plot(t, salida_volt, 'r-', linewidth=2, label='Filtrado')
        axes[0, 0].set_title(f'Señales - {len(entrada)/self.fs:.1f}s')
        axes[0, 0].set_xlabel('Tiempo (s)')
        axes[0, 0].set_ylabel('Voltaje (V)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Espectros
        try:
            f, Pxx_entrada = signal.welch(entrada_volt, self.fs, nperseg=min(256, len(entrada_volt)//2))
            f, Pxx_salida = signal.welch(salida_volt, self.fs, nperseg=min(256, len(salida_volt)//2))
            
            axes[0, 1].semilogy(f, Pxx_entrada, 'b-', alpha=0.7, label='Original')
            axes[0, 1].semilogy(f, Pxx_salida, 'r-', linewidth=2, label='Filtrado')
            axes[0, 1].set_title('Análisis Espectral')
            axes[0, 1].set_xlabel('Frecuencia (Hz)')
            axes[0, 1].set_ylabel('PSD')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
            axes[0, 1].set_xlim([0, self.fs/2])
        except:
            axes[0, 1].text(0.5, 0.5, 'Error en análisis espectral', 
                           ha='center', va='center', transform=axes[0, 1].transAxes)
        
        # Diferencia
        diferencia = entrada_volt - salida_volt
        axes[1, 0].plot(t, diferencia, 'g-', linewidth=1)
        axes[1, 0].set_title('Efecto del Filtro')
        axes[1, 0].set_xlabel('Tiempo (s)')
        axes[1, 0].set_ylabel('Diferencia (V)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Métricas
        axes[1, 1].axis('off')
        
        potencia_orig = np.var(entrada_volt)
        potencia_filt = np.var(salida_volt)
        reduccion_db = 10 * np.log10(potencia_orig / potencia_filt) if potencia_filt > 0 else 0
        
        # NUEVO: Verificar si realmente se aplicó filtro
        muestras_diferentes = np.sum(np.array(entrada) != np.array(salida))
        porcentaje_filtrado = (muestras_diferentes / len(entrada)) * 100
        
        # Calcular diferencia promedio
        diferencia_promedio = np.mean(np.abs(np.array(entrada) - np.array(salida)))
        
        texto_metricas = f"""
ANALISIS - FILTRO {nombre_filtro}:

ARCHIVO: {archivo}
DURACION: {len(entrada)/self.fs:.1f} segundos
MUESTRAS: {len(entrada)}

VERIFICACION DE FILTRO:
• Muestras modificadas: {muestras_diferentes}/{len(entrada)}
• Porcentaje filtrado: {porcentaje_filtrado:.1f}%
• Diferencia promedio: {diferencia_promedio:.1f} LSB

POTENCIA:
• Original: {potencia_orig:.4f} V²
• Filtrada: {potencia_filt:.4f} V²
• Reducción: {reduccion_db:.1f} dB

PROCESAMIENTO:
• ESP32: {self.puerto}
• Fs: {self.fs} Hz
• Fc: 800 Hz (aprox)

ESTADO: {'FILTRO APLICADO' if porcentaje_filtrado > 5 else 'SIN FILTRAR'}
        """
        
        # Color del fondo según si se aplicó filtro
        bg_color = "lightgreen" if porcentaje_filtrado > 5 else "lightcoral"
        
        axes[1, 1].text(0.05, 0.95, texto_metricas, transform=axes[1, 1].transAxes,
                        fontsize=9, verticalalignment='top', fontfamily='monospace',
                        bbox=dict(boxstyle="round,pad=0.4", facecolor=bg_color))
        
        plt.tight_layout()
        plt.show()
        
        return reduccion_db
    
    def reproducir_comparacion_simple(self, entrada, salida, nombre_filtro):
        """Reproduce comparación simple del audio"""
        
        print(f"\nREPRODUCCION - FILTRO {nombre_filtro}")
        print("=" * 40)
        
        # Convertir a audio
        entrada_audio = (np.array(entrada) / 511.5) - 1
        salida_audio = (np.array(salida) / 511.5) - 1
        
        # Normalizar
        if np.max(np.abs(entrada_audio)) > 0:
            entrada_audio = entrada_audio / np.max(np.abs(entrada_audio)) * 0.7
        if np.max(np.abs(salida_audio)) > 0:
            salida_audio = salida_audio / np.max(np.abs(salida_audio)) * 0.7
        
        duracion = len(entrada_audio) / self.fs
        print(f"Duración: {duracion:.1f} segundos")
        
        try:
            print(f"\n1. AUDIO ORIGINAL")
            input("   Presiona Enter para reproducir...")
            sd.play(entrada_audio, self.fs)
            sd.wait()
            
            time.sleep(1)
            
            print(f"\n2. AUDIO FILTRADO ({nombre_filtro})")
            input("   Presiona Enter para reproducir...")
            sd.play(salida_audio, self.fs)
            sd.wait()
            
            print(f"\nComparación {nombre_filtro} completada")
            
        except Exception as e:
            print(f"Error en reproducción: {e}")
    
    def comparar_resultados_finales(self, archivo, entrada_fir, salida_fir, entrada_iir, salida_iir):
        """Compara resultados finales FIR vs IIR"""
        
        print(f"\n{'='*60}")
        print("COMPARACION FINAL: FIR vs IIR")
        print(f"{'='*60}")
        
        # Calcular métricas
        entrada_fir_volt = np.array(entrada_fir) * 5.0 / 1023.0
        salida_fir_volt = np.array(salida_fir) * 5.0 / 1023.0
        entrada_iir_volt = np.array(entrada_iir) * 5.0 / 1023.0
        salida_iir_volt = np.array(salida_iir) * 5.0 / 1023.0
        
        pot_orig_fir = np.var(entrada_fir_volt)
        pot_filt_fir = np.var(salida_fir_volt)
        reduccion_fir = 10 * np.log10(pot_orig_fir / pot_filt_fir) if pot_filt_fir > 0 else 0
        
        pot_orig_iir = np.var(entrada_iir_volt)
        pot_filt_iir = np.var(salida_iir_volt)
        reduccion_iir = 10 * np.log10(pot_orig_iir / pot_filt_iir) if pot_filt_iir > 0 else 0
        
        print(f"RESULTADOS COMPARATIVOS:")
        print(f"{'FILTRO':^8} | {'REDUCCION':^10} | {'CALIFICACION':^12}")
        print("-" * 35)
        print(f"{'FIR':^8} | {reduccion_fir:^10.1f} | {'Buena' if reduccion_fir > 1 else 'Regular':^12}")
        print(f"{'IIR':^8} | {reduccion_iir:^10.1f} | {'Buena' if reduccion_iir > 1 else 'Regular':^12}")
        print("-" * 35)
        
        if reduccion_fir > reduccion_iir:
            print(f"GANADOR: FIR (mejor reducción de ruido)")
        elif reduccion_iir > reduccion_fir:
            print(f"GANADOR: IIR (mejor reducción de ruido)")
        else:
            print(f"EMPATE: Ambos filtros similares")
        
        # Reproducción comparativa
        respuesta = input(f"\n¿Reproducir comparación auditiva FIR vs IIR? (s/n): ")
        if respuesta.lower() == 's':
            self.reproducir_fir_vs_iir(salida_fir, salida_iir)
    
    def reproducir_fir_vs_iir(self, salida_fir, salida_iir):
        """Reproduce comparación FIR vs IIR"""
        
        print(f"\nCOMPARACION AUDITIVA: FIR vs IIR")
        print("=" * 40)
        
        try:
            # Convertir a audio
            audio_fir = (np.array(salida_fir) / 511.5) - 1
            audio_iir = (np.array(salida_iir) / 511.5) - 1
            
            # Normalizar
            if np.max(np.abs(audio_fir)) > 0:
                audio_fir = audio_fir / np.max(np.abs(audio_fir)) * 0.7
            if np.max(np.abs(audio_iir)) > 0:
                audio_iir = audio_iir / np.max(np.abs(audio_iir)) * 0.7
            
            print(f"\n1. FILTRO FIR")
            input("   Presiona Enter para escuchar FIR...")
            sd.play(audio_fir, self.fs)
            sd.wait()
            time.sleep(0.5)
            
            print(f"\n2. FILTRO IIR")
            input("   Presiona Enter para escuchar IIR...")
            sd.play(audio_iir, self.fs)
            sd.wait()
            
            print(f"\n¿Cuál filtro suena mejor para esta voz?")
            
        except Exception as e:
            print(f"Error en comparación auditiva: {e}")
    
    def procesar_archivo_especifico(self):
        """Procesa un archivo específico seleccionado por el usuario"""
        
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos WAV disponibles")
            return
        
        print(f"\nArchivos disponibles:")
        for i, archivo in enumerate(archivos_wav):
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   {i+1}. {archivo} ({duracion:.1f}s)")
            except:
                print(f"   {i+1}. {archivo} (error)")
        
        try:
            seleccion = int(input(f"\nSelecciona archivo (1-{len(archivos_wav)}): ")) - 1
            archivo = archivos_wav[seleccion]
            
            print(f"\nFiltros disponibles:")
            print("1. FIR (preserva fase)")
            print("2. IIR (más eficiente)")
            
            filtro_sel = int(input("Selecciona filtro (1/2): "))
            nombres = ["", "FIR", "IIR"]
            nombre_filtro = nombres[filtro_sel]
            
            if self.conectar_esp32():
                entrada, salida = self.procesar_con_esp32_corregido(archivo, filtro_sel)
                
                if entrada is not None and salida is not None:
                    self.generar_analisis_simple(archivo, entrada, salida, nombre_filtro)
                    self.reproducir_comparacion_simple(entrada, salida, nombre_filtro)
                else:
                    print("Error en procesamiento")
                
                self.cerrar_esp32()
            
        except (ValueError, IndexError):
            print("Selección inválida")
        except Exception as e:
            print(f"Error: {e}")
    
    def comparar_fir_vs_iir(self):
        """Compara FIR vs IIR con un archivo seleccionado"""
        
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos WAV disponibles")
            return
        
        print(f"\nSelecciona archivo para comparar FIR vs IIR:")
        for i, archivo in enumerate(archivos_wav):
            print(f"   {i+1}. {archivo}")
        
        try:
            seleccion = int(input(f"\nArchivo (1-{len(archivos_wav)}): ")) - 1
            archivo = archivos_wav[seleccion]
            
            if self.conectar_esp32():
                
                # Procesar con FIR
                print(f"\n{'='*50}")
                print("PROCESANDO CON FIR")
                print(f"{'='*50}")
                entrada_fir, salida_fir = self.procesar_con_esp32_corregido(archivo, 1)
                
                if entrada_fir is not None:
                    self.generar_analisis_simple(archivo, entrada_fir, salida_fir, "FIR")
                
                # Procesar con IIR
                print(f"\n{'='*50}")
                print("PROCESANDO CON IIR")
                print(f"{'='*50}")
                entrada_iir, salida_iir = self.procesar_con_esp32_corregido(archivo, 2)
                
                if entrada_iir is not None:
                    self.generar_analisis_simple(archivo, entrada_iir, salida_iir, "IIR")
                
                # Comparación final
                if entrada_fir is not None and entrada_iir is not None:
                    self.comparar_resultados_finales(archivo, entrada_fir, salida_fir, entrada_iir, salida_iir)
                
                self.cerrar_esp32()
            
        except Exception as e:
            print(f"Error: {e}")
    
    def mostrar_analisis_grabaciones(self):
        """Muestra análisis espectral de las grabaciones"""
        
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos WAV para analizar")
            return
        
        print(f"\nMostrando análisis espectral...")
        
        # Tomar hasta 3 archivos
        archivos_mostrar = archivos_wav[:3]
        
        fig, axes = plt.subplots(len(archivos_mostrar), 2, figsize=(12, 4*len(archivos_mostrar)))
        if len(archivos_mostrar) == 1:
            axes = axes.reshape(1, -1)
        
        for i, archivo in enumerate(archivos_mostrar):
            try:
                fs, audio = wavfile.read(archivo)
                
                if audio.ndim > 1:
                    audio = np.mean(audio, axis=1)
                
                if audio.dtype == np.int16:
                    audio = audio.astype(np.float32) / 32768.0
                
                # Señal temporal
                t = np.arange(len(audio)) / fs
                axes[i, 0].plot(t, audio)
                axes[i, 0].set_title(f'{archivo} - Señal Temporal')
                axes[i, 0].set_xlabel('Tiempo (s)')
                axes[i, 0].set_ylabel('Amplitud')
                axes[i, 0].grid(True, alpha=0.3)
                
                # Espectro
                f, Pxx = signal.welch(audio, fs, nperseg=min(1024, len(audio)//2))
                axes[i, 1].semilogy(f, Pxx)
                axes[i, 1].set_title(f'{archivo} - Espectro')
                axes[i, 1].set_xlabel('Frecuencia (Hz)')
                axes[i, 1].set_ylabel('PSD')
                axes[i, 1].grid(True, alpha=0.3)
                axes[i, 1].axvline(800, color='r', linestyle='--', alpha=0.7, label='fc=800Hz')
                axes[i, 1].legend()
                
                print(f"{archivo}: {len(audio)/fs:.1f}s, pico en {f[np.argmax(Pxx)]:.0f}Hz")
                
            except Exception as e:
                print(f"Error analizando {archivo}: {e}")
        
        plt.tight_layout()
        plt.show()
    
    def reproducir_archivos(self):
        """Reproduce archivos existentes"""
        
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos WAV para reproducir")
            return
        
        print(f"\nArchivos disponibles:")
        for i, archivo in enumerate(archivos_wav):
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   {i+1}. {archivo} ({duracion:.1f}s)")
            except:
                print(f"   {i+1}. {archivo} (error)")
        
        try:
            seleccion = int(input(f"\nSelecciona archivo (1-{len(archivos_wav)}): ")) - 1
            archivo = archivos_wav[seleccion]
            
            fs, audio = wavfile.read(archivo)
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1)
            
            print(f"Reproduciendo {archivo}...")
            sd.play(audio, fs)
            sd.wait()
            print("Reproducción completada")
            
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Función principal del sistema corregido"""
    
    print("SISTEMA PARA CLASE DE FILTROS DIGITALES - ESP32 CORREGIDO")
    print("Version mejorada con sincronización robusta")
    print("=" * 65)
    
    # Detectar puerto ESP32
    puertos = ['COM3', 'COM4', 'COM5', 'COM6', '/dev/ttyUSB0', '/dev/ttyUSB1']
    puerto_detectado = 'COM4'  # Por defecto
    
    for puerto in puertos:
        try:
            test_serial = serial.Serial(puerto, 115200, timeout=1)
            test_serial.close()
            puerto_detectado = puerto
            print(f"Puerto ESP32 detectado: {puerto}")
            break
        except:
            continue
    
    # Crear sistema
    sistema = SistemaCompletoClaseESP32(puerto_detectado)
    
    try:
        sistema.menu_principal_clase()
    except KeyboardInterrupt:
        print(f"\n\nSistema interrumpido - Clase finalizada!")
    except Exception as e:
        print(f"Error en sistema: {e}")
    finally:
        if hasattr(sistema, 'esp32') and sistema.esp32 and sistema.esp32.is_open:
            sistema.esp32.close()

if __name__ == "__main__":
    main()
