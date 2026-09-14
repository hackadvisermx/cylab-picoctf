# General Skills — bytemancy 1

## Descripción
> **Prompt oficial:** "Can you conjure the right bytes? The program's source code can be downloaded here. Connect to the program with netcat: `nc <host> <puerto>`"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

## Solución
El código fuente (`app.py`, adjunto en esta carpeta) es muy simple:

```python
user_input = input('==> ')
if user_input == "\x65"*1751:
  print(open("./flag.txt", "r").read())
```

Solo hay que enviar el carácter ASCII decimal 101 (`\x65` = `'e'`) repetido 1751 veces, sin separadores, seguido de un salto de línea.

```bash
python3 -c "print('e'*1751)" | nc -w 8 <host> <puerto>
```

Flag: `picoCTF{h0w_m4ny_e's???_0c1ad83a}`

## Notas adicionales
- **Nota de esta sesión:** el webshell embebido del navegador de CyLab Academy se quedó colgado varias veces al intentar conectar por `nc` desde ahí (estado "Starting instance..." indefinido, desconexiones tras inactividad). Conectar directamente desde una terminal local (`nc -w <segundos> <host> <puerto>`) funcionó al instante — para retos que solo requieren hablar con un servicio `nc` público (no archivos del webshell compartido), es más rápido usar la propia terminal que el navegador.

## Referencias
- Reto: https://learn.cylabacademy.org/library/762
- Fuente: `app.py` (copia en esta carpeta)
