# Artificial Intelligence — Perceptron Train Classic 1

## Descripción
> **Prompt oficial del reto:** "Watch a perceptron learn in real time using the classic update rule: only misclassified points trigger updates, with no weight decay. In this variant you must find `5` successful learning rates (each reaching 100% accuracy) before the flag is revealed. Dial in a rate, trigger a run, and the interface animates each step."

> **Hints:**
> 1. You get `16` updates per run, and correctly classified points do not change the model in the classic rule.
> 2. The learning-rate sweep is wider in this variant (`0.02` through `20.0`), so very high values can overshoot hard.
> 3. Overshooting is harder in this dataset because the clusters are well separated, but you can still watch the line swing too far if the rate is very high.
> 4. Use the slider to sweep the range and watch how the decision boundary moves between misclassification updates; there are many sweet spots that separate all points.
> 5. Binary search is a great strategy for finding a good learning rate. Try [this problem](https://learn.cylabacademy.org/library/442) to learn how to do a binary search.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
En esta variante del reto de entrenamiento de perceptrón clásico, el objetivo consiste en encontrar 5 tasas de aprendizaje distintas ($\eta$) que permitan alcanzar el 100% de precisión dentro de los 16 pasos de entrenamiento.

El servidor mantiene el conteo de éxitos (`successCount` de `successTarget: 5`) a través de la sesión HTTP. Mediante el endpoint `POST /train`, enviamos sucesivos valores de `learningRate`.

Script de resolución en Python usando `requests.Session`:
```python
import requests

session = requests.Session()
url = "http://<host>:<puerto>/train"

for lr_100 in range(2, 2001, 10):
    lr = round(lr_100 * 0.01, 2)
    resp = session.post(url, json={"learningRate": lr}).json()
    if resp.get("accuracy") == 1.0:
        print(f"Éxito con lr={lr} (progreso: {resp.get('successCount')}/5)")
        if resp.get("flag"):
            print(f"Flag obtenida: {resp.get('flag')}")
            break
```

Al enviar 5 tasas de aprendizaje válidas (por ejemplo: 0.02, 0.12, 0.22, 0.32 y 0.42), el backend alcanza la cuota de 5 aciertos y retorna la flag.

Flag: `academy{...}`

## Notas adicionales
El dataset cuenta con 8 puntos distribuidos en 2 grupos bien separados, por lo que valores moderados de $\eta$ convergen rápidamente sin sobreajustar ni oscilar violentamente.

## Referencias
- Reto: https://learn.cylabacademy.org/library/778
