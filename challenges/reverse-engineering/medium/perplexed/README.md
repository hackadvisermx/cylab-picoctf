# Reverse Engineering — perplexed

## Descripción
> **Prompt oficial del reto:** "Download the binary [here](https://challenge-files.cylabacademy.net/library/4c086b6045c5f2b5200e1ef7ff1daace7008f76e3614bc1d98e6fda8863c43c2/perplexed)."
>
> **Pistas oficiales:**
> *(Sin pistas proporcionadas)*

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** SkrubLawd

## Solución
El binario proporcionado es un ejecutable ELF de 64 bits para Linux (`perplexed`), no despojado de símbolos (*not stripped*). Al inspeccionar las funciones del binario se identifican `main` y una función de validación denominada `check`.

### Análisis de la función `check`

1. **Lectura y longitud de la entrada:**
   En `main`, el programa utiliza `fgets` para leer la cadena introducida por el usuario, almacenando hasta 256 bytes incluyendo el salto de línea `\n`. En `check`, se valida que la longitud total sea exactamente de 27 bytes (`0x1b`):
   ```assembly
   0x40116f: cmp rax, 0x1b
   0x401173: je  0x40117f
   ```
   Esto corresponde a 26 caracteres de la bandera seguidos del carácter de salto de línea `\n`.

2. **Constantes y empaquetado de bits:**
   El programa inicializa un buffer de 23 bytes en la pila (`[rbp - 0x50]`) utilizando tres valores de 64 bits:
   - `0x61fb7cbb4c0e8fc3` en offset 0
   - `0xd269df5b5afc9db9` en offset 8
   - `0xf467edf4ed1bfed2` en offset 15 (solapado 1 byte con el anterior)

3. **Lógica de comparación bit a bit:**
   - La función itera a través de los 23 bytes ($23 \times 8 = 184$ bits) del buffer cifrado.
   - Para la cadena de entrada del usuario, solo se comparan 7 bits por byte (los bits 1 a 7, omitiendo el bit más significativo 0 correspondiente al bit de signo en ASCII estándar):
     ```assembly
     0x4011d6: cmp dword ptr [rbp - 0x18], 0
     0x4011da: jne 0x4011e0
     0x4011dc: add dword ptr [rbp - 0x18], 1
     ```
   - Cada bit del buffer hardcodeado debe coincidir exactamente con el bit correspondiente de la entrada del usuario (`bit1 ^ bit2 == 0`). Si hay alguna discrepancia, la función retorna inmediatamente 1 (error).

### Script de resolución (Python)

Invirtiendo la asignación bit a bit:

```python
import struct

# Buffer reconstruido a partir de las constantes de 64 bits
buf = bytearray(32)
buf[0:8] = struct.pack("<Q", 0x61FB7CBB4C0E8FC3)
buf[8:16] = struct.pack("<Q", 0xD269DF5B5AFC9DB9)
buf[15:23] = struct.pack("<Q", 0xF467EDF4ED1BFED2)
data = buf[:23]

# Mapeo de bits para reconstruir la cadena esperada
input_bits = {}
str_byte_idx = 0
str_bit_idx = 0

for buf_byte_idx in range(23):
    for buf_bit_idx in range(8):
        if str_bit_idx == 0:
            str_bit_idx += 1

        mask1 = 1 << (7 - buf_bit_idx)
        bit1 = 1 if (data[buf_byte_idx] & mask1) > 0 else 0

        input_bits[(str_byte_idx, str_bit_idx)] = bit1

        str_bit_idx += 1
        if str_bit_idx == 8:
            str_bit_idx = 0
            str_byte_idx += 1
            if str_byte_idx == 27:
                break
    if str_byte_idx == 27:
        break

result = []
for b in range(27):
    val = 0
    for bit in range(8):
        val |= input_bits.get((b, bit), 0) << (7 - bit)
    result.append(val)

# Decodificar el texto resultante omitiendo el byte nulo / newline final
flag = bytes(result[:-1]).decode("latin1")
print(flag)
```

Al ejecutar el script de resolución:

```bash
python3 solve.py
```

Se obtiene la bandera completa con formato `academy{...}`.

## Notas adicionales
El reto ejemplifica una técnica clásica de ofuscación de contraseñas mediante serialización de bits y transposición de flujo (*bitstream deserialization*), donde la representación en memoria no almacena cadenas ASCII directamente visibles mediante `strings`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/458
- Apoyo: https://en.wikipedia.org/wiki/Bitstream
