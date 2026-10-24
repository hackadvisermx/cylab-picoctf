# Forensics — Sleuthkit Apprentice

## Descripción
> **Prompt oficial del reto:** "Download this disk image and find the flag.  
>  
> Note: if you are using the webshell, download and extract the disk image into `/tmp` not your home directory.  
> Download compressed disk image"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto provee una imagen de disco con múltiples particiones (`disk.flag.img.gz`).

1. **Extracción y examen de particiones:**
   ```bash
   gzip -dc disk.flag.img.gz > disk.flag.img
   7zz l disk.flag.img
   ```
   Se identifican 3 particiones:
   - `0.img` (100 MB)
   - `1.img` (75 MB)
   - `2.img` (124 MB, sistema ext4 raíz)

2. **Inspección del sistema de archivos ext4:**
   Buscamos archivos relacionados con la bandera en la partición 3 (`2.img`):
   ```bash
   7zz e disk.flag.img 2.img -o./
   7zz l 2.img | grep -i flag
   ```
   Se localiza el archivo: `root/my_folder/flag.uni.txt`.

3. **Extracción y lectura de la bandera:**
   ```bash
   7zz e 2.img root/my_folder/flag.uni.txt -o./
   cat flag.uni.txt
   ```
   El archivo contiene los caracteres de la bandera separados por espacios:
   `a c a d e m y { ... }`.
   Eliminando los espacios se obtiene la bandera requerida.

## Notas adicionales
- El formato de texto con espaciado uniforme a menudo se utiliza para eludir búsquedas de cadenas contiguas simples en análisis de triaje rápido.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/300
- The Sleuth Kit (fls / icat): https://www.sleuthkit.org/sleuthkit/
