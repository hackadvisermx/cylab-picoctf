# Artificial Intelligence — Neuron Meet 0

## Descripción
> **Prompt oficial del reto:** "Probe a 1D perceptron over the network. Send it numbers and watch whether the neuron fires or not. Use those responses to figure out the decision boundary, then line up the last eight outputs to read the ASCII for `p` (`01110000`) and you'll earn the flag."

> **Hints:**
> 1. A perceptron fires when `w*x + b >= 0`. With a 1D input there is only one threshold to find.
> 2. You only need values on opposite sides of the threshold to build the output pattern.
> 3. Remember that repeated inputs are blocked, even if they would produce the same output.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El reto evalúa un perceptrón 1D con rango $[-10.0, 10.0]$. El objetivo es encadenar las últimas 8 salidas del perceptrón para formar la secuencia binaria `01110000` (el carácter ASCII `'p'`). La única restricción es que no se permite enviar dos veces consecutivas el mismo valor numérico.

Para lograrlo:
1. Determinamos qué lado de la frontera de decisión activa la neurona. Probando valores en los extremos, observamos que los valores negativos grandes (p. ej. $-9.9$) producen `0` (*stays quiet*) y los positivos grandes (p. ej. $9.9$) producen `1` (*fires*).
2. Limpiamos el historial enviando el comando `RESET`.
3. Enviamos consecutivamente 8 números distintos que correspondan a los bits requeridos `01110000`:
   - Para el bit `0`: $-9.9$
   - Para el bit `1`: $9.9$
   - Para el bit `1`: $9.8$
   - Para el bit `1`: $9.7$
   - Para el bit `0`: $-9.8$
   - Para el bit `0`: $-9.7$
   - Para el bit `0`: $-9.6$
   - Para el bit `0`: $-9.5$

Al completar los 8 bits en la ventana deslizante, el servidor detecta el patrón `'p'` y entrega la bandera.

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
s.sendall(b"RESET\n")
recv_until("x> ")

# 01110000 ('p')
seq = [-9.9, 9.9, 9.8, 9.7, -9.8, -9.7, -9.6, -9.5]
for val in seq:
    s.sendall(f"{val}\n".encode())
    resp = recv_until("x> ")

print(resp)
```

Flag obtenida: `academy{...}`

## Notas adicionales
- Al alternar sutilmente los valores continuos en cada región (p. ej. decrementar o incrementar en 0.1), se evita la validación de repetición consecutiva manteniendo constante el resultado de la función escalón.

## Referencias
- Reto en CyLab: https://learn.cylabacademy.org/library/771
