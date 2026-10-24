# Artificial Intelligence — Perceptron Play Naught

## Descripción
> **Prompt oficial del reto:** "The points would be inseparable in just the x-dimension, but each point now has a new y-value so the set becomes linearly separable in 2D. Watch the ASCII plot update in real time as you tweak the perceptron weights and bias. Separate the labeled points with a single line to earn the flag."

> **Hints:**
> 1. Start with the `POINTS` command to see how the old 1D x-values were lifted into 2D.
> 2. Use `SET` for big changes and `ADJUST` for fine-tuning the weights.
> 3. A perceptron learns a linear boundary; look for a line that keeps class 0 points on one side and class 1 points on the other.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El reto ilustra la técnica clásica de elevación de dimensiones (*dimension lifting* / kernel trick conceptual): un conjunto de puntos que se solapan y no son linealmente separables en 1D (a lo largo del eje $x$) se vuelven perfectamente separables al proyectarlos a 2D agregando una dimensión $y$.

Al ejecutar `POINTS`, obtenemos los datos:
- **Clase 0:** $(-4, -1)$, $(0, -1)$, $(2, -1)$
- **Clase 1:** $(-1, 2)$, $(0, 2)$, $(3, 1)$, $(4, 2)$

Se aprecia que la coordenada $y$ distingue de forma absoluta ambas clases:
- Todos los puntos de Clase 0 tienen $y = -1$.
- Todos los puntos de Clase 1 tienen $y \ge 1$.

Una recta horizontal a la altura de $y = 0$ (ecuación $0 \cdot x + 1 \cdot y + 0 = 0$) separa perfectamente el espacio. En términos de pesos del perceptrón:
- $w_1 = 0$
- $w_2 = 1$
- $b = 0$

Con estos parámetros:
- Puntos Clase 0: $0 \cdot x + 1 \cdot (-1) + 0 = -1 < 0 \implies 0$ (correcto).
- Puntos Clase 1: $0 \cdot x + 1 \cdot y + 0 = y \ge 1 \ge 0 \implies 1$ (correcto).

Ejecutamos en el terminal:
```bash
SET 0 1 0
CHECK
```

El servidor confirma la clasificación perfecta del 100% de los puntos y entrega la flag.

Script de solución en Python:
```python
import socket

s = socket.create_connection(('<host>', <puerto>), timeout=5)
s.sendall(b"SET 0 1 0\n")
s.sendall(b"CHECK\n")
# Recibir respuesta y flag
```

Flag obtenida: `academy{...}`

## Notas adicionales
- El reto demuestra cómo el mapeo a una dimensión superior puede transformar un problema no linealmente separable en uno linealmente separable, principio fundamental detrás de las Support Vector Machines (SVMs) y capas ocultas en redes neuronales.

## Referencias
- Reto en CyLab: https://learn.cylabacademy.org/library/775
