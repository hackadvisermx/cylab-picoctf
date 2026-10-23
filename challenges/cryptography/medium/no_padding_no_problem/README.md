# Cryptography — No Padding, No Problem

## Descripción

> **Prompt oficial del reto:** "Oracles can be your best friend, they will decrypt anything, except the flag's ciphertext. How will you break it?"

> **Hints:**
> 1. What can you do with a different pair of ciphertext and plaintext? What if it is not so different after all...

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Sara

## Solución

El reto presenta un servicio por `nc` que proporciona un oráculo de descifrado RSA interactivo: entrega los parámetros públicos $n$, $e$ y el texto cifrado objetivo $c$ (que contiene la flag). El oráculo acepta cualquier texto cifrado y devuelve el descifrado correspondiente, excepto si se le envía exactamente $c$.

### Vulnerabilidad: Homomorfismo multiplicativo en RSA sin padding (Textbook RSA)

En RSA sin padding (*textbook RSA*), el cifrado preserva la multiplicación:
$$E(m_1) \cdot E(m_2) \equiv m_1^e \cdot m_2^e \equiv (m_1 \cdot m_2)^e \equiv E(m_1 \cdot m_2) \pmod n$$

Podemos explotar esta propiedad para realizar un **ataque de texto cifrado escogido** (*Chosen-Ciphertext Attack - CCA1*):

1. Elegimos un multiplicador arbitrario $k > 1$ (por ejemplo, $k = 2$) coprimo con $n$.
2. Ciframos el factor multiplicador con la clave pública:
   $$c_k \equiv k^e \pmod n$$
3. Calculamos un nuevo texto cifrado $c'$ multiplicando el texto cifrado objetivo $c$ por $c_k$:
   $$c' \equiv c \cdot k^e \equiv m^e \cdot k^e \equiv (k \cdot m)^e \pmod n$$
4. Como $c' \neq c$, el oráculo acepta $c'$ y lo descifra utilizando la clave privada $d$:
   $$m' \equiv (c')^d \equiv ((k \cdot m)^e)^d \equiv k \cdot m \pmod n$$
5. Con el resultado $m'$ devuelto por el oráculo, eliminamos el factor $k$ multiplicando por su inverso modular:
   $$m \equiv m' \cdot k^{-1} \pmod n$$
6. Convertimos el entero $m$ a bytes para obtener la flag.

### Script de resolución

```python
import socket, re

# Conexión al servicio
s = socket.create_connection(("<HOST>", <PUERTO>), timeout=10)
buf = ""
while "Give me ciphertext to decrypt:" not in buf:
    chunk = s.recv(1024).decode()
    if not chunk:
        break
    buf += chunk

n = int(re.search(r"n:\s*(\d+)", buf).group(1))
e = int(re.search(r"e:\s*(\d+)", buf).group(1))
c = int(re.search(r"ciphertext:\s*(\d+)", buf).group(1))

# Calcular c_prime = (c * 2^e) mod n
k = 2
c_prime = (c * pow(k, e, n)) % n

# Enviar c_prime al oráculo
s.sendall(f"{c_prime}\n".encode())

# Leer respuesta del oráculo
out = ""
while "Here you go:" not in out:
    chunk = s.recv(1024).decode()
    if not chunk:
        break
    out += chunk
s.close()

# Recuperar m_prime y despejar m = m_prime * 2^(-1) mod n
m_prime = int(re.search(r"Here you go:\s*(\d+)", out).group(1))
m = (m_prime * pow(k, -1, n)) % n

flag = m.to_bytes((m.bit_length() + 7) // 8, "big")
print(flag.decode())
```

## Referencias

- [Chosen-ciphertext attack on RSA — Wikipedia](https://en.wikipedia.org/wiki/Chosen-ciphertext_attack)
- [Multiplicative Property of RSA — Stanford CS255](https://crypto.stanford.edu/~dabo/cs255/)
