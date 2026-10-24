# Cryptography — Sequences

## Descripción
> **Prompt oficial del reto:** "I wrote this linear recurrence function, can you figure out how to make it run fast enough and get the flag? Download the code here sequences.py. Note that even an efficient solution might take several seconds to run. If your solution is taking several minutes, then you may need to reconsider your approach."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2022
- **Autor:** Anish Singhani

## Solución

El script original define una recurrencia lineal homogénea de orden 4:
$$m(i) = 21\,m(i-1) + 301\,m(i-2) - 9549\,m(i-3) + 55692\,m(i-4)$$
con condiciones iniciales $m(0) = 1, m(1) = 2, m(2) = 3, m(3) = 4$, y solicita computar $m(20\,000\,000) \pmod{10^{10000}}$.

Calcular este valor término a término o mediante recursión memoizada resulta inviable debido a los $2 \times 10^7$ pasos.

Podemos resolverlo eficientemente mediante **exponenciación rápida de matrices** (o diagonalización). Representando la recurrencia en forma matricial:

$$\begin{pmatrix} m(n) \\ m(n-1) \\ m(n-2) \\ m(n-3) \end{pmatrix} = \begin{pmatrix} 21 & 301 & -9549 & 55692 \\ 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \end{pmatrix} \begin{pmatrix} m(n-1) \\ m(n-2) \\ m(n-3) \\ m(n-4) \end{pmatrix}$$

Para $n = 2 \times 10^7$, basta con elevar la matriz de transición a la potencia $n - 3$ módulo $10^{10000}$ usando exponenciación binaria ($\approx 25$ multiplicaciones de matrices de $4 \times 4$).

Una vez obtenido el valor de $m(n) \pmod{10^{10000}}$:
1. Se verifica su hash MD5 contra la clave de verificación provista.
2. Se deriva la clave AES/XOR calculando el SHA-256 del entero en formato de texto.
3. Se aplica XOR con `ENCRYPTED_FLAG` para recuperar la bandera en texto claro.

```bash
python3 - << 'EOF'
import sys
sys.set_int_max_str_digits(0)
import hashlib

ITERS = int(2e7)
MOD = 10**10000

def mat_mul(A, B, mod):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k]:
                for j in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def mat_pow(A, p, mod):
    n = len(A)
    res = [[int(i == j) for j in range(n)] for i in range(n)]
    base = A
    while p > 0:
        if p & 1:
            res = mat_mul(res, base, mod)
        base = mat_mul(base, base, mod)
        p >>= 1
    return res

T = [
    [21, 301, -9549, 55692],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0]
]

Tn = mat_pow(T, ITERS - 3, MOD)
v = [4, 3, 2, 1]
sol = sum(Tn[0][j] * v[j] for j in range(4)) % MOD

sol_str = str(sol)
key = hashlib.sha256(sol_str.encode()).digest()
ENCRYPTED_FLAG = bytes.fromhex("53c1beea6e427b3de1acf4834baed794f4bbd0dfe1d85f6a248ba4c12b")
flag = bytearray([char ^ key[i] for i, char in enumerate(ENCRYPTED_FLAG)]).decode()
print(flag)
EOF
```

## Notas adicionales
- En Python 3.11 en adelante, la conversión de enteros con más de 4300 dígitos a cadenas (`str(sol)`) genera un `ValueError`. Es necesario llamar a `sys.set_int_max_str_digits(0)` para deshabilitar el límite.
- Flag en formato: `academy{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/297
- Apoyo: https://en.wikipedia.org/wiki/Matrix_exponential
