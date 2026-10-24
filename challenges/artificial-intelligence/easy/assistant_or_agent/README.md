# Artificial Intelligence — Assistant or Agent?

## Descripción
> **Prompt oficial del reto:** "Return to Westbrook High in this playful AI ethics interactive fiction. Learn when an AI assistant should advise, when an AI agent should act, and how permissions, guardrails, and review checkpoints keep autonomous actions safe."

> **Hints:**
> 1. The game pauses frequently. Press Enter at each continue prompt.
> 2. Agent mode can change the world. Assistant mode can only suggest.
> 3. A safe path usually includes approvals and limits before actions.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El reto consiste en una historia interactiva (interactive fiction) por terminal mediante `nc`. A lo largo de la historia, el protagonista Ren debe tomar decisiones sobre cómo utilizar la IA llamada ARIA para organizar el evento "Community Cleanup Night", evaluando las diferencias entre un asistente de IA (que solo redacta y aconseja) y un agente autónomo de IA (que ejecuta herramientas y realiza acciones con efectos secundarios).

Siguiendo los principios de seguridad en IA (human-in-the-loop, guardrails y control de presupuesto), las decisiones correctas son:
1. **Escena 1 (Horarios):** Opción `c` — Usar ARIA como agente, pero con un punto de control y aprobación humana (*approval checkpoint*) antes de enviar mensajes reales a los voluntarios.
2. **Escena 2 (Búsqueda de fuentes):** Opción `b` — Pedir a ARIA en modo agente que navegue por fuentes aprobadas, recopile citas y proporcione un paquete de verificación con niveles de confianza.
3. **Escena 3 (Presupuesto de refrigerios):** Opción `b` — Permitir a ARIA hacer el pedido con límites estrictos (*guardrails*): tope de $120, tiendas aprobadas y confirmación requerida ante cualquier sustitución.

Al completar todas las escenas de manera segura y responder a la reflexión final, el juego imprime la bandera.

```bash
nc <host> <puerto>
# Responder c en la Escena 1
# Responder b en la Escena 2
# Responder b en la Escena 3
```

Script de automatización en Python:
```python
import socket
import re

s = socket.create_connection(('<host>', <puerto>), timeout=10)
choices = ['c', 'b', 'b']
idx = 0

buf = ""
while True:
    data = s.recv(4096).decode('utf-8', errors='ignore')
    if not data:
        break
    buf += data
    if '(Press Enter to continue...)' in buf:
        s.sendall(b'\n')
        buf = ""
    elif re.search(r'\[[a-zA-Z/]+\]\s*>', buf):
        s.sendall(choices[idx].encode('utf-8') + b'\n')
        idx += 1
        buf = ""
```

Flag obtenida: `academy{...}`

## Notas adicionales
- El reto refuerza conceptos clave de seguridad en agentes de IA: control de permisos, aislamiento de entornos, limitación de presupuestos y supervisión humana en tareas con efectos en el mundo real.

## Referencias
- Reto en CyLab: https://learn.cylabacademy.org/library/768
