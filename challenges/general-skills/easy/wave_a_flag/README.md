# General Skills — Wave a flag

## Descripción
> **Prompt oficial:** "Can you invoke help flags for a tool or binary? This program has extraordinarily helpful information..." (binario descargable: `warm`)

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
El binario (ELF x86-64 para Linux) imprime la flag directamente al invocarlo con `--help` (según el propio nombre del reto). Como es un binario Linux, no se puede ejecutar directamente en macOS, pero no hace falta ejecutarlo: la cadena de texto ya está en claro dentro del propio archivo.

```bash
chmod +x warm
./warm --help     # en un host Linux: imprime la flag
# o, sin ejecutar nada (funciona igual en cualquier SO):
strings warm | grep picoCTF
```

Flag: `picoCTF{b1scu1ts_4nd_gr4vy_ac5832c}`

## Notas adicionales
- `strings` es la herramienta perfecta cuando el binario no se puede o no conviene ejecutar (arquitectura distinta, posible riesgo): busca todas las secuencias de texto imprimible embebidas en el archivo, sin necesidad de interpretarlo como código.

## Referencias
- Reto: https://learn.cylabacademy.org/library/170
