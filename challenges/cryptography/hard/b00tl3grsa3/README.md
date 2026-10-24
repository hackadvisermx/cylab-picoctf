# Cryptography — b00tl3gRSA3

## Descripción
> **Prompt oficial del reto:** "Why use p and q when I can use more?"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** invisibility

## Solución
Al conectarse a la instancia del servicio vía `nc`, se entregan los valores:
- $c$: Criptograma.
- $n$: Módulo RSA.
- $e = 65537$: Exponente público estándar.

### Vulnerabilidad: Multi-prime RSA con factores primos pequeños
En RSA estándar, $n = p \cdot q$ se compone del producto de dos primos grandes de longitud similar (por ejemplo, dos primos de 1024 bits para un módulo de 2048 bits). En este reto, el módulo $n$ se construyó multiplicando numerosos factores primos pequeños ($n = \prod_{i=1}^{k} p_i$), donde cada $p_i$ tiene un tamaño de alrededor de 34 bits ($\approx 10^{10}$).

Debido a que los factores primos son muy pequeños, el algoritmo **Pollard's rho** descompone $n$ completamente en cuestión de segundos.

### Cálculo de la clave privada en Multi-prime RSA
Una vez obtenidos todos los factores primos $p_1, p_2, \dots, p_k$:
1. Se calcula la función de Carmichael generalizada $\lambda(n)$:
   $$\lambda(n) = \text{lcm}(p_1 - 1, p_2 - 1, \dots, p_k - 1)$$
2. Se obtiene el exponente privado $d$:
   $$d \equiv e^{-1} \pmod{\lambda(n)}$$
3. Se descifra el criptograma mediante exponenciación modular:
   $$m \equiv c^d \pmod n$$

### Script de resolución
```bash
python3 - << 'EOF'
import math
import random
from Crypto.Util.number import isPrime, long_to_bytes
from functools import reduce

def pollard_rho(n):
    if n % 2 == 0: return 2
    if isPrime(n): return n
    while True:
        c = random.randint(1, n - 1)
        f = lambda x: (pow(x, 2, n) + c) % n
        x = random.randint(1, n - 1)
        y = x
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d

def get_factors(n):
    factors = []
    stack = [n]
    while stack:
        cur = stack.pop()
        if cur == 1: continue
        if isPrime(cur):
            factors.append(cur)
        else:
            d = pollard_rho(cur)
            stack.append(d)
            stack.append(cur // d)
    return factors

def lcm(a, b):
    return (a * b) // math.gcd(a, b)

# Parámetros recibidos del servicio
c = int(...)
n = int(...)
e = 65537

# Factorización completa de n
factors = get_factors(n)

# Cálculo de lambda(n) y clave privada d
phi = reduce(lcm, [p - 1 for p in factors])
d = pow(e, -1, phi)

# Descifrado
m = pow(c, d, n)
flag = long_to_bytes(m).decode()
print(f"[+] Flag recuperada: {flag}")
EOF
```

El descifrado entrega la flag en formato `academy{...}`.

## Notas adicionales
- Aunque Multi-prime RSA es un esquema contemplado en los estándares (PKCS #1 v2.1) para acelerar el descifrado mediante el Teorema del Resto Chino (CRT), la seguridad del módulo decrece drásticamente si los factores individuales son tan pequeños que pueden factorizarse mediante algoritmos genéricos como Pollard's rho o ECM.

## Referencias
- Reto: https://learn.cylabacademy.org/library/78
- Apoyo: RFC 8017 (PKCS #1 v2.2) Sección 3.1 — Multi-prime RSA
