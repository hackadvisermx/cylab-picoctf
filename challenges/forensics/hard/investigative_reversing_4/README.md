# Forensics — Investigative Reversing 4

## Descripción
> **Prompt oficial del reto:** "We have recovered a [binary](https://challenge-files.cylabacademy.net/library/b7b4e077cf4cf60f78116fb8a4f9b78e1ea5c283d8b5fd3a367ce41126196bcb/investigative-reversing-4-mystery) and 5 images: [image01](https://challenge-files.cylabacademy.net/library/b7b4e077cf4cf60f78116fb8a4f9b78e1ea5c283d8b5fd3a367ce41126196bcb/Item01_cp.bmp), [image02](https://challenge-files.cylabacademy.net/library/b7b4e077cf4cf60f78116fb8a4f9b78e1ea5c283d8b5fd3a367ce41126196bcb/Item02_cp.bmp), [image03](https://challenge-files.cylabacademy.net/library/b7b4e077cf4cf60f78116fb8a4f9b78e1ea5c283d8b5fd3a367ce41126196bcb/Item03_cp.bmp), [image04](https://challenge-files.cylabacademy.net/library/b7b4e077cf4cf60f78116fb8a4f9b78e1ea5c283d8b5fd3a367ce41126196bcb/Item04_cp.bmp), [image05](https://challenge-files.cylabacademy.net/library/b7b4e077cf4cf60f78116fb8a4f9b78e1ea5c283d8b5fd3a367ce41126196bcb/Item05_cp.bmp). See what you can make of it. There should be a flag somewhere."

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Santiago C/Danny T

## Solución
El reto proporciona un archivo ejecutable ELF de 64 bits (`mystery`) y cinco imágenes en formato BMP (`Item01_cp.bmp` a `Item05_cp.bmp`).

1. **Ingeniería inversa del binario (`mystery`):**
   - La función `main` lee hasta 50 bytes desde `flag.txt` y llama a la función `encodeAll`.
   - `encodeAll` procesa los archivos en orden inverso: desde `Item05.bmp` descendiendo hasta `Item01.bmp`, generando los correspondientes `Item0X_cp.bmp`.
   - En `encodeDataInFile`:
     - Se preserva el encabezado BMP copiando los primeros 2019 bytes (`0x7E3`).
     - A continuación, se ejecuta un bucle de 50 pasos (`k` de 0 a 49).
     - Si el índice `k` es divisible entre 5 (`k % 5 == 0`), se codifican los 8 bits del carácter actual de la bandera (`flag[flag_index]`) en el bit menos significativo (LSB) de 8 bytes consecutivos de la imagen de destino mediante la función `codedChar`.
     - Si `k % 5 != 0`, se copia 1 byte directamente sin alterar.
   - De esta manera, cada imagen alberga 10 caracteres de la bandera (5 archivos × 10 caracteres = 50 caracteres en total).

2. **Extracción y reconstrucción con Python:**
   - Se leen las 5 imágenes en orden descendente (`Item05_cp.bmp` a `Item01_cp.bmp`).
   - Tras el offset `2019`, se itera sobre los 50 bloques extrayendo los 8 LSBs de cada bloque con `k % 5 == 0`.

```python
#!/usr/bin/env python3
flag = []
for file_num in [5, 4, 3, 2, 1]:
    filename = f"Item0{file_num}_cp.bmp"
    with open(filename, "rb") as f:
        data = f.read()
    
    offset = 2019
    curr = offset
    for k in range(50):
        if k % 5 == 0:
            char_val = 0
            for b in range(8):
                bit = data[curr] & 1
                char_val |= (bit << b)
                curr += 1
            flag.append(chr(char_val))
        else:
            curr += 1

print("Flag recuperada:", "".join(flag))
```

## Notas adicionales
- Al procesar imágenes esteganográficas con LSB distribuidas entre múltiples archivos, es fundamental verificar el orden exacto de iteración definido en el desensamblado (en este caso decreciente: 5 a 1).

## Referencias
- Reto: https://learn.cylabacademy.org/library/54
- Esteganografía LSB: https://en.wikipedia.org/wiki/Least_significant_bit
