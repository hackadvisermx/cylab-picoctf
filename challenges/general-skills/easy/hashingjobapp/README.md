# General Skills — HashingJobApp

## Descripción
> **Prompt oficial:** "If you want to hash with the best, beat this test! `nc <host> <puerto>`"
>
> **Hints:**
> 1. You can use a commandline tool or web app to hash text
> 2. Press Ctrl and c on your keyboard to close your connection and return to the command prompt.

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
El servicio pide, en varias rondas seguidas, el hash **MD5** de una frase entre comillas (sin las comillas). Se automatizó con un socket Python que en bucle: lee la frase, calcula `hashlib.md5(frase.encode()).hexdigest()` y la envía, hasta que aparece la flag.

```python
import socket, hashlib, re, time
s = socket.create_connection(("<host>", <puerto>))
buf = s.recv(65536).decode()
while True:
    m = re.search(r"between quotes, excluding the quotes: '(.*?)'", buf)
    if not m: break
    s.sendall((hashlib.md5(m.group(1).encode()).hexdigest() + "\n").encode())
    time.sleep(0.4)
    buf = s.recv(65536).decode()
    if "picoCTF{" in buf: break
```

Flag: `picoCTF{4ppl1c4710n_r3c31v3d_bf2ceb02}`

## Notas adicionales
- Número variable de rondas antes de dar la flag (en esta ejecución fueron varias frases distintas seguidas); conviene iterar hasta ver `picoCTF{` en la respuesta en vez de asumir un número fijo de iteraciones.

## Referencias
- Reto: https://learn.cylabacademy.org/library/243
