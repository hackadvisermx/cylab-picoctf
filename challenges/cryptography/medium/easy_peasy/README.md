# Easy Peasy

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Origen:** picoCTF 2021  
**Puntos:** 40  
**Referencia:** https://play.picoctf.org/practice/challenge/284

---

## Descripción

> "A one-time pad is unbreakable, but can you manage to recover the flag? (Wrap around the end of the alphabet!) Connect with `nc mercury.picoctf.net 11188`"

El reto expone un servidor que cifra datos mediante un esquema de **One-Time Pad (OTP)**. En teoría, el OTP es criptográficamente irrompible. En la práctica, si el keystream se reutiliza, el esquema se rompe completamente. Aquí radica la vulnerabilidad.

> **Nota CyLab:** El reto requiere una instancia activa. En el entorno CyLab se accede mediante `nc <host> <puerto>` con las credenciales de la instancia asignada.

---

## Hints oficiales

1. "Maybe there's a way to get the key from the stream"
2. "If you know where the key started and the key length, could you tell where it was reused?"
3. "XOR the key with the ciphertext and see what happens"

---

## Solución

### Lógica del servidor

El servidor implementa un OTP con las siguientes características:

```python
KEY_LEN = 50000  # clave aleatoria de 50000 bytes
key = open('./key').read()

def encrypt(key_location, data):
    result = ''
    for i, c in enumerate(data):
        result += chr(ord(key[(key_location + i) % KEY_LEN]) ^ ord(c))
    return result
```

Al conectar:
1. El servidor cifra la flag con `key[0 : len(flag)]` y muestra el resultado en hexadecimal.
2. Guarda `key_location = len(flag)` como puntero interno.
3. A partir de ese momento, el usuario puede enviar datos para cifrar; cada llamada avanza `key_location`.

### La vulnerabilidad: reutilización del keystream

La propiedad fundamental del OTP es que la clave **nunca debe reutilizarse**. Si `C1 = P1 XOR K` y `C2 = P2 XOR K`, entonces `C1 XOR C2 = P1 XOR P2`, lo que permite recuperar el texto plano sin conocer la clave.

Aquí la clave tiene `KEY_LEN = 50000` bytes y el puntero avanza con cada cifrado aplicando módulo `KEY_LEN`. Esto significa que si forzamos al puntero a llegar a `50000`, el siguiente cifrado comenzará en la posición `0` — exactamente donde se cifró la flag.

### Pasos del ataque

```
1. Al conectar:
   server → encrypted_flag = flag XOR key[0 : flag_len]
   key_location = flag_len

2. Enviamos (50000 - flag_len) bytes de relleno:
   key_location = flag_len + (50000 - flag_len) = 50000 ≡ 0  (mod 50000)

3. Enviamos flag_len bytes de valor 0x00:
   server → encrypt(0, b'\x00' * flag_len) = key[0 : flag_len] XOR 0x00 = key[0 : flag_len]

4. Recuperamos la flag:
   flag = encrypted_flag XOR key[0 : flag_len]
```

Al cifrar bytes nulos (`\x00`), el XOR con el keystream produce directamente el keystream. Con ese keystream y el ciphertext original, obtenemos el plaintext.

---

## Script de ataque

