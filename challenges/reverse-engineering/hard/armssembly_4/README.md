# Reverse Engineering — ARMssembly 4

## Descripción
> **Prompt oficial del reto:** "What integer does this program print? Flag format: academy{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be academy{0055aabb}). Use argument a: 965270072"
>
> **Pistas oficiales:**
> 1. (Sin pistas adicionales proporcionadas)

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** Dylan McGire

## Solución
El reto proporciona código fuente en ensamblador ARMv8-A de 64 bits (`chall_4.S`). El programa lee un argumento entero por línea de comandos ($a = 965270072$) y evalúa una cadena de bifurcaciones condicionales a través de varias funciones anidadas.

### 1. Rastreo de la ejecución
Siguiendo el flujo del argumento $a = 965270072$:

1. En `main`:
   - Se convierte la cadena a entero con `atoi`, pasando $w_0 = 965270072$ a `func1`.
2. En `func1`:
   ```assembly
   cmp w0, 100
   bls .L2
   add w0, w0, 100
   bl  func2
   ```
   - Como $965270072 > 100$, no salta a `.L2`.
   - Suma 100: $w_0 = 965270072 + 100 = 965270172$.
   - Llama a `func2(965270172)`.
3. En `func2`:
   ```assembly
   cmp w0, 499
   bhi .L5
   ...
   .L5:
   add w0, w0, 13
   bl  func5
   ```
   - Como $965270172 > 499$, salta a `.L5`.
   - Suma 13: $w_0 = 965270172 + 13 = 965270185$.
   - Llama a `func5(965270185)`.
4. En `func5`:
   - Llama a `func8(965270185)`.
5. En `func8`:
   ```assembly
   add w0, w0, 2
   ret
   ```
   - Suma 2: $w_0 = 965270185 + 2 = 965270187$.
   - Retorna a través de la cadena de llamadas sin modificaciones adicionales.
6. En `main`:
   - El resultado $965270187$ es formateado e impreso.

### 2. Cálculo en Python

```python
a = 965270072
result = a + 100 + 13 + 2
hex_str = f"{result:08x}"

print(f"Resultado decimal: {result}")
# Flag: academy{...}
```

- $965270187_{10} = 0x3988daab_{16}$
- Bandera resultante: `academy{...}`

## Notas adicionales
- El archivo contiene funciones distractoras como `func6` (con bucles de multiplicación y división modular `udiv` hasta 899 iteraciones), las cuales no son alcanzadas por el flujo de control para este argumento.

## Referencias
- Reto: https://learn.cylabacademy.org/library/183
- Guía de arquitectura de ensamblador ARMv8: https://developer.arm.com/documentation/
