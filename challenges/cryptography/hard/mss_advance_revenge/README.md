# Cryptography — MSS_ADVANCE Revenge

## Descripción
> **Prompt oficial del reto:** "Last time we went easy on you. You'll never get the flag this time!
> 
> [chall.py](https://challenge-files.cylabacademy.net/library/6936c366a12516f20bd0ae04c6e560271c4811f57df2b60a41f5e7e24f29b95b/chall.py)
> 
> [output.txt](https://challenge-files.cylabacademy.net/library/6936c366a12516f20bd0ae04c6e560271c4811f57df2b60a41f5e7e24f29b95b/output.txt)"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2026
- **Autor:** Cayden (SuperBeetleGamer) Liao

## Solución
El reto genera una clave maestra de 256 bits y 29 coeficientes derivados iterativamente mediante SHA-256 (todos de 256 bits).
Con estos 30 coeficientes se evalúa un polinomio de grado 29 módulo un primo $p$ de 1024 bits en 20 puntos aleatorios $x_i$:
$$y_i \equiv \sum_{j=0}^{29} c_j x_i^{29-j} \pmod p$$

Se trata de un sistema subdeterminado de 20 ecuaciones con 30 incógnitas módulo $p$. Sin embargo, cada incógnita $c_j$ está acotada estrictamente por $0 \le c_j < 2^{256}$, mientras que $p \approx 2^{1024}$.
Las 20 ecuaciones aportan $20 \times 1024 = 20480$ bits de información frente a solo $30 \times 256 = 7680$ bits de entropía en las incógnitas, lo que garantiza que la solución de coeficientes pequeños es única.

Podemos modelar el problema como una búsqueda del vector más corto (SVP/CVP) mediante la técnica de incrustación de Kannan (Kannan's Embedding Technique) en una red de dimensión $51 \times 51$:
1. Las primeras 30 filas representan las variables $c_j$ escalando su contribución modular con un peso grande $K$.
2. Las siguientes 20 filas representan múltiplos de $p$ escalados por $K$.
3. La última fila representa los términos constantes $-y_i \cdot K$ y un peso objetivo $W = 2^{256}$.

Al aplicar reducción de redes con el algoritmo LLL (implementado eficientemente mediante `flint.fmpz_mat.lll`), el vector más corto de la red revela directamente los coeficientes originales $c_0, \dots, c_{29}$.
Con $c_0 = \text{MASTER\_KEY}$, se descifra el texto cifrado con AES-CBC.

```python
import flint
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib

with open('output.txt') as f:
    text = f.read()

globs = {}
exec(text, globs)
p = globs['p']
pairs = globs['pairs']
enc_flag = globs['enc_flag']

n_vars = 30
n_eqs = len(pairs)
dim = n_vars + n_eqs + 1

A = [[pow(pairs[i][0], 29 - j, p) for j in range(n_vars)] for i in range(n_eqs)]
K = 2**300
W = 2**256

mat = [[0]*dim for _ in range(dim)]
for j in range(n_vars):
    mat[j][j] = 1
    for i in range(n_eqs):
        mat[j][n_vars + i] = A[i][j] * K

for i in range(n_eqs):
    mat[n_vars + i][n_vars + i] = p * K

for i in range(n_eqs):
    mat[dim - 1][n_vars + i] = (p - pairs[i][1]) * K
mat[dim - 1][dim - 1] = W

flat = [val for row in mat for val in row]
fmat = flint.fmpz_mat(dim, dim, flat)
lll_mat = fmat.lll()

for r in range(dim):
    row_vals = [int(lll_mat[r, c]) for c in range(dim)]
    if abs(row_vals[-1]) == W:
        sgn = 1 if row_vals[-1] == W else -1
        c_cand = [row_vals[j] * sgn for j in range(n_vars)]
        if all(0 <= val < 2**256 for val in c_cand):
            master_key = long_to_bytes(c_cand[0])
            cipher = AES.new(master_key, AES.MODE_CBC, bytes.fromhex(enc_flag[0]))
            print(cipher.decrypt(bytes.fromhex(enc_flag[1])))
            break
```

Al descifrar se obtiene la flag con formato `academy{...}`.

## Notas adicionales
La reducción de redes LLL converge en apenas unos segundos gracias al uso de FLINT en C, resolviendo eficazmente el problema CVP sin requerir fuerza bruta.

## Referencias
- Reto: https://learn.cylabacademy.org/library/709
- Kannan's Embedding Technique: https://en.wikipedia.org/wiki/Closest_vector_problem
- FLINT (Fast Library for Number Theory): https://flintlib.org
