# Forensics — Forensics Git 0

## Descripción
> **Prompt oficial del reto:** "Can you find the flag in this disk image?  
> Download the disk image here."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

> **Pistas oficiales:**
> 1. How can you extract the directory from the disk image?

## Solución
El reto provee una imagen comprimida de disco (`disk.img.gz`). Al descomprimirla, se obtiene una imagen de disco particionada con esquema MBR.

1. **Inspección de las particiones del disco:**
   Utilizando `7zz` o herramientas del Sleuth Kit (`mmls`), listamos las particiones existentes:
   ```bash
   7zz l disk.img
   ```
   Se identifican 3 particiones:
   - Partición 1 (300 MB): Boot / Sistema base
   - Partición 2 (256 MB): Linux Swap
   - Partición 3 / `2.img` (467 MB): Sistema de archivos Linux principal (`ext4`)

2. **Extracción del sistema de archivos ext4:**
   Extraemos la tercera partición y examinamos los directorios de usuario:
   ```bash
   7zz x disk.img 2.img -o./
   7zz l 2.img | grep "home/ctf-player"
   ```
   Se detecta un repositorio git en `/home/ctf-player/Code/secrets/`.

3. **Recuperación del repositorio Git y lectura del historial:**
   Extraemos la carpeta del repositorio:
   ```bash
   7zz x 2.img "home/ctf-player/Code/secrets/*" -o./extracted/
   cd extracted/home/ctf-player/Code/secrets
   ```
   Al revisar el historial de commits mediante `git log`:
   ```bash
   git log -p
   ```
   El mensaje del commit inicial indica:
   `Wrap this phrase in the flag format: g17_1n_7h3_d15k_041217d8`

   Envolviendo la frase en el formato estándar `academy{...}` se obtiene la bandera requerida.

```bash
# Ejemplo de inspección directa:
git -C extracted/home/ctf-player/Code/secrets log -1 --pretty=format:"%B"
```

## Notas adicionales
- Las particiones ext4 pueden ser navegadas y extraídas directamente mediante utilidades de archivo como `7zz` sin necesidad de montar imágenes a nivel de kernel ni privilegios root.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/705
- Git Documentation (git-log): https://git-scm.com/docs/git-log
