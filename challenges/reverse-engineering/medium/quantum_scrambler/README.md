# Reverse Engineering — Quantum Scrambler

## Descripción
> **Prompt oficial del reto:** "We invented a new cypher that uses \"quantum entanglement\" to encode the flag. Do you have what it takes to decode it?
> Connect to the program with netcat:
>
> `$ nc xebec.cylabacademy.net 19133`
>
> The program's source code can be downloaded [here](https://challenge-files.cylabacademy.net/library/49eed5a0c24a96d414eea14fbd48e5d083bc01eae78b1f751ab89ebfbfa3f405/quantum_scrambler.py)."
>
> **Pistas oficiales:**
> 1. Run `eval` on the cypher to interpret it as a python object
> 2. Print the outer list one object per line
> 3. Feed in a known plaintext through the scrambler

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** Michael Crotty

## Solución
El reto expone un servicio por red mediante netcat que envía una extensa estructura de listas anidadas generada por el script `quantum_scrambler.py`.

### Análisis del algoritmo en `quantum_scrambler.py`

El script implementa las siguientes funciones principales:

1. **Codificación de caracteres (`get_flag`):**
   Convierte cada carácter de la bandera en su representación hexadecimal ASCII y la encapsula como una lista de un solo elemento:
   ```python
   hex_flag = [[str(hex(ord(c)))] for c in flag]
   ```

2. **Mezclado de listas (`scramble`):**
   ```python
   def scramble(L):
       A = L
       i = 2
       while i < len(A):
           A[i-2] += A.pop(i-1)
           A[i-1].append(A[:i-2])
           i += 1
       return L
   ```
   - El bucle fusiona elementos mediante concatenación de listas (`+=`) y añade referencias recursivas/anidadas a prefijos anteriores (`A[:i-2]`).
   - Los valores hexadecimales originales nunca son transformados ni destruidos; únicamente son reubicados y rodeados de sublistas accesorias.

3. **Reversibilidad y extracción:**
   Para recuperar los valores hexadecimales en el orden correcto original, basta con recorrer la lista exterior y descartar las sublistas anidadas añadidas por `.append(A[:i-2])`, concatenando únicamente las cadenas hexadecimales en su orden lineal.

### Script de resolución (Python)

```python
import itertools
import socket

HOST = "xebec.cylabacademy.net"
PORT = 19133

# Obtener los datos codificados desde el endpoint remoto
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
raw_data = b""
while True:
    chunk = s.recv(4096)
    if not chunk:
        break
    raw_data += chunk
s.close()

# Evaluar la representación textual como estructura nativa de Python
cypher = eval(raw_data.decode("utf-8").strip())

def unscramble(L):
    A = L
    for a in A:
        for idx, elem in enumerate(a):
            if isinstance(elem, list):
                a.pop(idx)
    return list(itertools.chain.from_iterable(A))

# Reconstruir la bandera a partir de los valores hexadecimales
hex_vals = unscramble(cypher)
flag = "".join(chr(int(h, 16)) for h in hex_vals)
print(flag)
```

Al ejecutar el script de resolución:

```bash
python3 solve.py
```

Se obtiene la bandera completa con formato `academy{...}`.

## Notas adicionales
El nombre "Quantum Scrambler" y la mención a "quantum entanglement" son elementos alegóricos del reto. Dado que la operación subyacente no es más que una reorganización de listas en memoria en CPython, no se requiere ningún cálculo de física cuántica ni computación especializada para revertir la estructura.

## Referencias
- Reto: https://learn.cylabacademy.org/library/479
- Apoyo: https://docs.python.org/3/tutorial/datastructures.html
