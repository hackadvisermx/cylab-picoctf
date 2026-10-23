# It's Not My Fault 2

**Categoría:** Criptografía — Medio  
**Evento:** picoCTF 2021  
**Autor:** rkm0959  
**Puntos:** 400  

## Descripción

> What do you mean RSA with CRT has an attack that's not a fault attack?

Se conecta al servidor con:
```
nc <host> <puerto>
```

El servidor proporciona un archivo `not_my_fault_again.py` que describe el esquema.

## Análisis del servidor

El servidor ejecuta el siguiente esquema:

1. **PoW (Proof of Work):** Hay que encontrar una cadena que empiece con 5 dígitos específicos cuyo MD5 termine en 6 dígitos hexadecimales dados.

2. **Generación de claves RSA-CRT:**
   - Se generan primos `p`, `q` de 512 bits con `GCD(p-1, q-1) = 2`.
   - `n = p * q` (módulo 1024-bit) se publica.

3. **Clue (exponente público):**
   - Se genera `d_p = random.randint(1, 1 << 36)` — exponente CRT *pequeño* (máximo 36 bits).
   - Se genera `d_q` aleatorio de tamaño completo.
   - `d = CRT(d_p, p-1, d_q, q-1)` — exponente privado completo.
   - `e = inverse(d, (p-1)*(q-1))` — exponente público.
   - El servidor publica `n` y `e`.

4. **Objetivo:** Responder con `p + q` en menos de 15 minutos.

## Ataque: BSGS con evaluación multipunto de polinomios

El título dice "It's Not My Fault 2": el parte 1 era el ataque de fallas de Bellcore. Este es un ataque **diferente** sobre RSA-CRT con exponente pequeño.

### Fundamento matemático

Dado que `e * d_p ≡ 1 (mod p-1)`, por el Pequeño Teorema de Fermat:
```
r^(e*d_p) ≡ r (mod p)   para cualquier r coprimo con p
```

Entonces `p | gcd(r^(e*d_p) - r, n)`.

Como `d_p ≤ 2^36`, usamos **Baby-Step Giant-Step (BSGS)** para encontrar `d_p`.

### BSGS + Polinomio

Sea `L = 2^18` (raíz cuadrada de `2^36`). Descomponemos `d_p = a + b*L` con `0 ≤ a < L` y `0 ≤ b ≤ L`.

- **Baby steps (raíces):** `root_l = r^(1-e*l) mod n` para `l = 1..L-1`
- **Giant steps (puntos):** `y_b = r^(e*b*L) mod n` para `b = 0..L`

Construimos el polinomio:
```
Q(x) = ∏_{l=1}^{L-1} (x - root_l)   sobre Z/nZ
```

Si `d_p = l + b*L`, entonces `root_l ≡ y_b (mod p)`, por lo que `p | Q(y_b)`, y:
```
gcd(Q(y_b), n) = p
```

### Algoritmo eficiente

1. **Calcular raíces:** `root_l = r * (r^{-e})^l mod n` — secuencia geométrica, O(L).

2. **Construir Q(x):** Árbol de subproductos (divide y vencerás), O(L log² L).

3. **Evaluar en todos los puntos:** Evaluación multipunto rápida, O(L log² L).

4. **Calcular GCDs:** Para cada `Q(y_b)`, computar `gcd(Q(y_b), n)`.

### Implementación

Se usa la librería **python-flint** que provee `fmpz_mod_poly_ctx` (polinomios sobre Z/nZ) con evaluación multipunto incorporada (`multipoint_evaluate`).

**Tiempos de ejecución:**
- Raíces baby steps: ~1 segundo
- Construcción del polinomio (grado 2^18): ~7 segundos
- Giant steps: ~1 segundo
- Evaluación multipunto: ~50 segundos
- **Total: ~60 segundos** (dentro del límite de 15 minutos)

## Script de solución

El script completo se encuentra en:
`cylab-picoctf/tmp/solve_fault2.py`

Pasos principales:
```python
from flint import fmpz_mod_poly_ctx, fmpz
from math import gcd

m, L = 2, 1 << 18
ctx = fmpz_mod_poly_ctx(n)
me_inv = pow(pow(m, e, n), -1, n)

# Baby steps (raíces del polinomio)
cur = m * me_inv % n
roots = [fmpz(cur := cur * me_inv % n) for _ in range(L-1)]
# Corregir: la primera iteración ya usa el valor inicial
# Ver script completo para la implementación correcta

# Construir polinomio
polys = [ctx([int(n - r), 1]) for r in roots]
# ...divide y vencerás para construir Q...

# Evaluación multipunto
T = pow(m, e * L, n)
giant_pts = [fmpz(cur := cur * T % n) for b in range(L+1)]
values = Q.multipoint_evaluate(giant_pts)

# Encontrar p
for b, val in enumerate(values):
    g = gcd(int(val), n)
    if 1 < g < n:
        p, q = g, n // g
        break
```

## Referencias

- Galbraith, "Mathematics of Public Key Cryptography", pp. 529 — ataque BSGS con árbol de subproductos
- Bleichenbacher & May (2006): "New Attacks on RSA with Small Secret CRT-Exponents"
- [CTFtime writeup](https://ctftime.org/writeup/27022)
