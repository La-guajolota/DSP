### GUIA DE USO

---

## dconv.py: Convolución Discreta  

### Descripción  
Este script implementa la **convolución discreta** entre dos señales:  
- **Filtro** (`h_filter`): coeficientes que modelan el comportamiento del sistema.  
- **Señal de entrada** (`x_signal`): datos que queremos filtrar.  

La función `dconv(h, x)` recorre todos los solapamientos posibles del filtro sobre la señal y suma los productos para obtener la salida.

### ¿Qué hace?  
1. Calcula la longitud de la señal resultante como `len(h) + len(x) – 1`.  
2. Inicializa un arreglo de ceros de esa longitud.  
3. Para cada posición, multiplica y acumula los valores de `h` y las muestras desplazadas de `x`.  
4. Devuelve la señal convolucionada `y`.

## dft.py: Transformada Discreta de Fourier  

### Descripción  
Este script implementa la **Transformada Discreta de Fourier (DFT)**, una herramienta fundamental en el procesamiento de señales digitales que permite transformar una secuencia de valores en componentes de diferentes frecuencias. La DFT se utiliza para analizar la frecuencia de señales discretas y es esencial en campos como el análisis de señales de audio, procesamiento de imágenes y compresión de datos. :contentReference[oaicite:0]{index=0}

### ¿Qué hace?  
1. **Lectura de la señal**: toma la lista `x`.  
2. **Padding** (opcional): si `padding` es un número, extiende `x` con ceros hasta esa longitud; si no, lleva la longitud al siguiente exponente de 2.  
3. **Cálculo de la DFT**: recorre todas las frecuencias `k` y muestras `n`, sumando `x[n] * exp(-2jπkn/N)`.  
4. **Salida**: retorna un array complejo `X` con valores de DFT.  
5. **Visualización**: gráfica dos subplots—uno con `|X[k]|` (magnitud) y otro con `∠X[k]` (fase).

## dft_signal.py: Análisis de Señal y DFT  
### Descripción  
Este script genera una señal compuesta por la suma de:  
- Una **sinusoidal** de frecuencia `freq` (1 Hz).  
- Una **cosenoidal** de frecuencia `freq/3` (≈0.33 Hz).  

Luego calcula su **Transformada Discreta de Fourier (DFT)** con la función `dft()` importada de `dft.py`, y grafica:  
1. La señal en el tiempo.  
2. La **magnitud** de su DFT.  
3. La **fase** de su DFT.  

### ¿Qué hace cada parte?  
1. **Parámetros de la señal**  
   - `freq`: frecuencia base (Hz).  
   - `signal_duration`: duración en segundos.  
   - `fs`: frecuencia de muestreo (10× la frecuencia base).  
   - `Ts`: vector de tiempos desde 0 hasta `signal_duration` con paso `1/fs`.  

2. **Construcción de la señal**  
   ```python
   x = np.array([
       np.sin(2*np.pi*freq*t)
       + np.cos(2*np.pi*(freq/3)*t)
       for t in Ts
   ])