```python
#!/usr/bin/env python3
"""
easy_peasy_solver.py
Explotación del OTP con keystream reutilizado (wrap-around en posición 0).
Uso: python3 easy_peasy_solver.py <host> <puerto>
"""

import socket
import sys

# ── Configuración ──────────────────────────────────────────────────────────────
HOST = sys.argv[1] if len(sys.argv) > 1 else 'mercury.picoctf.net'
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 11188
KEY_LEN = 50000
# ──────────────────────────────────────────────────────────────────────────────


def recv_until(s: socket.socket, delim: bytes = b'\n') -> bytes:
    """Leer bytes del socket hasta encontrar el delimitador."""
    buf = b''
    while not buf.endswith(delim):
        chunk = s.recv(1)
        if not chunk:
            break
        buf += chunk
    return buf


def recv_line(s: socket.socket) -> str:
    return recv_until(s, b'\n').decode(errors='replace').strip()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"[*] Conectado a {HOST}:{PORT}")

    # ── Paso 1: recibir la flag cifrada ────────────────────────────────────────
    enc_flag_hex = None
    while enc_flag_hex is None:
        line = recv_line(s)
        print(f"[server] {line}")
        # El servidor muestra algo como: "encrypted_flag = <hex>"
        if 'flag' in line.lower() and '=' in line:
            enc_flag_hex = line.split('=')[-1].strip()

    enc_flag = bytes.fromhex(enc_flag_hex)
    flag_len = len(enc_flag)
    print(f"[*] Flag cifrada ({flag_len} bytes): {enc_flag_hex}")

    # ── Paso 2: esperar el prompt para cifrar ──────────────────────────────────
    # El servidor muestra un menú / prompt; consumimos hasta que pide entrada
    while True:
        line = recv_line(s)
        print(f"[server] {line}")
        if line.endswith(':') or line.endswith('?') or 'input' in line.lower():
            break

    # ── Paso 3: agotar la clave enviando (KEY_LEN - flag_len) bytes de relleno ─
    padding_len = KEY_LEN - flag_len
    print(f"[*] Enviando {padding_len} bytes de relleno para wrap-around...")

    # El servidor suele pedir la longitud o los datos directamente en hex.
    # Ajusta el formato según el protocolo real observado al conectar.
    padding_hex = ('61' * padding_len)  # 'a' * padding_len en hex
    s.sendall((padding_hex + '\n').encode())

    # Consumir la respuesta del servidor (el ciphertext del relleno, ignorado)
    while True:
        line = recv_line(s)
        print(f"[server] {line}")
        if line.endswith(':') or line.endswith('?') or 'input' in line.lower():
            break

    # ── Paso 4: cifrar flag_len bytes de ceros → obtenemos el keystream ────────
    print(f"[*] Enviando {flag_len} bytes nulos para extraer keystream...")
    null_hex = ('00' * flag_len)
    s.sendall((null_hex + '\n').encode())

    # Leer la respuesta: keystream en hex
    keystream_hex = None
    while keystream_hex is None:
        line = recv_line(s)
        print(f"[server] {line}")
        if '=' in line:
            keystream_hex = line.split('=')[-1].strip()

    keystream = bytes.fromhex(keystream_hex)
    print(f"[*] Keystream recuperado: {keystream_hex}")

    # ── Paso 5: XOR → flag en claro ───────────────────────────────────────────
    flag_bytes = bytes(a ^ b for a, b in zip(enc_flag, keystream))
    flag = flag_bytes.decode(errors='replace')
    print(f"\n[+] Flag: {flag}")

    s.close()


if __name__ == '__main__':
    main()
```

> **Nota sobre el protocolo:** El script asume que el servidor recibe y responde en hexadecimal y usa `=` como separador. Al conectar con `nc` por primera vez, observa el formato exacto de los prompts y ajusta las condiciones de `recv_line` según sea necesario.

---

## Notas adicionales

### ¿Por qué este OTP no es seguro?

| Propiedad | OTP seguro | Este reto |
|-----------|-----------|-----------|
| Longitud de clave | = longitud del mensaje | 50 000 bytes (finita) |
| Reutilización | Nunca | Al llegar a 50 000, vuelve a 0 |
| Secuencia de cifrado | Independiente por mensaje | Puntero compartido y controlable |
| Seguridad | Perfecta (Shannon, 1949) | Rota por reutilización |

La lección del reto: **el OTP solo es seguro si la clave es tan larga como el mensaje, verdaderamente aleatoria y nunca reutilizada**. En cuanto el keystream se repite —aunque sea parcialmente— el esquema pierde toda su seguridad.

### Identidad algebraica usada

```
enc_flag  = flag    XOR key[0..n]
keystream = 0x00..0 XOR key[0..n]  →  keystream = key[0..n]

flag = enc_flag XOR keystream
     = (flag XOR key[0..n]) XOR key[0..n]
     = flag
```

La operación XOR es su propia inversa: `A XOR B XOR B = A`.

---

## Referencias

- Reto original: https://play.picoctf.org/practice/challenge/284
- Shannon, C. E. (1949). *Communication Theory of Secrecy Systems*. Bell System Technical Journal.
- [Wikipedia — One-time pad](https://en.wikipedia.org/wiki/One-time_pad)
- [Many-time pad attack](https://en.wikipedia.org/wiki/One-time_pad#Reuse_of_key_material)
