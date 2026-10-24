# Reverse Engineering — ARMssembly 2

## Descripción
> **Prompt oficial del reto:** "What integer does this program print?
>
> Flag format: academy{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be academy{0055aabb})
> Use argument a: 2729572966
>
> File: [chall_2.S](https://challenge-files.cylabacademy.net/library/7a8d8249f5474ae8934f3476b1cb13f43a8735d8e88b70b754bf8c211870bfbd/chall_2.S)"
>
> **Pistas oficiales:**
> 1. Loops

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Puntos:** 90
- **ID en CyLab:** 150

## Solución

El reto proporciona el código fuente en ensamblador ARM64 (AArch64) compilado desde C (`chall_2.S`). El programa recibe un argumento de línea de comandos (`argv[1]`), lo convierte a entero de 32 bits mediante `atoi` y lo pasa a la función `func1`. El resultado se imprime con `printf`.

### Análisis de `func1`

El código de `func1` implementa un **bucle que acumula un valor**:

```assembly
func1:
    sub     sp, sp, #32           // ajusta pila
    str     w0, [sp, 12]          // w0 = argumento (2729572966)
    str     wzr, [sp, 24]         // result = 0 (sp[24])
    str     wzr, [sp, 28]         // counter = 0 (sp[28])
    b       .L2                   // salta a .L2
.L3:
    ldr     w0, [sp, 24]          // carga result
    add     w0, w0, 3             // suma 3
    str     w0, [sp, 24]          // guarda result
    ldr     w0, [sp, 28]          // carga counter
    add     w0, w0, 1             // suma 1
    str     w0, [sp, 28]          // guarda counter
.L2:
    ldr     w1, [sp, 28]          // carga counter
    ldr     w0, [sp, 12]          // carga argumento
    cmp     w1, w0                // compara counter con argumento
    bcc     .L3                   // Branch if Carry Clear (w1 < w0)
    ldr     w0, [sp, 24]          // carga result en w0 para retornar
    add     sp, sp, 32            // ajusta pila
    ret                           // retorna
```

### Flujo del programa

1. **Inicialización:**
   - `result = 0`
   - `counter = 0`

2. **Bucle:** Mientras `counter < argumento`:
   - `result += 3`
   - `counter += 1`

3. **Retorno:** Al salir del bucle, retorna `result`

### Cálculo matemático

El bucle ejecuta `argumento` veces, sumando 3 en cada iteración:

```
result = argumento * 3
result = 2729572966 * 3
result = 8188718898
```

Sin embargo, como el cálculo se realiza en **registros de 32 bits** (`w0`, `w1`), hay **desbordamiento (overflow)** según la aritmética modular de 32 bits:

```
8188718898 % 2^32 = 8188718898 % 4294967296 = 3893751602
```

En hexadecimal (8 dígitos, lowercase):

```python
result_32bit = 3893751602
hex_str = f"{result_32bit:08x}"
# hex_str = "e815ef32"
```

### Formato de la bandera

La bandera está en formato `academy{XXXXXXXX}` donde `XXXXXXXX` es el número en hexadecimal de 32 bits (en minúsculas, sin prefijo `0x`, rellenado a 8 dígitos con ceros a la izquierda):

```
Flag: academy{...}
```

## Verificación

El programa, al ejecutarse con el argumento `2729572966`, imprime:
```
Result: 3893751602
```

Convertido a hex: `0xe815ef32` → `e815ef32`

## Referencias

- Reto en CyLab: https://learn.cylabacademy.org/library/150
- ARM64 Documentation: https://developer.arm.com/documentation/dui0801/g/
- Instrucción `bcc` (Branch if Carry Clear): https://developer.arm.com/documentation/dui0801/g/Condition-Codes/Condition-code-suffixes
