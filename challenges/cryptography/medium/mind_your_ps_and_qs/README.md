# Cryptography — Mind your Ps and Qs

## Descripción

> **Prompt oficial del reto:** "In RSA, a small $$e$$ value can be problematic, but what about $$N$$? Can you decrypt this?
> values"

> **Hints:**
> 1. Bits are expensive, I used only a little bit over 100 to save money

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Sara

## Solución

El reto entrega un archivo `values` con los parámetros públicos de RSA y el texto cifrado:
- $c = 717608817902276639011922897702552744324264244069272484013719744328086856277690292$
- $n = 1368992139315019955067447961537607041364451719382349005056752379702694554965203011$
- $e = 65537$

### Análisis y vulnerabilidad: Módulo RSA de tamaño reducido

Al analizar el tamaño del módulo $n$:
$$\lfloor \log_2(n) \rfloor + 1 = 270 \text{ bits}$$

Un módulo de 270 bits está muy por debajo de los estándares criptográficos modernos (2048–4096 bits) y puede factorizarse en segundos usando tablas públicas como [FactorDB](http://factordb.com/) o algoritmos locales como ECM / Pollard's $\rho$.

Consultando FactorDB:
- $p = 2074606527507983503944226222695401999839$
- $q = 659880377875535146491994798968813949893149$

Con $p$ y $q$, se calcula la función totiente de Euler $\phi(n) = (p - 1)(q - 1)$, el exponente privado $d \equiv e^{-1} \pmod{\phi(n)}$, y se descifra $m \equiv c^d \pmod n$.

*(Nota: En la instancia de este reto en CyLab Academy, la representación en bytes del entero descifrado resulta invertida, por lo que se invierte la cadena para obtener el formato estándar `academy{...}`).*

### Script de resolución

```python
import urllib.request, json

n = 1368992139315019955067447961537607041364451719382349005056752379702694554965203011
c = 717608817902276639011922897702552744324264244069272484013719744328086856277690292
e = 65537

# Factorizar n vía FactorDB API
url = f"http://factordb.com/api?query={n}"
res = json.loads(urllib.request.urlopen(url).read())
factors = [int(f[0]) for f in res["factors"]]
p, q = factors[0], factors[1]

# Calcular clave privada y descifrar
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)

raw_bytes = m.to_bytes((m.bit_length() + 7) // 8, "big")
text = raw_bytes.decode(errors="replace").strip()

# Invertir si viene en little-endian / orden inverso
if text.endswith("{ymedaca"):
    flag = text[::-1]
else:
    flag = text

print(flag)
```

## Referencias

- [FactorDB](http://factordb.com/)
- [RSA Key Size Vulnerability — Wikipedia](https://en.wikipedia.org/wiki/Key_size#Asymmetric_algorithm_key_lengths)
