# Cryptography — NSA Backdoor

## Descripción
> **Prompt oficial del reto:** "I heard someone has been sneakily installing backdoors in open-source implementations of Diffie-Hellman... I wonder who it could be... ;)"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2022
- **Autor:** Joshua Inscoe

## Solución

El reto presenta una implementación con puerta trasera de Diffie-Hellman en la cual:
1. El módulo $n = p \cdot q$ es un número compuesto producto de dos primos de 1024 bits.
2. Ambos primos $p$ y $q$ fueron generados deliberadamente para que $p - 1$ y $q - 1$ sean números $B$-smooth (todos sus factores primos son pequeños, $\le 2^{16}$ o $\le 2^{17}$).
3. El texto cifrado corresponde a $c \equiv 3^{\text{FLAG}} \pmod n$.

La recuperación de la bandera requiere dos etapas criptoanalíticas:

### 1. Factorización mediante Pollard's $p-1$
Dado que $p - 1$ está compuesto enteramente por factores primos menores a $65536$, la prueba de divisibilidad de Pollard $p-1$ encuentra un factor de $n$ de forma casi instantánea al computar:
$$a \equiv 2^{\prod q_i^{e_i}} \pmod n, \quad \gcd(a - 1, n) = p$$

### 2. Logaritmo Discreto mediante Pohlig-Hellman
Conocido $p$, reducimos el problema al logaritmo discreto en el campo finito $\mathbb{F}_p$:
$$3^{\text{FLAG}} \equiv c \pmod p$$
Dado que el orden del grupo multiplicativo es $p - 1 = \prod r_i$ con factores primos $r_i \le 65536$:
1. Proyectamos la relación a cada subgrupo cíclico de orden primo $r_i$:
   $$g_{r_i} = 3^{(p-1)/r_i} \pmod p, \quad h_{r_i} = c^{(p-1)/r_i} \pmod p$$
2. Resolvemos $g_{r_i}^{x_i} \equiv h_{r_i} \pmod p$ utilizando el algoritmo Baby-step Giant-step (BSGS) en $\mathcal{O}(\sqrt{r_i}) \le 256$ pasos.
3. Recombinamos los residuos $x_i \pmod{r_i}$ mediante el Teorema Chino del Resto (CRT) para reconstruir $\text{FLAG} \pmod{p - 1}$.

```bash
python3 - << 'EOF'
import gmpy2
from Crypto.Util.number import long_to_bytes
from sympy.ntheory import factorint
from sympy.ntheory.modular import crt

with open('output.txt') as f:
    lines = f.read().strip().split('\n')
    n = gmpy2.mpz(lines[0].split('=')[1].strip(), 16)
    c = gmpy2.mpz(lines[1].split('=')[1].strip(), 16)

# Factorización con Pollard p-1
a = gmpy2.mpz(2)
B = 150000
p = None
for prime in range(2, B):
    if gmpy2.is_prime(prime):
        k = prime
        while k * prime <= B:
            k *= prime
        a = gmpy2.powmod(a, k, n)
        g = gmpy2.gcd(a - 1, n)
        if 1 < g < n:
            p = g
            break

# Factores de p-1
fp = factorint(int(p - 1), limit=150000)

def bsgs(g, h, p, r):
    m = int(gmpy2.isqrt(r)) + 1
    table = {}
    cur = gmpy2.mpz(1)
    for j in range(m):
        table[cur] = j
        cur = (cur * g) % p
    gm = gmpy2.invert(pow(g, m, p), p)
    cur = gmpy2.mpz(h)
    for i in range(m):
        if cur in table:
            return (i * m + table[cur]) % r
        cur = (cur * gm) % p
    return None

remainders, moduli = [], []
for r in fp:
    e = (p - 1) // r
    gr = pow(3, e, p)
    hr = pow(c, e, p)
    xr = bsgs(gr, hr, p, r)
    remainders.append(int(xr))
    moduli.append(int(r))

x_p, _ = crt(moduli, remainders)
flag = long_to_bytes(int(x_p)).decode()
print(flag)
EOF
```

## Notas adicionales
- Este ataque reproduce el vector de vulnerabilidad descubierto en backdoors de generadores de parámetros criptográficos débiles.
- Flag en formato: `academy{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/283
- Apoyo: https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm
