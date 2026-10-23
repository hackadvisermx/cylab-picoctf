# Cryptography — Pixelated

## Descripción

> **Prompt oficial del reto:** "I have these 2 images, can you make a flag out of them?
> scrambled1.png scrambled2.png"

> **Hints:**
> 1. [https://en.wikipedia.org/wiki/Visual_cryptography](https://en.wikipedia.org/wiki/Visual_cryptography)
> 2. Think of different ways you can "stack" images

- **Categoría:** Cryptography
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Sara

## Solución

El reto entrega dos imágenes PNG aparentemente aleatorias (`scrambled1.png` y `scrambled2.png`) de 256×256 píxeles. Ambas pistas apuntan a **criptografía visual** (*Visual Cryptography*), una técnica donde una imagen secreta se divide en capas que revelan el mensaje cuando se superponen o combinan aritméticamente.

### Análisis y combinación de capas

En criptografía visual digital, las dos capas suelen combinarse mediante suma modular de canales de color:
$$\text{Pixel}_{\text{final}}(x, y) = (\text{Pixel}_1(x, y) + \text{Pixel}_2(x, y)) \bmod 256$$

Al sumar los valores RGB de ambas imágenes componente por componente módulo 256, los valores de ruido aleatorio de fondo se cancelan o alinean para formar el texto nítido de la flag sobre el fondo.

### Script de resolución

```python
from PIL import Image
import numpy as np

# Cargar ambas imágenes como arreglos numéricos
img1 = np.array(Image.open("scrambled1.png"))
img2 = np.array(Image.open("scrambled2.png"))

# Suma modular canal por canal
res_add = (img1.astype(np.uint16) + img2.astype(np.uint16)) % 256
res_img = Image.fromarray(res_add.astype(np.uint8))
res_img.save("combined.png")
```

La imagen resultante `combined.png` contiene el texto legible de la flag, que puede leerse visualmente o mediante OCR (`tesseract combined.png stdout`).

## Referencias

- [Visual Cryptography — Wikipedia](https://en.wikipedia.org/wiki/Visual_cryptography)
- [Pillow (PIL) Image Processing](https://pillow.readthedocs.io/)
