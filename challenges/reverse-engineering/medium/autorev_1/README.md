# Reverse Engineering — Autorev 1

## Descripción
> **Prompt oficial del reto:** "You think you can reverse engineer? Let's test out your speed"
>
> **Pistas oficiales:**
> (Ninguna pista proporcionada en la plataforma)

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** SkrubLawd

## Solución
El reto expone un servicio por red (`nc <host> <puerto>`) que genera y transmite dinámicamente **20 ejecutables ELF x86-64 distintos en formato hexadecimal**, otorgando un límite de 10 segundos por binario para extraer un "secreto" numérico y responderlo. Debido a la restricción temporal, la resolución manual es inviable y se requiere automatización en Python.

### 1. Análisis de los binarios muestra
Al examinar uno de los binarios recibidos:
```bash
objdump -d -M intel sample.elf | grep -A 25 "<main>:"
```

Se observa el siguiente patrón recurrente en la función `main`:
```assembly
40113e: c7 45 fc 15 95 c6 b1   mov dword ptr [rbp - 0x4], 0xb1c69515
401145: c7 45 f8 00 00 00 00   mov dword ptr [rbp - 0x8], 0x0
...
401167: call scanf             ; scanf("%u", &input)
40116f: cmp dword ptr [rbp - 0x4], eax
401172: jne failed
```

El binario define una variable local en la pila inicializada con un valor inmediato de 32 bits no nulo (en este caso `0xb1c69515`, es decir `2982581525` en decimal sin signo), y compara la entrada del usuario leída mediante `scanf("%u")`.

### 2. Script de automatización
Se implementa un script en Python que interactúa vía socket TCP:
1. Lee el banner y la cadena hexadecimal de cada ronda.
2. Convierte el hex a bytes y escribe un archivo temporal.
3. Desensambla rápidamente usando `objdump` y extrae mediante expresiones regulares el valor numérico cargado en `[rbp - 0x...]`.
4. Envía el número en formato decimal al servidor.
5. Repite el proceso para las 20 rondas consecutivas.

```python
#!/usr/bin/env python3
import socket
import subprocess
import re
import os

HOST = "xebec.cylabacademy.net"
PORT = 34210

def solve():
    s = socket.create_connection((HOST, PORT))
    f = s.makefile('rw', buffering=1)
    
    banner = f.readline()
    print("Banner:", banner.strip())

    for round_num in range(1, 21):
        prompt = f.readline()
        hexdata = f.readline().strip()
        if not hexdata:
            break
        
        elf_bytes = bytes.fromhex(hexdata)
        tmp_path = f"/tmp/autorev_{round_num}.elf"
        with open(tmp_path, "wb") as elf_file:
            elf_file.write(elf_bytes)
        
        out = subprocess.check_output(['objdump', '-d', '-M', 'intel', tmp_path]).decode()
        matches = re.findall(r'mov\s+dword ptr \[rbp\s*-\s*0x[0-9a-fA-F]+\]\s*,\s*(0x[0-9a-fA-F]+)', out)
        non_zeros = [x for x in matches if int(x, 16) != 0]
        secret = int(non_zeros[0], 16)
        
        f.write(f"{secret}\n")
        f.flush()
        
        resp = f.readline()
        try:
            os.remove(tmp_path)
        except:
            pass

    remainder = f.read()
    print("Resultado:", remainder)

if __name__ == "__main__":
    solve()
```

Salida final del servicio:
```text
Round 20/20: Found secret ...
Round 20 response: What's the secret?:Correct!
Woah, how'd you do that??
Here's your flag: academy{...}
```

## Notas adicionales
- Al ejecutar `objdump` directamente sobre el archivo en disco, el tiempo de análisis por binario es de aproximadamente 20 milisegundos, permitiendo resolver las 20 rondas en menos de 4 segundos en total.

## Referencias
- Reto: https://learn.cylabacademy.org/library/754
- GNU Binary Utilities (objdump): https://sourceware.org/binutils/docs/binutils/objdump.html
