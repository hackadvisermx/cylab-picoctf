# Cryptography — PowerAnalysis: Part 1

## Descripción
> **Prompt oficial del reto:** "This embedded system allows you to measure the power consumption of the CPU while it is running an AES encryption algorithm. Use this information to leak the key via dynamic power analysis."
> 
> *Hints:*
> 1. "The power consumption is correlated with the Hamming weight of the bits being processed"
> 2. "You will need to figure out how to deal with the noise"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2023
- **Autor:** Anish Singhani

## Solución

Al interactuar con el servicio por socket TCP, este solicita un texto en claro de 16 bytes (en formato hexadecimal) y devuelve una traza de potencia discreta compuesta por 2666 muestras temporales:
```
Please provide 16 bytes of plaintext encoded as hex: 00112233445566778899aabbccddeeff
power measurement result:  [134, 131, 124, 112, 91, 99, 127, ...]
```

### Análisis de Potencia por Correlación (CPA)
El consumo energético de procesadores CMOS durante operaciones de cómputo depende de la conmutación de compuertas lógicas, modelable linealmente mediante el peso de Hamming (*Hamming Weight*) del dato intermedio procesado.

En el cifrador AES-128, la primera ronda calcula:
$$X_i = \text{Sbox}[P_i \oplus K_i]$$
donde $P_i$ es el $i$-ésimo byte del texto en claro y $K_i$ es el $i$-ésimo byte de la clave secreta.

1. **Hipótesis del modelo:** Para cada byte $i \in \{0, \dots, 15\}$ y cada posible hipótesis de clave $k \in [0, 255]$:
   $$H_{i, k}^{(j)} = \text{HW}(\text{Sbox}[P_i^{(j)} \oplus k])$$
   donde $j \in \{1, \dots, N\}$ recorre el conjunto de trazas recolectadas ($N = 100$).

2. **Cálculo de correlación de Pearson:** Se normalizan tanto las predicciones del modelo $H$ como las trazas de potencia medidas $T$ en cada punto temporal $t \in [0, 2665]$:
   $$r(k, t) = \frac{\sum_{j=1}^N (H_{i, k}^{(j)} - \bar{H}_{i, k})(T^{(j)}(t) - \bar{T}(t))}{\sigma_H \sigma_T \cdot N}$$

3. **Discriminación de clave:** El byte correcto $K_i$ produce un pico de correlación estadísticamente significativo ($|r| \approx 0.50 - 0.68$) en el punto temporal exacto en el que el hardware ejecuta la sustitución $\text{Sbox}$ correspondiente en la ALU/bus de datos:
   $$K_i = \arg\max_{k \in [0, 255]} \max_{t} |r(k, t)|$$

### Script de Recuperación

```python
import socket
import re
import os
import numpy as np

CID = 364
Sbox = (...) # S-box estándar de AES
HW = [bin(i).count('1') for i in range(256)]

HOST, PORT = "host", 1337

def get_trace(pt_bytes):
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.recv(1024)
    s.sendall(pt_bytes.hex().encode() + b'\n')
    res = b''
    while True:
        chunk = s.recv(4096)
        if not chunk: break
        res += chunk
        if b']' in chunk: break
    s.close()
    return [int(x.strip()) for x in re.search(r'\[(.*?)\]', res.decode(), re.DOTALL).group(1).split(',')]

# 1. Recolección de 100 trazas con textos aleatorios
plaintexts, traces = [], []
for _ in range(100):
    pt = os.urandom(16)
    plaintexts.append(pt)
    traces.append(get_trace(pt))

# 2. Normalización de trazas
P = np.array([[b for b in pt] for pt in plaintexts], dtype=np.uint8)
T = np.array(traces, dtype=np.float64)
T_norm = (T - np.mean(T, axis=0)) / np.std(T, axis=0)

# 3. CPA por byte
key = []
for byte_idx in range(16):
    best_corr, best_k = -1, -1
    for k in range(256):
        h = np.array([HW[Sbox[P[j, byte_idx] ^ k]] for j in range(100)], dtype=np.float64)
        h_norm = (h - np.mean(h)) / np.std(h)
        corr = np.abs(np.dot(h_norm, T_norm) / 100.0)
        max_corr = np.max(corr)
        if max_corr > best_corr:
            best_corr, best_k = max_corr, k
    key.append(best_k)

key_hex = bytes(key).hex()
print(f"academy{{{key_hex}}}")
```

## Notas adicionales
- A diferencia de un ataque puramente criptoanalítico sobre el cifrador matemático, los ataques por canal lateral explotan características físicas de la implementación en silicio.
- Formato de la bandera: `academy{...}`
