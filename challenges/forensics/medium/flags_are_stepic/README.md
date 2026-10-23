# Forensics — flags are stepic

## Descripción
> **Prompt oficial del reto:** "A group of underground hackers might be using this legit site to communicate. Use your forensic techniques to uncover their message"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2025
- **Autor:** Ricky

> **Pistas oficiales:**
> 1. In the country that doesn't exist, the flag persists

## Solución
El reto despliega un servicio web que contiene una galería con banderas de 246 países del mundo.

1. **Identificación del país no existente:**
   La pista oficial indica: *"In the country that doesn't exist, the flag persists"*.
   Inspeccionando el código HTML/JavaScript de la página (`index.html`), se analiza la lista de banderas asociadas a los países:
   ```html
   { name: "United States of America (the)", img: "flags/us.png" },
   { name: "Upanzi, Republic The", img: "flags/upz.png" },
   { name: "Uruguay", img: "flags/uy.png" }
   ```
   *Upanzi* es un país ficticio utilizado en ejercicios y competencias de ciberseguridad. Su bandera se encuentra alojada en `/flags/upz.png`.

2. **Descarga de la imagen de Upanzi:**
   ```bash
   curl -O http://<instancia>/flags/upz.png
   file upz.png
   # upz.png: PNG image data, 14173 x 10630, 8-bit/color RGBA
   ```

3. **Extracción con Stepic:**
   El título del reto hace un juego de palabras directo con la herramienta de esteganografía en Python llamada `stepic`.
   Instalamos la librería y ejecutamos la extracción sobre los píxeles de la imagen:
   ```python
   import stepic
   from PIL import Image

   # Permitir imágenes de gran resolución
   Image.MAX_IMAGE_PIXELS = None

   im = Image.open("upz.png")
   data = stepic.decode(im)
   print("Flag:", data)
   ```
   La función `stepic.decode()` recupera los bytes ocultos en el canal LSB de la imagen, revelando la bandera de la academia.

## Notas adicionales
- `stepic` codifica bytes ocultos en los bits menos significativos de los canales RGB de la imagen PNG. Para imágenes gigantescas, PIL puede generar un aviso de `DecompressionBombWarning`, el cual se controla ajustando `Image.MAX_IMAGE_PIXELS`.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/481
- Stepic (Python Steganography): https://github.com/dominictarr/stepic
