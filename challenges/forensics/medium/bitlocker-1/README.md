# Forensics — Bitlocker-1

## Descripción
> **Prompt oficial del reto:** "Jacky is not very knowledgable about the best security passwords and used a simple password to encrypt their BitLocker drive. See if you can break through the encryption!  
> Download the disk image here"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** Venax

> **Pistas oficiales:**
> 1. Hash cracking

## Solución
El reto proporciona una imagen de disco con cifrado de volumen BitLocker (`bitlocker-1.dd`).

1. **Extracción del hash de BitLocker:**
   Utilizamos la herramienta `bitlocker2john` para inspeccionar los bloques de metadatos FVE (*Full Volume Encryption*) y extraer el material criptográfico necesario para el ataque:
   ```bash
   python3 bitlocker2john.py bitlocker-1.dd > bitlocker.hash
   ```
   El script detecta la firma `-FVE-FS-` y localiza el encabezado del bloque FVE con el VMK protegido por contraseña (`Protection type: 0x2000`). Se obtiene un hash en formato John:
   ```text
   $bitlocker$0$16$cb4809fe9628471a411f8380e0f668db$1048576$12$...
   ```

2. **Ataque de diccionario:**
   Dado que Jacky utilizó una contraseña débil según el enunciado, lanzamos un ataque de diccionario utilizando `john` o `hashcat` (modo 22100) contra la lista `rockyou.txt`:
   ```bash
   john --format=BitLocker --wordlist=rockyou.txt bitlocker.hash
   ```
   El proceso de descifrado revela la contraseña en texto plano utilizada por el usuario: `jacqueline`.

3. **Descifrado y montaje del volumen:**
   Con la contraseña recuperada, se descifra el volumen utilizando `dislocker` y se monta el archivo virtual resultante:
   ```bash
   sudo dislocker -v -V bitlocker-1.dd -u"jacqueline" -- /mnt/dislocker
   sudo mount -o loop,ro /mnt/dislocker/dislocker-file /mnt/decrypted
   cat /mnt/decrypted/flag.txt
   ```
   La lectura de `flag.txt` proporciona la bandera de la academia.

## Notas adicionales
- BitLocker utiliza PBKDF2 con 1,048,576 iteraciones de SHA-256 para derivar la clave intermedia a partir de la contraseña del usuario, lo que ralentiza significativamente los intentos de ataque por fuerza bruta; sin embargo, contraseñas basadas en nombres o palabras del diccionario siguen siendo vulnerables.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/453
- Dislocker: https://github.com/Aorimn/dislocker
- John the Ripper (BitLocker module): https://www.openwall.com/john/
