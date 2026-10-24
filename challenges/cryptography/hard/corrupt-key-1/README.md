# Cryptography — corrupt-key-1

## Descripción
> **Prompt oficial del reto:** "How to fix corrupted key???"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoMini by redpwn
- **Autor:** Tux

## Solución

El reto entrega una clave privada RSA corrupta codificada en formato PEM (`private.key`) y un archivo cifrado (`msg.enc`).

Al parsear la estructura ASN.1/DER del archivo PEM:
1. El módulo público $N$ de 1024 bits y el exponente público $e = 65537$ están intactos.
2. Los campos $d, q, dP, dQ, qInv$ fueron sobrescritos por ceros.
3. Para el factor primo $p$ (de 512 bits), los 256 bits más significativos (MSBs) están intactos, mientras que los 256 bits menos significativos fueron reemplazados por ceros.

### Ataque de Coppersmith (Known High Bits of $p$)
Cuando se conocen al menos la mitad de los bits de uno de los factores primos de un módulo RSA ($n = p \cdot q$), el teorema de Coppersmith garantiza que se pueden recuperar los bits restantes en tiempo polinomial formulando el problema como la búsqueda de raíces pequeñas de un polinomio mónico:

$$f(x) = p_{\text{known}} + x \pmod p$$

Utilizando reducción de reticulados (algoritmo LLL / método de Coppersmith para raíces univariadas en SageMath), se recupera la raíz entera $x_0$, obteniendo el valor completo de $p$:
$$p = 12098520864598198757294135341465388062087431109285224283440314414683283061468500249596026217234382854875647811812632201834942205849073893715844547051090363$$

Una vez obtenido $p$:
1. $q = N / p$.
2. $\phi(N) = (p - 1)(q - 1)$.
3. $d \equiv e^{-1} \pmod{\phi(N)}$.
4. Se descifra $m \equiv c^d \pmod N$ y se extrae el contenido del relleno PKCS#1 v1.5 para obtener la bandera.

```bash
python3 - << 'EOF'
from Crypto.Util.number import bytes_to_long, long_to_bytes
import base64

def parse_der(raw):
    idx = 0
    if raw[idx] == 0x30:
        idx += 1
        idx += (raw[idx] & 0x7f) + 1 if (raw[idx] & 0x80) else 1
    ints = []
    while idx < len(raw):
        idx += 1
        l = raw[idx]
        idx += 1
        if l & 0x80:
            nb = l & 0x7f
            l = int.from_bytes(raw[idx:idx+nb], 'big')
            idx += nb
        ints.append(int.from_bytes(raw[idx:idx+l], 'big'))
        idx += l
    return ints

with open('private.key') as f:
    raw = base64.b64decode(''.join(l.strip() for l in f if not l.startswith('---')))

ints = parse_der(raw)
n = ints[1]
e = ints[2]

# Primo recuperado vía Coppersmith LLL
p = 12098520864598198757294135341465388062087431109285224283440314414683283061468500249596026217234382854875647811812632201834942205849073893715844547051090363
q = n // p
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

with open('msg.enc', 'rb') as f:
    c = bytes_to_long(f.read())

m = pow(c, d, n)
decrypted = long_to_bytes(m)
print(decrypted[decrypted.index(b'picoCTF{'):].decode())
EOF
```

## Notas adicionales
- El mensaje utiliza relleno estándar RSA PKCS#1 v1.5 (`0x00 0x02 ... 0x00 [mensaje]`), por lo que la bandera se encuentra tras el byte nulo delimitador.
- Flag en formato: `picoCTF{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/207
- Apoyo: https://en.wikipedia.org/wiki/Coppersmith%27s_attack
