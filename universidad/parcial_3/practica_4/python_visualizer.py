import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import re

class ArduinoFilterAnalyzer:
    def __init__(self, puerto='COM3', baudrate=115200):
        self.puerto = puerto
        self.baudrate = baudrate
        self.fs = 200  # Frecuencia de muestreo corregida (5ms = 200Hz)
        
    def conectar_arduino(self, timeout=30):
        """Establece conexión con Arduino con timeout extendido"""
        try:
            ser = serial.Serial(self.puerto, self.baudrate, timeout=2)
            print(f"✓ Conectado al puerto: {self.puerto}")
            time.sleep(3)  # Tiempo extra para inicialización
            
            # Limpiar buffer de entrada
            ser.reset_input_buffer()
            return ser
            
        except Exception as e:
            print(f"✗ Error al conectar con Arduino: {e}")
            return None
    
    def cambiar_filtro(self, tipo_filtro=0):
        """Cambia el tipo de filtro en Arduino"""
        ser = self.conectar_arduino()
        if ser is None:
            return False
            
        try:
            print(f"Cambiando a filtro tipo: {tipo_filtro}")
            ser.write(str(tipo_filtro).encode())
            time.sleep(1)
            
            # Leer respuesta
            start_time = time.time()
            while (time.time() - start_time) < 3:
                if ser.in_waiting:
                    respuesta = ser.readline().decode().strip()
                    print(f"Arduino: {respuesta}")
                    if ">>>" in respuesta:
                        break
            
            ser.close()
            return True
            
        except Exception as e:
            print(f"Error cambiando filtro: {e}")
            if ser:
                ser.close()
            return False
    
    def iniciar_recoleccion(self):
        """Inicia la recolección de datos en Arduino"""
        ser = self.conectar_arduino()
        if ser is None:
            return False
            
        try:
            print("Iniciando recolección de datos...")
            ser.write(b's')
            time.sleep(1)
            
            # Monitorear progreso
            start_time = time.time()
            timeout = 60  # 1 minuto timeout
            
            while (time.time() - start_time) < timeout:
                if ser.in_waiting:
                    linea = ser.readline().decode().strip()
                    print(f"Arduino: {linea}")
                    
                    if "BUFFER COMPLETO" in linea:
                        print("✓ Recolección completada")
                        ser.close()
                        return True
                    elif "Timeout" in linea:
                        print("⚠ Timeout en Arduino")
                        ser.close()
                        return True
                        
                time.sleep(0.1)
            
            print("⚠ Timeout esperando datos")
            ser.close()
            return False
            
        except Exception as e:
            print(f"Error iniciando recolección: {e}")
            if ser:
                ser.close()
            return False
    
    def adquirir_datos(self, timeout=30):
        """Adquiere datos del buffer de Arduino"""
        ser = self.conectar_arduino()
        if ser is None:
            return None, None
            
        try:
            print("Solicitando datos del buffer...")
            ser.write(b's')
            time.sleep(1)
            
            datos_originales = []
            datos_filtrados = []
            estado = "esperando"
            
            inicio = time.time()
            while (time.time() - inicio) < timeout:
                if ser.in_waiting:
                    linea = ser.readline().decode().strip()
                    
                    # Debug: mostrar líneas recibidas
                    if linea and not linea.startswith("Arduino:"):
                        print(f"Recibido: {linea}")
                    
                    # Detectar inicio de datos
                    if linea == "index,original,filtered":
                        estado = "leyendo_datos"
                        print("✓ Encabezado CSV detectado")
                        continue
                    
                    # Detectar fin de datos
                    if "FIN DE DATOS" in linea:
                        print("✓ Fin de datos detectado")
                        break
                    
                    # Procesar datos CSV
                    if estado == "leyendo_datos":
                        try:
                            # Usar regex para extraer números
                            numeros = re.findall(r'\d+', linea)
                            if len(numeros) >= 3:
                                datos_originales.append(int(numeros[1]))
                                datos_filtrados.append(int(numeros[2]))
                        except (ValueError, IndexError):
                            # Ignorar líneas mal formadas
                            continue
                
                time.sleep(0.01)  # Pequeña pausa para no saturar
            
            ser.close()
            
            # Convertir a arrays numpy
            if datos_originales:
                print(f"✓ Datos adquiridos: {len(datos_originales)} muestras")
                return np.array(datos_originales), np.array(datos_filtrados)
            else:
                print("✗ No se recibieron datos válidos")
                return None, None
                
        except Exception as e:
            print(f"Error adquiriendo datos: {e}")
            if ser:
                ser.close()
            return None, None
    
    def reset_arduino(self):
        """Reinicia el buffer de Arduino"""
        ser = self.conectar_arduino()
        if ser is None:
            return False
            
        try:
            ser.write(b'r')
            time.sleep(1)
            
            # Leer confirmación
            start_time = time.time()
            while (time.time() - start_time) < 3:
                if ser.in_waiting:
                    respuesta = ser.readline().decode().strip()
                    print(f"Arduino: {respuesta}")
                    if "REINICIADO" in respuesta:
                        break
            
            ser.close()
            return True
            
        except Exception as e:
            print(f"Error reiniciando: {e}")
            if ser:
                ser.close()
            return False
    
    def analizar_datos(self, originales, filtradas):
        """Analiza y grafica los datos adquiridos"""
        if originales is None or filtradas is None:
            print("No hay datos para analizar")
            return
        
        print(f"Analizando {len(originales)} muestras...")
        
        # Convertir ADC a voltaje (0-1023 -> 0-5V)
        volt_orig = originales * 5.0 / 1023.0
        volt_filt = filtradas * 5.0 / 1023.0
        
        t = np.arange(len(originales)) / self.fs  # Vector de tiempo
        
        # Crear figura con subplots
        fig = plt.figure(figsize=(15, 10))
        
        # 1. Señales in tiempo
        plt.subplot(2, 2, 1)
        plt.plot(t, volt_orig, 'b-', alpha=0.7, label='Original')
        plt.plot(t, volt_filt, 'r-', linewidth=2, label='Filtrada')
        plt.title('Señales en el Dominio del Tiempo')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Voltaje (V)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 2. Espectros de frecuencia
        plt.subplot(2, 2, 2)
        
        # FFT de ambas señales
        N = len(originales)
        freq = np.fft.fftfreq(N, 1/self.fs)
        X_orig = np.fft.fft(volt_orig)
        X_filt = np.fft.fft(volt_filt)
        
        # Plotear solo frecuencias positivas
        pos_freq = freq[:N//2]
        plt.plot(pos_freq, np.abs(X_orig[:N//2])/N, 'b-', alpha=0.7, label='Original')
        plt.plot(pos_freq, np.abs(X_filt[:N//2])/N, 'r-', linewidth=2, label='Filtrada')
        plt.title('Espectro de Frecuencias')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud (V)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim([0, self.fs/2])
        
        # 3. Respuesta del filtro
        plt.subplot(2, 2, 3)
        if not np.array_equal(originales, filtradas):
            # Calcular respuesta en frecuencia del filtro
            H = np.divide(X_filt, X_orig, out=np.zeros_like(X_filt), where=X_orig!=0)
            plt.plot(pos_freq, 20*np.log10(np.abs(H[:N//2]) + 1e-10))
            plt.title('Respuesta en Frecuencia del Filtro')
            plt.xlabel('Frecuencia (Hz)')
            plt.ylabel('Magnitud (dB)')
            plt.grid(True, alpha=0.3)
            plt.xlim([0, self.fs/2])
        else:
            plt.text(0.5, 0.5, 'Sin filtrado aplicado', transform=plt.gca().transAxes, 
                    ha='center', va='center', fontsize=12)
            plt.title('Respuesta del Filtro')
        
        # 4. Estadísticas
        plt.subplot(2, 2, 4)
        plt.axis('off')
        
        # Calcular estadísticas
        stats_text = f"""
        ESTADÍSTICAS DE LAS SEÑALES
        
        Señal Original:
        • Promedio: {np.mean(volt_orig):.3f} V
        • Desv. Estándar: {np.std(volt_orig):.3f} V
        • Min/Max: {np.min(volt_orig):.3f} / {np.max(volt_orig):.3f} V
        
        Señal Filtrada:
        • Promedio: {np.mean(volt_filt):.3f} V
        • Desv. Estándar: {np.std(volt_filt):.3f} V
        • Min/Max: {np.min(volt_filt):.3f} / {np.max(volt_filt):.3f} V
        
        Reducción de ruido:
        • Ratio STD: {np.std(volt_orig)/np.std(volt_filt):.2f}
        
        Parámetros:
        • Muestras: {len(originales)}
        • Fs: {self.fs} Hz
        • Duración: {len(originales)/self.fs:.2f} s
        """
        
        plt.text(0.1, 0.9, stats_text, transform=plt.gca().transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace')
        
        plt.tight_layout()
        plt.show()
        
        return volt_orig, volt_filt

def main():
    # Configuración
    puerto = input("Ingrese el puerto COM (default: COM3): ").strip() or "COM3"
    
    # Crear analizador
    analyzer = ArduinoFilterAnalyzer(puerto)
    
    print("\n" + "="*50)
    print("    SISTEMA DE ANÁLISIS DE FILTROS DIGITALES")
    print("="*50)
    print("1. Probar sin filtro")
    print("2. Probar con filtro FIR")
    print("3. Comparar filtros")
    print("4. Reset Arduino")
    print("5. Salir")
    print("="*50)
    
    while True:
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            print("\n--- PRUEBA SIN FILTRO ---")
            if analyzer.cambiar_filtro(0):
                time.sleep(2)
                if analyzer.iniciar_recoleccion():
                    time.sleep(2)
                    orig, filt = analyzer.adquirir_datos()
                    analyzer.analizar_datos(orig, filt)
        
        elif opcion == '2':
            print("\n--- PRUEBA CON FILTRO FIR ---")
            if analyzer.cambiar_filtro(1):
                time.sleep(2)
                if analyzer.iniciar_recoleccion():
                    time.sleep(2)
                    orig, filt = analyzer.adquirir_datos()
                    analyzer.analizar_datos(orig, filt)
        
        elif opcion == '3':
            print("\n--- COMPARACIÓN DE FILTROS ---")
            
            # Datos sin filtro
            print("Recolectando datos SIN filtro...")
            analyzer.reset_arduino()
            time.sleep(1)
            analyzer.cambiar_filtro(0)
            time.sleep(2)
            analyzer.iniciar_recoleccion()
            time.sleep(2)
            orig1, filt1 = analyzer.adquirir_datos()
            
            # Datos con filtro FIR
            print("\nRecolectando datos CON filtro FIR...")
            analyzer.reset_arduino()
            time.sleep(1)
            analyzer.cambiar_filtro(1)
            time.sleep(2)
            analyzer.iniciar_recoleccion()
            time.sleep(2)
            orig2, filt2 = analyzer.adquirir_datos()
            
            # Comparar si ambos conjuntos son válidos
            if orig1 is not None and orig2 is not None:
                print("Graficando comparación...")
                analyzer.analizar_datos(orig1, filt1)
                analyzer.analizar_datos(orig2, filt2)
        
        elif opcion == '4':
            print("\n--- RESET ARDUINO ---")
            analyzer.reset_arduino()
        
        elif opcion == '5':
            print("Saliendo...")
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()