# General Skills — Undo

## Descripción
> **Prompt oficial:** "Can you reverse a series of Linux text transformations to recover the original flag? Start searching for the flag here `nc <host> <puerto>`"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
Es un servicio interactivo por `nc`: en cada paso muestra la flag transformada y una pista sobre qué transformación se aplicó; hay que responder con el comando Linux que **revierte** esa transformación. El servicio valida la respuesta y avanza al siguiente paso.

```bash
nc <host> <puerto>
# Step 1 — Hint: Base64 encoded the string.        -> base64 -d
# Step 2 — Hint: Reversed the text.                 -> rev
# Step 3 — Hint: Replaced underscores with dashes.   -> tr '-' '_'
# Step 4 — Hint: Replaced curly braces with parens.   -> tr '()' '{}'
# Step 5 — Hint: Applied ROT13 to letters.            -> tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Flag: `picoCTF{Revers1ng_t3xt_Tr4nsf0rm@t10ns_fa04039f}`

## Notas adicionales
- No hace falta escribir un script: se resuelve interactivamente, escribiendo el comando (como texto, no ejecutándolo) que el propio servidor espera como respuesta en cada paso.
- ROT13 es su propia inversa (aplicar la misma transformación dos veces devuelve el texto original).

## Referencias
- Reto: https://learn.cylabacademy.org/library/766
