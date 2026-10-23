# Forensics — Binary Digits

## Descripción
> **Prompt oficial del reto:** "This file doesn't look like much... just a bunch of 1s and 0s. But maybe it's not just random noise. Can you recover anything meaningful from this?
> Download the file [here](https://challenge-files.cylabacademy.net/library/6ba8983da0e17a2e2015a530788849e9c9c0bc3393d62fa3f9a06ce8068567c8/digits.bin)."
>
> **Hints:** Ninguna

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
El reto proporciona un archivo llamado `digits.bin` que contiene una secuencia continua de 71,744 caracteres ASCII compuestos exclusivamente por dígitos `0` y `1`.

1. **Interpretación del flujo binario:**
   - La longitud total es de 71,744 bits, lo que equivale exactamente a `71,744 / 8 = 8,968` bytes.
   - Analizando los primeros 10 octetos binarios:
     - `11111111` → `0xFF`
     - `11011000` → `0xD8`
     - `11111111` → `0xFF`
     - `11100000` → `0xE0`
     - `00000000` → `0x00`
     - `00010000` → `0x10`
     - `01001010` → `0x4A` ('J')
     - `01000110` → `0x46` ('F')
     - `01001001` → `0x49` ('I')
     - `01000110` → `0x46` ('F')
   - La secuencia corresponde exactamente a la cabecera JFIF de una imagen JPEG (`FF D8 FF E0 00 10 JFIF`).

2. **Reconstrucción del archivo:**
   - Se agrupan los caracteres de a 8 bits y se convierten a bytes binarios puros, guardando el resultado en `digits_extracted.jpg`.
   - El resultado es una imagen JPEG válida de resolución `800x500`.

3. **Extracción de la flag:**
   - Al visualizar la imagen reconstruida o procesarla mediante OCR / inspección de matriz de píxeles, se lee la flag en formato `academy{...}`.

```bash
# Script de conversión en Python
python3 -c "
with open('digits.bin', 'r') as f:
    bits = f.read().strip().replace(' ', '').replace('\n', '').replace('\r', '')

data = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
with open('digits_extracted.jpg', 'wb') as f:
    f.write(data)
"

# Verificar tipo de archivo generado
file digits_extracted.jpg
# digits_extracted.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 800x500, components 3
```

## Notas adicionales
- Este reto ilustra cómo flujos de datos binarios pueden ser serializados o volcados como representaciones textuales de bits ('0' y '1'), requiriendo únicamente el empaquetado de bits a bytes para recuperar el archivo estructurado original.

## Referencias
- Reto: https://learn.cylabacademy.org/library/698
