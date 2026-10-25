# MATRIX

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Autor:** asphyxia
- **Evento / Origen:** picoMini by redpwn (picoCTF)
- **ID CyLab:** 221
- **Puntos:** 500

---

## Descripción del Reto

```
Enter the M A T R I X
nc mars.cylabacademy.net 31259
```

Se proporciona un archivo ejecutable ELF x86-64 llamado `matrix`. Al conectarse al servicio remoto, se muestra:

```text
Welcome to the M A T R I X
Can you make it out alive?
```

Si se envía una entrada inválida, el programa responde con:
```text
You were eaten by a grue.
```

---

## Análisis del Binario

### 1. Propiedades del Archivo
- **Formato:** ELF 64-bit LSB PIE executable, x86-64
- **Estado:** Stripped (sin símbolos)
- **Compilador:** GCC 10.2.0

### 2. Estructura y Funcionamiento General
Al desensamblar `main` (0x10d0), se observa que el binario no es un programa ordinario: es una **Máquina Virtual (VM)** basada en pila de palabras de 16 bits:
1. Asigna dos buffers de 0x800 bytes (2048 bytes) mediante `malloc`:
   - `stack1`: Pila de ejecución de datos (operaciones y retorno).
   - `stack2`: Pila auxiliar / de llamadas.
2. Inicializa una estructura de control con:
   - Puntero al bytecode embebido en `.rodata` en el desplazamiento `0x20f0`.
   - Contador de programa (`PC`), inicializado en 0.
   - Puntero a función de entrada (wrapper de `getc`).
   - Puntero a función de salida (wrapper de `putc`).
3. Ejecuta la función del intérprete `fcn.00001350` en un bucle continuo hasta que la instrucción `HALT` (código 0x01) devuelva código 0.
4. Si la condición de terminación es exitosa (`status == 0`), abre y muestra el archivo `flag.txt`:
   ```c
   puts("Have a flag!");
   FILE *f = fopen("flag.txt", "r");
   fgets(buffer, 0x100, f);
   puts(buffer);
   ```

---

## Arquitectura de la Máquina Virtual

El intérprete decodifica los opcodes mediante una tabla de saltos (`jump table`) y comprobaciones directas:

| Opcode | Nemónico | Descripción |
|--------|----------|-------------|
| `0x00` | `NOP` | No operación (continúa ejecución). |
| `0x01` | `HALT` | Termina la VM; extrae el código de salida de `stack1`. Si es 0, imprime la flag. |
| `0x10` | `DUP` | Duplica el valor en la cima de `stack1`. |
| `0x11` | `DROP` | Descarta el valor en la cima de `stack1`. |
| `0x12` | `ADD` | Suma los dos valores superiores de `stack1`: `b = pop(), a = pop(); push(a + b)`. |
| `0x13` | `SUB` | Resta: `b = pop(), a = pop(); push(a - b)`. |
| `0x14` | `SWAP` | Intercambia los dos valores superiores de `stack1`. |
| `0x20` | `PUSH2` | Mueve un valor de `stack1` a la pila auxiliar `stack2`. |
| `0x21` | `POP2` | Mueve un valor de `stack2` a `stack1`. |
| `0x30` | `JMP` | Salto incondicional: `PC = pop()`. |
| `0x31` | `JZ` | Salto condicional si cero: `target = pop(), cond = pop(); if (cond == 0) PC = target`. |
| `0x32` | `JNZ` | Salto condicional si no cero: `if (cond != 0) PC = target`. |
| `0x33` | `JL` | Salto si menor a cero (signed): `if (cond < 0) PC = target`. |
| `0x34` | `JLE` | Salto si menor o igual a cero: `if (cond <= 0) PC = target`. |
| `0x80 <imm8>` | `PUSH imm8` | Inserta un inmediato con signo de 8 bits (extendido a 16 bits). |
| `0x81 <imm16>` | `PUSH imm16` | Inserta un inmediato de 16 bits (little-endian). |
| `0xc0` | `IN` | Lee un byte de `stdin` (`getc`) y lo inserta en `stack1`. |
| `0xc1` | `OUT` | Extrae un valor de `stack1` y lo envía a `stdout` (`putc`). |

---

## Análisis del Bytecode: El Laberinto 16x16

Al desensamblar el bytecode alojado en `0x20f0` de `.rodata`, se revelan las siguientes etapas:

