# Forensics — Flag in Flame

## Descripción
> **Prompt oficial del reto:** "The SOC team discovered a suspiciously large log file after a recent breach. When they opened it, they found an enormous block of encoded text instead of typical logs. Could there be something hidden within? Your mission is to inspect the resulting file and reveal the real purpose of it. The team is relying on your skills to uncover any concealed information within this unusual log.
> Download the encoded data here: [Logs Data](https://challenge-files.cylabacademy.net/library/0246cbed3fe2edb81de38ddfb60f948020c30448c0c21fcd82cee316fb9da111/logs.txt). Be prepared—the file is large, and examining it thoroughly is crucial ."
>
> **Hints:**
> 1. Use `base64` to decode the data and generate the image file.

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoMini by CMU-Africa
- **Autor:** Prince Niyonshuti N.

## Solución
El reto suministra un archivo `logs.txt` que contiene un único bloque de texto codificado en Base64.

1. **Identificación y decodificación de datos:**
   - La cabecera del texto Base64 comienza por `iVBORw0KGgoAAAANSUhEUg...`, lo cual corresponde a la firma mágica de una imagen PNG (`\x89PNG\r\n\x1a\n`).
   - Se decodifica el archivo `logs.txt` mediante Base64 para reconstruir la imagen binaria `flame.png`.

2. **Análisis de la imagen:**
   - Al abrir la imagen reconstruida, se observa una ilustración con una cadena hexadecimal inscrita sobre ella.
   - Mediante reconocimiento óptico de caracteres (OCR) con herramientas como `tesseract` o inspección visual directa, se extrae la secuencia hexadecimal:
     `61636164656D797B666F72656E736963735F616E616C797369735F69735F616D617A696E675F38646264333133337D`
   - La conversión de la cadena hexadecimal a texto ASCII revela la flag en formato `academy{...}`.

```bash
# 1. Decodificar Base64 a archivo PNG
python3 -c "
import base64
with open('logs.txt', 'r') as f:
    raw = base64.b64decode(f.read().strip())
with open('flame.png', 'wb') as f:
    f.write(raw)
"

# 2. Extraer texto mediante OCR con tesseract
tesseract flame.png stdout
# Resultado:
# 61636164656D797B666F72656E736963735F 616E616C797369735F69735F61 6D617A696E675F38646264333133337D

# 3. Decodificar cadena hexadecimal a ASCII
python3 -c "
h = '61636164656D797B666F72656E736963735F616E616C797369735F69735F616D617A696E675F38646264333133337D'
print(bytes.fromhex(h).decode())
"
```

## Notas adicionales
- La exfiltración de información y binarios ocultos como cadenas Base64 dentro de falsos archivos de logs es una técnica recurrente observada en incidentes reales para evadir reglas de detección basadas puramente en extensiones de archivo.

## Referencias
- Reto: https://learn.cylabacademy.org/library/523
- Tesseract OCR: https://github.com/tesseract-ocr/tesseract
