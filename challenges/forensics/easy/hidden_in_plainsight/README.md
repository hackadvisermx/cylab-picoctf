# Forensics — Hidden in plainsight

## Descripción
> **Prompt oficial del reto:** "You’re given a seemingly ordinary JPG image. Something is tucked away out of sight inside the file. Your task is to discover the hidden payload and extract the flag.
> Download the jpg image [here](https://challenge-files.cylabacademy.net/library/90fe779e0989ed7c80652fdd2b165f9661a7a00ba75fc766d01cd4c0e489fdbd/img.jpg)."
>
> **Hints:**
> 1. Download the jpg image and read its metadata

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoMini by CMU-Africa
- **Autor:** Yahaya Meddy

## Solución
El reto presenta una imagen JPEG llamada `img.jpg` con datos esteganográficos ocultos.

1. **Lectura de metadatos:** Al examinar la imagen con `exiftool` o `strings`, se observa una entrada en el campo `Comment`:
   `c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9`
2. **Decodificación de pistas:**
   - Decodificando `c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9` en Base64 se obtiene:
     `steghide:cEF6endvcmQ=`
   - La cadena indica el uso de la herramienta `steghide` y una contraseña codificada en Base64 (`cEF6endvcmQ=`).
   - Decodificando `cEF6endvcmQ=` en Base64 se obtiene la contraseña en texto plano: `pAzzword`.
3. **Extracción esteganográfica:**
   - Usando `steghide` con la contraseña extraída, se extrae el archivo incrustado `hidden_flag.txt`.
   - El contenido de `hidden_flag.txt` contiene la flag.

```bash
# 1. Inspeccionar metadatos
exiftool img.jpg | grep -i comment
# Comment                         : c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9

# 2. Decodificar pista y credencial
echo "c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9" | base64 -d
# steghide:cEF6endvcmQ=

echo "cEF6endvcmQ=" | base64 -d
# pAzzword

# 3. Extraer contenido oculto mediante steghide
steghide extract -sf img.jpg -p pAzzword -xf hidden_flag.txt

# 4. Leer la flag
cat hidden_flag.txt
```

## Notas adicionales
- `steghide` es una herramienta clásica de esteganografía para formatos JPEG, BMP, WAV y AU que utiliza algoritmos basados en teoría de grafos y cifrado para ocultar información sin alterar apreciablemente la apariencia o tamaño del archivo portador.

## Referencias
- Reto: https://learn.cylabacademy.org/library/524
- Steghide Manual: http://steghide.sourceforge.net/documentation/manpage.php
