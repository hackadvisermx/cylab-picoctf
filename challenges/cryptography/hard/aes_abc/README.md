# Cryptography — AES-ABC

## Descripción
> **Prompt oficial del reto:** "AES-ECB is bad, so I rolled my own cipher block chaining mechanism - Addition Block Chaining! You can find the source here: aes-abc.py. The AES-ABC flag is body.enc.ppm"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** waituckw

## Solución
El reto implementa un esquema de cifrado personalizado denominado *Addition Block Chaining* (ABC) sobre una imagen en formato PPM (`body.enc.ppm`). Analizando el código fuente `aes-abc.py`, el proceso de cifrado consta de dos etapas:

1. Primero, los datos crudos de la imagen (excluyendo el encabezado PPM) se cifran usando **AES en modo ECB**.
2. A continuación, los bloques resultantes $c_1, c_2, \dots, c_n$ (de 16 bytes cada uno) se encadenan mediante una suma modular con un vector de inicialización aleatorio $c_0 = \text{IV}$:
   $$y_0 = c_0$$
   $$y_i = (y_{i-1} + c_i) \pmod{2^{128}} \quad \text{para } i = 1, \dots, n$$

Donde $y_i$ son los bloques transmitidos en el archivo final `body.enc.ppm`.

Dado que la operación de combinación es una simple suma modular invertible sin depender de una clave secreta para el encadenamiento, podemos despejar directamente el bloque cifrado en ECB $c_i$:
$$c_i = (y_i - y_{i-1}) \pmod{2^{128}}$$

Al recuperar todos los bloques $c_i$, obtenemos la imagen cifrada directamente con AES en modo ECB. Debido a que el modo ECB preserva patrones idénticos entre bloques de texto claro repetidos (el clásico efecto del pingüino de ECB), el contraste entre los píxeles de fondo uniforme y los trazos del texto permite visualizar la bandera directamente en la imagen reconstruida.

```bash
# Script de resolución para invertir Addition Block Chaining
python3 - << 'EOF'
import math
from PIL import Image

BLOCK_SIZE = 16
UMAX = int(math.pow(256, BLOCK_SIZE))

def to_bytes(n):
    s = hex(n)[2:].rstrip("L")
    if len(s) % 2 != 0:
        s = "0" + s
    decoded = bytes.fromhex(s)
    pad = len(decoded) % BLOCK_SIZE
    if pad != 0:
        decoded = b"\0" * (BLOCK_SIZE - pad) + decoded
    return decoded

def remove_line(s):
    idx = s.index(b"\n") + 1
    return s[:idx], s[idx:]

def parse_header_ppm(f):
    data = f.read()
    header = b""
    for _ in range(3):
        h, data = remove_line(data)
        header += h
    return header, data

with open("body.enc.ppm", "rb") as f:
    header, data = parse_header_ppm(f)

blocks = [data[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE] for i in range(len(data) // BLOCK_SIZE)]
recovered_ecb = bytearray()
for i in range(1, len(blocks)):
    prev_blk = int.from_bytes(blocks[i-1], byteorder="big")
    curr_blk = int.from_bytes(blocks[i], byteorder="big")
    orig_blk = (curr_blk - prev_blk) % UMAX
    recovered_ecb.extend(to_bytes(orig_blk))

with open("flag.ppm", "wb") as f:
    f.write(header)
    f.write(bytes(recovered_ecb))

# Convertir a PNG y abrir
im = Image.open("flag.ppm")
im.save("flag.png")
print("[+] Imagen ECB guardada en flag.png")
EOF
```

Al abrir `flag.png` o binarizar la imagen filtrando los 16 colores correspondientes al fondo repetido, el texto de la flag aparece nítidamente: `academy{...}`.

## Notas adicionales
- El formato PPM almacena píxeles RGB en bruto (3 bytes por píxel). Como cada bloque de AES tiene 16 bytes y $\text{mcm}(3, 16) = 48$ bytes (16 píxeles), los bloques del fondo se alinean en un ciclo de 3 bloques, generando un conjunto de exactamente 16 colores aparentes en el modo ECB.
- Filtrar los colores predominantes del fondo deja únicamente los trazos de los caracteres.

## Referencias
- Reto: https://learn.cylabacademy.org/library/76
- Apoyo: Documentación sobre vulnerabilidades de modo ECB en imágenes (Wikipedia: Block cipher mode of operation - ECB mode)
