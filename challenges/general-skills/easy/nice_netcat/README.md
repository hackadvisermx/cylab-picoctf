# General Skills — Nice netcat...

## Descripción
> **Prompt oficial:** "There is a nice program that you can talk to by using this command in a shell: `nc <host> <puerto>`, but it doesn't speak English..."
>
> **Hints:**
> 1. You can practice using netcat with this picoGym problem: what's a netcat?
> 2. You can practice reading and writing ASCII with this picoGym problem: Let's Warm Up

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
El servicio envía directamente una lista de números decimales (uno por línea), que son códigos ASCII.

```python
import socket
s = socket.create_connection(("<host>", <puerto>))
data = s.recv(65536).decode()
print(''.join(chr(int(n)) for n in data.split()))
```

Flag: `picoCTF{g00d_k1tty!_n1c3_k1tty!_d9476}`

## Notas adicionales
- Muy similar en espíritu a `ASCII Numbers` (Medium), pero aquí los códigos vienen en **decimal** en vez de hexadecimal, y hay que conectarse por red en vez de leer un texto ya dado.

## Referencias
- Reto: https://learn.cylabacademy.org/library/156
