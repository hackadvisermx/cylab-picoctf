# General Skills — PW Crack 5

## Descripción
> **Prompt oficial del reto:** "Can you crack the password to get the flag? Download the password checker here and you'll need the encrypted flag and the hash in the same directory too. Here's a dictionary with all possible passwords based on the password conventions we've seen so far." — se entregan `level5.py`, `level5.flag.txt.enc`, `level5.hash.bin` y `dictionary.txt` (65,536 candidatos), sin instancia remota.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
`level5.py` compara el **MD5** de la contraseña ingresada contra un hash de referencia (`level5.hash.bin`); si coincide, usa la propia contraseña como clave para descifrar `level5.flag.txt.enc` con XOR de clave repetida (`str_xor`, la misma función usada en `Serpentine` de este mismo bloque).

En vez de ejecutar el programa interactivo, se automatiza el ataque de diccionario localmente:

```python
import hashlib
target = open('level5.hash.bin','rb').read()
with open('dictionary.txt', encoding='latin-1') as f:
    for line in f:
        pw = line.rstrip('\n')
        if hashlib.md5(pw.encode()).digest() == target:
            print('FOUND:', pw)   # -> '9581'
            break
```

Con la contraseña encontrada (`9581`), se reutiliza `str_xor` para descifrar la flag:

```python
def str_xor(secret, key):
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key = new_key + key[i]
        i = (i + 1) % len(key)
    return ''.join([chr(ord(a) ^ ord(b)) for (a, b) in zip(secret, new_key)])

flag_enc = open('level5.flag.txt.enc', 'rb').read().decode()
print(str_xor(flag_enc, '9581'))
# picoCTF{h45h_sl1ng1ng_36e992a6}
```

## Notas adicionales
- Diccionario de solo 65,536 candidatos (`2^16`) — sugiere contraseñas numéricas de 4-5 dígitos u otro espacio acotado; un ataque de diccionario/fuerza bruta local sobre MD5 (rápido de calcular) resuelve el reto en milisegundos, sin necesidad de herramientas externas como `hashcat`/`john`.
- Continúa el patrón de la serie "PW Crack": los niveles anteriores (1 y 2, ya documentados como Easy) probablemente usan hashes más simples/sin cifrado adicional; este nivel 5 añade la capa extra de usar la propia contraseña como clave de descifrado XOR de la flag.
- Mismo mecanismo de cifrado (`str_xor`) que en el reto `Serpentine` de este bloque — patrón recurrente del autor 'LT syreal Jones' en varios retos "PW Crack"/"Serpentine".

## Referencias
- Reto: https://learn.cylabacademy.org/library/249
