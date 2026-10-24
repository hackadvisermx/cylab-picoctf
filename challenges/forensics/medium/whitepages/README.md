# Forensics — WhitePages

## Descripción
> **Prompt oficial del reto:** "I stopped using YellowPages and moved onto WhitePages... but [the page they gave me](https://challenge-files.cylabacademy.net/library/164023ae7e53a7b325e50a82f7cd942427fd0f38084d555c162501500fc475c3/whitepages.txt) is all blank!"
>
> **Hints:**
> 1. There is data encoded somewhere... there might be an online decoder.

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** John Hammond

## Solución
El reto proporciona un archivo de texto llamado `whitepages.txt` que al abrirse parece estar completamente en blanco.

1. **Inspección de bytes y esteganografía de espacios en blanco (Whitespace Steganography):**
   - Al analizar los bytes binarios del archivo con Python o un visor hexadecimal, se observa que no está vacío; contiene 2,770 bytes compuestos exclusivamente por dos tipos de caracteres en blanco:
     - Espacios estándar ASCII (`0x20` / ` `)
     - Espacios largos Unicode *EM SPACE* (`U+2003`, representados en UTF-8 como la secuencia de bytes `\xe2\x80\x83`)
   - Hay exactamente 559 espacios ASCII y 737 espacios EM SPACE, sumando un total de 1,296 caracteres. Como $1296 / 8 = 162$, esto equivale exactamente a 162 bytes alineados en grupos de 8 bits.

2. **Decodificación binaria:**
   - Mapeando los espacios en blanco a dígitos binarios:
     - `\xe2\x80\x83` (EM SPACE) $\rightarrow$ `0`
     - `0x20` (ASCII SPACE) $\rightarrow$ `1`
   - Agrupando de 8 en 8 bits para formar caracteres ASCII se obtiene el texto plano subyacente con la flag.

```python
#!/usr/bin/env python3
"""Decodificador de esteganografía de espacios en blanco en whitepages.txt"""
with open("whitepages.txt", "rb") as f:
    raw = f.read()

# Mapeo: EM SPACE -> 0, ASCII space -> 1
bits = raw.replace(b"\xe2\x80\x83", b"0").replace(b" ", b"1").decode()

# Conversión de bits a texto ASCII
decoded_bytes = bytearray()
for i in range(0, len(bits), 8):
    chunk = bits[i:i+8]
    if len(chunk) == 8:
        decoded_bytes.append(int(chunk, 2))

print(decoded_bytes.decode(errors="ignore"))
```

```bash
# Ejecución del script
python3 solve_whitepages.py
```

## Notas adicionales
- La esteganografía en espacios en blanco (*Whitespace steganography*) utiliza caracteres invisibles al ojo humano (espacios simples, tabulaciones, caracteres de espacio de ancho cero o diferentes variantes Unicode de espacios) para codificar información sin alterar la apariencia visual del documento renderizado.

## Referencias
- Reto: https://learn.cylabacademy.org/library/51
- Unicode Space Characters: https://www.unicode.org/charts/PDF/U2000.pdf
