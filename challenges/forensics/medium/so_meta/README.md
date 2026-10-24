# Forensics — So Meta

## Descripción
> **Prompt oficial del reto:** "Find the flag in this [picture](https://challenge-files.cylabacademy.net/library/8179732d3bcbaaf9dadfc7fe08aa5b7fbf1d3189b0a2dc90eca34dca38a85b4a/pico_img.png)."
>
> **Hints:**
> 1. What does meta mean in the context of files?
> 2. Ever heard of metadata?

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Kevin Cooper/Danny

## Solución
El reto proporciona una imagen PNG de prueba llamada `pico_img.png`. Las pistas indican revisar los metadatos incrustados en el archivo.

1. **Inspección de metadatos:**
   - Usando la herramienta `exiftool` o mediante extracción simple de cadenas legibles con `strings`, se examinan los campos EXIF / metadatos de la imagen.
   - El campo de metadatos `Artist` contiene directamente la flag en texto claro.

```bash
# Método 1: Inspeccionar metadatos con exiftool
exiftool pico_img.png | grep -i "Artist"

# Método 2: Búsqueda rápida de cadenas con strings
strings pico_img.png | grep -E "academy\{|picoCTF\{"
```

## Notas adicionales
- Los metadatos de imágenes (EXIF, IPTC, XMP) con frecuencia contienen datos sensibles inadvertidamente expuestos como información del autor, cámara, coordenadas GPS o software de edición.
- En análisis forense, la extracción de metadatos es una de las primeras fases de triage al procesar evidencia multimedia.

## Referencias
- Reto: https://learn.cylabacademy.org/library/19
- ExifTool documentation: https://exiftool.org/
