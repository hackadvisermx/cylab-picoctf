# Forensics — Corrupted file

## Descripción
> **Prompt oficial del reto:** "This file seems broken... or is it? Maybe a couple of bytes could make all the difference. Can you figure out how to bring it back to life?
> Download the file [here](https://challenge-files.cylabacademy.net/library/217bef66dcb5fd0797e1c0f064b705a73600a8be2e1ebadeab51df5be013109d/file)."
>
> **Hints:**
> 1. Try checking the file’s header.
> 2. JPEG
> 3. Tools like xxd or hexdump can help you inspect and edit file bytes.

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoMini by CMU-Africa
- **Autor:** Yahaya Meddy

## Solución
El reto proporciona un archivo sin extensión llamado `file`. Al intentar visualizarlo o ejecutar `file` sobre él, el sistema no reconoce el formato binario porque los bytes iniciales (*magic bytes*) están corruptos.

1. **Inspección de cabecera:**
   - Al examinar los primeros bytes con `xxd` o `hexdump`, se observa la siguiente secuencia:
     `5c 78 ff e0 00 10 4a 46 49 46...`
   - Los bytes `4a 46 49 46` corresponden a la cadena ASCII `JFIF`.
   - Los dos primeros bytes son `5c 78` (los caracteres ASCII `\` y `x`).
   - Una cabecera estándar de imagen JPEG/JFIF debe comenzar con los bytes mágicos `FF D8` (SOI - *Start of Image*), seguidos de `FF E0 00 10 4A 46 49 46` (marcador APP0 JFIF).

2. **Reparación del archivo:**
   - Se reemplazan los dos primeros bytes (`5c 78`) por `ff d8`.
   - Tras este cambio, el comando `file` identifica correctamente el archivo como `JPEG image data, JFIF standard 1.01, 800x500`.

3. **Extracción de la flag:**
   - Al abrir la imagen reparada, se observa el texto de la flag en formato `academy{...}` dibujado en el centro.
   - Mediante OCR (`tesseract`) o inspección de píxeles, se recupera el texto completo de la flag.

```bash
# 1. Inspeccionar primeros bytes
xxd file | head -n 1
# 00000000: 5c78 ffe0 0010 4a46 4946 0001 0100 0001  \x....JFIF......

# 2. Corregir cabecera mágica (reemplazar 5c 78 por ff d8)
python3 -c "
with open('file', 'rb') as f:
    data = bytearray(f.read())
data[0:2] = b'\xff\xd8'
with open('fixed.jpg', 'wb') as f:
    f.write(data)
"

# 3. Verificar tipo de archivo e inspeccionar imagen
file fixed.jpg
# fixed.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 800x500, components 3
```

## Notas adicionales
- Los *magic bytes* son firmas fijas situadas al inicio de los archivos que permiten a los sistemas operativos y visores identificar el formato real de un archivo independientemente de su extensión de nombre.

## Referencias
- Reto: https://learn.cylabacademy.org/library/519
- List of file signatures: https://en.wikipedia.org/wiki/List_of_file_signatures
