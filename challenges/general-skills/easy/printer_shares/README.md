# General Skills — Printer Shares

## Descripción
> **Prompt oficial:** "Oops! Someone accidentally sent an important file to a network printer—can you retrieve it from the print server? The printer is on `<puerto>`. You can try `$ nc -vz <host> <puerto>`"
>
> **Hints:**
> 1. knowing how SMB protocol works would be helpful!
> 2. smbclient and smbutil are good tools

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Janice He

## Solución
El puerto indicado no es un puerto de impresión raw (9100/JetDirect); es en realidad un servicio **SMB** (Samba) expuesto en un puerto no estándar. Con `smbclient` se puede listar los recursos compartidos y descargar el archivo.

```bash
# Listar shares (autenticación anónima, -N)
smbclient -L //<host> -p <puerto> -N

# Sharename       Type      Comment
# ---------       ----      -------
# shares          Disk      Public Share With Guests
# IPC$            IPC       IPC Service

# Listar contenido del share "shares"
smbclient //<host>/shares -p <puerto> -N -c 'recurse ON; ls'
# dummy.txt
# flag.txt

# Descargar y leer la flag
smbclient //<host>/shares -p <puerto> -N -c 'get flag.txt /tmp/flag.txt' && cat /tmp/flag.txt
```

Flag: `picoCTF{5mb_pr1nter_5h4re5_b3f2f855}`

## Notas adicionales
- El share permite acceso anónimo (`-N`, sin usuario/contraseña) y "Guests", como indica el propio comentario del share (`Public Share With Guests`).
- `smbclient` acepta `-c '<comando1>; <comando2>'` para ejecutar una secuencia de comandos sin entrar al modo interactivo, útil para automatizar en un solo `curl`-style one-liner.
- Este reto usa `smbclient`, disponible en el webshell de CyLab Academy pero no en macOS de forma nativa (macOS trae `smbutil`, más limitado); se usó el webshell de la plataforma para esta parte en vez de la terminal local.

## Referencias
- Reto: https://learn.cylabacademy.org/library/759
