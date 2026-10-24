# Cryptography — college-rowing-team

## Descripción
> **Prompt oficial del reto:** "I just joined my college's rowing team! To make a good first impression, I started sending my teammates positive automated messages every day. I even send them flags from time to time!"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoMini by redpwn
- **Autor:** Boolean

## Solución

Al analizar el script de cifrado `encrypt.py`, observamos los siguientes parámetros de RSA:
- Exponente público pequeño: $e = 3$.
- Módulo RSA grande: $n = p \cdot q$ de 2048 bits ($p$ y $q$ de 1024 bits).
- Ausencia de padding (textbook RSA): $m$ es simplemente la representación entera directa del mensaje en bytes.

Debido a que el mensaje $m$ tiene menos de 50 bytes:
$$\text{longitud en bits de } m \approx 50 \times 8 = 400 \text{ bits}$$
Al elevar al cubo con $e = 3$:
$$\text{longitud en bits de } m^3 \approx 1200 \text{ bits} \ll 2048 \text{ bits}$$

Por consiguiente, $m^3 < n$, lo que significa que la operación modular nunca dio una vuelta ($m^3 \pmod n = m^3$ en los enteros). No es necesario siquiera aplicar el ataque de difusión de Håstad (Håstad's Broadcast Attack); basta con computar directamente la raíz cúbica entera de los textos cifrados:

$$m = \sqrt[3]{c}$$

```bash
python3 - << 'EOF'
import gmpy2
from Crypto.Util.number import long_to_bytes

with open('encrypted-messages.txt') as f:
    chunks = f.read().strip().split('\n\n')

for chunk in chunks:
    lines = chunk.strip().split('\n')
    c = int(lines[2].split(':')[1].strip())
    root, exact = gmpy2.iroot(c, 3)
    if exact:
        msg = long_to_bytes(int(root))
        if b'picoCTF{' in msg or b'academy{' in msg:
            print(msg.decode())
            break
EOF
```

## Notas adicionales
- Este vector de ataque ilustra por qué los esquemas de cifrado RSA en entornos reales deben implementar esquemas de relleno deterministas o probabilísticos seguros como OAEP (Optimal Asymmetric Encryption Padding).
- Flag en formato: `picoCTF{...}`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/212
- Apoyo: https://en.wikipedia.org/wiki/Coppersmith%27s_attack
