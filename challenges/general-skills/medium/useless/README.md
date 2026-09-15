# General Skills — useless

## Descripción
> **Prompt oficial del reto:** "There's an interesting script in the user's home directory. The work computer is running SSH. We've been given a script which performs some basic calculations, explore the script and find a flag." Se entrega acceso SSH: `saturn.picoctf.net:<puerto>`, usuario `picoplayer`, contraseña `password`. El reto trae la etiqueta de tema **"man"**.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** Loic Shema

## Solución
En el home de `picoplayer` hay un script `useless` (bash, no *setuid*, sin relación con root) que hace operaciones aritméticas básicas (`add`/`sub`/`mul`/`div`) sobre dos argumentos. A primera vista invita a buscar una inyección vía `$(( ))` (evaluación aritmética de bash es capaz de ejecutar `$(comando)` embebido) o algún camino de escalada de privilegios — pero en esta instancia no hay `sudo` instalado, ningún binario *setuid* propio, ni cron que ejecute el script como root, así que esa vía no lleva a ningún lado.

La pista real es la propia etiqueta del reto: **"man"**. El comando tiene una página de manual instalada en el sistema:

```bash
find / -xdev -name 'useless*' 2>/dev/null
# /home/picoplayer/useless
# /usr/local/share/man/man1/useless.1.gz

man useless
# (o, si MANPATH no está configurado)
zcat /usr/local/share/man/man1/useless.1.gz
```

La página de manual (formato *mdoc*) documenta el uso normal del script (`add`, `sub`, `mul`, `div` con ejemplos) y termina con una sección `Authors` que incluye la flag en texto plano:

```
.Sh Authors
This script was designed and developed by Cylab Africa

picoCTF{us3l3ss_ch4ll3ng3_3xpl0it3d_8504}
```

## Notas adicionales
- Lección principal: cuando un reto entrega o menciona un comando/script, **no asumir que la única superficie de ataque es el propio archivo ejecutable** — revisar también su documentación instalada (`man <comando>`, `--help`, `info`, archivos `.1`/`.5` en `/usr/share/man` o `/usr/local/share/man`) puede revelar directamente la flag o pistas adicionales.
- Se exploraron activamente varias vías de escalada de privilegios (setuid, `sudo -l`, cron, procesos root, capabilities) antes de encontrar la página de manual — todas resultaron ser callejones sin salida en esta instancia, reforzando que el nombre "useless" describe tanto al script (una calculadora trivial) como a esas pistas falsas de privesc.
- El nombre de la flag (`us3l3ss_ch4ll3ng3_3xpl0it3d`) sugiere que el reto SÍ contempla, en otras variantes/versiones, la inyección aritmética de bash como vector — pero en esta instancia concreta la vía más corta a la flag fue simplemente `man useless`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/384
