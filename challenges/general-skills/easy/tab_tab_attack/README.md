# General Skills — Tab, Tab, Attack

## Descripción
> **Prompt oficial:** "Using tabcomplete in the Terminal will add years to your life, esp. when dealing with long rambling directory structures and filenames." (zip descargable: `Addadshashanammu.zip`)

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
El zip contiene una cadena de carpetas anidadas con nombres larguísimos y difíciles de escribir a mano (`Addadshashanammu/Almurbalarammi/Ashalmimilkala/.../fang-of-haynekhtnamet.c`) — el propio enunciado sugiere usar autocompletado con Tab en vez de teclear cada nombre. `grep -r` evita el problema por completo:

```bash
unzip Addadshashanammu.zip -d extracted
grep -rl "picoCTF{" extracted
grep "picoCTF{" extracted/Addadshashanammu/.../fang-of-haynekhtnamet.c
# printf("*ZAP!* picoCTF{l3v3l_up!_t4k3_4_r35t!_fc588427}\n");
```

Flag: `picoCTF{l3v3l_up!_t4k3_4_r35t!_fc588427}`

## Notas adicionales
- Los nombres de carpeta parecen sacados de un juego de rol tipo Nethack (nombres rúnicos aleatorios) — puro sabor temático, sin relevancia para resolver el reto.

## Referencias
- Reto: https://learn.cylabacademy.org/library/176
