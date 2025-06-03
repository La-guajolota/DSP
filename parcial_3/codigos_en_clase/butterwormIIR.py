import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, freqz, lfilter, zpk2tf
import warnings
warnings.filterwarnings('ignore')
 
# Filtro digital Butterworth
# Se estiman el orden N y la frecuencia de corte del filtro
# H(s)
 
# Parámetros del filtro Butterworth
N = 3  # Orden del filtro
Wc = 0.5883  # Frecuencia de corte normalizada
 
print(f"Orden del filtro: {N}")
print(f"Frecuencia de corte: {Wc}")
 
# Se obtienen los coeficientes del filtro Butterworth digital
# Equivalente a buttord y butter en MATLAB
b, a = butter(N, Wc, btype='low', analog=False, output='ba')
 
print(f"\nCoeficientes del numerador (b): {b}")
print(f"Coeficientes del denominador (a): {a}")
 
# Se obtienen los polos y la función de transferencia H(s)
# Calcular polos y ceros
z, p, k = signal.tf2zpk(b, a)
 
print(f"\nCeros: {z}")
print(f"Polos: {p}")
print(f"Ganancia: {k}")
 
# Se aplica la transformación bilineal (T=2) implícita en butter
# (Ya está aplicada en la función butter de scipy)
 
# Se grafican los polos y ceros de Hd(z)
plt.figure(1, figsize=(10, 8))
plt.subplot(2, 2, 1)
 
# Dibujar círculo unitario
theta = np.linspace(0, 2*np.pi, 1000)
circle_x = np.cos(theta)
circle_y = np.sin(theta)
plt.plot(circle_x, circle_y, 'k--', alpha=0.5, label='Círculo unitario')
 
# Graficar polos y ceros
if len(z) > 0:
    plt.plot(np.real(z), np.imag(z), 'o', markersize=8, label='Ceros', color='blue')
plt.plot(np.real(p), np.imag(p), 'x', markersize=8, label='Polos', color='red')
 
plt.grid(True)
plt.axis('equal')
plt.xlabel('Parte Real')
plt.ylabel('Parte Imaginaria')
plt.title('Polos y ceros de Hd(z)')
plt.legend()
 
# Se evalúa z=e(jw) y se obtiene la Respuesta en Frecuencia Hd(ejw)
w, Hw = freqz(b, a, worN=1024, whole=False)
 
# Gráfica de respuesta en frecuencia - escala lineal
plt.subplot(2, 2, 2)
plt.plot(w*5000/np.pi, np.abs(Hw))
plt.title('Respuesta en frecuencia en lineal del filtro digital')
plt.xlabel('frecuencia en rad/s, w/pi')
plt.ylabel('|H(w)|')
plt.grid(True)
 
# Gráfica de respuesta en frecuencia - escala logarítmica
plt.subplot(2, 2, 3)
plt.plot(w/np.pi, 20*np.log10(np.abs(Hw)))
plt.title('Respuesta en frecuencia en dB del filtro digital')
plt.xlabel('frecuencia en rad/s, w/pi')
plt.ylabel('|H(w)| (dB)')
plt.grid(True)
 
# Respuesta al impulso del filtro digital
plt.subplot(2, 2, 4)
# Crear impulso unitario
impulse = np.zeros(50)
impulse[0] = 1
hn1 = lfilter(b, a, impulse)
 
plt.stem(range(len(hn1)), hn1, basefmt=" ")
plt.title('Respuesta al impulso del filtro digital')
plt.xlabel('n (muestras)')
plt.ylabel('h[n]')
plt.grid(True)
 
plt.tight_layout()
plt.show()
 
# Señal senoidal de prueba
n1 = np.arange(0, 300)  # 300 muestras
w0 = 0.7 * np.pi
xn = np.cos(w0 * n1)
 
print(f"\nSeñal de prueba:")
print(f"Frecuencia: w0 = {w0:.4f} rad")
print(f"Número de muestras: {len(n1)}")
 
# Se filtra la señal de prueba
yn1 = lfilter(b, a, xn)
 
# Gráfica de la señal filtrada
plt.figure(2, figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(n1, xn, 'b-', label='Señal original')
plt.title('Señal original')
plt.xlabel('n (muestras)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
 
plt.subplot(2, 1, 2)
plt.plot(n1, yn1, 'r-', label='Señal filtrada')
plt.title('Señal filtrada')
plt.xlabel('n (muestras)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
 
plt.tight_layout()
plt.show()
 
# Información adicional del filtro
print(f"\nInformación del filtro:")
print(f"Tipo: Butterworth paso-bajas")
print(f"Orden: {N}")
print(f"Frecuencia de corte normalizada: {Wc}")
print(f"Frecuencia de corte en Hz (asumiendo fs=1): {Wc/2:.4f} Hz")
 
# Verificar estabilidad
if all(np.abs(p) < 1):
    print("El filtro es ESTABLE (todos los polos dentro del círculo unitario)")
else:
    print("ADVERTENCIA: El filtro puede ser INESTABLE")