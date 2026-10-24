# Cryptography — Very Smooth

## Descripción
> **Prompt oficial del reto:** "Forget safe primes... Here, we like to live life dangerously... >:)
> - gen.py
> - output.txt"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2022
- **Autor:** Joshua Inscoe

## Solución
El reto implementa RSA con dos primos grandes $p$ y $q$ generados usando números "smooth" donde $p - 1$ y $q - 1$ son productos de primos pequeños (de a lo sumo 16 y 17 bits).

Dado que $p - 1$ es $B$-smooth con $B \approx 2^{17}$, el algoritmo $p-1$ de Pollard es sumamente eficiente para factorizar $n = p \cdot q$.
Computamos de manera incremental:
$$a \leftarrow a^k \pmod n$$
para cada primo $p_i \le B$, verificando en cada paso $\gcd(a - 1, n)$. Tan pronto como $p - 1$ divide el exponente acumulado antes que $q - 1$, obtenemos $p = \gcd(a - 1, n)$. Una vez factorizado $n$, derivamos $d = e^{-1} \pmod{(p-1)(q-1)}$ y desciframos el texto cifrado $c$.

```python
import math
from Crypto.Util.number import long_to_bytes

with open('output.txt') as f:
    lines = f.read().strip().split('\n')
    n = int(lines[0].split('=')[1].strip(), 16)
    c = int(lines[1].split('=')[1].strip(), 16)

def sieve(n):
    primes = []
    is_p = [True] * (n + 1)
    for p in range(2, n + 1):
        if is_p[p]:
            primes.append(p)
            for i in range(p * p, n + 1, p):
                is_p[i] = False
    return primes

primes = sieve(2**17 + 1000)
a = 2
for p in primes:
    k = p
    while k * p <= 2**17 + 1000:
        k *= p
    a = pow(a, k, n)
    g = math.gcd(a - 1, n)
    if 1 < g < n:
        p_val = g
        q_val = n // g
        e = 0x10001
        phi = (p_val - 1) * (q_val - 1)
        d = pow(e, -1, phi)
        m = pow(c, d, n)
        print('FLAG:', long_to_bytes(m).decode())
        break
```

Al ejecutar el script de resolución se obtiene la flag con formato `academy{...}`.

## Notas adicionales
La vulnerabilidad radica en que no se emplearon "safe primes" (donde $(p-1)/2$ es también un número primo grande), permitiendo la descomposición inmediata mediante el algoritmo de Pollard $p-1$.

## Referencias
- Reto: https://learn.cylabacademy.org/library/315
- Pollard's p - 1 algorithm: https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm
