# Reverse Engineering — ARMssembly 3

## Descripción
> **Prompt oficial del reto:** "What integer does this program print?
>
> Flag format: academy{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be academy{0055aabb})
> Use argument a: 605030239
>
> File: [chall_3.S](https://challenge-files.cylabacademy.net/library/a8f64134c86006a99b0c668c4004fde02d68233afd7144d6a750ca2bb79409be/chall_3.S)"
>
> **Pistas oficiales:**
> 1. beep boop beep boop...

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Puntos:** 130
- **ID en CyLab:** 106

## Solución
El reto proporciona código fuente en ensamblador ARMv8-A (`chall_3.S`). El programa recibe un argumento entero por línea de comandos ($a = 605030239$) y ejecuta dos funciones (`func1` y `func2`) para computar un resultado impreso con `printf`.

### 1. Análisis del código ensamblador
Al inspeccionar las funciones en `chall_3.S`:

```assembly
func2:
    sub sp, sp, #16
    str w0, [sp, 12]
    ldr w0, [sp, 12]
    add w0, w0, 3
    add sp, sp, 16
    ret
```
La función `func2(x)` simplemente suma 3 al parámetro recibido:
$$\text{func2}(x) = x + 3$$

En `func1(n)`:
```assembly
func1:
    stp x29, x30, [sp, -48]!
    mov x29, sp
    str w0, [sp, 28]      ; [sp, 28] = n (argumento)
    str wzr, [sp, 44]     ; [sp, 44] = resultado = 0
    b   .L2

.L4:
    ldr w0, [sp, 28]
    and w0, w0, 1         ; w0 = n & 1
    cmp w0, 0
    beq .L3
    ldr w0, [sp, 44]      ; si el bit menos significativo es 1
    bl  func2             ; resultado = func2(resultado) => resultado += 3
    str w0, [sp, 44]

.L3:
    ldr w0, [sp, 28]
    lsr w0, w0, 1         ; n = n >> 1 (desplazamiento lógico a la derecha)
    str w0, [sp, 28]

.L2:
    ldr w0, [sp, 28]
    cmp w0, 0
    bne .L4               ; continuar mientras n != 0
    ldr w0, [sp, 44]      ; retornar resultado
```

La lógica de `func1(n)` implementa un bucle que inspecciona cada bit de `n`. Por cada bit encendido (`1`), invoca `func2`, sumando 3 al acumulador. Por lo tanto:
$$\text{Resultado} = \text{popcount}(n) \times 3$$
donde $\text{popcount}(n)$ (peso de Hamming) es el número de bits en 1 en la representación binaria de $n$.

### Interpretación de la pista

La pista "beep boop beep boop..." hace referencia al sonido de transmisión binaria (beep = 1, boop = 0), sugiriendo que el programa realiza procesamiento a nivel de bits individuales. Esta pista confirma que el enfoque debe centrarse en analizar el comportamiento del programa bit por bit.

### 2. Cálculo en Python

```python
n = 605030239
popcount = bin(n).count("1")
res = popcount * 3
hex_str = f"{res:08x}"

print(f"Popcount: {popcount}")
print(f"Resultado decimal: {res}")
print(f"Flag: academy{{{hex_str}}}")
```

Para $n = 605030239 = 0b100100000100000000011101011111_2$:
- $\text{popcount}(605030239) = 12$
- $\text{Resultado} = 12 \times 3 = 36$
- En hexadecimal de 32 bits a 8 dígitos: `00000024`

## Notas adicionales
- El reto refuerza el reconocimiento de patrones clásicos de manipulación de bits en compiladores (desplazamiento `lsr` y máscara `and w0, w0, 1` para pruebas de paridad/bit a bit).

## Referencias
- Reto: https://learn.cylabacademy.org/library/106
- ARMv8 A64 Instruction Set Architecture: https://developer.arm.com/documentation/ddi0596/latest/
