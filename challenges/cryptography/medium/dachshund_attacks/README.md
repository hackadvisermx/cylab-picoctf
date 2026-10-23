# Cryptography — Dachshund Attacks

## Descripción

> **Prompt oficial del reto:** "What if $$d$$ is too small?"

> **Hints:**
> 1. What do you think about my pet? dachshund.jpg

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Sara

## Solución

El reto presenta un servicio por `nc` que entrega $e$, $n$ y $c$, con la premisa: *"What if $d$ is too small?"*. La pista muestra una imagen de un perro teckel / salchicha (**Dachshund** o *Wiener dog*), lo cual es una alusión directa al **ataque de Wiener** (*Wiener's Attack*).

### Fundamento teórico: Ataque de Wiener sobre RSA

El teorema de Wiener demuestra que si el exponente privado $d$ satisface:
$$d < \frac{1}{3} n^{1/4}$$
entonces la fracción $\frac{k}{d}$ es uno de los convergentes del desarrollo en fracciones continuas de $\frac{e}{n}$.

Para cada convergente $\frac{h_i}{k_i} = \frac{k}{d}$:
1. Se calcula una estimación de $\phi(n)$:
   $$\phi(n) = \frac{e \cdot d - 1}{k}$$
2. Como $n = p \cdot q$ y $\phi(n) = n - (p + q) + 1$, la suma $s = p + q = n - \phi(n) + 1$.
3. $p$ y $q$ son las raíces de la ecuación cuadrática:
   $$x^2 - s \cdot x + n = 0$$
   cuyo discriminante es $\Delta = s^2 - 4n$.
4. Si $\Delta$ es un cuadrado perfecto entero no negativo y $p \cdot q = n$, se ha encontrado la factorización de $n$ y el exponente privado $d$.
5. Se descifra la flag mediante $m \equiv c^d \pmod n$.

### Script de resolución

```python
import socket, re, math

# 1. Conexión al servicio on-demand
s = socket.create_connection(("<HOST>", <PUERTO>), timeout=10)
buf = b""
while b"c: " not in buf:
    chunk = s.recv(4096)
    if not chunk:
        break
    buf += chunk
s.close()

text = buf.decode(errors="replace")
e = int(re.search(r"e:\s*(\d+)", text).group(1))
n = int(re.search(r"n:\s*(\d+)", text).group(1))
c = int(re.search(r"c:\s*(\d+)", text).group(1))

# 2. Expansión en fracciones continuas de e/n
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

# 3. Evaluar convergentes para encontrar d
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
                flag = m.to_bytes((m.bit_length() + 7) // 8, "big")
                print(flag.decode())
                break
```

## Referencias

- [Wiener's Attack — Wikipedia](https://en.wikipedia.org/wiki/Wiener%27s_attack)
- [Michael J. Wiener (1990) - Cryptanalysis of Short RSA Secret Exponents](https://link.springer.com/article/10.1007/BF02252870)
