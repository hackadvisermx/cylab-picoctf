# General Skills — Wave a flag

## Descripción
> **Prompt oficial:** "Can you invoke help flags for a tool or binary? This program has extraordinarily helpful information..." (binario descargable: `warm`)
>
> **Hints:**
> 1. This program will only work in the webshell or another Linux computer.
> 2. To get the file accessible in your shell, enter the following in the Terminal prompt: `$ wget <URL here>`, where the url can be found in the details section.
> 3. Run this program by entering the following in the Terminal prompt: `$ ./warm`, but you'll first have to make it executable with `$ chmod +x warm`
> 4. -h and --help are the most common arguments to give to programs to get more information from them!
> 5. Not every program implements help features like -h and --help.

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
El binario (ELF x86-64 para Linux) imprime la flag directamente al invocarlo con `--help` (según el propio nombre del reto). Como es un binario Linux, no se puede ejecutar directamente en macOS, pero no hace falta ejecutarlo: la cadena de texto ya está en claro dentro del propio archivo.

```bash
chmod +x warm
./warm --help     # en un host Linux: imprime la flag
# o, sin ejecutar nada (funciona igual en cualquier SO):
strings warm | grep picoCTF
```

Flag: `picoCTF{b1scu1ts_4nd_gr4vy_ac5832c}`

## Notas adicionales
- `strings` es la herramienta perfecta cuando el binario no se puede o no conviene ejecutar (arquitectura distinta, posible riesgo): busca todas las secuencias de texto imprimible embebidas en el archivo, sin necesidad de interpretarlo como código.

## Referencias
- Reto: https://learn.cylabacademy.org/library/170
