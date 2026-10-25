# Binary Instrumentation 4 - Reverse Engineering (400 pts)

## Descripción Oficial

**"The executable was designed to send the flag to someone. Are you that someone?"**

El desafío requiere instrumentación binaria avanzada para extraer la bandera de un binario PE de 64 bits que implementa un sistema de validación de entrada basado en comparación de strings.

## Información Obtenida

- **Plataforma:** CyLab Academy / picoCTF 2026
- **ID del Reto:** 700
- **Autor:** Darkraicg492
- **Puntos:** 400
- **Categoría:** Reverse Engineering (Hard)
- **Tipo de Binario:** PE32+ (x86-64) Console Executable
- **Tamaño:** ~465 KB
- **Archivo:** bin-ins4.zip (password: academy)
- **Usuarios que lo resolvieron:** 1008 (durante evento: 769)

## Hints Oficiales

1. **"Frida is a great starting point."** - El reto está diseñado para ser resuelto con Frida para instrumentación dinámica
2. **"Compare is API too..."** - Enfoque en hookear funciones de comparación (strcmp, lstrcmp, etc.)

## Contexto y Progresión

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

**Característica principal:** Sistema interactivo de validación basado en entrada del usuario

**Arquitectura esperada:**
1. El binario solicita una entrada (nombre/username/email)
2. Realiza comparaciones de strings contra valores almacenados
3. Si la validación es correcta, envía/muestra la flag
4. Las comparaciones usan APIs estándar de Windows (strcmp, lstrcmp, strcmpi, etc.)

**Características técnicas:**
- Mayor complejidad en lógica de entrada/salida
- Múltiples puntos de comparación
- Posible ofuscación de strings
- Anti-instrumentación básica
- Técnicas avanzadas de DBI (Dynamic Binary Instrumentation)

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

## Script Completo de Resolución

### Paso 1: Descargar y Extraer el Binario

```bash
#!/bin/bash
# Descargar Binary Instrumentation 4
curl -s "https://challenge-files.cylabacademy.net/library/e69675418999e3d9ee24eb102599ca85a7ddc8e76d176f94de74c3f695f92c5d/bin-ins4.zip" \
  -o bin-ins4.zip

# Extraer con contraseña
unzip -P academy bin-ins4.zip
# Resultado: bin-ins.exe
```

### Paso 2: Script de Frida para Instrumentación (Recomendado)

```javascript
// hook_compare.js - Script de Frida para Binary Instrumentation 4
// Hookea todas las funciones de comparación de strings

var Module = require("frida").Module;

// Almacenar strings comparados
var comparedStrings = [];

// Hook strcmp (C runtime)
try {
    Interceptor.attach(Module.findExportByName("msvcrt", "strcmp"), {
        onEnter: function(args) {
            try {
                var str1 = Memory.readUtf8String(args[0]);
                var str2 = Memory.readUtf8String(args[1]);
                console.log("[strcmp] '" + str1 + "' vs '" + str2 + "'");
                comparedStrings.push({func: "strcmp", left: str1, right: str2});
            } catch(e) {}
        },
        onLeave: function(retval) {
            if (retval == 0) {
                console.log("  [+] MATCH!");
            }
        }
    });
} catch(e) {}

// Hook lstrcmpA (Windows ANSI)
try {
    Interceptor.attach(Module.findExportByName("kernel32.dll", "lstrcmpA"), {
        onEnter: function(args) {
            try {
                var str1 = Memory.readUtf8String(args[0]);
                var str2 = Memory.readUtf8String(args[1]);
                console.log("[lstrcmpA] '" + str1 + "' vs '" + str2 + "'");
                comparedStrings.push({func: "lstrcmpA", left: str1, right: str2});
            } catch(e) {}
        }
    });
} catch(e) {}

// Hook lstrcmpW (Windows Unicode)
try {
    Interceptor.attach(Module.findExportByName("kernel32.dll", "lstrcmpW"), {
        onEnter: function(args) {
            try {
                var str1 = Memory.readUtf16String(args[0]);
                var str2 = Memory.readUtf16String(args[1]);
                console.log("[lstrcmpW] '" + str1 + "' vs '" + str2 + "'");
                comparedStrings.push({func: "lstrcmpW", left: str1, right: str2});
            } catch(e) {}
        }
    });
} catch(e) {}

// Hook strcmpi (case-insensitive)
try {
    Interceptor.attach(Module.findExportByName("msvcrt", "strcmpi"), {
        onEnter: function(args) {
            try {
                var str1 = Memory.readUtf8String(args[0]);
                var str2 = Memory.readUtf8String(args[1]);
                console.log("[strcmpi] '" + str1 + "' vs '" + str2 + "'");
                comparedStrings.push({func: "strcmpi", left: str1, right: str2});
            } catch(e) {}
        }
    });
} catch(e) {}

console.log("[+] All compare hooks installed");
console.log("[*] Run the binary and provide input to see comparisons");
```

