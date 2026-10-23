# Forensics — DISKO 1

## Descripción
> **Prompt oficial del reto:** "Can you find the flag in this disk image?
> 
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/dccdae2c264a78f31f0eb8d86c0f8fcbaccf0b0d9e775e97b08da044c05b2277/disko-1.dd.gz)."
>
> **Hints:**
> 1. Maybe Strings could help? If only there was a way to do that?

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Darkraicg492

## Solución
El reto suministra una imagen de disco comprimida `disko-1.dd.gz`. La pista sugiere expresamente la utilidad `strings`.

1. **Descompresión:** Se descomprime el archivo con `gzip -d`.
2. **Búsqueda directa de cadenas:** Al ejecutar `strings` sobre la imagen `disko-1.dd` y filtrar por el prefijo `academy{`, se extrae la flag directamente sin necesidad de montar la partición ni parsear estructuras complejas del sistema de archivos.

```bash
# 1. Descomprimir imagen
gzip -d disko-1.dd.gz

# 2. Buscar flag con strings
strings disko-1.dd | grep -i "academy{"
```

## Notas adicionales
- El análisis rápido de cadenas legibles (`strings`) es siempre uno de los primeros pasos de triage en análisis forense digital (DFIR) antes de proceder a técnicas más complejas de *carving* o reconstrucción de sistemas de archivos.

## Referencias
- Reto: https://learn.cylabacademy.org/library/505
- GNU Strings Manual: https://sourceware.org/binutils/docs/binutils/strings.html
