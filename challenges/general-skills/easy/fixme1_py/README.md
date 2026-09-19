# General Skills — fixme1.py

## Descripción
> **Prompt oficial:** "Fix the syntax error in this Python script to print the flag."
>
> **Hints:**
> 1. Indentation is very meaningful in Python
> 2. To view the file in the webshell, do: `$ nano fixme1.py`
> 3. To exit nano, press Ctrl and x and follow the on-screen prompts.
> 4. The `str_xor` function does not need to be reverse engineered for this challenge.

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
Error de **indentación**: la línea `print(...)` tiene dos espacios de más al principio, sin que haya ningún bloque (`if`/`for`/`def`) que lo justifique.

```python
# antes
flag = str_xor(flag_enc, 'enkidu')
  print('That is correct! Here\'s your flag: ' + flag)

# después
flag = str_xor(flag_enc, 'enkidu')
print('That is correct! Here\'s your flag: ' + flag)
```

```bash
python3 fixme1_fixed.py
# That is correct! Here's your flag: picoCTF{...}
```

Flag: `picoCTF{1nd3nt1ty_cr1515_09ee727a}`

## Notas adicionales
- Primero de la pareja `fixme1.py`/`fixme2.py` (mismo autor, mismo XOR de relleno con clave `'enkidu'`); aquí el error es de indentación, en `fixme2.py` es `=` en vez de `==`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/240
- Fuente corregida: `fixme1_fixed.py` (copia en esta carpeta)
