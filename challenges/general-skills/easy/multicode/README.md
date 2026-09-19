# General Skills — MultiCode

## Descripción
> **Prompt oficial:** "We intercepted a suspiciously encoded message, but it's clearly hiding a flag. No encryption, just multiple layers of obfuscation. Can you peel back the layers and reveal the truth?"
>
> **Hints:**
> 1. The flag has been wrapped in several layers of common encodings such as ROT13, URL encoding, Hex, and Base64. Can you figure out the order to peel them back?
> 2. A tool like CyberChef can be interesting.

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
Cuatro capas de codificación (no cifrado) apiladas, a pelar de fuera hacia dentro:

```python
import base64, urllib.parse, codecs

s = open("message.txt").read().strip()
d1 = base64.b64decode(s)          # -> hex en ASCII
d2 = bytes.fromhex(d1.decode())    # -> texto URL-encoded + ROT13
d3 = urllib.parse.unquote(d2.decode())  # -> texto ROT13 puro
flag = codecs.encode(d3, "rot13")
print(flag)
```

Capas, en orden de aplicación (de fuera hacia dentro al desenvolver): **Base64 → Hex → URL-encoding (`%7B`/`%7D` para `{`/`}`) → ROT13**.

Flag: `picoCTF{nested_enc0ding_8dd03efe}`

## Notas adicionales
- Se reconoce cada capa por su "forma": Base64 (alfabeto `A-Za-z0-9+/=`), hex (solo `0-9a-f`), texto con `%XX` (URL-encoding), y finalmente texto legible tras ROT13 (`cvpbPGS` se reconoce a simple vista como "picoCTF" rotado).
- CyberChef (disponible en el propio Workspace de CyLab Academy) también resuelve esto con una receta "From Base64 → From Hex → URL Decode → ROT13" sin necesidad de escribir código.

## Referencias
- Reto: https://learn.cylabacademy.org/library/710
- Archivo: `message.txt` (copia en esta carpeta)
