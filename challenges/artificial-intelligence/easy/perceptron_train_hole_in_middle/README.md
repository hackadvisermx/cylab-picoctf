# Artificial Intelligence — Perceptron Train Hole in Middle

## Descripción
> **Prompt oficial del reto:** "Watch a perceptron learn in real time on a \"hole in the middle\" pattern: positive points surround one negative center point. The classic perceptron update rule still applies (only misclassified points trigger updates, with no weight decay), but this shape is not linearly separable by a single line. Reach `88.9%` accuracy to reveal the flag."

> **Hints:**
> 1. You get `16` updates per run, and correctly classified points do not change the model in the classic rule.
> 2. The learning-rate sweep is wide (`0.02` through `20.0`), so very high values can swing the boundary aggressively.
> 3. A single line cannot isolate the center point while keeping all surrounding points on the other side; `88.9%` (8/9) is the best achievable target here.
> 4. Use the slider to sweep the range and watch how the decision boundary moves between misclassification updates.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El conjunto de datos consta de 9 puntos en $\mathbb{R}^2$:
- 8 puntos positivos ($y = 1$) distribuidos simétricamente en un círculo exterior alrededor del origen: $(0, 3), (2, 2), (3, 0), (2, -2), (0, -3), (-2, -2), (-3, 0), (-2, 2)$.
- 1 punto negativo ($y = 0$) ubicado exactamente en el centro: $(0, 0)$.

Dado que ninguna recta puede encerrar un punto central y dejar a todos los puntos perimetrales al otro lado de la frontera de decisión, la topología no es linealmente separable. La máxima precisión teóricamente alcanzable con un perceptrón de una sola línea es clasificar 8 de los 9 puntos correctamente ($8/9 \approx 88.89\%$).

El servicio interactivo requiere alcanzar este límite teórico del 88.9% (`successThreshold: 0.8888888888888888`) dentro de los 16 pasos de entrenamiento.

Script de automatización en Python:
```python
import requests

url = "http://<host>:<puerto>/train"

for lr_100 in range(2, 2001, 1):
    lr = round(lr_100 * 0.01, 2)
    resp = requests.post(url, json={"learningRate": lr}).json()
    if resp.get("accuracy", 0) >= 0.888:
        print(f"Precisión alcanzada con lr={lr}: {resp.get('flag')}")
        break
```

Al probar con $\eta = 0.14$, el perceptrón alcanza una precisión del 88.9% y el backend entrega la flag.

Flag: `academy{...}`

## Notas adicionales
El endpoint `/config.json` muestra los 9 puntos y confirma que el umbral de éxito está fijado en $8/9$.

## Referencias
- Reto: https://learn.cylabacademy.org/library/780