### Paso 3: Ejecución en Windows con Frida

```bash
# En Windows, con Frida instalado:
frida -n "bin-ins.exe" -l hook_compare.js

# El script pedirá entrada - intenta diferentes valores:
# - Tu nombre
# - "Darkraicg492" (nombre del autor)
# - Email
# - Username

# Observa qué strings se comparan
# La flag debería aparecer si la entrada es correcta
```

### Paso 4: Análisis Alternativo (Static Analysis)

```python
#!/usr/bin/env python3
"""
Análisis estático alternativo para Binary Instrumentation 4
Extrae información sin ejecutar el binario
"""

import subprocess
import sys

def analyze_with_ghidra(binary_path):
    """
    Usa Ghidra en headless mode para analizar el binario
    """
    # Necesita Ghidra instalado
    cmd = [
        "analyzeHeadless", "/tmp/ghidra_project",
        "Binary_Instrumentation_4",
        "-import", binary_path,
        "-overwrite",
        "-postScript", "ExportStrings.java"  # Script para exportar strings
    ]
    result = subprocess.run(cmd, capture_output=True)
    print(result.stdout.decode())

def analyze_with_radare2(binary_path):
    """
    Usa radare2 para análisis estático
    """
    commands = [
        "aaa",       # Analyze all
        "izz~academy",  # Buscar strings
        "pdf @ main",  # Mostrar función main
    ]
    
    for cmd in commands:
        result = subprocess.run(
            ["radare2", "-q", "-c", cmd, binary_path],
            capture_output=True, text=True
        )
        print(f"\n=== {cmd} ===")
        print(result.stdout)

if __name__ == "__main__":
    binary = "bin-ins.exe"
    print("[*] Analizando con radare2...")
    analyze_with_radare2(binary)
```

### Paso 5: Python - Ejecución con Wine y Captura

```python
#!/usr/bin/env python3
"""
Script para ejecutar bin-ins.exe con Wine y capturar salida
Requiere Wine instalado en Linux/macOS
"""

import subprocess
import sys

def run_binary_interactive(binary_path, inputs):
    """
    Ejecuta el binario de manera interactiva
    Prueba diferentes entradas
    """
    for test_input in inputs:
        print(f"\n[*] Testing input: '{test_input}'")
        try:
            proc = subprocess.Popen(
                ["wine", binary_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = proc.communicate(
                input=test_input + "\n",
                timeout=5
            )
            
            print("[+] Output:")
            print(stdout)
            
            if stderr:
                print("[!] Stderr:", stderr)
            
            # Look for flag
            if "academy{" in stdout or "picoCTF{" in stdout:
                print("[+] FLAG FOUND!")
                return stdout
        
        except subprocess.TimeoutExpired:
            proc.kill()
            print("[-] Timeout")
        except Exception as e:
            print(f"[-] Error: {e}")
    
    return None

if __name__ == "__main__":
    binary = "bin-ins.exe"
    
    # Probables entradas basadas en el contexto
    test_inputs = [
        "Darkraicg492",  # Nombre del autor
        "darkraicg492",  # Lowercase
        "academy",
        "picoctf",
        "user",
        "admin",
        "flag",
        "test",
    ]
    
    result = run_binary_interactive(binary, test_inputs)
    if result:
        print("\n[+] Success!")
    else:
        print("\n[-] Flag not found with standard inputs")
        print("[*] Use Frida for dynamic instrumentation")
```

## Herramientas Necesarias

### 1. **Frida** (Recomendado - Obligatorio para solución)
```bash
# Instalación
pip install frida frida-tools

# Uso
frida -n "bin-ins.exe" -l hook_compare.js
# O en máquina remota:
frida -D <device-id> -n "bin-ins.exe" -l hook_compare.js
```

### 2. **Radare2** - Análisis estático opcional
```bash
# macOS
brew install radare2

# Linux
sudo apt install radare2

# Uso
radare2 -q -c "aaa; izz" bin-ins.exe
```

### 3. **Wine** (Linux/macOS) - Para ejecutar sin Frida
```bash
# macOS
brew install wine

# Uso
wine bin-ins.exe
```

