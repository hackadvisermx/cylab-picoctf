# Cryptography — shift registers

## Descripción

> **Prompt oficial del reto:** "I learned about lfsr today in school so i decided to implement it in my program. It must be safe right?"

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Philip Thayer

## Solución

El reto presenta una implementación de un generador de flujo basado en LFSR (*Linear Feedback Shift Register*):

```python
key = bytes_to_long(get_random_bytes(126))

def steplfsr(lfsr):
    b7 = (lfsr >> 7) & 1
    b5 = (lfsr >> 5) & 1
    b4 = (lfsr >> 4) & 1
    b3 = (lfsr >> 3) & 1

    feedback = b7 ^ b5 ^ b4 ^ b3
    lfsr = (feedback << 7) | (lfsr >> 1)
    return lfsr

def encrypt_lfsr(pt_bytes):
    output = bytearray()
    lfsr = key & 0xFF
    for p in pt_bytes:
        lfsr = steplfsr(lfsr)
        ks = lfsr
        output.append(p ^ ks)
    return bytes_to_long(bytes(output))
```

### Vulnerabilidad: Espacio de estados diminuto (8 bits)

Aunque la clave generada inicialmente tiene 126 bytes (`get_random_bytes(126)`), la función de cifrado solo utiliza los últimos 8 bits para inicializar el LFSR:
$$\text{lfsr}_0 = \text{key} \ \& \ 0\text{xFF}$$

Un LFSR de 8 bits tiene únicamente $2^8 = 256$ estados iniciales posibles ($0 \le \text{lfsr}_0 < 256$).

Por lo tanto, basta con iterar exhaustivamente sobre los 256 estados iniciales posibles, simular el avance del LFSR para descifrar el flujo mediante XOR y buscar la cadena que contenga `academy{`.

### Script de resolución

```python
ct_hex = "30cbb50e507774fdafd01e0bfdbc38d5eadf92991cdd347064e37444e517d661cea9"
ct_bytes = bytes.fromhex(ct_hex)

def steplfsr(lfsr):
    b7 = (lfsr >> 7) & 1
    b5 = (lfsr >> 5) & 1
    b4 = (lfsr >> 4) & 1
    b3 = (lfsr >> 3) & 1

    feedback = b7 ^ b5 ^ b4 ^ b3
    return (feedback << 7) | (lfsr >> 1)

# Probar los 256 estados posibles
for initial_state in range(256):
    lfsr = initial_state
    pt = bytearray()
    for c in ct_bytes:
        lfsr = steplfsr(lfsr)
        pt.append(c ^ lfsr)
    if b"academy{" in pt or b"picoCTF{" in pt:
        print("Flag encontrada:", pt.decode())
        break
```

## Referencias

- [Linear-feedback shift register — Wikipedia](https://en.wikipedia.org/wiki/Linear-feedback_shift_register)
- [Stream cipher attacks — Wikipedia](https://en.wikipedia.org/wiki/Stream_cipher)
