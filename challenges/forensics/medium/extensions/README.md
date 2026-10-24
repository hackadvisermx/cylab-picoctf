# Forensics — extensions

## Descripción
> **Prompt oficial del reto:** "This is a really weird text file. Can you find the flag?
> Get the flag from [TXT](https://challenge-files.cylabacademy.net/library/a5d365fedad883763fb28c78e25a1765220bef6501848c84f2a7a7adf74d83cd/flag.txt)."
>
> **Hints:**
> 1. How do operating systems know what kind of file it is? (It's not just the ending!)
> 2. Make sure to submit the flag as academy{XXXXX}

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Sanjay C/Danny

## Solución
El reto provee un archivo nombrado `flag.txt`, pero su contenido no corresponde a texto plano legible.

1. **Identificación de la cabecera (Magic Bytes):**
   - La extensión de un archivo (`.txt`) es solo una convención del sistema operativo para asociar programas por defecto. El formato real de un archivo se determina por sus números mágicos (*magic numbers*) en los primeros bytes del encabezado.
   - Usando el comando `file flag.txt`, se identifica que la cabecera real corresponde a una imagen PNG:
     `PNG image data, 1697 x 608, 8-bit/color RGB, non-interlaced`
     (Magic bytes `89 50 4E 47 0D 0A 1A 0A`).

2. **Visualización y recuperación de la flag:**
   - Cambiando la extensión a `.png` o abriéndola directamente con un visor de imágenes / herramienta OCR (`tesseract`), se lee la imagen que dibuja la flag en texto estilizado.

```bash
# 1. Determinar el tipo real del archivo mediante sus magic bytes
file flag.txt

# 2. Renombrar el archivo a su extensión legítima
mv flag.txt flag.png

# 3. Leer la flag gráfica mediante OCR o visor de imágenes
tesseract flag.png stdout
```

## Notas adicionales
- La discrepancia entre la extensión y los *magic bytes* de un archivo es un vector recurrente en ciberseguridad, utilizado tanto por atacantes para evadir filtros de subida en aplicaciones web como por analistas forenses para detectar archivos señuelo.

## Referencias
- Reto: https://learn.cylabacademy.org/library/52
- List of file signatures: https://en.wikipedia.org/wiki/List_of_file_signatures
