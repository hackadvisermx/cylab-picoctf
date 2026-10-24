# Cryptography — Double DES

## Descripción
> **Prompt oficial del reto:** "I wanted an encryption service that's more secure than regular DES, but not as slow as 3DES... The flag is not in standard format."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** madStacks

## Solución

El servicio remoto implementa un esquema de cifrado Double DES:
$$C = E_{K_2}(E_{K_1}(P))$$
donde cada clave se deriva mediante:
```python
def generate_key():
    return pad("".join(random.choice(string.digits) for _ in range(6)))
```
Esto genera una clave formada por 6 dígitos decimales rellenada con espacios hasta completar los 8 bytes requeridos por DES. Por lo tanto, el espacio de claves para cada una es de exactamente $10^6$ posibilidades ($1\,000\,000$).

### Vulnerabilidad: Ataque Meet-in-the-Middle (MITM)
Un ataque de fuerza bruta directa sobre Double DES requeriría $(10^6)^2 = 10^{12}$ operaciones. Sin embargo, podemos reescribir la relación de cifrado como:
$$E_{K_1}(P) = D_{K_2}(C)$$
donde $P$ es un texto en claro conocido y $C$ es su texto cifrado correspondiente.

### Proceso de Explotación
1. Nos conectamos al servicio mediante `nc` y leemos el texto cifrado de la bandera provisto al inicio.
2. Enviamos un texto en claro conocido $P = \text{"13371337"}$ en hexadecimal para obtener su texto cifrado correspondiente $C$.
3. **Fase directa (hacia adelante):**
   - Para las $10^6$ claves candidatas $K_1 \in \{000000, \dots, 999999\}$:
   - Calculamos el valor intermedio $M_{\text{mid}} = E_{K_1}(P)$.
   - Guardamos el mapeo en una tabla hash: $\text{table}[M_{\text{mid}}] = K_1$.
4. **Fase inversa (hacia atrás):**
   - Para las $10^6$ claves candidatas $K_2 \in \{000000, \dots, 999999\}$:
   - Calculamos $M'_{\text{mid}} = D_{K_2}(C)$.
   - Si $M'_{\text{mid}} \in \text{table}$, hemos encontrado el par correcto $(K_1, K_2)$.
5. Desciframos la bandera aplicando $D_{K_1}(D_{K_2}(C_{\text{flag}}))$.

```bash
python3 - << 'EOF'
import socket
import binascii
import time
from Crypto.Cipher import DES

# Configuración de endpoint del reto
host = "chatelaine.cylabacademy.net"
port = 45397

s = socket.create_connection((host, port), timeout=15)
f = s.makefile("rw", buffering=1)

f.readline()  # "Here is the flag:"
enc_flag_hex = f.readline().strip()

while True:
    if f.read(1) == "?":
        f.read(1)  # espacio
        break

known_ptxt = "13371337"
f.write(binascii.hexlify(known_ptxt.encode()).decode() + "\n")
f.flush()
enc_known_hex = f.readline().strip()
s.close()

padded_plain = known_ptxt.encode()
target_cipher = binascii.unhexlify(enc_known_hex)[:8]

# 1. Tabla de búsqueda hacia adelante
forward_table = {}
for i in range(1000000):
    k1 = f"{i:06d}  ".encode()
    c1 = DES.new(k1, DES.MODE_ECB).encrypt(padded_plain)
    forward_table[c1] = k1

# 2. Búsqueda hacia atrás
found_k1, found_k2 = None, None
for j in range(1000000):
    k2 = f"{j:06d}  ".encode()
    mid = DES.new(k2, DES.MODE_ECB).decrypt(target_cipher)
    if mid in forward_table:
        found_k1 = forward_table[mid]
        found_k2 = k2
        break

cipher_flag = binascii.unhexlify(enc_flag_hex)
dec1 = DES.new(found_k2, DES.MODE_ECB).decrypt(cipher_flag)
flag = DES.new(found_k1, DES.MODE_ECB).decrypt(dec1).decode().strip()
print(flag)
EOF
```

## Notas adicionales
- El ataque Meet-in-the-Middle reduce la complejidad de $2^{2k}$ a $2^{k+1}$, demostrando por qué 2DES no ofrece un margen de seguridad superior a DES estándar frente a atacantes con memoria suficiente.
- Flag no utiliza el prefijo habitual: es una cadena hexadecimal directa.

## Referencias
- Reto: https://learn.cylabacademy.org/library/140
- Apoyo: https://en.wikipedia.org/wiki/Meet-in-the-middle_attack
