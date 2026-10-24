# Cryptography — It's Not My Fault 1

## Descripción
> **Prompt oficial del reto:** "What do you mean RSA with CRT has an attack that's not a fault attack?"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** rkm0959

## Solución

El servicio remoto implementa un esquema RSA con optimización por Teorema Chino del Resto (RSA-CRT), donde:
- El módulo RSA es $N = p \cdot q$ de 1024 bits ($p$ y $q$ de 512 bits).
- El exponente CRT $d_p$ fue elegido deliberadamente pequeño: $d_p < 2^{20} = 1\,048\,576$.
- El exponente público $e$ satisface $e \cdot d_p \equiv 1 \pmod{p - 1}$.
- El servicio exige enviar la suma $p + q$ en un plazo límite para entregar la bandera.

### Vulnerabilidad: Ataque de Exponente CRT Pequeño (Small $d_p$)
Por el Pequeño Teorema de Fermat, para cualquier base $a$ coprima con $p$:
$$a^{p - 1} \equiv 1 \pmod p$$
Dado que $e \cdot d_p = 1 + k(p - 1)$:
$$a^{e \cdot d_p} = a^{1 + k(p - 1)} \equiv a \cdot (a^{p - 1})^k \equiv a \pmod p$$
Por lo tanto:
$$a^{e \cdot d_p} - a \equiv 0 \pmod p \implies p \mid (a^{e \cdot d_p} - a)$$

Tomando $a = 2$:
$$\gcd(2^{e \cdot d_p} - 2, N) = p$$

Dado que $d_p \le 2^{20} \approx 10^6$:
1. Definimos la base multiplicativa $B \equiv 2^e \pmod N$.
2. Para cada $d_p \in [1, 2^{20}]$, el término correspondiente es $x \equiv B^{d_p} \pmod N$, actualizable en cada paso mediante una multiplicación modular:
   $$x_{k+1} = (x_k \cdot B) \bmod N$$
3. Para optimizar, acumulamos el producto de $(x - 2) \bmod N$ en lotes (batch GCD) de $65\,536$ pasos y calculamos $\gcd(\text{producto}, N)$.
4. Al detectar $\gcd > 1$, se identifica el $d_p$ exacto en menos de un segundo, obteniendo el factor primo $p$.
5. Se calcula $q = N / p$ y se envía la suma $p + q$ al servicio remoto para obtener la bandera.

```bash
python3 - << 'EOF'
import socket, hashlib, itertools, string, re, gmpy2

HOST, PORT = "chatelaine.cylabacademy.net", 41706

s = socket.create_connection((HOST, PORT), timeout=60)
f = s.makefile('rw', buffering=1)

# PoW
pow_line = f.readline()
m = re.search(r'"([0-9]{5})".*?([0-9a-f]{6})', pow_line)
prefix, suffix = m.group(1), m.group(2)
for i in range(10_000_000):
    cand = prefix + str(i)
    if hashlib.md5(cand.encode()).hexdigest()[-6:] == suffix:
        f.write(cand + "\n")
        break

# Parse N and e
N = int(f.readline().split()[-1])
e = int(f.readline().split()[-1])

# Linear scan con batch GCD
N_mpz = gmpy2.mpz(N)
e_mpz = gmpy2.mpz(e)
base = gmpy2.powmod(2, e_mpz, N_mpz)
x = base
BATCH = 65536
prod = gmpy2.mpz(1)
p = None

for dp in range(1, (1 << 20) + 1):
    prod = (prod * (x - 2)) % N_mpz
    if dp % BATCH == 0:
        g = gmpy2.gcd(prod, N_mpz)
        if 1 < g < N_mpz:
            p = int(g)
            break
        prod = gmpy2.mpz(1)
    x = (x * base) % N_mpz

q = N // p
f.write(str(p + q) + "\n")
for _ in range(5):
    line = f.readline()
    if "academy{" in line or "picoCTF{" in line:
        print(line.strip())
        break
s.close()
EOF
```

## Notas adicionales
- Este vector demuestra que un exponente de descifrado CRT $d_p$ pequeño compromete la seguridad completa del sistema RSA, aun cuando el exponente público $e$ o el módulo $N$ sean de tamaño estándar.
- Flag en formato: `academy{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/123
- Apoyo: https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Fault-resistant_RSA-CRT
