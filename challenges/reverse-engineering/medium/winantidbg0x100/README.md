# Reverse Engineering — WinAntiDbg0x100

## Descripción
> **Prompt oficial del reto:** "This challenge will introduce you to 'Anti-Debugging.' Malware developers don't like it when you attempt to debug their executable files because debugging these files reveals many of their secrets! That's why, they include a lot of code logic specifically designed to interfere with your debugging process.
>
> Now that you've understood the context, go ahead and debug this Windows executable!
>
> This challenge binary file is a Windows console application and you can start with running it using `cmd` on Windows.
>
> Challenge can be downloaded [here](https://challenge-files.cylabacademy.net/library/d8cfd1a0bd55ecb5969f0cf29f61c0583e3722489583a13460000bb6fb0e8585/WinAntiDbg0x100.zip). Unzip the archive with the password `academy`"
>
> **Pistas oficiales:**
> 1. Hints will be displayed to the Debug console. Good luck!

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** Nandan Desai

## Solución
El reto proporciona un archivo ZIP protegido por contraseña (`academy`) que contiene `WinAntiDbg0x100.exe` y un archivo de configuración cifrado `config.bin`.

### Análisis del binario

1. **Lectura de `config.bin`:**
   Al inicio, el binario busca y lee `config.bin` en el mismo directorio de ejecución. `config.bin` tiene una estructura con:
   - Primeros 4 bytes: entero de longitud en little-endian ($41$ bytes).
   - Bloque 1 ($41$ bytes): cadena de texto en minúsculas utilizada como buffer intermedio.
   - Byte nulo separador.
   - Bloque 2 ($41$ bytes): secuencia cifrada de bytes.

2. **Mecanismo Anti-Debugging:**
   En la dirección `0x4015fc`, el ejecutable llama a `IsDebuggerPresent()`. Si detecta un depurador (`EAX == 1`), imprime un mensaje de error y finaliza la ejecución:
   ```assembly
   0x4015fc: call *0x403014  ; IsDebuggerPresent
   0x401602: test eax, eax
   0x401604: je   0x40161b   ; Si EAX == 0, continúa al bloque de descifrado
   ; Si EAX != 0: Mensaje de debugger detectado y salida
   ```

3. **Algoritmo de descifrado:**
   - La función `0x401440` se invoca primero con el argumento `7` y luego (tras pasar la verificación anti-debug) con `11` (totalizando $18$ rondas).
   - En cada ronda, para cada posición $j$ de la cadena intermedia, calcula el número de bits en 1 (*popcount*) de $j \pmod{255}$ mediante una secuencia estándar de máscaras de bits (`0x55`, `0x33`, `0x0F`):
     $$\text{shift} = \text{popcount}(j \pmod{255})$$
     $$c_j \leftarrow 'a' + ((c_j - 'a' + \text{shift}) \pmod{26})$$
   - Posteriormente, en `0x401530`, se realiza un XOR byte a byte entre el Bloque 2 y el Bloque 1 transformado:
     $$\text{flag}[j] = \text{Bloque 2}[j] \oplus \text{Bloque 1}[j]$$
   - El resultado resultante se convierte a UTF-16 con `MultiByteToWideChar` y se imprime como la bandera en pantalla.

### Script de resolución estática (Python)

Dado que se conoce el algoritmo completo tras el desensamblado, no es necesario ejecutar el binario en un entorno Windows ni usar un depurador:

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

# 7 rondas antes del check + 11 rondas después del bypass
transform(part1, 7)
transform(part1, 11)

flag = bytes([a ^ b for a, b in zip(part1, part2)]).decode("latin1")
print(flag)
```

Al ejecutar el script sobre `config.bin`, se obtiene la flag en formato `academy{...}`.

```bash
python3 solve.py
```

## Notas adicionales
En un depurador interactivo de Windows (como `x32dbg`), el método dinámico consiste en colocar un punto de interrupción en la llamada a `IsDebuggerPresent` o en `0x401602`, y modificar el registro `EAX` a `0` (o activar la bandera `ZF = 1`) para forzar el salto hacia la continuación de las rondas de descifrado.

## Referencias
- Reto: https://learn.cylabacademy.org/library/429
- Apoyo: https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-isdebuggerpresent
