# Cryptography — Sum-O-Primes

## Descripción
> **Prompt oficial del reto:** "We have so much faith in RSA we give you not just the product of the primes, but their sum as well!"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2022
- **Autor:** Joshua Inscoe

## Solución

En el cifrado RSA estándar, la seguridad radica en la dificultad de factorizar el módulo $n = p \cdot q$ cuando $p$ y $q$ son números primos grandes y secretos.

En este reto, el generador proporciona tanto el producto $n = p \cdot q$ como la suma $x = p + q$. Conociendo la suma y el producto de dos números desconocidos, podemos plantear una ecuación cuadrática o usar la identidad algebraica:

$$(p - q)^2 = (p + q)^2 - 4pq = x^2 - 4n$$

Definiendo $\Delta = \sqrt{x^2 - 4n}$:
$$p = \frac{x + \Delta}{2}$$
$$q = \frac{x - \Delta}{2}$$

Una vez obtenidos $p$ y $q$:
1. Se calcula la función totiente de Euler $\phi(n) = (p - 1)(q - 1)$.
2. Se computa el exponente privado $d = e^{-1} \pmod{\phi(n)}$.
3. Se descifra el texto cifrado mediante $m = c^d \pmod{n}$.
4. Se convierte el entero $m$ a bytes para obtener la bandera.

```bash
python3 - << 'EOF'
import gmpy2
from Crypto.Util.number import long_to_bytes

with open('output.txt') as f:
    lines = f.read().strip().split('\n')
    x = int(lines[0].split('=')[1].strip(), 16)
    n = int(lines[1].split('=')[1].strip(), 16)
    c = int(lines[2].split('=')[1].strip(), 16)

delta2 = x * x - 4 * n
delta = gmpy2.isqrt(delta2)
p = (x + delta) // 2
q = (x - delta) // 2

phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)
m = pow(c, d, n)
print(long_to_bytes(m).decode())
EOF
```

## Notas adicionales
- Dado que $x^2 - 4n$ es un cuadrado perfecto exacto, la raíz cuadrada entera se computa instantáneamente con `gmpy2.isqrt` o `math.isqrt`.
- Flag en formato: `academy{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/310
- Apoyo: https://en.wikipedia.org/wiki/Vieta%27s_formulas
