# Forensics — Secret of the Polyglot

## Descripción
> **Prompt oficial del reto:** "The Network Operations Center (NOC) of your local institution picked up a suspicious file, they're getting conflicting information on what type of file it is. They've brought you in as an external expert to examine the file. Can you extract all the information from this strange file?
> 
> Download the suspicious file [here](https://challenge-files.cylabacademy.net/library/70f90e64dbbf4b6c6da7c0cd024663e66eb3fecf36dde7c7947c96debe14885a/flag2of2-final.pdf)."
>
> **Hints:**
> 1. This problem can be solved by just opening the file in different ways

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** syreal

## Solución
El reto presenta un archivo `flag2of2-final.pdf`. El nombre del reto y la pista aluden al concepto de archivo **políglota** (*polyglot*), es decir, un archivo que es sintácticamente válido simultáneamente bajo dos o más formatos distintos (en este caso, PNG y PDF).

1. **Primera mitad de la flag (como imagen PNG):**
   - Aunque la extensión del archivo es `.pdf`, el comando `file` identifica el encabezado inicial como `PNG image data, 200 x 40`.
   - Abriendo el archivo con un visor de imágenes o procesándolo con OCR (`tesseract flag2of2-final.pdf stdout`), se revela la primera mitad de la flag:
     `academy{f1u3n7_...`

2. **Segunda mitad de la flag (como documento PDF):**
   - Más adelante en el binario, tras el bloque PNG, se encuentra la cabecera `%PDF-1.4`.
   - Abriendo el archivo con un visor de PDF o descomprimiendo el flujo del objeto con zlib, se renderiza la segunda mitad de la flag:
     `1n_pn9_&_pdf_2f8da0be}`

3. **Reconstrucción:**
   - Uniendo ambas mitades se completa la flag en formato `academy{...}`.

```bash
# 1. Leer como imagen PNG
tesseract flag2of2-final.pdf stdout
# academy{f1u3n7_...

# 2. Abrir como documento PDF en el visor
pdftotext flag2of2-final.pdf -
# 1n_pn9_&_pdf_2f8da0be}

# O mediante inspección con strings/python zlib
```

## Notas adicionales
- Los archivos políglotas explotan la tolerancia de los formatos de archivo a datos superfluos antes o después de sus marcadores mágicos (por ejemplo, los visores PDF buscan la firma `%PDF-` en los primeros 1024 bytes, mientras que PNG exige sus bytes mágicos exactamente en el offset 0). Son utilizados frecuentemente en ataques de evasión de antivirus o explotación de subida de archivos (bypaseando validaciones MIME).

## Referencias
- Reto: https://learn.cylabacademy.org/library/423
- PoC||GTFO (Polyglot files): https://github.com/angea/pocorgtfo
