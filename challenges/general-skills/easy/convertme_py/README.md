# General Skills — convertme.py

## Descripción
> **Prompt oficial:** "Run the Python script and convert the given number from decimal to binary to get the flag."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
El script genera un número decimal aleatorio (10-100) y pide su representación en binario. Al ejecutarlo **localmente**, se puede leer el número generado desde la propia salida del proceso y responder automáticamente con `bin(num)[2:]`.

```python
import subprocess, re
proc = subprocess.Popen(['python3','convertme.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
line = proc.stdout.readline()
num = int(re.search(r'If (\d+) is', line).group(1))
proc.stdin.write(bin(num)[2:] + "\n"); proc.stdin.flush()
print(proc.stdout.read())
```

Flag: `picoCTF{4ll_y0ur_b4535_722f6b39}`

## Notas adicionales
- Al ser un script que se ejecuta localmente (no un servicio remoto), leer su propia salida antes de responder es trivial — no hace falta calcular nada "a ciegas", basta con automatizar la interacción con el propio proceso.
- Reutiliza el mismo cifrado XOR con clave `'enkidu'` que el resto de la serie de retos de este autor (`fixme1/2.py`, `PW Crack 1/2`).

## Referencias
- Reto: https://learn.cylabacademy.org/library/239
- Fuente: `convertme.py` (copia en esta carpeta)
