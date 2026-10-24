# Reverse Engineering — GDB baby step 1

## Descripción
> **Prompt oficial del reto:** "Can you figure out what is in the `eax` register at the end of the `main` function? Put your answer in the academy flag format: `academy{n}` where `n` is the contents of the `eax` register in the decimal number base. If the answer was `0x11` your flag would be `academy{17}`."
>
> **Pistas:**
> 1. gdb is a very good debugger to use for this problem and many others!
> 2. `main` is actually a recognized symbol that can be used with gdb commands.

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
Se suministra un archivo binario ELF x86-64 titulado `debugger0_a`. El objetivo consiste en inspeccionar el contenido del registro `eax` al concluir la ejecución de la función `main` y representarlo en notación decimal.

Desensamblamos el binario para examinar la función `main`:
```bash
objdump -d debugger0_a | grep -A 10 "<main>:"
```

Código desensamblado:
```assembly
0000000000001129 <main>:
    1129: f3 0f 1e fa                  	endbr64
    112d: 55                           	pushq	%rbp
    112e: 48 89 e5                     	movq	%rsp, %rbp
    1131: 89 7d fc                     	movl	%edi, -0x4(%rbp)
    1134: 48 89 75 f0                  	movq	%rsi, -0x10(%rbp)
    1138: b8 42 63 08 00               	movl	$0x86342, %eax          # imm = 0x86342
    113d: 5d                           	popq	%rbp
    113e: c3                           	retq
```

La instrucción `movl $0x86342, %eax` carga directamente el valor constante hexadecimal `0x86342` en el registro `eax`.

Convertimos el valor hexadecimal a base 10:
```bash
python3 -c "print(int('0x86342', 16))"
# Salida: 549698
```

En GDB:
```bash
gdb ./debugger0_a
(gdb) disassemble main
(gdb) print/d 0x86342
$1 = 549698
```

Flag: `academy{...}`

## Notas adicionales
En arquitecturas x86 y x86-64, la instrucción `ret` toma el valor presente en `eax` / `rax` como el código de retorno numérico de la función `main`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/395
