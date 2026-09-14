# General Skills — Password Profiler

## Descripción
> **Prompt oficial:** "We intercepted a suspicious file from a system, but instead of the password itself, it only contains its SHA-1 hash. Using OSINT techniques, you are provided with personal details about the target. Your task is to leverage this information to generate a custom password list and recover the original password by matching its hash. Download: `userinfo` (detalles personales), `hash` (hash SHA-1), `check_password` (script para probar contraseñas contra el hash)."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
`check_password.py` deja claro que la wordlist se generó con **CUPP** (Common User Passwords Profiler), una herramienta que crea diccionarios de contraseñas probables a partir de datos personales (nombre, apodo, fecha de nacimiento, pareja, hijo/a, mascota...).

```
userinfo.txt:
First Name: Alice
Surname: Johnson
Nickname: AJ
Birthdate: 15-07-1990
Partner's Name: Bob
Child's Name: Charlie
```

Pasos:

```bash
git clone https://github.com/Mebus/cupp.git
cd cupp
python3 cupp.py -i   # modo interactivo, se rellenan los campos con los datos de userinfo.txt
# -> genera alice.txt (~14.8k palabras)

cp alice.txt /ruta/al/reto/passwords.txt
python3 check_password.py
# Password found: picoCTF{Aj_15901990}
```

## Notas adicionales
- CUPP no está preinstalado ni en macOS ni en el webshell de la plataforma; se clonó desde su repo oficial (https://github.com/Mebus/cupp) y se ejecutó localmente.
- El modo interactivo de CUPP (`-i`) pide, en este orden: nombre, apellido, apodo, fecha de nacimiento, nombre/apodo/fecha de la pareja, nombre/apodo/fecha del hijo/a, mascota, empresa, si se quieren añadir palabras clave, caracteres especiales al final y números aleatorios — cada pregunta admite Enter para dejarla en blanco. Automatizarlo con un heredoc/`<` requiere contar exactamente el número de líneas de respuesta esperadas (o se desincroniza el diálogo).
- Al terminar, CUPP pregunta "Hyperspeed Print? (Y/n)" — decir que sí abre un modo de impresión con `curses` que, sin una TTY real (por ejemplo al ejecutarlo con entrada/salida redirigida), se queda en un bucle imprimiendo errores de `TERM` indefinidamente; no afecta al archivo de salida (ya se generó antes de esa pregunta), así que basta con matar el proceso e ignorar esa parte.
- El resultado exacto (`Aj_15901990`) reordena los dígitos de la fecha de nacimiento (15071990 → 15901990) siguiendo uno de los patrones de mangling propios de CUPP, no un error de transcripción — se verificó programáticamente comparando el hash SHA-1 de cada candidato con el hash objetivo.

## Referencias
- Reto: https://learn.cylabacademy.org/library/712
- Herramienta: https://github.com/Mebus/cupp
- Archivos: `userinfo.txt`, `hash.txt`, `check_password.py` (copias en esta carpeta)
