# General Skills — bytemancy 2

## Descripción
> **Prompt oficial del reto:** "Can you conjure the right bytes? The program's source code can be downloaded here. Connect to the program with netcat."

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

## Solución
El código fuente entregado (`app.py`) es muy directo:

```python
user_input = sys.stdin.buffer.readline().rstrip(b"\n")
if user_input == b"\xff\xff\xff":
    print(open("./flag.txt", "r").read())
```

El servicio pide literalmente "el byte hexadecimal 0xFF, 3 veces, uno junto al otro" — pero espera los **bytes crudos** `0xFF 0xFF 0xFF`, no la cadena de texto `"FF FF FF"` ni `"\\xff\\xff\\xff"`. Cualquier cliente de texto (como escribir a mano en una sesión de `nc` interactiva) mandaría los caracteres ASCII `f`, `f`, etc., no el byte 0xFF real — hace falta un socket que mande el valor binario exacto.

```python
import socket
s = socket.create_connection(("lonely-island.picoctf.net", <puerto>), timeout=10)
s.sendall(b"\xff\xff\xff\n")
print(s.recv(4096).decode(errors="replace"))
```

## Notas adicionales
- Lección central: distinguir entre **el valor de un byte** y **su representación textual en hexadecimal** — "0xFF" escrito con el teclado son dos caracteres ASCII (`0`, `x`, `F`, `F`), mientras que el byte `0xFF` es un único byte con valor 255. Herramientas de línea de comandos como `nc` en modo interactivo no permiten teclear bytes arbitrarios fácilmente; conviene generar el payload con `printf '\xff\xff\xff'` o, más simple y portable, un socket en Python.
- Continuidad de la serie "bytemancy": bytemancy 0/1 (Easy, ya documentados) trabajan con bytes imprimibles/no imprimibles; bytemancy 2 introduce el envío de bytes crudos no imprimibles por red; bytemancy 3 (Medium, este mismo bloque) sube el nivel a leer símbolos de un binario ELF.

## Referencias
- Reto: https://learn.cylabacademy.org/library/724
