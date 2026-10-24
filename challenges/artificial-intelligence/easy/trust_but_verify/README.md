# Artificial Intelligence — Trust But Verify

## Descripción
> **Prompt oficial del reto:** "Play through an AI ethics interactive fiction where confident AI outputs can be wrong, subtly wrong, or almost-right. Verify claims, code, and citations to learn practical habits for safe AI-assisted work."

> **Hints:**
> 1. The game pauses frequently. Press Enter at each continue prompt.
> 2. The flag is printed near the end of the story.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El reto presenta una historia interactiva (ficción interactiva sobre ética y seguridad en IA) a través de una conexión de terminal por netcat (`nc`).

En la narrativa, el estudiante Ren colabora con su asistente de IA, ARIA, para redactar una propuesta de feria de ciencias sobre contaminación plástica. En cada escena, ARIA formula respuestas de manera elocuente y con total confianza, pero con errores o sutilezas que deben ser verificadas críticamente por el usuario:
1. **Escena 1 (La estadística):** ARIA asegura que 500 millones de toneladas métricas de plástico entran a los océanos anualmente (según un supuesto informe del PNUMA). 
   - **Acción correcta:** Opción `c` (*Look it up independently first*). La cifra real ronda los 8-10 millones de toneladas (estaba errada por un factor de 50).
2. **Escena 2 (El código):** ARIA genera un script en Python para calcular el promedio anual, pero incluye un término espurio `+ 1` en el cálculo (`average = sum(data) / len(years) + 1`).
   - **Acción correcta:** Opción `b` (*Read through it carefully before running*). Inspeccionar la lógica antes de ejecutar código generado por IA.
3. **Escena 3 (La cita académica):** ARIA cita un estudio de la Dra. Heather Leslie en la Universidad Libre de Ámsterdam con detalles muy específicos, fechándolo en 2021 y como dato confirmado.
   - **Acción correcta:** Opción `b` (*Verify it anyway*). La investigación existe y es real, pero fue publicada en 2022 y con resultados preliminares.

Tras superar las tres escenas aplicando el principio de verificación rigurosa ("Trust but verify"), la historia concluye y el sistema imprime la flag.

```bash
nc <host> <puerto>
# Escena 1: c
# Escena 2: b
# Escena 3: b
# Presionar Enter en cada pausa
```

Script de automatización en Python:
```python
import socket
import re

s = socket.create_connection(('<host>', <puerto>), timeout=10)

def step(choice=None):
    buf = ""
    while True:
        chunk = s.recv(4096).decode("utf-8", errors="ignore")
        if not chunk:
            break
        buf += chunk
        if "(Press Enter to continue...)" in buf:
            s.sendall(b"\n")
            buf = ""
        m = re.search(r"\[([a-zA-Z/]+)\]\s*>", buf)
        if m:
            if choice:
                s.sendall(choice.encode("utf-8") + b"\n")
                return
            return

step("c")
step("b")
step("b")
```

Flag: `academy{...}`

## Notas adicionales
La lección central del reto refuerza que la confianza sintáctica y el tono autoritario de un modelo de lenguaje no equivalen a veracidad lógica ni fáctica: la verificación humana crítica es esencial.

## Referencias
- Reto: https://learn.cylabacademy.org/library/783
