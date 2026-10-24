# Artificial Intelligence — Neuron Express 2D-0

## Descripción
> **Prompt oficial del reto:** "Probe a 2D perceptron over the network. Send it integer pairs (x, y) and watch whether the neuron fires or not. Use those responses to figure out the underlying integer weights and bias, then submit your guess with the `TEST` command to earn the flag."

> **Hints:**
> 1. A perceptron fires when `w1*x + w2*y + b >= 0`. With a 2D input this is a line in the plane.
> 2. Try testing a few integer points to locate the boundary and which side returns 0 or 1.
> 3. The weights and bias are integers, so your guess should use integers too.
> 4. The `TEST` command checks every integer (x, y) input in the range.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
En este reto interactuamos con un perceptrón en dos dimensiones cuya activación viene dada por:
$$f(x, y) = \begin{cases} 1 & \text{si } w_1 x + w_2 y + b \ge 0 \\ 0 & \text{si } w_1 x + w_2 y + b < 0 \end{cases}$$

Las coordenadas de entrada $(x, y)$ están restringidas al plano discreto $[-10, 10] \times [-10, 10]$ (un total de $21 \times 21 = 441$ puntos). Disponemos de un límite de 128 consultas al servicio remoto.

Para identificar los coeficientes enteros $(w_1, w_2, b)$ eficientemente sin agotar el límite de consultas:
1. Sondeamos primero una cuadrícula gruesa de puntos espaciados (por ejemplo, combinaciones de $\{-10, -5, 0, 5, 10\}$).
2. Filtramos el espacio de búsqueda de parámetros $(w_1, w_2, b) \in [-15, 15]^2 \times [-30, 30]$ manteniendo únicamente los modelos consistentes con las observaciones.
3. Aplicamos una estrategia de *active learning* (aprendizaje activo): si varios modelos candidatos difieren en su predicción para algún punto $(x', y')$, consultamos precisamente ese punto al servidor. Esto poda rápidamente las hipótesis ambiguas.
4. En cuanto todos los candidatos restantes concuerdan en la totalidad de los 441 puntos de la cuadrícula, enviamos `TEST w1 w2 b` y obtenemos la bandera.

Script de solución en Python:
```python
import socket
import itertools

s = socket.create_connection(('<host>', <puerto>), timeout=5)

def recv_until(prompt):
    buf = ""
    while prompt not in buf:
        chunk = s.recv(1024).decode('utf-8', errors='ignore')
        if not chunk:
            break
        buf += chunk
    return buf

recv_until("(x,y)> ")
probed = {}

def probe(x, y):
    s.sendall(f"{x} {y}\n".encode())
    resp = recv_until("(x,y)> ")
    val = 1 if "fires" in resp else 0
    probed[(x, y)] = val
    return val

# Cuadrícula inicial
for x in [-10, -5, 0, 5, 10]:
    for y in [-10, -5, 0, 5, 10]:
        probe(x, y)

# Candidatos y aprendizaje activo por discrepancia
# ... (selección de puntos donde los modelos difieran hasta convergencia)
# s.sendall(f"TEST {w1} {w2} {b}\n".encode())
```

Flag obtenida: `academy{...}`

## Notas adicionales
- La técnica de discriminación activa permite encontrar la recta divisoria óptima en menos de 65 consultas, muy por debajo del límite de 128.

## Referencias
- Reto en CyLab: https://learn.cylabacademy.org/library/770
