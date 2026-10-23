# Cryptography — cryptomaze

## Descripción

> **Prompt oficial del reto:** "In this challenge, you are tasked with recovering a hidden flag that has been encrypted using a combination of Linear Feedback Shift Register (LFSR) and AES encryption. The LFSR is used to derive a key for AES encryption, making it crucial to understand its workings to decrypt the message.
>
> The flag has been stored in a file and encrypted. Your goal is to derive the key used for encryption from the LFSR state and taps provided in the output, and then decrypt the flag to retrieve it.
> Download the encrypted flag from here which contains the following information:
> - The initial state of the LFSR
> - The taps used for the LFSR
> - The encrypted flag in hexadecimal format"

> **Hints:**
> 1. Use the LFSR’s initial state and taps to generate a 128-bit sequence.
> 2. Convert this 128-bit sequence into a 16-byte AES key by:
>    - Grouping the bits into 8-bit chunks (16 chunks in total).
>    - Converting each chunk from binary to a byte to form the AES key.
> 3. Decrypt the flag using AES in ECB mode.
> 4. Convert the encrypted flag from hex to bytes before decrypting.

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Sabine Gisagara

## Solución

El reto entrega un archivo `output.txt` con:
1. El estado inicial de un LFSR (Linear Feedback Shift Register) de 64 bits: una lista de 64 valores `0` y `1`.
2. Las posiciones de las tomas (*taps*) del LFSR: `[63, 61, 60, 58]`.
3. El texto cifrado en hexadecimal (`5fdec2...`).

Siguiendo las pistas oficiales, la clave AES de 128 bits (16 bytes) se deriva ejecutando el LFSR durante 128 pasos:
- En cada paso se calcula el bit de retroalimentación haciendo XOR de los bits en los índices de *taps*.
- Se extrae el bit saliente (`pop(0)`) y se inserta el bit de retroalimentación al final (`append`).
- Los 128 bits generados se agrupan en 16 bytes (orden más significativo primero, MSB).
- Se descifra el ciphertext en modo AES-ECB con la clave derivada.

### Script de resolución

```python
from Crypto.Cipher import AES

state = [
    0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0,
    1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1,
    0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1,
    1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1
]
taps = [63, 61, 60, 58]
enc_flag = bytes.fromhex("5fdec2e502a7c8d5951f41da4b0e0057244532434cd6a723c1e6e97f482f17d738338e7e04fbddef0c6260a4eb758417")

# Simular 128 pasos del LFSR
st = list(state)
bits = []
for _ in range(128):
    feedback = 0
    for t in taps:
        feedback ^= st[t]
    out = st.pop(0)
    st.append(feedback)
    bits.append(out)

# Agrupar en 16 bytes (MSB primero)
key_bytes = bytearray()
for i in range(0, 128, 8):
    val = 0
    for b in bits[i:i+8]:
        val = (val << 1) | b
    key_bytes.append(val)

# Descifrar con AES-ECB
cipher = AES.new(bytes(key_bytes), AES.MODE_ECB)
decrypted = cipher.decrypt(enc_flag)
print(decrypted)
```

Al ejecutar el script, obtenemos el texto plano de la flag con padding PKCS#7.

## Referencias

- [Linear-feedback shift register — Wikipedia](https://en.wikipedia.org/wiki/Linear-feedback_shift_register)
- [PyCryptodome AES documentation](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html)
