# General Skills — Glitch Cat

## Descripción
> **Prompt oficial:** "Our flag printing service has started glitching! `nc <host> <puerto>`"
>
> **Hints:**
> 1. ASCII is one of the most common encodings used in programming
> 2. We know that the glitch output is valid Python, somehow!
> 3. Press Ctrl and c on your keyboard to close your connection and return to the command prompt.

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** Beginner picoMini 2022
- **Autor:** LT 'syreal' Jones

## Solución
El servicio, en vez de imprimir la flag, imprime literalmente el **código fuente de la expresión Python** que la construiría (el `print()` interno probablemente falla o usa `repr()` por error):

```
'picoCTF{gl17ch_m3_n07_' + chr(0x61) + chr(0x34) + chr(0x33) + chr(0x39) + chr(0x32) + chr(0x64) + chr(0x32) + chr(0x65) + '}'
```

Basta con evaluar esa expresión (literalmente pegarla en un intérprete Python):

```bash
python3 -c "print('picoCTF{gl17ch_m3_n07_' + chr(0x61) + chr(0x34) + chr(0x33) + chr(0x39) + chr(0x32) + chr(0x64) + chr(0x32) + chr(0x65) + '}')"
```

Flag: `picoCTF{gl17ch_m3_n07_a4392d2e}`

## Notas adicionales
- El "glitch" del servicio es justamente no evaluar la expresión antes de imprimirla — la solución es hacer manualmente lo que el servidor debería haber hecho.

## Referencias
- Reto: https://learn.cylabacademy.org/library/242
