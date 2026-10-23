# Cryptography — Black Cobra Pepper

## Descripción

> **Prompt oficial del reto:** "i like peppers. (change!)"

> **Hints:**
> 1. Does this remind you of any other popular encryption?
> 2. What purpose does the s-box serve?

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Philip Thayer & Cayden Liao

## Solución

El reto implementa una variante de cifrado por bloques tipo AES-128 con 10 rondas. Sin embargo, al inspeccionar el código fuente (`chall.py`), se observa un detalle crítico:

```python
def sub_bytes(state):
    return state

def sub_word(word):
    return word

def rcon(word):
    return word
```

### Vulnerabilidad: Cifrado completamente lineal sobre $\text{GF}(2)$

En AES estándar, la única componente no lineal que otorga resistencia a criptoanálisis diferencial y lineal es la sustitución de bytes (**S-box**). 

Sin la S-box:
1. `ShiftRows` es simplemente una permutación de bytes (lineal sobre $\text{GF}(2)$).
2. `MixColumns` multiplica cada columna por una matriz fija sobre $\text{GF}(2^8)$ (lineal sobre $\text{GF}(2)$).
3. `AddRoundKey` es un XOR directo (adición lineal sobre $\text{GF}(2)$).
4. El programa de expansión de clave (`gen_keys`) consiste exclusivamente en rotaciones y XORs sin no-linealidad.

Como todas las operaciones son lineales sobre $\text{GF}(2)$, el cifrado es una función afín:
$$\text{AES}(p, k) = M_{pt} \cdot p \oplus M_{k} \cdot k$$

Dado que se nos entregan dos textos cifrados cifrados con la misma clave desconocida $k$:
- $c_1 = \text{AES}(pt_1, k)$ (donde $pt_1 = \text{"72616e646f6d64617461313131313131"}$)
- $c_2 = \text{AES}(\text{flag}, k)$

Podemos cancelar la clave desconocida haciendo XOR entre ambos textos cifrados:
$$c_1 \oplus c_2 = M_{pt} \cdot (pt_1 \oplus \text{flag}) = \text{AES}(pt_1 \oplus \text{flag}, 0)$$

Dado que la matriz $M_{pt}$ es un operador lineal invertible de dimensión $128 \times 128$ sobre $\text{GF}(2)$, podemos:
1. Construir las 128 columnas de la matriz $M_{pt}$ cifrando cada vector canónico $e_i$ ($1 \le i \le 128$) con la clave nula (`00`*16).
2. Resolver el sistema lineal $M_{pt} \cdot x = c_1 \oplus c_2$ mediante eliminación gaussiana sobre $\text{GF}(2)$.
3. Recuperar la flag despejando: $\text{flag} = pt_1 \oplus x$.

### Script de resolución

```python
def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# Funciones de chall.py sin dependencias externas
from chall import AES

def hex_to_int(h):
    return int(h, 16)

def int_to_hex(val):
    return hex(val)[2:].zfill(32)

# 1. Construir las 128 columnas de la matriz lineal M sobre GF(2)
cols = []
for i in range(128):
    vec = 1 << (127 - i)
    out_hex = AES(int_to_hex(vec), "00" * 16)
    cols.append(hex_to_int(out_hex))

# 2. Cargar textos cifrados y vector y = c1 ^ c2
with open("output.txt") as f:
    lines = [l.strip() for l in f if l.strip()]

c1 = hex_to_int(lines[0])
c2 = hex_to_int(lines[1])
pt1 = hex_to_int("72616e646f6d64617461313131313131")
y = c1 ^ c2

# Construir matriz aumentada para eliminación gaussiana
rows = []
for r in range(128):
    bit_y = (y >> (127 - r)) & 1
    row_val = 0
    for c in range(128):
        bit_col = (cols[c] >> (127 - r)) & 1
        row_val |= (bit_col << (127 - c))
    rows.append([row_val, bit_y])

# Eliminación Gaussiana sobre GF(2)
for i in range(128):
    pivot = -1
    for r in range(i, 128):
        if (rows[r][0] >> (127 - i)) & 1:
            pivot = r
            break
    rows[i], rows[pivot] = rows[pivot], rows[i]
    for r in range(128):
        if r != i and ((rows[r][0] >> (127 - i)) & 1):
            rows[r][0] ^= rows[i][0]
            rows[r][1] ^= rows[i][1]

# Recuperar x = pt1 ^ flag
x_val = 0
for i in range(128):
    x_val |= (rows[i][1] << (127 - i))

flag_int = pt1 ^ x_val
flag_bytes = bytes.fromhex(int_to_hex(flag_int))
print("Flag descifrada:", flag_bytes.decode(errors="replace"))
```

## Referencias

- [Rijndael S-box — Wikipedia](https://en.wikipedia.org/wiki/Rijndael_S-box)
- [Linear Cryptanalysis — Wikipedia](https://en.wikipedia.org/wiki/Linear_cryptanalysis)
