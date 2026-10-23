# Forensics — Dear Diary

## Descripción
> **Prompt oficial del reto:** "If you can find the flag on this disk image, we can close the case for good!
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/a25bb84ce58309d7ba5cfe01dd4d6d2ce05e5d4cfd5307216cec07d1eab3267c/disk.flag.img.gz)."
>
> **Hints:**
> 1. If you're observing binary data raw in the terminal you may be misled about the contents of a block.

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** syreal

## Solución
El reto proporciona una imagen de disco comprimida `disk.flag.img.gz` de aproximadamente 1 GB al descomprimirse.

1. **Inspección de la estructura de particiones:**
   - Al descomprimir con `gunzip` o `gzip -d`, se obtiene `disk.flag.img`.
   - Inspeccionando la tabla de particiones MBR (con `fdisk -l` o `mmls`), se observan 3 particiones:
     - Partición 1 (Linux ext4, 300 MiB)
     - Partición 2 (Linux swap, 256 MiB)
     - Partición 3 (Linux ext4, 467 MiB, sector inicial 1140736)

2. **Exploración del sistema de archivos y espacio residual (Slack / Journal):**
   - En la partición 3, el directorio `/root/secret-secrets/` contiene archivos aparentemente vacíos como `innocuous-file.txt` y `its-all-in-the-name`.
   - La pista ("If you're observing binary data raw in the terminal you may be misled about the contents of a block") advierte sobre la naturaleza de la información: no es un archivo de texto regular, sino fragmentos distribuidos en los bloques de directorio o en el journal del sistema de archivos (`ext4 journal`, Inode 8).
   - En el journal y en el espacio no asignado (slack space) de los bloques de directorio, se registraron creaciones y borrados sucesivos de archivos cuyos nombres contenían fragmentos de 3 caracteres de la flag:
     `pic` + `oCT` + `F{1` + `_53` + `3_n` + `4m3` + ...
   - Extrayendo el journal mediante The Sleuth Kit (`icat`) o analizando directamente los bloques no asignados mediante `blkls` / Python, es posible reconstruir la secuencia completa y obtener la flag.

```bash
# 1. Descomprimir la imagen de disco
gunzip -k disk.flag.img.gz

# 2. Examinar las particiones
file disk.flag.img

# 3. Analizar el journal de ext4 (inodo 8) en la partición 3 (offset sector 1140736)
# Usando The Sleuth Kit (TSK):
icat -o 1140736 disk.flag.img 8 | strings | grep -E ".{1,4}\.txt" -B 1 -A 1

# O extrayendo los fragmentos en orden con un script de inspección de bloques
python3 -c "
import re
with open('disk.flag.img', 'rb') as f:
    data = f.read()
# Localizar bloques asociados al directorio secret-secrets y journal
# y reconstruir las entradas consecutivas creadas en el sistema de archivos
"
```

## Notas adicionales
- En sistemas de archivos con registro transaccional como `ext4`, los metadatos de archivos temporales o borrados recientemente persisten en el journal transaccional (`jbd2`) mucho después de que los archivos han sido eliminados del árbol de directorios activo.
- El análisis de journal y de espacio de holgura (slack space) es una técnica estándar en informática forense para reconstruir la cronología de acciones del usuario o atacante.

## Referencias
- Reto: https://learn.cylabacademy.org/library/413
- The Sleuth Kit Documentation: https://wiki.sleuthkit.org/index.php?title=TSK_Tool_Overview
