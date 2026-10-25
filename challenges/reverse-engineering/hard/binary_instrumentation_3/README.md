# Binary Instrumentation 3 - Reverse Engineering (400 pts)

## Descripción Oficial

"The executable was designed to write the flag but it seems like I messed up a few things on the way. Can you find a way to get it to work?"

El desafío requiere identificar y extraer el payload oculto del binario, descomprimirlo y recuperar la bandera.

## Contexto

- **Objetivo:** Extraer y analizar un binario comprometido
- **Tipo:** Instrumentación binaria, extracción de payloads
- **Técnicas:** LZMA decompresión, PE manual mapping (reflective loading)
- **Dificultad:** Hard (400 pts)
- **Plataforma:** Windows (binario PE)

## Análisis Técnico

### Arquitectura del Desafío

El binario consta de **dos capas:**

1. **Binario Externo:** Intenta cargar un payload interno
2. **Payload Comprimido:** LZMA, almacenado en sección PE personalizada
3. **Payload Descomprimido:** Ejecutable PE adicional con la lógica real
4. **Flag Encriptada:** Base64 codificada dentro del payload

### Paso 1: Análisis de Secciones PE

```bash
# Comando para listar secciones
objdump -h binario.exe
# o en Ghidra:
# View > Memory Map
```

**Sección personalizada encontrada:**
```
.ATOM  457KB (0x73400 bytes)
Tipo: Payload comprimido
Formato: LZMA "Alone"
Magic Bytes: 5d 00 00 10 00
```

### Paso 2: Detección de Compresión LZMA

**Magic Bytes de LZMA "Alone":**
```
5d 00 00 10 00
```

Donde:
- `5d` = Byte de propiedades LZMA
- `00 00 10 00` = Tamaño descomprimido (big-endian)

### Paso 3: Decompresión LZMA

**Script Python para decompresión:**

```python
#!/usr/bin/env python3
import lzma
import sys

def extract_and_decompress_lzma(exe_path, output_path):
    """
    Extrae la sección .ATOM y descomprime el payload LZMA
    """
    with open(exe_path, 'rb') as f:
        exe_data = f.read()
    
    # Buscar magic bytes de LZMA
    lzma_magic = b'\x5d\x00\x00\x10\x00'
    
    idx = exe_data.find(lzma_magic)
    if idx == -1:
        print("No se encontraron datos LZMA")
        return None
    
    print(f"Datos LZMA encontrados en offset: 0x{idx:x}")
    
    # Extraer datos LZMA (desde el magic byte)
    lzma_data = exe_data[idx:]
    
    try:
        # Python's lzma puede no soportar el formato "Alone" sin ajustes
        # Usamos el modo raw para manejar streams incompletos
        decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
        decompressed = decompressor.decompress(lzma_data)
        
        # Guardar payload descomprimido
        with open(output_path, 'wb') as f:
            f.write(decompressed)
        
        print(f"Payload descomprimido: {len(decompressed)} bytes")
        print(f"Guardado en: {output_path}")
        
        return decompressed
    
    except Exception as e:
        print(f"Error en decompresión: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 extract_lzma.py <binario.exe> <salida.bin>")
        sys.exit(1)
    
    extract_and_decompress_lzma(sys.argv[1], sys.argv[2])
```

### Paso 4: Análisis del Payload Descomprimido

Una vez descomprimido, el payload es un **binario PE válido**:

- **Cabecera PE:** Está presente y válida
- **Secciones:** .text, .rdata, .data, etc.
- **Punto de entrada:** Función main

### Paso 5: Análisis del Binario Externo

**Problema identificado:**
```
El binario externo intenta hacer "reflective loading" (PE manual mapping)
Dirección objetivo: 0x400000 (ImageBase específico)
En Wine: La asignación de memoria falla sin manejo de errores
Resultado: Crash durante copia de secciones PE
```

**Técnica de reflective loading:**
```c
// Pseudo-código del binario externo
void* allocated = VirtualAlloc(ImageBase, size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
if (!allocated) {
    // El binario no maneja este error en Wine
    // Continúa y crashea
    return;
}

// Copiar secciones PE
memcpy(allocated, payload_data, size);

// Ejecutar
((void (*)(void))allocated)();
```

### Paso 6: Pivote a Análisis Estático

Debido a problemas en tiempo de ejecución, cambiar a **análisis estático**:

1. **Abrir payload descomprimido en Ghidra**
2. **Buscar cadenas de texto**
3. **Localizar función que genera flag**

### Paso 7: Recuperación de Flag

**Ubicación de flag:**
```
Símbolo C++ mangled: _ZL9flagParts
Tipo: Array de std::string (5 elementos)
Ubicación: Sección .rdata
```

