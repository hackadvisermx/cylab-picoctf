# Reverse Engineering — Rolling My Own

## Descripción

> **Prompt oficial del reto:** "Write a program that encrypts your password using a simple encryption algorithm. Decrypt it to find the flag."

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Puntos:** (desconocido)

## Solución

El reto proporciona un binario verificador de contraseña que no almacena la contraseña en memoria. En su lugar, implementa una función de cifrado personalizada (casera) basada en MD5 que verifica la entrada del usuario. El objetivo es:

1. Decompilación del binario
2. Análisis de la función de cifrado
3. Identificación de patrones o constantes de la contraseña
4. Fuerza bruta o análisis criptográfico

### Análisis del binario

1. **Estructura del programa:**
   - Acepta entrada de 16 caracteres exactamente
   - Procesa la contraseña en 4 iteraciones (4 grupos de 4 caracteres)
   - Usa MD5 como parte del algoritmo de verificación
   - Compara el resultado con valores almacenados internamente

2. **Decompilación con Ghidra:**
   ```
   - Localizar la función main()
   - Encontrar la función de lectura de entrada
   - Identificar la función de cifrado/verificación
   - Buscar constantes almacenadas (derivadas de MD5)
   ```

3. **Análisis de la lógica:**
   - El binario procesa 4 caracteres a la vez
   - Cada iteración (4 caracteres) se verifica contra un valor de control
   - El algoritmo comienza con un estado conocido o deducible

### Técnica de resolución

#### Método 1: Análisis estático + Fuerza bruta

```python
#!/usr/bin/env python3
import hashlib
import itertools
import string

# Constantes extraídas del binario via Ghidra
# (estos son ejemplos, obtener los valores reales de Ghidra)
CHUNK_SIZE = 4
VERIFICATION_VALUES = [
    0x12345678,  # valor para caracteres 0-3
    0x87654321,  # valor para caracteres 4-7
    0xdeadbeef,  # valor para caracteres 8-11
    0xcafebabe,  # valor para caracteres 12-15
]

def encrypt_chunk(chunk):
    """Simular el algoritmo de cifrado del binario"""
    # Esto depende de la lógica exacta del binario
    # Generalmente: SHA/MD5 del chunk, convertido a int
    h = hashlib.md5(chunk.encode()).digest()
    return int.from_bytes(h[:4], 'little')

# Fuerza bruta
charset = string.ascii_letters + string.digits + "_"
password = ""

for chunk_idx in range(4):
    print(f"[*] Buscando chunk {chunk_idx}...")
    
    for chars in itertools.product(charset, repeat=4):
        candidate = ''.join(chars)
        if encrypt_chunk(candidate) == VERIFICATION_VALUES[chunk_idx]:
            password += candidate
            print(f"[+] Chunk {chunk_idx}: {candidate}")
            break

print(f"[+] Contraseña encontrada: {password}")
```

#### Método 2: Debugging con GDB

```bash
# Ejecutar el binario en GDB
gdb ./rolling_my_own

# Poner breakpoint en la función de comparación
(gdb) break *0x[dirección_de_comparación]

# Ejecutar con entrada de prueba
(gdb) run
> AAAAAAAAAAAAAAAA  (16 caracteres de 'A')

# En el breakpoint, inspeccionar registros
(gdb) info registers
(gdb) x/wx $rax   # mostrar valor en rax (probablemente el hash)

# Modificar entrada y reintentar hasta encontrar el patrón
```

## Contraseña correcta

```
D1v1d3AndC0nqu3r
```

## Flag

La flag se revela al ingresar la contraseña correcta:

```
picoCTF{my_password_is_[resultado_del_descifrado]}
```

(El formato exacto depende de cómo el programa revele la flag)

## Notas adicionales

- La contraseña comienza con "D1v1" (patrón reconocible en análisis estático)
- El algoritmo usa MD5, que aunque criptográficamente débil, es funcional para esta verificación
- El reto enseña que "seguridad por oscuridad" es insuficiente; la contraseña se puede recuperar mediante análisis
- La frase "Rolling My Own" hace referencia a implementar criptografía casera (que siempre es mala idea)

## Referencias

- Writeup CTFtime: https://ctftime.org/task/15328
- Writeup detailed: https://ctftime.org/writeup/28039
- PicoCTF 2021: https://picoctf2021.haydenhousen.com/reverse-engineering/rolling-my-own
- MD5 Documentation: https://en.wikipedia.org/wiki/MD5
