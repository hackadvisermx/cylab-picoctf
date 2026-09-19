# General Skills — PW Crack 3

## Descripción
> **Prompt oficial del reto:** "Can you crack the password to get the flag? Download the password checker here and you'll need the encrypted flag and the hash in the same directory too. There are 7 potential passwords with 1 being correct. You can find these by examining the password checker script." — se entregan `level3.py`, `level3.flag.txt.enc` y `level3.hash.bin`, sin instancia remota ni diccionario externo.
>
> **Hints:**
> 1. To view the level3.hash.bin file in the webshell, do: `$ bvi level3.hash.bin`
> 2. To exit bvi type `:q` and press enter.
> 3. The `str_xor` function does not need to be reverse engineered for this challenge.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
Misma estructura que el resto de la serie "PW Crack" (MD5 de la contraseña comparado contra un hash, luego la contraseña se usa como clave XOR para descifrar la flag). Aquí los **7 candidatos están hardcodeados al final del propio script** en la lista `pos_pw_list`, así que basta con probarlos todos localmente sin necesidad de fuerza bruta ni diccionario externo:

```python
import hashlib
target = open('level3.hash.bin', 'rb').read()
pos_pw_list = ["f09e", "4dcf", "87ab", "dba8", "752e", "3961", "f159"]

for pw in pos_pw_list:
    if hashlib.md5(pw.encode()).digest() == target:
        print("FOUND:", pw)   # -> "87ab"
        break
```

Con la contraseña (`87ab`) se descifra la flag con la misma función `str_xor` (XOR de clave repetida) del script:

```python
def str_xor(secret, key):
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key = new_key + key[i]
        i = (i + 1) % len(key)
    return "".join([chr(ord(a) ^ ord(b)) for (a, b) in zip(secret, new_key)])

flag_enc = open("level3.flag.txt.enc", "rb").read().decode()
print(str_xor(flag_enc, "87ab"))
# picoCTF{m45h_fl1ng1ng_cd6ed2eb}
```

## Notas adicionales
- El reto no requiere lanzar ninguna instancia: los 3 archivos (`level3.py`, `.hash.bin`, `.flag.txt.enc`) se descargan directamente desde los enlaces del modal y se resuelven 100% en local.
- Mismo mecanismo de descifrado (`str_xor`, XOR de clave repetida) y mismo patrón de "candidatos hardcodeados en el propio script" que `PW Crack 4` — solo cambia el tamaño del espacio de búsqueda (7 aquí, 100 en el 4, un diccionario externo de 65,536 palabras en el 5).

## Referencias
- Reto: https://learn.cylabacademy.org/library/247
