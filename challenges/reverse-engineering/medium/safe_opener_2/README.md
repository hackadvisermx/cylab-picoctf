# Reverse Engineering — Safe Opener 2

## Descripción
> **Prompt oficial del reto:** "What can you do with this file? I forgot the key to my safe but this file is supposed to help me with retrieving the lost key. Can you help me unlock my safe?"
>
> **Pistas oficiales:**
> 1. Download and try to decompile the file.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** Mubarak Mikail

## Solución
El reto proporciona un archivo compilado de bytecode de Java denominado `SafeOpener.class`.

### 1. Inspección del archivo de clase
Un archivo `.class` almacena constantes, nombres de clases, métodos y literales de cadena en una sección estructurada denominada *Constant Pool*.

Al inspeccionar el Constant Pool mediante desensamblado con `javap` o extrayendo literales de texto con Python o `strings`:

```bash
javap -c -v SafeOpener.class
```

O mediante un script sencillo en Python:

```python
with open('SafeOpener.class', 'rb') as f:
    content = f.read()

import re
matches = re.findall(rb'academy\{[^}]+\}', content)
for m in matches:
    print(m.decode())
```

### 2. Extracción de la bandera
A diferencia de la primera versión del reto donde la clave estaba codificada en base64, en esta versión el valor de la clave coincide directamente con la bandera en texto claro dentro de la tabla de constantes.

La clave recuperada tiene el formato `academy{...}`.

## Notas adicionales
- Los archivos `.class` de Java conservan todos los nombres de métodos, variables y literales no encriptados a menos que se apliquen herramientas de ofuscación de bytecode.

## Referencias
- Reto: https://learn.cylabacademy.org/library/375
- Java Class File Format: https://docs.oracle.com/javase/specs/jvms/se17/html/jvms-4.html
