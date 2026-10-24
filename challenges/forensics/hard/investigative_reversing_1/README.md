# Forensics — Investigative Reversing 1

## Descripción
> **Prompt oficial del reto:** "We have recovered a [binary](https://challenge-files.cylabacademy.net/library/428a45313c06c7d816da8d54d4d0da7708758f1eaec853ddec3d30bcbb0c7c89/investigative-reversing-1-mystery) and a few images: [image](https://challenge-files.cylabacademy.net/library/428a45313c06c7d816da8d54d4d0da7708758f1eaec853ddec3d30bcbb0c7c89/investigative-reversing-1-mystery.png), [image2](https://challenge-files.cylabacademy.net/library/428a45313c06c7d816da8d54d4d0da7708758f1eaec853ddec3d30bcbb0c7c89/investigative-reversing-1-mystery2.png), [image3](https://challenge-files.cylabacademy.net/library/428a45313c06c7d816da8d54d4d0da7708758f1eaec853ddec3d30bcbb0c7c89/investigative-reversing-1-mystery3.png). See what you can make of it. There should be a flag somewhere."
>
> **Hints:**
> 1. Try using some forensics skills on the image
> 2. This problem requires both forensics and reversing skills
> 3. A hex editor may be helpful

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny Tunitis

## Solución
El reto proporciona un archivo binario ELF (`mystery`) y tres imágenes en formato PNG (`mystery.png`, `mystery2.png`, `mystery3.png`).

1. **Análisis Forense de las imágenes PNG:**
   - La especificación PNG define que todo archivo termina formalmente con el chunk `IEND` (`49 45 4E 44 AE 42 60 82`).
   - Al inspeccionar los archivos más allá del chunk `IEND`, se descubren bytes adicionales anexados (*trailing data*):
     - `mystery.png`: 16 bytes.
     - `mystery2.png`: 2 bytes.
     - `mystery3.png`: 8 bytes.
     - Total: 26 bytes (longitud exacta de la bandera).

2. **Ingeniería Inversa del binario (`mystery`):**
   - El desensamblado de la función `main` muestra cómo se distribuyeron y transformaron los caracteres de `flag.txt`:
     - `mystery3.png` recibe `flag[1]`, `flag[2]`, `flag[5]` y el bloque `flag[10..14]`.
     - `mystery2.png` recibe `flag[0] + 21` y `flag[3] + 4`.
     - `mystery.png` recibe `flag[4]`, el bloque `flag[6..9]` y el bloque final `flag[15..25]`.

3. **Reconstrucción de la bandera:**
   - Invirtiendo las operaciones aritméticas para los 2 bytes de `mystery2.png` (`flag[0] = f2[0] - 21`, `flag[3] = f2[1] - 4`) y ordenando los bytes en sus posiciones correspondientes, se recompone la bandera íntegramente.

```python
#!/usr/bin/env python3

def get_trailing(filename):
    with open(filename, "rb") as f:
        data = f.read()
    return data[data.find(b"IEND") + 8:]

f1 = get_trailing("mystery.png")
f2 = get_trailing("mystery2.png")
f3 = get_trailing("mystery3.png")

flag = [None] * 26

# Reconstruir bytes transformados desde mystery2
flag[0] = chr(f2[0] - 21)
flag[3] = chr(f2[1] - 4)

# Posicionar bytes directos desde mystery3
flag[1] = chr(f3[0])
flag[2] = chr(f3[1])
flag[5] = chr(f3[2])
for idx, i in enumerate(range(10, 15)):
    flag[i] = chr(f3[3 + idx])

# Posicionar bytes directos desde mystery1
flag[4] = chr(f1[0])
for idx, i in enumerate(range(6, 10)):
    flag[i] = chr(f1[1 + idx])
for idx, i in enumerate(range(15, 26)):
    flag[i] = chr(f1[5 + idx])

print("Flag reconstruida:", "".join(flag))
```

## Notas adicionales
- Los chunks de datos ubicados después del marcador `IEND` en imágenes PNG son ignorados por los visores de imágenes estándar, constituyendo una técnica común de ocultación forense sencilla.

## Referencias
- Reto: https://learn.cylabacademy.org/library/27
- PNG File Chunk Specification: https://www.w3.org/TR/png/#11IEND
