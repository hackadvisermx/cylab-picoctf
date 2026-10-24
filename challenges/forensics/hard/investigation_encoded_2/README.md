# Forensics — investigation_encoded_2

## Descripción
> **Prompt oficial del reto:** "What can you make of this? We have recovered a [binary](https://challenge-files.cylabacademy.net/library/a9b971171194fa6973c2c94fbafe04aadfadfd84d190012e3f21955398e31c5b/no_auth_mistery) and 1 file: [image01](https://challenge-files.cylabacademy.net/library/a9b971171194fa6973c2c94fbafe04aadfadfd84d190012e3f21955398e31c5b/investigation-encoded-2-output). See what you can make of it. NOTE: The flag is not in the normal academy{XXX} format."
>
> **Hints:**
> 1. Only use lower case letters and numbers

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Santiago C

## Solución
El reto proporciona un archivo ejecutable ELF (`no_auth_mistery`) y un archivo codificado binario (`output`).

1. **Ingeniería inversa de la función de codificación (`encode`):**
   - El algoritmo procesa cada carácter de entrada de la siguiente forma:
     - Si es espacio `' '`, se asigna el código `36` (`0x24`).
     - Si es un dígito `'0'-'9'`, se transforma según `c + 0x4B - 0x61` (rango 26 a 35).
     - Si es una letra minúscula `'a'-'z'`, se indexa como `c - 0x61` (rango 0 a 25).
     - Para caracteres distintos del espacio, se calcula `(c + 18) % 36`.
   - Se consulta una tabla de offsets acumulados llamada `indexTable` en `.rodata` (`0x1360`).
   - El rango de bits de cada símbolo se delimita por `start = indexTable[c]` y `end = indexTable[c + 1]`.
   - Los bits correspondientes se leen secuencialmente de un arreglo constante `secret` en `.rodata` (`0x1300`) y se empaquetan en `output`.

2. **Decodificación por diccionario de bits:**
   - Dado que el espacio de caracteres válidos comprende únicamente letras minúsculas `'a'-'z'` y números `'0'-'9'`, se calcula la secuencia de bits exacta para cada uno de los 36 caracteres posibles.
   - Con este mapeo unívoco, se recorre el archivo `output` bit a bit decodificando cada símbolo correspondiente sin ambigüedad.

```python
#!/usr/bin/env python3
import struct

with open("mystery", "rb") as f:
    data = f.read()

# secret e indexTable ubicados en .rodata
secret_offset = 0x1300
index_offset = 0x1360

secret = data[secret_offset : secret_offset + 0x48]
indexTable = [struct.unpack("<I", data[index_offset + i*4 : index_offset + (i+1)*4])[0] for i in range(38)]

def get_bit(idx):
    byte_idx = idx >> 3
    bit_pos = idx & 7
    return (secret[byte_idx] >> (7 - bit_pos)) & 1

def encode_char(ch):
    c = ord(ch.lower())
    if c == ord(" "):
        code = 36
    elif ord("0") <= c <= ord("9"):
        code = c + 0x4b - 0x61
    else:
        code = c - 0x61
    if code != 36:
        code = (code + 18) % 36
    start, end = indexTable[code], indexTable[code + 1]
    return "".join(str(get_bit(b)) for b in range(start, end))

# Crear tabla de decodificación
bits_map = {encode_char(ch): ch for ch in "abcdefghijklmnopqrstuvwxyz0123456789 "}

with open("output", "rb") as f:
    out_data = f.read()

out_bits = "".join(f"{b:08b}" for b in out_data)

decoded = ""
curr = ""
for bit in out_bits:
    curr += bit
    if curr in bits_map:
        decoded += bits_map[curr]
        curr = ""

print("Flag recuperada:", decoded)
```

## Notas adicionales
- La bandera se entrega directamente en texto plano (sin el prefijo `academy{...}`), como estipula la consigna oficial del reto.

## Referencias
- Reto: https://learn.cylabacademy.org/library/36
- Desensamblado x86_64 y optimizaciones aritméticas del compilador: https://godbolt.org
