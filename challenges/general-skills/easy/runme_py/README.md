# General Skills — runme.py

## Descripción
> **Prompt oficial:** "Run the `runme.py` script to get the flag. Download the script with your browser or with `wget` in the webshell."
>
> **Hints:**
> 1. If you have Python on your computer, you can download the script normally and run it. Otherwise, use the `wget` command in the webshell.
> 2. To use `wget` in the webshell, first right click on the download link and select 'Copy Link' or 'Copy Link Address'
> 3. Type everything after the dollar sign in the webshell: `$ wget`, then paste the link after the space after `wget` and press enter. This will download the script for you in the webshell so you can run it!
> 4. Finally, to run the script, type everything after the dollar sign and then press enter: `$ python3 runme.py` You should have the flag now!

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** Sujeet Kumar

## Solución
Literalmente eso: descargar y ejecutar el script.

```bash
wget https://artifacts.picoctf.net/c/34/runme.py
python3 runme.py
# picoCTF{run_s4n1ty_run}
```

Flag: `picoCTF{run_s4n1ty_run}`

## Notas adicionales
- Reto de "sanity check"/calentamiento puro: el script solo define `flag = 'picoCTF{...}'` y hace `print(flag)`. No hay lógica que resolver.

## Referencias
- Reto: https://learn.cylabacademy.org/library/250
- Fuente: `runme.py` (copia en esta carpeta)
