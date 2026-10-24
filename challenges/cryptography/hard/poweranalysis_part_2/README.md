# Cryptography — PowerAnalysis: Part 2

## Descripción
> **Prompt oficial del reto:** "This embedded system allows you to measure the power consumption of the CPU while it is running an AES encryption algorithm. However, this time you have access to only a very limited number of measurements.
> 
> Download the power-consumption traces for a sample of encryptions [traces.zip](https://challenge-files.cylabacademy.net/library/1c645847eff720372171865551b27cbd466a25ce19125bc19d81ad2169e2d0b8/traces.zip). The flag will be of the format `academy{<encryption key>}` where `<encryption key>` is 32 lowercase hex characters comprising the 16-byte encryption key being used by the program."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2023
- **Autor:** Anish Singhani

## Solución
El reto proporciona 100 trazas de consumo de energía (`trace00.txt` a `trace99.txt`) capturadas durante la ejecución de cifrado AES de 128 bits con una clave fija desconocida. Cada archivo contiene el texto en claro (16 bytes en hexadecimal) y 2666 muestras de potencia de la CPU.

Para recuperar la clave secreta se utiliza un ataque de análisis de potencia por correlación (Correlation Power Analysis - CPA) modelando la primera ronda de AES:
1. **Modelo de fuga:** El consumo energético en procesadores embebidos se correlaciona linealmente con el peso de Hamming (Hamming Weight) del estado intermedio tras la sustitución no lineal `SubBytes`:
$$H_{i, k} = \text{HW}(\text{SBOX}[P_i \oplus k])$$
donde $P_i$ es el $i$-ésimo byte del texto plano y $k \in [0, 255]$ es la hipótesis del byte de clave correspondiente.
2. **Cálculo de correlación:** Para cada byte $i \in \{0, \dots, 15\}$ y cada posible valor de clave $k \in \{0, \dots, 255\}$, se calcula el coeficiente de correlación de Pearson entre las predicciones del modelo $H$ y las trazas normalizadas $T$:
$$r = \frac{\sum (H - \bar{H})(T - \bar{T})}{\sqrt{\sum (H - \bar{H})^2 \sum (T - \bar{T})^2}}$$
3. Para cada posición de byte, el valor de $k$ que maximiza el valor absoluto de la correlación $|r|$ a lo largo de las muestras temporales corresponde al byte correcto de la clave.

```python
import numpy as np

# Tabla S-Box de AES y pesos de Hamming
sbox = [...] # S-box estándar de AES
HW = [bin(i).count('1') for i in range(256)]

plaintexts, traces = [], []
for i in range(100):
    with open(f'traces/trace{i:02d}.txt') as f:
        pt_hex = f.readline().split(':')[1].strip()
        tr_list = eval(f.readline().split(':')[1].strip())
        plaintexts.append(bytes.fromhex(pt_hex))
        traces.append(tr_list)

P = np.array([[b for b in pt] for pt in plaintexts])
T = np.array(traces, dtype=np.float64)

# Normalizar trazas
T_norm = (T - np.mean(T, axis=0)) / np.std(T, axis=0)

key = []
for byte_idx in range(16):
    best_corr, best_k = -1, -1
    for k in range(256):
        h = np.array([HW[sbox[P[i, byte_idx] ^ k]] for i in range(100)], dtype=np.float64)
        h_norm = (h - np.mean(h)) / np.std(h)
        corr = np.abs(np.dot(h_norm, T_norm) / 100.0)
        max_corr = np.max(corr)
        if max_corr > best_corr:
            best_corr, best_k = max_corr, k
    key.append(best_k)

recovered_key = bytes(key).hex()
print(f'academy{{{recovered_key}}}')
```

Al correlacionar los 16 bytes se recupera la clave de 32 caracteres hexadecimales y se forma la flag `academy{<encryption_key>}`.

## Notas adicionales
A diferencia de ataques por fuerza bruta tradicionales que requieren $2^{128}$ operaciones, CPA descompone el problema en 16 búsquedas independientes de 256 hipótesis cada una, reduciendo la complejidad total a $16 \times 256 = 4096$ evaluaciones.

## Referencias
- Reto: https://learn.cylabacademy.org/library/365
- Correlation Power Analysis: https://wiki.newae.com/Correlation_Power_Analysis
