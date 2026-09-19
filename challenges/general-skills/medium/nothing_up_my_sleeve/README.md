# General Skills — Nothing Up My Sleeve

## Descripción
> **Prompt oficial del reto:** "Let's check that your internet connection is working. This flag is 'in-the-clear', I promise!" — el modal de instancia entrega un enlace directo "Download flag.txt".
>
> **Hints:**
> 1. If all you had access to was a shell, you could use wget to download the file at the URL above!

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2020 Mini-Competition
- **Autor:** Q0h313th

## Solución
Reto trivial de "comprobar la conexión a internet": al lanzar la instancia, el modal ofrece directamente un enlace de descarga `flag.txt` apuntando a `challenge-files.picoctf.net`. La flag está en texto plano dentro del archivo, sin cifrado ni ofuscación:

```bash
curl -s https://challenge-files.picoctf.net/c_shape_facility/.../flag.txt
# picoCTF{c0ngr4ts_0n_y0ur_s4n1ty}
```

## Notas adicionales
- El propio hint confirma la intención: en un entorno restringido a solo terminal (sin navegador), `wget`/`curl` contra la URL del enlace resuelve el reto igual de directo.
- No requiere ninguna técnica: sirve como verificación de que el entorno de trabajo (terminal + acceso a internet saliente) funciona correctamente antes de abordar retos más complejos.

## Referencias
- Reto: https://learn.cylabacademy.org/library/91
