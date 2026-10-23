# Forensics — Timeline 1

## Descripción
> **Prompt oficial del reto:** "Can you find the flag in this disk image? Wrap what you find in the academy{} flag format.
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/0b369ed5974a5e777ca3bc323bd39d75a6f27762a449d16cd2a0ffc08b2a6aa8/timeline-1-partition4.img.gz)."
>
> **Hints:**
> 1. Create a Sleuthkit MAC timeline!
> 2. Look at recent timestamps
> 3. Pay close attention to timestamps near an anti-forensic action
> 4. Filter only new files by grepping for `macb`

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

## Solución
A diferencia de `Timeline 0` (donde la flag residía en un archivo con una fecha del pasado remoto), este reto requiere examinar los eventos más recientes del sistema de archivos, prestando atención a acciones de antiforense y archivos recién creados marcados con el estado `macb` (Modificado, Accedido, Cambiado inodo, Creado).

1. **Generación de línea de tiempo con TSK:**
   - Se descomprime `timeline-1-partition4.img.gz`.
   - Se procesa la imagen `timeline1.img` con `fls -r -m /` y `mactime -b body.txt -d > mactime.csv`.

2. **Análisis de la ventana temporal reciente:**
   - Al inspeccionar el final del archivo cronológico (alrededor de `Mon Dec 01 2025 21:50:23`), se detecta un apagado del sistema registrado en `/root/.ash_history` (`poweroff`, inodo `4943`).
   - Justo 16 segundos antes de la orden de apagado (a las `21:50:07`), se creó un archivo inusual en `/etc/chat` (inodo `32716`, tamaño 49 bytes) con marcas completas `macb`.

3. **Extracción y decodificación de la flag:**
   - Empleando `icat` sobre el inodo `32716`, se extrae el contenido:
     `NTczNDE3aDEzcl83aDRuXzdoM18xNDU3XzU4NTI3YmIyMjIK`
   - Decodificando la cadena Base64 se obtiene:
     `573417h13r_7h4n_7h3_1457_58527bb222`
   - Envolviéndola en el formato `academy{...}` se completa la flag.

```bash
# 1. Descomprimir imagen
gzip -d timeline-1-partition4.img.gz

# 2. Generar línea de tiempo
fls -r -m / timeline1.img > body.txt
mactime -b body.txt -d > mactime.csv

# 3. Filtrar archivos creados recientemente (macb)
grep "macb" mactime.csv | tail -n 10
# Mon Dec 01 2025 21:50:07,49,macb,r/rrw-r--r--,0,0,32716,"/etc/chat"
# Mon Dec 01 2025 21:50:23,9,macb,r/rrw-------,0,0,4943,"/root/.ash_history"

# 4. Extraer el contenido del archivo /etc/chat (inodo 32716)
icat timeline1.img 32716
# NTczNDE3aDEzcl83aDRuXzdoM18xNDU3XzU4NTI3YmIyMjIK

# 5. Decodificar Base64
echo "NTczNDE3aDEzcl83aDRuXzdoM18xNDU3XzU4NTI3YmIyMjIK" | base64 -d
# 573417h13r_7h4n_7h3_1457_58527bb222
```

## Notas adicionales
- En respuesta a incidentes, la correlación temporal entre eventos de administración (comandos en historiales como `.bash_history` o `.ash_history`), artefactos creados temporalmente y el apagado forzado del equipo permite reconstruir la ventana exacta de actividad del intruso.

## Referencias
- Reto: https://learn.cylabacademy.org/library/721
- The Sleuth Kit Timeline Guide: https://wiki.sleuthkit.org/index.php?title=Timeline
