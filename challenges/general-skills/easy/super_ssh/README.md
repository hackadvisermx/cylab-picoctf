# General Skills — Super SSH

## Descripción
> **Prompt oficial:** "Using a Secure Shell (SSH) is going to be pretty important. Can you ssh as ctf-player to `<host>` at port `<puerto>` to get the flag? You'll also need the password `<pass>`."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Jeffery John

## Solución
Reto introductorio de SSH: solo hay que conectarse; el propio mensaje de bienvenida (`motd`/banner) de la sesión ya contiene la flag.

```bash
ssh -p <puerto> ctf-player@<host>
# (contraseña)
# Welcome ctf-player, here's your flag: picoCTF{...}
```

Flag: `picoCTF{s3cur3_c0nn3ct10n_8969f7d3}`

## Notas adicionales
- Ojo al transcribir la contraseña desde la página: el texto renderizado puede recortar visualmente algún carácter en una captura o zoom parcial (aquí, la contraseña real era `83dcefb7`, no `83cefb7` como pareció en un primer vistazo) — conviene extraer el texto exacto con `get_page_text`/DOM en vez de leerlo de una imagen cuando el primer intento de login falla con "Permission denied".

## Referencias
- Reto: https://learn.cylabacademy.org/library/424
