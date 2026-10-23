# Forensics — Enhance!

## Descripción
> **Prompt oficial del reto:** "Download this image file and find the flag.
> - [Download image file](https://challenge-files.cylabacademy.net/library/e64e2668a8f34ef7ddcbdd713ba52720a8804ff3a0914677983d29a4b48c3e6a/drawing.flag.svg)"
>
> **Hints:** Ninguna

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona un archivo gráfico vectorial `drawing.flag.svg`. Al abrir la imagen en un navegador o visor SVG se observan círculos concéntricos que invitan a hacer "zoom" progresivo hacia el punto central.

1. **Estructura del archivo SVG:**
   - Dado que los archivos SVG son documentos XML en texto plano, no es necesario realizar zoom visual manual.
   - Al inspeccionar el contenido XML del archivo con un editor de texto o mediante expresiones regulares, se encuentran múltiples etiquetas `<tspan>` dentro de elementos `<text>`.

2. **Extracción y concatenación:**
   - Los caracteres individuales de la flag están distribuidos secuencialmente a través de varios elementos `<tspan>`:
     `a c a d e m y { 3 n h 4 n c 3 d _ 9 f 3 1 c 0 4 b }`
   - Concatenando el texto de todas las etiquetas `<tspan>` se reconstruye directamente la flag completa.

```bash
# Extracción rápida con grep y expresiones regulares
grep -oE '<tspan[^>]*>[^<]+</tspan>' drawing.flag.svg | sed -e 's/<[^>]*>//g' | tr -d ' \n'

# O mediante un script de Python
python3 -c "
import re
with open('drawing.flag.svg') as f:
    tspans = re.findall(r'<tspan[^>]*>(.*?)</tspan>', f.read())
print(''.join(tspans).replace(' ', ''))
"
```

## Notas adicionales
- El formato SVG (Scalable Vector Graphics) admite texto incrustado, transformaciones geométricas y animaciones mediante etiquetas XML legibles. La fragmentación de cadenas en múltiples subelementos de texto es un método común de ocultación simple en retos de esteganografía vectorial.

## Referencias
- Reto: https://learn.cylabacademy.org/library/265
- SVG Specification (W3C): https://www.w3.org/TR/SVG2/
