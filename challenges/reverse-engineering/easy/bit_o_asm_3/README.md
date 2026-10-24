# Reverse Engineering — Bit-O-Asm-3

## Descripción
> **Prompt oficial del reto:** "Can you figure out what is in the `eax` register? Put your answer in the academy flag format: `academy{n}` where `n` is the contents of the `eax` register in the decimal number base. If the answer was `0x11` your flag would be `academy{17}`. Download the assembly dump [here](https://challenge-files.cylabacademy.net/library/f16508f6e8ba4c520e7541081aee169bf4f5cab84d6852b697299b8cf4aff76a/disassembler-dump0_c.txt)."
>
> **Pistas oficiales:**
> 1. Not everything in this disassembly listing is optimal.

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto presenta un listado de desensamblado x86_64 (`disassembler-dump0_c.txt`) que incluye operaciones aritméticas elementales (`imul` y `add`) aplicadas sobre registros y variables locales en pila.

### Análisis del desensamblado

```assembly
<+0>:     endbr64 
<+4>:     push   rbp
<+5>:     mov    rbp,rsp
<+8>:     mov    DWORD PTR [rbp-0x14],edi
<+11>:    mov    QWORD PTR [rbp-0x20],rsi
<+15>:    mov    DWORD PTR [rbp-0xc],0x9fe1a
<+22>:    mov    DWORD PTR [rbp-0x8],0x4
<+29>:    mov    eax,DWORD PTR [rbp-0xc]
<+32>:    imul   eax,DWORD PTR [rbp-0x8]
<+36>:    add    eax,0x1f5
<+41>:    mov    DWORD PTR [rbp-0x4],eax
<+44>:    mov    eax,DWORD PTR [rbp-0x4]
<+47>:    pop    rbp
<+48>:    ret
```

Trazando la ejecución paso a paso:
1. `<+15>`: Se guarda `0x9fe1a` en la dirección local `[rbp-0xc]`.
2. `<+22>`: Se guarda `0x4` en la dirección local `[rbp-0x8]`.
3. `<+29>`: Se carga el contenido de `[rbp-0xc]` en el registro `eax` ($eax = \text{0x9fe1a}$).
4. `<+32>`: La instrucción `imul eax, DWORD PTR [rbp-0x8]` multiplica con signo el registro `eax` por el valor en `[rbp-0x8]` ($0x4$):
   $$eax = 0x9fe1a \times 4 = 0x27f868$$
5. `<+36>`: La instrucción `add eax, 0x1f5` suma el inmediato `0x1f5` al registro `eax`:
   $$eax = 0x27f868 + 0x1f5 = 0x27fa5d$$
6. `<+41>` y `<+44>`: El resultado se almacena temporalmente en `[rbp-0x4]` y luego se vuelve a cargar en `eax` para ser retornado.
7. `<+48>`: `ret` finaliza la ejecución con `eax` valiendo `0x27fa5d`.

### Conversión a base decimal

Calculando en decimal:
- $\text{0x9fe1a} = 654874$
- $\text{Multiplicación por 4} = 654874 \times 4 = 2619496$
- $\text{0x1f5} = 501$
- $\text{Suma} = 2619496 + 501 = 2619997$

```bash
# Inspección del código
cat disassembler-dump0_c.txt

# Emulación de las operaciones en Python
python3 -c "
v1 = 0x9fe1a
v2 = 0x4
res = (v1 * v2) + 0x1f5
print(f'Hex: {hex(res)}, Dec: {res}')
"
# Salida: Hex: 0x27fa5d, Dec: 2619997
```

La flag final tiene la estructura `academy{...}`.

## Notas adicionales
- La pista oficial menciona que el código no es óptimo debido a que el compilador (en modo sin optimización `-O0`) almacena y vuelve a cargar redundante e innecesariamente variables en la pila entre cada paso aritmético.

## Referencias
- Reto: https://learn.cylabacademy.org/library/393
- X86 Instruction Reference (IMUL): https://www.felixcloutier.com/x86/imul
- X86 Instruction Reference (ADD): https://www.felixcloutier.com/x86/add