1. **Mensaje de Bienvenida:**
   Empuja caracteres en orden inverso y ejecuta una rutina de impresión en `0x013b`, mostrando:
   `Welcome to the M A T R I X\nCan you make it out alive?\n`

2. **Lectura de Movimientos:**
   Inicializa la posición del jugador en `(x = 1, y = 1)` y un contador de llaves en `keys = 0`.
   Lee un carácter por turno y comprueba:
   - `'u'` (117): Decrementa `y` (`y = y - 1`).
   - `'d'` (100): Incrementa `y` (`y = y + 1`).
   - `'l'` (108): Decrementa `x` (`x = x - 1`).
   - `'r'` (114): Incrementa `x` (`x = x + 1`).
   - Cualquier otra entrada salta a `0x00fb` ("You were eaten by a grue.").

3. **Indexación de la Matriz:**
   Calcula la posición lineal dentro de una matriz de 16x16:
   $$\text{idx} = y \times 16 + x$$
   Cada celda en la tabla que inicia en `0x0174` ocupa 4 bytes (`idx * 4`):
   - **Pared / Trampa (`81 fb 00 30`):** `PUSH 0x00fb; JMP`. Muestra mensaje de muerte y finaliza.
   - **Pasillo vacío (`30 00 00 00`):** `JMP 0x007b`. Salta directamente a leer el siguiente comando.
   - **Llave (`K`, `81 7f 05 30`):** `PUSH 0x057f; JMP`. Ejecuta `keys += 1` y continúa.
   - **Puerta (`D`, `81 74 05 30`):** `PUSH 0x0574; JMP`. Verifica `keys > 0`; si `keys == 0`, muere devorado por el grue; si `keys > 0`, descuenta una llave (`keys -= 1`) y permite el paso.
   - **Meta / Salida (`G`, `81 85 05 30` en `x=14, y=15`):** `PUSH 0x0585; JMP`. Muestra `"Congratulations, you made it!\n"`, termina la VM con código 0 y el binario lee e imprime `flag.txt`.

### Mapa del Laberinto Extraído

```text
 0 ################
 1 #S....K#.#K..#.#
 2 ####D###.###.#.#
 3 #..........#.#.#
 4 ##.#.#####.#.D.#
 5 #..#.#K..#.#.#.#
 6 #.##.###.#.#.#.#
 7 #.#......#.#.#.#
 8 #.#.######.#.#.#
 9 #.#........#.#.#
10 #.###.######.#.#
11 #...#..D..#..#.#
12 #.###..#..#.#..#
13 #.#...###.#.#D##
14 #.#....#..D.#..#
15 ##############G#
```
- `#` = Pared
- `.` = Pasillo
- `S` = Inicio `(1, 1)`
- `K` = Llave (`keys + 1`)
- `D` = Puerta (`keys - 1`, requiere `keys >= 1`)
- `G` = Meta `(14, 15)`

### Mecánica de "Farming" de Llaves
Dado que el código se encuentra en memoria de solo lectura (`.rodata`), las casillas `K` no desaparecen tras ser visitadas. Esto permite acumular llaves dando pasos repetidos de ida y vuelta sobre una casilla `K` (por ejemplo `rlrlrl...`).

---

## Resolución Mediante Búsqueda en Anchura (BFS)

Se implementó un algoritmo de búsqueda en anchura (BFS) modelando el estado como `(x, y, keys)` para encontrar el camino más corto hacia la salida `G`:

```python
# Estado: (x, y, keys)
# Camino resultante de 63 movimientos:
path = "rrrrrlrlrlrlrllddddddlddrrddrrrdrddrruuuruuuuuuurrddddddddlddrd"
```

Al enviar la secuencia de movimientos al servicio remoto:

```bash
python3 solve.py
```

Salida del servidor:
```text
Congratulations, you made it!
Have a flag!
academy{y0uv3_3sc4p3d_th3_m4ze...f0r_n0w-hYkq2D9PmrA5GpEq}
```

---

## Flag

```
academy{y0uv3_3sc4p3d_th3_m4ze...f0r_n0w-hYkq2D9PmrA5GpEq}
```
*(Flag original del servidor: `picoCTF{y0uv3_3sc4p3d_th3_m4ze...f0r_n0w-hYkq2D9PmrA5GpEq}`)*
