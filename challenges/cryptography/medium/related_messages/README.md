# Cryptography — Related Messages

## Descripción

> **Prompt oficial del reto:** "Oops! I have a typo in my first message so i sent it again! I used RSA twice so this is secure right?"

> **Hints:**
> 1. How are the two messages related?
> 2. Franklin Reiter _______ _______ attack.

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Philip Thayer

## Solución

El reto implementa el cifrado de dos mensajes afines con la misma clave pública RSA $(N, e)$:

```python
e = 0x11 # 17
ciphertext = pow(Message, e, N)
ciphertext2 = pow(Message_fixed, e, N)

print(ciphertext, ciphertext2)
print(Message - Message_fixed)
print(N)
```

En `output.txt` se nos entregan:
- $c_1 \equiv M^e \pmod N$
- $c_2 \equiv M_{\text{fixed}}^e \pmod N$
- $\Delta = M - M_{\text{fixed}} = -3 \implies M_{\text{fixed}} = M + 3$
- $N$ (módulo RSA de 2048 bits)
- $e = 17$

### Ataque de mensajes relacionados de Franklin-Reiter

Cuando dos textos planos satisfacen una relación polinomial conocida de grado pequeño $M_2 = f(M)$ y se cifran con el mismo módulo $N$ y exponente público $e$ pequeño, ambos satisfacen el sistema:
$$P_1(x) = x^e - c_1 \equiv 0 \pmod N$$
$$P_2(x) = (x - \Delta)^e - c_2 \equiv 0 \pmod N$$

Dado que $M$ es una raíz común de ambos polinomios módulo $N$, el polinomio lineal $(x - M)$ divide a ambos en $\mathbb{Z}_N[x]$:
$$\gcd(P_1(x), P_2(x)) = x - M \pmod N$$

Como $e = 17$ es pequeño, calcular el máximo común divisor de polinomios mediante el algoritmo de Euclides toma fracciones de segundo. El término constante del polinomio mónico resultante de grado 1 nos da directamente $-M \pmod N$.

Una vez recuperado $M$, el mensaje corregido es $M_{\text{fixed}} = M + 3$. Al convertir $M_{\text{fixed}}$ a bytes, se obtiene la flag completa (el error tipográfico original era una `z` en vez de la llave de cierre `}`).

### Script de resolución

```python
def poly_deg(p):
    while len(p) > 0 and p[-1] == 0:
        p.pop()
    return len(p) - 1

def poly_mul(p1, p2, N):
    res = [0] * (len(p1) + len(p2) - 1)
    for i, a in enumerate(p1):
        for j, b in enumerate(p2):
            res[i + j] = (res[i + j] + a * b) % N
    return res

def poly_mod(A, B, N):
    A = list(A)
    degB = poly_deg(B)
    lead_inv = pow(B[degB], -1, N)
    while poly_deg(A) >= degB:
        degA = poly_deg(A)
        factor = (A[degA] * lead_inv) % N
        shift = degA - degB
        for i in range(degB + 1):
            A[i + shift] = (A[i + shift] - factor * B[i]) % N
    while len(A) > 0 and A[-1] == 0:
        A.pop()
    return A

def poly_gcd(A, B, N):
    while B and poly_deg(B) >= 0:
        A, B = B, poly_mod(A, B, N)
    degA = poly_deg(A)
    if degA >= 0:
        inv = pow(A[degA], -1, N)
        A = [(c * inv) % N for c in A]
    return A

with open("output.txt") as f:
    lines = [l.strip() for l in f if l.strip()]

c1 = int(lines[0])
c2 = int(lines[1])
diff = int(lines[2])
N = int(lines[3])
e = 17

# P1(x) = x^17 - c1
P1 = [-c1 % N] + [0] * 16 + [1]

# P2(x) = (x - diff)^17 - c2
base = [-diff % N, 1]
P2 = [1]
cur = base
p = e
while p > 0:
    if p % 2 == 1:
        P2 = poly_mul(P2, cur, N)
    cur = poly_mul(cur, cur, N)
    p //= 2
P2[0] = (P2[0] - c2) % N

G = poly_gcd(P1, P2, N)
if poly_deg(G) == 1:
    M = (-G[0]) % N
    M_fixed = M - diff
    from Crypto.Util.number import long_to_bytes
    print("Flag:", long_to_bytes(M_fixed).decode())
```

## Referencias

- [Franklin-Reiter related-message attack — Wikipedia](https://en.wikipedia.org/wiki/Franklin%E2%80%93Reiter_related-message_attack)
- [Coppersmith, Franklin, Patarin, Reiter (1996) - Low-Exponent RSA with Related Messages](https://link.springer.com/chapter/10.1007/3-540-68697-5_1)
