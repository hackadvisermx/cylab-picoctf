# Reverse Engineering — WinAntiDbg0x300

## Descripción
> **Prompt oficial del reto:** "This challenge is a little bit invasive. It will try to fight your debugger. With that in mind, debug the binary and get the flag!
>
> This challenge executable is a GUI application and it requires admin privileges. And remember, the flag might get corrupted if you mess up the process's state.
>
> Challenge can be downloaded [here](https://challenge-files.cylabacademy.net/library/345bdce65d0479346abcc4d63ddc161b2ca4964d88abde47228c9b5d77917004/WinAntiDbg0x300.zip). Unzip the archive with the password `academy`
>
> If you get "VCRUNTIME140D.dll" and "ucrtbased.dll" missing error, then that means the Universal C Runtime library and Visual C++ Debug library are not installed on your Windows machine.
>
> The quickest way to fix this is:
> - Download Visual Studio Community installer from https://visualstudio.microsoft.com/vs/community/
> - After the installer starts, first select 'Desktop development with C++' and then, in the right side column, select 'MSVC v143 - VS 2022 C++ x64/x86 build tools' and 'Windows 11 SDK' packages.
>
> This will take ~30 mins to install any missing DLLs."
>
> **Pistas oficiales:**
> 1. There is an infinite loop to constantly check for the debugger.
> 2. Get past that infinite loop. Maybe 'Patch' the binary to jump to the appropriate location?
> 3. If you've done everything correctly, the flag should pop-up on your screen after 5 seconds of launching the program. The flag will also be printed to the Debug output to make it easy for you to copy the flag to the clipboard. See 'DebugView' program in Sysinternals Suite.

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** Nandan Desai

## Solución
`WinAntiDbg0x300` es el reto final de la serie de anti-debugging de Windows en picoCTF 2024. A diferencia de los retos anteriores, este programa es una aplicación gráfica (GUI) compilada en modo depuración (incluyendo archivo `.pdb`) que implementa un hilo con un bucle infinito de detección activa de depuradores.

### Análisis del binario

1. **Estructura del archivo `config.bin`:**
   Contiene:
   - Entero little-endian de 4 bytes indicando la longitud de la cadena ($40$ bytes).
   - Bloque 1 ($40$ bytes): cadena base en texto claro (`wvqkabneuexnurysashbmfuwekasrnpruazjevth`).
   - Byte nulo separador.
   - Bloque 2 ($40$ bytes): vector de bytes cifrados mediante XOR.

2. **Mecanismo de protección y bucle anti-debug:**
   - La aplicación inicia un temporizador de 5 segundos y un hilo secundario que ejecuta continuamente verificaciones de depuración (`CheckRemoteDebuggerPresent`, `NtQueryInformationProcess`, etc.).
   - La pista oficial menciona parchear el binario para evitar caer en el bucle infinito y permitir que se ejecute la rutina de descifrado.

3. **Cálculo de la transformación y rondas válidas:**
   El algoritmo de descifrado aplica la misma transformación de rotación dependiente de los bits activos del índice:
   $$\text{shift} = \text{popcount}(j \pmod{255})$$
   $$c_j \leftarrow 'a' + ((c_j - 'a' + \text{shift}) \pmod{26})$$
   $$\text{flag}[j] = \text{Bloque 2}[j] \oplus \text{Bloque 1}[j]$$

   Analizando el flujo de rondas necesarias para alcanzar el estado descifrado, un total acumulado de $12$ rondas genera la bandera válida con el prefijo canónico `academy{...}`.

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

# 12 rondas de transformación en la ruta exitosa
transform(part1, 12)

flag = bytes([a ^ b for a, b in zip(part1, part2)]).decode("latin1")
print(flag)
```

Al ejecutar el script sobre `config.bin`:

```bash
python3 solve.py
```

Se obtiene la flag completa con formato `academy{...}`.

## Notas adicionales
En un entorno con herramientas de depuración dinámicas en Windows (como x64dbg o IDA Pro con Sysinternals DebugView), la bandera se escribe en la salida de depuración mediante `OutputDebugStringW` tras superar las rutinas de protección.

## Referencias
- Reto: https://learn.cylabacademy.org/library/431
- Apoyo: https://learn.microsoft.com/en-us/sysinternals/downloads/debugview
