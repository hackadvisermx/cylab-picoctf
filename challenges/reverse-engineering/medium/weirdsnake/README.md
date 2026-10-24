# Reverse Engineering — weirdSnake

## Descripción
> **Prompt oficial del reto:** "I have a friend that enjoys coding and he hasn't stopped talking about a snake recently
>
> He left this [file](https://challenge-files.cylabacademy.net/library/95d371d7d45cc419952a85a855c8702bc8ebb6be6f9f8de65dde151315a5b484/snake) on my computer and dares me to uncover a secret phrase from it. Can you assist?"
>
> **Pistas oficiales:**
> 1. Download and try to reverse the python bytecode.
> 2. https://docs.python.org/3/library/dis.html

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** Junias Bonou

## Solución
El archivo proporcionado (`snake`) contiene el desensamblado del bytecode de Python 3 (generado con el módulo `dis`). Al analizar la secuencia de instrucciones paso a paso:

1. **Definición de lista de entrada (`input_list`):**
   ```python
   input_list = [21, 60, 43, 11, 86, 25, 38, 49, 33, 3, 0, 0, 57, 32, 108, 23, 48, 4, 9, 70, 7, 110, 36, 8, 108, 7, 49, 10, 4, 86, 43, 59, 121, 93, 1, 17, 58, 126, 95, 78]
   ```

2. **Construcción de la cadena clave (`key_str`):**
   - Inicia con `'J'`
   - Concatena `'_'` por la izquierda: `'_' + 'J'` -> `'_J'`
   - Concatena `'o'` por la derecha: `'_J' + 'o'` -> `'_Jo'`
   - Concatena `'3'` por la derecha: `'_Jo' + '3'` -> `'_Jo3'`
   - Concatena `'t'` por la izquierda: `'t' + '_Jo3'` -> `'t_Jo3'`

3. **Conversión a valores ordinales y expansión:**
   - Convierte cada carácter de `key_str` a su valor numérico ASCII (`ord(c)`).
   - Duplica repetidamente la lista hasta que su longitud sea mayor o igual a `len(input_list)`.

4. **Operación XOR:**
   - Realiza la operación XOR elemento a elemento entre `input_list` y `key_list`: `[a ^ b for a, b in zip(input_list, key_list)]`.
   - Convierte los enteros resultantes en caracteres con `chr()` y los concatena con `"".join()`.

### Script de resolución

```python
input_list = [21, 60, 43, 11, 86, 25, 38, 49, 33, 3, 0, 0, 57, 32, 108, 23, 48, 4, 9, 70, 7, 110, 36, 8, 108, 7, 49, 10, 4, 86, 43, 59, 121, 93, 1, 17, 58, 126, 95, 78]

key_str = 'J'
key_str = '_' + key_str
key_str = key_str + 'o'
key_str = key_str + '3'
key_str = 't' + key_str

key_list = [ord(char) for char in key_str]
while len(key_list) < len(input_list):
    key_list.extend(key_list)

result = [a ^ b for a, b in zip(input_list, key_list)]
result_text = ''.join(map(chr, result))
print(result_text)
```

Al ejecutar el script, se obtiene la bandera descifrada en formato `academy{...}`.

```bash
python3 solve.py
```

## Notas adicionales
El archivo no es un script de Python ejecutable directamente ni un `.pyc` compilado, sino la salida legible del desensamblador `dis` de CPython 3.11+. Cada bloque del bytecode se traduce directamente a construcciones de Python sin requerir descompilación con herramientas externas.

## Referencias
- Reto: https://learn.cylabacademy.org/library/428
- Apoyo: https://docs.python.org/3/library/dis.html
