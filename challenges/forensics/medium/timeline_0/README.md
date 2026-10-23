# Forensics — Timeline 0

## Descripción
> **Prompt oficial del reto:** "Can you find the flag in this disk image? Wrap what you find in the academy{} flag format.
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/bf9a20c350075c5863371e078daee1d570d4062902edc8a4a042e02a7cebf161/partition4.img.gz)."
>
> **Hints:**
> 1. Create a Sleuthkit MAC timeline!
> 2. Sloppy timestomping can yield strange (very old) timestamps

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

## Solución
El reto suministra una imagen de disco comprimida `partition4.img.gz` correspondiente a un sistema de archivos Linux `ext4`. Las pistas sugieren crear una línea de tiempo (MAC timeline) y buscar anomalías temporales causadas por técnicas de *timestomping* (falsificación de fechas de modificación/acceso/creación).

1. **Descompresión y generación de línea de tiempo:**
   - Se descomprime la imagen con `gzip -d`.
   - Utilizando The Sleuth Kit (TSK), se ejecuta `fls -r -m / partition4.img` para generar un volcado de metadatos en formato *bodyfile*.
   - A partir del *bodyfile*, se ordenan los registros cronológicamente.

2. **Detección de la anomalía temporal (*Outlier*):**
   - Mientras que los archivos legítimos del sistema operativo presentan fechas situadas entre los años 2021 y 2025, resalta una única entrada anómala en `/bin/bcab` (inodo `4945`, tamaño 41 bytes).
   - Todas sus marcas de tiempo (MACB) fueron modificadas intencionalmente al 1 de enero de 1985 (`1985-01-01 17:00:00 UTC` / timestamp Unix `473446800`).

3. **Extracción y decodificación del artefacto:**
   - Empleando la herramienta `icat` de Sleuthkit sobre el inodo `4945`, se extrae el contenido del archivo:
     `NzFtMzExbjNfMHU3MTEzcl9oM3JfNDNhMmU3YWYK`
   - La cadena decodificada en Base64 revela:
     `71m311n3_0u7113r_h3r_43a2e7af`
   - Envolviendo el resultado en el formato solicitado `academy{...}` se obtiene la flag.

```bash
# 1. Descomprimir imagen
gzip -d partition4.img.gz

# 2. Generar bodyfile con The Sleuth Kit
fls -r -m / partition4.img > body.txt

# 3. Analizar línea de tiempo y buscar fechas anómalas
mactime -b body.txt -d | head -n 10
# Se observa:
# 1985-01-01 17:00:00,41,macb,r/rrwxr-xr-x,0,0,4945,"/bin/bcab"

# 4. Extraer el inodo 4945 con icat
icat partition4.img 4945
# NzFtMzExbjNfMHU3MTEzcl9oM3JfNDNhMmU3YWYK

# 5. Decodificar Base64
echo "NzFtMzExbjNfMHU3MTEzcl9oM3JfNDNhMmU3YWYK" | base64 -d
# 71m311n3_0u7113r_h3r_43a2e7af
```

## Notas adicionales
- El *timestomping* es una técnica antiforense utilizada por adversarios para camuflar binarios maliciosos o herramientas de ataque asignándoles marcas temporales antiguas o idénticas a las de archivos legítimos del sistema. Sin embargo, inconsistencias entre timestamps de metadatos (como divergencias entre `$STANDARD_INFORMATION` y `$FILE_NAME` en NTFS, o fechas anteriores a la creación del propio sistema operativo) a menudo exponen el artefacto.

## Referencias
- Reto: https://learn.cylabacademy.org/library/720
- The Sleuth Kit (TSK): https://www.sleuthkit.org/sleuthkit/
- SANS SIFT Workstation & Timeline Analysis: https://www.sans.org/tools/sift-workstation/
