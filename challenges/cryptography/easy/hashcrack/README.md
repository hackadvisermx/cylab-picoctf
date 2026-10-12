# Cryptography — hashcrack

## Descripción
> **Prompt oficial del reto:** "A company stored a secret message on a server which got breached due to the admin using weakly hashed passwords. Can you gain access to the secret stored within the server? Access the server using `nc xebec.cylabacademy.net <puerto>`."
>
> **Hints:**
> 1. Understanding hashes is very crucial. Read more here.
> 2. Can you identify the hash algorithm? Look carefully at the length and structure of each hash identified.
> 3. Tried using any hash cracking tools?

- **Categoría:** Cryptography
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2025
- **Autor:** Nana Ama Atombo-Sackey

## Solución
El servicio presenta **3 hashes en secuencia**, uno por algoritmo, que hay que crackear para avanzar. El algoritmo se identifica por la longitud del hash:
- **MD5** (32 hex): `482c811da5d5b4bc6d497ffa98491e38` → `password123`
- **SHA-1** (40 hex): `b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3` → `letmein`
- **SHA-256** (64 hex): `916e8c4f79b25028c9e467f1eb8eee6d6bbdff965f9928310ad30a8d88697745` → `qwerty098`

Los dos primeros son contraseñas muy comunes; el tercero se crackea contra `rockyou.txt`:

```python
import hashlib
target='916e8c4f...88697745'
for w in open('rockyou.txt',encoding='latin-1'):
    if hashlib.sha256(w.strip().encode()).hexdigest()==target:
        print(w.strip()); break   # qwerty098
```

Al responder las 3 rondas correctamente, el servidor entrega la flag:

```
academy{UseStr0nG_h@shEs_&PaSswDs!_6bbfe014}
```

Se automatizó la conexión (socket Python): leer cada hash, resolverlo por longitud→algoritmo contra un diccionario / rockyou, y enviar el plaintext.

## Notas adicionales
- La **longitud en hex** identifica el algoritmo: 32=MD5, 40=SHA-1, 64=SHA-256. Es el primer paso antes de crackear.
- Hashes sin sal de contraseñas débiles se rompen al instante con un diccionario (`rockyou.txt`) — justamente la lección del reto.

## Referencias
- Reto: https://learn.cylabacademy.org/library/475
