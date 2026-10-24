# Reverse Engineering — Picker II

## Descripción
> **Prompt oficial del reto:** "Can you figure out how this program works to get the flag?"
>
> **Pistas:**
> 1. Can you do what `win` does with your input to the program?

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El programa `picker-II.py` implementa un menú interactivo que lee la entrada del usuario y la evalúa dinámicamente utilizando `eval(user_input + '()')`:
```python
def filter(user_input):
  if 'win' in user_input:
    return False
  return True

while(True):
  try:
    user_input = input('==> ')
    if( filter(user_input) ):
      eval(user_input + '()')
    else:
      print('Illegal input')
  except Exception as e:
    print(e)
    break
```

Aunque la función `filter()` bloquea el uso de la palabra `win` para evitar llamar directamente a la función que imprime la bandera, `eval()` permite ejecutar expresiones completas en Python.
Observando el código de la función `win()`, esta simplemente abre el archivo `flag.txt` y lo lee:
```python
flag = open('flag.txt', 'r').read()
```

Podemos pasar como entrada una llamada que lea e imprima el archivo directamente:
```python
print(open('flag.txt').read())
```

Al concatenar los paréntesis `()`, la expresión a evaluar se convierte en `print(open('flag.txt').read())()`. Esto imprime el contenido de `flag.txt` en pantalla y posteriormente intenta llamar al resultado `None()`, lo cual genera una excepción `TypeError: 'NoneType' object is not callable` que es atrapada por el bloque `try/except`, terminando la ejecución de forma segura tras mostrar la clave.

```bash
# Conectar al reto mediante netcat
nc xebec.cylabacademy.net <puerto>

# En el prompt '==>', enviar:
print(open('flag.txt').read())
```

Flag: `academy{...}`

## Notas adicionales
Las listas negras basadas en filtros de subcadenas simples son insuficientes para proteger funciones de evaluación dinámica (`eval`/`exec`), ya que el lenguaje permite expresar la misma funcionalidad de múltiples formas.

## Referencias
- Reto: https://learn.cylabacademy.org/library/401
