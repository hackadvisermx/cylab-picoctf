# Reverse Engineering — file-run2

## Descripción
> **Prompt oficial del reto:** "Another program, but this time, it seems to want some input. What happens if you try to run it on the command line with input "Hello!"?
> Download the program [here](https://challenge-files.cylabacademy.net/library/91e81bb7648674261d1bde25fe941741961c7363343913199c60928f9179788e/run)."
>
> **Pistas oficiales:**
> 1. Try running it and add the phrase "Hello!" with a space in front (i.e. `./run Hello!`)

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** Will Hong

## Solución
El reto provee un ejecutable ELF de Linux de 64 bits (`run`). Al intentar ejecutarlo sin argumentos o con un argumento incorrecto, indica que espera la cadena `"Hello!"` como primer parámetro en la línea de comandos (`argv[1]`).

Podemos otorgar permisos de ejecución y correr el binario con el argumento solicitado:

```bash
chmod +x run
./run Hello!
```

Al pasar `"Hello!"`, la condición de verificación en `main` se cumple y el programa imprime la bandera en formato `academy{...}`.

De manera alternativa, al inspeccionar las cadenas del binario mediante `strings`, observamos que la cadena de la bandera está embebida en texto plano sin cifrar:

```bash
strings run | grep -E "academy|picoCTF"
```

## Notas adicionales
El binario no está ofuscado ni empaquetado. La lógica en `main` simplemente evalúa `argc > 1` y realiza un `strcmp(argv[1], "Hello!")` antes de mostrar la cadena almacenada en la sección `.rodata`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/267
- Apoyo: https://man7.org/linux/man-pages/man1/strings.1.html
