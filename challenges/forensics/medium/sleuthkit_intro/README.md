# Forensics — Sleuthkit Intro

## Descripción
> **Prompt oficial del reto:** "Download the disk image and use `mmls` on it to find the size of the Linux partition. Connect to the remote checker service to check your answer and get the flag.  
>  
> Note: if you are using the webshell, download and extract the disk image into `/tmp` not your home directory.  
> Download disk image"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona una imagen de disco comprimida (`disk.img.gz`). El objetivo es determinar la longitud en sectores de la partición Linux y enviarla al servicio de verificación en red.

1. **Descompresión y análisis con mmls:**
   ```bash
   gzip -dc disk.img.gz > disk.img
   mmls disk.img
   ```
   O inspeccionando las particiones con `7zz` / `fdisk`:
   ```bash
   7zz l disk.img
   ```
   La tabla de particiones DOS muestra la partición de tipo Linux (`0x83`):
   ```text
   Slot      Start        End          Length       Description
   002:      0000002048   0000204799   0000202752   Linux (0x83)
   ```
   El tamaño de la partición Linux es de **202752** sectores.

2. **Verificación remota:**
   Nos conectamos mediante `nc` al puerto asignado por la instancia:
   ```bash
   nc <host> <port>
   ```
   Al solicitar *"What is the size of the Linux partition in the given disk image?"*, ingresamos `202752`. El servicio confirma la respuesta y devuelve la bandera.

## Notas adicionales
- `mmls` (Media Management List) de The Sleuth Kit permite inspeccionar tablas de particiones MBR, GPT y BSD disklabel sin necesidad de privilegios administrativos.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/301
- Sleuthkit mmls: https://wiki.sleuthkit.org/index.php?title=Mmls
