# Cryptography — Tapping

## Descripción

> **Prompt oficial del reto:** "Theres tapping coming in from the wires."

> **Hints:**
> 1. [What kind of encoding uses dashes and dots?](https://en.wikipedia.org/wiki/Morse_code)
> 2. The flag is in the format academy{}

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny

## Solución

Al conectarse al servicio por `nc`, se recibe una secuencia de pulsos en código Morse compuesta por puntos (`.`) y rayas (`-`), separados por espacios:

```
.- -.-. .- -.. . -- -.-- { -- ----- .-. ... ...-- -.-. ----- -.. ...-- .---- ... ..-. ..- -. ..--- .---- ---.. -.-. ..-. ----. --... ----. }
```

### Decodificación de Código Morse

Decodificando símbolo por símbolo con el alfabeto Morse internacional:

| Símbolo | Carácter | Símbolo | Carácter |
|---|---|---|---|
| `.-` | A | `-.-.` | C |
| `.-` | A | `-..` | D |
| `.` | E | `--` | M |
| `-.--` | Y | `{` | { |
| `--` | M | `-----` | 0 |
| `.-.` | R | `...` | S |
| `...--` | 3 | `-.-.` | C |
| `-----` | 0 | `-..` | D |
| `...--` | 3 | `.----` | 1 |
| `...` | S | `..-.` | F |
| `..-` | U | `-.` | N |
| `..---` | 2 | `.----` | 1 |
| `---..` | 8 | `-.-.` | C |
| `..-.` | F | `----.` | 9 |
| `--...` | 7 | `----.` | 9 |
| `}` | } | | |

La flag decodificada es: `academy{M0RS3C0D31SFUN218CF979}`.

### Script de resolución

```python
import socket

# Conectar al servicio
s = socket.create_connection(("<HOST>", <PUERTO>), timeout=10)
morse_raw = s.recv(4096).decode().strip()
s.close()

MORSE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F",
    "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
    "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R",
    "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
    "-.--": "Y", "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7",
    "---..": "8", "----.": "9"
}

decoded = "".join(MORSE.get(token, token) for token in morse_raw.split())
print(decoded)
```

## Referencias

- [Morse Code — Wikipedia](https://en.wikipedia.org/wiki/Morse_code)
