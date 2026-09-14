# General Skills — Piece by Piece

## Descripción
> **Prompt oficial:** "After logging in, you will find multiple file parts in your home directory. These parts need to be combined and extracted to reveal the flag. SSH to `<host>:<puerto>` and login as `ctf-player` with password `<pass>`."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
En el home del usuario `ctf-player` hay `instructions.txt` y varios `part_a*` (salida típica de `split`). Las instrucciones dicen que, juntando las partes, se reconstruye un `.zip` protegido con la contraseña `supersecret`.

```bash
scp -P <puerto> "ctf-player@<host>:part_a*" .
cat part_a* > combined.zip
unzip -P supersecret combined.zip -d out
cat out/*.txt
```

Flag: `picoCTF{z1p_and_spl1t_f1l3s_4r3_fun_8fa833a5}`

## Notas adicionales
- Equivalente a lo que produciría `split -b <n> flag.zip part_`; para reconstruir basta con `cat` en el orden alfabético correcto (`part_aa`, `part_ab`, ...), que es justo el orden que produce `split` por defecto.
- Se resolvió con `scp`/`ssh` directos desde la terminal local (usando `expect` para automatizar la contraseña) en vez del webshell embebido de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/740
