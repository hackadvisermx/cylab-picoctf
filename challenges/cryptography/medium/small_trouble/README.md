# Cryptography — Small Trouble

## Descripción

> **Prompt oficial del reto:** "Everything seems secure; strong numbers, familiar parameters but something small might ruin it all. Can you recover the message?
> Download the message. And source code"

> **Hints:**
> 1. This might be a job for Boneh-Durfee.

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución

El script `encryption.py` genera un esquema RSA con primos de 1048 bits ($N = p \cdot q$ de 2096 bits) pero con un exponente privado $d$ muy pequeño:

```python
p = getPrime(1048)
q = getPrime(1048)
n = p * q
phi = (p - 1) * (q - 1)

# compute d
d = getPrime(256)

# Compute the public exponent
e = inverse(d, phi)
```

### Análisis: Ataques de exponente privado pequeño

Aunque la pista oficial sugiere el ataque de retículos de Boneh-Durfee ($d < N^{0.292}$), el tamaño del exponente privado es de solo 256 bits ($d < 2^{256}$), mientras que el límite clásico de **Wiener** es:
$$d < \frac{1}{3} N^{1/4} \approx \frac{1}{3} (2^{2096})^{1/4} = \frac{1}{3} 2^{524}$$

Como $2^{256} \ll 2^{524}$, el exponente privado $d$ se encuentra muy por debajo de la cota de Wiener. Por lo tanto, no es necesario recurrir a reducciones de retículos complejas de Boneh-Durfee: la fracción $\frac{k}{d}$ aparece directamente en los convergentes de la expansión en fracciones continuas de $\frac{e}{n}$.

Calculando los convergentes de $\frac{e}{n}$ y buscando la factorización válida de $n$ en las raíces de $x^2 - (n - \phi(n) + 1)x + n = 0$, se recupera el valor exacto de $d$ en menos de 0.1 segundos y se descifra la flag.

### Script de resolución

```python
import math
from Crypto.Util.number import long_to_bytes

with open("message.txt") as f:
    text = f.read()

params = {}
for line in text.strip().split("\n"):
    if "=" in line:
        k, v = line.split("=", 1)
        params[k.strip()] = int(v.strip())

n = params["n"]
e = params["e"]
c = params["c"]

# Fracciones continuas y convergentes de e/n
def continued_fraction(num, den):
    cf = []
    while den != 0:
        q = num // den
        cf.append(q)
        num, den = den, num - q * den
    return cf

def convergents(cf):
    convs = []
    h0, h1 = 0, 1
    k0, k1 = 1, 0
    for a in cf:
        hn = a * h1 + h0
        kn = a * k1 + k0
        convs.append((hn, kn))
        h0, h1 = h1, hn
        k0, k1 = k1, kn
    return convs

cf = continued_fraction(e, n)
convs = convergents(cf)

for k, d in convs:
    if k == 0 or (e * d - 1) % k != 0:
        continue
    phi = (e * d - 1) // k
    s_val = n - phi + 1
    discr = s_val * s_val - 4 * n
    if discr >= 0:
        r = math.isqrt(discr)
        if r * r == discr and (s_val - r) % 2 == 0:
            p = (s_val - r) // 2
            q = (s_val + r) // 2
            if p * q == n:
                m = pow(c, d, n)
                print("Flag:", long_to_bytes(m).decode())
                break
```

## Referencias

- [Wiener's Attack — Wikipedia](https://en.wikipedia.org/wiki/Wiener%27s_attack)
- [Boneh, Durfee (2000) - Cryptanalysis of RSA with Private Key d Less than N^0.292](https://link.springer.com/article/10.1007/s001450010016)
