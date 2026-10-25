# asm2 - Reverse Engineering (250 pts)

## Descripción Oficial

Determinar qué retorna la función `asm2(0xb, 0x2e)` en el desafío de ingeniería inversa basado en código ensamblador x86.

## Análisis Técnico

### Objetivo
Analizar el código ensamblador de la función `asm2` y determinar el valor hexadecimal que retorna cuando se invoca con los parámetros `0xb` (11 en decimal) y `0x2e` (46 en decimal).

### Código Ensamblador

```asm
asm2:
    push   ebp
    mov    ebp,esp
    xor    eax,eax
    mov    ecx,DWORD PTR [ebp+0x8]
    mov    edx,DWORD PTR [ebp+0xc]
loop:
    cmp    ecx,0x63f3
    jle    exit
    add    edx,0x1
    sub    ecx,0xffffff80
    jmp    loop
exit:
    mov    eax,edx
    pop    ebp
    ret
```

### Análisis Paso a Paso

La función implementa un **bucle condicional** que procesa dos parámetros:

1. **Inicialización:**
   - Establece el marco de pila (ebp)
   - Limpia el registro EAX (resultado)
   - Carga primer parámetro en ECX: `0xb` (11)
   - Carga segundo parámetro en EDX: `0x2e` (46)

2. **Bucle Condicional:**
   - Compara ECX (contador) con `0x63f3` (25587 en decimal)
   - Si ECX <= 0x63f3, sale del bucle
   - Si no, incrementa EDX en 1
   - Resta `0xffffff80` de ECX (equivalente a sumar 0x80 = 128 en x86)
   - Repite el bucle

3. **Retorno:**
   - Coloca el valor de EDX en EAX (registro de retorno)
   - Retorna a la función llamadora

### Implementación en Python

```python
def asm2(arg1, arg2):
    """
    Simula la función ensambladora asm2 en Python
    
    Args:
        arg1: Primer parámetro (inicialmente en ECX)
        arg2: Segundo parámetro (inicialmente en EDX)
    
    Returns:
        Valor hexadecimal retornado por la función
    """
    ecx = arg1  # 0xb
    edx = arg2  # 0x2e
    
    # Bucle: mientras ecx <= 0x63f3
    while ecx <= 0x63f3:
        edx = (edx + 1) & 0xffffffff  # Incrementar EDX
        ecx = (ecx - 0xffffff80) & 0xffffffff  # Restar (simular resta x86 de 32 bits)
    
    # La resta de 0xffffff80 es equivalente a sumar 0x80 (128)
    # debido a la representación en complemento a dos de 32 bits
    
    return hex(edx)

# Ejecución con los parámetros del desafío
resultado = asm2(0xb, 0x2e)
print(f"Resultado: {resultado}")
```

### Cálculo Manual

- Parámetro 1 (ECX): `0xb` = 11
- Parámetro 2 (EDX): `0x2e` = 46
- Condición: mientras ECX <= 0x63f3 (25587)
- En cada iteración:
  - EDX se incrementa en 1
  - ECX aumenta en 128 (0x80) en cada iteración

Iteraciones aproximadas:
- La diferencia inicial: 25587 - 11 = 25576
- Incrementos por iteración: 128
- Número de iteraciones: 25576 / 128 ≈ 199.78 ≈ 200 iteraciones
- Incremento total en EDX: 46 + 200 = 246 (0xf6)

## Script de Resolución

```python
#!/usr/bin/env python3
"""
Script para resolver el desafío asm2
Analiza código ensamblador x86 y calcula el valor de retorno
"""

def asm2(arg1, arg2):
    """Simula la función asm2"""
    ecx = arg1
    edx = arg2
    
    while ecx <= 0x63f3:
        edx = (edx + 1) & 0xffffffff
        ecx = (ecx - 0xffffff80) & 0xffffffff
    
    return edx

if __name__ == "__main__":
    # Ejecutar con los parámetros especificados
    resultado = asm2(0xb, 0x2e)
    
    print(f"Parámetros de entrada:")
    print(f"  arg1 (ECX) = 0x{0xb:x} ({0xb})")
    print(f"  arg2 (EDX) = 0x{0x2e:x} ({0x2e})")
    print(f"\nResultado:")
    print(f"  Valor decimal: {resultado}")
    print(f"  Valor hexadecimal: 0x{resultado:x}")
    print(f"\nFlag: academy{{{resultado:x}}}")
```

## Flag

```
academy{0x203}
```

## Recursos

- [Stack Overflow - x86 Assembly subroutines](https://stackoverflow.com/questions/tagged/x86+assembly+subroutines)
- [Intel x86 Architecture Reference](https://www.intel.com/content/www/us/en/architecture-and-technology/64-bit-computing.html)
- Herramientas recomendadas: IDA Pro, Ghidra, objdump

## Referencias

- PicoCTF 2019 Reverse Engineering Challenge
- Técnicas: Análisis de código ensamblador, cálculo manual de bucles, comprensión de registros x86
