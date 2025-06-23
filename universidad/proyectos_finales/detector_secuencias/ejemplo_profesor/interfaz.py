import serial 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation 
from scipy import signal 
import time 
 
# Configuración 
PUERTO_SERIE = 'COM3'  # Cambiar según corresponda 
BAUDRATE = 115200 
MAX_POINTS = 1000  # Número máximo de puntos a mostrar 
 
# Frecuencias DTMF 
low_freq = [697, 770, 852, 941] 
high_freq = [1209, 1336, 1477, 1633] 
 
# Matriz de teclas 
keys = [ 
    ['1', '2', '3', 'A'], 
    ['4', '5', '6', 'B'], 
    ['7', '8', '9', 'C'], 
    ['*', '0', '#', 'D'] 
] 
 
# Inicialización 
ser = None 
try: 
    ser = serial.Serial(PUERTO_SERIE, BAUDRATE) 
    print(f"Conectado a {PUERTO_SERIE} a {BAUDRATE} baudios") 
    time.sleep(2)  # Esperar inicialización 
except Exception as e: 
    print(f"Error al conectar: {e}") 
    exit() 
 
# Crear figura para visualización 
plt.style.use('dark_background') 
fig, axs = plt.subplots(2, 1, figsize=(12, 10)) 
fig.suptitle('Análisis de Tonos DTMF en Tiempo Real') 
 
# Inicializar datos 
filter_energies = np.zeros(8) 
bar_positions = np.arange(8) 
bar_labels = [f"{f} Hz" for f in low_freq + high_freq] 
 
# Crear gráficos de barras para energía de los filtros 
bars = axs[0].bar(bar_positions, filter_energies, color='cyan') 
axs[0].set_xticks(bar_positions) 
axs[0].set_xticklabels(bar_labels, rotation=45) 
axs[0].set_ylabel('Energía') 
axs[0].set_title('Energía por Filtro') 
axs[0].grid(True, axis='y') 
 
# Visualización de tecla detectada 
detected_key_text = axs[1].text(0.5, 0.5, "", fontsize=120,  
                              ha='center', va='center') 
axs[1].set_title('Tecla Detectada') 
axs[1].set_xticks([]) 
axs[1].set_yticks([]) 
 
# Función para actualizar gráficos 
def update_plot(frame): 
    global filter_energies 
     
    # Leer datos del puerto serie 
    if ser.in_waiting: 
        try: 
            line = ser.readline().decode().strip() 
             
            # Procesar datos de energía 
            if line.startswith("Energía de filtros:"): 
                # Leer las siguientes 8 líneas con valores de energía 
                for i in range(8): 
                    energy_line = ser.readline().decode().strip() 
                    try: 
                        # Extraer valor numérico 
                        energy_value = float(energy_line.split(": ")[1]) 
                        filter_energies[i] = energy_value 
                    except: 
                        pass 
                 
                # Actualizar gráfico de barras 
                for i, bar in enumerate(bars): 
                    bar.set_height(filter_energies[i]) 
                 
                # Determinar tecla detectada 
                max_low_idx = np.argmax(filter_energies[:4]) 
                max_high_idx = np.argmax(filter_energies[4:]) + 4 
                 
                # Si ambos superan un umbral, mostrar tecla 
                threshold = 10.0  # Ajustar según datos reales 
                if filter_energies[max_low_idx] > threshold and filter_energies[max_high_idx] > threshold: 
                    row_idx = max_low_idx 
                    col_idx = max_high_idx - 4 
                    key = keys[row_idx][col_idx] 
                    detected_key_text.set_text(key) 
                    detected_key_text.set_color('lime') 
                else: 
                    detected_key_text.set_text("") 
             
            # Mostrar en consola información de tecla detectada 
            if line.startswith("Tecla detectada:"): 
                key = line.split(": ")[1] 
                print(f"Tecla detectada: {key}") 
                 
        except Exception as e: 
            print(f"Error procesando datos: {e}") 
     
    return bars + [detected_key_text] 
 
# Configurar animación 
ani = FuncAnimation(fig, update_plot, interval=100, blit=True) 
 
plt.tight_layout() 
plt.subplots_adjust(hspace=0.3) 
 
try: 
    plt.show() 
except KeyboardInterrupt: 
    print("Análisis finalizado") 
finally: 
    if ser is not None and ser.is_open: 
        ser.close() 
    print("Puerto serial cerrado")