# General Skills — Log Hunt

## Descripción
> **Prompt oficial:** "Our server seems to be leaking pieces of a secret flag in its logs. The parts are scattered and sometimes repeated. Can you reconstruct the original flag? Download the logs and figure out the full flag from the fragments."

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoMini by CMU-Africa
- **Autor:** Yahaya Meddy

## Solución
El log (`server.log`, adjunto) tiene miles de líneas, pero solo unas pocas contienen `FLAGPART:`. Cada fragmento aparece repetido varias veces seguidas (líneas casi idénticas con distinto timestamp), pero **el orden de primera aparición** de cada fragmento distinto reconstruye la flag completa.

```bash
grep -i "FLAGPART" server.log | head -30
# picoCTF{us3_      (primera aparición: línea 1)
# y0urlinux_        (primera aparición: línea 34)
# sk1lls_           (primera aparición: línea 66)
# cedfa5fb}         (primera aparición: línea 118)
```

Concatenando en ese orden: `picoCTF{us3_y0urlinux_sk1lls_cedfa5fb}`

## Notas adicionales
- No hace falta ordenar por timestamp ni deduplicar de forma compleja: `grep` + inspección visual del orden de aparición basta, porque cada fragmento se repite de forma consecutiva (nunca entrelazado con otro fragmento antes de completarse el ciclo).
- Reto puramente offline (sin instancia ni conexión de red), solo requiere el archivo de log descargable.

## Referencias
- Reto: https://learn.cylabacademy.org/library/527
- Archivo: `server.log` (copia en esta carpeta)
