# Cryptography — Guess My Cheese (Part 1)

## Descripción

> **Prompt oficial del reto:** "Try to decrypt the secret cheese password to prove you're not the imposter!"

> **Hints:**
> 1. Remember that cipher we devised together Squeexy? The one that incorporates your *affinity* for *linear equations*???

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** aditin

## Solución

Al conectarse al servicio por `nc`, el programa presenta una cadena cifrada que representa un nombre de queso secreto y ofrece dos opciones:
- `(e)`: Cifra un nombre de queso válido (tomado de la lista oficial de quesos).
- `(g)`: Adivina el queso secreto.

La pista *"affinity for linear equations"* apunta de forma inequívoca al **cifrado afín** (*Affine Cipher*):
$$E(x) = (a \cdot x + b) \bmod 26$$
donde $x \in \{0, \dots, 25\}$ representa la posición alfabética ($A=0, B=1, \dots, Z=25$) y $\gcd(a, 26) = 1$.

### Deducción de los parámetros $a$ y $b$

Solicitamos al oráculo cifrar el queso conocido `Cheddar`:
$$\text{Cheddar} \xrightarrow{E} c_0 c_1 c_2 c_3 c_4 c_5 c_6$$

Como:
- La letra `a` está en la posición 5 ($x = 0$):
  $$E(0) = (a \cdot 0 + b) \equiv b \pmod{26}$$
  Por lo tanto, $b = \text{ord}(c_5) - \text{ord}(\text{'A'})$.
- La letra `d` está en la posición 3 ($x = 3$) y `e` en la posición 2 ($x = 4$):
  $$E(4) - E(3) = (4a + b) - (3a + b) \equiv a \pmod{26}$$
  Por lo tanto, $a = (c_2 - c_3) \bmod 26$.

### Descifrado y envío de la respuesta

Con $a$ y $b$ determinados, calculamos el inverso modular $a^{-1} \pmod{26}$. La función de descifrado es:
$$D(y) = a^{-1} \cdot (y - b) \bmod 26$$

Al aplicar $D(y)$ a cada letra del texto cifrado secreto, obtenemos el nombre en claro del queso y lo enviamos a través de la opción `(g)`, obteniendo la flag.

### Script de resolución

```python
import socket, re

s = socket.create_connection(("<HOST>", <PUERTO>), timeout=10)

def recv_until(target):
    buf = b""
    while target not in buf:
        d = s.recv(1024)
        if not d: break
        buf += d
    return buf.decode(errors="replace")

# 1. Cifrar 'Cheddar' para recuperar a y b
recv_until(b"What would you like to do?")
s.sendall(b"e\n")
recv_until(b"What cheese would you like to encrypt?")
s.sendall(b"Cheddar\n")
out = recv_until(b"What would you like to do?")
enc = re.search(r"encrypted cheese:\s*([A-Za-z]+)", out).group(1).upper()

# Derivar parámetros afines
y_a = ord(enc[5]) - ord("A")
y_e = ord(enc[2]) - ord("A")
y_d = ord(enc[3]) - ord("A")
b = y_a
a = (y_e - y_d) % 26
a_inv = pow(a, -1, 26)

# 2. Obtener ciphertext secreto y descifrar
s.sendall(b"g\n")
prompt = recv_until(b"So...what's my cheese?\n")
secret_ct = re.search(r"encrypted cheese:\s*([A-Za-z]+)", prompt).group(1).upper()

plain = "".join(chr(ord("A") + (a_inv * ((ord(c) - ord("A")) - b)) % 26) for c in secret_ct)

# 3. Enviar respuesta
s.sendall(f"{plain}\n".encode())
print(s.recv(4096).decode(errors="replace"))
s.close()
```

## Referencias

- [Affine Cipher — Wikipedia](https://en.wikipedia.org/wiki/Affine_cipher)
- [Modular Multiplicative Inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse)
