# Reverse Engineering — ARMssembly 0

## Descripción
> **Prompt oficial del reto:** "What integer does this program print?
>
> Flag format: academy{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be academy{0055aabb})
> Use arguments a and b: 2432642318 and 3919355441
>
> File: [chall.S](https://challenge-files.cylabacademy.net/library/2aee1bfb8502d5360e5d9f5b6f68bbefb2a62a6e45ba42cc6a198a0eab1a71a3/chall.S)"
>
> **Pistas oficiales:**
> 1. Simple compare

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Dylan McGuire

## Solución
El reto proporciona el código fuente en ensamblador ARM64 (AArch64) compilado desde C (`chall.S`). El programa recibe dos argumentos de línea de comandos (`argv[1]` y `argv[2]`), los convierte a enteros de 32 bits mediante `atoi` y los pasa a `func1`.

### Análisis de `func1`

El código de `func1` es el siguiente:

```assembly
func1:
	sub	sp, sp, #16
	str	w0, [sp, 12]    // guarda arg1 (2432642318)
	str	w1, [sp, 8]     // guarda arg2 (3919355441)
	ldr	w1, [sp, 12]    // w1 = arg1
	ldr	w0, [sp, 8]     // w0 = arg2
	cmp	w1, w0          // compara w1 con w0
	bls	.L2             // salta a .L2 si w1 <= w0 (comparación sin signo: Branch if Lower or Same)
	ldr	w0, [sp, 12]    // si w1 > w0, retorna w1
	b	.L3
.L2:
	ldr	w0, [sp, 8]     // retorna w0
.L3:
	add	sp, sp, 16
	ret
```

1. La instrucción `cmp w1, w0` seguida de `bls` realiza una **comparación de enteros sin signo** (*unsigned comparison*).
2. `w1 = 2432642318` (`0x90ff2d0e`)
3. `w0 = 3919355441` (`0xe99c9e31`)
4. Como `2432642318 <= 3919355441` en representación sin signo de 32 bits, la condición `bls .L2` se cumple y la ejecución salta a `.L2`.
5. En `.L2`, se carga en `w0` el valor `[sp, 8]` que corresponde al segundo argumento: `3919355441`.
6. En `main`, el valor retornado por `func1` se imprime en formato decimal con `printf("Result: %ld\n", ...)`:
   ```assembly
   bl func1
   mov w1, w0
   adrp x0, .LC0
   add x0, x0, :lo12:.LC0
   bl printf
   ```

### Formato de la bandera

El prompt solicita el entero impreso convertido a hexadecimal en minúsculas, de 32 bits (relleno con ceros a la izquierda hasta 8 caracteres), sin prefijo `0x`:

```python
val = 3919355441
hex_str = f"{val:08x}"
print(f"academy{{{hex_str}}}")
```

El valor hexadecimal de `3919355441` es de 8 dígitos y se encapsula en el formato `academy{...}`.

## Notas adicionales
La instrucción `bls` (*Branch if Lower or Same*) evalúa los flags de condición `C == 0 || Z == 1`, lo que confirma que opera como comparación sin signo. Si la comparación hubiera sido con signo (`ble`), `2432642318` se habría interpretado como `-1862324978` y `3919355441` como `-375611855`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/160
- Apoyo: https://developer.arm.com/documentation/dui0801/g/Condition-Codes/Condition-code-suffixes
