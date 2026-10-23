# Cryptography — Timestamped Secrets

## Descripción

> **Prompt oficial del reto:** "Someone encrypted a message using AES in ECB mode but they weren’t very careful with their key. Turns out it’s derived from something as simple as the current time!
> Can you uncover the key and decrypt the flag?
> Download the encrypted message: message  
> You may also find the encryption script helpful: code"

> **Hints:**
> 1. `encryption.py` is a redacted example of the program

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución

El reto entrega dos archivos:
1. `encryption.py`: El script de cifrado en Python.
2. `message.txt`: El texto cifrado y una pista con el timestamp aproximado.

```python
def encrypt(plaintext: str, timestamp: int) -> str:
    timestamp = int(time.time())
    key = sha256(str(timestamp).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad(plaintext.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded)
    return ciphertext.hex()
```

Y en `message.txt`:
```
Hint: The encryption was done around 1790147509 UTC
Ciphertext (hex): e24b9c357ad38df368104cc83fd235607bdac8f0f83123b38a89f459e46a3db2
```

### Vulnerabilidad: Clave derivada de una semilla con entropía trivial (Timestamp Unix)

La clave AES de 128 bits se genera tomando los primeros 16 bytes del hash SHA-256 de la representación en cadena de un timestamp Unix:
$$\text{key} = \text{SHA256}(\text{str}(\text{timestamp}))[:16]$$

Dado que el timestamp aproximado $T_0 = 1790147509$ es conocido, el espacio de búsqueda es diminuto. Evaluando los timestamps en un radio cercano alrededor de $T_0$ (de hecho, el timestamp exacto es $1790147509$ con $\Delta = 0$), se deriva la clave AES y se descifra el texto plano en modo ECB.

### Script de resolución

```python
from hashlib import sha256
from Crypto.Cipher import AES

target_ct = bytes.fromhex("e24b9c357ad38df368104cc83fd235607bdac8f0f83123b38a89f459e46a3db2")
base_ts = 1790147509

# Búsqueda en una ventana de segundos
for delta in range(1000):
    for sign in [1, -1]:
        ts = base_ts + sign * delta
        key = sha256(str(ts).encode()).digest()[:16]
        cipher = AES.new(key, AES.MODE_ECB)
        dec = cipher.decrypt(target_ct)
        if b"academy{" in dec or b"picoCTF{" in dec:
            print("Flag descifrada:", dec.decode(errors="replace").strip())
            exit(0)
```

## Referencias

- [Insecure Randomness / Predictable Seeds — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [PyCryptodome AES ECB Mode](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html)
