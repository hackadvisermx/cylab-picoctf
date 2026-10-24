# Artificial Intelligence — Perceptron Train Classic 0

## Descripción
> **Prompt oficial del reto:** "Watch a perceptron learn in real time using the classic update rule: only misclassified points trigger updates, with no weight decay. This dataset is intentionally gentle, so many learning rates still converge quickly. Dial in a rate, trigger a run, and the interface will animate each step until every point is classified correctly."

> **Hints:**
> 1. You get `16` updates per run, and correctly classified points do not change the model in the classic rule.
> 2. Overshooting is harder in this dataset because the clusters are well separated, but you can still watch the line swing too far if the rate is very high.
> 3. Use the slider to sweep the range and watch how the decision boundary moves between misclassification updates; there are many sweet spots that separate all points.
> 4. Binary search is a great strategy for finding a good learning rate. Try [this problem](https://learn.cylabacademy.org/library/442) to learn how to do a binary search.

- **Categoría:** Artificial Intelligence
- **Dificultad:** Easy
- **Evento/origen:** AI Foundations I
- **Autor:** LT 'syreal' Jones

## Solución
El reto nos presenta una aplicación web interactiva que simula el algoritmo clásico de entrenamiento del perceptrón (Rosenblatt) sobre un conjunto de datos en 2D linealmente separable.

Bajo la regla clásica:
- La predicción se calcula como $\hat{y} = \text{step}(w_1 x_1 + w_2 x_2 + b)$.
- Si la clasificación es correcta ($y = \hat{y}$), no se modifican los pesos.
- Si hay un error, los pesos se actualizan: $w \leftarrow w + \eta(y - \hat{y})x$ y el sesgo: $b \leftarrow b + \eta(y - \hat{y})$.
- Se dispone de un máximo de 16 pasos por ejecución. Al alcanzar una precisión del 100% (accuracy = 1.0), el backend devuelve la bandera.

La aplicación expone el endpoint `POST /train` que recibe un JSON `{"learningRate": lr}` y devuelve el historial de pasos, la precisión obtenida y, si se alcanza el 100%, la flag.

Podemos realizar un barrido automático de la tasa de aprendizaje ($\eta \in [0.02, 2.0]$) mediante un script en Python:

```python
import requests

url = "http://<host>:<puerto>/train"
for lr_int in range(2, 201):
    lr = round(lr_int * 0.01, 2)
    resp = requests.post(url, json={"learningRate": lr}).json()
    if resp.get("accuracy") == 1.0 or resp.get("flag"):
        print(f"Éxito con lr={lr}: {resp.get('flag')}")
        break
```

Al probar con una tasa de aprendizaje suave como $\eta = 0.02$, el perceptrón converge en menos de 16 pasos y el servidor entrega la flag.

Flag: `academy{...}`

## Notas adicionales
El endpoint `GET /config.json` describe la configuración del dataset, los límites del learning rate (`lrMin: 0.02`, `lrMax: 2.0`) y el modelo inicial.

## Referencias
- Reto: https://learn.cylabacademy.org/library/777
