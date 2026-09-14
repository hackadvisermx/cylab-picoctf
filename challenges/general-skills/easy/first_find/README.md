# General Skills — First Find

## Descripción
> **Prompt oficial:** "Unzip this archive and find the file named 'uber-secret.txt'"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** (General Skills)
- **Autor:** LT 'syreal' Jones

## Solución
El zip tiene un árbol de carpetas profundo (incluyendo una oculta, `.secret`); en vez de navegar manualmente, `find` localiza el archivo por nombre en una sola pasada:

```bash
unzip files.zip -d extracted
find extracted -iname "uber-secret.txt"
# extracted/files/adequate_books/more_books/.secret/deeper_secrets/deepest_secrets/uber-secret.txt
cat extracted/files/.../uber-secret.txt
```

Flag: `picoCTF{f1nd_15_f457_ab443fd1}`

## Notas adicionales
- Complementa a `Big Zip` (que se resuelve con `grep -r` por contenido): aquí la búsqueda es por **nombre de archivo**, el caso de uso canónico de `find`.
- Nota: `find` por defecto no explora archivos/carpetas ocultos de forma diferente a los normales en Linux (a diferencia de `ls` sin `-a`), así que encuentra `.secret/` sin necesidad de ninguna opción extra.

## Referencias
- Reto: https://learn.cylabacademy.org/library/320
