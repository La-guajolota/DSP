import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# === CONFIGURACIÓN SERIAL ===
PUERTO = '/dev/ttyACM0'   # Cambiar si es diferente
BAUDIOS = 115200

# === Conexión serial ===
try:
    ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
    print(f"Conectado a {PUERTO}")
    time.sleep(2)
except Exception as e:
    print(f"Error al conectar: {e}")
    exit()  # Salir si no se puede conectar al puerto serial

# === DTMF FRECUENCIAS ===
low_freq = [697, 770, 852, 941]
high_freq = [1209, 1336, 1477, 1633]
labels = [f"{f} Hz" for f in low_freq + high_freq]

# === Inicialización de figura ===
plt.style.use('dark_background')
fig, axs = plt.subplots(3, 1, figsize=(12, 9))
fig.suptitle('Monitor DTMF (Arduino Mega)', fontsize=18)

# Gráfico de energía
energias = np.zeros(8)
barras = axs[0].bar(range(8), energias, color='#00BFFF')
axs[0].set_xticks(range(8))
axs[0].set_xticklabels(labels, rotation=45, ha='right')
axs[0].set_ylabel('Energía')
axs[0].set_title('Energía por filtro DTMF')
axs[0].grid(axis='y', alpha=0.3)

# Última tecla detectada
texto_tecla = axs[1].text(0.5, 0.5, "", fontsize=70, ha='center', va='center')
axs[1].axis('off')
axs[1].set_title('Última Tecla Detectada')

# Último comando / acción
texto_comando = axs[2].text(0.5, 0.5, "", fontsize=20, ha='center', va='center', color='lime')
axs[2].axis('off')
axs[2].set_title('Acción / Comando')

# Estado
comando_actual = ""

# === Función de actualización ===
def actualizar(frame):
    global comando_actual
    global energias

    if ser and ser.in_waiting:
        try:
            # Leer línea del puerto serial
            linea = ser.readline().decode(errors='ignore').strip()
            print(f"Datos recibidos: {linea}")  # Depuración

            # Procesar "Tecla detectada"
            if linea.startswith("Tecla detectada:"):
                partes = linea.split(": ")
                if len(partes) > 1:
                    tecla = partes[1]
                    texto_tecla.set_text(tecla)

                    # Actualizar comando actual
                    if tecla == '*':
                        comando_actual = ""
                    elif tecla == '#':
                        texto_comando.set_text(f"Secuencia completa: {comando_actual}")
                    else:
                        comando_actual += tecla

            # Procesar "Energía de filtros"
            elif linea.startswith("Energía de filtros:"):
                for i in range(8):
                    e_line = ser.readline().decode(errors='ignore').strip()
                    partes = e_line.split(" Hz: ")
                    if len(partes) > 1:
                        try:
                            energias[i] = float(partes[1])
                        except ValueError:
                            energias[i] = 0
                # Actualizar las barras de energía
                for i, bar in enumerate(barras):
                    bar.set_height(energias[i])

            # Procesar otros comandos (LED, ACCESO, etc.)
            elif "LED" in linea or "ACCESO" in linea:
                texto_comando.set_text(linea)

        except Exception as e:
            print(f"Error al leer: {e}")
    else:
        print("No se están recibiendo datos del Arduino.")  # Advertencia si no hay datos

    return list(barras) + [texto_tecla, texto_comando]

# Animación
ani = FuncAnimation(fig, actualizar, interval=100, blit=False, cache_frame_data=False)
plt.tight_layout()
plt.subplots_adjust(hspace=0.6)

try:
    plt.show()
except KeyboardInterrupt:
    print("Interfaz cerrada")
finally:
    if ser and ser.is_open:
        ser.close()
        print("Puerto cerrado")