# Forensics — Disk, disk, sleuth!

## Descripción
> **Prompt oficial del reto:** "Use `srch_strings` from the sleuthkit and some terminal-fu to find a flag in this disk image.
> [dds1-alpine.flag.img.gz](https://challenge-files.cylabacademy.net/library/0e33413e7b309ae38964211ca09f5c86005b6fe4f2cc95b75ad5b482d98a2d76/dds1-alpine.flag.img.gz)"
>
> **Hints:**
> - "Have you ever used `file` to determine what a file was?"
> - "Relevant terminal-fu in Challenge Library: https://learn.cylabacademy.org/library/85"
> - "Mastering this terminal-fu would enable you to find the flag in a single command: https://learn.cylabacademy.org/library/48"
> - "Using your own computer, you could use qemu to boot from this disk!"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
El reto proporciona una imagen de disco comprimida de una máquina Alpine Linux (`dds1-alpine.flag.img.gz`). La descripción sugiere utilizar la utilidad `srch_strings` de The Sleuth Kit (o herramientas equivalentes de extracción de cadenas) junto con comandos estándar del shell.

### Paso 1: Descompresión de la imagen
Descomprimimos el archivo `.gz` para obtener la imagen de disco sin comprimir:

```bash
gzip -d dds1-alpine.flag.img.gz
```

### Paso 2: Búsqueda de cadenas en la imagen
Utilizamos `srch_strings` o la utilidad del sistema `strings` para extraer secuencias de caracteres imprimibles de la imagen de disco, filtrando por el patrón de flag de la plataforma (`academy{` o `picoCTF{`):

```bash
srch_strings dds1-alpine.flag.img | grep "academy{"
# O con strings estándar:
strings dds1-alpine.flag.img | grep "academy{"
```

El comando localiza de inmediato la cadena correspondiente a la flag dentro de los bloques del sistema de archivos.

## Notas adicionales
- `srch_strings` es parte del paquete The Sleuth Kit (TSK) y permite extraer cadenas tanto en ASCII como en Unicode desde imágenes de disco completas, independientemente del formato de la partición (ext4, FAT, NTFS).
- En análisis forense digital de imágenes de almacenamiento, la búsqueda de cadenas indexadas o expresiones regulares (*string searching*) es la primera técnica de triage para identificar credenciales, llaves y artefactos conocidos antes de realizar el análisis a bajo nivel de inodos o tablas de asignación de archivos.

## Referencias
- The Sleuth Kit Documentation: http://wiki.sleuthkit.org/index.php?title=TSK_Tool_Overview
