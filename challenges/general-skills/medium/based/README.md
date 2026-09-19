# General Skills — Based

## Descripción
> **Prompt oficial del reto:** "To get truly 1337, you must understand different data encodings, such as hexadecimal or binary. Can you get the flag from this program to prove you are on the way to becoming 1337? Connect with `nc fickle-tempest.picoctf.net 62899`."
>
> **Hints:**
> 1. I hear python can convert things.
> 2. It might help to have multiple windows open.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Alex Fulton/Daniel Tunitis

## Solución
El servicio es un pequeño "quiz" interactivo de 3 rondas: en cada ronda muestra una palabra aleatoria codificada en un sistema de numeración distinto y pide devolverla en texto plano, con un límite de 45 segundos por ronda:

1. **Binario** (`01100011 01101111 ...`, bytes separados por espacio) → decodificar con `chr(int(byte, 2))` por cada grupo de 8 bits.
2. **Octal** (`o143 o150 o141 ...`, prefijo `o` + separado por espacio) → decodificar con `chr(int(num, 8))`.
3. **Hexadecimal** (`636f6c6f7261646f`, cadena contigua sin espacios ni prefijo `0x`) → decodificar con `bytes.fromhex(...)`.

Si las 3 respuestas son correctas y a tiempo, el servidor entrega la flag. Automatizado con un socket que detecta el formato de cada ronda por regex y responde en consecuencia:

```python
import socket, time, re

s = socket.create_connection(("fickle-tempest.picoctf.net", 62899), timeout=15)
s.settimeout(5)

def read_until_prompt():
    data = b""
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk: break
            data += chunk
            if b"Input:" in data or b"picoCTF" in data:
                break
    except socket.timeout:
        pass
    return data.decode(errors="replace")

def solve(buf):
    m = re.search(r"([01]{8}(?: [01]{8})+)", buf)
    if m:
        return "".join(chr(int(b, 2)) for b in m.group(1).split())
    m = re.search(r"((?:o[0-7]{2,3} ?)+)", buf)
    if m:
        nums = re.findall(r"o([0-7]{2,3})", m.group(1))
        return "".join(chr(int(n, 8)) for n in nums)
    m = re.search(r"\b([0-9a-fA-F]{6,})\b", buf)
    if m and len(m.group(1)) % 2 == 0:
        return bytes.fromhex(m.group(1)).decode()
    return None

buf = read_until_prompt()
while "Input:" in buf and "picoCTF" not in buf:
    ans = solve(buf)
    s.sendall((ans + "\n").encode())
    time.sleep(1)
    buf = read_until_prompt()
print(buf)
# You've beaten the challenge
# Flag: picoCTF{learning_about_converting_values_aa2bA794}
```

## Notas adicionales
- Punto clave para automatizar: cada ronda usa un **formato distinto de separadores/prefijos** (binario con espacios cada 8 bits, octal con prefijo `o` y espacios, hexadecimal contiguo sin separador ni prefijo), así que la detección debe basarse en regex específicas por formato, no en una sola heurística genérica.
- La ventana de 45 segundos por ronda hace inviable resolverlo a mano con calculadoras de conversión; conviene automatizar la conexión completa con un script en vez de ir copiando cada valor a un conversor online.

## Referencias
- Reto: https://learn.cylabacademy.org/library/35
