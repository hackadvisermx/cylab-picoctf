# Cryptography — Compress and Attack

## Descripción
> **Prompt oficial del reto:** "Your goal is to find the flag."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** Jake Beley

## Solución
El reto expone un servicio interactivo a través del script `compress_and_attack.py`. El proceso implementado para cada entrada del usuario consiste en:
1. Concatenar la bandera secreta con la entrada del usuario: `flag + usr_input`.
2. Comprimir el texto resultante mediante el algoritmo DEFLATE usando `zlib.compress(...)`.
3. Cifrar el flujo comprimido mediante el cifrador de flujo Salsa20 (`Salsa20.new(key=secret)`).
4. Retornar el nonce, el criptograma y la **longitud en bytes del criptograma**.

### Vulnerabilidad: Ataque de oráculo de compresión (CRIME attack)
Aunque Salsa20 es un cifrador de flujo criptográficamente robusto, los cifradores de flujo no introducen relleno (padding), por lo que:
$$\text{len}(\text{ciphertext}) = \text{len}(\text{compressed\_plaintext})$$

El algoritmo de compresión DEFLATE (LZ77 + Huffman) sustituye cadenas de caracteres duplicadas por punteros (distancia, longitud). Cuando el atacante envía una cadena que coincide con una subsecuencia contigua dentro de la bandera:
- Si el carácter conjeturado es incorrecto, no existe repetición y el tamaño comprimido permanece constante o aumenta.
- Si el carácter conjeturado es correcto, LZ77 detecta la repetición de la secuencia compartida entre `flag` y `usr_input`, mejorando la tasa de compresión y reduciendo la longitud en bytes del criptograma resultante.

### Estrategia de explotación
1. Comenzar con el prefijo conocido del formato de flag (`academy{`).
2. Iterar sobre todos los caracteres posibles (alfanumérico y guión bajo).
3. Evaluar la longitud devuelta para cada conjetura `known + c`.
4. Seleccionar el carácter que minimice la longitud del criptograma (ajustando con padding cuando sea necesario para alinear con las fronteras de compresión de bytes).
5. Repetir hasta alcanzar el carácter de cierre `}`.

```bash
python3 - << 'EOF'
import socket
import string
import re

s = socket.create_connection(("chatelaine.cylabacademy.net", 38273))

def recv_prompt():
    buf = ""
    while "Enter your text to be encrypted: " not in buf:
        buf += s.recv(1024).decode("utf-8", errors="ignore")
    return buf

recv_prompt()

def query(payload):
    s.sendall(f"{payload}\n".encode())
    buf = recv_prompt()
    lines = [l.strip() for l in buf.split("\n") if l.strip().isdigit()]
    return int(lines[-1]) if lines else 9999

known = "academy{"
charset = string.ascii_letters + string.digits + "_}"

while not known.endswith("}"):
    scores = {}
    for c in charset:
        scores[c] = query(known + c)
    best_char = min(scores, key=scores.get)
    known += best_char
    print(f"[+] Flag parcial: {known}")

print(f"[+] Flag recuperada: {known}")
s.close()
EOF
```

La filtración progresiva carácter por carácter revela la flag completa en formato `academy{...}`.

## Notas adicionales
- Esta técnica es idéntica al ataque **CRIME** (Compression Ratio Info-leak Made Easy, CVE-2012-4929) desarrollado por Juliano Rizzo y Thai Duong contra protocolos TLS/SPDY con compresión activa, lo que motivó la deshabilitación sistemática de la compresión en capas de transporte seguras.

## Referencias
- Reto: https://learn.cylabacademy.org/library/127
- Apoyo: Juliano Rizzo and Thai Duong (2012), *The CRIME Attack against TLS compression*
