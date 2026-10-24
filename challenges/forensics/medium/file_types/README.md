# Forensics — File types

## Descripción
> **Prompt oficial del reto:** "This file was found among some files marked confidential but my pdf reader cannot read it, maybe yours can.  
> You can download the file from here."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** Geoffrey Njogu

> **Pistas oficiales:**
> 1. Remember that some file types can contain and nest other files

## Solución
El reto suministra un archivo con extensión `.pdf` que no es un PDF válido.

1. **Identificación inicial del tipo de archivo:**
   ```bash
   file Flag.pdf
   # Flag.pdf: shell archive text
   ```
   Se trata de un archivo Shell Archive (`shar`). Al ejecutarlo con `sh Flag.pdf`, extrae un archivo llamado `flag`.

2. **Desempaquetado recursivo de capas de compresión:**
   El archivo `flag` ha sido empaquetado sucesivamente en múltiples formatos de compresión anidados:
   - Capa 1: `ar archive` -> `flag`
   - Capa 2: `cpio archive` -> `flag`
   - Capa 3: `bzip2 compressed data` -> `bzip2 -d`
   - Capa 4: `gzip compressed data` -> `gzip -d`
   - Capa 5: `lzip compressed data` -> `lzip -d`
   - Capa 6: `LZ4 compressed data` -> `lz4 -d`
   - Capa 7: `LZMA compressed data` -> `xz -d`
   - Capa 8: `lzop compressed data` -> `lzop -d`
   - Capa 9: `lzip compressed data` -> `lzip -d`
   - Capa 10: `XZ compressed data` -> `xz -d`
   - Capa 11: `ASCII text` conteniendo una cadena hexadecimal:
     `61636164656d797b...`

3. **Decodificación de la bandera:**
   ```bash
   echo "61636164656d797b..." | xxd -r -p
   ```
   La conversión de hex a texto plano imprime la bandera.

## Notas adicionales
- Este desafío refuerza el uso de la utilidad `file` para identificar firmas binarias (*magic bytes*) independientemente de las extensiones de archivo declaradas.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/268
- Linux file utility and magic database: https://www.darwinsys.com/file/
