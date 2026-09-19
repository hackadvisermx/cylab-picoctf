# General Skills — chrono

## Descripción
> **Prompt oficial del reto:** "How to automate tasks to run at intervals on linux servers? Use ssh to connect to this server." — se entrega acceso SSH (`ssh -p <puerto> picoplayer@saturn.picoctf.net`, contraseña provista). Etiqueta de tema: **"linux"**.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** Mubarak Mikail

## Solución
El propio enunciado apunta directamente al mecanismo de "tareas programadas a intervalos" de Linux: **cron**. Basta con leer el archivo de configuración estándar de cron a nivel de sistema:

```bash
cat /etc/crontab
# picoCTF{Sch3DUL7NG_T45K3_L1NUX_0bb95b71}
```

La flag está puesta directamente como un comentario al inicio de `/etc/crontab`, un archivo de lectura pública (`-rw-r--r--`) en cualquier instalación estándar de Linux — no hace falta ninguna escalada de privilegios ni explotación adicional, solo saber dónde vive la configuración de cron del sistema.

## Notas adicionales
- Reto de calentamiento puro sobre la ubicación estándar de archivos de configuración de Linux (`/etc/crontab`, y por extensión `/etc/cron.d/`, `/etc/cron.{hourly,daily,weekly,monthly}/`, `crontab -l` para tareas de usuario) — sin ningún componente de explotación.
- Se revisó también `/etc/cron.d/` por si la flag viniera de un cron job real que hubiera que abusar (patrón común en retos de escalada de privilegios vía cron con permisos de escritura), pero en esta instancia concreta el archivo con la flag era simplemente `/etc/crontab`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/347
