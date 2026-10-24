# Reverse Engineering — ARMssembly 4

## Descripción
> **Prompt oficial del reto:** "What integer does this program print?
>
> Flag format: academy{XXXXXXXX} → (hex, minúsculas, sin 0x, 32 bits. ej. 5614267 sería academy{0055aabb}).
>
> Usar argumento a: 965270072"
>
> **Pistas oficiales:**
> 1. (Sin pistas adicionales proporcionadas)

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard (3)
- **Evento/origen:** picoCTF 2021
- **Autor:** Dylan McGuire
- **Puntos:** 170
- **ID en CyLab:** 183

## Solución
El reto proporciona código fuente en ensamblador ARMv8-A de 64 bits (`chall_4.S`). El programa lee un argumento entero por línea de comandos ($a = 965270072$) y evalúa una cadena de bifurcaciones condicionales a través de varias funciones anidadas para computar un resultado.

### 1. Rastreo de la ejecución

Siguiendo el flujo de control del argumento $a = 965270072$:

**Paso 1: main → func1**
- Se convierte la cadena a entero con `atoi`, obteniendo $w_0 = 965270072$.
- Se pasa a `func1(965270072)`.

**Paso 2: func1**
```assembly
cmp w0, 100      ; compara con 100
bls .L2          ; salta si es menor o igual
add w0, w0, 100  ; suma 100
bl  func2        ; llama func2
```
- Como $965270072 > 100$, no salta a `.L2`.
- Suma 100: $w_0 = 965270072 + 100 = 965270172$.
- Llama a `func2(965270172)`.

**Paso 3: func2**
```assembly
cmp w0, 499      ; compara con 499
bhi .L5          ; salta si es mayor
; ... código para ramas alternativas
.L5:
add w0, w0, 13   ; suma 13
bl  func5        ; llama func5
```
- Como $965270172 > 499$, salta a `.L5`.
- Suma 13: $w_0 = 965270172 + 13 = 965270185$.
- Llama a `func5(965270185)`.

**Paso 4: func5**
```assembly
bl  func8        ; llama directamente a func8
```
- Pasa el valor a `func8(965270185)`.

**Paso 5: func8**
```assembly
add w0, w0, 2    ; suma 2
ret              ; retorna
```
- Suma 2: $w_0 = 965270185 + 2 = 965270187$.
- Retorna sin modificaciones adicionales.

**Paso 6: main**
- El resultado $965270187$ es formateado con `printf` e impreso.

### 2. Cálculo en Python

```python
a = 965270072
resultado = a + 100 + 13 + 2
print(f"Resultado decimal: {resultado}")
print(f"Resultado en hex: {resultado:08x}")

# Salida:
# Resultado decimal: 965270187
# Resultado en hex: 3988daab
```

**Cálculo:**
- $965270072 + 100 + 13 + 2 = 965270187$
- $965270187_{10} = \mathtt{0x3988daab}_{16}$
- **Bandera resultante: `academy{3988daab}`**

### 3. Sumisión y verificación

- Bandera: `academy{3988daab}`
- Estado: ✓ **CORRECTA**
- Puntos: 170

## Notas adicionales
- El archivo contiene funciones distractoras como `func6` (con bucles de multiplicación y división modular `udiv` hasta 899 iteraciones), `func3`, `func4` y `func7` que no son alcanzadas por el flujo de control para este argumento específico.
- El reto refuerza el reconocimiento de patrones de bifurcación condicional en ARMv8 y la capacidad de seguir cadenas de llamadas de funciones.
- Las instrucciones clave son:
  - `cmp`: comparación
  - `bls`: branch if less or same (sin signo)
  - `bhi`: branch if higher (sin signo)
  - `add`: suma
  - `bl`: branch and link (llamada a función)
  - `ret`: retorno

## Referencias
- Reto: https://learn.cylabacademy.org/library/183
- ARMv8 A64 Instruction Set Architecture: https://developer.arm.com/documentation/ddi0596/latest/
- Documentación ARM: https://developer.arm.com/documentation/
