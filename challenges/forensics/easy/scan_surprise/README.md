# Forensics — Scan Surprise

## Descripción
> **Prompt oficial del reto:** "I've gotten bored of handing out flags as text. Wouldn't it be cool if they were an image instead?
> 
> You can download the challenge files here:
> - [challenge.zip](https://challenge-files.cylabacademy.net/library/dd59b9740e3ce6a2a25dd2e5eebb59d3d6734cbaef0d41e03b42af73855a97da/challenge.zip)"
>
> **Hints:**
> 1. QR codes are a way of encoding data. While they're most known for storing URLs, they can store other things too.
> 2. Mobile phones have included native QR code scanners in their cameras since version 8 (Oreo) and iOS 11
> 3. If you don't have access to a phone, you can also use zbar-tools to convert an image to text

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Jeffery John

## Solución
El reto suministra un archivo comprimido `challenge.zip` que contiene una imagen llamada `flag.png`.

1. **Identificación del contenido:**
   - La imagen `flag.png` es un código QR bidimensional.

2. **Lectura y decodificación del código QR:**
   - Empleando herramientas de terminal como `zbarimg` (del paquete `zbar-tools`) o librerías de visión por computador como `opencv` en Python, se decodifica el código QR, obteniendo directamente el texto de la flag.

```bash
# Descomprimir archivo
unzip challenge.zip

# Decodificar código QR con zbarimg
zbarimg home/ctf-player/drop-in/flag.png
# QR-Code:academy{...}
```

En Python:
```python
import cv2

detector = cv2.QRCodeDetector()
val, _, _ = detector.detectAndDecode(cv2.imread('home/ctf-player/drop-in/flag.png'))
print('Flag:', val)
```

## Notas adicionales
- Los códigos QR (*Quick Response Code*) emplean corrección de errores basada en códigos Reed-Solomon, permitiendo recuperar información incluso con daño o distorsión parcial de la imagen.

## Referencias
- Reto: https://learn.cylabacademy.org/library/444
- ZBar Bar Code Reader: http://zbar.sourceforge.net/
