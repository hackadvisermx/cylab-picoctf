# General Skills — PW Crack 1

## Descripción
> **Prompt oficial:** "Can you crack the password to get the flag? Download the password checker here and you'll need the encrypted flag in the same directory too."
>
> **Hints:**
> 1. To view the file in the webshell, do: `$ nano level1.py`
> 2. To exit nano, press Ctrl and x and follow the on-screen prompts.
> 3. The `str_xor` function does not need to be reverse engineered for this challenge.

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
Versión aún más directa que `PW Crack 2`: la contraseña está en texto plano en el propio código fuente.

```python
if( user_pw == "1e1a"):
```

```bash
echo "1e1a" | python3 level1.py
# Welcome back... your flag, user:
# picoCTF{...}
```

Flag: `picoCTF{545h_r1ng1ng_fa343060}`

## Notas adicionales
- Primero de la serie "PW Crack" (1 y 2 comparten estructura: función XOR de relleno + comprobación de contraseña); en el nivel 1 la contraseña está en claro, en el nivel 2 está ofuscada como códigos ASCII hexadecimales (`chr(0x64)+...`).

## Referencias
- Reto: https://learn.cylabacademy.org/library/245
- Fuente: `level1.py` (copia en esta carpeta)
