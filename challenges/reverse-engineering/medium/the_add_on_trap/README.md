# Reverse Engineering — The Add/On Trap

## Descripción
> **Prompt oficial del reto:** "What kind of information can an Add/On reach? Is it possible to exfiltrate them without me noticing? Do they really do what they say? Most importantly, when to eat? These and many other questions Add/On users should be asking themselves.
>
> Download the provided browser extension and inspect it to uncover the hidden flag:
> - [Download the .xpi](https://challenge-files.cylabacademy.net/library/ba1d9edf14b6cb9cf90cb78eae4378c0e41f32f2ae4491251502e18d124d93aa/suspicious.zip), password `academy`"
>
> **Pistas oficiales:**
> 1. What kind of file is one ending in `.xpi`?
> 2. Which modern Python scheme uses url-safe Base64 32-byte keys?

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Alessandro Greco aka Aleff

## Solución
El reto proporciona un archivo comprimido protegido por contraseña (`academy`) que contiene una extensión de navegador Firefox con extensión `.xpi`.

### 1. Extracción del complemento
Un archivo `.xpi` es un archivo ZIP estándar utilizado por extensiones de Mozilla Firefox. Se descomprime para examinar su estructura:

```bash
unzip -P academy suspicious.zip
unzip 56102ec0438646c68605-1.0.xpi -d xpi_extracted/
```

### 2. Inspección del código JavaScript
Al revisar los archivos extraídos, se encuentra el script de segundo plano `background/main.js`:

```javascript
// Secret key must be 32 url-safe base64-encoded bytes!
// TODO I must find a solution to remove the key from here, for now I'll leave it there because I need it to encrypt the webhook

function logOnCompleted(details) {
    console.log(`Information to exfiltrate: ${details.url}`);
    const key="YWNhZGVteXt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0="
    const webhookUrl='gAAAAABqUwkJWn6EVtro8ovh-MzUjpxg4dolaPtGOvfvZJDoDpYXWCaV0TWf4VBBiBh2l0ega8nyZMoUrIoK38IDB2GnRtbkktQmBLlxKFPe_ZWThc72G6pwmUo5Gk8ZLGSWe_NVfyS4'
    ...
```

El script revela:
- Una clave en Base64 seguro para URL de 32 bytes: `YWNhZGVteXt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0=` (al decodificarla en texto plano dice `academy{you're on the right tra}`).
- Una cadena cifrada `webhookUrl` que comienza con `gAAAAA...`, el prefijo característico del formato de cifrado simétrico **Fernet** de la librería `cryptography` de Python.

### 3. Descifrado con Fernet
Utilizando la clave para descifrar el token Fernet en Python:

```python
from cryptography.fernet import Fernet

key = b"YWNhZGVteXt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0="
f = Fernet(key)
token = b"gAAAAABqUwkJWn6EVtro8ovh-MzUjpxg4dolaPtGOvfvZJDoDpYXWCaV0TWf4VBBiBh2l0ega8nyZMoUrIoK38IDB2GnRtbkktQmBLlxKFPe_ZWThc72G6pwmUo5Gk8ZLGSWe_NVfyS4"

flag = f.decrypt(token).decode()
print("Flag:", flag)
```

Salida:
```text
Flag: academy{...}
```

## Notas adicionales
- Fernet utiliza AES en modo CBC con claves de 128 bits, relleno PKCS7 y autenticación mediante HMAC-SHA256 con claves de 128 bits, empaquetadas juntas en una clave Base64 URL-safe de 32 bytes (256 bits en total).

## Referencias
- Reto: https://learn.cylabacademy.org/library/697
- Cryptography Fernet Specification: https://cryptography.io/en/latest/fernet/
