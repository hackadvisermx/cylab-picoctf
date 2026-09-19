# General Skills — Special

## Descripción
> **Prompt oficial del reto:** "Don't power users get tired of making spelling mistakes in the shell? Not anymore! Enter Special, the Spell Checked Interface for Affecting Linux. Now, every word is properly spelled and capitalized... automatically and behind-the-scenes! Be the first to test Special in beta [...] That's Special (TM)" — se entrega acceso SSH (`ssh -p <puerto> ctf-player@saturn.picoctf.net`, contraseña provista).

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
Al conectar, en vez de un `bash` normal aparece un prompt `Special$` que corre cada comando a través de un "corrector ortográfico" antes de ejecutarlo. Probando comandos comunes se observa el patrón exacto:

```
$ ls          ->  ejecuta: Is       (sh: Is: not found)
$ cat         ->  ejecuta: Cat      (sh: Cat: not found)
$ id          ->  ejecuta: Id       (sh: Id: not found)
$ pwd         ->  ejecuta: Pod      (sh: Pod: not found)
$ cd          ->  ejecuta: Ad       (sh: Ad: not found)
```

Dos transformaciones distintas, con reglas distintas:
1. **Corrección ortográfica** (`ls`→`is`, `pwd`→`pod`, `cd`→`ad`, `whoami`→`whom`): se aplica a **cualquier palabra que no exista en el diccionario**, sin importar su posición en la línea.
2. **Capitalización de la primera letra**: se aplica **solo a la primera palabra de la línea**, sin importar si es una palabra válida o no (`cat`→`Cat`, `id`→`Id`).

Como los nombres de comandos de Linux son sensibles a mayúsculas/minúsculas, la primera palabra **siempre** queda rota (`Cat`, `Id`, `Ls`... ninguno existe), incluso si el comando en sí estaba bien escrito.

**Bypass:** dado que solo la *primera* palabra de la línea se capitaliza forzosamente, basta con anteponer una palabra basura + `;` (separador de comandos de `sh`) para que el comando real quede en segunda posición y no sea tocado por la capitalización — solo necesita ser una palabra ya válida en el diccionario (para que tampoco la "corrija"):

```
Special$ x ; cat /home/ctf-player/blargh/flag.txt
I ; cat /home/ctf-player/blargh/flag.txt
sh: 1: I: not found
picoCTF{5p311ch3ck_15_7h3_w0r57_0c61d335}
```

`x` se corrige/capitaliza a `I` y falla ("command not found"), pero `sh` sigue ejecutando lo que viene después del `;` sin abortar, y como `cat` es una palabra válida en el diccionario y ya no está en primera posición, pasa intacto — el comando real se ejecuta con éxito.

El archivo se encontró recorriendo el sistema con `find` (aunque las banderas con guion, como `-iname`, se pierden — el corrector también les quita el `-`, así que `find` termina corriendo sin filtro y lista todo el árbol de directorios; hay que buscar "flag" en esa salida completa en vez de depender de la bandera).

## Notas adicionales
- Lección clave: cuando una "protección" solo actúa sobre **una posición fija** de la entrada (aquí, la primera palabra) en vez de sobre la semántica completa del comando, basta con desplazar el contenido malicioso/real a una posición no protegida usando la sintaxis propia del intérprete de destino (aquí, el separador `;` de `sh`) — un patrón general útil contra filtros de "primera palabra"/"primer carácter" en cualquier shell restringido.
- Los guiones de las banderas (`-iname`, `-la`) se pierden en la reescritura del corrector — cualquier intento de usar flags con guion falla silenciosamente (el guion desaparece y el resto de la bandera se trata como un argumento posicional más).
- Palabras ya válidas en inglés (`cat`, `id`) atraviesan el corrector sin cambios en cualquier posición que no sea la primera; palabras inventadas o abreviaturas de Unix (`ls`, `pwd`, `cd`, `whoami`) se "corrigen" a la palabra válida más parecida, rompiéndolas siempre, sin importar la posición.

## Referencias
- Reto: https://learn.cylabacademy.org/library/377
