# General Skills — ABSOLUTE NANO

## Descripción
> **Prompt oficial del reto:** "You have complete power with nano. Think you can get the flag?" — se entrega acceso SSH: `ssh -p <puerto> ctf-player@crystal-peak.picoctf.net` con contraseña provista.
>
> **Hints:**
> 1. What can you do with nano?

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Darkraicg492

## Solución
Al conectar por SSH se cae en una shell normal (`ctf-player@challenge:~$`), no directamente en `nano` como sugiere el nombre. `sudo -l` revela el privilegio clave:

```
User ctf-player may run the following commands on challenge:
    (ALL) NOPASSWD: /bin/nano /etc/sudoers
```

`ctf-player` puede ejecutar `nano` como root, sin contraseña, pero solo apuntando a `/etc/sudoers`. Esto es el escape clásico de **GTFOBins para `nano`**: al abrir el editor (con cualquier privilegio, aquí root vía `sudo`), la función "Insertar archivo" (`^R`) puede conmutarse a "Ejecutar un comando" (`^X` dentro de ese mismo prompt) — el comando se ejecuta con los privilegios del propio `nano`, y su salida se inserta en el buffer. Enviando como comando `reset; sh 1>&0 2>&0` se reemplaza la sesión de `nano` por una shell interactiva root usando los mismos descriptores de la terminal.

```bash
sudo /bin/nano /etc/sudoers
# dentro de nano:
^R          # Insertar archivo...
^X          # cambia el prompt a "Ejecutar un comando"
reset; sh 1>&0 2>&0        # <Enter> -> shell root interactiva
```

Ya con shell root:

```bash
id                              # uid=0(root) gid=0(root) groups=0(root)
cat /home/ctf-player/flag.txt   # picoCTF{n4n0_411_7h3_w4y_17bbc630}
```

`flag.txt` en `/home/ctf-player` tenía permisos `-r--r----- root:root`, ilegible para `ctf-player` directamente — el escape a root vía `nano` es indispensable para leerlo.

## Notas adicionales
- **Automatización con `expect`:** como todo esto ocurre dentro de una app de terminal a pantalla completa (`nano`, en modo *alternate screen*), se automatizó con un script `expect` que hace login SSH, envía `export TERM=xterm` (crítico: sin `$TERM` válido, `nano` falla con `Error opening terminal: unknown.` y los `^R`/`^X` se interpretan como atajos de `bash`, p. ej. `^R` dispara `reverse-i-search`), lanza `sudo /bin/nano /etc/sudoers`, y envía la secuencia `^R^X` + el comando `reset; id; cat ... ; echo DONEMARKER`. La salida (incluida la del `id`/`cat`) queda embebida entre los códigos de escape ANSI del redibujado de la terminal, pero sigue siendo legible con `cat -v` o buscando el texto plano en el log.
- Es el mismo patrón documentado en [GTFOBins - nano (Sudo)](https://gtfobins.github.io/gtfobins/nano/#sudo): cualquier binario con capacidad de "insertar salida de un comando" o abrir un shell embebido, si se puede invocar vía `sudo`, se convierte en un vector de escalada de privilegios total sin importar a qué archivo esté restringido en `/etc/sudoers`.
- El nombre del reto es un juego de palabras ("ABSOLUTE NANO" ~ "absolutely nothing" / `NOPASSWD: ALL` de facto vía escape de editor).

## Referencias
- Reto: https://learn.cylabacademy.org/library/748
- Apoyo: [GTFOBins — nano](https://gtfobins.github.io/gtfobins/nano/#sudo)
