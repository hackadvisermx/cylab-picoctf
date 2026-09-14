# General Skills — 2warm

## Descripción
> **Prompt oficial:** "Can you convert the number 42 (base 10) to binary (base 2)?"

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2019
- **Autor:** Sanjay C/Danny Tunitis

## Solución
`bin(42) = 101010`.

```bash
python3 -c "print(bin(42)[2:])"
# 101010
```

Flag: `picoCTF{101010}`

## Referencias
- Reto: https://learn.cylabacademy.org/library/86
