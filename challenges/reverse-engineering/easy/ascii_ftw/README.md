# Reverse Engineering — ASCII FTW

## Descripción
> **Prompt oficial del reto:** "This program has constructed the flag using hex ascii values. Identify the flag text by disassembling the program. You can download the file from [here](https://challenge-files.cylabacademy.net/library/60ac124e46a3c8894d62ac83ba929cdebd78f28658dc91611d4aae76ad1cb41a/asciiftw)."
>
> **Pistas oficiales:**
> 1. The combined range of hex-ascii for English alphabets and numerical digits is from 30 to 7A.
> 2. Online hex-ascii converters can be helpful.

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** Abhishek Agarwal

## Solución
El binario proporcionado es un ejecutable ELF de 64 bits para Linux (`asciiftw`). Al desensamblar la función `main`, se observa cómo el programa construye la cadena de la flag byte a byte en el marco de pila utilizando valores hexadecimales de caracteres ASCII legibles.

### Desensamblado estático de `main`

Utilizando `objdump` con sintaxis Intel:

```bash
objdump -d -M intel asciiftw | grep -A 45 "<main>:"
```

Se observa la inicialización secuencial del arreglo en la pila:

```assembly
0000000000001169 <main>:
...
1184: c6 45 d0 61        mov    byte ptr [rbp - 0x30], 0x61
1188: c6 45 d1 63        mov    byte ptr [rbp - 0x2f], 0x63
118c: c6 45 d2 61        mov    byte ptr [rbp - 0x2e], 0x61
1190: c6 45 d3 64        mov    byte ptr [rbp - 0x2d], 0x64
1194: c6 45 d4 65        mov    byte ptr [rbp - 0x2c], 0x65
1198: c6 45 d5 6d        mov    byte ptr [rbp - 0x2b], 0x6d
119c: c6 45 d6 79        mov    byte ptr [rbp - 0x2a], 0x79
11a0: c6 45 d7 7b        mov    byte ptr [rbp - 0x29], 0x7b
11a4: c6 45 d8 41        mov    byte ptr [rbp - 0x28], 0x41
11a8: c6 45 d9 53        mov    byte ptr [rbp - 0x27], 0x53
11ac: c6 45 da 43        mov    byte ptr [rbp - 0x26], 0x43
11b0: c6 45 db 49        mov    byte ptr [rbp - 0x25], 0x49
11b4: c6 45 dc 49        mov    byte ptr [rbp - 0x24], 0x49
11b8: c6 45 dd 5f        mov    byte ptr [rbp - 0x23], 0x5f
11bc: c6 45 de 49        mov    byte ptr [rbp - 0x22], 0x49
11c0: c6 45 df 53        mov    byte ptr [rbp - 0x21], 0x53
11c4: c6 45 e0 5f        mov    byte ptr [rbp - 0x20], 0x5f
11c8: c6 45 e1 45        mov    byte ptr [rbp - 0x1f], 0x45
11cc: c6 45 e2 41        mov    byte ptr [rbp - 0x1e], 0x41
11d0: c6 45 e3 53        mov    byte ptr [rbp - 0x1d], 0x53
11d4: c6 45 e4 59        mov    byte ptr [rbp - 0x1c], 0x59
11d8: c6 45 e5 5f        mov    byte ptr [rbp - 0x1b], 0x5f
11dc: c6 45 e6 41        mov    byte ptr [rbp - 0x1a], 0x41
11e0: c6 45 e7 43        mov    byte ptr [rbp - 0x19], 0x43
11e4: c6 45 e8 33        mov    byte ptr [rbp - 0x18], 0x33
11e8: c6 45 e9 45        mov    byte ptr [rbp - 0x17], 0x45
11ec: c6 45 ea 30        mov    byte ptr [rbp - 0x16], 0x30
11f0: c6 45 eb 43        mov    byte ptr [rbp - 0x15], 0x43
11f4: c6 45 ec 38        mov    byte ptr [rbp - 0x14], 0x38
11f8: c6 45 ed 43        mov    byte ptr [rbp - 0x13], 0x43
11fc: c6 45 ee 7d        mov    byte ptr [rbp - 0x12], 0x7d
```

