# john_pollard

**Categoría:** Cryptography — Medium  
**Plataforma:** CyLab picoCTF Academy (ID 6)  
**Año:** picoCTF 2019  
**Referencia:** https://learn.cylabacademy.org/library/6

---

## Descripción

> "Sometimes RSA certificates are breakable."

Se entrega un certificado X.509 (PEM) con una clave pública RSA. El módulo N = p × q fue generado con primos lo suficientemente pequeños como para ser factorizados. El reto alude directamente al **algoritmo de Pollard's p−1**, una técnica de factorización que explota cuando p−1 es *B-smooth* (todos sus factores primos son pequeños).

---

## Hints oficiales

- "The flag is in the format `academy{p,q}`"
- "Try swapping p and q if it does not work"

---

## Solución

### 1. Examinar el certificado

```bash
openssl x509 -in cert -noout -text
```

Salida relevante:

```
Public Key Algorithm: rsaEncryption
    Public-Key: (53 bit)
    Modulus: 4966306421059967 (0x11a4d45212b17f)
    Exponent: 65537 (0x10001)
```

El módulo N tiene sólo **53 bits**, un tamaño completamente inseguro para RSA (los módulos modernos tienen al menos 2048 bits).

### 2. Factorizar N

Con N tan pequeño, la división por prueba simple es suficiente. En Python:

```python
N = 4966306421059967

def factorize(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

factors = sorted(factorize(N))
p, q = factors[0], factors[1]
print(f"p = {p}")
print(f"q = {q}")
```

Resultado:

```
p = 67867967
q = 73176001
```

Verificación: 67867967 × 73176001 = 4966306421059967 ✓

### 3. Análisis de suavidad (Pollard's p−1)

El nombre del reto hace referencia al algoritmo **Pollard's p−1** de factorización, que funciona cuando p−1 tiene únicamente factores primos pequeños (*B-smooth*):

- `p − 1 = 67867966 = 2 × 1301 × 26083` → factor primo máximo: **26083**
- `q − 1 = 73176000 = 2⁶ × 3 × 5³ × 3049` → factor primo máximo: **3049**

Ambos valores de p−1 y q−1 son B-smooth con B relativamente pequeño, lo que los hace vulnerables al algoritmo de Pollard's p−1 con un límite B ≥ 26083.

### 4. Construir la flag

El segundo hint indica "Try swapping p and q if it does not work". CyLab espera el **mayor primo primero** (q,p):

```
q = 73176001  (el mayor)
p = 67867967  (el menor)
```

---

## Notas adicionales

- El certificado usa `md2WithRSAEncryption` como algoritmo de firma, otro indicador de obsolescencia (MD2 fue depreciado en 2011).
- Las fechas de validez del certificado son inválidas (`Not After` es anterior a `Not Before`), señal de que fue fabricado deliberadamente para el reto.
- Para módulos RSA más grandes donde la factorización directa no es viable, la búsqueda en **FactorDB** (https://factordb.com) es el primer paso recomendado antes de intentar algoritmos propios.

---

## Referencias

- [Pollard's p−1 algorithm — Wikipedia](https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm)
- [FactorDB](https://factordb.com)
- [OpenSSL x509 manual](https://www.openssl.org/docs/man1.1.1/man1/x509.html)
- https://learn.cylabacademy.org/library/6
