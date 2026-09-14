# General Skills — PW Crack 2

## Descripción
> **Prompt oficial:** "Can you crack the password to get the flag? Download the password checker here and you'll need the encrypted flag in the same directory too."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
El script (`level2.py`, adjunto) compara la contraseña introducida contra una construida con códigos de carácter ASCII explícitos en el propio código, a pesar del comentario "THIS FUNCTION WILL NOT HELP YOU FIND THE FLAG" (que se refiere solo a la función XOR, no a la contraseña):

```python
if user_pw == chr(0x64) + chr(0x65) + chr(0x37) + chr(0x36):
```

`chr(0x64)+chr(0x65)+chr(0x37)+chr(0x36)` = `"de76"`.

```bash
echo "de76" | python3 level2.py
# Welcome back... your flag, user:
# picoCTF{...}
```

Flag: `picoCTF{tr45h_51ng1ng_489dea9a}`

## Notas adicionales
- Basta con leer el código fuente para "adivinar" la contraseña sin necesidad de ningún ataque de fuerza bruta real — el propio script contiene la respuesta en claro, solo ligeramente ofuscada como valores hexadecimales de caracteres ASCII.
- El comentario "THIS FUNCTION WILL NOT HELP YOU FIND THE FLAG" es una pista/broma para no perder tiempo intentando invertir la función `str_xor` — la contraseña ya está fija en el código.

## Referencias
- Reto: https://learn.cylabacademy.org/library/246
- Fuente: `level2.py` (copia en esta carpeta)
