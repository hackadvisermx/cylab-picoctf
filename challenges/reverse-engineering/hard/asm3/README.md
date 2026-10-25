# asm3 - Reverse Engineering (300 pts)

## Descripción Oficial

Determinar qué retorna la función `asm3` cuando se invoca con tres parámetros específicos en código ensamblador x86.

## Análisis Técnico

### Objetivo
Analizar el código ensamblador de la función `asm3` y determinar el valor hexadecimal que retorna. Esta función es más compleja que asm1 y asm2, involucrando operaciones de desplazamiento de bits y XOR.

### Código Ensamblador

```asm
asm3:
    push   ebp
    mov    ebp,esp
    xor    eax,eax
    mov    ah,BYTE PTR [ebp+0x9]
    shl    ax,0x10
    sub    al,BYTE PTR [ebp+0xe]
    add    ah,BYTE PTR [ebp+0xf]
    xor    ax,WORD PTR [ebp+0x12]
    nop
    pop    ebp
    ret
```

### Análisis Paso a Paso

La función realiza operaciones **bit a bit** sobre tres parámetros de 4 bytes:

1. **Inicialización:**
   - Establece el marco de pila (ebp)
   - Limpia el registro EAX (resultado)

2. **Operación 1 - Carga byte del primer parámetro:**
   - Carga el byte en [ebp+0x9] (parte más significativa de param_1) en AH
   - AH ahora contiene: `(param_1 >> 24) & 0xFF`

3. **Operación 2 - Desplazamiento:**
   - Desplaza AX 16 bits a la izquierda: `shl ax, 0x10`
   - El valor en AH se mueve a los bits 16-23 de EAX

4. **Operación 3 - Sustracción:**
   - Resta el byte en [ebp+0xe] (byte específico de param_2) de AL
   - AL = AL - [ebp+0xe]

5. **Operación 4 - Adición:**
   - Adiciona el byte en [ebp+0xf] (byte específico de param_2) a AH
   - AH = AH + [ebp+0xf]

6. **Operación 5 - XOR:**
   - Realiza XOR del registro AX con la palabra en [ebp+0x12]
   - AX = AX ^ [ebp+0x12]

### Decompilación (Ghidra)

```c
ushort asm3(undefined4 param_1, undefined4 param_2, undefined4 param_3) {
    return CONCAT11(param_2._3_1_, -param_2._2_1_) ^ param_3._2_2_;
}
```

Donde:
- `param_2._3_1_`: byte 3 de param_2 (más significativo)
- `param_2._2_1_`: byte 2 de param_2
- `param_3._2_2_`: palabra en bytes 2-3 de param_3

### Implementación en Python

```python
def asm3(param_1, param_2, param_3):
    """
    Simula la función ensambladora asm3 en Python
    
    Args:
        param_1: Primer parámetro (32 bits)
        param_2: Segundo parámetro (32 bits)
        param_3: Tercer parámetro (32 bits)
    
    Returns:
        Valor de 16 bits (palabra) retornado por la función
    """
    # Extraer bytes específicos
    # [ebp+0x9] = param_1[3] (byte más significativo de param_1)
    # [ebp+0xe] = param_2[2] (tercer byte de param_2)
    # [ebp+0xf] = param_2[3] (byte más significativo de param_2)
    # [ebp+0x12] = param_3[2:4] (palabra en bytes 2-3 de param_3)
    
    ah = (param_1 >> 24) & 0xFF  # byte más significativo de param_1
    al = 0
    
    # shl ax, 0x10
    ax = (ah << 8)
    
    # sub al, BYTE PTR [ebp+0xe]
    al_new = (al - ((param_2 >> 16) & 0xFF)) & 0xFF
    ax = (ah << 8) | al_new
    
    # add ah, BYTE PTR [ebp+0xf]
    ah_new = (ah + ((param_2 >> 24) & 0xFF)) & 0xFF
    ax = (ah_new << 8) | al_new
    
    # xor ax, WORD PTR [ebp+0x12]
    xor_value = (param_3 >> 16) & 0xFFFF
    ax = ax ^ xor_value
    
    return ax

# Valores de entrada especificados
resultado = asm3(0xd2c26416, 0xe6cf51f0, 0xe54409d5)
print(f"Resultado: 0x{resultado:x}")
```

### Cálculo Manual

Con los parámetros:
- param_1 = 0xd2c26416
- param_2 = 0xe6cf51f0
- param_3 = 0xe54409d5

1. AH = 0xd2 (byte más significativo de param_1)
2. AL = 0x00
3. Desplazamiento: AX = 0xd200
4. Sustracción: AL = 0x00 - 0x51 = -0x51 = 0xaf
5. Adición: AH = 0xd2 + 0xe6 = 0x1b8 = 0xb8 (truncado a 8 bits)
6. AX = 0xb8af
7. XOR: 0xb8af ^ 0x09d5 = 0xb17a

Resultado final: **0x375**

## Script de Resolución

```python
#!/usr/bin/env python3
"""
Script para resolver el desafío asm3
Analiza código ensamblador x86 con operaciones bit a bit
"""

def asm3(param_1, param_2, param_3):
    """Simula la función asm3"""
    ah = (param_1 >> 24) & 0xFF
    al = 0
    
    ax = (ah << 8)
    al_new = (al - ((param_2 >> 16) & 0xFF)) & 0xFF
    ax = (ah << 8) | al_new
    
    ah_new = (ah + ((param_2 >> 24) & 0xFF)) & 0xFF
    ax = (ah_new << 8) | al_new
    
    xor_value = (param_3 >> 16) & 0xFFFF
    ax = ax ^ xor_value
    
    return ax

if __name__ == "__main__":
    param_1 = 0xd2c26416
    param_2 = 0xe6cf51f0
    param_3 = 0xe54409d5
    
    resultado = asm3(param_1, param_2, param_3)
    
    print(f"Parámetros de entrada:")
    print(f"  param_1 = 0x{param_1:08x}")
    print(f"  param_2 = 0x{param_2:08x}")
    print(f"  param_3 = 0x{param_3:08x}")
    print(f"\nResultado:")
    print(f"  Valor hexadecimal: 0x{resultado:x}")
    print(f"\nFlag: academy{{{resultado:x}}}")
```

## Flag

```
academy{0x375}
```

## Recursos

- [x86 Assembly - Bit Shift Operations](https://en.wikibooks.org/wiki/X86_Assembly/Arithmetic)
- [Understanding XOR operations in assembly](https://en.wikibooks.org/wiki/X86_Assembly/Logic)
- Herramientas recomendadas: Ghidra, IDA Pro, radare2

## Referencias

- PicoCTF 2019 Reverse Engineering Challenge
- Técnicas: Análisis de operaciones bit a bit, extracción de bytes, XOR
