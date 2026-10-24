# Forensics — Pitter, Patter, Platters

## Descripción
> **Prompt oficial del reto:** "'Suspicious' is written all over this disk image. 
> Download [suspicious.dd.sda1](https://challenge-files.cylabacademy.net/library/7bcab7a0c2a5ae68cd09fedcc2495c27deb3044a411252614d10f35388630756/suspicious.dd.sda1)"
>
> **Hints:**
> 1. It may help to analyze this image in multiple ways: as a blob, and as an actual mounted disk.
> 2. Have you heard of slack space? There is a certain set of tools that now come with Ubuntu that I'd recommend for examining that disk space phenomenon...

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2020 Mini-Competition
- **Autor:** syreal

## Solución
El reto provee una imagen forense de partición de disco en formato RAW (`suspicious.dd.sda1`) de aproximadamente 31 MB.

1. **Localización del archivo objetivo y concepto de Slack Space:**
   - Explorando el sistema de archivos (ext3/ext4) se localiza en la raíz el archivo `suspicious-file.txt`.
   - Al inspeccionar su contenido visible, solo muestra una línea inocua:
     `Nothing to see here! But you may want to look here -->`
   - El espacio de holgura de archivo (*File Slack Space*) es la porción de un clúster/bloque asignado a un archivo que queda sin usar entre el final del archivo (*End Of File*, EOF) y el final físico del sector o clúster de disco.

2. **Extracción y decodificación del residuo en Slack Space:**
   - Inspeccionando los bytes directamente posteriores al salto de línea (`\n`) en el bloque que aloja `suspicious-file.txt`, se encuentra una cadena codificada en **UTF-16LE** y en orden invertido (*reversed*):
     `}\x00e\x001\x00e\x001\x00...`
   - Decodificando los caracteres en UTF-16LE e invirtiendo la cadena resultante (`rev`), se recupera la flag completa.

```python
#!/usr/bin/env python3
"""Extracción de slack space en suspicious.dd.sda1"""
with open("suspicious.dd.sda1", "rb") as f:
    data = f.read()

marker = b"Nothing to see here! But you may want to look here -->\n"
pos = data.find(marker)
if pos != -1:
    slack_data = data[pos + len(marker) : pos + len(marker) + 128]
    # Extraer la porción UTF-16LE hasta el relleno nulo
    decoded = slack_data.split(b"\x00\x00\x00\x00")[0].decode("utf-16le")
    # Invertir la cadena
    print("Flag:", decoded[::-1])
```

```bash
# Alternativa con grep e inversión por terminal
strings -e l suspicious.dd.sda1 | grep "ymedaca" | rev
```

## Notas adicionales
- El análisis de *Slack Space* es una de las técnicas periciales esenciales para descubrir fragmentos de información borrada, claves criptográficas o malware que intentan ocultarse en las áreas no controladas por el sistema operativo dentro de clústeres asignados.

## Referencias
- Reto: https://learn.cylabacademy.org/library/87
- File Slack Space Forensics: https://en.wikipedia.org/wiki/Slack_space
