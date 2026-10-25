# OTP Implementation (RE Hard, 300pts)

## Desafío
Resolver un reto de One-Time Pad (OTP) que implementa cifrado XOR con una clave validada.

## Análisis

### Archivo: `otp`
Binario ELF 64-bit que:
1. Toma una clave como argumento de línea de comandos
2. Valida la clave contra una tabla de valores predeterminados
3. Si es válida, proporciona un mensaje diciendo "Now xor it with the flag!"

### Función `valid_char()`
Valida que cada carácter de entrada sea:
- Dígito hexadecimal: 0-9 (0x30-0x39)
- Letras hex minúsculas: a-f (0x61-0x66)  
- Barra diagonal: / (0x2f)

Rango permitido: {0-9, a-f, /}

### Función `jumble()`
Implementa una transformación bit a bit:
```c
int jumble(int c) {
    if (c > 0x60) c += 9;
    int d = ((signed char)c) >> 7;
    d = d >> 4;
    c = c + d;
    c = c & 0xf;
    c = c - d;
    c = c << 1;
    return c & 0xff;
}
```

Mapea caracteres válidos a valores específicos:
- '0' -> 0  -> 'a'
- '1' -> 2  -> 'c'
- '2' -> 4  -> 'e'
- ...
- 'f' -> 30 -> '' (OOB)

### Algoritmo de Validación
El programa procesa la clave mediante una cadena de transformaciones:
1. Para i=0: `buffer[0] = transform(jumble(key[0]))`
2. Para i>0: `buffer[i] = transform(jumble(key[i]) + buffer[i-1])`

Luego convierte cada valor a ASCII: `chr(buffer[i] + 'a')`

La tabla esperada es:
```
fbfgakjbjnndpippmclmnjonmilohidamgofjkmfogfceogbjehcdkpbabgneddjpnnfddpedocpjemlfejnienpedmlpboihgda
```

### Flag Cifrada
Archivo `enc_flag.txt` contiene la bandera cifrada en hex:
```
c74b3490276e15cb80bdf5dbc6f497b410264a70f78d4a793faee5d5a79fe064074b1435cc4a6e0e0095e5f0ccab10d1cf93
```

## Solución

### Pasos:
1. Implementar la función `jumble()` correctamente
2. Implementar el algoritmo de cadena de procesamiento
3. Mediante reverse engineering o búsqueda, encontrar la clave correcta
4. Validar la clave contra la tabla
5. XOR la clave con `enc_flag.txt`

### Desafío de Reverse Engineering:
El mapeo de caracteres válidos a salida de la tabla es limitado, lo que sugiere que la mayoría de caracteres de la tabla esperada NO son producidos directamente por la función jumble con entradas válidas.

Esto implica que:
- O el algoritmo incluye lógica adicional no identificada
- O los caracteres de la tabla están codificados de otra manera
- O se necesita symbolic execution (ANGR) para encontrar la clave

## Herramientas Sugeridas
- GDB con scripts Python para trace
- ANGR para symbolic execution
- Decompiladores (Ghidra, IDA)

## Código del Análisis

```python
def jumble(c_input):
    c = c_input & 0xff
    if c > 0x60:
        c = (c + 9) & 0xff
    
    if c & 0x80:
        c_signed = c - 256
    else:
        c_signed = c
    
    d = c_signed >> 7  # Sign extend
    d = d >> 4
    
    result = (c + d) & 0xffffffff
    result = result & 0xf
    result = (result - d) & 0xffffffff
    result = (result << 1) & 0xff
    return result
```

## Mapeo de Caracteres
Caracteres válidos -> valores de jumble:
- '0' -> 0  -> 'a'
- '1' -> 2  -> 'c'
- '2' -> 4  -> 'e'
- '3' -> 6  -> 'g'
- '4' -> 8  -> 'i'
- '5' -> 10 -> 'k'
- '6' -> 12 -> 'm'
- '7' -> 14 -> 'o'
- '8' -> 16 -> 'q'
- '9' -> 18 -> 's'
- 'a' -> 20 -> 'u'
- 'b' -> 22 -> 'w'
- 'c' -> 24 -> 'y'
- 'd' -> 26 -> '{'
- 'e' -> 28 -> '}'
- 'f' -> 30 -> (OOB)
- '/' -> 30 -> (OOB)

## Problema Fundamental Identificado

La tabla de validación contiene caracteres que NO son generables mediante la función jumble con caracteres de entrada válidos:

- **Caracteres generables**: {a, c, e, g, i, k, m, o, q, s, u, w, y, {, }}
- **Caracteres en tabla**: {a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, ...}
- **Brecha**: Faltan {b, d, f, h, j, l, n, p, ...}

Esto indica:
1. Implementación incompleta de `jumble()` o
2. Procesamiento adicional no identificado en el asm o
3. Algoritmo más complejo que lo analizado

## Herramientas Necesarias

- GDB con scripts Python para trace dinámico
- ANGR framework para symbolic execution
- Ghidra o IDA Pro para decompilación avanzada
- Acceso a código fuente original de picoCTF 2020

## Estado
**PENDIENTE** - Análisis arquitectónico completado.  
Reverse engineering del algoritmo incompleto debido a limitaciones de herramientas disponibles.  
Requiere análisis dinámico o symbolic execution para resolver completamente.
