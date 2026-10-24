# Reverse Engineering — Bit-O-Asm-1

## Descripción
> **Prompt oficial del reto:** "Can you figure out what is in the `eax` register? Put your answer in the academy flag format: `academy{n}` where `n` is the contents of the `eax` register in the decimal number base. If the answer was `0x11` your flag would be `academy{17}`. Download the assembly dump [here](https://challenge-files.cylabacademy.net/library/f24a79de39123fb31928d2d4baf2de2385e587d089b95005083051f9afb90fa9/disassembler-dump0_a.txt)."
>
> **Pistas oficiales:**
> 1. As with most assembly, there is a lot of noise in the instruction dump. Find the one line that pertains to this question and don't second guess yourself!

- **Categoría:** Reverse Engineering
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona un volcado de desensamblado x86_64 en sintaxis Intel (`disassembler-dump0_a.txt`). El objetivo es determinar el valor almacenado en el registro `eax` al finalizar la ejecución de la función y formatearlo en decimal dentro del formato `academy{n}`.

### Análisis del desensamblado

El archivo contiene las siguientes instrucciones:

```assembly
<+0>:     endbr64 
<+4>:     push   rbp
<+5>:     mov    rbp,rsp
<+8>:     mov    DWORD PTR [rbp-0x4],edi
<+11>:    mov    QWORD PTR [rbp-0x10],rsi
<+15>:    mov    eax,0x30
<+20>:    pop    rbp
<+21>:    ret
```

1. **Prólogo de función (`<+0>` a `<+5>`):** Se prepara el stack frame (`push rbp; mov rbp, rsp`).
2. **Parámetros (`<+8>` a `<+11>`):** Se guardan los argumentos pasados en `edi` y `rsi` en el stack local.
3. **Carga en `eax` (`<+15>`):**
   ```assembly
   <+15>:    mov    eax,0x30
   ```
   La instrucción `mov eax, 0x30` carga de forma inmediata la constante hexadecimal `0x30` en el registro acumulador `eax`.
4. **Epílogo y retorno (`<+20>` a `<+21>`):** Se restaura el frame pointer (`pop rbp`) y se ejecuta `ret`, devolviendo el control al llamador con el valor de `eax` intacto (en las convenciones de llamada System V AMD64, el valor de retorno de una función se ubica precisamente en `rax`/`eax`).

### Conversión a base decimal

El valor hexadecimal `0x30` en base decimal:
$$3 \times 16^1 + 0 \times 16^0 = 48$$

Por tanto, el contenido de `eax` es `48`.

```bash
# Inspección del archivo descargado
cat disassembler-dump0_a.txt

# Conversión directa en Python o shell
python3 -c "print(int('0x30', 16))"
# Salida: 48
```

La flag final tiene la estructura `academy{...}`.

## Notas adicionales
- Este reto introduce la lectura básica de instrucciones de transferencia de datos (`mov`) en arquitectura x86_64 y la convención de que `eax` actúa como el registro de retorno de funciones enteras de 32 bits.

## Referencias
- Reto: https://learn.cylabacademy.org/library/391
- Intel 64 and IA-32 Architectures Software Developer Manual: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
