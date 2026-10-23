# Cryptography — ClusterRSA

## Descripción

> **Prompt oficial del reto:** "A message has been encrypted using RSA, but this time something feels... more crowded than usual. Can you decrypt it?
> Download the message."

> **Hints:**
> 1. RSA usually means two primes... but what if someone got greedy?
> 2. Prime factors decomposition

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución

El reto entrega un archivo `message.txt` con los parámetros:
- Módulo $n = 8749002899132047699790752490331099938058737706735201354674975134719667510377522805717156720453193651$ (aprox. 332 bits).
- Exponente público $e = 65537$.
- Texto cifrado $ct = 4944656015192104544447685273211645817619034785653092117903505126209101571061420351868516667543242371$.

### Análisis: Multi-prime RSA con factores agrupados (*Cluster*)

El nombre *ClusterRSA* y la pista *"RSA usually means two primes... but what if someone got greedy?"* indican que $n$ no está compuesto por 2 primos, sino por múltiples factores primos que además están muy cercanos entre sí (*clustered* alrededor de $n^{1/4}$).

Consultando FactorDB o factorizando localmente, $n$ se descompone en 4 factores primos de 25 dígitos (aprox. 83 bits cada uno):
- $p_1 = 9671406556917033397931773$
- $p_2 = 9671406556917033398314601$
- $p_3 = 9671406556917033398439721$
- $p_4 = 9671406556917033398454847$

Verificamos que $n = p_1 \cdot p_2 \cdot p_3 \cdot p_4$.

### Descifrado

Para RSA con múltiples factores primos $p_1, p_2, \dots, p_k$:
$$\phi(n) = \prod_{i=1}^k (p_i - 1) = (p_1 - 1)(p_2 - 1)(p_3 - 1)(p_4 - 1)$$

Calculamos el exponente privado $d \equiv e^{-1} \pmod{\phi(n)}$ y desciframos:
$$m \equiv ct^d \pmod n$$

### Script de resolución

```python
import json, urllib.request

# Parámetros del reto
n = 8749002899132047699790752490331099938058737706735201354674975134719667510377522805717156720453193651
e = 65537
ct = 4944656015192104544447685273211645817619034785653092117903505126209101571061420351868516667543242371

# Factorización de n (vía FactorDB)
url = f"http://factordb.com/api?query={n}"
res = json.loads(urllib.request.urlopen(url).read())
factors = [int(f[0]) for f in res["factors"]]

# Totiente de Euler generalizado
phi = 1
for p in factors:
    phi *= (p - 1)

# Inverso modular y descifrado
d = pow(e, -1, phi)
m = pow(ct, d, n)

flag = m.to_bytes((m.bit_length() + 7) // 8, "big")
print(flag.decode())
```

## Referencias

- [Multi-prime RSA — Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Multi-prime_RSA)
- [FactorDB](http://factordb.com/)
