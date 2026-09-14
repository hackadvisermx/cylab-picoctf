# General Skills — Commitment Issues

## Descripción
> **Prompt oficial:** "I accidentally wrote the flag down. Good thing I deleted it!"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Jeffery John

## Solución
De nuevo un repo Git en el zip descargable. `git log` muestra dos commits: uno que crea `message.txt` con la flag, y otro posterior que la "borra" (sobrescribiéndola con "TOP SECRET"). Como es un commit normal (no un `reset`/`rebase` que dejara el blob huérfano), el contenido original sigue perfectamente accesible en el historial:

```bash
cd drop-in
git log --all --oneline
# 42942c9 remove sensitive info
# b562f0b create flag

git show b562f0b
# +picoCTF{s@n1t1z3_c785c319}
```

Flag: `picoCTF{s@n1t1z3_c785c319}`

## Notas adicionales
- A diferencia de otros retos de "borrado" en Git, aquí no hace falta `git reflog` ni `git fsck --lost-found` (no hay commits huérfanos/colgantes) — el commit con la flag sigue siendo un ancestro normal de `HEAD`, así que `git log`/`git show` bastan.
- Lección general: **"eliminar" un archivo con un nuevo commit no borra su contenido del historial de Git** — solo `git filter-repo`/`BFG` (reescribiendo el historial) o borrar el propio repositorio lo harían.

## Referencias
- Reto: https://learn.cylabacademy.org/library/411
