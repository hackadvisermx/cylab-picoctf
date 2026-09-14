# General Skills — Static ain't always noise

## Descripción
> **Prompt oficial:** "Can you look at the data in this binary? The bash script might help!" (`static`, `ltdis.sh`)

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2021
- **Autor:** syreal

## Solución
`ltdis.sh` es un pequeño wrapper para desensamblar con `objdump`, pero para este binario ni hace falta desensamblar nada: la flag ya está en texto plano en la sección de datos.

```bash
strings static | grep picoCTF
# picoCTF{d15a5m_t34s3r_20335e41}
```

Flag: `picoCTF{d15a5m_t34s3r_20335e41}`

## Notas adicionales
- El nombre del reto ("static" no siempre es "ruido") es un guiño a que un análisis estático simple (`strings`) basta, sin necesidad de ejecutar el binario ni desensamblarlo con la herramienta que se ofrece.

## Referencias
- Reto: https://learn.cylabacademy.org/library/163
