# Cryptography — Shared Secrets

## Descripción
> **Prompt oficial del reto:** "A message was encrypted using a shared secret... but it looks like one side of the exchange leaked something. Can you piece together the secret and get the flag? Download the message. And source code."
>
> **Hints:**
> 1. What do you get if you combine a public key with a known private one?

- **Categoría:** Cryptography
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
El `encryption.py` implementa un intercambio **Diffie-Hellman** y cifra la flag con XOR usando el secreto compartido módulo 256:

```python
shared = pow(A, b, p)
enc = bytes([x ^ (shared % 256) for x in flag])
```

El `message.txt` entregado **filtra `b`** (el secreto privado del cliente), además de `g`, `p`, `A` y `enc`. Con `b` conocido, el secreto compartido se recomputa directamente (`shared = A^b mod p`) — justo lo que dice el hint: combinar la clave pública `A` con la privada conocida `b` da el secreto compartido. Luego XOR inverso:

```python
shared = pow(A, b, p)
k = shared % 256
print(bytes([x ^ k for x in bytes.fromhex(enc)]))
# academy{dh_s3cr3t_913ddd75}
```

## Notas adicionales
- La seguridad de Diffie-Hellman depende de que **ambos** secretos privados (a y b) permanezcan ocultos. Si uno se filtra, cualquiera recomputa el secreto compartido y descifra todo.
- El cifrado XOR con `shared % 256` reduce el secreto a un solo byte de clave — débil incluso sin la fuga, pero aquí la fuga de `b` lo hace instantáneo.

## Referencias
- Reto: https://learn.cylabacademy.org/library/715
