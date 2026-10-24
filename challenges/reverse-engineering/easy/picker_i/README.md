# Reverse Engineering — Picker I

## Descripción
> **Prompt oficial del reto:** "This service can provide you with a random number, but can it do anything else?"
>
> **Pistas:**
> 1. Can you point the program to a function that does something useful for you?

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El servicio interactivo ejecuta el script en Python `picker-I.py`, el cual implementa un bucle principal donde solicita la entrada del usuario mediante `input('==> ')` y la evalúa dinámicamente con `eval(user_input + '()')`:
```python
while(True):
  try:
    print('Try entering "getRandomNumber" without the double quotes...')
    user_input = input('==> ')
    eval(user_input + '()')
  except Exception as e:
    print(e)
    break
```

Al inspeccionar el código fuente del script, descubrimos la función `win()`:
```python
def win():
  flag = open('flag.txt', 'r').read()
  flag = flag.strip()
  str_flag = ''
  for c in flag:
    str_flag += str(hex(ord(c))) + ' '
  print(str_flag)
```

Dado que no existe ningún filtro que limite qué identificadores pueden ser invocados, simplemente ingresamos `win` en la consola interactiva. El programa llamará a `win()`, imprimiendo la bandera representada como una secuencia de valores hexadecimales correspondientes a los códigos ASCII de cada carácter:
```bash
0x61 0x63 0x61 0x64 0x65 0x6d 0x79 0x7b ...
```

Posteriormente, convertimos cada valor hexadecimal a su carácter correspondiente para obtener la bandera en texto claro.

```bash
# Conectar al reto mediante netcat
nc chatelaine.cylabacademy.net <puerto>

# En el prompt '==>', ingresar:
win

# Decodificar los valores hexadecimales obtenidos en Python:
python3 -c "
hex_data = '0x61 0x63 0x61 0x64 0x65 0x6d 0x79 ...'
print(''.join(chr(int(x, 16)) for x in hex_data.split()))
"
```

Flag: `academy{...}`

## Notas adicionales
El uso de `eval()` con datos de entrada del usuario sin validar permite la ejecución arbitraria de funciones internas dentro del espacio de nombres global del script.

## Referencias
- Reto: https://learn.cylabacademy.org/library/400
