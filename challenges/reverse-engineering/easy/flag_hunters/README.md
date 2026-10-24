# Reverse Engineering — Flag Hunters

## Descripción
> **Prompt oficial del reto:** "Lyrics jump from verses to the refrain kind of like a subroutine call. There's a hidden refrain this program doesn't print by default. Can you get it to print it? There might be something in it for you."
>
> **Pistas:**
> 1. This program can easily get into undefined states. Don't be shy about Ctrl-C.
> 2. Unsanitized user input is always good, right?
> 3. Is there any syntax that is ripe for subversion?

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2025
- **Autor:** syreal

## Solución
El reto proporciona un script en Python (`lyric-reader.py`) que interpreta una secuencia lírica como si fuera código ensamblador o un flujo de control estructurado con subrutinas:
- La bandera se lee de `flag.txt` y se almacena en `secret_intro` en las primeras líneas del arreglo `song_lines` (índices 0 a 3), fuera del recorrido normal que inicia en `[VERSE1]`.
- El flujo avanza con un puntero de instrucción `lip`. Cuando encuentra la directiva `REFRAIN;`, salta al bloque `[REFRAIN]` y almacena una instrucción de retorno dinámico `RETURN <lip+1>` en la posición `refrain_return`.
- Dentro de `[REFRAIN]`, se ejecuta la directiva `CROWD (Singalong here!);`. Cuando coincide con la expresión regular `re.match(r"CROWD.*", line)`, solicita una entrada interactiva con `input('Crowd: ')` y sobrescribe esa línea en la memoria del programa: `song_lines[lip] = 'Crowd: ' + crowd`.
- Las líneas son evaluadas separándolas por punto y coma (`;`). Por tanto, si inyectamos una directiva de control en la entrada del público (`crowd`), por ejemplo `;RETURN 0`, no causará efecto inmediato en ese instante porque la línea actual ya fue dividida, pero se almacenará permanentemente en la posición del coro.
- Cuando el programa termina el estribillo y regresa al verso 1, avanza hasta encontrar la siguiente invocación a `REFRAIN;`. Al volver a entrar al coro y alcanzar la línea modificada, el intérprete la divide por `;`, procesa la instrucción inyectada `RETURN 0`, actualiza el puntero de instrucción a `lip = 0` y comienza a imprimir secuencialmente `secret_intro`, revelando la bandera.

```bash
# Conectar al servicio interactivo con netcat
nc chatelaine.cylabacademy.net <puerto>

# Esperar a que se muestre la solicitud del coro
# Enviar la carga útil para inyectar la instrucción de retorno al inicio:
;RETURN 0

# En el segundo ciclo del coro, el intérprete saltará a la línea 0 e imprimirá la flag
```

Script de explotación automatizada:
```python
import socket
import re

s = socket.socket()
s.connect(("chatelaine.cylabacademy.net", <puerto>))

buf = ""
while "Crowd: " not in buf:
    chunk = s.recv(1024).decode(errors="ignore")
    if not chunk:
        break
    buf += chunk

s.sendall(b";RETURN 0\n")

while True:
    data = s.recv(1024).decode(errors="ignore")
    if not data:
        break
    if "academy{" in data or "picoCTF{" in data:
        print("Flag encontrada:", re.search(r"(academy\{[^}]+\}|picoCTF\{[^}]+\})", data).group(1))
        break

s.close()
```

Flag: `academy{...}`

## Notas adicionales
El fallo radica en la modificación dinámica del código ejecutable en memoria a partir de entradas no sanitizadas del usuario (`self-modifying code`), permitiendo subvertir el puntero de instrucción del intérprete artesanal.

## Referencias
- Reto: https://learn.cylabacademy.org/library/472
