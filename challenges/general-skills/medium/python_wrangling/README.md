# General Skills — Python Wrangling

## Descripción
> **Prompt oficial del reto:** "Python scripts are invoked kind of like programs in the Terminal... Can you run `ende.py` using `password.txt` to get `flag.txt.en`?" — se entregan los tres archivos directamente (sin instancia remota).
>
> **Hints:**
> 1. Get the Python script accessible in your shell by entering the following command in the Terminal prompt: $ wget followed by a link to the script. The link can be copied from the details section.
> 2. $ man python

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
`ende.py` es un script de cifrado/descifrado simétrico basado en **Fernet** (de la librería `cryptography`), que deriva la clave a partir de una contraseña codificada en Base64:

```python
if sys.argv[1] == "-d":
    sim_sala_bim = sys.argv[3]        # contraseña por argumento
    ssb_b64 = base64.b64encode(sim_sala_bim.encode())
    c = Fernet(ssb_b64)
    with open(sys.argv[2], "r") as f:
        data_c = c.decrypt(data.encode())
```

`password.txt` contiene literalmente la contraseña en texto plano (`720b6ad346f84cd483c60c7464dd95d4`), así que basta con invocar el script tal como indica el enunciado, pasando el modo, el archivo cifrado y la contraseña como argumentos:

```bash
python3 ende.py -d flag.txt.en "$(cat password.txt)"
# picoCTF{4p0110_1n_7h3_h0us3_9c5f9bcf}
```

(la única fricción real fue instalar la dependencia `cryptography`, ausente en un Python del sistema gestionado externamente — se resolvió con un virtualenv: `python3 -m venv venv && ./venv/bin/pip install cryptography`).

## Notas adicionales
- El reto es literal: el propio enunciado da el comando exacto a ejecutar ("Can you run ende.py using password.txt to get flag.txt.en?"). No hace falta ingeniería inversa del cifrado Fernet, solo leer el `usage_msg`/código para saber el orden de los argumentos (`-d archivo contraseña`).
- No requiere lanzar instancia remota: los 3 archivos se descargan directamente desde los enlaces del modal y todo se resuelve en local.

## Referencias
- Reto: https://learn.cylabacademy.org/library/166
