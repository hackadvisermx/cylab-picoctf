# Reverse Engineering — GDB baby step 2

## Descripción
> **Prompt oficial del reto:** "Can you figure out what is in the `eax` register at the end of the `main` function? Put your answer in the academy flag format: `academy{n}` where `n` is the contents of the `eax` register in the decimal number base. If the answer was `0x11` your flag would be `academy{17}`."
>
> **Pistas:**
> 1. You could calculate `eax` yourself, or you could set a breakpoint for after the calculation and inspect `eax` to let the program do the heavy-lifting for you.

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
Se suministra un archivo binario ELF x86-64 denominado `debugger0_b`. El reto pide obtener el valor final contenido en el registro `eax` al concluir la función `main` expresado en base decimal.

Desensamblamos el binario:
```bash
objdump -d debugger0_b | grep -A 25 "<main>:"
```

Estructura de la función `main`:
```assembly
0000000000401106 <main>:
  ...
  401115: c7 45 fc da e0 01 00         	movl	$0x1e0da, -0x4(%rbp)    # a = 0x1e0da
  40111c: c7 45 f4 5f 02 00 00         	movl	$0x25f, -0xc(%rbp)      # limit = 0x25f
  401123: c7 45 f8 00 00 00 00         	movl	$0x0, -0x8(%rbp)        # i = 0
  40112a: eb 0a                        	jmp	0x401136 <main+0x30>
  40112c: 8b 45 f8                     	movl	-0x8(%rbp), %eax
  40112f: 01 45 fc                     	addl	%eax, -0x4(%rbp)        # a += i
  401132: 83 45 f8 01                  	addl	$0x1, -0x8(%rbp)        # i++
  401136: 8b 45 f8                     	movl	-0x8(%rbp), %eax
  401139: 3b 45 f4                     	cmpl	-0xc(%rbp), %eax        # i < limit ?
  40113c: 7c ee                        	jl	0x40112c <main+0x26>
  40113e: 8b 45 fc                     	movl	-0x4(%rbp), %eax        # return a
  401141: 5d                           	popq	%rbp
  401142: c3                           	retq
```

La lógica en C equivale a un bucle que acumula los números enteros desde 0 hasta `0x25f - 1` comenzando con `0x1e0da`:
$$\text{eax} = 0x1E0DA + \sum_{i=0}^{0x25F - 1} i$$

Calculamos el resultado directamente con Python:
```bash
python3 -c "
a = 0x1e0da
for i in range(0x25f):
    a += i
print('Decimal:', a)
"
# Salida: 307019
```

O ejecutando el binario en GDB inspeccionando el valor de `%eax` justo antes del retorno:
```bash
gdb ./debugger0_b
(gdb) break *0x401141
(gdb) run
(gdb) print/d $eax
$1 = 307019
```

Flag: `academy{...}`

## Notas adicionales
El registro `eax` (o `rax` en 64 bits) es el registro estándar utilizado por la convención de llamadas de x86 para almacenar el valor de retorno de una función.

## Referencias
- Reto: https://learn.cylabacademy.org/library/396
