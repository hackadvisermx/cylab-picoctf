# Forensics — hideme

## Descripción
> **Prompt oficial del reto:** "Every file gets a flag. The image file could be concealing something.
> Download the image [here](https://challenge-files.cylabacademy.net/library/072ab2768814bc12f4cc180b5e7bf48e8501774bfb741ff9263792824887fd04/flag.png)."
>
> **Hints:**
> 1. Look for hidden data appended after the valid image structure.

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** Geoffrey Njogu

## Solución
El reto proporciona una imagen PNG de 700 × 450 píxeles llamada `flag.png` (22 KB).

1. **Inspección de estructuras de archivo superpuestas (Carving / Appended data):**
   - Una técnica común de ocultamiento de archivos consiste en concatenar o anexar datos al final de una imagen válida, justo después del chunk terminador de PNG (`IEND`, bytes `49 45 4E 44 AE 42 60 82`).
   - Al inspeccionar el archivo con `7zz l flag.png` o `binwalk flag.png`, se detecta un archivo comprimido en formato ZIP incrustado a partir del offset de bytes 15929.
   - La estructura interna del ZIP revela un directorio `secret/` que alberga otra imagen: `secret/flag.png`.

2. **Extracción y lectura del secreto:**
   - Se utiliza `7zz x flag.png` o `binwalk -e flag.png` para extraer el archivo ZIP incrustado.
   - La imagen extraída `secret/flag.png` contiene directamente el texto de la flag en formato gráfico.
   - Puede visualizarse con cualquier visor de imágenes o procesarse mediante OCR (`tesseract`) para obtener el texto.

```bash
# 1. Inspeccionar y listar el contenido del archivo incrustado
7zz l flag.png
# O mediante binwalk:
binwalk flag.png

# 2. Extraer el archivo ZIP contenido dentro del PNG
7zz x flag.png -oextracted/
# O con binwalk:
binwalk -e flag.png

# 3. Leer el texto de la imagen extraída
tesseract extracted/secret/flag.png stdout
```

## Notas adicionales
- Los visores estándar de imágenes PNG ignoran cualquier dato posterior al bloque `IEND`, lo que permite ocultar payloads arbitrarios sin corromper la visualización normal de la imagen portadora.
- Herramientas forenses de file carving como `binwalk`, `foremost` y descompresores multipropósito como `7zz` detectan automáticamente las firmas (magic bytes `PK\x03\x04`) de archivos incrustados.

## Referencias
- Reto: https://learn.cylabacademy.org/library/350
- W3C PNG Specification (Chunk Specifications): https://www.w3.org/TR/png/#5Chunk-layout
- Binwalk: https://github.com/ReFirmLabs/binwalk
