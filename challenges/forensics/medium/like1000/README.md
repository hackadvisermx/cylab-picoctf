# Forensics — like1000

## Descripción
> **Prompt oficial del reto:** "This [.tar file](https://challenge-files.cylabacademy.net/library/0fcc092f4e3d0027bc89f6de85e2b750462dca0a96c5643e38e5825e2da1c3d2/1000.tar) got tarred a lot."
>
> **Hints:**
> 1. Try and script this, it'll save you a lot of time

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny

## Solución
El reto proporciona un archivo comprimido `1000.tar` de aproximadamente 9.8 MB.

1. **Estructura de archivos anidados (*Matryoshka Archive*):**
   - Al descomprimir `1000.tar`, se extrae el archivo `999.tar` junto a un archivo de relleno `filler.txt`.
   - El proceso se repite recursivamente de forma anidada exactamente 1,000 veces (`1000.tar` $\rightarrow$ `999.tar` $\rightarrow \dots \rightarrow$ `1.tar`).
   - La pista recomienda automatizar la extracción mediante un script para evitar hacerlo manualmente.

2. **Automatización de extracción con Python o Bash:**
   - Un script que itere en reversa desde 1000 hasta 1 descomprime sucesivamente cada archivo `.tar` y elimina el anterior para ahorrar espacio.
   - Dentro del último archivo `1.tar` se encuentra `flag.png`, una imagen que dibuja la flag (`academy{...}`).

```python
#!/usr/bin/env python3
"""Extracción automatizada de 1000 archivos TAR anidados"""
import tarfile
import os

curr = 1000
while curr >= 1:
    tar_name = f"{curr}.tar"
    if not os.path.exists(tar_name):
        break
    with tarfile.open(tar_name) as tar:
        tar.extractall()
    os.remove(tar_name)
    curr -= 1

print("Extracción completada. Archivos finales:", os.listdir("."))
```

```bash
# Alternativa en Bash puro
for i in $(seq 1000 -1 1); do
    tar -xf "${i}.tar"
    rm -f "${i}.tar"
done

# Leer el texto de la imagen resultante
tesseract flag.png stdout
```

## Notas adicionales
- Los archivos recursivos o bombas de descompresión (*zip bombs* / *tar bombs*) son vectores de denegación de servicio (DoS) comunes en servicios que descomprimen archivos subidos por usuarios de manera desatendida.
- En este caso, el reto simula una estructura de capas tipo muñeca rusa (Matryoshka) benigna que requiere scripting básico para su resolución.

## Referencias
- Reto: https://learn.cylabacademy.org/library/81
- Python tarfile module: https://docs.python.org/3/library/tarfile.html
