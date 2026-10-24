# Reverse Engineering — GDB Test Drive

## Descripción
> **Prompt oficial del reto:** "Can you get the flag? Download this binary. Here's the test drive instructions:
> - `$ chmod +x gdbme`
> - `$ gdb gdbme`
> - `(gdb) layout asm`
> - `(gdb) break *(main+99)`
> - `(gdb) run`
> - `(gdb) jump *(main+104)`"
>
> **Pistas oficiales:**
> (Ninguna pista proporcionada en la plataforma)

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona un binario ejecutable ELF de 64 bits llamado `gdbme`.

### 1. Análisis estático del flujo de ejecución
Al desensamblar `main` con `objdump`:

```bash
objdump -d gdbme | grep -A 35 "<main>:"
```

Se observa lo siguiente:
```assembly
1325: movl   $0x186a0, %edi    ; 100000 segundos
132a: callq  sleep@plt         ; Pausa de larga duración
132f: leaq   -0x30(%rbp), %rax
1333: movq   %rax, %rsi
1336: movl   $0x0, %edi
133b: callq  rotate_encrypt    ; Cifrado / descifrado de la bandera
1355: callq  fputs@plt         ; Imprime la bandera en stdout
```

El programa entra deliberadamente en una suspensión de `100,000` segundos antes de invocar la rutina de descifrado e imprimir la bandera. Las instrucciones provistas en la descripción demuestran cómo omitir la llamada a `sleep()` usando GDB mediante un salto incondicional (`jump *(main+104)`).

### 2. Análisis del cifrado (ROT47)
La función `rotate_encrypt` implementa la rotación de caracteres ASCII imprimibles (ROT47):
$$((\text{char} - 33 + 47) \pmod{94}) + 33$$

Al reconstruir estáticamente los valores de 64 bits cargados en `[rbp - 0x30]` a `[rbp - 0x18]`:

```python
import struct

part1 = struct.pack('<Q', 0x4c4a3e3635323432)
part2 = struct.pack('<Q', 0x4362383846336235)
part3 = struct.pack('<Q', 0x3530624760433530)
part4 = struct.pack('<Q', 0x4e615f3232356761)
enc = part1 + part2 + part3 + part4

def rot47(s):
    res = []
    for c in s:
        if 33 <= c <= 126:
            res.append(chr(33 + ((c - 33 + 47) % 94)))
        else:
            res.append(chr(c))
    return ''.join(res)

print(rot47(enc))
```

Al aplicar ROT47 sobre la secuencia cargada en memoria, se obtiene directamente la bandera en formato `academy{...}`.

## Notas adicionales
- El comando `jump` en GDB modifica directamente el registro del puntero de instrucciones (`%rip`), permitiendo saltar bloques de código malicioso o retardos intencionales sin requerir parchear el binario en disco.

## Referencias
- Reto: https://learn.cylabacademy.org/library/273
- GDB Documentation: https://sourceware.org/gdb/current/onlinedocs/gdb.html/Jumping.html
