# Forensics — MSB

## Descripción
> **Prompt oficial del reto:** "This image seems to hide something in its bits... Most Significant Bit steganography is a fun twist on traditional LSB techniques.
> Download the image [here](https://challenge-files.cylabacademy.net/library/69c14eeee4da4e8eb3f3529914a6fd1f0fde9d4a2a8f68d2aa388b519d1bd747/Ninja-and-Prince-Genji-Ukiyoe-Utagawa-Kunisada.flag.png)."
>
> **Hints:**
> 1. Remember how LSB works, and see how it might be adapted for MSB.

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona una imagen PNG de 1074 × 1500 píxeles en formato RGB (24 bits) titulada `Ninja-and-Prince-Genji-Ukiyoe-Utagawa-Kunisada.flag.png`.

1. **Comprensión de esteganografía MSB (Most Significant Bit):**
   - A diferencia de la esteganografía LSB tradicional (que altera el bit menos significativo `bit 0` para minimizar distorsiones visuales), aquí los datos ocultos se incrustaron en el bit más significativo (`bit 7`, MSB) de cada uno de los canales de color (R, G, B).
   - Para extraer el mensaje, se recorre la imagen píxel a píxel en orden de lectura estándar (fila por fila, de izquierda a derecha), extrayendo el bit 7 de los canales R, G y B consecutivamente:
     $$\text{bit} = (\text{channel\_value} \gg 7) \ \& \ 1$$
   - Cada 8 bits extraídos se agrupan en un byte (con el primer bit recibido colocado en la posición más significativa).

2. **Extracción y recuperación del mensaje:**
   - Al reconstruir los bytes resultantes, se observa que el contenido extraído corresponde al libro de dominio público *The History of Don Quixote* de Miguel de Cervantes (Project Gutenberg).
   - Buscando la expresión regular `academy\{[^}]+\}` en los datos decodificados, se localiza la flag oculta dentro del texto.

```python
#!/usr/bin/env python3
"""Script de extracción de esteganografía MSB en canales RGB."""
from PIL import Image
import re

# Cargar la imagen
img = Image.open("Ninja-and-Prince-Genji-Ukiyoe-Utagawa-Kunisada.flag.png")
width, height = img.size
pixels = img.load()

# Extraer el bit más significativo (bit 7) de cada canal R, G, B
bits = []
for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]
        bits.append((r >> 7) & 1)
        bits.append((g >> 7) & 1)
        bits.append((b >> 7) & 1)

# Agrupar bits en bytes (MSB-first)
data = bytearray()
for i in range(0, len(bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val = (byte_val << 1) | bits[i + j]
    data.append(byte_val)

# Buscar el patrón de la flag
match = re.search(rb"academy\{[^}]+\}", data)
if match:
    print("Flag encontrada:", match.group().decode())
```

```bash
# Ejecutar la extracción con Python
python3 solve_msb.py
```

## Notas adicionales
- Usar el MSB para ocultar información genera un patrón visual ruidoso o distorsiones de contraste perceptibles en la imagen original, lo cual es inusual para esteganografía encubierta en el mundo real, pero común como variante conceptual en competencias de seguridad (CTF).
- Herramientas como `stegsolve` o bibliotecas como `Pillow` y `numpy` facilitan la inspección individual de los planos de bits (bit planes).

## Referencias
- Reto: https://learn.cylabacademy.org/library/359
- Pillow (PIL Fork) Documentation: https://pillow.readthedocs.io/
