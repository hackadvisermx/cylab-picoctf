# General Skills — FANTASY CTF

## Descripción
> **Prompt oficial:** "Play this short game to get familiar with terminal applications and some of the most important rules in scope for picoCTF. Connect to the program with netcat: `nc <host> <puerto>`"
>
> **Hints:**
> 1. When a choice is presented like [a/b/c] choose one, for example: c and then press Enter.

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2025
- **Autor:** syreal

## Solución
No es un reto técnico: es una **novela visual/aventura de texto** ambientada en una estudiante de ficción (Eibhilin) jugando su primer CTF, cuyo objetivo real es enseñar las **reglas de picoCTF** (no crear varias cuentas, no compartir cuentas ni flags, no publicar writeups antes de que se anuncien ganadores, etc.). Cada decisión ofrece 2-3 opciones (`[a/b]` o `[a/b/c]`); eligiendo siempre la opción **correcta según las reglas del concurso** (cuenta única y privada, no compartir la flag, jugar el propio juego en vez de buscar la respuesta en internet) el juego avanza y al final revela la flag.

```bash
nc <host> <puerto>
# ... (Press Enter to continue...) varias veces
# Options:
# A) Register multiple accounts
# B) Share an account with a friend
# C) Register a single, private account   <- correcta
# [a/b/c] > c
# ...
# Options:
# A) Play the game                          <- correcta
# B) Search the Ether for the flag
# [a/b] > a
# ... (barra de progreso simulando "jugar")
# "Here's the flag I found: picoCTF{...}"
```

Flag: `picoCTF{m1113n1um_3d1710n_219b5811}`

## Notas adicionales
- Se automatizó el recorrido completo con un script Python que detecta líneas de tipo `Options:` seguidas de un prompt `[a/b/c] >` y elige la opción cuyo texto contiene palabras clave de "buena práctica" (single, private, play the game) frente a las de mala práctica (share, multiple accounts, search for the flag online).
- Sirve como recordatorio in-game de las reglas reales de picoCTF: una cuenta por participante, no compartir flags/soluciones, y esperar a que se anuncien los ganadores antes de publicar writeups — reglas que aplican igual a este propio proyecto de documentación.

## Referencias
- Reto: https://learn.cylabacademy.org/library/471
