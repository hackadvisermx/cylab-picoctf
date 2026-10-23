# Forensics — endianness-v2

## Descripción
> **Prompt oficial del reto:** "Here's a file that was recovered from a 32-bits system that organized the bytes a weird way. We're not even sure what type of file it is.
>
> Download it [here](https://challenge-files.cylabacademy.net/library/34b04af55ac0dc37f085cf697ec3f4a8153759e9027555b695fc9635dd1296e0/challengefile) and see what you can get out of it"
>
> **Hints:** Ninguna

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** Junias Bonou

## Solución
El reto presenta un archivo binario `challengefile` recuperado de un sistema de 32 bits donde el orden de los bytes se encuentra alterado por la arquitectura del procesador (endianness).

### Paso 1: Inspección de los números mágicos (Magic Bytes)
Al inspeccionar los primeros 16 bytes del archivo con `xxd`:

```bash
xxd -l 16 challengefile
# 00000000: e0ff d8ff 464a 1000 0100 4649 0100 0001  ....FJ....FI....
```

Se pueden deducir los marcadores de una imagen JPEG estándar:
- Una imagen JPEG/JFIF comienza con el marcador SOI (Start of Image) `FF D8` seguido del marcador APP0 `FF E0`. En el archivo aparece como `E0 FF D8 FF`, lo que representa exactamente una inversión de 4 bytes: `[FF D8 FF E0]`.
- Los siguientes 4 bytes en el archivo son `46 4A 10 00`. Invertidos corresponden a `00 10 4A 46` (longitud 0x0010 y las letras `JF`).
- Los 4 bytes subsecuentes son `01 00 46 49`. Invertidos corresponden a `49 46 00 01` (las letras `IF` y la versión 1.01 de JFIF).

Esto confirma que el archivo fue almacenado invirtiendo los bytes de cada palabra de 32 bits (bloques de 4 bytes).

### Paso 2: Reversión del endianness por bloques de 4 bytes
Escribimos un script en Python para leer el binario, invertir cada segmento contiguo de 4 bytes y guardar el resultado como un archivo `.jpg`:

```python
with open("challengefile", "rb") as f:
    data = f.read()

# Invertir cada bloque de 4 bytes (palabra de 32 bits)
recovered = bytearray()
for i in range(0, len(data), 4):
    recovered.extend(data[i:i+4][::-1])

with open("recovered.jpg", "wb") as f:
    f.write(recovered)
```

Al verificar el archivo generado con la utilidad `file`:
```bash
file recovered.jpg
# recovered.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 300x150, components 3
```

### Paso 3: Obtención de la flag
Al abrir la imagen `recovered.jpg` con cualquier visor de imágenes o procesarla mediante OCR (`tesseract recovered.jpg stdout`), se visualiza claramente el texto con la flag del reto: `academy{...}`.

```bash
tesseract recovered.jpg stdout
```

## Notas adicionales
- El concepto de *endianness* define el orden en que una secuencia de bytes se almacena en las direcciones de memoria de la computadora:
  - **Big Endian:** El byte más significativo (MSB) se ubica en la dirección más baja.
  - **Little Endian:** El byte menos significativo (LSB) se ubica en la dirección más baja.
- En arquitecturas de 32 bits, transferir o volcar datos entre procesadores con diferente ordenamiento sin la adecuada conversión causa una permutación periódica de 4 bytes, como se ilustra en este escenario forense.

## Referencias
- Reto: https://learn.cylabacademy.org/library/415
- JPEG File Interchange Format (JFIF): https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format
- Endianness Concepts: https://en.wikipedia.org/wiki/Endianness
