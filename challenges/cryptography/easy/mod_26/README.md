# Cryptography — Mod 26

## Descripción
> **Prompt oficial del reto:** "Cryptography can be easy, do you know what ROT13 is? `values.txt`"
>
> **Hints:**
> 1. This can be solved online if you don't want to do it by hand!

- **Categoría:** Cryptography
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2021
- **Autor:** Pandu

## Solución
"Mod 26" alude al alfabeto de 26 letras: es de nuevo **ROT13**. El cipher viene en `values.txt`; se decodifica rotando 13:

```bash
curl -s "<url>/values.txt" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
# academy{next_time_I'll_try_2_rounds_of_rot13_5c5f5b36}
```

## Notas adicionales
- Idéntico a *13*: ROT13 sobre todo el texto. El nombre "Mod 26" es la pista del tamaño del alfabeto.

## Referencias
- Reto: https://learn.cylabacademy.org/library/144
