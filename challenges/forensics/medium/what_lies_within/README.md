# Forensics — What Lies Within

## Descripción
> **Prompt oficial del reto:** "There's something in the [building](https://challenge-files.cylabacademy.net/library/5235bfccd8f3cc2d059ee828f774846542f28f7ec66cb4f0c6ceb536c38026d4/buildings.png). Can you retrieve the flag?"
>
> **Hints:**
> 1. There is data encoded somewhere... there might be an online decoder.

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Julio/Danny

## Solución
El reto provee una imagen PNG (`buildings.png`). La pista y el título del reto hacen referencia a esteganografía en imágenes para ocultar un mensaje en el plano de bits.

1. **Análisis de planos de bits (LSB Steganography):**
   - La técnica más común de esteganografía espacial en imágenes RGB es LSB (*Least Significant Bit*), donde el bit menos significativo de cada canal de color (R, G, B) de los píxeles contiene datos ocultos sin alterar perceptiblemente los colores de la imagen.
   - Utilizando la herramienta especializada `zsteg`, se escanean automáticamente las combinaciones de canales y planos de bits.
   - En el modo `b1,rgb,lsb,xy` (bit 1, canales RGB, orden secuencial de coordenadas X/Y), se detecta inmediatamente la cadena de la flag en texto claro.

```bash
# Análisis esteganográfico con zsteg
zsteg buildings.png

# O filtrando directamente por cadenas legibles en LSB
zsteg -a buildings.png | grep -E "academy\{|picoCTF\{"
```

```python
#!/usr/bin/env python3
"""Extracción manual de LSB en canales RGB con Python"""
from PIL import Image

img = Image.open("buildings.png")
pixels = img.load()
width, height = img.size

bits = []
for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y][:3]
        bits.extend([r & 1, g & 1, b & 1])

data = bytearray()
for i in range(0, len(bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val = (byte_val << 1) | bits[i + j]
    data.append(byte_val)

flag_start = data.find(b"academy{")
if flag_start != -1:
    flag_end = data.find(b"}", flag_start) + 1
    print("Flag:", data[flag_start:flag_end].decode())
```

## Notas adicionales
- `zsteg` es el estándar *de facto* para la detección rápida de esteganografía LSB en formatos sin pérdida (PNG y BMP), ya que analiza múltiples combinaciones de permutación de canales (RGB, BGR, RGBA), direcciones de barrido y planos de bits de 1 a 8 bits.

## Referencias
- Reto: https://learn.cylabacademy.org/library/74
- zsteg repository: https://github.com/zed-0xff/zsteg
