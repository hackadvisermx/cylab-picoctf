# Forensics — Forensics Git 2

## Descripción
> **Prompt oficial del reto:** "The agents interrupted the perpetrator's disk deletion routine. Can you recover this git repo?  
> Download the disk image here."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

> **Pistas oficiales:**
> 1. We think the deletion was interrupted before any git objects were touched

## Solución
El reto presenta una imagen de disco donde el usuario intentó destruir un repositorio Git antes de ser interrumpido.

1. **Inspección del disco y extracción:**
   Extraemos la tercera partición (`ext4`) de `disk.img`:
   ```bash
   7zz x disk.img 2.img -o./
   7zz l 2.img | grep "home/ctf-player"
   ```
   En esta ocasión, la carpeta no se llama `secrets`, sino `/home/ctf-player/Code/killer-chat-app`.
   La carpeta de trabajo contiene archivos y la carpeta `.git`, pero las referencias (`refs/heads/master`) fueron alteradas o borradas.

2. **Extracción y examen del repositorio:**
   ```bash
   7zz x 2.img "home/ctf-player/Code/killer-chat-app/*" -o./extracted/
   cd extracted/home/ctf-player/Code/killer-chat-app
   ```
   Al ejecutar `git log` se recibe el error:
   `fatal: your current branch 'master' does not have any commits yet`

3. **Recuperación vía Reflog / Object Database:**
   Como señala la pista oficial, los objetos de Git y los registros de log no fueron destruidos. Inspeccionamos el archivo `.git/logs/HEAD`:
   ```bash
   cat .git/logs/HEAD
   ```
   Se observan múltiples commits registrados:
   - `commit (initial): Add netcat scripts` (`2c0a9b...`)
   - `commit: Add video game chat log` (`26b809...`)
   - `commit: Add TV show chat log` (`582763...`)
   - `commit: Add secret hideout chat log` (`e817cd5367847bbfcc98b724bbe9d3e25cb22264`)
   - `commit: Remove secret hideout log` (`407c5f...`)

4. **Visualización del commit del escondite secreto:**
   Examinando el commit `e817cd5367847bbfcc98b724bbe9d3e25cb22264`:
   ```bash
   git show e817cd5367847bbfcc98b724bbe9d3e25cb22264
   ```
   El commit añade el archivo `logs/3.txt`:
   ```text
   Rex: Meet at the old arcade basement for the secret hideout.
   Jay: Ask Rusty at the door and use password academy{...}.
   Rex: Bring the decoder map so we can plan the route.
   ```
   La contraseña revelada corresponde a la bandera.

## Notas adicionales
- Incluso cuando el puntero de una rama es borrado o reseteado, los objetos huérfanos pueden ser localizados a través de los reflogs (`.git/logs/`) o mediante utilidades como `git fsck --lost-found`.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/707
- Git Internals - Maintenance and Data Recovery: https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery
