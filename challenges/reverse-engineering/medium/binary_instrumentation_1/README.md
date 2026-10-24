# Reverse Engineering — Binary Instrumentation 1

## Descripción
> **Prompt oficial del reto:** "I have been learning to use the Windows API to do cool stuff! Can you wake up my program to get the flag?
>
> Download the exe [here](https://challenge-files.cylabacademy.net/library/b707862077450010bce3c050b139b7c00762859eb94eea5db8eded717a6318d0/bininst1.zip). Unzip the archive with the password `academy`"
>
> **Pistas oficiales:**
> 1. Frida is an easy-to-install, lightweight binary instrumentation toolkit
> 2. Try using the CLI tools like frida-trace to auto-generate handlers

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** Venax

## Solución
El reto proporciona un ejecutable para Windows de 64 bits (`bininst1.exe`) empaquetado. Al ejecutarse directamente, el programa muestra un mensaje en consola indicando que entrará en reposo indefinido (`zzzzzz....`) mediante una llamada bloqueante a la API de Windows `Sleep()`, impidiendo que el flujo continúe hacia la impresión de la bandera.

### Instrumentación Dinámica con Frida

Para resolver el reto sin esperar la finalización del retardo, se utiliza Frida (`frida-trace`) para interceptar dinámicamente la llamada a la función `Sleep` en tiempo de ejecución y forzar que el tiempo de espera sea 0 milisegundos.

1. **Generación automática del handler:**
   ```bash
   frida-trace -i Sleep -f bininst1.exe
   ```

2. **Modificación del handler de `Sleep`:**
   En el archivo generado en `__handlers__/KERNEL32.DLL/Sleep.js` (o `KERNELBASE.dll/Sleep.js`), se sobreescribe el primer argumento (`args[0]`, que corresponde a los milisegundos de espera en el prototipo `void Sleep(DWORD dwMilliseconds)`):

   ```javascript
   defineHandler({
     onEnter(log, args, state) {
       log('Interceptando Sleep(). Reduciendo retardo a 0ms');
       args[0] = ptr(0);
     },
     onLeave(log, retval, state) {
     }
   });
   ```

3. **Alternativa con script autónomo de Frida (`hook.js`):**
   ```javascript
   var sleepPtr = Module.findExportByName("kernel32.dll", "Sleep");
   if (sleepPtr) {
       Interceptor.replace(sleepPtr, new NativeCallback(function(ms) {
           console.log("[*] Sleep llamada con", ms, "ms -> Anulada.");
       }, "void", ["uint32"]));
   }
   ```

   Ejecución del script con Frida:
   ```bash
   frida -f bininst1.exe -l hook.js
   ```

Al anular el retardo, el ejecutable prosigue inmediatamente con la rutina final, imprimiendo una cadena codificada en Base64 en la consola estándar:

```text
Y2FkZW15e3c0a2VfbTNfdXBfdzF0aF9mcjFkYV9mMjdhY2MzOH0=
```

Decodificando la salida Base64:

```bash
echo "Y2FkZW15e3c0a2VfbTNfdXBfdzF0aF9mcjFkYV9mMjdhY2MzOH0=" | base64 -d
```

Se obtiene la bandera completa en formato `academy{...}`.

## Notas adicionales
El ejecutable utiliza compresión/empaquetado PE para dificultar el análisis estático ingenuo de cadenas, lo que hace que la instrumentación binaria dinámica (DBI) mediante Frida sea el camino más limpio y directo para resolverlo.

## Referencias
- Reto: https://learn.cylabacademy.org/library/451
- Apoyo: https://frida.re/docs/frida-trace/
