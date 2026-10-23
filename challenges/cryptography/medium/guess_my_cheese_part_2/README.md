# Cryptography — Guess My Cheese (Part 2)

## Descripción

> **Prompt oficial del reto:** "The imposter was able to fool us last time, so we've strengthened our defenses!
> Here's our list of cheeses."

> **Hints:**
> 1. I heard that *SHA-256* is the best hash function out there!
> 2. Remember Squeexy, we enjoy our cheese with exactly *2 nibbles* of *hexadecimal-character salt*!
> 3. Ever heard of *rainbow tables*?

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** aditin

## Solución

En esta segunda parte, el servicio reemplaza el cifrado afín por una función hash criptográfica SHA-256 con sal (*salt*). Al conectarse, entrega un hash SHA-256 de 64 caracteres hexadecimales.

### Análisis y espacio de búsqueda

Las pistas indican:
1. Función hash: **SHA-256**.
2. Sal: *"exactly 2 nibbles of hexadecimal-character salt"* $\implies 1 \text{ byte} = 2 \text{ nibbles} = 256$ posibles valores ($0 \text{ a } 255$, o bytes `\x00` a `\xff`).
3. Diccionario: Un archivo provisto con 599 nombres de queso (`cheese_list.txt`).

La sal consiste en un byte binario añadido al final del nombre del queso en minúsculas:
$$H = \text{SHA256}(\text{cheese.lower()} + \text{bytes}([b]))$$

El espacio total de búsqueda es:
$$599 \times 256 = 153{,}344 \text{ combinaciones}$$

Calcular 150 mil hashes SHA-256 en memoria toma menos de 0.05 segundos en Python.

### Proceso de resolución

1. Conectarse al servicio por socket y extraer el hash objetivo de la sesión activa.
2. Iterar en memoria sobre los 599 quesos y los 256 valores de sal hasta encontrar la colisión con el hash objetivo.
3. El servicio solicita primero el nombre del queso original y luego el valor de la sal en formato hexadecimal de dos dígitos (`00` a `ff`).
4. Al enviar ambos valores correctamente, el servidor entrega la flag.

### Script de resolución

```python
import socket, re, hashlib

# Cargar lista de quesos
with open("cheese_list.txt") as f:
    cheeses = [l.strip() for l in f if l.strip()]

# Conectar al servicio
s = socket.create_connection(("<HOST>", <PUERTO>), timeout=10)

def recv_until(target):
    buf = b""
    while target not in buf:
        d = s.recv(1024)
        if not d: break
        buf += d
    return buf.decode(errors="replace")

init = recv_until(b"What would you like to do?")
target_hash = re.search(r"secret cheese --.*?:\s*([0-9a-fA-F]{64})", init).group(1).lower()

# Fuerza bruta local inmediata en memoria (<0.05s)
found = None
for cheese in cheeses:
    var = cheese.lower()
    for b in range(256):
        p = (var + chr(b)).encode("latin1")
        if hashlib.sha256(p).hexdigest() == target_hash:
            found = (cheese, f"{b:02x}")
            break
    if found: break

orig_cheese, salt_hex = found

# Responder al cuestionario
s.sendall(b"g\n")
recv_until(b"So...what's my cheese?\n")
s.sendall(f"{orig_cheese}\n".encode())

recv_until(b"Annnnd...what's my salt?\n")
s.sendall(f"{salt_hex}\n".encode())

resp = s.recv(4096).decode(errors="replace")
print(resp)
s.close()
```

## Referencias

- [SHA-2 — Wikipedia](https://en.wikipedia.org/wiki/SHA-2)
- [Salt (cryptography) — Wikipedia](https://en.wikipedia.org/wiki/Salt_(cryptography))
