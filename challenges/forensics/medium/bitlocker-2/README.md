# Forensics — Bitlocker-2

## Descripción
> **Prompt oficial del reto:** "Jacky has learnt about the importance of strong passwords and made sure to encrypt the BitLocker drive with a very long and complex password. We managed to capture the RAM while this drive was opened however. See if you can break through the encryption!  
> Download the disk image here and the RAM dump here"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** Venax

> **Pistas oficiales:**
> 1. Try using a volatility plugin

## Solución
A diferencia de la primera parte, en este escenario la contraseña empleada es excesivamente compleja para ataques de diccionario convencionales. Sin embargo, se dispone de un volcado de memoria física (`memdump.mem.gz`) capturado mientras el volumen BitLocker se encontraba montado y desbloqueado en el sistema operativo.

1. **Descompresión del volcado de RAM:**
   ```bash
   gzip -dc memdump.mem.gz > memdump.mem
   ```

2. **Análisis de memoria forense:**
   Cuando un volumen BitLocker está activo en Windows, tanto la clave maestra del volumen (FVEK) como los buffers de los archivos abiertos residen en la memoria RAM del sistema.
   Podemos extraer los artefactos directamente analizando las cadenas de memoria o utilizando el plugin `bitlocker` de Volatility 3:
   ```bash
   strings -a memdump.mem | grep "academy{"
   ```
   Debido a que el archivo de la bandera se encontraba abierto o en la memoria caché del explorador en el momento de la captura del volcado, la bandera aparece en texto plano en la memoria física capturada.

3. **Recuperación mediante clave FVEK (Alternativa Volatility):**
   ```bash
   vol -f memdump.mem windows.bitlocker
   ```
   Volatility identifica los objetos de volumen y recupera la clave FVEK (Full Volume Encryption Key), permitiendo montar la imagen de disco `bitlocker-2.dd` con `dislocker -K <FVEK>`.

## Notas adicionales
- El cifrado de disco completo protege los datos en reposo mientras el dispositivo está apagado; una vez encendido y desbloqueado el volumen, las claves criptográficas y los datos leídos residen en la memoria volátil, susceptibles a ataques de *live memory forensics* o *cold boot*.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/454
- Volatility 3 Framework: https://github.com/volatilityfoundation/volatility3
