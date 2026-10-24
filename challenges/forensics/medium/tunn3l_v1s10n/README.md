# Forensics — tunn3l v1s10n

## Descripción
> **Prompt oficial del reto:** "We found this file. Recover the flag.
> [tunn3l_v1s10n](https://challenge-files.cylabacademy.net/library/3b5add918cb4cf98fa62ef4e05eb8c55c6c9ae547a939c6be992ee3aa656ee69/tunn3l_v1s10n)"
>
> **Hints:**
> - "Weird that it won't display right..."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Danny

## Solución
El reto proporciona un archivo binario nombrado `tunn3l_v1s10n`. Al inspeccionar sus primeros bytes mediante un editor hexadecimal o la herramienta `file`, se observa que comienza con el número mágico `42 4D` (`BM`), correspondiente a una imagen de mapa de bits (BMP), aunque la cabecera ha sido alterada deliberadamente para impedir su correcta visualización.

### Paso 1: Análisis de la cabecera BMP
La estructura de la cabecera de un archivo BMP estándar (BITMAPINFOHEADER) se define de la siguiente forma:

| Offset | Longitud | Campo | Valor observado / esperado |
|:---:|:---:|:---|:---|
| `0x00` | 2 bytes | Firma de archivo | `42 4D` (`BM`) |
| `0x02` | 4 bytes | Tamaño total del archivo | `2893454` bytes (`8E 26 2C 00`) |
| `0x0A` | 4 bytes | Offset de inicio de píxeles | `54` bytes (`36 00 00 00`) |
| `0x0E` | 4 bytes | Tamaño de cabecera DIB | Corrupto (`BA D0 00 00` $\rightarrow$ debe ser `28 00 00 00` = 40 bytes) |
| `0x12` | 4 bytes | Ancho de imagen (*width*) | `1134` px (`6E 04 00 00`) |
| `0x16` | 4 bytes | Alto de imagen (*height*) | `306` px (`32 01 00 00`) |

Al corregir el tamaño de la cabecera DIB en el offset `0x0E` a `28 00 00 00`, los visores de imágenes logran renderizar el archivo, pero solo se visualiza una imagen falsa (*decoy*).

### Paso 2: Cálculo y corrección de la altura real de la imagen
El tamaño total del archivo es de 2,893,454 bytes. Con una profundidad de color de 24 bpp (3 bytes por píxel):
- Ancho: 1134 píxeles.
- Cada fila requiere $1134 \times 3 = 3402$ bytes. Con el relleno (*padding*) a múltiplos de 4 bytes de la especificación BMP, cada fila mide 3404 bytes.
- Datos de píxeles: $2893454 - 54 = 2893400$ bytes.
- Altura real esperada:
  $$\text{Filas} = \frac{2893400}{3404} = 850\text{ píxeles}$$

En formato little-endian de 4 bytes, $850 = \text{0x00000352}$, representado como los bytes `52 03 00 00`.

### Paso 3: Modificación del binario con Python
Aplicamos los parches necesarios en los offsets correspondientes:

```python
with open("tunn3l_v1s10n", "rb") as f:
    data = bytearray(f.read())

# Corregir tamaño del DIB header (offset 0x0E a 40 bytes)
data[0x0E:0x12] = (40).to_bytes(4, byteorder="little")

# Corregir altura a 850 px (offset 0x16)
data[0x16:0x1A] = (850).to_bytes(4, byteorder="little")

with open("tunn3l_fixed.bmp", "wb") as f:
    f.write(data)
```

Al abrir `tunn3l_fixed.bmp`, la porción superior previamente truncada del lienzo se vuelve visible, revelando la flag grabada en la imagen.

## Notas adicionales
- Las especificaciones de formatos de mapa de bits sin compresión calculan el tamaño de imagen como $\text{alto} \times \text{stride}$. Alterar el campo de altura (*height*) es una técnica clásica de esteganografía forense para ocultar datos debajo o encima del área de renderizado sin alterar el tamaño del archivo en disco.

## Referencias
- BMP File Format Specification: https://en.wikipedia.org/wiki/BMP_file_format
