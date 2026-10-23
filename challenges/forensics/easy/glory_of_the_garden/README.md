# Forensics — Glory of the Garden

## Descripción
> **Prompt oficial del reto:** "This file contains more than it seems.
> Get the flag from [garden.jpg](https://challenge-files.cylabacademy.net/library/e78198c6a7dc5e471e8429d4953e7595feafe17764258eec169b8dab8bb3c925/garden.jpg)."
>
> **Hints:**
> 1. What is a hex editor?

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2019
- **Autor:** jedavis/Danny

## Solución
El reto suministra una imagen JPEG llamada `garden.jpg`.

1. **Datos al final del archivo (Appended Data / Overlay):**
   - Las imágenes JPEG terminan normalmente con el marcador EOI (*End of Image*): `FF D9`.
   - Sin embargo, datos añadidos después del marcador `FF D9` son ignorados por la mayoría de visores de imágenes pero permanecen en el archivo físico.
   - Ejecutando `strings` sobre la imagen o visualizando el archivo con un visor hexadecimal (`xxd`), se localiza la cadena de texto plano adjunta al final del archivo.

```bash
# Búsqueda directa de la flag con strings
strings garden.jpg | grep -i "academy{"
# Here is a flag: academy{...}
```

## Notas adicionales
- El *file appending* o datos tras el EOF es la forma más elemental de ocultación de datos en esteganografía. Se detecta de inmediato comparando el tamaño reportado en la estructura del archivo con el tamaño real en disco, o mediante herramientas de análisis de estructura como `binwalk`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/44
- JPEG File Format Specification: https://www.w3.org/Graphics/JPEG/itu-t81.pdf
