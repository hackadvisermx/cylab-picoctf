# Forensics — Lookey here

## Descripción
> **Prompt oficial del reto:** "Attackers have hidden information in a very large mass of data in the past, maybe they are still doing it.
> Download the data [here](https://challenge-files.cylabacademy.net/library/764d21f0248d7c1df55583eb1ad863dad241f86f90dd2717e8aa5b9fc3a7e26e/anthem.flag.txt)."
>
> **Hints:**
> 1. Download the file and search for the flag based on the known prefix.

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones / Mubarak Mikail

## Solución
El reto proporciona un archivo de texto de gran tamaño llamado `anthem.flag.txt` que contiene el texto completo de la novela corta *Anthem* de Ayn Rand (más de 2,100 líneas).

1. **Búsqueda por patrón conocido:**
   - La pista indica buscar la flag utilizando el prefijo conocido del CTF (`academy{` o `picoCTF{`).
   - Usando la herramienta estándar `grep`, se localiza inmediatamente la línea exacta que contiene la flag en medio del texto literario.

```bash
# Búsqueda directa con grep
grep -oE "academy\{[^}]+\}" anthem.flag.txt

# O de forma general buscando por prefijo
grep -i "academy{" anthem.flag.txt
```

## Notas adicionales
- `grep` es una de las herramientas fundamentales en análisis forense y triage rápido para localizar patrones, indicadores de compromiso (IoC) y artefactos en logs y volcados de texto de gran volumen.

## Referencias
- Reto: https://learn.cylabacademy.org/library/279
- GNU Grep Manual: https://www.gnu.org/software/grep/manual/grep.html
