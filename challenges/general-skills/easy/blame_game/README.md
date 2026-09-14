# General Skills — Blame Game

## Descripción
> **Prompt oficial:** "Someone's commits seems to be preventing the program from working. Who is it?"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Jeffery John

## Solución
El repo tiene **cientos** de commits triviales ("important business work") que solo sirven para enterrar el commit real entre ruido. En vez de recorrer el log entero, `git blame` va directo al grano: muestra, línea por línea del archivo, quién (y en qué commit) escribió esa línea por última vez.

```bash
cd drop-in
git blame message.py
# 23e9d4ce (picoCTF{@sk_th3_1nt3rn_81e716ff} 2024-03-12 ...) 1) print("Hello, World!"
```

La flag está en el campo **autor** del commit que rompió el archivo (`message.py` quedó con una línea `print("Hello, World!"` sin cerrar el paréntesis, de ahí que "el programa no funcione").

Flag: `picoCTF{@sk_th3_1nt3rn_81e716ff}`

## Notas adicionales
- Es justo el caso de uso para el que existe `git blame`: encontrar rápidamente quién introdujo un cambio concreto en una línea, sin tener que revisar manualmente un historial larguísimo con `git log`.
- El nombre de autor de Git es un campo de texto libre controlado por quien hace el commit (`git config user.name`) — aquí se usa como "contenedor" de la flag, similar en espíritu al reto `MY GIT` (donde el autor se usaba como mecanismo de "autenticación").

## Referencias
- Reto: https://learn.cylabacademy.org/library/405
