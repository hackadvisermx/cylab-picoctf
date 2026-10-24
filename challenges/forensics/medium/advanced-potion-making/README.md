# Forensics — advanced-potion-making

## Descripción
> **Prompt oficial del reto:** "Ron just found his own copy of advanced potion making, but its been corrupted by some kind of spell. Help him recover it!"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoMini by redpwn
- **Autor:** bigC

## Solución
El reto suministra un archivo binario corrupto (`advanced-potion-making`).

1. **Reparación de la cabecera PNG:**
   Al inspeccionar los primeros bytes en hexadecimal:
   `89 50 42 11 0d 0a 1a 0a 00 12 13 14 49 48 44 52 ...`
   Se detecta una cabecera de imagen PNG con bytes alterados intencionalmente:
   - Firma PNG: debe ser `89 50 4E 47 0D 0A 1A 0A` (`\x89PNG\r\n\x1a\n`).
   - Longitud del chunk `IHDR`: debe ser exactamente `00 00 00 0D` (13 bytes).
   - Recalculamos el CRC32 del chunk `IHDR` corregido.

```python
import zlib

with open("advanced-potion-making", "rb") as f:
    data = bytearray(f.read())

data[:8] = b"\x89PNG\r\n\x1a\n"
data[8:12] = b"\x00\x00\x00\x0d"
crc = zlib.crc32(data[12:12+4+13])
data[12+4+13:12+4+13+4] = crc.to_bytes(4, "big")

with open("fixed.png", "wb") as f:
    f.write(data)
```

2. **Análisis de planos de color / Esteganografía:**
   Al abrir la imagen reparada, se observa un lienzo predominantemente rojo.
   Analizando los valores de los canales RGB con Python y NumPy:
   - Canal Rojo: valores discretos `[237, 238, 239]`
   - Canal Verde: valores `[17, 18]`
   - Canal Azul: valores `[27, 28, 29]`

   Aislando los píxeles donde `R == 239`:
   ```python
   from PIL import Image
   import numpy as np

   im = Image.open("fixed.png")
   arr = np.array(im)
   r = arr[:, :, 0]
   mask = (r == 239).astype(np.uint8) * 255
   Image.fromarray(mask).save("flag_revealed.png")
   ```
   La imagen resultante `flag_revealed.png` muestra el texto nítido de la bandera en formato original del evento `picoCTF{...}`.

## Notas adicionales
- Cuando un archivo PNG está dañado, la mayoría de visualizadores rechazan cargarlo por completo si la firma o los chunks críticos (`IHDR`, `IDAT`, `IEND`) tienen tamaños o sumas de verificación CRC32 incorrectas.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/205
- W3C PNG Specification: https://www.w3.org/TR/png-3/
