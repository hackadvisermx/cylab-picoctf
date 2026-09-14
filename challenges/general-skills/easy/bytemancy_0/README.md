# General Skills — bytemancy 0

## Descripción
> **Prompt oficial:** "Can you conjure the right bytes? The program's source code can be downloaded here. Connect to the program with netcat: `nc <host> <puerto>`"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

## Solución
Versión más sencilla de `bytemancy 1`. El código (`app.py`, adjunto) solo pide:

```python
if user_input == "\x65\x65\x65":
  print(open("./flag.txt", "r").read())
```

`\x65` = `'e'`, así que basta con enviar `eee`.

```bash
printf 'eee\n' | nc -w 5 <host> <puerto>
```

Flag: `picoCTF{pr1n74813_ch4r5_334c472c}`

## Notas adicionales
- Es el "hermano fácil" de `bytemancy 1` (que pide 1751 repeticiones de `'e'` en vez de 3) — misma idea, menor escala.

## Referencias
- Reto: https://learn.cylabacademy.org/library/742
- Fuente: `app.py` (copia en esta carpeta)
