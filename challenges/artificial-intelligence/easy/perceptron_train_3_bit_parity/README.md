# Artificial Intelligence — Perceptron Train 3-Bit Parity

## Descripción
> **Prompt oficial del reto:** "Watch a perceptron learn in real time on 3-bit parity data using the classic update rule: only misclassified points trigger updates, with no weight decay. This challenge extends the same idea into 3 dimensions, and the frontend renders the points in 3D space. Because parity is not linearly separable by one plane, a single perceptron cannot hit 100% accuracy. Reach `75%` accuracy to reveal the flag."

> **Hints:**
> 1. You get `16` updates per run, and correctly classified points do not change the model in the classic rule.
> 2. The learning-rate sweep is wide (`0.02` through `20.0`), so very high values can swing the boundary aggressively.
> 3. 3-bit parity cannot be perfectly separated by one plane; `75%` is the best achievable target for this setup.
> 4. Use the slider to sweep the range and watch how the decision plane moves between misclassification updates in the 3D plot.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El problema de paridad de 3 bits (función XOR de 3 entradas) asigna la etiqueta 1 a aquellas combinaciones con un número impar de 1s y 0 a las de número par:
- Puntos en 3D: $(\pm 2, \pm 2, \pm 2)$
- Debido a que la función de paridad no es linealmente separable mediante un único hiperplano en $\mathbb{R}^3$, un perceptrón simple no puede alcanzar una precisión del 100%. Lo máximo alcanzable geométricamente con un solo plano es 6 de los 8 puntos correctos, es decir, un 75% de precisión.

El servicio web ofrece una simulación interactiva con un endpoint `POST /train` que evalúa un ratio de aprendizaje $\eta \in [0.02, 20.0]$. Al alcanzar el umbral de éxito del 75% (`successThreshold: 0.75`), el servicio nos proporciona la flag.

Script de automatización en Python para realizar el barrido:
```python
import requests

url = "http://<host>:<puerto>/train"

for lr_100 in range(2, 2001, 5):
    lr = round(lr_100 * 0.01, 2)
    resp = requests.post(url, json={"learningRate": lr}).json()
    if resp.get("accuracy", 0) >= 0.75:
        print(f"Objetivo alcanzado con lr={lr}: {resp.get('flag')}")
        break
```

Con una tasa de aprendizaje de $\eta = 0.12$, el perceptrón alcanza la precisión requerida del 75% dentro de los 16 pasos y revela la bandera.

Flag: `academy{...}`

## Notas adicionales
La configuración obtenida en `/config.json` detalla los 8 vértices del cubo $[-2, 2]^3$ y sus etiquetas correspondientes, así como el umbral de éxito establecido en 0.75.

## Referencias
- Reto: https://learn.cylabacademy.org/library/776
