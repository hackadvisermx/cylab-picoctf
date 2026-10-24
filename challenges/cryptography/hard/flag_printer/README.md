# Cryptography — flag_printer

## Descripción
> **Prompt oficial del reto:** "I made a program to solve a problem, but it seems too slow :(
> 
> Download the program [here](https://challenge-files.cylabacademy.net/library/97e9e5e3ae193cc9ab6e1be52bd5323a2907e17f8ad0059bcf91aa5c690a1525/flag_printer.py).
> 
> Download the message [here](https://challenge-files.cylabacademy.net/library/97e9e5e3ae193cc9ab6e1be52bd5323a2907e17f8ad0059bcf91aa5c690a1525/encoded.txt)."

- **Categoría:** Cryptography
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2024
- **Autor:** ehhthing

## Solución
El reto proporciona un script en Python (`flag_printer.py`) y una lista de pares $(x, y)$ en `encoded.txt`.
El programa intenta resolver el sistema lineal $Ap = y$ usando `numpy.linalg.solve` sobre el cuerpo finito $\mathbb{F}_p$ con $p = 7514777789$. La matriz $A$ es una matriz de Vandermonde construida a partir de las coordenadas $x$.

Dado el gran número de puntos, resolver el sistema mediante eliminación gaussiana o inversión matricial directa toma $O(n^3)$ operaciones, lo cual resulta prohibitivo en tiempo y memoria.

El problema es equivalente a la interpolación polinomial rápida de Lagrange:
Reconstruir el polinomio $f(x)$ tal que $f(x_i) = y_i \pmod p$.
Una vez hallado el polinomio, sus coeficientes corresponden a los bytes de un archivo BMP (`output.bmp`).

Utilizando técnicas de evaluación/interpolación rápida divide y vencerás (o aprovechando que las abscisas son consecutivas mediante optimizaciones basadas en factoriales en $\mathbb{F}_p$), se calculan los coeficientes en tiempo $O(n \log^2 n)$.

```python
# Esquema de interpolación rápida en SageMath
import multiprocessing as mp

p = 7514777789
X, Y = [], []
for line in open('encoded.txt').read().strip().split('\n'):
    x, y = line.split(' ')
    X.append(int(x))
    Y.append(int(y))

K = GF(p)
R = PolynomialRing(K, 'x')

# Reconstrucción recursiva de sub-productos e interpolación de Lagrange
# ...
# f = fast_interpolate(X, Y)
# open('output.bmp', 'wb').write(bytearray(f.coefficients(sparse=False)[:-1]))
```

La imagen resultante `output.bmp` contiene visualmente el texto de la flag en formato `academy{...}`.

## Notas adicionales
El reto demuestra las limitaciones prácticas del álgebra lineal estándar cuando se trata de matrices estructuradas (como Vandermonde) y la necesidad de recurrir a algoritmos especializados de teoría de números e interpolación polinomial.

## Referencias
- Reto: https://learn.cylabacademy.org/library/417
- Fast Polynomial Interpolation: https://codeforces.com/blog/entry/82953
- Writeup de referencia: https://github.com/SuperBeetleGamer/Crypto-Writeups/tree/main/picoCTF%202024/Flag_printer
