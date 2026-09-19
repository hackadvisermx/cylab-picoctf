# General Skills — fixme2.py

## Descripción
> **Prompt oficial:** "Fix the syntax error in the Python script to print the flag."
>
> **Hints:**
> 1. Are equality and assignment the same symbol?
> 2. To view the file in the webshell, do: `$ nano fixme2.py`
> 3. To exit nano, press Ctrl and x and follow the on-screen prompts.
> 4. The `str_xor` function does not need to be reverse engineered for this challenge.

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
Error clásico de sintaxis: usar `=` (asignación) en vez de `==` (comparación) dentro de un `if`.

```python
# antes
if flag = "":

# después
if flag == "":
```

```bash
python3 fixme2_fixed.py
# That is correct! Here's your flag: picoCTF{...}
```

Flag: `picoCTF{3qu4l1ty_n0t_4551gnm3nt_e8814d03}`

## Notas adicionales
- El propio Python 3 moderno ya sugiere la corrección en el mensaje de error (`SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?`).
- El resto del script (relleno de clave y XOR sobre un array de `chr(0x..)`) es idéntico en estructura a `PW Crack 1/2`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/241
- Fuente corregida: `fixme2_fixed.py` (copia en esta carpeta)
