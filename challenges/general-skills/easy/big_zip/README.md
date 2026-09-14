# General Skills — Big Zip

## Descripción
> **Prompt oficial:** "Unzip this archive and find the flag."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** (General Skills, sin evento especificado)
- **Autor:** LT 'syreal' Jones

## Solución
El zip contiene miles de carpetas y archivos `.txt` con nombres aleatorios sin sentido (8732 archivos en total) — la fuerza bruta manual es inviable. En vez de abrir archivo por archivo, `grep -r` recursivo encuentra el que contiene la flag en segundos.

```bash
unzip big-zip-files.zip -d extracted
grep -rl "picoCTF{" extracted
# extracted/big-zip-files/folder_.../folder_.../whzxrpivpqld.txt
cat extracted/big-zip-files/.../whzxrpivpqld.txt
```

Flag: `picoCTF{gr3p_15_m4g1c_ef8790dc}`

## Notas adicionales
- La propia flag ("gr3p is m4g1c") confirma que la solución esperada es exactamente `grep -r` — la lección del reto es no perder tiempo navegando manualmente un árbol de directorios enorme.

## Referencias
- Reto: https://learn.cylabacademy.org/library/322
