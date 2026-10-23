# Easy Peasy

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Origen:** picoCTF 2021  
**Puntos:** 40  
**CyLab ID:** 125  
**Estado:** Resuelto

---

## Descripción

> "A one-time pad is unbreakable, but can you manage to recover the flag? (Wrap with academy{})"

El reto expone un servidor que cifra datos mediante un esquema de **One-Time Pad (OTP)**. En teoría, el OTP es criptográficamente irrompible. En la práctica, si el keystream se reutiliza, el esquema se rompe completamente.

**Hint oficial:** "Maybe there's a way to make this a 2x pad."

---

## Código del servidor

El servidor (`otp.py`) implementa el siguiente esquema:

```python
KEY_LEN = 50000
key = open("key", "rb").read()   # clave aleatoria de 50000 bytes

def startup(key_location):
    flag = open("flag").read()
    key = kf[key_location : key_location + len(flag)]
    key_location += len(flag)
    # imprime: "This is the encrypted flag!\n<hex>"
    return key_location

def encrypt(key_location):
    ui = input("What data would you like to encrypt? ").rstrip()
    # XOR de ui con kf[key_location : key_location + len(ui)]
    # key_location avanza (con wrap-around mod KEY_LEN)
    return key_location
```

Al conectar:
1. El servidor cifra la flag con `key[0 : len(flag)]` y muestra el resultado en hex.
2. Guarda `key_location = len(flag)` como puntero interno.
3. Permite al usuario cifrar datos arbitrarios; cada cifrado avanza `key_location`.
4. Cuando `key_location + len(input) >= KEY_LEN`, el wrap-around se aplica: usa `kf[start:] + kf[:stop]`.

---

## La vulnerabilidad: reutilización del keystream

La propiedad fundamental del OTP es que la clave **nunca debe reutilizarse**. Si `C1 = P1 XOR K` y `C2 = P2 XOR K`, entonces `C1 XOR C2 = P1 XOR P2`, lo que permite recuperar el texto plano.

Aquí la clave tiene `KEY_LEN = 50000` bytes y el puntero avanza con cada cifrado. Si forzamos al puntero a llegar a posición `50000 mod 50000 = 0`, el siguiente cifrado comenzará exactamente donde se cifró la flag.

---

## Ataque paso a paso

```
Paso 1: Conectar → servidor envía enc_flag = flag XOR key[0:N]
         key_location = N  (donde N = len(flag))

Paso 2: Enviamos (50000 - N) caracteres 'a':
         key_location = N + (50000 - N) = 50000 ≡ 0  (mod 50000)
         Resultado cifrado: lo ignoramos.

Paso 3: Enviamos N caracteres 'a':
         ks_result = key[0:N] XOR 'a'*N
         → keystream = ks_result XOR 'a'*N = key[0:N]

Paso 4: flag = enc_flag XOR keystream
              = (flag XOR key[0:N]) XOR key[0:N]
              = flag
```

### Identidad algebraica usada

```
enc_flag  = flag  XOR key[0:N]
ks_result = 'a'*N XOR key[0:N]
keystream = ks_result XOR 'a'*N = key[0:N]

flag = enc_flag XOR keystream
     = (flag XOR key[0:N]) XOR key[0:N]
     = flag
```

La operación XOR es su propia inversa: `A XOR B XOR B = A`.

---

## Ejecución real (CyLab)

La instancia CyLab se inicia en: `https://learn.cylabacademy.org/library/125`

Tras iniciar la instancia, la descripción incluye la cadena de conexión:  
`nc <host>.cylabacademy.net <puerto>`

### Protocolo del servidor

El servidor lee **cadenas de texto crudas** (no hex). Se envían directamente los caracteres:

```
Banner inicial:
  "******************Welcome to our OTP implementation!******************"
  "This is the encrypted flag!"
  "<hex del flag cifrado>"
  ""
  "What data would you like to encrypt? "

Turno 1 (padding):
  Enviamos: "aaa...a\n"  (50000 - flag_len caracteres)
  Servidor: "<hex del ciphertext de relleno>"

Turno 2 (extracción de keystream):
  Enviamos: "aaa...a\n"  (flag_len caracteres)
  Servidor: "Here ya go!"
            "<hex = key[0:N] XOR 'a'*N>"
```

### Script de ataque

```python
#!/usr/bin/env python3
"""
otp_solve.py  — Easy Peasy OTP wrap-around attack
Uso: python3 otp_solve.py <host> <port>
"""
import socket, sys, re, time

HOST, PORT = sys.argv[1], int(sys.argv[2])
KEY_LEN = 50000
PAD_CHAR = ord('a')

def recv_until(s, marker, timeout=20.0):
    data, deadline = b"", time.time() + timeout
    s.settimeout(timeout)
    while time.time() < deadline:
        ch = s.recv(1)
        if not ch: break
        data += ch
        if data.endswith(marker): break
    return data

s = socket.socket(); s.connect((HOST, PORT))

banner = recv_until(s, b"encrypt? ").decode(errors="replace")
m = re.search(r'This is the encrypted flag!\s*\n([0-9a-f]+)', banner, re.I)
enc_flag = bytes.fromhex(m.group(1))
N = len(enc_flag)
print(f"[*] enc_flag ({N}B): {m.group(1)}")

# Padding
s.sendall(b"a" * (KEY_LEN - N) + b"\n")
recv_until(s, b"encrypt? ", timeout=30.0)

# Keystream
s.sendall(b"a" * N + b"\n")
resp = recv_until(s, b"\n\n").decode(errors="replace")
ks = bytes.fromhex(re.search(r'([0-9a-f]{' + str(N*2) + r'})', resp, re.I).group(1))

# Flag
key = bytes(b ^ PAD_CHAR for b in ks)
flag_raw = bytes(a ^ b for a, b in zip(enc_flag, key)).decode()
inner = re.search(r'picoCTF\{([^}]+)\}', flag_raw).group(1)
print(f"[+] FLAG: academy{{{inner}}}")
```

---

## Resultado

- **Flag obtenida:** `academy{...}` (ver `scripts/creds.txt`)
- **Submission:** Correcto (`correct: true`)
- **Instancia usada:** `*.cylabacademy.net` (on-demand, 15 minutos)

---

## ¿Por qué este OTP no es seguro?

| Propiedad | OTP seguro | Este reto |
|-----------|-----------|-----------|
| Longitud de clave | = longitud del mensaje | 50 000 bytes (finita) |
| Reutilización | Nunca | Al llegar a 50 000, vuelve a 0 |
| Control del atacante | Ninguno | Podemos forzar el wrap-around |
| Seguridad | Perfecta (Shannon, 1949) | Rota por reutilización |

La lección: **el OTP solo es seguro si la clave es tan larga como el mensaje, verdaderamente aleatoria y nunca reutilizada**. En cuanto el keystream se repite —aunque sea parcialmente— el esquema pierde toda su seguridad.

---

## Referencias

- Reto original picoCTF: https://play.picoctf.org/practice/challenge/284
- CyLab Academy: https://learn.cylabacademy.org/library/125
- Código del servidor: `otp.py` (disponible en la instancia CyLab)
- Shannon, C. E. (1949). *Communication Theory of Secrecy Systems*. Bell System Technical Journal.
- [Wikipedia — One-time pad](https://en.wikipedia.org/wiki/One-time_pad)
