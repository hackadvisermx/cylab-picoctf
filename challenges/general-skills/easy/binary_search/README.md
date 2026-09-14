# General Skills — Binary Search

## Descripción
> **Prompt oficial:** "Want to play a game? Binary search is a classic algorithm used to quickly find an item in a sorted list. Can you find the flag? You'll have 1000 possibilities and only 10 guesses. `ssh -p <puerto> ctf-player@<host>` con contraseña `<pass>`."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Jeffery John

## Solución
Al conectar por SSH, el propio login lanza directamente el juego (un "comando forzado" en el servidor, no una shell normal): hay que adivinar un número entre 1 y 1000 en como mucho 10 intentos, recibiendo "Higher!"/"Lower!" tras cada intento — el caso de uso de libro de texto para **búsqueda binaria** (cada intento descarta la mitad del rango restante; con 1000 números, ⌈log2(1000)⌉ = 10 intentos son justo suficientes).

Se automatizó con `pexpect` en Python: en cada iteración se envía el punto medio del rango actual y, según la respuesta, se actualiza el límite inferior o superior.

```python
import pexpect
child = pexpect.spawn("ssh -p <puerto> ctf-player@<host>")
child.expect("password:"); child.sendline("<pass>")
lo, hi = 1, 1000
while True:
    child.expect("Enter your guess:")
    guess = (lo + hi) // 2
    child.sendline(str(guess))
    idx = child.expect(["Lower!", "Higher!", "Congratulations"])
    if idx == 0: hi = guess - 1
    elif idx == 1: lo = guess + 1
    else: break  # la flag aparece en la salida
```

Flag: `picoCTF{g00d_gu355_1597707f}`

## Notas adicionales
- El número objetivo de esta partida fue **301**, encontrado en el intento nº10 exacto (500 → 250 → 375 → 312 → 281 → 296 → 304 → 300 → 302 → 301).
- No se necesitó ningún archivo del `challenge.zip` descargable (probablemente el código fuente del propio juego) para resolverlo — bastó con jugar bien.

## Referencias
- Reto: https://learn.cylabacademy.org/library/442
