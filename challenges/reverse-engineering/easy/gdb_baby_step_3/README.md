# Reverse Engineering — GDB baby step 3

## Descripción
> **Prompt oficial del reto:** "Now for something a little different. `0x2262c96b` is loaded into memory in the `main` function. Examine byte-wise the memory that the constant is loaded in by using the GDB command `x/4xb addr`. The flag is the four bytes as they are stored in memory. If you find the bytes `0x11  0x22  0x33  0x44` in the memory location, your flag would be: `academy{0x11223344}`."
>
> **Pistas:**
> 1. You'll need to breakpoint the instruction after the memory load.
> 2. Use the gdb command `x/4xb addr` with the memory location as the address `addr` to examine.
> 3. Any registers in `addr` should be prepended with `$` like `$rbp`.
> 4. Don't use square brackets for `addr`.
> 5. What is endianness?

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto provee un archivo ejecutable ELF x86-64 llamado `debugger0_c`. El objetivo es comprender cómo se almacenan los datos multibyte en la memoria en una arquitectura *little-endian*.

Al desensamblar la función `main`:
```bash
objdump -d debugger0_c | grep -A 10 "<main>:"
```

Se observa la instrucción encargada de guardar el valor en la pila:
```assembly
0000000000401106 <main>:
  ...
  401115: c7 45 fc 6b c9 62 22         	movl	$0x2262c96b, -0x4(%rbp)
  40111c: 8b 45 fc                     	movl	-0x4(%rbp), %eax
  ...
```

Los procesadores con arquitectura x86-64 son *little-endian*, lo que significa que el byte menos significativo (*least significant byte*, LSB) se almacena en la dirección de memoria más baja, y el más significativo en la más alta:
- Constante: `0x2262c96b`
  - Byte 0 (dirección `$rbp - 4`): `0x6b`
  - Byte 1 (dirección `$rbp - 3`): `0xc9`
  - Byte 2 (dirección `$rbp - 2`): `0x62`
  - Byte 3 (dirección `$rbp - 1`): `0x22`

En una sesión interactiva de GDB:
```bash
gdb ./debugger0_c
(gdb) break *0x40111c
(gdb) run
(gdb) x/4xb $rbp-0x4
0x7fffffffdc4c: 0x6b    0xc9    0x62    0x22
```

Uniendo los 4 bytes en el orden en que residen en memoria, obtenemos `0x6bc96222`.

Flag: `academy{...}`

## Notas adicionales
El orden de bytes (*endianness*) es fundamental en ingeniería inversa y análisis de protocolos de red. Mientras que x86/x64 utiliza *little-endian*, los protocolos de red tradicionales (como TCP/IP) emplean *big-endian* (*network byte order*).

## Referencias
- Reto: https://learn.cylabacademy.org/library/397
- Endianness (Wikipedia): https://en.wikipedia.org/wiki/Endianness
