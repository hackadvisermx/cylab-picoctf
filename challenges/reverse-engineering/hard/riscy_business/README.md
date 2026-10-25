# Reverse Engineering — riscy business

## Descripción

> **Prompt oficial del reto:** "Reverse engineer a RISC-V binary to extract the flag."

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF
- **Puntos:** (desconocido)
- **ID CyLab:** 219

## Solución

El reto proporciona un binario ELF compilado para arquitectura **RISC-V de 64 bits** (no x86/ARM). El programa verifica cada byte del input contra la flag de forma iterativa.

### Requisitos de emulación

RISC-V no es una arquitectura de procesador común, por lo que necesita emulación:

1. **Instalar herramientas RISC-V:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install qemu-user qemu-user-static gdb-multiarch
   
   # Verificar instalación
   qemu-riscv64 --version
   gdb-multiarch --version
   ```

2. **Verificar tipo de binario:**
   ```bash
   file wizardlike_riscv
   # Output: ELF 64-bit LSB executable, RISC-V, RV64I, version 1 (SYSV), dynamically linked
   ```

### Técnica: Debugging con GDB + QEMU

1. **Iniciar QEMU en modo debug:**
   ```bash
   qemu-riscv64 -g 1234 ./wizardlike_riscv
   # QEMU se detiene y espera conexión en puerto 1234
   ```

2. **Conectar GDB en otra terminal:**
   ```bash
   gdb-multiarch ./wizardlike_riscv
   (gdb) target remote :1234
   (gdb) continue
   ```

3. **Identificar función de verificación:**
   - Usar `info functions` para listar funciones
   - Buscar funciones de comparación de strings
   - Poner breakpoint en función de validación

4. **Extraer flag byte a byte:**
   ```bash
   # En GDB, si el programa pide input:
   # Ingresar "A" y ver dónde falla la comparación
   (gdb) run
   > A
   # El programa compara con el primer byte de la flag
   # Revisar registros para ver qué espera
   (gdb) info registers
   (gdb) x/i $pc  # mostrar instrucción actual
   ```

### Técnica: Automatización con pwntools

```python
#!/usr/bin/env python3
from pwn import *

# Conectar al binario via QEMU
# Nota: requiere configurar QEMU previamente en modo debug
context.log_level = 'debug'

# Iterar sobre caracteres ASCII para encontrar la flag
flag = ""
for pos in range(64):  # asumiendo flag de ~64 caracteres
    for ascii_val in range(32, 127):
        char = chr(ascii_val)
        attempt = flag + char + "A" * (63 - len(flag) - 1)
        
        # Ejecutar el programa con el intento
        # (Esto depende de cómo se estructure el programa)
        
        # Si el programa responde diferente para este carácter,
        # es probable que sea el correcto
        if is_correct_char(attempt):
            flag += char
            print(f"[+] Flag so far: {flag}")
            break

print(f"[+] Flag: {flag}")
```

### Notas de RISC-V

- RISC-V es una ISA (Instruction Set Architecture) abierta
- RV64I es la versión de 64 bits básica sin extensiones
- Los registros de RISC-V tienen nombres distintos: a0-a7 (argumentos), t0-t6 (temporales), etc.
- La convención de llamada es diferente a x86/ARM

## Flag

(Se extrae del binario mediante debugging - la técnica es más importante que memorizarla)

## Notas adicionales

- Este reto es notablemente difícil debido a la rareza de RISC-V en CTFs
- Solo ~72 equipos resolvieron este reto en picoCTF original
- La clave es reconocer el tipo de binario temprano y configurar el entorno correcto
- GDB multiarch es esencial para debugging de arquitecturas no-convencionales

## Referencias

- Writeup: https://pc-b.github.io/posts/riscy-business/
- GitHub Gist (solución): https://gist.github.com/spezifisch/b8d15ccb2a2577a7a8e3830ef5fce8e0
- RISC-V Spec: https://riscv.org/specifications/
- QEMU RISC-V: https://wiki.qemu.org/Documentation/Platforms/RISCV
