# Cryptography — b00tl3gRSA2

## Descripción
> **Prompt oficial del reto:** "In RSA d is a lot bigger than e, why don't we use d to encrypt instead of e?"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** invisibility

## Solución
Al conectarse a la instancia del servicio por red, se presentan tres parámetros:
- $c$: El texto cifrado.
- $n$: El módulo RSA.
- $e$: Un valor inusualmente grande (de longitud similar a $n$).

### Vulnerabilidad: Confusión entre clave pública y privada ($e$ y $d$)
En el criptosistema RSA convencional, el par de claves cumple:
$$e \cdot d \equiv 1 \pmod{\phi(n)}$$

Por estándar de la industria, el exponente público $e$ se escoge casi universalmente como un número primo de Fermat pequeño con baja densidad de Hamming para optimizar la exponenciación rápida, comúnmente $e = 65537$ ($2^{16} + 1$). El exponente privado $d$ se calcula como el inverso multiplicativo de $e$ módulo $\phi(n)$, por lo que $d$ suele tener un tamaño del mismo orden de magnitud que $n$.

El autor del reto pensó: *"d es mucho más grande que e, ¿por qué no usamos d para cifrar en vez de e?"*. En consecuencia, cifró el mensaje utilizando el exponente privado $d$:
$$c = m^d \pmod n$$

Debido a la simetría de la relación modular de RSA:
$$(m^d)^e \equiv m^{d \cdot e} \equiv m \pmod n$$

Cualquiera puede descifrar el mensaje simplemente elevando el criptograma al exponente estándar original $e = 65537$:
$$m = c^{65537} \pmod n$$

### Script de resolución
```bash
python3 - << 'EOF'
import socket
from Crypto.Util.number import long_to_bytes

# Conexión al servicio
s = socket.create_connection(("chatelaine.cylabacademy.net", 16238))
data = s.recv(4096).decode()
s.close()

lines = data.strip().split("\n")
c = int(lines[0].split(":")[1])
n = int(lines[1].split(":")[1])

# Descifrar usando el e estándar (65537)
e_std = 65537
m = pow(c, e_std, n)
flag = long_to_bytes(m).decode()
print(f"[+] Flag recuperada: {flag}")
EOF
```

El mensaje descifrado produce la bandera en formato `academy{...}`.

## Notas adicionales
- La seguridad asimétrica de RSA depende críticamente de que el exponente secreto sea inaccesible. Si se utiliza la clave secreta como exponente de cifrado "público", la clave inversa necesaria para descifrar no es otra que el exponente público trivialmente conocido $65537$.

## Referencias
- Reto: https://learn.cylabacademy.org/library/2
- Apoyo: RFC 8017 — PKCS #1: RSA Cryptography Specifications Version 2.2
