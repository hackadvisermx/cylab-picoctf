# General Skills — dont-you-love-banners

## Descripción
> **Prompt oficial del reto:** "Can you abuse the banner? The server has been leaking some crucial information on `tethys.picoctf.net <puerto>`. Use the leaked information to get to the server. To connect to the running application use `nc tethys.picoctf.net <puerto>`. From the above information abuse the machine and find the flag in the /root directory."
>
> **Hints:**
> 1. Do you know about symlinks?
> 2. Maybe some small password cracking or guessing

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** Loic Shema / syreal

## Solución
El reto expone dos puertos: uno "filtra información crucial" y otro corre la aplicación real.

1. El puerto de "leak" resulta ser un socket que devuelve el banner SSH de OpenSSH, pero con una contraseña añadida directamente al string de versión:

```bash
nc -w 5 tethys.picoctf.net <puerto_leak> < /dev/null
# SSH-2.0-OpenSSH_7.6p1 My_Passw@rd_@1234
```

2. Con esa contraseña se conecta al puerto de la aplicación (`nc tethys.picoctf.net <puerto_app>`), que pide una serie de preguntas encadenadas:
   - `what is the password?` → `My_Passw@rd_@1234`
   - `What is the top cyber security conference in the world?` → `DEF CON`
   - `the first hacker ever was known for phreaking...` → `John Draper`

   Si las tres respuestas son correctas, el programa hace `pty.spawn('su - player')`, dando un shell interactivo como el usuario `player`.

3. `/root/script.py` es legible por todos (`-rw-r--r--`) y revela el código completo del servidor. La parte clave:

```python
if __name__ == "__main__":
    try:
      with open("/home/player/banner", "r") as f:
        print(f.read())
    except:
      print("*** DEFAULT BANNER ***")
```

   Este bloque se ejecuta **antes** de pedir la contraseña, y el proceso del servidor corre como **root** (es el proceso que luego hace `su - player`). Es decir, cada vez que alguien se conecta al puerto de la app, un proceso root abre y muestra el contenido de `~player/banner`.

4. `/root/flag.txt` existe pero es `-rwx------` (solo root puede leerlo). El "abuso del banner" consiste en reemplazar el archivo `banner` del home de `player` (que sí es escribible por `player`) por un **symlink** a `/root/flag.txt`:

```bash
rm -f /home/player/banner
ln -s /root/flag.txt /home/player/banner
```

5. Al reconectar al puerto de la app, el proceso root vuelve a ejecutar `open("/home/player/banner")` — pero ahora ese archivo es un symlink a `/root/flag.txt`, así que el proceso root lo lee y lo imprime en el banner, filtrando la flag antes incluso de pedir la contraseña:

```bash
nc -w 5 tethys.picoctf.net <puerto_app> < /dev/null
# picoCTF{b4nn3r_gr4bb1n9_su((3sfu11y_a0e119d4}
```

## Notas adicionales
- Todo el flujo se automatizó con un script Python (`socket.create_connection` + lectura por timeouts) en vez de escribir a mano en el webshell del navegador, ya que el reto está marcado como `browser_webshell_solvable` pero interactuar por `nc` directo desde la terminal local es más confiable.
- Se detectó que abrir/cerrar muchas conexiones muy seguidas contra el mismo puerto de la app provocaba `Connection reset by peer` en intentos posteriores (probablemente algún tipo de throttling o un socket que queda en un estado raro tras `su - player`). La solución fue reiniciar la instancia y hacer un único intento limpio de principio a fin.
- Es un ejemplo clásico de "arbitrary file read vía symlink" cuando un proceso privilegiado abre un archivo bajo control de un usuario sin privilegios, sin verificar que no sea un symlink hacia una ruta protegida.

## Referencias
- Reto: https://learn.cylabacademy.org/library/437
