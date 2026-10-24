# Artificial Intelligence — Neuron Meet 2D-0

## Descripción
> **Prompt oficial del reto:** "Probe a 2D perceptron over the network. Send it pairs of numbers (x, y) and watch whether the neuron fires or not. Use those responses to figure out the decision boundary, then line up the last eight outputs to read the ASCII for `p` (`01110000`) and you'll earn the flag."

> **Hints:**
> 1. A 2D perceptron fires when `w1*x + w2*y + b >= 0`. You need to find the decision boundary in 2D space.
> 2. Test points to determine which side of the boundary produces 0 and which produces 1.
> 3. Remember that repeated inputs are blocked, even if they would produce the same output.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El reto extiende el concepto de *Neuron Meet 0* a dos dimensiones con coordenadas $(x, y) \in [-10.0, 10.0]^2$. El objetivo nuevamente es emitir 8 salidas consecutivas que codifiquen el carácter ASCII `'p'` (`01110000`) sin repetir pares idénticos de manera consecutiva.

Procedimiento:
1. Sondeamos las esquinas del espacio muestral para identificar qué cuadrante activa el perceptrón. Descubrimos que la zona de $(9.9, 9.9)$ genera $1$ (*fires*) y la zona de $(-9.9, -9.9)$ genera $0$ (*stays quiet*).
2. Ejecutamos el comando `RESET` para limpiar el buffer de activaciones.
3. Enviamos una secuencia de 8 puntos variando ligeramente las coordenadas para cumplir con la regla de no repetición:
   - Para el bit `0`: $(-9.9, -9.9)$
   - Para el bit `1`: $(9.9, 9.9)$
   - Para el bit `1`: $(9.8, 9.8)$
   - Para el bit `1`: $(9.7, 9.7)$
   - Para el bit `0`: $(-9.8, -9.8)$
   - Para el bit `0`: $(-9.7, -9.7)$
   - Para el bit `0`: $(-9.6, -9.6)$
   - Para el bit `0`: $(-9.5, -9.5)$

Al registrar el octavo bit, el servidor detecta el patrón `01110000` y devuelve la flag.

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

recv_until("(x,y)> ")
s.sendall(b"RESET\n")
recv_until("(x,y)> ")

seq = [
    (-9.9, -9.9), # 0
    (9.9, 9.9),   # 1
    (9.8, 9.8),   # 1
    (9.7, 9.7),   # 1
    (-9.8, -9.8), # 0
    (-9.7, -9.7), # 0
    (-9.6, -9.6), # 0
    (-9.5, -9.5), # 0
]

for x, y in seq:
    s.sendall(f"{x} {y}\n".encode())
    resp = recv_until("(x,y)> ")

print(resp)
```

Flag obtenida: `academy{...}`

## Notas adicionales
- Al ubicarnos bien dentro de los semiplanos positivo y negativo, nos aseguramos de que pequeñas perturbaciones en las entradas no crucen la frontera de decisión $w_1 x + w_2 y + b = 0$.

## Referencias
- Reto en CyLab: https://learn.cylabacademy.org/library/772
