# Forensics — DISKO 2

## Descripción
> **Prompt oficial del reto:** "Can you find the flag in this disk image?  
> The right one is Linux! One wrong step and its all gone!  
> Download the disk image here."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** CyLab Academy
- **Autor:** Darkraicg492

> **Pistas oficiales:**
> 1. How can you extract/isolate a partition?

## Solución
El reto provee una imagen particionada `disko-2.dd.gz` (100 MB).

1. **Inspección de las particiones:**
   Listamos la tabla de particiones MBR:
   ```bash
   7zz l disko-2.dd
   ```
   Se observan tres particiones:
   - `0.img` (25 MB, ext4)
   - `1.fat` (32 MB, FAT16)
   - `2` (42 MB, datos no formateados)

2. **Detección de señuelos y análisis del mensaje:**
   El prompt advierte explícitamente: *"The right one is Linux! One wrong step and its all gone!"*.
   Si realizamos una búsqueda de cadenas `academy{` en las particiones `1.fat` o `2`, encontramos 50 cadenas falsas generadas con permutaciones de caracteres hex aleatorios como señuelos.
   
3. **Aislamiento de la partición Linux:**
   Extraemos únicamente la partición Linux (`0.img`):
   ```bash
   7zz x disko-2.dd 0.img -o./parts/
   file parts/0.img
   ```
   Confirmamos que `0.img` corresponde a `Linux rev 1.0 ext4 filesystem data`.
   Al buscar cadenas coincidentes con el formato de bandera dentro de esta partición:
   ```bash
   strings -a parts/0.img | grep "academy{"
   ```
   A diferencia de las demás particiones repletas de señuelos, en la partición Linux ext4 existe exactamente una única bandera válida.

## Notas adicionales
- Este desafío enseña la importancia de aislar y analizar particiones específicas en evidencia forense para no caer en trampas y datos de distracción (*honeytokens* o *anti-forensics decoys*).
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/506
- Sleuthkit mmls / fls: https://wiki.sleuthkit.org/index.php?title=Mmls
