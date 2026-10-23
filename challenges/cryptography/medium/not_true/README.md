# Cryptography — Not TRUe

## Descripción

> **Prompt oficial del reto:** "no. no. that's Not TRUe. that's impossible!
> Download encryption script and public info."

> **Hints:**
> 1. This is a lattice based cryptosystem. Is there a lattice attack that allows you to compute the private key given the public information?

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** ishaanharry

## Solución

El reto implementa el criptosistema post-cuántico basado en retículos **NTRU** sobre el anillo de polinomios:
$$R = \mathbb{Z}[x] / (x^N - 1)$$
con los parámetros:
- $N = 48$
- $p = 3$
- $q = 509$

La clave pública es el polinomio $h \equiv p \cdot f^{-1} \cdot g \pmod q$, donde $f$ y $g$ son polinomios ternarios secretos con coeficientes pequeños en $\{-1, 0, 1\}$.

### Ataque de retículos de Coppersmith-Shamir sobre NTRU

La relación de clave pública satisface:
$$f \cdot h \equiv p \cdot g \pmod q \implies f \cdot h - q \cdot k = p \cdot g$$

Consideramos el retículo generado por las filas de la matriz en bloques de dimensión $2N \times 2N$ ($96 \times 96$):
$$
M = \begin{pmatrix}
I_N & H \\
0 & q I_N
\end{pmatrix}
$$
donde $H$ es la matriz circulante generada por las rotaciones cíclicas del polinomio de clave pública $h$ ($x^i \cdot h \bmod (x^N - 1)$).

El vector $(f, p \cdot g) = (f, 3g)$ pertenece a este retículo. Dado que los coeficientes de $f$ pertenecen a $\{-1, 0, 1\}$ y los de $3g$ a $\{-3, 0, 3\}$, la norma euclidiana del vector secreto es diminuta:
$$\|(f, 3g)\|^2 \le 48 \cdot 1^2 + 48 \cdot 3^2 = 480 \implies \|(f, 3g)\| \le 21.9$$

En comparación, el radio de empaquetamiento esperado de Minkowski para un vector genérico en este retículo de dimensión 96 es $\approx 53.5$.

Por tanto, el vector de clave privada es un vector excepcionalmente corto en el retículo. Aplicando el algoritmo **LLL** (*Lenstra–Lenstra–Lovász*) sobre la matriz de $96 \times 96$, la primera fila del retículo reducido recupera directamente el polinomio secreto $f$.

### Descifrado

Con $f$ recuperado:
1. Calculamos el inverso $f_p^{-1} \pmod 3$ en $\mathbb{Z}_3[x] / (x^N - 1)$.
2. Para cada bloque cifrado $c_i$:
   - Calculamos $a \equiv f \cdot c_i \pmod q$.
   - Centramos los coeficientes de $a$ en el intervalo $(-q/2, q/2]$.
   - Recuperamos el polinomio de mensaje: $m \equiv f_p^{-1} \cdot a \pmod 3$.
3. Concatenamos los bits de $m$ y los convertimos a bytes para obtener la flag.

### Script de resolución

```python
import ast
from flint import fmpz_mat

N = 48
p = 3
q = 509

with open("public.txt") as f:
    text = f.read()

for line in text.strip().split("\n"):
    if line.startswith("h ="):
        h = ast.literal_eval(line.split("=", 1)[1].strip())
    elif line.startswith("ct ="):
        ct = ast.literal_eval(line.split("=", 1)[1].strip())

# 1. Construir matriz del retículo NTRU (96x96)
H = [[h[(k - i) % N] for k in range(N)] for i in range(N)]

M = [[0] * (2 * N) for _ in range(2 * N)]
for i in range(N):
    M[i][i] = 1
    for j in range(N):
        M[i][N + j] = H[i][j]
for i in range(N):
    M[N + i][N + i] = q

# 2. Reducción LLL con FLINT
mat = fmpz_mat(M)
reduced = mat.lll()
f = [int(reduced[0, c]) for c in range(N)]

def poly_mul_mod(a, b, mod=None):
    res = [0] * N
    for i in range(N):
        for j in range(N):
            k = (i + j) % N
            res[k] += a[i] * b[j]
    if mod:
        res = [c % mod for c in res]
    return res

# 3. Inversión de f módulo 3
F_mat = [[f[(k - i) % N] % 3 for k in range(N)] for i in range(N)]
aug = [F_mat[i] + [1 if i == j else 0 for j in range(N)] for i in range(N)]
for col in range(N):
    pivot = [r for r in range(col, N) if aug[r][col] % 3 != 0][0]
    aug[col], aug[pivot] = aug[pivot], aug[col]
    inv = pow(aug[col][col], -1, 3)
    aug[col] = [(c * inv) % 3 for c in aug[col]]
    for r in range(N):
        if r != col and aug[r][col] % 3 != 0:
            factor = aug[r][col]
            aug[r] = [(aug[r][i] - factor * aug[col][i]) % 3 for i in range(2 * N)]

f_p_inv = [aug[0][N + j] for j in range(N)]

# 4. Descifrado de los bloques de la flag
all_bits = []
for c_chunk in ct:
    fc = poly_mul_mod(f, c_chunk, q)
    a = [x if x <= q // 2 else x - q for x in fc]
    m_poly = poly_mul_mod(f_p_inv, [x % 3 for x in a], 3)
    all_bits.extend([x % 3 for x in m_poly])

bin_str = "".join(str(b) for b in all_bits)
flag = "".join(chr(int(bin_str[i:i+8], 2)) for i in range(0, len(bin_str), 8) if len(bin_str[i:i+8]) == 8)
print("Flag:", flag.strip("\x00"))
```

## Referencias

- [NTRUEncrypt — Wikipedia](https://en.wikipedia.org/wiki/NTRUEncrypt)
- [Coppersmith, Shamir (1997) - Lattice Attacks on NTRU](https://link.springer.com/chapter/10.1007/BFb0052233)
- [Hoffstein, Pipher, Silverman - An Introduction to Mathematical Cryptography (Chapter on NTRU)](https://link.springer.com/book/10.1007/978-1-4939-1711-2)
