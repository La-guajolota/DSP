### GUIA DE USO

## Convolución Discreta (dconv.py): Algoritmo y Uso
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

