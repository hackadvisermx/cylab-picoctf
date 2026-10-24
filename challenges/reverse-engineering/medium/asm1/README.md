# Reverse Engineering — asm1

## Descripción
> **Prompt oficial del reto:** "What does asm1(0x51d) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. [Source](https://challenge-files.cylabacademy.net/library/618d41beba1f89e61dc92c5d0125189c1a0435eeeed75645a56824e092667930/test.S)"
>
> **Pistas oficiales:**
> 1. assembly [conditions](https://www.tutorialspoint.com/assembly_programming/assembly_conditions.htm)

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Sanjay C

## Solución
El reto proporciona un archivo en ensamblador x86 de 32 bits (`test.S`) con la sintaxis de Intel y solicita determinar el valor de retorno de la función `asm1` cuando recibe como argumento `0x51d`.

### Código fuente de `asm1`

```assembly
asm1:
	<+0>:	push   ebp
	<+1>:	mov    ebp,esp
	<+3>:	cmp    DWORD PTR [ebp+0x8],0x6b1
	<+10>:	jg     0x11a2 <asm1+37>
	<+12>:	cmp    DWORD PTR [ebp+0x8],0x281
	<+19>:	jne    0x119a <asm1+29>
	<+21>:	mov    eax,DWORD PTR [ebp+0x8]
	<+24>:	add    eax,0x7
	<+27>:	jmp    0x11b9 <asm1+60>
	<+29>:	mov    eax,DWORD PTR [ebp+0x8]
	<+32>:	sub    eax,0x7
	<+35>:	jmp    0x11b9 <asm1+60>
	<+37>:	cmp    DWORD PTR [ebp+0x8],0x7be
	<+44>:	jne    0x11b3 <asm1+54>
	<+46>:	mov    eax,DWORD PTR [ebp+0x8]
	<+49>:	sub    eax,0x7
	<+52>:	jmp    0x11b9 <asm1+60>
	<+54>:	mov    eax,DWORD PTR [ebp+0x8]
	<+57>:	add    eax,0x7
	<+60>:	pop    ebp
	<+61>:	ret
```

### Rastreo paso a paso con entrada `0x51d`

En la convención de llamadas cdecl de 32 bits, el primer argumento de la función se encuentra en `[ebp+0x8]`.
Por lo tanto, `[ebp+0x8] = 0x51d` (en base 10: 1309).

1. **Línea `<+3>`:** `cmp DWORD PTR [ebp+0x8], 0x6b1`
   - Compara `0x51d` (1309) con `0x6b1` (1713).
   - Como $1309 \ngtr 1713$, la condición `jg` (*jump if greater*) no se cumple.
   - La ejecución continúa en `<+12>`.

2. **Línea `<+12>`:** `cmp DWORD PTR [ebp+0x8], 0x281`
   - Compara `0x51d` (1309) con `0x281` (641).
   - Como $1309 \neq 641$, la condición `jne` (*jump if not equal*) **se cumple**.
   - El salto a `<+29>` (`0x119a`) se ejecuta.

3. **Línea `<+29>`:** `mov eax, DWORD PTR [ebp+0x8]`
   - Carga el valor `0x51d` en el registro `eax`.

4. **Línea `<+32>`:** `sub eax, 0x7`
   - Resta `0x7` al valor cargado en `eax`:
   $$\text{eax} = 0\text{x}51\text{d} - 0\text{x}7$$

5. **Línea `<+35>`:** `jmp 0x11b9 <asm1+60>`
   - Salta directamente al epílogo de la función en `<+60>`.

6. **Línea `<+60>` y `<+61>`:**
   - `pop ebp`
   - `ret`: Retorna el contenido del registro `eax`.

### Formato de entrega

El prompt indica explícitamente:
"Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format."

Por lo tanto, la bandera a enviar es el valor de retorno en hexadecimal con su prefijo `0x`:
```text
0x...
```

## Notas adicionales
En arquitecturas x86 de 32 bits, el registro `eax` almacena de forma estandarizada el valor de retorno para tipos enteros y punteros. Las instrucciones condicionales `jg` y `jne` evalúan los registros de estado (*EFLAGS*) configurados previamente por la instrucción `cmp`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/20
- Apoyo: https://www.felixcloutier.com/x86/cmp
- Apoyo: https://www.felixcloutier.com/x86/jcc
