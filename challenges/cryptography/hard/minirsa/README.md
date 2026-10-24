# Cryptography — miniRSA

## Descripción
> **Prompt oficial del reto:** "Let's decrypt this. Can you decrypt this ciphertext? Something seems a bit small."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** speeeday/Danny

## Solución
El reto proporciona los parámetros de un cifrado RSA:
- Módulo público $N$ de 2048 bits.
- Exponente público $e = 3$.
- Criptograma $c$.

### Vulnerabilidad: Exponente público pequeño sin reducción modular
El cifrado RSA calcula $c = m^e \pmod N$. Cuando el exponente público es extremadamente pequeño ($e = 3$) y el mensaje $m$ no tiene un relleno (padding) que expanda su longitud hasta aproximarse a $N$, ocurre que:
$$m^3 < N \implies c = m^3 \quad (\text{en } \mathbb{Z})$$

Al no haberse producido reducción modular (o si se produjo con un múltiplo $k$ pequeño tal que $m^3 = c + k \cdot N$), es posible recuperar el texto plano $m$ simplemente calculando la raíz cúbica entera directa de $c$:
$$m = \lfloor \sqrt[3]{c} \rfloor$$

### Pasos de ejecución
Usando la librería `gmpy2` en Python para realizar operaciones aritméticas de precisión arbitraria:

```bash
python3 - << 'EOF'
import gmpy2
from Crypto.Util.number import long_to_bytes

with open("ciphertext") as f:
    lines = f.read().strip().split("\n")

N = int(lines[0].split(":")[1])
e = int(lines[1].split(":")[1])
c = int(lines[2].split(":")[1])

# Intentar raíz cúbica directa (k = 0)
root, exact = gmpy2.iroot(c, 3)
if exact:
    flag = long_to_bytes(int(root)).decode()
    print(f"[+] Flag recuperada: {flag}")
else:
    # Si m^3 > N pero k es pequeño
    for k in range(1, 100000):
        val = c + k * N
        root, exact = gmpy2.iroot(val, 3)
        if exact:
            flag = long_to_bytes(int(root)).decode()
            print(f"[+] Flag recuperada (k={k}): {flag}")
            break
EOF
```

La raíz cúbica entera es exacta en $k = 0$, revelando directamente el texto plano en formato `academy{...}`.

## Notas adicionales
- Para evitar este ataque (ataque de Coppersmith / raíz directa), los esquemas modernos de RSA exigen el uso de esquemas de relleno probabilísticos estandarizados como OAEP (Optimal Asymmetric Encryption Padding) y valores estándar de $e$ como $65537$ ($2^{16}+1$).

## Referencias
- Reto: https://learn.cylabacademy.org/library/73
- Apoyo: Dan Boneh, *Twenty Years of Attacks on the RSA Cryptosystem* (Sección sobre Small Public Exponents)
