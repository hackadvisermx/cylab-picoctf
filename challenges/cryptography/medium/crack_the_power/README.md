# Cryptography — Crack the Power

## Descripción

> **Prompt oficial del reto:** "We received an encrypted message. The modulus is built from primes large enough that factoring them isn’t an option, at least not today. See if you can make sense of the numbers and reveal the flag.
> Download the message."

> **Hints:**
> 1. When certain values in the encryption setup are smaller than usual, it opens up unexpected shortcuts to recover the plaintext
> 2. Consider whether you can invert the encryption without factoring `n`.
> 3. Read more about Coppersmith's_attack [ here](https://en.wikipedia.org/wiki/Coppersmith's_attack )

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoMini by CMU-Africa
- **Autor:** Yahaya Meddy

## Solución

El reto entrega un archivo `message.txt` con los parámetros:
- Un módulo RSA $n$ de 4096 bits.
- Un exponente público $e = 20$.
- El texto cifrado $c$.

### Análisis y vulnerabilidad: Low Public Exponent sin reducción modular

En RSA, el texto cifrado se calcula como:
$$c \equiv m^e \pmod n$$

Si el mensaje en texto plano $m$ es suficientemente corto en comparación con el módulo $n$, se cumple que:
$$m^e < n$$

En este caso, nunca ocurre una reducción modular:
$$c = m^e \quad \text{en los enteros } \mathbb{Z}$$

Al comparar las longitudes de bits:
- $n$ tiene 4096 bits.
- $c$ tiene solo 3813 bits.

Dado que $c < n$, el cálculo nunca dio la vuelta al módulo. Por lo tanto, no es necesario factorizar $n$ ni aplicar ataques avanzados de Coppersmith: basta con calcular la **raíz $e$-ésima entera exacta** de $c$ sobre $\mathbb{Z}$.

### Script de resolución

```python
# Cargar parámetros
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

# Búsqueda binaria para la raíz e-ésima exacta sobre enteros
def integer_nth_root(val, n_root):
    low = 0
    high = 1 << ((val.bit_length() + n_root - 1) // n_root + 1)
    while low <= high:
        mid = (low + high) // 2
        p = mid ** n_root
        if p == val:
            return mid, True
        elif p < val:
            low = mid + 1
        else:
            high = mid - 1
    return high, False

m, exact = integer_nth_root(c, e)
assert exact, "La raíz debe ser exacta"

# Convertir el entero m a bytes
flag_bytes = m.to_bytes((m.bit_length() + 7) // 8, "big")
print(flag_bytes.decode(errors="replace"))
```

## Referencias

- [RSA (cryptosystem) — Attacks against RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Attacks_against_plain_RSA)
- [Coppersmith's Attack — Wikipedia](https://en.wikipedia.org/wiki/Coppersmith's_attack)
