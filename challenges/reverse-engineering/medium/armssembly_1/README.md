# Reverse Engineering — ARMssembly 1

## Descripción
> **Prompt oficial del reto:** "For what argument does this program print "win"?
>
> Flag format: academy{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be academy{0055aabb})
> Variables: a = 60, b = 0, c = 3
>
> File: [chall_1.S](https://challenge-files.cylabacademy.net/library/042e2374e799f3dc0d439957290320a2d53fd2485a33136211b52d303286a221/chall_1.S)"
>
> **Pistas oficiales:**
> 1. Shifts

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Pranay Garg

## Solución
El reto proporciona un archivo en ensamblador ARMv8-A (`chall_1.S`). En la función `main`, se convierte el primer argumento recibido por línea de comandos con `atoi` y se pasa a la función `func`.

Si el valor de retorno de `func` es igual a 0:
```assembly
bl func
cmp w0, 0
bne .L4
adrp x0, .LC0      // .LC0: "You win!"
bl puts
```
El objetivo es encontrar qué argumento entero hace que `func` retorne `0`.

### Desglose de la función `func`

Analizando paso a paso las operaciones en `func`:

```assembly
func:
	sub	sp, sp, #32
	str	w0, [sp, 12]     // [sp, 12] = input (el argumento del usuario)
	mov	w0, 60
	str	w0, [sp, 16]     // [sp, 16] = 60 (constante a)
	str	wzr, [sp, 20]    // [sp, 20] = 0 (constante b, wzr es el registro zero de 32 bits)
	mov	w0, 3
	str	w0, [sp, 24]     // [sp, 24] = 3 (constante c)

	ldr	w0, [sp, 20]     // w0 = 0
	ldr	w1, [sp, 16]     // w1 = 60
	lsl	w0, w1, w0       // w0 = w1 << w0 = 60 << 0 = 60
	str	w0, [sp, 28]     // [sp, 28] = 60

	ldr	w1, [sp, 28]     // w1 = 60
	ldr	w0, [sp, 24]     // w0 = 3
	sdiv	w0, w1, w0       // w0 = w1 / w0 = 60 / 3 = 20
	str	w0, [sp, 28]     // [sp, 28] = 20

	ldr	w1, [sp, 28]     // w1 = 20
	ldr	w0, [sp, 12]     // w0 = input
	sub	w0, w1, w0       // w0 = 20 - input
	str	w0, [sp, 28]     // [sp, 28] = 20 - input
	ldr	w0, [sp, 28]     // carga el resultado para retornar en w0
	add	sp, sp, 32
	ret
```

### Cálculo de la condición ganadora

Para que el programa imprima `"You win!"`, se requiere que `func` retorne `0`:
$$20 - \text{input} = 0 \implies \text{input} = 20$$

### Formato de la bandera

El formato requerido especifica:
- Representación en hexadecimal de 32 bits (8 dígitos hexadecimales).
- Letras en minúsculas.
- Sin prefijo `0x`.
- Relleno con ceros a la izquierda (`08x`).

Convertimos el valor decimal a hexadecimal de 8 caracteres con relleno de ceros a la izquierda (`08x`) y lo encapsulamos en el formato requerido:
```text
academy{...}
```

## Notas adicionales
La instrucción `wzr` en la arquitectura ARM64 representa el registro nulo (*zero register*) para operaciones de 32 bits, garantizando lectura de ceros sin necesidad de inicializar un registro general. La instrucción `sdiv` realiza división entera con signo (*signed divide*).

## Referencias
- Reto: https://learn.cylabacademy.org/library/111
- Apoyo: https://developer.arm.com/documentation/dui0801/g/A64-General-Instructions/SDIV
