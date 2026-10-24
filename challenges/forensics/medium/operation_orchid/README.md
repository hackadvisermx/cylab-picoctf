# Forensics — Operation Orchid

## Descripción
> **Prompt oficial del reto:** "Download this disk image and find the flag.  
>  
> Note: if you are using the webshell, download and extract the disk image into `/tmp` not your home directory.  
> Download compressed disk image"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto presenta una imagen de disco Linux comprimida (`disk.flag.img.gz`).

1. **Extracción del sistema de archivos ext4:**
   ```bash
   gzip -dc disk.flag.img.gz > disk.flag.img
   7zz e disk.flag.img 2.img -o./
   ```

2. **Inspección del directorio /root:**
   Al listar el directorio `/root/`:
   ```bash
   7zz l 2.img | grep "root/"
   ```
   Se detectan dos archivos de alto interés:
   - `root/.ash_history`
   - `root/flag.txt.enc`

3. **Análisis del historial de comandos (.ash_history):**
   ```bash
   7zz e 2.img root/.ash_history -o./
   cat .ash_history
   ```
   El historial de la terminal del usuario root contiene la secuencia de comandos ejecutada:
   ```bash
   nano flag.txt 
   openssl aes256 -salt -in flag.txt -out flag.txt.enc -k unbreakablepassword1234567
   shred -u flag.txt
   ```

4. **Descifrado con OpenSSL:**
   Extraemos `flag.txt.enc` y revertimos el cifrado AES-256 utilizando la contraseña `unbreakablepassword1234567`:
   ```bash
   7zz e 2.img root/flag.txt.enc -o./
   openssl enc -aes-256-cbc -d -salt -in flag.txt.enc -k unbreakablepassword1234567 -md sha256
   ```
   El descifrado produce la bandera en texto claro.

## Notas adicionales
- En distribuciones Alpine Linux modernas, OpenSSL utiliza SHA-256 por defecto para derivar la clave criptográfica mediante `EVP_BytesToKey`.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/285
- OpenSSL enc command: https://www.openssl.org/docs/manmaster/man1/openssl-enc.html
