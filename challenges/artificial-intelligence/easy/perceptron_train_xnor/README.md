# Artificial Intelligence — Perceptron Train XNOR

## Descripción
> **Prompt oficial del reto:** "Watch a perceptron learn in real time on XNOR data using the classic update rule: only misclassified points trigger updates, with no weight decay. Because XNOR is not linearly separable, a single perceptron cannot hit 100% accuracy. Reach `75%` accuracy to prove you understand the limitation and reveal the flag."

> **Hints:**
> 1. You get `16` updates per run, and correctly classified points do not change the model in the classic rule.
> 2. The learning-rate sweep is wide (`0.02` through `20.0`), so very high values can swing the boundary aggressively.
> 3. XNOR cannot be perfectly separated by one line; `75%` is the best achievable target for this setup.
> 4. Use the slider to sweep the range and watch how the decision boundary moves between misclassification updates.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
La función lógica XNOR devuelve 1 si ambas entradas coinciden y 0 si son distintas:
- Puntos clase 1: $(-2, -2)$ y $(2, 2)$ (ambos negativos o ambos positivos).
- Puntos clase 0: $(-2, 2)$ y $(2, -2)$.

Al igual que ocurre con XOR, los puntos con etiqueta idéntica están situados en diagonales opuestas, lo que impide que una única línea recta separe las dos clases. Por tanto, la máxima precisión posible para un perceptrón lineal de una sola capa es de $3/4 = 75\%$.

Para resolver el reto, enviamos una solicitud de entrenamiento al endpoint `POST /train` que logre dicho 75% (`successThreshold: 0.75`).

Script de automatización en Python:
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

Incluso con una tasa de aprendizaje base como $\eta = 0.02$, el perceptrón se posiciona para clasificar correctamente 3 de los 4 puntos (75%), liberando la flag.

Flag: `academy{...}`

## Notas adicionales
El endpoint `/config.json` muestra los 4 puntos de la tabla de verdad XNOR y fija el umbral de éxito en 0.75.

## Referencias
- Reto: https://learn.cylabacademy.org/library/781
