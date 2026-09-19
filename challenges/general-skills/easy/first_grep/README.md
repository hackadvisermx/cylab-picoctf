# General Skills — First Grep

## Descripción
> **Prompt oficial:** "Can you find the flag in the file? This would be really tedious to look through manually, something tells me there is a better way."
>
> **Hints:**
> 1. grep tutorial

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2019
- **Autor:** Alex Fulton/Danny Tunitis

## Solución
Archivo lleno de basura aleatoria con la flag embebida en medio. `grep -o` la extrae directamente.

```bash
grep -o "picoCTF{[^}]*}" file
```

Flag: `picoCTF{grep_is_good_to_find_things_01aE5e9d}`

## Referencias
- Reto: https://learn.cylabacademy.org/library/85
