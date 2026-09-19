# General Skills — PW Crack 4

## Descripción
> **Prompt oficial del reto:** "Can you crack the password to get the flag? [...] There are 100 potential passwords with only 1 being correct. You can find these by examining the password checker script." — se entregan `level4.py`, `level4.flag.txt.enc` y `level4.hash.bin`, sin instancia remota ni diccionario externo.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
Misma estructura que `PW Crack 5` (MD5 de la contraseña comparado contra un hash, luego la contraseña se usa como clave XOR para descifrar la flag), pero aquí el "diccionario" no es un archivo aparte: los **100 candidatos están hardcodeados al final del propio script** en la lista `pos_pw_list`. Basta con probarlos todos localmente:

```python
import hashlib
target = open('level4.hash.bin', 'rb').read()
pos_pw_list = ["8c86", "7692", ..., "a7e2"]   # copiados tal cual del script

for pw in pos_pw_list:
    if hashlib.md5(pw.encode()).digest() == target:
        print("FOUND:", pw)   # -> "9f63"
        break
```

Con la contraseña (`9f63`) se descifra la flag con la misma función `str_xor` (XOR de clave repetida) del script:

```python
def str_xor(secret, key):
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key = new_key + key[i]
        i = (i + 1) % len(key)
    return "".join([chr(ord(a) ^ ord(b)) for (a, b) in zip(secret, new_key)])

flag_enc = open("level4.flag.txt.enc", "rb").read().decode()
print(str_xor(flag_enc, "9f63"))
# picoCTF{fl45h_5pr1ng1ng_d770d48c}
```

## Notas adicionales
- Diferencia clave con `PW Crack 5`: ahí el espacio de búsqueda era un diccionario externo de 65,536 palabras; aquí son solo **100 candidatos explícitos dentro del propio código fuente** — el enunciado literalmente indica dónde buscarlos ("examining the password checker script"), reforzando la idea de leer el archivo completo antes de intentar nada más sofisticado.
- Mismo mecanismo de descifrado (`str_xor`, XOR de clave repetida) reutilizado en toda la serie "PW Crack"/"Serpentine" de este autor — una vez identificado el patrón en un reto, se aplica igual en el resto.

## Referencias
- Reto: https://learn.cylabacademy.org/library/248
