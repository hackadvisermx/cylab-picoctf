# Reverse Engineering — Tap into Hash

## Descripción
> **Prompt oficial del reto:** "Can you make sense of this source code file and write a function that will decode the given encrypted file content?
> Find the encrypted file [here](https://challenge-files.cylabacademy.net/library/e114790a79c2c4117cfc3b0d050e6c79b9cc0e7b8dc87e3322f2365fc272a3d6/enc_flag). It might be good to analyze [source file](https://challenge-files.cylabacademy.net/library/e114790a79c2c4117cfc3b0d050e6c79b9cc0e7b8dc87e3322f2365fc272a3d6/block_chain.py) to get the flag."
>
> **Pistas oficiales:**
> 1. Do you know what blockchains are? If so, you know that hashing is used in blockchains.
> 2. Download the encrypted flag file and the source file and reverse engineer the source file.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** NGIRIMANA Schadrack

## Solución
El reto proporciona un script en Python (`block_chain.py`) y un archivo de salida (`enc_flag`). Al examinar el archivo `enc_flag`, se observa que contiene la clave secreta y la cadena cifrada:

```text
Key: b'\xdar\xbd%x\x05\x979\xca\xb9\xa0\xb3\x92\xa6W\x06\xa0\xa7\xc0\xb8\xb7\x02\xa3\x93\x80\xa1>\xba\xc9\x0e^('
Encrypted Blockchain: b'\xe9p\x9a\x1f...'
```

### Análisis del algoritmo de cifrado en `block_chain.py`

1. **Construcción del mensaje plano:**
   - Se crea una simulación de blockchain con 5 bloques encadenados por sus hashes SHA-256.
   - La cadena `blockchain_string` concatena los hashes de los bloques separados por guiones `-`.
   - Se inserta el token (la bandera) en el punto medio de `blockchain_string`:
     ```python
     midpoint = len(plaintext) // 2
     modified_plaintext = plaintext[:midpoint] + inner_txt + plaintext[midpoint:]
     ```
   - Se aplica padding estándar PKCS#7 al mensaje con un tamaño de bloque de 16 bytes.

2. **Cifrado XOR simétrico:**
   - Se calcula el hash SHA-256 de la clave de 32 bytes: `key_hash = hashlib.sha256(key).digest()`.
   - Para cada bloque de 16 bytes de datos (`block`), se aplica una operación XOR contra `key_hash`:
     ```python
     cipher_block = xor_bytes(block, key_hash)
     ```
   - Dado que `xor_bytes` itera con `zip(a, b)` y `block` mide 16 bytes mientras que `key_hash` mide 32 bytes, la operación es equivalente a un XOR repetitivo de cada bloque de 16 bytes contra los primeros 16 bytes de `key_hash`.

### Descifrado

Dado que el XOR es una operación involutiva ($A \oplus K \oplus K = A$), para descifrar simplemente se aplica la misma operación XOR con `key_hash[:16]` sobre cada bloque de 16 bytes del texto cifrado, se retira el padding y se extrae la bandera ubicada en el centro del texto descifrado.

### Script de resolución (Python)

```python
import hashlib
import re

with open("enc_flag", "r") as f:
    lines = f.readlines()

key = eval(lines[0].split("Key: ")[1].strip())
enc = eval(lines[1].split("Encrypted Blockchain: ")[1].strip())

key_hash = hashlib.sha256(key).digest()[:16]

decrypted = bytearray()
for i in range(0, len(enc), 16):
    block = enc[i : i + 16]
    dec = bytes([a ^ b for a, b in zip(block, key_hash)])
    decrypted.extend(dec)

# Eliminar padding PKCS#7
pad_len = decrypted[-1]
plaintext = decrypted[:-pad_len].decode("latin1", errors="ignore")

# Extraer la flag con regex
match = re.search(r"academy\{[^}]+\}", plaintext)
if match:
    print(match.group(0))
```

Al ejecutar el script:

```bash
python3 solve.py
```

Se recupera la bandera en formato `academy{...}`.

## Notas adicionales
A pesar de la temática de blockchain y prueba de trabajo (*proof of work*), el reto no requiere revertir funciones hash unidireccionales: la clave simétrica y el texto cifrado completo están presentes en el archivo suministrado, reduciendo la resolución a la implementación de la función inversa de XOR por bloques.

## Referencias
- Reto: https://learn.cylabacademy.org/library/466
- Apoyo: https://en.wikipedia.org/wiki/XOR_cipher
