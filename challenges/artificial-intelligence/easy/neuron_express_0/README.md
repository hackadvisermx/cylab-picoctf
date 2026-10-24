# Artificial Intelligence — Neuron Express 0

## Descripción
> **Prompt oficial del reto:** "Probe a 1D perceptron over the network. Send it integers and watch whether the neuron fires or not. Use those responses to figure out the underlying weight and bias, then submit your guess with the `TEST` command to earn the flag."

> **Hints:**
> 1. A perceptron fires when `w*x + b >= 0`. With a 1D input there is only one threshold to find.
> 2. Try testing a few integers around the boundary to pin down the exact inequality.
> 3. The `TEST` command checks every integer input in the range.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El reto nos conecta a un perceptrón 1D que evalúa la función de activación de Heaviside (o función escalón):
$$f(x) = \begin{cases} 1 & \text{si } w \cdot x + b \ge 0 \\ 0 & \text{si } w \cdot x + b < 0 \end{cases}$$

El dominio de entrada está acotado al rango discreto $[-10, 10]$ y se nos permite probar hasta 128 valores enteros. Al enviar cada entero del intervalo $[-10, 10]$, observamos el estado de activación (`Perceptron fires!` vs `Perceptron stays quiet.`).

Una vez obtenido el vector de salidas para cada $x \in [-10, 10]$, basta con iterar sobre un espacio pequeño de enteros para el peso $w$ y el sesgo (*bias*) $b$, verificando cuál combinación reproduce exactamente los resultados para todos los valores del rango. Finalmente, enviamos el comando `TEST <w> <b>` para recibir la flag.

Script de solución en Python:
```python
import socket

s = socket.create_connection(('<host>', <puerto>), timeout=5)

def recv_until(prompt):
    buf = ""
    while prompt not in buf:
        chunk = s.recv(1024).decode('utf-8', errors='ignore')
        if not chunk:
            break
        buf += chunk
    return buf

recv_until("x> ")

results = {}
for x in range(-10, 11):
    s.sendall(f"{x}\n".encode())
    resp = recv_until("x> ")
    results[x] = 1 if "fires" in resp else 0

for w in range(-20, 21):
    for b in range(-20, 21):
        if w == 0 and b == 0:
            continue
        if all((1 if w * x + b >= 0 else 0) == results[x] for x in results):
            s.sendall(f"TEST {w} {b}\n".encode())
            print(s.recv(4096).decode('utf-8', errors='ignore'))
            exit()
```

Flag obtenida: `academy{...}`

## Notas adicionales
- Al ser un espacio unidimensional continuo o discreto monótono, el punto de corte divide la recta en dos semi-rectas. Cualquier escala positiva $(k \cdot w, k \cdot b)$ con $k > 0$ genera la misma frontera de decisión, por lo que existen infinitos pares válidos; el primer par entero encontrado satisface la verificación.

## Referencias
- Reto en CyLab: https://learn.cylabacademy.org/library/769
