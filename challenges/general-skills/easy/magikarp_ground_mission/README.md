# General Skills — Magikarp Ground Mission

## Descripción
> **Prompt oficial:** "Do you know how to move between directories and read files in the shell? Start the container, ssh to it, and then ls once connected to begin. Login via ssh as ctf-player con la contraseña `<pass>` en el host `<host>` y puerto `<puerto>`."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
La flag está repartida en 3 archivos esparcidos por el sistema de archivos, cada uno con una pista hacia el siguiente:

```bash
ssh -p <puerto> ctf-player@<host>
ls -la
# 3of3.flag.txt (en el home) y drop-in/ (subcarpeta)

cat drop-in/1of3.flag.txt              # picoCTF{xxsh_
cat drop-in/instructions-to-2of3.txt   # "go to the root of all things, more succinctly `/`"
cat /2of3.flag.txt                     # 0ut_0f_//4t3r_
cat 3of3.flag.txt                      # 0b24fc4f}
```

Concatenando las tres partes (usando `od -c` para verificar los bytes exactos, sin saltos de línea de más):

Flag: `picoCTF{xxsh_0ut_0f_//4t3r_0b24fc4f}`

## Notas adicionales
- Ejercicio básico de navegación (`cd`/`ls`) entre el home del usuario y la raíz `/` del sistema de archivos — cada parte da una pista textual de dónde está la siguiente en vez de venir todas en el mismo sitio.
- Al concatenar partes leídas con `cat`, cuidado con los saltos de línea finales de cada archivo (`od -c` permite comprobar si un archivo termina en `\n` o no, para no meter un salto de línea de más en la flag final).

## Referencias
- Reto: https://learn.cylabacademy.org/library/189
