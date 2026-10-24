# Reverse Engineering — Bit-O-Asm-2

## Descripción
> **Prompt oficial del reto:** "Can you figure out what is in the `eax` register? Put your answer in the academy flag format: `academy{n}` where `n` is the contents of the `eax` register in the decimal number base. If the answer was `0x11` your flag would be `academy{17}`. Download the assembly dump [here](https://challenge-files.cylabacademy.net/library/0325d59cb3b29a78bb7872b19f37856d51973b33085362dd4fe5f4cbe7aef80c/disassembler-dump0_b.txt)."
>
> **Pistas oficiales:**
> 1. `PTR`'s or 'pointers', reference a location in memory where values can be stored.

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto presenta un fragmento de desensamblado x86_64 (`disassembler-dump0_b.txt`) donde intervienen accesos a la memoria de pila (*stack variables*) mediante direccionamiento relativo al registro base `rbp`.

### Análisis del desensamblado

```assembly
<+0>:     endbr64 
<+4>:     push   rbp
<+5>:     mov    rbp,rsp
<+8>:     mov    DWORD PTR [rbp-0x14],edi
<+11>:    mov    QWORD PTR [rbp-0x20],rsi
<+15>:    mov    DWORD PTR [rbp-0x4],0x9fe1a
<+22>:    mov    eax,DWORD PTR [rbp-0x4]
<+25>:    pop    rbp
<+26>:    ret
```

1. **Prólogo:** Se establece el marco de pila habitual (`push rbp; mov rbp, rsp`).
2. **Asignación en pila (`<+15>`):**
   ```assembly
   <+15>:    mov    DWORD PTR [rbp-0x4],0x9fe1a
   ```
   Se almacena una palabra doble (4 bytes) con el valor inmediato hexadecimal `0x9fe1a` en la dirección local de la pila `[rbp-0x4]`.
3. **Lectura de la variable a `eax` (`<+22>`):**
   ```assembly
   <+22>:    mov    eax,DWORD PTR [rbp-0x4]
   ```
   Se lee la palabra doble almacenada en `[rbp-0x4]` y se carga en el registro `eax`. Por lo tanto, `eax` toma el valor `0x9fe1a`.
4. **Epílogo y retorno:** Se desapila el frame pointer y se regresa (`ret`).

### Conversión a base decimal

El valor hexadecimal `0x9fe1a` convertido a decimal:
$$9 \times 16^4 + 15 \times 16^3 + 14 \times 16^2 + 1 \times 16^1 + 10 \times 16^0 = 654874$$

```bash
# Inspección del código desensamblado
cat disassembler-dump0_b.txt

# Cálculo del valor en decimal con Python
python3 -c "print(int('0x9fe1a', 16))"
# Salida: 654874
```

La flag final tiene la estructura `academy{...}`.

## Notas adicionales
- El especificador `DWORD PTR` indica el tamaño del operando en memoria (Double Word = 32 bits / 4 bytes). El direccionamiento `[rbp - 0x4]` representa el acceso a una variable local reservada en el marco de activación de la función.

## Referencias
- Reto: https://learn.cylabacademy.org/library/392
- X86-64 Architecture Guide: https://www.cs.virginia.edu/~evans/cs216/guides/x86.html
