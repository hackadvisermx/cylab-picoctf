# Cryptography — Clouds

## Descripción
> **Prompt oficial del reto:** "Cloud watching is a lot of fun! There are so many different shapes you see in them, and so many different types. They even inspired me to dig up an old cipher I once found to store notes about them. See if you can decrypt them!"
> 
> *Nota del reto:* "The flag for this challenge does not include the standard academy{} wrapper."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** madStacks

## Solución

Al inspeccionar el código fuente del servicio (`clouds.py`), se observa la implementación de un cifrador por bloques de 64 bits (8 bytes) conocido como **Nimbus**, compuesto por 5 rondas y una clave maestra de 40 bytes dividida en 5 subclaves de 64 bits ($k_0, k_1, k_2, k_3, k_4$):

### Función de Ronda de Nimbus
Para cada bloque de 64 bits $b$ y cada ronda $i \in \{0, \dots, 4\}$:
1. **XOR:** $\text{temp} = b \oplus k_i$
2. **Inversión de bits (bit-reversal):** $g(\text{temp})$ invierte el orden de los 64 bits.
3. **Multiplicación modular:** $\text{out} = (g(\text{temp}) \cdot (k_i \mid 1)) \pmod{2^{64}}$

El servidor permite almacenar notas de hasta 512 bytes y recuperarlas por su índice, estando la bandera almacenada en el índice 0:
```python
flag = open("./flag").read().rstrip()
notes = [encrypt(flag)]
```

### Criptoanálisis Diferencial de Nimbus
El cifrador Nimbus es susceptible a criptoanálisis diferencial estructurado (investigación de Vladimir Furman / Dhrumil Patel).

Al escoger pares de textos en claro con una diferencia controlada:
$$\Delta = 2^{63} - 2$$
la operación de inversión de bits $g(x)$ y la multiplicación modular por $(k_i \mid 1)$ inducen cancelaciones predecibles en los bits menos significativos con una alta probabilidad diferencial:
1. Se generan 128 pares de textos en claro elegidos ($256$ bloques en total) con la diferencia fija $\Delta = 2^{63} - 2$.
2. **Optimización por lotes:** Dado que cada nota permite hasta 512 bytes (64 bloques = 32 pares), los 128 pares se envían en exactamente 4 notas al servidor, reduciendo drásticamente las operaciones I/O y evitando caídas de conexión por timeout.
3. **Filtrado por Condición 1:** Se evalúan los textos cifrados $(C_0, C_1)$ descartando aquellos que no cumplen las invariantes del bit menos significativo en $C_0 \oplus C_1$.
4. **Recuperación de Subclave Impar:** Usando el Algoritmo Extendido de Euclides para calcular la inversa modular sobre la diferencia observada:
$$k_{\text{odd}} \equiv ((C_0 + C_1) / \gcd(\Delta, 2^{64})) \cdot \text{scaler} \pmod{2^{64}}$$
5. **Pelado de Rondas Recursivo (Peeling):** Una vez hallada una subclave candidata para la ronda exterior, se descifra una ronda hacia atrás y se repite el procedimiento recursivamente para las 5 rondas hasta coincidir con los textos en claro originales.
6. **Descifrado de la Bandera:** Con las 5 subclaves $[k_0, k_1, k_2, k_3, k_4]$ recuperadas, se invierte la transformación sobre el bloque cifrado del índice 0:
$$b = \left(g\left( (C \cdot (k_i \mid 1)^{-1} \pmod{2^{64}}) \right) \oplus k_i\right) \pmod{2^{64}}$$

### Script de Solución

