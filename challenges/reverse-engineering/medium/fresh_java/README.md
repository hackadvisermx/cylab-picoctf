# Reverse Engineering — Fresh Java

## Descripción
> **Prompt oficial del reto:** "Can you get the flag?
> Reverse engineer this [Java program](https://challenge-files.cylabacademy.net/library/c4a314dfe5c08934f6cd752b3f741addebb964687c6384c5a184bb6a1411b11b/KeygenMe.class)."
>
> **Pistas oficiales:**
> 1. Use a decompiler for Java!

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona un archivo compilado de Java denominado `KeygenMe.class`. Al ejecutarlo, solicita introducir una clave ("Enter key:") y verifica si coincide con la requerida.

Podemos inspeccionar el bytecode directamente utilizando el desensamblador nativo de Java (`javap -c`) o cualquier decompilador (como CFR o Fernflower):

```bash
javap -c KeygenMe.class
```

En la salida del desensamblado del método `main`, se observa lo siguiente:
1. Verifica que la longitud de la cadena sea de 34 caracteres (`bipush 34`, `if_icmpeq`).
2. Realiza comprobaciones individuales carácter por carácter sobre cada índice utilizando `charAt(i)` y comparándolo contra un valor ASCII numérico (`bipush <ascii_code>`):
   - Índice 33: compara con `125` (`'}'`)
   - Índice 32: compara con `49` (`'1'`)
   - Índice 31: compara con `56` (`'8'`)
   - ...
   - Índice 0: compara con `97` (`'a'`)

Las comparaciones se realizan en orden inverso (desde el índice 33 hasta el 0), pero cada instrucción especifica explícitamente el índice evaluado.

### Script de extracción y reconstrucción

Podemos procesar el desensamblado con Python para mapear cada índice a su respectivo carácter:

```python
import subprocess, re

proc = subprocess.run(['javap', '-c', 'KeygenMe.class'], capture_output=True, text=True)
lines = proc.stdout.splitlines()

flag_chars = {}
curr_idx = None

for i, line in enumerate(lines):
    line = line.strip()
    if 'charAt' in line or 'invokevirtual #42' in line:
        prev = lines[i-1].strip()
        idx_match = re.search(r'(?:bipush|iconst_)\s*(\d+)', prev)
        if idx_match:
            curr_idx = int(idx_match.group(1))
        nxt = lines[i+1].strip()
        val_match = re.search(r'(?:bipush|iconst_)\s*(\d+)', nxt)
        if val_match and curr_idx is not None:
            flag_chars[curr_idx] = chr(int(val_match.group(1)))

flag = ''.join(flag_chars[k] for k in sorted(flag_chars.keys()))
print("Flag:", flag)
```

Al ordenar los caracteres de 0 a 33, se reconstruye la bandera completa en formato `academy{...}`.

```bash
python3 solve.py
```

## Notas adicionales
El bytecode de Java mantiene de forma completamente determinista los índices y códigos de comparación en la tabla de constantes e instrucciones inmediatas, por lo que no es necesario forzar la ejecución ni realizar fuerza bruta: la verificación estática directa entrega la clave exacta.

## Referencias
- Reto: https://learn.cylabacademy.org/library/271
- Apoyo: https://docs.oracle.com/javase/specs/jvms/se17/html/jvms-6.html
