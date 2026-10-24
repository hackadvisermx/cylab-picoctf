# Artificial Intelligence — Perceptron Play 1D Alpha

## Descripción
> **Prompt oficial del reto:** "Play with the weight and bias of a 1D perceptron on a number line. Adjust the parameters until every labeled point is classified correctly and you will earn the flag."

> **Hints:**
> 1. Start with the `POINTS` command to see the labeled data you need to classify.
> 2. `SET` changes both weight and bias at once; `ADJUST` lets you nudge them.
> 3. A 1D perceptron splits the line at a threshold; move the boundary so class 0 points stay on one side and class 1 points on the other.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El reto presenta un entorno interactivo en terminal para ajustar los parámetros de un perceptrón 1D. Al consultar los puntos etiquetados con el comando `POINTS`, obtenemos el conjunto de entrenamiento:
- Puntos de clase 0: $x \in \{-4, -2, 0\}$
- Puntos de clase 1: $x \in \{2, 3, 4\}$

Inicialmente el perceptrón arranca con $w = 1$ y $b = 0$, por lo que la frontera se sitúa en $x = 0$. Dado que la regla de activación es $w \cdot x + b \ge 0 \implies 1$, el punto $x = 0$ resulta incorrectamente clasificado como $1$ ($1 \cdot 0 + 0 = 0 \ge 0$).

Para separar estrictamente los puntos $\{0\}$ y $\{2\}$:
- Elegimos la frontera de decisión en $x = 1$.
- Con $w = 1$, necesitamos $w \cdot 1 + b = 0 \implies b = -1$.
- Para $x \le 0$: $1 \cdot x - 1 \le -1 < 0 \implies 0$ (correcto).
- Para $x \ge 2$: $1 \cdot x - 1 \ge 1 \ge 0 \implies 1$ (correcto).

Enviamos los comandos:
```bash
SET 1 -1
CHECK
```

El comando `CHECK` verifica que todos los puntos están correctamente clasificados y nos otorga la bandera.

Script de solución en Python:
```python
import socket

s = socket.create_connection(('<host>', <puerto>), timeout=5)
# Esperar prompt
s.sendall(b"SET 1 -1\n")
# Esperar actualización
s.sendall(b"CHECK\n")
print(s.recv(4096).decode('utf-8', errors='ignore'))
```

Flag obtenida: `academy{...}`

## Notas adicionales
- El reto ilustra la noción básica de margen de separación y umbral en un espacio euclidiano unidimensional. Cualquier umbral $T \in (0, 2)$ con pendiente positiva separa perfectamente las dos clases.

## Referencias
- Reto en CyLab: https://learn.cylabacademy.org/library/773
