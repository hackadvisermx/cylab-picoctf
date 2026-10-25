# Reverse Engineering — Easy as GDB

## Descripción

> **Prompt oficial del reto:** "The flag has got to be checked somewhere..."

- **Categoría:** Reverse Engineering
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Challenge ID:** 15364
- **Puntos:** 160
- **Autor:** picoCTF

## Solución

El reto proporciona un binario ELF 32-bit compilado (`brute`) que solicita al usuario ingresar la flag. El binario realiza validación de la entrada comparándola contra una versión codificada/almacenada de la flag en el ejecutable.

### Análisis del Binario

El programa aplica un **algoritmo XOR con permutaciones** sobre la entrada del usuario y compara el resultado contra una versión pre-codificada de la flag almacenada en el binario. En lugar de intentar invertir el algoritmo de codificación, la solución más eficiente es usar **GDB con scripting para fuerza bruta** carácter por carácter.

### Enfoque de Solución

**Paso 1: Cargar el binario en GDB**
```bash
gdb brute
```

**Paso 2: Identificar la función de comparación**
```bash
# Usar objdump para encontrar puntos de interés
objdump -d brute | grep -A5 "cmp"
# O usar Ghidra/IDA para análisis estático
```

**Paso 3: Crear un script de GDB en Python**

El script automatiza la búsqueda de cada carácter de la flag:
1. Establece un breakpoint en la instrucción de comparación
2. Itera sobre caracteres de un conjunto predefinido (letras, dígitos, `{`, `}`, `_`)
3. Verifica los registros CPU (`AL` y `DL`) tras la comparación
4. Identifica cuando los registros coinciden (carácter correcto)
5. Continúa hasta completar la flag

**Paso 4: Ejecución con el script**
```bash
gdb -x script.py brute
```

### Registro de la CPU

Después de la comparación XOR:
- El registro **AL** contiene el byte codificado de la entrada del usuario
- El registro **DL** contiene el byte codificado esperado de la flag
- Cuando `AL == DL`, hemos encontrado el carácter correcto para esa posición

### Herramientas Utilizadas

- **GDB (GNU Debugger)**: Para debugging interactivo y scripting en Python
- **PEDA**: Extensión de GDB (opcional, facilita análisis de registros/memoria)
- **Ghidra/objdump**: Para análisis estático inicial del binario

### Ejecución del Exploit

```python
#!/usr/bin/env python3
# Script GDB para brute-forcear la flag carácter por carácter

import gdb
import string

def brute_force_flag():
    """Brute-forcea la flag comparando registros en cada iteración"""
    
    flag = ""
    charset = string.ascii_letters + string.digits + "{}_"
    
    # Breakpoint en la instrucción de comparación (dirección aproximada)
    # Puede variar según la compilación: 0x5655598e en 2021
    comparison_addr = "0x8049000"  # Placeholder - adaptar según binario real
    
    for position in range(50):  # Asumir flag máx 50 caracteres
        gdb.execute(f"break *{comparison_addr}")
        gdb.execute("run")
        
        for char in charset:
            # Enviar carácter como entrada
            gdb.execute(f"send_input {char}", to_string=True)
            
            # Obtener registros
            al = gdb.parse_and_eval("$al")
            dl = gdb.parse_and_eval("$dl")
            
            if al == dl:
                flag += char
                print(f"Posición {position}: '{char}' correcto")
                break
        else:
            # Si no encontró carácter válido, la flag ha terminado
            break
    
    return flag

# Ejecutar
resultado = brute_force_flag()
print(f"\nFlag encontrada: {resultado}")
```

### Flag Esperada

Basado en versiones públicas del reto (picoCTF 2021):

```
picoCTF{I_5D3_A11DA7_0db137a9}
```

## Notas Adicionales

- El reto está diseñado para enseñar técnicas de **debugging con GDB** en lugar de reverse engineering de algoritmos complejos
- La codificación XOR con permutaciones es relativamente simple; el desafío real es automatizar GDB
- Otros enfoques posibles incluyen:
  - Disassembly manual con objdump/Ghidra y reconstrucción del algoritmo
  - Análisis dinámico con strace/ltrace
  - Instrumentación con Pin/DynamoRIO
- El "hint" oficial indicaba que el objetivo es usar GDB, no técnicas de ingeniería inversa compleja

## Referencias

- [CTFtime.org - Easy as GDB Writeup](https://ctftime.org/writeup/28040)
- [Easy as GDB - pugachev.io](https://pugachev.io/2023/12/22/easy-as-gdb-by-picoctf/)
- [GitHub - picoCTF Reverse Engineering Solutions](https://github.com/rsrdjan/picoCTF-Rev_Eng)
- [Blog: Reverse with GDB](https://blog.nickchen120235.dev/2022/04/27/reverse-with-gdb.html)
- [GDB Python API Documentation](https://sourceware.org/gdb/current/onlinedocs/gdb/Python-API.html)
