# Reverse Engineering — Binary Instrumentation 2

## Descripción
> **Prompt oficial del reto:** "I've been learning more Windows API functions to do my bidding. Hmm... I swear this program was supposed to create a file and write the flag directly to the file. Can you try and intercept the file writing function to see what went wrong?
>
> Download the exe [here](https://challenge-files.cylabacademy.net/library/ce8f745beda824c87d5482c853c90b7758b9a95d9b05db0c74fb2b0678f8115b/bininst2.zip). Unzip the archive with the password `academy`"
>
> **Pistas oficiales:**
> 1. Frida is an easy-to-install, lightweight binary instrumentation toolkit
> 2. Try using the CLI tools like frida-trace
> 3. You can specify the exact function name you want to trace

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** Venax

## Solución
En este reto, el ejecutable empaquetado para Windows (`bininst2.exe`) tiene como propósito escribir la bandera directamente en un archivo en disco mediante las APIs estándar de Win32 (`CreateFileA` y `WriteFile`). Sin embargo, el programa falla silenciosamente debido a dos problemas intencionales:
1. `CreateFileA` recibe una ruta/nombre de archivo no válido.
2. Al invocar `WriteFile`, el parámetro `nNumberOfBytesToWrite` se pasa como `0`.

A pesar de que no se escriben bytes físicamente en el disco, el buffer en memoria (`lpBuffer`) contiene los datos de la bandera listos para ser persistidos.

### Instrumentación Dinámica con Frida

Utilizando `frida-trace`, se interceptan las funciones de archivo en `KERNEL32.DLL`:

```bash
frida-trace -i CreateFileA -i WriteFile -f bininst2.exe -X KERNEL32
```

Frida genera las plantillas JavaScript de inspección en `__handlers__/KERNEL32.DLL/`.

#### 1. Modificación de `CreateFileA.js`
Se asegura de que el descriptor de archivo (`hFile`) devuelto sea válido redirigiendo el primer argumento (`lpFileName`) a una ruta válida:

```javascript
defineHandler({
  onEnter(log, args, state) {
    log('Interceptando CreateFileA()');
    this.validPath = Memory.allocUtf8String('output.txt');
    args[0] = this.validPath;
  },
  onLeave(log, retval, state) {}
});
```

#### 2. Modificación de `WriteFile.js`
En el prototipo de `BOOL WriteFile(HANDLE hFile, LPCVOID lpBuffer, DWORD nNumberOfBytesToWrite, LPDWORD lpNumberOfBytesWritten, LPOVERLAPPED lpOverlapped)`:
- `args[1]` es el puntero `lpBuffer`.
- Mediante un volcado de memoria (`hexdump`) o leyendo como cadena de texto, se extrae la información contenida en el buffer:

```javascript
defineHandler({
  onEnter(log, args, state) {
    log('Interceptando WriteFile()');
    var buffer = args[1];
    log(hexdump(buffer, { length: 80, ansi: true }));
  },
  onLeave(log, retval, state) {}
});
```

Al relanzar la traza:

```bash
frida-trace -i CreateFileA -i WriteFile -f bininst2.exe -X KERNEL32
```

Frida intercepta la llamada e imprime en consola el volcado del buffer, el cual contiene la cadena codificada en Base64:

```text
Y2FkZW15e2ZyMWRhX2Ywcl9iMW5faW41dHJ1bTNudDR0aW9uIV9iMjFhZWYzOX0=
```

Decodificando la cadena con `base64`:

```bash
echo "Y2FkZW15e2ZyMWRhX2Ywcl9iMW5faW41dHJ1bTNudDR0aW9uIV9iMjFhZWYzOX0=" | base64 -d
```

Se recupera la bandera completa con formato `academy{...}`.

## Notas adicionales
La instrumentación dinámica permite inspeccionar directamente la memoria de los argumentos de funciones nativas antes de que una validación o parámetro erróneo anule la operación, obviando la necesidad de desempacar el ejecutable o recrear la lógica criptográfica de descifrado.

## Referencias
- Reto: https://learn.cylabacademy.org/library/452
- Apoyo: https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile
