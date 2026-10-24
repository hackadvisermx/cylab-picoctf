# Forensics — Investigative Reversing 2

## Descripción
> **Prompt oficial del reto:** "We have recovered a [binary](https://challenge-files.cylabacademy.net/library/e23623607ce25c954aa96cecd5e2a839ed5a8aec026cad6b09f1a6c3d11289d2/investigative-reversing-2-mystery) and an [image](https://challenge-files.cylabacademy.net/library/e23623607ce25c954aa96cecd5e2a839ed5a8aec026cad6b09f1a6c3d11289d2/investigative-reversing-2-encoded.bmp) See what you can make of it. There should be a flag somewhere."
>
> **Hints:**
> 1. Try using some forensics skills on the image
> 2. This problem requires both forensics and reversing skills
> 3. What is LSB encoding?

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Santiago C/Danny Tunitis

## Solución
El reto proporciona un archivo ejecutable ELF (`mystery`) y una imagen en formato BMP codificada (`encoded.bmp`).

1. **Ingeniería Inversa del binario (`mystery`):**
   - La función `main` preserva los primeros `0x7D0` bytes (2000 bytes) copiándolos directamente desde el archivo original a la imagen de salida.
   - A partir del offset 2000, itera sobre 50 caracteres del archivo `flag.txt`:
     - Para cada carácter `flag[c]`, le resta 5 unidades: `val = flag[c] - 5`.
     - Llama a `codedChar` 8 veces consecutivas (una para cada bit de `val`, de menor a mayor peso, bit 0 a bit 7).
     - Cada llamada a `codedChar` incrusta el bit correspondiente en el bit menos significativo (LSB) del siguiente byte del archivo BMP: `byte = (byte & 0xFE) | bit`.
   - Por tanto, cada carácter ocupa 8 bytes consecutivos a partir del offset 2000.

2. **Extracción y recuperación con Python:**
   - Se abre `encoded.bmp` y se lee la sección de datos a partir del byte `2000` (`0x7D0`).
   - Para cada bloque de 8 bytes, se reconstruye el entero a partir de sus LSBs y se suma `5` para revertir el desplazamiento inicial.

```python
#!/usr/bin/env python3

with open("encoded.bmp", "rb") as f:
    data = f.read()

offset = 2000 # 0x7D0
flag = []

for c_idx in range(50):
    val = 0
    for b_idx in range(8):
        byte = data[offset + c_idx * 8 + b_idx]
        bit = byte & 1
        val |= (bit << b_idx)
    char_code = (val + 5) & 0xFF
    flag.append(chr(char_code))

print("Flag recuperada:", "".join(flag))
```

## Notas adicionales
- La esteganografía LSB (*Least Significant Bit*) altera el bit de menor peso de los canales de color, produciendo cambios imperceptibles para el ojo humano (una variación de luminancia de apenas 1 unidad sobre 255).

## Referencias
- Reto: https://learn.cylabacademy.org/library/13
- LSB Steganography Concepts: https://en.wikipedia.org/wiki/Steganography
