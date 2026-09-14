# General Skills — MY GIT

## Descripción
> **Prompt oficial:** "I have built my own Git server with my own rules! You can clone the challenge repo using the command below: `git clone ssh://git@<host>:<puerto>/git/challenge.git`. Here's the password: `<pass>`. Check the README to get your flag!"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Darkraicg492

## Solución
El `README.md` del repo clonado dice literalmente:

```
### If you want the flag, make sure to push the flag!
Only flag.txt pushed by ```root:root@picoctf``` will be updated with the flag.
```

El servidor Git remoto valida, al recibir un push, si el **autor del commit** coincide exactamente con `root <root@picoctf>` y si el commit añade un archivo `flag.txt`. Si ambas condiciones se cumplen, el propio hook del servidor devuelve la flag en la salida de `git push` (mensajes `remote: ...`).

```bash
git clone ssh://git@<host>:<puerto>/git/challenge.git
cd challenge
git config user.name root
git config user.email root@picoctf
echo hello > flag.txt
git add flag.txt
git commit -m "flag"
git push
# remote: Author matched and flag.txt found in commit...
# remote: Congratulations! You have successfully impersonated the root user
# remote: Here's your flag: picoCTF{...}
```

## Notas adicionales
- No hace falta ningún contenido específico dentro de `flag.txt` — el hook del servidor solo comprueba el **autor del commit** y el **nombre del archivo**, no su contenido.
- Es un ejemplo sencillo de por qué la identidad de autor de Git (`user.name`/`user.email`) es información que el propio cliente controla libremente y no debe usarse como mecanismo de autenticación/autorización en un servidor.

## Referencias
- Reto: https://learn.cylabacademy.org/library/764
