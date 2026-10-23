# Cryptography — la cifra de

## Descripción

> **Prompt oficial del reto:** "I found this cipher in an old book."

> **Hints:**
> 1. There are tools that make this easy.
> 2. Perhaps looking at history will help

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Alex Fulton/Daniel Tunitis

## Solución

El reto presenta un texto extenso cifrado que relata la historia de la criptografía polialfabética:
- El título *"la cifra de"* hace alusión al tratado histórico de 1553: *La cifra del Sig. Giovan Battista Bellaso*, quien introdujo el concepto de clave polialfabética que posteriormente fue atribuido de forma errónea a Blaise de Vigenère.
- El texto está cifrado mediante el **cifrado Vigenère**.

### Análisis y obtención de la clave

Comparando las primeras palabras del texto cifrado con el texto histórico conocido en inglés:
- Ciphertext: `Ne iy nytkwpsznyg...`
- Plaintext: `It is interesting...`

Calculando el desplazamiento carácter por carácter:
- `N` (13) - `I` (8) = 5 → `f`
- `e` (4) - `t` (19) ≡ 11 → `l`
- `i` (8) - `i` (8) = 0 → `a`
- `y` (24) - `s` (18) = 6 → `g`

La clave del cifrado es la palabra **`flag`** (de longitud 4).

### Descifrado de la flag

Al aplicar el descifrado Vigenère con la clave `flag` (ajustando la fase de rotación por los caracteres que no avanzan el flujo de clave), la línea final del mensaje revela el texto en claro:

```
For the implementation of this cipher a table is formed by sliding the lower half of an ordinary alphabet for an apparently random number of places with respect to the upper halfacademy{b311a50_0r_v1gn3r3_c1ph3r36311a0a}
```

La flag obtenida es: `academy{b311a50_0r_v1gn3r3_c1ph3r36311a0a}`.

### Script de resolución

```python
import socket

# Obtener texto cifrado del servicio
s = socket.create_connection(("<HOST>", <PUERTO>), timeout=10)
buf = b""
while True:
    data = s.recv(4096)
    if not data:
        break
    buf += data
s.close()

ciphertext = buf.decode(errors="replace")
key = "flag"

# Localizar la línea que contiene la flag cifrada
for line in ciphertext.split("\n"):
    if "{" in line:
        target_line = line
        break

# Probar la fase correcta de la clave 'flag' (longitud 4)
for phase in range(4):
    res = []
    ki = phase
    for ch in target_line:
        if ch.isalpha():
            k = key[ki % len(key)]
            shift = ord(k) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            res.append(chr(base + (ord(ch) - base - shift) % 26))
            ki += 1
        else:
            res.append(ch)
    plain = "".join(res)
    if "academy{" in plain or "picoCTF{" in plain:
        print("Flag encontrada:", plain)
```

## Referencias

- [Vigenère Cipher — Wikipedia](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
- [Giovan Battista Bellaso — Wikipedia](https://en.wikipedia.org/wiki/Giovan_Battista_Bellaso)
