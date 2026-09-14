# General Skills — SansAlpha

## Descripción
> **Prompt oficial del reto:** "The Multiverse is within your grasp! Unfortunately, the server that contains the secrets of the multiverse is in a universe where keyboards only have numbers and (most) symbols." Se entrega `ssh -p <puerto> ctf-player@mimas.picoctf.net` con una contraseña.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** syreal

## Solución
Al conectar por SSH se cae en un prompt personalizado `SansAlpha$` (en realidad **bash real**, con un filtro de teclado que intercepta cada carácter tecleado). Cualquier letra o dígito (a-z, A-Z, 0-9) dispara `SansAlpha: Unknown character detected` y descarta el comando. Los símbolos (`/ * ? $ { } . ~ ! @ # %`, etc.) sí se aceptan tal cual, así que hay que construir comandos de bash usando **solo símbolos**.

Con eso disponible se puede usar:
- **Comodines de glob** (`*`, `?`) para referirse a nombres de archivo sin escribir sus letras.
- **Parámetros especiales de bash** que se referencian solo con símbolos: `$?`, `$$`, `$#`, `$@`, `$*`, `$-`, `$_` (no hicieron falta todos, pero están disponibles).
- **Sustitución de comando "desnuda" de lectura de archivo**: `$(<archivo)` (equivalente a `$(cat archivo)` pero sin invocar ningún binario por nombre), construida solo con `$ ( < )`.

Pasos:

1. Enumerar el directorio home con `*` a secas como comando: bash expande el glob y trata el resultado como "comando no encontrado", filtrando el nombre en el mensaje de error:
   ```
   *
   → bash: blargh: command not found
   ```
   Hay un único elemento, `blargh`, que resulta ser un directorio.

2. Bajar un nivel con `*/*` (glob anidado, sin necesidad de `cd`):
   ```
   */*
   → bash: blargh/flag.txt: Permission denied
   ```
   Revela `blargh/flag.txt`, pero sin permiso de **ejecución** (no se puede correr como comando).

3. Determinar la longitud exacta del nombre para poder referenciarlo sin ambigüedad de glob, probando `*/` + N signos de interrogación como *target* de una redirección (`$(<patrón)`), hasta encontrar la longitud que no da "No such file" ni "ambiguous redirect":
   ```bash
   $(<*/????????)   # 8 signos de interrogación = len("flag.txt")
   ```
   Esto sí abre el archivo para **lectura** (el permiso denegado anterior era solo de ejecución), y el contenido leído se ejecuta como línea de comando — filtrando su texto en el mensaje de error de "comando no encontrado". Para evitar que el *word-splitting* trocee el contenido en varias palabras (y así perder texto en el mensaje de error, ya que solo se muestra la primera palabra no reconocida), se encierra la sustitución entre comillas dobles para que todo el contenido viaje como un único argumento:
   ```bash
   "$(<*/????????)"
   → bash: return 0 picoCTF{7h15_mu171v3r53_15_m4dn355_36a674c0}: command not found
   ```

   El archivo tenía una línea decorativa `return 0` antes de la flag real.

## Notas adicionales
- Es la variante "sin alfanuméricos" del clásico truco de *shell escape*: en vez de intentar generar letras a partir de variables de entorno (imposible aquí porque sus nombres, `PATH`, `HOME`, etc., contienen letras y no se pueden teclear), la solución se apoya enteramente en el globbing del sistema de archivos (`*`, `?`) para "deletrear" rutas, y en la sustitución de comando `$(<archivo)` — una construcción 100% simbólica — para leer archivos sin invocar `cat`, `less`, etc.
- Interactuar con este reto requirió una sesión **SSH interactiva real** (no un simple `nc`), automatizada con `paramiko` (`invoke_shell` + gestión manual del *cursor position report* `\x1b[6n` que pide la terminal remota) en vez del webshell embebido del navegador, que en sesiones anteriores se había vuelto inestable con este mismo tipo de reto.
- Al usar patrones de glob de 3+ caracteres sin querer (p. ej. `/???/???`), bash puede terminar ejecutando binarios inesperados (`ar`, `awk`, ...) porque el glob resuelve alfabéticamente a *todos* los que calzan el patrón, y solo el primero se trata como comando — hay que ser preciso con el número de `?` para apuntar exactamente al archivo/directorio deseado.

## Referencias
- Reto: https://learn.cylabacademy.org/library/436
