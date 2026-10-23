# Forensics — information

## Descripción
> **Prompt oficial del reto:** "Files can always be changed in a secret way. Can you find the flag?
> [cat.jpg](https://challenge-files.cylabacademy.net/library/c585b4adbdaa06f409db7bf5012c2e58e9aab24669764a5f1cf0f9ce0d60dcfd/cat.jpg)"
>
> **Hints:**
> 1. Look at the details of the file
> 2. Make sure to submit the flag as academy{XXXXX}

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2021
- **Autor:** susie

## Solución
El reto suministra una imagen JPEG llamada `cat.jpg`.

1. **Inspección de metadatos:**
   - Al ejecutar `exiftool` sobre la imagen, se examinan los campos EXIF, IPTC y XMP.
   - En el campo `License` aparece una cadena codificada en Base64:
     `YWNhZGVteXt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9`

2. **Decodificación:**
   - Al decodificar el valor Base64 se obtiene directamente la flag.

```bash
# Inspección de metadatos con exiftool
exiftool cat.jpg | grep -i license
# License                         : YWNhZGVteXt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9

# Decodificación Base64
echo "YWNhZGVteXt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9" | base64 -d
```

## Notas adicionales
- Los campos de metadatos de imágenes fotográficas a menudo pasan desapercibidos en revisiones casuales y constituyen un canal común de esteganografía superficial.

## Referencias
- Reto: https://learn.cylabacademy.org/library/186
- ExifTool: https://exiftool.org/
