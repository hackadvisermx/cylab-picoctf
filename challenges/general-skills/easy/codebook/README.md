# General Skills — Codebook

## Descripción
> **Prompt oficial:** "Run the Python script `code.py` in the same directory as `codebook.txt`."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
Literal: descargar ambos archivos en la misma carpeta y ejecutar. El script construye la clave XOR leyendo caracteres concretos de `codebook.txt` por índice (`codebook[4]`, `codebook[14]`, etc.), sin necesidad de que el usuario haga nada más.

```bash
python3 code.py
# picoCTF{c0d3b00k_455157_197a982c}
```

Flag: `picoCTF{c0d3b00k_455157_197a982c}`

## Notas adicionales
- El único requisito real es tener ambos archivos (`code.py` y `codebook.txt`) en el mismo directorio — el propio script comprueba `FileNotFoundError` y avisa de esto si falta `codebook.txt`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/238
- Ficheros: `code.py`, `codebook.txt` (copias en esta carpeta)
