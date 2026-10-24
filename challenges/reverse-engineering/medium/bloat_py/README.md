# Reverse Engineering — bloat.py

## Descripción
> **Prompt oficial del reto:** "Can you get the flag?
> Run this [Python program](https://challenge-files.cylabacademy.net/library/29555ba70e983dd8216407779bca6085b7eeab85c0c2a3a16d6b1c757a9eaa9c/bloat.flag.py) in the same directory as this [encrypted flag](https://challenge-files.cylabacademy.net/library/29555ba70e983dd8216407779bca6085b7eeab85c0c2a3a16d6b1c757a9eaa9c/flag.txt.enc)."
>
> **Pistas oficiales:** Ninguna

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona un script ofuscado en Python (`bloat.flag.py`) y un archivo cifrado (`flag.txt.enc`).

Al inspeccionar el código del script:
1. Define un alfabeto de caracteres ASCII imprimibles:
   ```python
   a = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "
   ```
2. Todas las cadenas (mensajes, contraseñas y claves de cifrado) están construidas indexando individualmente posiciones de la cadena `a` (por ejemplo, `a[71]+a[64]+...`).
3. La función `arg133(arg432)` comprueba la contraseña ingresada por el usuario contra la cadena construida:
   ```python
   a[71]+a[64]+a[79]+a[79]+a[88]+a[66]+a[71]+a[64]+a[77]+a[66]+a[68] # "happychance"
   ```
4. Si la contraseña es correcta, invoca `arg111(arg444)` para descifrar el contenido del archivo `flag.txt.enc` usando una clave de cifrado repetitiva con la función `arg122`:
   ```python
   a[81]+a[64]+a[79]+a[82]+a[66]+a[64]+a[75]+a[75]+a[72]+a[78]+a[77] # "rapscallion"
   ```
5. El algoritmo de descifrado es un XOR simple carácter a carácter entre el texto cifrado y la clave extendida.

### Resolución mediante script

Podemos escribir un script para desofuscar las cadenas y descifrar la bandera directamente sin necesidad de introducir la contraseña interactivamente:

```python
a = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "
key = a[81]+a[64]+a[79]+a[82]+a[66]+a[64]+a[75]+a[75]+a[72]+a[78]+a[77]

with open("flag.txt.enc", "rb") as f:
    enc = f.read().decode()

def decrypt(ciphertext, key):
    extended_key = key
    i = 0
    while len(extended_key) < len(ciphertext):
        extended_key += key[i]
        i = (i + 1) % len(key)
    return "".join(chr(ord(c) ^ ord(k)) for c, k in zip(ciphertext, extended_key))

flag = decrypt(enc, key)
print("Flag:", flag)
```

Al ejecutar el script de resolución:

```bash
python3 solve.py
```

Se obtiene la bandera descifrada en formato `academy{...}`.

## Notas adicionales
La ofuscación por indexación de caracteres es trivialmente reversible evaluando las expresiones en un intérprete interactivo de Python. Además, al tratarse de un cifrado de flujo XOR simétrico con una clave estática predecible, el descifrado es instantáneo.

## Referencias
- Reto: https://learn.cylabacademy.org/library/256
- Apoyo: https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals
