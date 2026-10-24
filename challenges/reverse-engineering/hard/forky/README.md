# Reverse Engineering — Forky

## Descripción
> **Prompt oficial del reto:** "In this program, identify the last integer value that is passed as parameter to the function doNothing()."
>
> **Pistas oficiales:**
> 1. (Sin pistas adicionales proporcionadas)

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Sanjay C / Danny T

## Solución
El reto proporciona un binario ELF de 32 bits denominado `vuln`. El objetivo consiste en identificar el último valor entero pasado a la función `doNothing()`.

### 1. Análisis del flujo del programa
Al analizar la función `main` en C equivalente:

```c
int main() {
    int *ptr = (int *)mmap(NULL, 4, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    *ptr = 1000000000;

    fork();
    fork();
    fork();
    fork();

    *ptr = *ptr + 0x499602d2;
    doNothing(*ptr);
    return 0;
}
```

Puntos clave:
1. Se reserva una región de memoria compartida (`MAP_SHARED | MAP_ANONYMOUS`) para un entero de 32 bits, inicializado en $1\,000\,000\,000$.
2. Se realizan 4 llamadas consecutivas a `fork()`. Dado que cada llamada duplica el proceso actual, el número total de procesos resultantes es:
   $$2^4 = 16 \text{ procesos}$$
3. Cada uno de los 16 procesos suma el valor constante `0x499602d2` ($1\,234\,567\,890$ en decimal) a la variable en memoria compartida.
4. Debido a que la memoria es compartida entre todos los procesos concurrentes, tras completarse las 16 operaciones de suma el valor final acumulado es:
   $$\text{Valor final} = 1\,000\,000\,000 + 16 \times 1\,234\,567\,890$$
5. Calculando en aritmética entera con signo de 32 bits (módulo $2^{32}$ con complemento a dos):
   $$1\,000\,000\,000 + 19\,753\,086\,240 = 20\,753\,086\,240$$
   $$20\,753\,086\,240 \equiv 3\,573\,217\,056 \pmod{2^{32}}$$
   $$3\,573\,217\,056 - 2^{32} = -721\,750\,240$$

El último entero con signo pasado a `doNothing()` corresponde al valor calculado modularmente. Al envolver dicho valor en el formato de bandera, se obtiene `academy{...}`.

### 2. Script de cálculo en Python

```python
initial = 1000000000
increment = 0x499602d2
processes = 2**4  # 16

raw = (initial + processes * increment) & 0xFFFFFFFF
signed_val = raw if raw < 0x80000000 else raw - 0x100000000

print(f"Resultado entero: {signed_val}")
# Flag: academy{...}
```
```

## Notas adicionales
- El reto ilustra el comportamiento de `mmap` con la bandera `MAP_SHARED` en sistemas POSIX: a diferencia de las variables normales en la pila o montón (que se copian con semántica *copy-on-write* al invocar `fork()`), los segmentos compartidos son leídos y modificados simultáneamente por todos los procesos hijos.

## Referencias
- Reto: https://learn.cylabacademy.org/library/24
- Man page mmap(2): https://man7.org/linux/man-pages/man2/mmap.2.html
- Man page fork(2): https://man7.org/linux/man-pages/man2/fork.2.html
