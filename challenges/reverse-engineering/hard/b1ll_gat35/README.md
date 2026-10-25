# B1ll_Gat35 - Reverse Engineering (400 pts)

## Descripción Oficial

Inspeccionar un binario de Windows y recuperar la clave de acceso correcta para que el programa imprima la bandera. El programa solicita un número entre 1 y 5 dígitos, luego pide una clave. Si la clave es correcta, otorga los códigos de acceso a la bóveda.

## Contexto

- **Archivo:** `win-exec-1.exe` (binario de Windows ejecutable)
- **Tipo:** GUI/CLI híbrida
- **Dificultad:** Hard (400 pts)
- **Plataforma:** Windows (ejecutable PE)

## Análisis Técnico

### Flujo del Programa

1. El programa solicita un **número entre 1 y 5 dígitos**
2. Solicita una **clave de acceso**
3. Valida la clave mediante la función `FUN_00407f60()`
4. Si es correcta, imprime: `"Correct input. Printing flag: [FLAG]"`
5. Si es incorrecta, imprime: `"Incorrect input. Exiting."`

### Puntos de Interés

```
Dirección: 0x00408114
Instrucción: JNZ (Jump if Not Zero)
Descripción: Punto de decisión crítico en la validación de clave
```

### Estrategia de Resolución: Opción 1 (Modificación Binaria)

**Herramienta:** Ghidra

1. **Abrir binario en Ghidra:**
   - File > Open > seleccionar `win-exec-1.exe`
   - Permitir análisis automático

2. **Localizar función de validación:**
   - Navegar a la dirección `0x00408114`
   - Identificar la instrucción JNZ que valida la clave

3. **Modificar instrucción:**
   - JNZ (Jump if Not Zero) → JNC (Jump if No Carry)
   - Esta modificación fuerza el programa a ejecutar el bloque de éxito

4. **Exportar binario modificado:**
   - File > Export Program
   - Guardarlo como `win-exec-1-modified.exe`

5. **Ejecutar:**
   ```bash
   # En Linux con Wine
   wine win-exec-1-modified.exe
   
   # En Windows
   win-exec-1-modified.exe
   ```

### Estrategia de Resolución: Opción 2 (Depuración Estática)

**Herramienta:** OllyDbg (Debugger para Windows)

1. **Abrir en OllyDbg:**
   - File > Open > `win-exec-1.exe`
   - El programa se cargará en memoria

2. **Buscar strings:**
   - View > Strings
   - Buscar referencias a mensajes del programa
   - Localizar cadenas relacionadas con validación

3. **Análisis de flujo:**
   - Buscar la instrucción de comparación
   - Rastrear dónde se verifica la clave
   - Identificar la clave almacenada en memoria

4. **Clave encontrada:**
   - Dirección de memoria: `0xc280`
   - Valor: valor específico requerido
   - Comparación: se verifica contra entrada del usuario

### Herramientas Utilizadas

1. **Ghidra:**
   - Decompilación pseudo-C
   - Análisis de flujo de control
   - Modificación binaria
   - Exportación de binarios modificados

2. **OllyDbg:**
   - Depuración paso a paso
   - Inspección de memoria
   - Búsqueda de strings
   - Análisis en tiempo de ejecución

3. **Wine (en Linux):**
   - Ejecución de binarios Windows en Linux
   - Compatibilidad con GUI Windows

4. **radare2:**
   - Análisis de binarios alternativo
   - Scripting y automatización
   - Inspección de secciones PE

## Arquitectura del Binario

### Formato
- **Tipo:** PE (Portable Executable)
- **Máquina:** x86 (32-bit Intel)
- **Subsistema:** Windows GUI/Console

### Secciones Relevantes
```
.text     - Código ejecutable
.rdata    - Datos de solo lectura (strings)
.data     - Datos modificables (almacenamiento de clave)
```

## Script de Resolución

```python
#!/usr/bin/env python3
"""
Script para resolver B1ll_Gat35
Utiliza análisis estático para extraer/verificar la clave de acceso
"""

import struct
import sys

def analizar_binario(file_path):
    """
    Analiza el binario PE para extraer información clave
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Buscar firma PE
    pe_offset = struct.unpack('<I', data[0x3c:0x40])[0]
    print(f"PE Header offset: 0x{pe_offset:x}")
    
    # Información adicional sobre el binario
    print(f"Tamaño total: {len(data)} bytes")
    
    # Buscar strings relevantes
    strings = []
    current = b''
    for byte in data:
        if 32 <= byte <= 126:  # caracteres imprimibles ASCII
            current += bytes([byte])
        else:
            if len(current) > 4:
                strings.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    # Filtrar strings potencialmente interesantes
    keywords = ['key', 'password', 'vault', 'access', 'codes', '1063340']
    interesting = [s for s in strings if any(k.lower() in s.lower() for k in keywords)]
    
    print("\nStrings potencialmente interesantes:")
    for s in interesting[:20]:  # Mostrar primeros 20
        print(f"  - {s}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 b1ll_gat35.py <binario.exe>")
        sys.exit(1)
    
    binario = sys.argv[1]
    analizar_binario(binario)
```

## Datos Extraídos

### Validación de Clave

```
Función: FUN_00407f60()
Entrada: Cadena de usuario (clave)
Salida: 0 (incorrecto) o 1 (correcto)
Comparación: Contra valor global en 0xc280
```

### Proceso de Validación

```
1. Lee entrada del usuario
2. Compara con valor almacenado en 0xc280
3. Si coinciden:
   - Retorna 0
   - Salta a bloque de éxito
   - Imprime flag
4. Si no coinciden:
   - Retorna 1
   - Salta a bloque de fallo
   - Termina
```

## Flag

```
PICOCTF{These are the access codes to the vault: 1063340}
```

## Pasos de Solución Rápida

1. **Opción 1 (Recomendada):** Usar Ghidra para modificar JNZ → JNC
2. **Opción 2:** Ejecutar en OllyDbg y buscar strings
3. **Opción 3:** Usar radare2 con scripting

## Recursos

- [Ghidra Quick Start Guide](https://ghidra-sre.org/)
- [OllyDbg Documentation](https://www.ollydbg.de/)
- [PE Format Specification](http://www.delorie.com/djgpp/doc/coff/index.html)
- [Wine Project](https://www.winehq.org/)

## Técnicas Aprendidas

1. **Análisis de binarios PE**
2. **Decompilación con Ghidra**
3. **Depuración de binarios compilados**
4. **Modificación de instrucciones x86**
5. **Búsqueda de valores almacenados en memoria**

## Referencias

- PicoCTF 2019 Reverse Engineering Challenge (400 pts)
- Tipo: Reverse Engineering / Binary Patching
- Dificultad: Hard
