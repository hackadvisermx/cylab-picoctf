# Artificial Intelligence — Perceptron Train XOR

## Descripción
> **Prompt oficial del reto:** "Watch a perceptron learn in real time on XOR data using the classic update rule: only misclassified points trigger updates, with no weight decay. Because XOR is not linearly separable, a single perceptron cannot hit 100% accuracy. Reach `75%` accuracy to prove you understand the limitation and reveal the flag."

> **Hints:**
> 1. You get `16` updates per run, and correctly classified points do not change the model in the classic rule.
> 2. The learning-rate sweep is wide (`0.02` through `20.0`), so very high values can swing the boundary aggressively.
> 3. XOR cannot be perfectly separated by one line; `75%` is the best achievable target for this setup.
> 4. Use the slider to sweep the range and watch how the decision boundary moves between misclassification updates.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
La función XOR (OR exclusivo) es el ejemplo histórico más célebre (señalado por Minsky y Papert en 1969) de un problema no linealmente separable:
- Puntos clase 0: $(-2, -2)$ y $(2, 2)$
- Puntos clase 1: $(-2, 2)$ y $(2, -2)$

Cualquier línea recta que divida el plano solo puede separar como máximo 3 de los 4 puntos de forma simultánea, dando una cota superior de precisión del 75%. El objetivo del reto es alcanzar dicha precisión máxima del 75% (`successThreshold: 0.75`).

A través del endpoint `POST /train`, enviamos una solicitud de entrenamiento:

```python
import requests

url = "http://<host>:<puerto>/train"

for lr_100 in range(2, 2001, 1):
    lr = round(lr_100 * 0.01, 2)
    resp = requests.post(url, json={"learningRate": lr}).json()
    if resp.get("accuracy", 0) >= 0.75:
        print(f"Precisión máxima alcanzada con lr={lr}: {resp.get('flag')}")
        break
```

Con una tasa de aprendizaje de $\eta = 0.02$, el modelo clasifica 3 puntos correctamente dentro de los 16 pasos, cumpliendo el umbral de éxito y revelando la flag.

Flag: `academy{...}`

## Notas adicionales
El archivo `/config.json` describe la configuración del dataset XOR, los límites de la tasa de aprendizaje ($\eta \in [0.02, 20.0]$) y el límite de 16 iteraciones.

## Referencias
- Reto: https://learn.cylabacademy.org/library/782
