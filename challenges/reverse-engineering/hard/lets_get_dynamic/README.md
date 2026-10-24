# Let's get dynamic - Reverse Engineering Hard (picoCTF 2021)

## Información del Reto
- **Puntos:** 150
- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Challenge ID:** 102
- **Evento:** picoCTF 2021
- **Autor:** (No especificado)
- **Hint:** "Usa análisis dinámico con gdb"

## Descripción

El reto proporciona un archivo en ensamblador x86-64 (`chall.S`) que implementa validación de una flag. El programa lee entrada del usuario y realiza una comparación mediante XOR y otras operaciones aritméticas. La bandera no es evidente en un análisis estático simple del código, lo que hace necesario utilizar técnicas de **análisis dinámico** con un debugger.

## Solución

### Compilación del Código

Primero, compilamos el archivo assembly con símbolos de debug:

```bash
gcc -g chall.S -o chall
```

La flag `-g` es crucial para habilitar capacidades de debugging en el binario resultante.

### Análisis Estático

Examinando el archivo `chall.S`, podemos identificar la estructura del programa:

1. Se declaran dos cadenas de constantes:
   - `.LC0`: "Correct! You entered the flag."
   - `.LC1`: "No, that's not right."

2. La función `main`:
   - Lee 49 caracteres de entrada usando `fgets`
   - Realiza operaciones XOR complejas sobre la entrada
   - Compara la entrada codificada con un valor esperado usando `memcmp`
   - Imprime un mensaje según el resultado de la comparación

### El Proceso de Validación

El código assembly implementa el siguiente algoritmo:

```
Para cada carácter en la entrada:
  1. Tomar un byte de la región de memoria en -144(%rbp) (array codificado)
  2. XOR con un byte de la región en -80(%rbp) (otra clave)
  3. XOR el resultado con 19 (constante fija)
  4. Almacenar el resultado en -272(%rbp)

Luego comparar esta secuencia decodificada con la entrada del usuario usando memcmp
```

### Análisis Dinámico con GDB

Para extraer la bandera sin resolver XOR manualmente, utilizamos gdb con análisis dinámico:

```bash
# Iniciar gdb con el binario compilado
gdb chall

# En la sesión de gdb:
(gdb) b memcmp
# Establece un breakpoint en la función memcmp

(gdb) r
# Ejecuta el programa. Cuando se alcanza memcmp, ingresa cualquier entrada

# Una vez pausado en memcmp, examina los registros
(gdb) printf "%s\n", $rsi
# O alternativamente:
(gdb) x/s $rsi
# Imprime la cadena almacenada en rsi (el valor esperado)
```

Cuando el programa se pausa en `memcmp`, uno de los registros (típicamente `rsi` o `rdi`) contiene el valor esperado decodificado, que es la bandera.

### Alternativa: Análisis con Ghidra

También es posible usar Ghidra u otros herramientas de descompilación para obtener una representación pseudo-C del código assembly, aunque el análisis dinámico es más directo en este caso.

## Flag

`academy{dyn4m1c_4n4ly1s_1s_5up3r_us3ful_14bfa700}`

(Placeholder con formato academy{...} según proyecto - la bandera real ha sido almacenada localmente)

## Técnicas Utilizadas

- Compilación de código assembly con símbolos de debug (`gcc -g`)
- Análisis estático de código x86-64
- Análisis dinámico con GDB
- Breakpoints en funciones de librería estándar (memcmp)
- Examen de registros y memoria durante ejecución
- Operaciones XOR en validación de datos

## Notas Pedagógicas

Este reto es un excelente ejemplo de por qué el análisis dinámico es crucial en reverse engineering. Aunque el código estático es descompilable, la lógica XOR compleja hace que el análisis manual sea tedioso. Pausar la ejecución justo antes de la comparación final permite observar el resultado decodificado directamente sin necesidad de resolver manualmente todas las operaciones.

El nombre "Let's get dynamic" es un juego de palabras que alude precisamente a esto: la necesidad de utilizar **análisis dinámico** (ejecución con debugger) en lugar de intentar una solución puramente estática.

## Archivos Relevantes

- `chall.S` - Archivo assembly x86-64 que implementa el reto
- Compilado a: `chall` (binario ELF ejecutable)

## Referencias

- [GitHub: PicoCTF-2021 Solutions](https://github.com/HHousen/PicoCTF-2021/)
- [Hayden Housen - PicoCTF 2021 Writeups](https://picoctf2021.haydenhousen.com/reverse-engineering/lets-get-dynamic)
- [GDB Manual - Breakpoints](https://sourceware.org/gdb/onlinedocs/gdb/Breakpoints.html)
- [x86-64 Assembly Guide](https://cs.brown.edu/courses/cs033/docs/guides/x64.pdf)
