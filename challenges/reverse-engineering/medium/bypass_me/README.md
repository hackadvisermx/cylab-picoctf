# Reverse Engineering — Bypass Me

## Descripción
> **Prompt oficial del reto:** "Your task is to analyze and exploit a password-protected binary called **bypassme.bin** and binary performs input sanitization.
>
> However, instead of guessing the password, you are expected to reverse engineer or debug the program to bypass the authentication logic and retrieve the hidden flag.
>
> You'll need to think like an attacker using tool like [LLDB](https://lldb.llvm.org/use/tutorial.html) to uncover how the binary works under the hood and leak the correct password."
>
> **Pistas oficiales:**
> 1. Try disassembling the binary to understand its inner workings.
> 2. Pay special attention to functions available
> 3. The password might be hidden or decoded at runtime

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Prince Niyonshuti N.

## Solución
El reto proporciona acceso remoto vía SSH a una máquina donde reside el binario `bypassme.bin` con privilegios SUID root. Se descarga una copia local vía `scp` para su análisis estático y dinámico:

```bash
scp -P <puerto> ctf-player@<host>:bypassme.bin ./bypassme.bin
```

### 1. Análisis estático del binario
Inspeccionando los símbolos de `bypassme.bin` con `objdump -t`, se identifican funciones clave sin ofuscar:
- `decode_password(char*)` (`_Z15decode_passwordPc`)
- `sanitize(char const*, char*)` (`_Z8sanitizePKcPc`)
- `auth_sequence()` (`_Z13auth_sequencev`)
- `intro_sequence()` (`_Z14intro_sequencev`)

### 2. Desensamblado de `decode_password`
Al revisar `decode_password`:
```assembly
movabs rax, -0x3630062730252007   ; 0xc9cff9d8cfdadff9
mov    qword ptr [rbp - 0x13], rax
mov    dword ptr [rbp - 0xc], 0xcfd8dfc9
...
loop:
movzx  eax, byte ptr [rbp + rax - 0x13]
xor    eax, 0xaa                   ; xor con 0xaa (-0x56)
...
cmp    rax, 0xa
jbe    loop
```

En memoria se cargan 11 bytes secuenciales:
- `0xf9, 0xdf, 0xda, 0xcf, 0xd8, 0xf9, 0xcf, 0xc9, 0xdf, 0xd8, 0xcf`

Aplicando XOR con `0xaa` a cada uno:
```python
raw = [0xf9, 0xdf, 0xda, 0xcf, 0xd8, 0xf9, 0xcf, 0xc9, 0xdf, 0xd8, 0xcf]
password = bytes([b ^ 0xaa for b in raw])
print(password)  # b'SuperSecure'
```

### 3. Verificación en `main`
En `main`:
1. El programa llama a `decode_password` al inicio para colocar la contraseña esperada (`SuperSecure`) en el búfer local `[rbp - 0x110]`.
2. Lee la entrada del usuario en `[rbp - 0x210]`.
3. Ejecuta `sanitize` (que preserva únicamente caracteres alfabéticos vía `isalpha`).
4. Compara la entrada cruda del usuario directamente contra la contraseña decodificada usando `strcmp`:
   ```assembly
   lea rdx, [rbp - 0x110]  ; Contraseña esperada ("SuperSecure")
   lea rax, [rbp - 0x210]  ; Entrada del usuario
   mov rsi, rdx
   mov rdi, rax
   call strcmp
   ```
5. Si coinciden (`strcmp == 0`), invoca `auth_sequence` y lee `flag.txt`.

### 4. Ejecución y obtención de la flag
Conectándose por SSH y enviando la contraseña descubierta `SuperSecure`:

```bash
echo "SuperSecure" | ./bypassme.bin
```

Salida:
```text
[3 tries left] Enter password: 
Raw Input:      [SuperSecure]
Sanitized Input:[SuperSecure]
Hint: Input must match something special...

Authenticating...
🎉 Flag: academy{...}
```

## Notas adicionales
- Aunque el reto sugiere utilizar un depurador interactivo (como GDB o LLDB) en tiempo de ejecución para interceptar la cadena en `strcmp`, el análisis estático de las constantes en `decode_password` permite obtener la contraseña directamente sin necesidad de gdb remoto.

## Referencias
- Reto: https://learn.cylabacademy.org/library/761
- LLDB Tutorial: https://lldb.llvm.org/use/tutorial.html
