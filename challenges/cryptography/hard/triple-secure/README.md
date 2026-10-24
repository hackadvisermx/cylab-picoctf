# Cryptography — triple-secure

## Descripción
> **Prompt oficial del reto:** "To get the flag, you must break RSA not once, but three times!"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoMini by redpwn
- **Autor:** Boolean

## Solución

Al examinar el script de cifrado `encrypt.py`, se generan tres primos de 1024 bits: $p, q, r$.
A partir de estos se construyen tres módulos RSA:
- $n_1 = p \cdot q$
- $n_2 = p \cdot r$
- $n_3 = q \cdot r$

El texto en claro se cifra consecutivamente a través de los tres módulos:
1. $c_1 = m^e \pmod{n_1}$
2. $c_2 = c_1^e \pmod{n_2}$
3. $c = c_2^e \pmod{n_3}$

### Vulnerabilidad: Factores Primos Compartidos
Cada par de módulos comparte exactamente un factor primo en común:
- $\gcd(n_1, n_2) = p$
- $\gcd(n_1, n_3) = q$
- $\gcd(n_2, n_3) = r$

El algoritmo de Euclides ($\gcd$) permite factorizar instantáneamente los tres módulos sin coste computacional significativo.

### Proceso de Descifrado
Se invierten las tres capas de cifrado en orden inverso:
1. **Capa 3 ($n_3 = q \cdot r$):**
   $$\phi(n_3) = (q - 1)(r - 1)$$
   $$d_3 \equiv e^{-1} \pmod{\phi(n_3)}$$
   $$c_2 \equiv c^{d_3} \pmod{n_3}$$
2. **Capa 2 ($n_2 = p \cdot r$):**
   $$\phi(n_2) = (p - 1)(r - 1)$$
   $$d_2 \equiv e^{-1} \pmod{\phi(n_2)}$$
   $$c_1 \equiv c_2^{d_2} \pmod{n_2}$$
3. **Capa 1 ($n_1 = p \cdot q$):**
   $$\phi(n_1) = (p - 1)(q - 1)$$
   $$d_1 \equiv e^{-1} \pmod{\phi(n_1)}$$
   $$m \equiv c_1^{d_1} \pmod{n_1}$$

```bash
python3 - << 'EOF'
import math
from Crypto.Util.number import long_to_bytes

with open('public-key.txt') as f:
    lines = [l.strip() for l in f if l.strip()]

data = {}
for l in lines:
    k, v = l.split(':')
    data[k.strip()] = int(v.strip())

n1, n2, n3 = data['n1'], data['n2'], data['n3']
e, c = data['e'], data['c']

p = math.gcd(n1, n2)
q = math.gcd(n1, n3)
r = math.gcd(n2, n3)

d3 = pow(e, -1, (q - 1) * (r - 1))
c2 = pow(c, d3, n3)

d2 = pow(e, -1, (p - 1) * (r - 1))
c1 = pow(c2, d2, n2)

d1 = pow(e, -1, (p - 1) * (q - 1))
m = pow(c1, d1, n1)

print(long_to_bytes(m).decode())
EOF
```

## Notas adicionales
- Este ataque resalta la importancia crítica de que ningún par de claves públicas RSA reutilice factores primos, ya que el cálculo del máximo común divisor rompe ambas claves inmediatamente.
- Flag en formato: `picoCTF{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/209
- Apoyo: https://en.wikipedia.org/wiki/Euclidean_algorithm
