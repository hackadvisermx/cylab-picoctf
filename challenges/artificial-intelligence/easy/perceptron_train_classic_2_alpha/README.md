# Artificial Intelligence — Perceptron Train Classic 2 Alpha

## Descripción
> **Prompt oficial del reto:** "Watch a perceptron learn in real time using the classic update rule: only misclassified points trigger updates, with no weight decay. In this variant you must find `5` successful learning rates (each reaching 100% accuracy) before the flag is revealed. The dataset is still linearly separable, but it is less toy-like and the separation is less obvious. Dial in a rate, trigger a run, and the interface animates each step."

> **Hints:**
> 1. You get `16` updates per run, and correctly classified points do not change the model in the classic rule.
> 2. The learning-rate sweep is wider in this variant (`0.02` through `20.0`), so very high values can overshoot hard.
> 3. This dataset is still separable, but the points are less cleanly split than earlier variants, so rate choice matters more.
> 4. Use the slider to sweep the range and watch how the decision boundary moves between misclassification updates; there are many sweet spots that separate all points.
> 5. Binary search is a great strategy for finding a good learning rate. Try [this problem](https://learn.cylabacademy.org/library/442) to learn how to do a binary search.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
En esta versión avanzada de *Perceptron Train Classic*, el dataset contiene 12 puntos en el plano 2D que, aunque siguen siendo linealmente separables, presentan una frontera más estrecha y menos obvia. Al igual que en la variante anterior, se requiere acumular 5 tasas de aprendizaje distintas que logren una precisión del 100% dentro del límite de 16 iteraciones.

A través del endpoint `POST /train`, enviamos sucesivos valores de `learningRate` dentro de una misma sesión HTTP (`requests.Session`):

```python
import requests

session = requests.Session()
url = "http://<host>:<puerto>/train"

for lr_100 in range(2, 2001, 1):
    lr = round(lr_100 * 0.01, 2)
    resp = session.post(url, json={"learningRate": lr}).json()
    if resp.get("accuracy") == 1.0:
        print(f"Éxito con lr={lr} ({resp.get('successCount')}/5)")
        if resp.get("flag"):
            print(f"Flag: {resp.get('flag')}")
            break
```

Tasas como 0.09, 0.11, 0.12, 0.16 y 0.17 logran la separación perfecta de los 12 puntos sin rebasar el límite de pasos, alcanzando el objetivo de 5 éxitos y liberando la flag.

Flag: `academy{...}`

## Notas adicionales
El endpoint `/config.json` detalla los 12 puntos de entrenamiento y el estado inicial del modelo con pesos $[1.0, -1.0]$ y sesgo $0.0$.

## Referencias
- Reto: https://learn.cylabacademy.org/library/779
