# Reverse Engineering — Chronohack

## Descripción
> **Prompt oficial del reto:** "Can you guess the exact token and unlock the hidden flag?
>
> Our school relies on tokens to authenticate students. Unfortunately, someone leaked an important [file for token generation](https://challenge-files.cylabacademy.net/library/08e018333ab14dda7d636ae20eee7f0e5cd1a76f796866c00705a44322fd63af/token_generator.py). Guess the token to get the flag.
> The access is granted through `nc chatelaine.cylabacademy.net 36089`."
>
> **Pistas oficiales:**
> 1. https://www.epochconverter.com/
> 2. https://learn.snyk.io/lesson/insecure-randomness/
> 3. Time tokens generation
> 4. Generate tokens for a range of seed values very close to the target time

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** Theoneste Byagutangaza

## Solución
El reto consiste en un servicio TCP interactivo en Python que genera un token aleatorio de 20 caracteres y permite hasta 50 intentos para adivinarlo.

### Análisis del archivo `token_generator.py`

En el código fuente proporcionado:

```python
def get_random(length):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random.seed(int(time.time() * 1000))  # seeding with current time (milliseconds)
    s = ""
    for i in range(length):
        s += random.choice(alphabet)
    return s
```

1. **Vulnerabilidad de aleatoriedad insegura:**
   - La función utiliza el generador pseudoaleatorio predeterminado de Python (Mersenne Twister), el cual es completamente determinista dado el valor inicial de semilla (*seed*).
   - La semilla se inicializa con el tiempo de época actual en milisegundos: `int(time.time() * 1000)`.

2. **Espacio de búsqueda reducido:**
   - Al establecer la conexión TCP con el servidor, la ejecución de `python3 token_generator.py` se dispara de forma inmediata.
   - El momento exacto de la semilla ocurre en la ventana de tiempo comprendida entre la conexión exitosa y la recepción del prompt `exit):`.
   - Dado que el servidor permite hasta 50 intentos por sesión, es posible probar un bloque de 50 milisegundos contiguos alrededor de la marca de tiempo estimada.

### Script de explotación (Python)

El script sincroniza la marca de tiempo local al conectar, estima el instante en el servidor y barre ventanas de semillas en milisegundos:

```python
import random
import socket
import time

HOST = "chatelaine.cylabacademy.net"
PORT = 36089
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
TOKEN_LENGTH = 20

def generate_token(seed):
    random.seed(seed)
    return "".join(random.choice(ALPHABET) for _ in range(TOKEN_LENGTH))

def recv_until(s, delim=b":"):
    buf = b""
    while not buf.endswith(delim):
        chunk = s.recv(1)
        if not chunk:
            break
        buf += chunk
    return buf

# Ventanas de búsqueda desplazadas por la latencia del proceso remoto
ranges = [
    range(-25, 25),
    range(25, 75),
    range(75, 125),
    range(125, 175),
    range(175, 225),
]

for r in ranges:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    t_connected = time.time() * 1000
    prompt = recv_until(s, b"exit):")
    t_prompt = time.time() * 1000

    t_est = int((t_connected + t_prompt) / 2)

    for delta in r:
        cand_seed = t_est + delta
        token = generate_token(cand_seed)
        s.sendall(token.encode() + b"\n")
        resp = recv_until(s, b"\n")
        if b"Congratulations" in resp:
            flag_data = s.recv(1024)
            print(resp + flag_data)
            break
        prompt = recv_until(s, b"exit):")
    s.close()
```

Al coincidir la semilla generada con la del servidor remoto, el programa imprime la bandera en formato `academy{...}`.

```bash
python3 solve.py
```

## Notas adicionales
La vulnerabilidad demuestra el riesgo de utilizar fuentes deterministas y predecibles (como el reloj del sistema) para sembrar PRNGs en contextos de autenticación o seguridad, violando el principio de aleatoriedad criptográficamente segura (CSPRNG, ej. módulo `secrets` de Python).

## Referencias
- Reto: https://learn.cylabacademy.org/library/468
- Apoyo: https://learn.snyk.io/lesson/insecure-randomness/