### Decodificación de los bytes

Mapeando cada byte hexadecimal cargado en `[rbp - 0x30]` hasta `[rbp - 0x12]` a su carácter ASCII correspondiente:

| Offset en Stack | Hexadecimal | Decimal | ASCII |
|---|---|---|---|
| `[rbp - 0x30]` | `0x61` | 97 | `a` |
| `[rbp - 0x2f]` | `0x63` | 99 | `c` |
| `[rbp - 0x2e]` | `0x61` | 97 | `a` |
| `[rbp - 0x2d]` | `0x64` | 100 | `d` |
| `[rbp - 0x2c]` | `0x65` | 101 | `e` |
| `[rbp - 0x2b]` | `0x6d` | 109 | `m` |
| `[rbp - 0x2a]` | `0x79` | 121 | `y` |
| `[rbp - 0x29]` | `0x7b` | 123 | `{` |
| `[rbp - 0x28]` | `0x41` | 65 | `A` |
| `[rbp - 0x27]` | `0x53` | 83 | `S` |
| `[rbp - 0x26]` | `0x43` | 67 | `C` |
| `[rbp - 0x25]` | `0x49` | 73 | `I` |
| `[rbp - 0x24]` | `0x49` | 73 | `I` |
| `[rbp - 0x23]` | `0x5f` | 95 | `_` |
| `[rbp - 0x22]` | `0x49` | 73 | `I` |
| `[rbp - 0x21]` | `0x53` | 83 | `S` |
| `[rbp - 0x20]` | `0x5f` | 95 | `_` |
| `[rbp - 0x1f]` | `0x45` | 69 | `E` |
| `[rbp - 0x1e]` | `0x41` | 65 | `A` |
| `[rbp - 0x1d]` | `0x53` | 83 | `S` |
| `[rbp - 0x1c]` | `0x59` | 89 | `Y` |
| `[rbp - 0x1b]` | `0x5f` | 95 | `_` |
| `[rbp - 0x1a]` | `0x41` | 65 | `A` |
| `[rbp - 0x19]` | `0x43` | 67 | `C` |
| `[rbp - 0x18]` | `0x33` | 51 | `3` |
| `[rbp - 0x17]` | `0x45` | 69 | `E` |
| `[rbp - 0x16]` | `0x30` | 48 | `0` |
| `[rbp - 0x15]` | `0x43` | 67 | `C` |
| `[rbp - 0x14]` | `0x38` | 56 | `8` |
| `[rbp - 0x13]` | `0x43` | 67 | `C` |
| `[rbp - 0x12]` | `0x7d` | 125 | `}` |

### Automatización con Python

```python
bytes_list = [
    0x61, 0x63, 0x61, 0x64, 0x65, 0x6d, 0x79, 0x7b,
    0x41, 0x53, 0x43, 0x49, 0x49, 0x5f, 0x49, 0x53,
    0x5f, 0x45, 0x41, 0x53, 0x59, 0x5f, 0x41, 0x43,
    0x33, 0x45, 0x30, 0x43, 0x38, 0x43, 0x7d
]
flag = bytes(bytes_list).decode('ascii')
print(flag)
```

La flag final tiene la estructura `academy{...}`.

## Notas adicionales
- Este patrón de inicialización byte a byte (*stack strings*) se utiliza con frecuencia en binarios como técnica elemental de ofuscación para evitar que herramientas como `strings` encuentren el texto en texto claro dentro de las secciones `.rodata` o `.data`. Sin embargo, al desensamblar el código estáticamente, las instrucciones de carga inmediata hacen visible cada byte.

## Referencias
- Reto: https://learn.cylabacademy.org/library/389
- ASCII Table: https://www.asciitable.com/
- Binary Disassembly with Objdump: https://sourceware.org/binutils/docs/binutils/objdump.html
