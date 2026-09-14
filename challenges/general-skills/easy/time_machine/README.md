# General Skills — Time Machine

## Descripción
> **Prompt oficial:** "What was I last working on? I remember writing a note to help me remember..."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Jeffery John

## Solución
El `challenge.zip` contiene una carpeta con un repositorio Git (`.git/`) y un `message.txt`. La flag está directamente en el **mensaje del commit**, visible con `git log`.

```bash
unzip challenge.zip
cd drop-in
git log --all --oneline
# b92bdd8 picoCTF{t1m3m@ch1n3_5cde9075}
```

Flag: `picoCTF{t1m3m@ch1n3_5cde9075}`

## Notas adicionales
- No hace falta mirar el diff ni el contenido de `message.txt`; el propio mensaje de commit (`git log`, sin `-p`) ya contiene la flag completa — el ejercicio busca que el estudiante recuerde revisar el historial de commits (`git log`), no solo el estado actual de los archivos.

## Referencias
- Reto: https://learn.cylabacademy.org/library/425
