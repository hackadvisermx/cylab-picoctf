# General Skills — 1_wanna_b3_a_r0ck5tar

## Descripción
> **Prompt oficial:** "I wrote you another song. Put the flag in the picoCTF{} flag format"
>
> El enlace "song" descarga otro `lyrics.txt` (ver copia local en esta carpeta) — de nuevo código **Rockstar**, como en el reto `mus1c`.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Alex Bushkin

## Solución
Este reto reutiliza la idea de `mus1c` (código Rockstar disfrazado de letra de canción), pero añade dos complicaciones reales:

1. **Requiere entrada por stdin** (`Listen to the music` / `Listen to the rhythm`) y tiene una rama condicional (`If ... / Else ...`), a diferencia del programa lineal de `mus1c`.
2. **Contiene una variable llamada `Rock`**, que colisiona con la palabra reservada de Rockstar para la operación de pila `Rock <var> like <expr>` (push). Tanto el intérprete oficial online (Starship, https://codewithrockstar.com/online) como el intérprete de referencia (Satriani, repo `RockstarLang/rockstar`) fallan al parsear la línea `Rock is electric heaven` con un error de sintaxis. Hubo que **parchear localmente esa única línea** (renombrar la variable a `Rocking`, que no colisiona) para poder ejecutar el programa; el resto del código es idéntico al original.

Con el código parcheado, ejecutarlo con el intérprete de referencia (Satriani) en Node, controlando el `stdin` mediante una función de entrada propia (más fiable que intentar pasar `stdin` real, ya que `readline-sync` exige una TTY interactiva que no está disponible en el webshell/CI):

```js
// run.js
const satriani = require('./satriani.js'); // del repo RockstarLang/rockstar, carpeta satriani/
const fs = require('fs');
const program = fs.readFileSync('lyrics_patched.rock', 'utf8');
let rockstar = new satriani.Interpreter();
let inputs = ["10", "170"]; // ver razonamiento abajo
let idx = 0;
let outputs = [];
rockstar.run(program, () => inputs[idx++], (s) => outputs.push(s));
console.log(JSON.stringify(outputs));
```

¿Por qué esos dos valores de entrada? Inspeccionando el AST (`rockstar.parse(program)`) se ve que:
- `A guitar is a six-string` asigna a la variable `a_guitar` el número **10** (literal poético: la longitud de cada palabra tras "is" forma un dígito).
- `Music is a billboard-burning razzmatazz!` asigna a `music` el número **170**.
- La condición `If the music is a guitar` compara la entrada de `Listen to the music` contra `a_guitar` (10) — hay que introducir `10`.
- La condición `If the rhythm without Music is nothing` compara `rhythm - Music == 0`, es decir, la segunda entrada debe **igualar el valor que tenía `Music` en ese momento** (170) para que la resta dé cero ("nothing").

Solo si ambas condiciones son verdaderas se ejecuta el bloque completo que reasigna variables y hace varios `Shout`/`Scream`/`Say` de valores numéricos (todos ellos códigos ASCII):

```
Salida: ["Keep on rocking!", 66, 79, 78, 74, 79, 86, 73]
```

```bash
python3 -c "
vals = [66,79,78,74,79,86,73]
print(''.join(chr(v) for v in vals))
"
# -> BONJOVI
```

Flag: `picoCTF{BONJOVI}` (un guiño a la banda de rock Bon Jovi).

## Notas adicionales
- **Detalle clave sobre Rockstar que hay que recordar**: los bloques (`If`/`Else`, bucles) en Rockstar terminan con una **línea en blanco**, no con indentación. El archivo original no tiene ninguna línea en blanco, así que el `If` de la línea 7 (y el `If` anidado de la línea 10) engloban **todo el resto del programa** hasta el primer `Break it down` (instrucción de "break" de bucle, aunque aquí no hay ningún bucle activo — su efecto es simplemente terminar la ejecución en ese punto, ya que la acción "break" se propaga hacia arriba por cada `list`/`conditional` hasta el nivel superior). Sin entender esto, es fácil asumir erróneamente que las líneas se ejecutan de forma independiente/secuencial.
- Si las dos entradas no coinciden con los valores esperados, el programa no imprime nada (las condiciones son falsas y no hay una rama alternativa en el `If` exterior) — es una señal útil para verificar que el razonamiento sobre los valores de entrada es correcto.
- Se evitó usar el intérprete web (`codewithrockstar.com/online`) para la ejecución final porque su editor basado en CodeMirror interceptaba las pulsaciones de teclado al pegar texto mediante automatización de navegador (atajos de teclado no deseados), haciendo poco fiable escribir el programa completo por esa vía; el intérprete de Node (Satriani) permite pasar el programa como string y controlar par completo el stdin con una función propia, evitando ese problema.

## Referencias
- Reto: https://learn.cylabacademy.org/library/82
- Archivo fuente original: `lyrics.txt` (copia en esta carpeta)
- Intérprete de referencia: https://github.com/RockstarLang/rockstar (carpeta `satriani/`)
- Especificación de Rockstar: https://codewithrockstar.com/docs
