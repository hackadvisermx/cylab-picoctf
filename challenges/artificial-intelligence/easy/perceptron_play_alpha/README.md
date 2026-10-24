# Artificial Intelligence — Perceptron Play Alpha

## Descripción
> **Prompt oficial del reto:** "Play with the weights and bias of a 2D perceptron while watching an ASCII plot update in real time. Tune the parameters so that the decision boundary separates all of the labeled points and you will earn the flag."

> **Hints:**
> 1. Start with the `POINTS` command to see the labeled data you need to classify.
> 2. Use `SET` for big changes and `ADJUST` for fine-tuning the weights.
> 3. A perceptron learns a linear boundary; look for a line that keeps class 0 points on one side and class 1 points on the other.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El reto ofrece una visualización ASCII de un conjunto de datos linealmente separable en dos dimensiones:
- **Clase 0:** $(-3, -2)$, $(-1, -1)$, $(-4, -2)$
- **Clase 1:** $(+3, +1)$, $(+2, +2)$, $(+1, +3)$

Observamos que para todos los puntos de la Clase 1 la suma de coordenadas $x + y = 4$, mientras que para los de la Clase 0 la suma cumple $x + y \le -2$.

Por lo tanto, una recta con ecuación $x + y - 1 = 0$ (o en forma de perceptrón $w_1 x + w_2 y + b \ge 0$ con $w_1 = 1$, $w_2 = 1$ y $b = -1$) separa limpiamente ambos conjuntos:
- Para cualquier punto de Clase 1: $1 \cdot x + 1 \cdot y - 1 = 4 - 1 = 3 \ge 0 \implies 1$
- Para cualquier punto de Clase 0: $1 \cdot x + 1 \cdot y - 1 \le -2 - 1 = -3 < 0 \implies 0$

Comandos ejecutados en el servicio interactivo:
```bash
SET 1 1 -1
CHECK
```

Al cumplirse el 100% de precisión en el conjunto de entrenamiento, `CHECK` imprime la bandera.

Script de solución en Python:
```python
import socket

s = socket.create_connection(('<host>', <puerto>), timeout=5)
s.sendall(b"SET 1 1 -1\n")
s.sendall(b"CHECK\n")
# Recibir respuesta y flag
```

Flag obtenida: `academy{...}`

## Notas adicionales
- Al ser linealmente separables por una recta oblicua descendente, los coeficientes de los pesos deben tener el mismo signo ($w_1 > 0, w_2 > 0$).

## Referencias
- Reto en CyLab: https://learn.cylabacademy.org/library/774
