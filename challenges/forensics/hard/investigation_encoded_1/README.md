# Forensics — investigation_encoded_1

## Descripción
> **Prompt oficial del reto:** "What can you make of this? We have recovered a [binary](https://challenge-files.cylabacademy.net/library/4a85bdcac735d185e4e3e54f742e3804535fe4289c3857ac0516599e78614382/investigation-encoded-1-mystery) and 1 file: [image01](https://challenge-files.cylabacademy.net/library/4a85bdcac735d185e4e3e54f742e3804535fe4289c3857ac0516599e78614382/investigation-encoded-1-output). See what you can make of it. NOTE: The flag is not in the normal academy{XXX} format."

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Santiago C

## Solución
El reto proporciona un binario ELF de 64 bits (`mystery`) y un archivo resultante de la codificación (`output`).

1. **Análisis del algoritmo de codificación:**
   - Al desensamblar el binario se observa que el contenido de `flag.txt` se procesa carácter a carácter en la función `encode`.
   - Cada carácter alfabético se convierte a minúsculas y se consulta en una tabla de pares (`matrix`) ubicada en la sección `.rodata` (`0x2060`).
   - Cada entrada en `matrix` consta de:
     - Una longitud de bits (`length`).
     - Un offset inicial en bits (`start`).
   - A partir de este rango de bits, la función `getValue` lee una secuencia de bits desde un arreglo global constante denominado `secret` (`0x2020`).
   - La función `save` acumula estos bits de izquierda a derecha (MSB primero) y escribe los bytes correspondientes en el archivo `output`.
   - Si quedan bits pendientes al final, se rellena con bits cero hasta completar el último byte.

2. **Decodificación del flujo binario:**
   - Extrayendo las tablas `matrix` y `secret` del binario, se construye un diccionario unívoco de prefijos de bits para cada carácter del alfabeto ('a'-'z').
   - Posteriormente, se convierte el archivo `output` en un flujo de bits y se decodifica de forma secuencial empleando las secuencias prefijo.

```python
#!/usr/bin/env python3
import struct

with open("mystery", "rb") as f:
    data = f.read()

# secret y matrix en .rodata
secret_offset = 0x2020
matrix_offset = 0x2060
secret = data[secret_offset : secret_offset + 0x28]

def get_bit(idx):
    byte_idx = idx >> 3
    bit_pos = idx & 7
    return (secret[byte_idx] >> (7 - bit_pos)) & 1

bits_to_char = {}
for i in range(26):
    length, start = struct.unpack("<II", data[matrix_offset + i*8 : matrix_offset + (i+1)*8])
    char = chr(0x61 + i)
    bits = "".join(str(get_bit(start + b)) for b in range(length))
    bits_to_char[bits] = char

with open("output", "rb") as f:
    out_data = f.read()

out_bits = "".join(f"{b:08b}" for b in out_data)

decoded = ""
curr = ""
for bit in out_bits:
    curr += bit
    if curr in bits_to_char:
        decoded += bits_to_char[curr]
        curr = ""

print("Flag decodificada:", decoded)
```

## Notas adicionales
- Como se indica en la descripción oficial, la bandera para este reto no utiliza el formato con envoltura `academy{...}`, sino directamente la cadena en texto plano obtenida tras la decodificación.

## Referencias
- Reto: https://learn.cylabacademy.org/library/47
- Codificación Huffman / Códigos de prefijo: https://en.wikipedia.org/wiki/Prefix_code
