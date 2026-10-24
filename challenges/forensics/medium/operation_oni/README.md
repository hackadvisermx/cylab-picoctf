# Forensics — Operation Oni

## Descripción
> **Prompt oficial del reto:** "Download this disk image, find the key and log into the remote machine.  
>  
> Note: if you are using the webshell, download and extract the disk image into `/tmp` not your home directory.  
> Download disk image"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto requiere extraer una clave privada SSH desde una imagen de disco (`disk.img.gz`) y autenticarse en una máquina remota.

1. **Extracción de la imagen:**
   ```bash
   gzip -dc disk.img.gz > disk.img
   7zz l disk.img
   ```
   Se encuentran dos particiones MBR: `0.img` (100 MB) y `1.img` (129 MB, sistema raíz ext4).

2. **Localización de la clave privada SSH:**
   Extraemos la partición `1.img` y buscamos archivos dentro del directorio `.ssh`:
   ```bash
   7zz e disk.img 1.img -o./
   7zz l 1.img | grep -i "\.ssh"
   ```
   Se identifican:
   - `root/.ssh/id_ed25519`
   - `root/.ssh/id_ed25519.pub`

3. **Extracción y conexión SSH remota:**
   Extraemos la clave privada y le asignamos permisos restringidos (`600`):
   ```bash
   7zz e 1.img root/.ssh/id_ed25519 -o./
   chmod 600 id_ed25519
   ssh -i id_ed25519 -p <PORT> ctf-player@<HOST> "cat flag.txt"
   ```
   La ejecución del comando devuelve la bandera almacenada en el servidor.

## Notas adicionales
- Los clientes OpenSSH requieren de forma obligatoria que las claves privadas tengan permisos de lectura exclusivos para el propietario (`chmod 600`), de lo contrario rechazan la clave por motivos de seguridad (*Permissions are too open*).
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/284
- OpenSSH Client Configuration: https://www.openssh.com
