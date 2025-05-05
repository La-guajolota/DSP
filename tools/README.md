<!-- Estilos inline para colores y diseño -->
<style>
  .section-title { font-size: 1.6em; color: #2c3e50; border-bottom: 2px solid #2980b9; margin-top: 1.5em; padding-bottom: 0.2em; }
  .subsection-title { font-size: 1.3em; color: #34495e; margin-top: 1em; }
  .code-block { background: #ecf0f1; padding: 1em; border-radius: 5px; font-family: monospace; }
  .highlight { background: #f1c40f; padding: 0.1em 0.3em; border-radius: 3px; }
  .bullet { color: #2980b9; font-weight: bold; }
</style>

<div class="section-title">GUÍA DE USO</div>

---

<div class="subsection-title">📁 dconv.py: Convolución Discreta</div>

**Descripción**  
Este script aplica una operación de <span class="highlight">convolución discreta</span> entre:  
- <span class="bullet">•</span> **Filtro** (`h_filter`): define cómo responde el sistema.  
- <span class="bullet">•</span> **Señal de entrada** (`x_signal`): datos originales a procesar.  

La función `<code>dconv(h, x)</code>` desliza el filtro sobre la señal, multiplica y suma los productos para obtener la salida.

**Flujo de ejecución**  
1. 🧮 Calcula la longitud de salida: <code>len(h) + len(x) – 1</code>.  
2. 🔢 Crea un array de ceros de esa longitud.  
3. 🔄 Para cada índice, acumula <code>h[k] * x[n-k]</code> cuando aplique.  
4. 📤 Devuelve la señal convolucionada `y`.

<details>
<summary><strong>Código clave</strong></summary>

<div class="code-block">
```python
def dconv(h, x):
    len_h, len_x = len(h), len(x)
    y = [0] * (len_h + len_x - 1)
    for n in range(len(y)):
        for k in range(len_h):
            if 0 <= n - k < len_x:
                y[n] += h[k] * x[n - k]
    return y
