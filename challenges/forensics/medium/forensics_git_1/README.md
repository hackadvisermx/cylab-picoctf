# Forensics — Forensics Git 1

## Descripción
> **Prompt oficial del reto:** "Can you find the flag in this disk image?  
> Download the disk image here."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

> **Pistas oficiales:**
> 1. How can you checkout the files of a previous commit?

## Solución
El reto proporciona una imagen de disco con esquema MBR que contiene una partición ext4 con un repositorio Git en `/home/ctf-player/Code/secrets/`.

1. **Extracción de la partición ext4:**
   ```bash
   7zz x disk.img 2.img -o./
   7zz x 2.img "home/ctf-player/Code/secrets/*" -o./extracted/
   cd extracted/home/ctf-player/Code/secrets
   ```

2. **Análisis del historial de commits:**
   Al inspeccionar el árbol de trabajo actual, los archivos no contienen la bandera directamente. Sin embargo, al inspeccionar el registro de commits (`git log` con `-p` para ver diffs):
   ```bash
   git log -p
   ```
   Se aprecian dos commits:
   - `Add flag`: Añadió un archivo `flag.txt` conteniendo la bandera de la academia.
   - `Remove flag`: Eliminó el archivo `flag.txt`.

3. **Recuperación del archivo eliminado:**
   Podemos visualizar la bandera examinando el diff del commit anterior o haciendo checkout del commit previo:
   ```bash
   git show HEAD~1:flag.txt
   ```
   Esto imprime el contenido original del archivo antes de su eliminación.

## Notas adicionales
- En Git, la eliminación de un archivo mediante un commit ordinario no borra el contenido de la base de datos de objetos (`.git/objects`); el blob y el árbol siguen existiendo en el historial accesible mediante referencias y reflog.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/706
- Git checkout: https://git-scm.com/docs/git-checkout
