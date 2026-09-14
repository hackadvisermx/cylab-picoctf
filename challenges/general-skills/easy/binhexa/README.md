# General Skills — binhexa

## Descripción
> **Prompt oficial:** "How well can you perform basic binary operations? Start searching for the flag here `nc <host> <puerto>`"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Nana Ama Atombo-Sackey

## Solución
El servicio genera dos números binarios aleatorios y pide, en 6 pasos consecutivos, aplicar una operación distinta (`<<`, `>>`, `+`, `-`, `*`, `/`, `&`, `|`, `^`, `~`) sobre uno de los dos números originales o sobre "Binary Number 1&2" (ambos), entregando el resultado en binario. Al final pide el resultado de la **última** operación en hexadecimal.

Se automatizó con un socket Python que en cada paso:
1. Extrae de la descripción qué operando(s) usa (`Number 1`, `Number 2`, o ambos) — **siempre a partir de los valores originales**, no del resultado acumulado de pasos anteriores, salvo cuando la propia operación es un shift/NOT sobre "el resultado".
2. Calcula el resultado en Python y lo envía en binario.
3. Al llegar al prompt final, convierte el resultado de la última operación a hexadecimal con `format(valor, 'x')`.

```python
import socket, re
s = socket.create_connection(("<host>", <puerto>))
# leer banner, extraer Binary Number 1 y 2
# por cada "Operation N/6": detectar operador y operando(s) por texto, calcular, enviar en binario
# al final: enviar format(ultimo_resultado, 'x')
```

Flag: `picoCTF{b1tw^3se_0p3eR@tI0n_su33essFuL_d6f8047e}`

## Notas adicionales
- Los números binarios y el orden/tipo de las 6 operaciones son **aleatorios en cada conexión**, así que no sirve memorizar una secuencia fija de respuestas — el script tiene que parsear el enunciado de cada pregunta dinámicamente.
- Operadores vistos en una ejecución: `<<`, `>>`, `+`, `*`, `&`, `|` (posiblemente también aparezcan `-`, `/`, `^`, `~`/NOT en otras ejecuciones, dado que el enunciado dice "unique operations").

## Referencias
- Reto: https://learn.cylabacademy.org/library/404
