# Reverse Engineering — GDB baby step 4

## Descripción
> **Prompt oficial del reto:** "`main` calls a function that multiplies `eax` by a constant. The flag for this challenge is that constant in decimal base. If the constant you find is 0x1000, the flag will be `academy{4096}`."
>
> **Pistas:**
> 1. A function can be referenced by either its name or its starting address in gdb.

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
Se suministra un archivo binario ELF x86-64 denominado `debugger0_d`. El objetivo es inspeccionar la función invocada por `main` y determinar por qué constante se multiplica el registro `eax`.

Podemos analizar el binario mediante `gdb` o con un desensamblador estático como `objdump`:

```bash
# Desensamblar la función main y funciones auxiliares
objdump -d debugger0_d
```

En la función `main` observamos la llamada a la función auxiliar `func1`:
```assembly
000000000040111c <main>:
  ...
  40113d: 8b 45 fc                     	movl	-0x4(%rbp), %eax
  401140: 89 c7                        	movl	%eax, %edi
  401142: e8 bf ff ff ff               	callq	0x401106 <func1>
  ...
```

Inspeccionando el cuerpo de `func1` en la dirección `0x401106`:
```assembly
0000000000401106 <func1>:
  401106: f3 0f 1e fa                  	endbr64
  40110a: 55                           	pushq	%rbp
  40110b: 48 89 e5                     	movq	%rsp, %rbp
  40110e: 89 7d fc                     	movl	%edi, -0x4(%rbp)
  401111: 8b 45 fc                     	movl	-0x4(%rbp), %eax
  401114: 69 c0 69 32 00 00            	imull	$0x3269, %eax, %eax
  40111a: 5d                           	popq	%rbp
  40111b: c3                           	retq
```

La instrucción `imull $0x3269, %eax, %eax` multiplica el valor de `%eax` por la constante `0x3269`.

Convertimos dicho valor a decimal:
```bash
python3 -c "print(int('0x3269', 16))"
# Salida: 12905
```

Alternativamente con GDB:
```bash
gdb ./debugger0_d
(gdb) disassemble func1
(gdb) print/d 0x3269
```

Flag: `academy{...}`

## Notas adicionales
La convención de llamadas System V AMD64 pasa el primer argumento entero en `%rdi` (o `%edi` para enteros de 32 bits), el cual es recogido y procesado por `func1` antes de devolver el resultado en `%eax`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/398
- GDB Documentation: https://sourceware.org/gdb/current/onlinedocs/gdb.html