**Contenido del array:**
```
flagParts[0] = "cGljb0NU"          (base64)
flagParts[1] = "Rns..."            (base64)
flagParts[2] = "..."               (base64)
...
```

**Decodificación:**
```python
import base64

# Segmentos codificados encontrados
segments = [
    "cGljb0NU",      # "picoCTF" cuando se decodifica
    "Rns..."         # más segmentos...
]

# Concatenar y decodificar
combined = ''.join(segments)
flag = base64.b64decode(combined).decode('ascii')
print(f"Flag: {flag}")
```

## Script Completo de Resolución

```python
#!/usr/bin/env python3
"""
Script completo para resolver Binary Instrumentation 3
1. Extrae payload LZMA
2. Descomprime
3. Extrae strings y base64
4. Recupera flag
"""

import lzma
import base64
import struct
import sys

def extract_payload(exe_path):
    """Extrae datos LZMA del binario"""
    with open(exe_path, 'rb') as f:
        data = f.read()
    
    # Buscar magic bytes LZMA
    lzma_magic = b'\x5d\x00\x00\x10\x00'
    idx = data.find(lzma_magic)
    
    if idx == -1:
        return None
    
    return data[idx:]

def decompress_lzma(lzma_data):
    """Descomprime payload LZMA"""
    try:
        decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
        return decompressor.decompress(lzma_data)
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_strings_from_binary(binary_data):
    """Extrae strings ASCII del binario"""
    strings = []
    current = b''
    
    for byte in binary_data:
        if 32 <= byte <= 126:
            current += bytes([byte])
        else:
            if len(current) > 3:
                strings.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    return strings

def find_flag_components(binary_data):
    """Busca componentes de flag en base64"""
    strings = extract_strings_from_binary(binary_data)
    
    # Filtrar strings que parecen base64
    base64_strings = []
    for s in strings:
        if all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in s):
            if len(s) > 4:
                base64_strings.append(s)
    
    return base64_strings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 bi3_solver.py <binario.exe>")
        sys.exit(1)
    
    exe_path = sys.argv[1]
    
    # Paso 1: Extraer payload LZMA
    print("[*] Extrayendo payload LZMA...")
    lzma_data = extract_payload(exe_path)
    if not lzma_data:
        print("[-] No se encontró payload LZMA")
        sys.exit(1)
    
    print(f"[+] Payload LZMA encontrado ({len(lzma_data)} bytes)")
    
    # Paso 2: Descomprimir
    print("[*] Descomprimiendo LZMA...")
    decompressed = decompress_lzma(lzma_data)
    if not decompressed:
        print("[-] Fallo en decompresión")
        sys.exit(1)
    
    print(f"[+] Descomprimido ({len(decompressed)} bytes)")
    
    # Paso 3: Extraer componentes de flag
    print("[*] Buscando componentes de flag...")
    components = find_flag_components(decompressed)
    
    print(f"[+] Encontrados {len(components)} strings base64")
    
    # Paso 4: Reconstruir flag
    if components:
        combined = ''.join(sorted(components)[:5])  # Tomar primeros 5
        try:
            flag = base64.b64decode(combined).decode('ascii')
            print(f"\n[+] FLAG: {flag}")
        except Exception as e:
            print(f"[-] Error decodificando: {e}")
```

## Técnicas Anti-Ingeniería Inversa Encontradas

1. **Compresión LZMA:** Ofusca el payload dentro del binario
2. **Reflective Loading:** Intenta eludir detección de carga de DLL
3. **Magic Bytes Específicos:** Marca la sección de payload
4. **Base64 Encoding:** Adicional obfuscación de strings

## Defensa del Sistema de EDR

Un EDR debería monitorear:
- **Secciones PE no estándar** (.ATOM)
- **Asignación de memoria sin archivo en disco**
- **Secuencias de copia de memoria** características de PE mapping
- **Ejecución de código desde memoria asignada**

## Flag

```
picoCTF{411_4r3_4p15_n07h1n9_3l53_0cfabbfe}
```

## Recursos

- [LZMA Format Specification](https://tukaani.org/lzma/)
- [PE Format Documentation](https://docs.microsoft.com/en-us/windows/win32/debug/pe-format)
- [Ghidra String Search](https://ghidra-sre.org/)
- [Python lzma Module](https://docs.python.org/3/library/lzma.html)

## Referencias

- PicoCTF 2019 Reverse Engineering Challenge (400 pts)
- Técnicas: Payload extraction, LZMA decompression, PE analysis, Static analysis
- Herramientas: Python, Ghidra, hexdump, strings
