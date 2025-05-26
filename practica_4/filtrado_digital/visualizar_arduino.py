import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# --- Función para adquirir datos del Arduino ---
def adquirir_datos(puerto='COM3', baudrate=115200, timeout=10):
    """
    Adquiere datos del Arduino a través del puerto serial.

    Parámetros:
    - puerto: Nombre del puerto COM (por defecto 'COM3').
    - baudrate: Velocidad de comunicación serial (por defecto 115200).
    - timeout: Tiempo máximo de espera para recibir datos (en segundos).

    Retorna:
    - datos_originales: Lista con los datos originales adquiridos.
    - datos_filtrados: Lista con los datos filtrados adquiridos.
    """
    try:
        # Configurar puerto serial
        ser = serial.Serial(puerto, baudrate)
        print(f"Conectado al puerto: {puerto}")
        time.sleep(2)  # Esperar inicialización del Arduino

        # Solicitar datos enviando el comando 's'
        ser.write(b's')
        print("Solicitando datos del buffer...")

        # Variables para almacenar datos
        datos_originales = []
        datos_filtrados = []
        encabezado_leido = False
        inicio = time.time()

        # Leer datos del puerto serial
        while (time.time() - inicio) < timeout:
            if ser.in_waiting:
                linea = ser.readline().decode().strip()

                # Verificar si el buffer ha sido enviado completamente
                if linea == "Buffer enviado y reiniciado":
                    break

                # Leer datos después del encabezado
                if encabezado_leido:
                    try:
                        partes = linea.split(',')
                        datos_originales.append(int(partes[1]))
                        datos_filtrados.append(int(partes[2]))
                    except ValueError:
                        print(f"Error al procesar línea: {linea}")
                elif linea == "index,original,filtered":
                    encabezado_leido = True

        ser.close()
        return datos_originales, datos_filtrados

    except Exception as e:
        print(f"Error al conectar con Arduino: {e}")
        return None, None

# --- Función para analizar y graficar los datos adquiridos ---
def analizar_datos(originales, filtradas, fs=1000):
    """
    Analiza y grafica los datos adquiridos en el dominio del tiempo y la frecuencia.

    Parámetros:
    - originales: Lista con los datos originales.
    - filtradas: Lista con los datos filtrados.
    - fs: Frecuencia de muestreo (por defecto 1000 Hz).
    """
    if originales is None or filtradas is None:
        print("No hay datos para analizar.")
        return

    t = np.arange(len(originales)) / fs  # Vector de tiempo

    # Gráficas en el dominio del tiempo
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(t, originales, label="Original")
    plt.title('Señal Original')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud (ADC)')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(t, filtradas, label="Filtrada", color='orange')
    plt.title('Señal Filtrada')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud (ADC)')
    plt.grid(True)
    plt.tight_layout()

    # Gráficas en el dominio de la frecuencia
    plt.figure(figsize=(12, 8))

    # FFT de la señal original
    X = np.fft.fft(originales)
    freq = np.fft.fftfreq(len(originales), 1/fs)

    plt.subplot(2, 1, 1)
    plt.plot(freq[:len(freq)//2], np.abs(X[:len(X)//2])/len(X))
    plt.title('Espectro de la Señal Original')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True)
    plt.xlim([0, fs/2])

    # FFT de la señal filtrada
    Y = np.fft.fft(filtradas)

    plt.subplot(2, 1, 2)
    plt.plot(freq[:len(freq)//2], np.abs(Y[:len(Y)//2])/len(Y), color='orange')
    plt.title('Espectro de la Señal Filtrada')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True)
    plt.xlim([0, fs/2])

    plt.tight_layout()
    plt.show()

# --- Función para cambiar el tipo de filtro en el Arduino ---
def cambiar_filtro(puerto, tipo_filtro):
    """
    Cambia el tipo de filtro en el Arduino enviando un comando serial.

    Parámetros:
    - puerto: Nombre del puerto COM.
    - tipo_filtro: Tipo de filtro (0: Sin filtro, 1: FIR).
    """
    try:
        ser = serial.Serial(puerto, 115200)
        ser.write(f"{tipo_filtro}".encode())
        print(f"Filtro cambiado a tipo: {'Sin filtro' if tipo_filtro == 0 else 'FIR'}")
        ser.close()
    except Exception as e:
        print(f"Error al cambiar el filtro: {e}")

# --- Función principal ---
def main():
    """
    Función principal para interactuar con el sistema de adquisición y filtrado digital.
    """
    puerto = input("Ingrese el puerto COM (default: COM3): ") or "COM3"

    print("\n--- SISTEMA DE ANÁLISIS DE FILTROS DIGITALES ---")
    print("1. Adquirir datos sin filtro")
    print("2. Adquirir datos con filtro FIR")
    print("3. Salir")

    while True:
        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            cambiar_filtro(puerto, tipo_filtro=0)
            time.sleep(1)
            orig, filt = adquirir_datos(puerto)
            analizar_datos(orig, filt)

        elif opcion == '2':
            cambiar_filtro(puerto, tipo_filtro=1)
            time.sleep(1)
            orig, filt = adquirir_datos(puerto)
            analizar_datos(orig, filt)

        elif opcion == '3':
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

# --- Punto de entrada ---
if __name__ == "__main__":
    main()