```bash
python3 - << 'EOF'
import socket, random, time
from collections import Counter
from itertools import repeat

ROUNDS = 5
BLOCK_LEN = 8
HEX_BLOCK_LEN = BLOCK_LEN * 2
diff = (1 << 63) - 2

def g(i):
    b = bin(i).lstrip("0b").rstrip("L").rjust(BLOCK_LEN * 8, "0")
    return int(b[::-1], 2)

def comp(msg, index):
    msg[index] = '1' if msg[index] == '0' else '0'
    return msg

def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return b, x, y

def condition1(ciphertexts):
    precandidates = []
    thirdLSBis1 = thirdLSBis0 = 0
    for ctext in ciphertexts:
        ci0, ci1 = map(int, ctext, repeat(16))
        cxor = ci0 ^ ci1
        cb0, cb1, cbxor = f'{ci0:064b}', f'{ci1:064b}', f'{cxor:064b}'
        if cbxor[-2:] != '10' or cb0[-1] != '0' or cb1[-1] != '0':
            continue
        precandidates.append(ctext)
        if cbxor[-3] == '1': thirdLSBis1 += 1
        else: thirdLSBis0 += 1
    defining = '1' if thirdLSBis1 >= thirdLSBis0 else '0'
    candidates = [pre for pre in precandidates if f'{int(pre[0], 16)^int(pre[1], 16):064b}'[-3] == defining]
    return candidates

def crack_subkey(ciphertexts):
    candidates = condition1(ciphertexts)
    gcdd, key_scaler, _ = egcd(diff, 1 << 64)
    keycounter = Counter()
    for cand in candidates:
        ci1, ci2 = map(int, cand, repeat(16))
        if (ci1 + ci2) % 2 != 0 or ci1 ^ ci2 == diff: continue
        kodd = (((ci1 + ci2) // gcdd) * key_scaler) % (1 << 64)
        kcomp = int(''.join(comp(list(f'{kodd:064b}'), 0)), 2)
        keycounter[kodd] += 1
        keycounter[kcomp] += 1
    if not keycounter: return None
    k_odd, conf = keycounter.most_common(1)[0]
    if conf <= 1: return None
    kcomp = int(''.join(comp(list(f'{k_odd:064b}'), 0)), 2)
    return [k_odd, kcomp, k_odd ^ 1, kcomp ^ 1]

def recurse(plaintexts, ciphertexts, kcands, keyers=[], depth=1):
    if depth > 5: return None, None
    for k in kcands:
        dciphertexts = [pair[:] for pair in ciphertexts]
        for pair in range(len(dciphertexts)):
            ci1, ci2 = map(int, dciphertexts[pair], repeat(16))
            ci1 = g((ci1 * pow(k | 1, -1, 1 << 64)) % (1 << 64)) ^ k
            ci2 = g((ci2 * pow(k | 1, -1, 1 << 64)) % (1 << 64)) ^ k
            dciphertexts[pair] = [f"{ci1:016x}", f"{ci2:016x}"]
        if all(int(dciphertexts[i][j], 16) == int(plaintexts[i][j], 2)
               for j in range(2) for i in range(len(dciphertexts))):
            return dciphertexts, [k] + keyers
        dkcands = crack_subkey(dciphertexts)
        if dkcands is None: continue
        v = recurse(plaintexts, dciphertexts, dkcands, [k] + keyers, depth + 1)
        if v is not None: return v
    return None

def decrypt_flag(ciphertext, keys):
    result = b""
    for i in range(0, len(ciphertext), HEX_BLOCK_LEN):
        block = int(ciphertext[i: i + HEX_BLOCK_LEN], 16)
        for k in keys[::-1]:
            block = (g(((block % (1 << 64)) * pow(k | 1, -1, 1 << 64)) % (1 << 64)) ^ k) % (1 << 64)
        result += block.to_bytes(8, 'big')
    return result
EOF
```

## Notas adicionales
- El cifrador Nimbus carece de suficiente no-linealidad en su función de ronda (la inversión de bits $g(x)$ y la multiplicación modular preservan demasiada estructura sobre diferencias seleccionadas), haciéndolo vulnerable a ataques diferenciales con muy pocos pares de textos elegidos.
- Flag en formato: `academy{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/136
- Análisis Diferencial de Nimbus: Vladimir Furman / Dhrumil Patel (Full Nimbus Attack)
