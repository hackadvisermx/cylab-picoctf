# Reverse Engineering — unpackme

## Descripción
> **Prompt oficial del reto:** "Can you get the flag? Reverse engineer this binary."
>
> **Pistas oficiales:**
> 1. What is UPX?

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto suministra un binario ejecutable ELF de 64 bits empaquetado con UPX denominado `unpackme-upx`.

### 1. Desempaquetado con UPX
Se descomprime el binario original mediante la herramienta oficial de UPX:

```bash
upx -d unpackme-upx -o unpackme-unpacked
```

### 2. Análisis de la función `main`
Al desensamblar el binario descomprimido con `objdump`:

```bash
objdump -d unpackme-unpacked | grep -A 40 "<main>:"
```

Se observa que `main` realiza las siguientes operaciones:
1. Inicializa una cadena codificada en la pila local (`[rbp - 0x30]`).
2. Solicita al usuario un número favorito con `scanf("%d", &fav_num)`.
3. Compara el valor ingresado contra la constante hexadecimal `0xb83cb` (equivalente a `754635` en base 10):
   ```assembly
   401aaf: cmpl $0xb83cb, %eax
   401ab4: jne  401af9 <main+0xd6>
   ```
4. Si el valor coincide, invoca a la función `rotate_encrypt` pasando como argumento el buffer local, e imprime el resultado con `fputs`.

### 3. Algoritmo de descifrado (ROT47)
Al analizar la función `rotate_encrypt` en la dirección `0x401965`:
- Para cada carácter con código ASCII entre 33 (`!`) y 126 (`~`), suma 47 (`0x2f`) y realiza la rotación módulo 94 (`0x5e`).
- Este algoritmo corresponde exactamente al cifrado **ROT47**.

Reconstruyendo los bytes de la pila en Python y aplicando ROT47:

```python
import struct

buf = bytearray(64)
buf[0:8]   = struct.pack('<Q', 0x4c4a3e3635323432)
buf[8:16]  = struct.pack('<Q', 0x30623e306b6d4146)
buf[14:22] = struct.pack('<Q', 0x6565304866373062)
buf[22:30] = struct.pack('<Q', 0x4e615f61666368)

raw_str = bytes(buf).split(b'\x00')[0]

def rot47(s):
    res = []
    for c in s:
        if 33 <= c <= 126:
            res.append(chr(33 + ((c - 33 + 47) % 94)))
        else:
            res.append(chr(c))
    return ''.join(res)

print(rot47(raw_str))
```

Al rotar la cadena se obtiene la bandera en formato `academy{...}`. Alternativamente, al ejecutar el binario e introducir el número `754635` por consola se imprime la misma bandera.

## Notas adicionales
- ROT47 es un cifrado simétrico que rota todos los caracteres imprimibles ASCII estándar, siendo su propia función inversa.

## Referencias
- Reto: https://learn.cylabacademy.org/library/313
- UPX: https://upx.github.io/
