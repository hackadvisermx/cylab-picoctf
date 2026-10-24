# Reverse Engineering — WinAntiDbg0x200

## Descripción
> **Prompt oficial del reto:** "If you have solved WinAntiDbg0x100, you'll discover something new in this one. Debug the executable and find the flag!
>
> This challenge executable is a Windows console application, and you can start by running it using Command Prompt on Windows.
>
> This executable requires admin privileges. You might want to start Command Prompt or your debugger using the 'Run as administrator' option.
>
> Challenge can be downloaded [here](https://challenge-files.cylabacademy.net/library/842fd067da1fb3a42394847ad47fa3f7a479a37a676e8053f175959077b9930e/WinAntiDbg0x200.zip). Unzip the archive with the password `academy`"
>
> **Pistas oficiales:**
> 1. Hints will be displayed to the Debug console. Good luck!

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** Nandan Desai

## Solución
El reto expande los conceptos de `WinAntiDbg0x100`, incorporando creación de procesos hijos y múltiples verificaciones de estado entre rutinas de transformación de datos.

### Análisis del binario

1. **Estructura de `config.bin`:**
   Al igual que en `0x100`, el archivo contiene un entero de longitud (en este caso 37 bytes), una primera parte (`part1`) de texto ASCII y una segunda parte (`part2`) con bytes cifrados.

2. **Flujo de ejecución y rutinas de transformación:**
   La función de transformación (`0x401090`) es idéntica a la de `0x100`, aplicando una rotación sobre el alfabeto minúsculo basada en el número de bits activos (*popcount*) de la posición:
   $$\text{shift} = \text{popcount}(j \pmod{255})$$
   $$c_j \leftarrow 'a' + ((c_j - 'a' + \text{shift}) \pmod{26})$$

3. **Mecanismo Anti-Debugging e hilos de ejecución:**
   - En `0x401812`: se ejecuta la transformación con argumento $3$.
   - En `0x40181c`: se llama a la subrutina `0x4011d0`, la cual:
     - Ejecuta la transformación con argumento $5$.
     - Lanza un subproceso hijo (`CreateProcessW`) para realizar validaciones en paralelo.
     - Espera al subproceso con `WaitForSingleObject` y ejecuta la transformación con argumento $4$.
     - Verifica el código de salida del hijo (`0xBEEF`) mediante `GetExitCodeProcess` y ejecuta la transformación con argumento $4$.
   - Al retornar a la función principal, si el depurador no es detectado (`IsDebuggerPresent` retorna 0 en `0x401828`), ejecuta una última ronda de transformación con argumento $1$.
   - El número total de rondas acumuladas en una ejecución limpia y legítima es:
     $$3 + 5 + 4 + 4 + 1 = 17 \text{ rondas}$$
   - Finalmente, en `0x401180`, se realiza un XOR byte a byte entre `part1` (transformada 17 veces) y `part2`.

### Script de resolución estática (Python)

```python
import struct

with open("config.bin", "rb") as f:
    data = f.read()

length = struct.unpack("<I", data[:4])[0]
part1 = bytearray(data[4 : 4 + length])
part2 = bytearray(data[4 + length + 1 : 4 + length + 1 + length])

def transform(buf, count):
    for _ in range(count):
        for j in range(len(buf)):
            shift = bin(j % 255).count("1")
            val = buf[j] - ord("a")
            val = (val + shift) % 26
            buf[j] = ord("a") + val

# Total acumulado de 17 rondas de transformación
transform(part1, 17)

flag = bytes([a ^ b for a, b in zip(part1, part2)]).decode("latin1")
print(flag)
```

Al ejecutar el script sobre `config.bin`, se obtiene la flag en formato `academy{...}`.

```bash
python3 solve.py
```

## Notas adicionales
En un entorno dinámico sobre Windows, el reto requiere privilegios de administrador (`SeDebugPrivilege`) debido a la creación del proceso hijo con flags de depuración supervisada. El análisis estático evita la complejidad del entorno emulado o de máquinas virtuales Windows.

## Referencias
- Reto: https://learn.cylabacademy.org/library/430
- Apoyo: https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw
