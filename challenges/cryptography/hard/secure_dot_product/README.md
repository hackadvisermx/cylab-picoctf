# Cryptography — Secure Dot Product

## Descripción
> **Prompt oficial del reto:** "Our intern thought it was a great idea to vibe code a secure dot product server using our AES key. Having taken a class in linear algebra, they're confident the server can't ever leak our key, but I'm not so sure...
> 
> Download the source code [remote.py](https://challenge-files.cylabacademy.net/library/46861c5fb134ad1409993f6940617bf8116f55ad1fa77698214f055842a0caf5/remote.py)"

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2026
- **Autor:** watermelon, Donkey

## Solución
El servicio interactivo almacena una clave secreta AES-256 (`key_vector` de 32 bytes) y ofrece calcular el producto punto con vectores "de confianza" proporcionados por el usuario. La confianza se valida comprobando un hash con sal:
$$\text{hash} = \text{SHA-512}(\text{salt} + \text{vector}[1:-1])$$
donde la sal tiene un tamaño fijo de 256 bytes (`SALT_SIZE = 256`). El servidor nos revela 5 vectores iniciales confiables junto con sus respectivos hashes con sal.

### Vulnerabilidades identificadas:
1. **Ataque de extensión de longitud (Length Extension Attack):** Dado que la función de autenticación utiliza la construcción ingenua $\text{SHA-512}(\text{salt} + \text{message})$, podemos extender cualquiera de los vectores confiables agregando el padding estándar de SHA-512 y un sufijo arbitrario sin conocer la sal.
2. **Sanitización incompleta de entrada:** El servidor procesa la cadena con `unicode_escape` y luego filtra la entrada con `sanitized = "".join(c if c in '0123456789,[]' else '' for c in vector)`. Como los bytes del padding de SHA-512 (bytes nulos, delimitador `\x80`, etc.) no son dígitos ni comas, el parser los descarta y concatena limpiamente nuestros nuevos elementos numéricos al final del vector evaluado.

### Procedimiento de explotación:
1. Tomamos uno de los vectores confiables de longitud $k \le 32$ y su hash.
2. Construimos un sufijo con valores numéricos adicionales que se extiendan hasta la dimensión 32.
3. Calculamos el hash extendido reanudando el estado interno de SHA-512 a partir del hash inicial conocido.
4. Repetimos el proceso variando el sufijo para obtener 32 ecuaciones linealmente independientes con los productos punto devueltos.
5. Resolvemos el sistema de ecuaciones lineales $M \cdot \vec{k} = \vec{r}$ para despejar los 32 bytes de la clave AES.
6. Desciframos el texto cifrado inicial utilizando `AES-256-CBC` con el IV y la clave recuperada.

```python
# Reanudación de estado SHA-512 y resolución lineal
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Extensión de SHA-512 con salt_size=256
padding, ext_hash = extend_sha512(base_hash, 256 + len(orig_encoding), suffix)
# Envío de vector con padding escapado: '[' + orig + pad_escaped + suffix + ']'
# Recepción del producto punto calculado
...
# Resolución del sistema matricial M * k = y
k_sol = np.linalg.solve(M, y)
key_bytes = bytes([int(round(x)) % 256 for x in k_sol])
cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
flag = unpad(cipher.decrypt(ct), AES.block_size).decode()
```

Al descifrar se obtiene la flag con formato `academy{...}`.

## Notas adicionales
La vulnerabilidad fundamental proviene de usar la construcción $\text{Hash}(key \parallel message)$ en lugar de un código de autenticación de mensajes seguro como HMAC ($\text{HMAC-SHA-512}$).

## Referencias
- Reto: https://learn.cylabacademy.org/library/728
- SHA-512 Length Extension Attack: https://en.wikipedia.org/wiki/Length_extension_attack
