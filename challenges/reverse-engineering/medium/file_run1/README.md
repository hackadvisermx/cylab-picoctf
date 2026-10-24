# Reverse Engineering — file-run1

## Descripción
> **Prompt oficial del reto:** "A program has been provided to you, what happens if you try to run it on the command line?
> Download the program [here](https://challenge-files.cylabacademy.net/library/4cb47d716d0004f01f73bbcc894465736c68b3c2d78e32c622e5a63c2bcb885e/run)."
>
> **Pistas oficiales:**
> 1. To run the program at all, you must make it executable (i.e. `$ chmod +x run`)
> 2. Try running it by adding a '.' in front of the path to the file (i.e. `$ ./run`)

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** Will Hong

## Solución
El reto proporciona un archivo binario ejecutable ELF de 64 bits para arquitectura x86-64 denominado `run`.

Para resolverlo:
1. Otorgamos permisos de ejecución al archivo con `chmod +x run`.
2. Ejecutamos el archivo en la terminal anteponiendo `./`:

```bash
chmod +x run
./run
```

El programa se ejecuta directamente e imprime la bandera correspondiente en la salida estándar.

Asimismo, mediante análisis estático podemos inspeccionar las cadenas del binario utilizando el comando `strings` o con herramientas de desensamblado como `objdump` o `ghidra`:

```bash
strings run | grep "academy{"
```

La bandera se encuentra directamente como una cadena ASCII en texto plano dentro de la sección `.rodata`.

## Notas adicionales
En sistemas tipo UNIX, un archivo descargado normalmente carece del bit de ejecución (`+x`) por defecto por motivos de seguridad. Agregar dicho permiso permite que el kernel reconozca el archivo como un ejecutable válido.

## Referencias
- Reto: https://learn.cylabacademy.org/library/266
- Apoyo: https://man7.org/linux/man-pages/man1/chmod.1.html