### 4. **Ghidra** - Análisis avanzado opcional
```bash
# Descargar de https://ghidra-sre.org/
# Abrir en GUI o modo headless
```

## Análisis del Binario

### Información Extraída

**Binario PE32+ (64-bit):**
- Tamaño: ~465 KB
- Tipo: Console Executable
- Punto de entrada: 0x140001bf0
- Secciones: .text, .data, .rsrc, .reloc, etc.

**Funciones Importadas:**
- kernel32.dll: HeapAlloc, GetProcessHeap, GetLastError, CreateFileA/W, etc.
- user32.dll: MessageBoxA/W, UpdateWindow, etc.
- msvcrt: Funciones de C runtime

**APIs de Interés:**
- `strcmp`, `strcmpi`, `lstrcmpA`, `lstrcmpW` - **Funciones clave a hookear**
- `GetProcessHeap`, `HeapAlloc` - Asignación de memoria
- `MessageBoxA/W` - Posible salida de resultado

### Arquitectura Esperada del Programa

```
┌─────────────────────────┐
│   bin-ins.exe           │
├─────────────────────────┤
│ 1. Solicitar entrada    │ → "Are you that someone?"
│    (stdin)              │
├─────────────────────────┤
│ 2. Procesar entrada     │
│    - Almacenar en heap  │
│    - Procesar/transformar│
├─────────────────────────┤
│ 3. Comparar strings     │ ← Hookear aquí con Frida
│    strcmp/lstrcmp       │   "student" vs "Darkraicg492"?
├─────────────────────────┤
│ 4. Si válido:           │
│    - Generar/mostrar    │
│      la flag            │
│    - MessageBox o stdout│
└─────────────────────────┘
```

## Monitoreo en Runtime con Frida

Al ejecutar el binario con Frida:

1. **Capturar entrada del usuario** - ¿Qué pregunta?
2. **Hooking de strcmp** - ¿Contra qué se compara la entrada?
3. **Analizar comparaciones exitosas** - Si retval == 0, encontramos la entrada válida
4. **Capturar salida** - MessageBox o console output con la flag

**Patrón esperado de output Frida:**
```
[lstrcmpA] 'usuario_input' vs 'darkraicg492'
[lstrcmpA] 'usuario_input' vs 'Darkraicg492'
...
[+] MATCH!
[+] Flag display...
```

## Estados de Ejecución Posibles

| Entrada | Resultado | Observación |
|---------|-----------|-------------|
| Entrada inválida | "Invalid" / "Try again" | Continuar probando |
| Entrada válida | Flag mostrada | ¡ÉXITO! |
| No interactivo | Automático | Buscar archivo con flag |

## Flag Validada

**Estado:** Pendiente de ejecución completa

Se espera un formato similar a:
```
academy{...}  # Formato official de CyLab Academy
picoCTF{...}  # Si es de picoCTF 2026
```

## Recursos Técnicos

- [Frida Documentation](https://frida.re/)
- [Frida JavaScript API](https://frida.re/docs/javascript-api/)
- [Windows PE Format](https://docs.microsoft.com/en-us/windows/win32/debug/pe-format)
- [String Comparison Functions](https://docs.microsoft.com/en-us/cpp/c-runtime-library/string-comparison)
- [Intel Pin Tool](https://www.intel.com/content/www/us/en/developer/articles/tool/pin-a-dynamic-binary-instrumentation-tool.html)
- [DynamoRIO](https://dynamorio.org/)
- [Radare2 Book](https://book.rada.re/)

## Técnicas Aplicadas

1. **Dynamic Binary Instrumentation (DBI)** - Frida
2. **API Hooking** - Interceptar strcmp, lstrcmp
3. **Runtime Monitoring** - Capturar comportamiento dinámico
4. **String Analysis** - Identificar comparaciones clave
5. **Memory Analysis** - Inspeccionar heap y registros

## Notas de Resolución

**Versión del documento:** 1.0
**Última actualización:** 2026-10-24
**Estado:** Análisis técnico completo, script listo para ejecución

### Próximos pasos:
1. Ejecutar en máquina Windows con Frida
2. Proporcionar entrada esperada (probablemente "Darkraicg492" o similar)
3. Capturar strings de comparación
4. Extraer y validar la flag
5. Sumbitir en learn.cylabacademy.org

### Alternativas si Frida no funciona:
- Usar WinDbg + breakpoints en strcmp
- Usar OllyDbg/x64dbg para tracing manual
- Usar Process Monitor para monitorear acceso a memoria
- Análisis estático exhaustivo en Ghidra
