# Reverse Engineering — Bit-O-Asm-4

## Descripción
> **Prompt oficial del reto:** "Can you figure out what is in the `eax` register? Put your answer in the academy flag format: `academy{n}` where `n` is the contents of the `eax` register in the decimal number base. If the answer was `0x11` your flag would be `academy{17}`. Download the assembly dump [here](https://challenge-files.cylabacademy.net/library/b14a53c80d0f28fa842055ab567694917ef71b9f466545c3597aa8940284e212/disassembler-dump0_d.txt)."
>
> **Pistas oficiales:**
> 1. Don't tell anyone I told you this, but you can solve this problem without understanding the compare/jump relationship.
> 2. Of course, if you're really good, you'll only need one attempt to solve this problem.

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto presenta un fragmento de desensamblado x86_64 (`disassembler-dump0_d.txt`) que introduce bifurcaciones condicionales mediante la comparación de operandos (`cmp`) e instrucciones de salto condicional (`jle`) e incondicional (`jmp`).

### Análisis del desensamblado

```assembly
<+0>:     endbr64 
<+4>:     push   rbp
<+5>:     mov    rbp,rsp
<+8>:     mov    DWORD PTR [rbp-0x14],edi
<+11>:    mov    QWORD PTR [rbp-0x20],rsi
<+15>:    mov    DWORD PTR [rbp-0x4],0x9fe1a
<+22>:    cmp    DWORD PTR [rbp-0x4],0x2710
<+29>:    jle    0x55555555514e <main+37>
<+31>:    sub    DWORD PTR [rbp-0x4],0x65
<+35>:    jmp    0x555555555152 <main+41>
<+37>:    add    DWORD PTR [rbp-0x4],0x65
<+41>:    mov    eax,DWORD PTR [rbp-0x4]
<+44>:    pop    rbp
<+45>:    ret
```

Trazando el flujo de ejecución:
1. `<+15>`: Se asigna `0x9fe1a` (decimal `654874`) a la variable local `[rbp-0x4]`.
2. `<+22>`: Se compara el valor de `[rbp-0x4]` con la constante `0x2710` (decimal `10000`). La instrucción `cmp a, b` calcula internamente `a - b` y actualiza las banderas de estado (`EFLAGS`):
   $$\text{0x9fe1a} > \text{0x2710} \implies 654874 > 10000$$
3. `<+29>`: `jle <main+37>` (*jump if less or equal*). Dado que $654874 > 10000$, la condición de menor o igual es **falsa**. El salto **no se ejecuta**, continuando con la siguiente instrucción secuencial.
4. `<+31>`: `sub DWORD PTR [rbp-0x4], 0x65`. Se resta `0x65` (decimal `101`) del valor en memoria:
   $$\text{0x9fe1a} - \text{0x65} = 654874 - 101 = 654773 \quad (\text{0x9fdb5})$$
5. `<+35>`: `jmp <main+41>`. Salto incondicional a la dirección `<main+41>`, evitando la rama de suma en `<main+37>`.
6. `<+41>`: Se carga el valor de `[rbp-0x4]` (`654773` / `0x9fdb5`) en `eax`.
7. `<+45>`: `ret` finaliza la rutina retornando dicho valor.

### Conversión a base decimal

El resultado almacenado en `eax` al final es `654773`.

```bash
# Inspección del código
cat disassembler-dump0_d.txt

# Simulación en Python
python3 -c "
val = 0x9fe1a
limit = 0x2710
if val <= limit:
    val += 0x65
else:
    val -= 0x65
print(f'Decimal: {val}, Hex: {hex(val)}')
"
# Salida: Decimal: 654773, Hex: 0x9fdb5
```

La flag final tiene la estructura `academy{...}`.

## Notas adicionales
- Las ramas condicionales en x86 evalúan los flags aritméticos (`ZF`, `SF`, `OF`). La instrucción `jle` toma el salto si $ZF = 1$ o $SF \neq OF$. En este caso, al ser el operando izquierdo significativamente mayor que el derecho, la condición no se cumplió y se tomó la rama por defecto (*fall-through*).

## Referencias
- Reto: https://learn.cylabacademy.org/library/394
- X86 Control Flow (CMP and Jcc): https://www.felixcloutier.com/x86/cmp
