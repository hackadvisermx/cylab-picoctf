# Forensics — DISKO 3

## Descripción
> **Prompt oficial del reto:** "Can you find the flag in this disk image?  
> This time, its not as plain as you think it is!  
> Download the disk image here."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** CyLab Academy
- **Autor:** Darkraicg492

> **Pistas oficiales:**
> 1. How will you search and extract files in a partition?

## Solución
El reto proporciona una imagen de disco `disko-3.dd.gz`. Tras descomprimirla, se examina el sistema de archivos de la imagen.

1. **Inspección de la imagen:**
   Utilizando `7zz` o utilidades del Sleuth Kit (`fls`, `fsstat`), inspeccionamos la estructura:
   ```bash
   7zz l disko-3.dd
   ```
   La imagen consiste en un sistema de archivos FAT32 de 100 MB que alberga principalmente directorios del sistema operativo (`log/`, `log/installer/`, `log/journal/`, etc.).

2. **Búsqueda de archivos de interés:**
   Al filtrar por el nombre `flag`:
   ```bash
   7zz l disko-3.dd | grep -i flag
   ```
   Se detecta un archivo comprimido almacenado en la ruta `log/flag.gz`.

3. **Extracción y descompresión:**
   Extraemos el archivo directamente con `7zz` y lo descomprimimos:
   ```bash
   7zz x disko-3.dd log/flag.gz -o./
   gzip -dc log/flag.gz
   ```
   El contenido descomprimido revela la bandera de la academia.

## Notas adicionales
- En sistemas de archivos FAT32, `7zz` permite listar y extraer archivos directamente sin necesidad de montar la imagen como dispositivo de bucle (`loop device`) ni permisos de superusuario.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/507
- The Sleuth Kit (fls / icat): https://www.sleuthkit.org/sleuthkit/
