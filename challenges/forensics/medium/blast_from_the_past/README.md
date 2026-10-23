# Forensics — Blast from the past

## Descripción
> **Prompt oficial del reto:** "The judge for these pictures is a real fan of antiques. Can you age this photo to the specifications?
>
> Set the timestamps on this picture to `1970:01:01 00:00:00.001+00:00` with as much precision as possible for each timestamp. In this example, `+00:00` is a timezone adjustment. Any timezone is acceptable as long as the time is equivalent. As an example, this timestamp is acceptable as well: `1969:12:31 19:00:00.001-05:00`. For timestamps without a timezone adjustment, put them in GMT time (+00:00). The checker program provides the timestamp needed for each.
>
> Use this [picture](https://challenge-files.cylabacademy.net/library/73ebaa71bc2c07d861465efe191d4240b50855fa44894086209fafc2c86929bb/original.jpg)."
>
> **Hints:** "Exiftool is really good at reading metadata, but you might want to use something else to modify it."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2024
- **Autor:** syreal

## Solución
El reto solicita alterar todas las marcas de tiempo (timestamps) de la imagen `original.jpg` para establecerlas exactamente en `1970:01:01 00:00:00.001+00:00` (1 milisegundo después del Unix Epoch). La verificación remota evalúa 7 etiquetas específicas:

1. `IFD0:ModifyDate` -> `1970:01:01 00:00:00`
2. `ExifIFD:DateTimeOriginal` -> `1970:01:01 00:00:00`
3. `ExifIFD:CreateDate` -> `1970:01:01 00:00:00`
4. `Composite:SubSecCreateDate` -> `1970:01:01 00:00:00.001` (requiere `SubSecTimeDigitized=001`)
5. `Composite:SubSecDateTimeOriginal` -> `1970:01:01 00:00:00.001` (requiere `SubSecTimeOriginal=001`)
6. `Composite:SubSecModifyDate` -> `1970:01:01 00:00:00.001` (requiere `SubSecTime=001`)
7. `Samsung:TimeStamp` -> `1970:01:01 00:00:00.001+00:00`

### Paso 1: Modificación de metadatos estándar con ExifTool
Las primeras 6 etiquetas pertenecen a la estructura estándar EXIF y pueden ajustarse mediante `exiftool`, definiendo tanto la fecha base como los submilisegundos y las zonas horarias (+00:00):

```bash
exiftool "-AllDates=1970:01:01 00:00:00" \
         "-DateTimeOriginal=1970:01:01 00:00:00" \
         "-CreateDate=1970:01:01 00:00:00" \
         "-ModifyDate=1970:01:01 00:00:00" \
         "-SubSecTime=001" \
         "-SubSecTimeOriginal=001" \
         "-SubSecTimeDigitized=001" \
         "-OffsetTime=+00:00" \
         "-OffsetTimeOriginal=+00:00" \
         "-OffsetTimeDigitized=+00:00" \
         original.jpg -overwrite_original
```

### Paso 2: Modificación de la marca propietaria (Samsung Trailer)
La séptima verificación evalúa la marca propietaria de Samsung (`Samsung:TimeStamp`), que `exiftool` no edita directamente por estar en el trailer binario final del archivo JPEG (`Image_UTC_Data`).
Al inspeccionar el final del archivo con un editor hexadecimal o Python, se encuentra una cadena ASCII de 13 dígitos que representa los milisegundos desde el epoch: `1700513181420`.
Para representar 1 ms después del epoch (`1970-01-01 00:00:00.001 UTC`), el valor numérico es `1`. Manteniendo la longitud original de 13 bytes en ASCII para preservar la alineación del trailer, se reemplaza por `0000000000001`:

```python
with open("original.jpg", "rb") as f:
    data = f.read()

# Reemplazar la marca de 13 dígitos del trailer Samsung
data = data.replace(b"1700513181420", b"0000000000001")

with open("original_modified.jpg", "wb") as f:
    f.write(data)
```

### Paso 3: Envío y verificación en el servidor remoto
El reto proporciona dos puertos: uno para cargar la imagen mediante `netcat` y otro para ejecutar el validador automático:

```bash
# 1. Enviar imagen modificada
nc -w 2 chatelaine.cylabacademy.net <PORT_UPLOAD> < original_modified.jpg

# 2. Consultar el verificador
nc chatelaine.cylabacademy.net <PORT_CHECK>
```

El validador analiza las 7 etiquetas, confirma que todas coinciden con el epoch + 1 ms, y devuelve la flag: `academy{...}`.

## Notas adicionales
- Las especificaciones EXIF almacenan la precisión subsegundo en etiquetas separadas (`SubSecTime*`) que las bibliotecas compuestas combinan con las fechas principales.
- Muchos fabricantes móviles (Samsung, Google, Apple) adjuntan bloques de metadatos propietarios al final de los archivos JPEG después del marcador `FF D9` (EOI). Si las herramientas convencionales no admiten escritura para estas estructuras, es necesario recurrir a edición binaria directa.

## Referencias
- Reto: https://learn.cylabacademy.org/library/432
- ExifTool Tag Names (EXIF & MakerNotes): https://exiftool.org/TagNames/EXIF.html
- Samsung Trailer Format: https://exiftool.org/TagNames/Samsung.html
