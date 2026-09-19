# General Skills — YaraRules0x100

## Descripción
> **Prompt oficial del reto:** "Dear Threat Intelligence Analyst, quick heads up - we stumbled upon a shady executable on one of our employee's Windows PCs... Seems like this file sneaked past our Intrusion Detection Systems, indicating a fresh threat with no matching signatures in our database. Can you dive into this file and whip up some YARA rules?" Se entrega un `.zip` (contraseña `picoctf`) con un ejecutable `suspicious.exe`, y un servicio `socat -t60 - TCP:standard-pizzas.picoctf.net:62542 < regla.yar` que valida la regla contra "varios casos de prueba" (versión empaquetada, desempaquetada, variantes ligeramente modificadas).

> **Hints:**
> 1. The test cases will attempt to match your rule with various variations of this suspicious file, including a packed version, an unpacked version, slight modifications to the file while retaining functionality, etc.
> 2. Since this is a Windows executable file, some strings within this binary can be "wide" strings. Try declaring your string variables something like $str = "Some Text" wide ascii wherever necessary.
> 3. Your rule should also not generate any false positives (or false negatives). Refine your rule to perfection! One YARA rule file can have multiple rules! Maybe define one rule for Packed binary and another rule for Unpacked binary in the same rule file?

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** Nandan Desai / syreal

## Solución

1. Se descarga y descomprime el archivo:
   ```bash
   curl -sL -o suspicious.zip "<url del reto>"
   unzip -P picoctf suspicious.zip -d extracted
   ```
   `suspicious.exe` resulta ser un PE32 comprimido con **UPX**.

2. Se desempaqueta una copia para poder analizar el comportamiento real:
   ```bash
   upx -d suspicious.exe -o suspicious_unpacked.exe
   ```

3. Extrayendo cadenas ASCII/UTF-16 del binario desempaquetado aparecen mensajes de depuración muy reveladores (el propio autor deja pistas dentro del binario):
   - *"To develop an effective YARA rule, find any suspicious Win32 API functions that are being used by this program."*
   - *"Developing rules solely based on strings (...) is not a good idea, as it can lead to false positives."*
   - *"Your rules should work even if this binary is packed (or unpacked)."*

   Combinado con la lista de imports (`pefile`), el binario desempaquetado muestra una combinación de APIs muy característica de una técnica **anti-debug "self-debugging"**: obtiene `SeDebugPrivilege` (`LookupPrivilegeValueW` + `AdjustTokenPrivileges`), enumera procesos (`CreateToolhelp32Snapshot` + `Process32NextW`), comprueba/depura su propio proceso (`IsDebuggerPresent`, `DebugActiveProcess`, `DebugActiveProcessStop`), y crea un mutex de instancia única (`CreateMutexW`).

4. Comparando el import table del `.exe` empaquetado contra el desempaquetado (con `pefile`), se confirma que **UPX solo deja visibles `LoadLibraryA`/`GetProcAddress`/`ExitProcess`/`VirtualProtect`** — todos los imports "interesantes" se resuelven en tiempo de ejecución y no existen como texto plano en el binario empaquetado. Por eso la regla debe tener dos caminos:
   - Si el import table trae los símbolos anti-debug/anti-análisis mencionados → sospechoso (caso desempaquetado).
   - Si el binario está empaquetado con UPX (secciones `UPX0`/`UPX1`) → también se marca, ya que las variantes empaquetadas del mismo malware deben poder detectarse igual.

5. Regla final (usa el módulo `pe` de YARA en vez de simples strings de mensajes, según la pista del propio binario):

```yara
import "pe"

rule YaraRules0x100_Suspicious
{
    meta:
        author = "solver"
        description = "Detects self-debugging anti-analysis malware sample (packed or unpacked)"

    condition:
        uint16(0) == 0x5A4D and
        (
            (
                pe.imports("KERNEL32.DLL", "DebugActiveProcess") and
                pe.imports("KERNEL32.DLL", "DebugActiveProcessStop") and
                pe.imports("KERNEL32.DLL", "IsDebuggerPresent") and
                pe.imports("KERNEL32.DLL", "CreateToolhelp32Snapshot") and
                pe.imports("KERNEL32.DLL", "Process32NextW") and
                pe.imports("KERNEL32.DLL", "CreateMutexW") and
                pe.imports("ADVAPI32.dll", "AdjustTokenPrivileges") and
                pe.imports("ADVAPI32.dll", "LookupPrivilegeValueW")
            )
            or
            (
                pe.section_index("UPX0") >= 0 and
                pe.section_index("UPX1") >= 0
            )
        )
}
```

   Ver [rule.yar](rule.yar).

6. Se prueba localmente con la CLI de `yara` contra ambas variantes antes de enviarla:
   ```bash
   yara -w rule.yar suspicious_unpacked.exe   # match
   yara -w rule.yar suspicious_packed.exe     # match
   ```

7. Se envía al servicio validador tal como indica el enunciado:
   ```bash
   socat -t60 - TCP:standard-pizzas.picoctf.net:62542 < rule.yar
   # Status: Passed
   # Congrats! Here is your flag: picoCTF{yara_rul35_r0ckzzz_aa7b0fbf}
   ```

## Notas adicionales
- Herramientas usadas: `unzip`, `upx` (Homebrew), `yara`/`libyara` (Homebrew) para compilar y probar la regla localmente, `pefile` (Python) para inspeccionar tablas de importación y secciones antes de escribir la regla, `socat` para el envío final.
- El propio ejecutable, aunque simula ser malware, imprime literalmente *"This is a fake malware. It means no harm."* — es un binario didáctico construido para enseñar detección basada en comportamiento (imports) en vez de en cadenas de texto triviales, que son las primeras en desaparecer al empaquetar con UPX.

## Referencias
- Reto: https://learn.cylabacademy.org/library/483
