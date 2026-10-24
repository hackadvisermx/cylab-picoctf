# Reverse Engineering — Powershelly

## Descripción
> **Prompt oficial del reto:** "It's not a bad idea to learn to read Powershell. We give you the output, but do you think you can find the input?"
>
> **Pistas oficiales:**
> 1. (Sin pistas adicionales proporcionadas)

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** LT 'syreal' Jones

## Solución
El reto suministra un script en PowerShell (`rev_PS.ps1`) y un archivo con el resultado de su ejecución (`output.txt`). El objetivo consiste en revertir el algoritmo para recuperar el contenido del archivo original `input.txt` y extraer la bandera.

### 1. Análisis de `rev_PS.ps1`
Al inspeccionar el script:

1. **Estructura de entrada:**
   - `input.txt` consta de 5 líneas compuestas por 264 bloques de 6 caracteres (`0` y `1`) separados por espacios.
   - Cada bloque de columna $j$ contiene 5 fragmentos de 6 bits (30 caracteres en total).
2. **Generación determinista de semillas:**
   - Semillas: `seeds[i] = ((i + 1) * 127) % 500`.
   - Constantes pseudoaleatorias: `randoms[i] = ((((i + 1) * 327) % 681) + 344) % 313`.
3. **Encadenamiento XOR:**
   - La variable `$result` se acumula secuencialmente:
     $$output_i = fun_i \oplus output_{i-1} \oplus randoms_i$$
     donde $output_{-1} = 0$.
   - Invirtiendo la operación XOR:
     $$fun_i = output_i \oplus output_{i-1} \oplus randoms_i$$
4. **Función `Scramble`:**
   - Toma los 30 bits de cada columna (`$raw`) y los permuta en una máscara de 30 pares de bits (`bm`) según el generador congruencial `y = (i * seed) % 30`.
   - Cada bit original `1` se codifica como el par binario `"11"` y cada `0` como `"00"`.
   - El resultado se interpreta como un entero de 64 bits (`[convert]::ToInt64($raw2, 2)`).
5. **Reconstrucción del texto plano:**
   - Al invertir la permutación para cada columna, los bloques de 6 bits en la primera fila adoptan únicamente dos patrones consistentes: `"100001"` (correspondiente al bit binario `0`) y `"110011"` (correspondiente al bit binario `1`).
   - Mapeando los 264 bloques de columna resultantes a sus bits binarios respectivos se obtienen $264 / 8 = 33$ bytes ASCII que revelan directamente la bandera.

### 2. Script de resolución en Python

```python
with open("output.txt") as f:
    outputs = [int(line.strip()) for line in f if line.strip()]

total = 264
seeds = [((i + 1) * 127) % 500 for i in range(total)]
randoms = [((((i + 1) * 327) % 681) + 344) % 313 for i in range(total)]

# 1. Revertir encadenamiento XOR
fun = []
prev_res = 0
for i in range(total):
    f_val = outputs[i] ^ prev_res ^ randoms[i]
    fun.append(f_val)
    prev_res = outputs[i]


# 2. Revertir Scramble por bloque
def unscramble_block(fun_val, seed):
    bin_str = bin(fun_val)[2:].zfill(60)
    bm = [bin_str[j : j + 2] for j in range(0, 60, 2)]
    raw = ["?"] * 30
    used = [False] * 30
    for i in range(30):
        y = (i * seed) % 30
        while used[y]:
            y = (y + 1) % 30
        used[y] = True
        if bm[y] == "11":
            raw[i] = "1"
        elif bm[y] == "00":
            raw[i] = "0"
    return "".join(raw)


# 3. Decodificar la secuencia binaria de la bandera
bits = ""
for col in range(total):
    raw = unscramble_block(fun[col], seeds[col])
    # '100001' representa bit 0, '110011' representa bit 1
    bits += "0" if raw[:6] == "100001" else "1"

flag_bytes = bytes([int(bits[i : i + 8], 2) for i in range(0, len(bits), 8)])
print("Flag:", flag_bytes.decode("ascii"))
```

## Notas adicionales
- Al pasar la bandera por terminal en shells como `bash` o `zsh`, es indispensable escapar caracteres especiales como `$` (`\$hel`) o encerrar la cadena en comillas simples para evitar expansiones no deseadas de variables de entorno.

## Referencias
- Reto: https://learn.cylabacademy.org/library/119
- Documentación de PowerShell (Operadores aritméticos y bitwise): https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators
