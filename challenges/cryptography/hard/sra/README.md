# Cryptography — SRA

## Descripción
> **Prompt oficial del reto:** "I just recently learnt about the SRA public key cryptosystem... or wait, was it supposed to be RSA? Hmmm, I should probably check...
> 
> Connect to the program on our server: `nc <host> <port>`
> 
> Download the program: [chal.py](https://challenge-files.cylabacademy.net/library/4ed7cee044a0a6034082643ea47eb939295bf88af80be27e5f480bc7501eea59/chal.py)"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2023
- **Autor:** f0xtr0t

## Solución
El servicio implementa un sistema RSA con claves de 128 bits ($p$ y $q$) y exponente público estándar $e = 65537$.
El servidor genera una cadena aleatoria de 16 caracteres alfanuméricos (`pride`), la cifra como $c = m^e \pmod n$ y nos entrega el texto cifrado `anger` ($c$) y el exponente privado `envy` ($d$), pero omite el módulo $n = p \cdot q$. Si devolvemos el texto plano `pride`, el servidor nos entrega la flag.

Por la definición de la inversa modular en RSA:
$$e \cdot d \equiv 1 \pmod{\phi(n)} \implies e \cdot d - 1 = k \cdot (p - 1)(q - 1)$$

Dado que $(p - 1)$ divide $(p - 1)(q - 1)$, también divide a $e \cdot d - 1$.
1. Calculamos $val = e \cdot d - 1$ y encontramos su descomposición en factores primos usando `sympy.factorint`.
2. Generamos todos los divisores de $val$ que tengan una longitud de 128 bits.
3. Para cada divisor candidato $D$, comprobamos si $D + 1$ es primo. Estos forman el conjunto de posibles valores para $p$ y $q$.
4. Probamos pares de primos $(p, q)$ para reconstruir $n = p \cdot q$ y desciframos $m = c^d \pmod n$.
5. Aquel resultado que consista exactamente en 16 caracteres imprimibles alfanuméricos corresponde a `pride`.
6. Enviamos `pride` al servidor interactivo y recibimos la flag.

```python
import socket
import string
import sympy
from Crypto.Util.number import long_to_bytes

s = socket.socket()
s.connect((HOST, PORT))
f = s.makefile('rw', buffering=1)

anger = int(f.readline().split('=')[1].strip())
envy = int(f.readline().split('=')[1].strip())

e = 65537
d = envy
c = anger
val = e * d - 1

fac_dict = sympy.factorint(val)
primes_unique = list(fac_dict.keys())
counts = [fac_dict[p] for p in primes_unique]

candidates = set()
def gen_div(idx, current):
    if current.bit_length() > 128:
        return
    if idx == len(primes_unique):
        if current.bit_length() == 128 and sympy.isprime(current + 1):
            candidates.add(current + 1)
        return
    p_val, p_pow = primes_unique[idx], 1
    for _ in range(counts[idx] + 1):
        if (current * p_pow).bit_length() > 128:
            break
        gen_div(idx + 1, current * p_pow)
        p_pow *= p_val

gen_div(0, 1)
cand_list = list(candidates)
allowed = set((string.ascii_letters + string.digits).encode())

pride_found = None
for i in range(len(cand_list)):
    for j in range(i + 1, len(cand_list)):
        n_cand = cand_list[i] * cand_list[j]
        m_cand = pow(c, d, n_cand)
        b_cand = long_to_bytes(m_cand)
        if len(b_cand) == 16 and all(ch in allowed for ch in b_cand):
            pride_found = b_cand.decode()
            break
    if pride_found:
        break

f.readline() # prompt
f.write(pride_found + '\n')
print(f.read())
```

Al enviar `pride`, el servidor responde `Conquered!` y muestra la flag con formato `academy{...}`.

## Notas adicionales
El ataque funciona porque $p$ y $q$ son de solo 128 bits, por lo que $e \cdot d - 1$ tiene un tamaño de ~267 bits y sus factores primos son fácilmente computables en pocos segundos.

## Referencias
- Reto: https://learn.cylabacademy.org/library/379
- Factoring ed - 1 RSA attack: https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Faulty_key_generation
