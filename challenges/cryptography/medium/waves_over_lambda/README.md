# Cryptography — waves over lambda

## Descripción

> **Prompt oficial del reto:** "We made a lot of substitutions to encrypt this. Can you decrypt it?"

> **Hints:**
> 1. Flag is not in the usual flag format

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** invisibility/Danny

## Solución

Al conectar al servicio por `nc`, se recibe un encabezado con la flag cifrada seguido de un fragmento de texto literario (*Los hermanos Karamazov* de Fiódor Dostoyevski), todo cifrado con una sustitución monoalfabética aleatoria:

```
-------------------------------------------------------------------------------
auswqezd viqi fd gucq bjew - bqiocisag_fd_a_uhiq_jerple_hllawudjuz
-------------------------------------------------------------------------------
```

### Análisis del cifrado por sustitución

El encabezado sigue el patrón típico:
- `auswqezd` → `congrats`
- `viqi` → `here`
- `fd` → `is`
- `gucq` → `your`
- `bjew` → `flag`

Esto nos da una correspondencia inicial casi completa de los caracteres clave:
- `a` = `c`, `u` = `o`, `s` = `n`, `w` = `g`, `q` = `r`, `e` = `a`, `z` = `t`, `d` = `s`
- `v` = `h`, `i` = `e`
- `f` = `i`
- `g` = `y`
- `b` = `f`, `j` = `l`

En la cadena de la flag:
- `bqiocisag` → `frequency` (confirmando `o` = `q`)
- `fd` → `is`
- `a` → `c`
- `uhiq` → `over` (confirmando `h` = `v`)
- `jerple` → `lambda` (confirmando `r` = `m`, `p` = `b`, `l` = `d`)

El término "waves over lambda" alude a la relación física fundamental de la frecuencia de onda: $f = \frac{c}{\lambda}$ (*frequency is c over lambda*).

Finalmente, decodificando el bloque de sufijo `hllawudjuz`:
- `h` → `v`
- `l` → `d`
- `l` → `d`
- `a` → `c`
- `w` → `g`
- `u` → `o`
- `d` → `s`
- `j` → `l`
- `u` → `o`
- `z` → `t`

Resultado: `vddcgoslot`.

Uniendo todos los términos, la flag obtenida es `frequency_is_c_over_lambda_vddcgoslot` (sin prefijo `picoCTF{}` ni `academy{}`, tal como advertía la pista oficial).

### Script de resolución

```python
import socket

# Conexión al servicio y obtención del texto
s = socket.create_connection(("<HOST>", <PUERTO>), timeout=10)
data = b""
while True:
    chunk = s.recv(4096)
    if not chunk:
        break
    data += chunk
s.close()

text = data.decode(errors="replace")

# Mapeo derivado por análisis de frecuencia y patrones de palabras
mapping = {
    "a": "c", "b": "f", "c": "u", "d": "s", "e": "a", "f": "i", "g": "y",
    "h": "v", "i": "e", "j": "l", "l": "d", "o": "q", "p": "b", "q": "r",
    "r": "m", "s": "n", "u": "o", "v": "h", "w": "g", "z": "t"
}

decrypted_header = []
target_line = text.split("\n")[1]
for ch in target_line:
    decrypted_header.append(mapping.get(ch, ch))

print("".join(decrypted_header))
```

## Referencias

- [Monoalphabetic Substitution Cipher — Wikipedia](https://en.wikipedia.org/wiki/Substitution_cipher)
- [Frequency analysis — Wikipedia](https://en.wikipedia.org/wiki/Frequency_analysis)
