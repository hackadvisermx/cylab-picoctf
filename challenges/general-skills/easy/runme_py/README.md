# General Skills — runme.py

## Descripción
> **Prompt oficial:** "Run the `runme.py` script to get the flag. Download the script with your browser or with `wget` in the webshell."

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
