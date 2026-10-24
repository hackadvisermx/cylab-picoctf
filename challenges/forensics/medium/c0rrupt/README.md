# Forensics — c0rrupt

## Descripción
> **Prompt oficial del reto:** "We found this [file](https://challenge-files.cylabacademy.net/library/8388ecc430588d15064755583476bec46e23d42a6d8de6e8995c19e40f2e4c58/c0rrupt-mystery). Recover the flag."
>
> **Hints:**
> 1. Try fixing the file header

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny

## Solución
El reto proporciona un archivo sin extensión llamado `c0rrupt-mystery` cuyo comando `file` reporta genéricamente como `data` debido a múltiples corrupciones estructurales.

1. **Reparación de la firma del archivo (PNG Magic Bytes):**
   - Los primeros 8 bytes están alterados (`89 65 4E 34 0D 0A B0 AA`).
   - Se reemplazan por la firma canónica de PNG: `89 50 4E 47 0D 0A 1A 0A`.

2. **Reparación del chunk `IHDR`:**
   - El primer chunk obligatorio de imagen tiene el nombre corrupto `C"DR` (`43 22 44 52`) en el offset `0x0C`.
   - Se restaura al nombre estándar `IHDR` (`49 48 44 52`).

3. **Reparación del chunk `pHYs`:**
   - En el offset `0x42`, el chunk de escala física `pHYs` tiene el primer byte de resolución horizontal alterado a `0xAA` en lugar de `0x00` (`\xaa\x00\x16%\x00\x00\x16%\x01`). Corregir este byte a `0x00` restaura la correspondencia con el CRC calculado del chunk (`0x495224F0`).

4. **Reparación del primer chunk de datos `IDAT`:**
   - En el offset `0x53`, la longitud del chunk está inflada a `\xAA\xAA\xFF\xA5` y su identificador a `\xABDET` en lugar de `IDAT`.
   - La longitud real hasta el siguiente chunk `IDAT` (offset `0x10008`) es de `65,445` bytes (`0x0000FFA5`).
   - Se corrigen los 4 bytes de longitud a `\x00\x00\xFF\xA5` y los 4 bytes del identificador a `IDAT` (`\x49\x44\x41\x54`).

5. **Apertura de la imagen reconstruida:**
   - Tras aplicar los 4 parches estructurales, la imagen se decodifica limpiamente revelando la flag dibujada en pantalla.

```python
#!/usr/bin/env python3
"""Script de reparación binaria para c0rrupt-mystery (PNG corrupto)"""

with open("c0rrupt-mystery", "rb") as f:
    data = bytearray(f.read())

# 1. Cabecera PNG
data[0:8] = b"\x89PNG\r\n\x1a\n"

# 2. Nombre del chunk IHDR
data[12:16] = b"IHDR"

# 3. Primer byte del valor de resolución en pHYs
data[0x46] = 0x00

# 4. Longitud y nombre del primer chunk IDAT
data[0x53:0x57] = b"\x00\x00\xff\xa5"
data[0x57:0x5B] = b"IDAT"

with open("fixed.png", "wb") as f:
    f.write(data)

print("Archivo reparado con éxito como fixed.png")
```

```bash
# Ejecución del script y visualización
python3 repair_png.py
open fixed.png
```

## Notas adicionales
- El formato PNG está diseñado en bloques modulares (*chunks*) donde cada bloque contiene: Longitud (4 bytes) + Tipo/Nombre (4 bytes) + Datos ($N$ bytes) + CRC-32 (4 bytes).
- Herramientas de diagnóstico como `pngcheck` permiten validar la integridad del flujo de chunks y señalar inconsistencias en campos de longitud o sumas de verificación.

## Referencias
- Reto: https://learn.cylabacademy.org/library/53
- W3C PNG Specification: https://www.w3.org/TR/png/
- pngcheck utility: http://www.libpng.org/pub/png/apps/pngcheck.html
