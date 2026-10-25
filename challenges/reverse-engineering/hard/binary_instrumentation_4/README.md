# Binary Instrumentation 4 - Reverse Engineering (400 pts)

## Descripción Oficial

Reto de instrumentación binaria de CyLab Academy que requiere análisis dinámico avanzado y técnicas de instrumentación para extraer la bandera del binario.

## Estado

**Nota:** Este reto es específico de CyLab Academy. Se requiere acceso a la plataforma learn.cylabacademy.org para obtener:
1. Descripción completa del desafío
2. Binario ejecutable
3. Hints adicionales
4. Especificaciones técnicas exactas

## Contexto Esperado

Basándose en la progresión de desafíos de Binary Instrumentation:

### Binary Instrumentation 1 (Esperado)
- Eludir funciones de `Sleep()`
- Utilizar Frida para hooks
- Manipulación de parámetros en tiempo de ejecución

### Binary Instrumentation 2
- Interceptar llamadas a WriteFile
- Monitoreo de parámetros de memoria
- Análisis de buffers Base64

### Binary Instrumentation 3
- Extracción de payloads comprimidos LZMA
- Análisis de PE manual mapping
- Recuperación de strings Base64 de secciones .rdata

### Binary Instrumentation 4 (Este reto)

Posible progresión esperada:
- **Mayor complejidad:** APIs más sofisticadas (cifrado, red, timing)
- **Ofuscación adicional:** Anti-instrumentación, detección de Frida
- **Técnicas avanzadas:** Hooks anidados, sincronización de threads
- **Desafío de ejecución:** Evasión de detección, validaciones dinámicas

## Técnicas Esperadas para Solución

### Técnicas de Instrumentación Binaria (DBI)

1. **Frida (Recomendado para este nivel)**
   ```javascript
   // Script de Frida para Binary Instrumentation 4
   // Estructura esperada
   
   Interceptor.attach(Module.findExportByName("kernel32.dll", "CreateFileA"), {
       onEnter: function(args) {
           console.log("CreateFileA called");
           console.log("FileName:", Memory.readUtf8String(args[0]));
       },
       onLeave: function(retval) {
           console.log("CreateFileA returned:", retval);
       }
   });
   ```

2. **Intel Pin (Alternativa)**
   ```cpp
   // Tool de Pin para tracing
   // Instrumentación a nivel de instrucción
   VOID Instruction(INS ins, VOID *v) {
       INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)printip,
           IARG_INST_PTR, IARG_END);
   }
   ```

3. **DynamoRIO**
   - Control de flujo dinámico
   - Instrumentación selectiva
   - Inyección de código personalizado

### Aproximaciones de Análisis

1. **Análisis Dinámico (Runtime)**
   - Ejecutar con Frida
   - Monitorear todas las llamadas API
   - Registrar parámetros y retornos
   - Inspeccionar memoria

2. **Análisis Estático (Previo)**
   - Decompilación con Ghidra
   - Identificación de funciones clave
   - Búsqueda de strings incriptados
   - Análisis de flujo de control

3. **Análisis Híbrido (Recomendado)**
   - Análisis estático: identificar funciones objetivo
   - Análisis dinámico: instrumentar esas funciones
   - Extracción de datos en tiempo de ejecución
   - Validación de resultados

## Estructura Esperada del Script de Resolución

```python
#!/usr/bin/env python3
"""
Script para resolver Binary Instrumentation 4
Estructura esperada basada en patrones anteriores
"""

import subprocess
import sys
import json

def analyze_with_ghidra(binary_path):
    """
    Análisis estático previo
    """
    # Identificar funciones críticas
    # Buscar strings importantes
    # Mapear flujo de datos
    pass

def create_frida_script(target_functions):
    """
    Crear script de Frida para instrumentación
    """
    script = """
    // Hooks para funciones objetivo
    Interceptor.attach(Module.findExportByName(null, "CriticalFunction"), {
        onEnter: function(args) {
            console.log("CriticalFunction called with:");
            console.log("  Arg0:", args[0]);
        },
        onLeave: function(retval) {
            console.log("Returned:", retval);
        }
    });
    """
    return script

def run_instrumented_binary(binary_path, frida_script):
    """
    Ejecutar binario con instrumentación de Frida
    """
    # Conectar con dispositivo/proceso
    # Inyectar script
    # Capturar salida
    pass

def extract_flag_from_output(output):
    """
    Extraer flag de la salida capturada
    """
    # Parsear output
    # Buscar patrones de flag
    # Decodificar si es necesario
    pass

if __name__ == "__main__":
    binary = sys.argv[1] if len(sys.argv) > 1 else "target.exe"
    
    # Paso 1: Análisis estático
    print("[*] Analizando binario...")
    analyze_with_ghidra(binary)
    
    # Paso 2: Crear script de Frida
    print("[*] Creando script de instrumentación...")
    frida_script = create_frida_script([])
    
    # Paso 3: Ejecutar con Frida
    print("[*] Ejecutando binario con Frida...")
    output = run_instrumented_binary(binary, frida_script)
    
    # Paso 4: Extraer flag
    print("[*] Extrayendo flag...")
    flag = extract_flag_from_output(output)
    
    print(f"[+] Flag: {flag}")
```

## Herramientas Recomendadas

1. **Frida** - Instrumentación dinámica (Recomendado)
   ```bash
   pip install frida-tools
   frida -U -n "application.exe" -l script.js
   ```

2. **Ghidra** - Análisis estático previo
   ```bash
   ghidra &
   ```

3. **Process Monitor** - Monitoreo de API calls
4. **Wireshark** - Si hay comunicación de red
5. **Python** - Scripting de resolución

## Instalación de Frida

```bash
# En la máquina host (Linux/Mac)
pip install frida
pip install frida-tools

# En dispositivo Windows (si es remoto)
# Descargar server de Frida
# https://github.com/frida/frida/releases

# Instalar SDK (opcional para desarrollo)
pip install frida-python
```

## Monitoreo Esperado en Runtime

- Llamadas a CreateFileA/CreateFileW
- WriteFile / ReadFile
- GetProcAddress
- LoadLibraryA/LoadLibraryW
- Operaciones criptográficas (si aplica)
- Llamadas a APIs de red (si aplica)

## Flag Esperada

```
academy{...}  # Pendiente de información de plataforma
```

## Recursos

- [Frida Documentation](https://frida.re/)
- [Frida - Hook Functions](https://frida.re/docs/javascript-api/)
- [Intel Pin Tool](https://www.intel.com/content/www/us/en/developer/articles/tool/pin-a-dynamic-binary-instrumentation-tool.html)
- [DynamoRIO](https://dynamorio.org/)
- [Ghidra Scripting](https://ghidra-sre.org/)

## Referencias

- CyLab Academy - Reverse Engineering Hard Challenge
- Técnicas: Dynamic Binary Instrumentation, Frida, API Hooking
- Dificultad: Hard (400 pts)
- Nivel: Avanzado

## Notas de Desarrollo

Este README será actualizado cuando se obtenga:
1. Acceso a learn.cylabacademy.org
2. Descripción oficial del reto
3. Binario ejecutable
4. Información técnica específica
5. Flag válida

**Estado:** Pendiente de información de plataforma
**Última actualización:** 2026-10-24
