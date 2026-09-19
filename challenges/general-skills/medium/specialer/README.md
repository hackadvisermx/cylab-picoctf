# General Skills — Specialer

## Descripción
> **Prompt oficial del reto:** "Reception of Special has been cool to say the least. That's why we made an exclusive version of Special, called Secure Comprehensive Interface for Affecting Linux Empirically Rad, or just 'Specialer'. With Specialer, we really tried to remove the distractions from using a shell. Yes, we took out spell checker because of everybody's complaining. But we think you will be excited about our new, reduced feature set for keeping you focused on what needs it the most."
>
> **Hints:**
> 1. What programs do you have access to?

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones, et al.

## Solución
Al conectar por SSH se obtiene un prompt `Specialer$` que es **bash real**, pero con `$PATH` apuntando a directorios vacíos: no hay ningún binario externo disponible (`ls`, `whoami`, `cat`, `wc`, `file`... todos dan `command not found` o `No such file or directory`, incluso invocándolos por ruta absoluta como `/bin/ls`).

Sin embargo, siguen disponibles todos los **builtins de bash** (confirmado con `help`), que alcanzan para explorar el sistema de archivos y leer contenido sin depender de ningún binario:

1. Listar el directorio home usando expansión de glob con `echo` (builtin):
   ```bash
   echo *
   # abra ala sim
   ```
   Tres subdirectorios con nombres temáticos de trucos de magia (abra[cadabra], ala[kazam], sim[salabim]).

2. Bajar un nivel para ver los archivos dentro de cada uno:
   ```bash
   echo */*
   # abra/cadabra.txt abra/cadaniel.txt ala/kazam.txt ala/mode.txt sim/city.txt sim/salabim.txt
   ```
   Cada carpeta tiene un archivo "correcto" (la palabra mágica real: `cadabra`, `kazam`, `salabim`) y uno señuelo (`cadaniel`, `mode`, `city`).

3. Leer cada archivo sin `cat`, usando el builtin `mapfile` (carga el archivo en un array de bash):
   ```bash
   mapfile -t L < abra/cadabra.txt; echo "${L[@]}"
   mapfile -t L < ala/kazam.txt;    echo "${L[@]}"
   mapfile -t L < sim/salabim.txt;  echo "${L[@]}"
   ```
   `ala/kazam.txt` (la palabra mágica correcta de esa carpeta) contiene la flag:
   ```
   return 0 picoCTF{y0u_d0n7_4ppr3c1473_wh47_w3r3_d01ng_h3r3_d5ef8b71}
   ```
   Los demás archivos son solo mensajes decorativos ("Nothing up my sleeve!", "Yummy! Ice cream!", un UUID señuelo, una línea de canción).

## Notas adicionales
- Es la contraparte de "Special" (reto hermano en la misma tanda), pero más restringida: aquí no queda ningún binario externo utilizable, forzando a resolver el reto exclusivamente con comandos internos (`echo`, `mapfile`/`read`, expansión de glob, redirecciones) — sin `cat`, sin `ls`, sin `grep`.
- Automatizado con `paramiko` (sesión SSH interactiva) desde la terminal local en vez del webshell embebido.

## Referencias
- Reto: https://learn.cylabacademy.org/library/378
