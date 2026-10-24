# Cryptography — corrupt-key-2

## Descripción
> **Prompt oficial del reto:** "Key corrupted again..."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoMini by redpwn
- **Autor:** Tux

## Solución

Al igual que en `corrupt-key-1`, se nos proporciona una clave RSA privada dañada (`private.key`) y un mensaje cifrado (`msg.enc`).

Al inspeccionar el factor primo $p$ en la estructura ASN.1:
- El módulo $N$ (1024 bits) y el exponente $e = 65537$ se encuentran íntegros.
- En este caso, $p$ no tiene un solo bloque faltante en la cola, sino **tres fragmentos discontinuos** de bytes sobrescritos por ceros:
  - Gap 1: 5 bytes (40 bits).
  - Gap 2: 4 bytes (32 bits).
  - Gap 3: 5 bytes (40 bits).
- Total de bits faltantes: 112 bits distribuidos en tres posiciones.

### Ataque Multivariado de Coppersmith
Dado que las incógnitas están distribuidas en tres variables independientes ($x_0, x_1, x_2$), se formula un polinomio lineal multivariado:

$$f(x_0, x_1, x_2) = p_{\text{fixed}} + x_0 \cdot 2^{k_0} + x_1 \cdot 2^{k_1} + x_2 \cdot 2^{k_2} \pmod p$$

Utilizando el método de Coppersmith multivariado mediante construcción de reticulados y reducción LLL en SageMath, se obtienen las raíces pequeñas simultáneas para cada variable, reconstruyendo el factor primo original $p$:
$$p = 13331193528989238711281209084398307362804767638940062463831686008684031051105241659991501990308217733345218358352985573809576597628552151562857633661821019$$

Con $p$ completamente recuperado:
1. $q = N / p$.
2. $\phi(N) = (p - 1)(q - 1)$.
3. $d \equiv e^{-1} \pmod{\phi(N)}$.
4. Se descifra $m \equiv c^d \pmod N$ y se extrae el texto en claro.

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

# Primo recuperado vía Multivariate Coppersmith LLL
p = 13331193528989238711281209084398307362804767638940062463831686008684031051105241659991501990308217733345218358352985573809576597628552151562857633661821019
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
- La técnica multivariada generaliza el algoritmo de Coppersmith para recuperar múltiples bloques faltantes siempre que la dimensión y cotas del reticulado satisfagan la condición de Howgrave-Graham.
- Flag en formato: `picoCTF{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/211
- Apoyo: https://github.com/defund/coppersmith
