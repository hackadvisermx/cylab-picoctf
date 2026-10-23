# Forensics — CanYouSee

## Descripción
> **Prompt oficial del reto:** "How about some hide and seek?
> 
> Download this file [here](https://challenge-files.cylabacademy.net/library/db9453955f3bd6e863102fd10b5c3b1e6ce0517e7c648b76d86172eed079e028/unknown.zip)."
>
> **Hints:**
> 1. How can you view the information about the picture?
> 2. If something isn't in the expected form, maybe it deserves attention?

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Mubarak Mikail

## Solución
El reto suministra un archivo comprimido `unknown.zip` que al descomprimirse produce una imagen JPEG de alta resolución `ukn_reality.jpg`.

1. **Lectura de metadatos:**
   - La pista sugiere examinar la información de la imagen. Al ejecutar `exiftool` sobre `ukn_reality.jpg`, se revisan los distintos campos de metadatos estándar y extendidos (XMP).
   - En el campo `Attribution URL`, en lugar de un enlace web convencional, se observa una cadena codificada en Base64:
     `YWNhZGVteXtNRTc0RDQ3QV9ISUREM05fYTgxZDk0MzF9Cg==`

2. **Decodificación:**
   - Al decodificar el valor Base64 se obtiene directamente la flag.

```bash
# 1. Descomprimir el archivo
unzip unknown.zip

# 2. Inspeccionar metadatos con exiftool
exiftool ukn_reality.jpg | grep -i "attribution"
# Attribution URL                 : YWNhZGVteXtNRTc0RDQ3QV9ISUREM05fYTgxZDk0MzF9Cg==

# 3. Decodificar la cadena Base64
echo "YWNhZGVteXtNRTc0RDQ3QV9ISUREM05fYTgxZDk0MzF9Cg==" | base64 -d
```

## Notas adicionales
- Los campos XMP (*Extensible Metadata Platform*) permiten a los programas de edición gráfica incrustar metadatos personalizados o arbitrarios dentro de archivos multimedia. Los analistas deben auditar sistemáticamente todos los esquemas XMP no estándar.

## Referencias
- Reto: https://learn.cylabacademy.org/library/408
- Adobe XMP Specification: https://www.adobe.com/devnet/xmp.html
