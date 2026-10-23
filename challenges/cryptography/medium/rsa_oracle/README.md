# Cryptography — rsa_oracle

## Descripción

> **Prompt oficial del reto:** "Can you abuse the oracle?
>
> An attacker was able to intercept communications between a bank and a fintech company. They managed to get the message (ciphertext) and the password that was used to encrypt the message.
> After some intensive reconassainance they found out that the bank has an oracle that was used to encrypt the password and can be found here `nc <host> <port>`. Decrypt the password and use it to decrypt the message. The oracle can decrypt anything except the password."

> **Hints:**
> 1. Crytography Threat models: chosen plaintext attack.
> 2. OpenSSL can be used to decrypt the message. e.g `openssl enc -aes-256-cbc -d ...`
> 3. The key to getting the flag is by sending a custom message to the server by taking advantage of the RSA encryption algorithm.
> 4. Minimum requirements for a useful cryptosystem is CPA security.

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** Geoffrey Njogu

## Solución

Se proporcionan dos archivos:
1. `secret.enc`: Datos cifrados con OpenSSL (`enc'd data with salted password`).
2. `password.enc`: Un entero que representa la contraseña cifrada con RSA ($c_{\text{pass}}$).

El servicio remoto ofrece un oráculo interactivo con dos opciones:
- `E`: Cifra cualquier texto plano que enviemos ($c = m^e \pmod n$).
- `D`: Descifra cualquier texto cifrado proporcionado ($m = c^d \pmod n$), **excepto** si se le envía directamente $c_{\text{pass}}$.

### Ataque homomórfico (Blinding) sobre RSA sin padding

Debido a que el oráculo implementa RSA de libro de texto (*textbook RSA*), el cifrado preserva la multiplicación:
$$(m_1 \cdot m_2)^e \equiv m_1^e \cdot m_2^e \pmod n$$

Para descifrar $c_{\text{pass}}$ evadiendo la restricción del servidor:

1. **Obtener el cifrado de un factor conocido:**
   Usamos la opción `E` del oráculo para cifrar el número $2$ (`\x02`), obteniendo:
   $$c_2 \equiv 2^e \pmod n$$

2. **Cifrado cegado (Blinded Ciphertext):**
   Multiplicamos el texto cifrado objetivo por $c_2$:
   $$c' = c_{\text{pass}} \cdot c_2 \pmod n$$
   Como $c' \neq c_{\text{pass}}$, el oráculo lo acepta.

3. **Consulta al oráculo de descifrado:**
   Enviamos $c'$ a la opción `D`. El oráculo calcula:
   $$(c')^d \equiv (c_{\text{pass}} \cdot c_2)^d \equiv (P^e \cdot 2^e)^d \equiv 2P \pmod n$$
   donde $P$ es la contraseña en texto plano.

4. **Recuperación de la contraseña:**
   Dividimos el valor devuelto por 2 en los enteros (o multiplicamos por el inverso modular si hubiera reducción):
   $$P = \frac{2P}{2}$$
   Convertimos el entero $P$ a caracteres ASCII, obteniendo la contraseña en claro.

5. **Descifrado del archivo con OpenSSL:**
   Con la contraseña recuperada, desciframos `secret.enc` mediante AES-256-CBC:
   ```bash
   openssl enc -aes-256-cbc -d -in secret.enc -pass pass:<CONTRASEÑA>
   ```

### Script de resolución

```python
import socket, re, subprocess

# 1. Cargar ciphertext objetivo
with open("password.enc") as f:
    c_target = int(f.read().strip())

# 2. Conectar al oráculo
s = socket.create_connection(("<HOST>", <PUERTO>), timeout=10)

def recv_until(target):
    buf = b""
    while target not in buf:
        d = s.recv(1024)
        if not d:
            break
        buf += d
    return buf.decode(errors="replace")

# Esperar menú y cifrar \x02
recv_until(b"decrypt.")
s.sendall(b"E\n")
recv_until(b"keysize):")
s.sendall(b"\x02\n")

out = recv_until(b"decrypt.")
c2 = int(re.search(r"ciphertext \(m \^ e mod n\) (\d+)", out).group(1))

# Descifrar ciphertext multiplicado (cegado)
c_blind = c_target * c2
s.sendall(b"D\n")
recv_until(b"Enter text to decrypt:")
s.sendall(f"{c_blind}\n".encode())

resp = recv_until(b"decrypt.")
s.close()

# Extraer 2P y despejar P
m2_hex = re.search(r"decrypted ciphertext as hex \(c \^ d mod n\): ([0-9a-fA-F]+)", resp).group(1)
m2 = int(m2_hex, 16)
p_int = m2 // 2
password = bytes.fromhex(hex(p_int)[2:]).decode()
print("Contraseña recuperada:", password)

# Descifrar secret.enc con openssl
res = subprocess.run(
    ["openssl", "enc", "-aes-256-cbc", "-d", "-in", "secret.enc", "-pass", f"pass:{password}"],
    capture_output=True, text=True
)
print("Contenido descifrado:", res.stdout)
```

## Referencias

- [RSA chosen-ciphertext attack — Wikipedia](https://en.wikipedia.org/wiki/Chosen-ciphertext_attack)
- [OpenSSL enc documentation](https://www.openssl.org/docs/manmaster/man1/openssl-enc.html)
