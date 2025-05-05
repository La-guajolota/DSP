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