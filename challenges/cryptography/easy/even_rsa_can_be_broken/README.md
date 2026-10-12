# Cryptography — EVEN RSA CAN BE BROKEN???

## Descripción
> **Prompt oficial del reto:** "This service provides you an encrypted flag. Can you decrypt it with just N & e? Connect to the program with netcat: `nc chatelaine.cylabacademy.net <puerto>`. The program's source code can be downloaded here."
>
> **Hints:**
> 1. How much do we trust randomness?
> 2. Notice anything interesting about N?
> 3. Try comparing N across multiple requests

- **Categoría:** Cryptography
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2025
- **Autor:** Michael Crotty

## Solución
El servicio entrega `N`, `e` y el flag cifrado por RSA. El truco está en el nombre ("EVEN RSA") y el hint 2: **N es par**. Si N es par, uno de sus factores primos es **2**, así que la factorización es trivial:

- `p = 2`, `q = N // 2`
- `phi = (p-1)*(q-1) = q - 1`
- `d = e^{-1} mod phi`
- `m = c^d mod N` → bytes → flag

```python
p=2; q=N//2
phi=(p-1)*(q-1)
d=pow(e,-1,phi)
m=pow(c,d,N)
print(m.to_bytes((m.bit_length()+7)//8,'big'))
# academy{tw0_1$_pr!m3207f407f}
```

## Notas adicionales
- RSA es seguro solo si N = p·q con p, q primos grandes y secretos. Si N es par (p=2), factorizarlo es instantáneo y toda la "seguridad" se cae.
- Los hints apuntan a que la generación de primos usa mala aleatoriedad, produciendo un N par en cada instancia.

## Referencias
- Reto: https://learn.cylabacademy.org/library/470
