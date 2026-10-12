# Cryptography — 13

## Descripción
> **Prompt oficial del reto:** "Cryptography can be easy, do you know what ROT13 is? `npnqrzl{abg_gbb_onq_bs_n_ceboyrz}`"
>
> **Hints:**
> 1. This can be solved online if you don't want to do it by hand!

- **Categoría:** Cryptography
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2019
- **Autor:** Alex Fulton/Daniel Tunitis

## Solución
El cipher está en el propio enunciado y, como dice el nombre del reto, es **ROT13** (César con desplazamiento 13). Se decodifica rotando cada letra 13 posiciones:

```bash
echo "npnqrzl{abg_gbb_onq_bs_n_ceboyrz}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
# academy{not_too_bad_of_a_problem}
```

## Notas adicionales
- ROT13 es su propia inversa (aplicarlo dos veces devuelve el texto original), por eso `tr 'A-Za-z' 'N-ZA-Mn-za-m'` sirve tanto para cifrar como descifrar.

## Referencias
- Reto: https://learn.cylabacademy.org/library/62
