# Reverse Engineering — Picker III

## Descripción
> **Prompt oficial del reto:** "Can you figure out how this program works to get the flag?"
>
> **Pistas oficiales:**
> 1. Is there any way to modify the function table?

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** CyLab Academy
- **Autor:** LT 'syreal' Jones

## Solución
El reto provee un script en Python (`picker-III.py`) ejecutándose en un servicio accesible mediante Netcat. El programa implementa un menú interactivo controlado por una "tabla de funciones" (`func_table`) de 4 entradas fijas de 32 caracteres cada una:

1. `print_table`
2. `read_variable`
3. `write_variable`
4. `getRandomNumber`

Además, existe una función oculta `win()` que lee el archivo `flag.txt` e imprime cada carácter en formato hexadecimal.

### 1. Análisis de la vulnerabilidad
La función `write_variable()` solicita el nombre de una variable y su nuevo valor, ejecutando:
```python
exec('global ' + var_name + '; ' + var_name + ' = ' + value)
```

Aunque `filter_value(value)` restringe el uso de caracteres como `;`, `(`, y `)`, es posible sobrescribir directamente la variable global `func_table`. La función `check_table()` exige únicamente que la longitud total sea exactamente `FUNC_TABLE_ENTRY_SIZE * FUNC_TABLE_SIZE = 32 * 4 = 128` caracteres.

### 2. Explotación
Sobrescribiendo `func_table` con el nombre de la función `win` relleno con espacios hasta alcanzar la longitud esperada, al seleccionar la opción `1` del menú se invocará `win()` en lugar de `print_table()`.

Script de interacción y decodificación:

```python
import socket
import re

s = socket.create_connection(("<host>", <puerto>))
f = s.makefile('rw', buffering=1)

# Esperar prompt
while "==> " not in f.readline():
    pass

# Seleccionar write_variable
f.write("3\n")
f.write("func_table\n")

# Enviar cadena de 128 caracteres con 'win' en el primer slot
f.write("'" + "win" + " " * 125 + "'\n")

# Ejecutar opción 1 (invoca win())
f.write("1\n")

# Leer respuesta y decodificar hex
resp = f.read()
hex_vals = re.findall(r'0x[0-9a-fA-F]+', resp)
flag = ''.join(chr(int(h, 16)) for h in hex_vals)
print("Flag:", flag)
```

Al decodificar la secuencia de enteros hexadecimales impresos por `win()`, se obtiene la bandera en formato `academy{...}`.

## Notas adicionales
- Esta vulnerabilidad ilustra los riesgos asociados al uso de `exec()` para asignar variables dinámicas a partir de datos no confiables.

## Referencias
- Reto: https://learn.cylabacademy.org/library/402
- Python eval/exec security considerations: https://docs.python.org/3/library/functions.html#eval
