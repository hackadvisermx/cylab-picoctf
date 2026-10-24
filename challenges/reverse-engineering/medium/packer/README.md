# Reverse Engineering — packer

## Descripción
> **Prompt oficial del reto:** "Reverse this linux executable?"
>
> **Pistas oficiales:**
> 1. What can we do to reduce the size of a binary after compiling it.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** Mubarak Mikail

## Solución
El reto proporciona un archivo ejecutable ELF x86-64 llamado `out`. Al analizar el binario con la herramienta `file` y verificar su estructura:

```bash
file out
upx -t out
```

Se observa que está empaquetado con **UPX** (*Ultimate Packer for eXecutables*). Los empaquetadores comprimen y ofuscan el código ejecutable para reducir el tamaño en disco, descomprimiéndolo en memoria al momento de la ejecución.

### 1. Desempaquetado del binario
Para analizar la lógica original del programa, se utiliza UPX con la bandera de descompresión `-d`:

```bash
upx -d out -o out-unpacked
```

### 2. Análisis estático de la función `main`
Al examinar la función `main` en el binario desempaquetado con `objdump`:

```bash
objdump -d out-unpacked | grep -A 40 "<main>:"
```

Se observa una secuencia de instrucciones `movabsq` que cargan constantes de 64 bits directamente en la pila local (`[rbp - 0x80]`, `[rbp - 0x78]`, etc.):
```assembly
4019c6: movabsq $0x3436313633363136, %rax
4019d0: movabsq $0x6237393764363536, %rdx
...
```

Posteriormente, el programa solicita una entrada con `fgets` y la compara con esta cadena en memoria. Al extraer los valores hexadecimales little-endian en orden:

```python
import struct

vals = [
    0x3436313633363136,
    0x6237393764363536,
    0x6635383539333535,
    0x3433303565363535,
    0x6534313362363336,
    0x3133323466353633,
    0x3936323534336536,
    0x3236663533353333,
    0x3636313635363533,
    0x6437323334363636,
]

b = b''.join(struct.pack('<Q', v) for v in vals)
hex_ascii = b.decode('latin1', 'ignore')
flag = bytes.fromhex(hex_ascii).decode('latin1')
print(flag)
```

Al decodificar la representación hexadecimal en ASCII se obtiene directamente la bandera en formato `academy{...}`.

## Notas adicionales
- UPX es una de las herramientas de compresión de binarios más utilizadas. Identificar las firmas UPX en las cabeceras ELF permite revertir el empaquetado de forma directa sin requerir un volcado de memoria en ejecución.

## Referencias
- Reto: https://learn.cylabacademy.org/library/421
- UPX: https://upx.github.io/
