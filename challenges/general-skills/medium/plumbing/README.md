# General Skills — plumbing

## Descripción
> **Prompt oficial del reto:** "Sometimes you need to handle process data outside of a file. Can you find a way to keep the output from this program and search for the flag? Connect to `fickle-tempest.picoctf.net 53243`."
>
> **Hints:**
> 1. Remember the flag format is picoCTF{XXXX}
> 2. What's a pipe? No not that kind of pipe... This kind |

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Alex Fulton/Danny Tunitis

## Solución
Al conectarse con `nc` al servicio, este empieza a escupir un chorro interminable de líneas de "ruido" ("Not a flag either", "This is definitely not a flag", etc.) demasiado rápido y largo para leerlo a ojo en la terminal. La flag real está mezclada en algún punto de ese output. La pista del reto ("keep the output... find a way") apunta a **capturar todo el stream en un buffer/archivo en vez de solo mirarlo pasar por pantalla** — de ahí el hint del pipe `|` (p. ej. `nc host puerto | tee output.txt` o redirigir a un archivo) para poder después buscar el patrón `picoCTF{` con `grep` con calma.

Se automatizó igual con un socket en Python, acumulando todo el output hasta que el servidor cierra la conexión (o timeout) y luego buscando la flag con una expresión regular:

```python
import socket
s = socket.create_connection(("fickle-tempest.picoctf.net", 53243), timeout=8)
s.settimeout(3)
data = b""
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
except socket.timeout:
    pass
```

```bash
grep -o "picoCTF{[^}]*}" salida.txt
# picoCTF{digital_plumb3r_0BAc587E}
```

## Notas adicionales
- El "truco" real del reto no es técnico sino de flujo de trabajo: en vez de intentar leer un stream de texto que se desplaza demasiado rápido en la terminal, hay que **redirigirlo/guardarlo** (pipe a `tee`/archivo, o acumular el buffer en un script) para poder buscarlo después con calma.
- El output es de tamaño considerable (~280 KB en este caso) — conviene usar `grep -o` sobre el patrón `picoCTF{...}` en vez de intentar inspeccionar el archivo manualmente.

## Referencias
- Reto: https://learn.cylabacademy.org/library/48
