# Forensics — Invisible WORDs

## Descripción
> **Prompt oficial del reto:** "Do you recognize this cyberpunk baddie? We don't either. AI art generators are all the rage nowadays, which makes it hard to get a reliable known cover image. But we know you'll figure it out. The suspect is believed to be trafficking in classics. That probably won't help crack the stego, but we hope it will give motivation to bring this criminal to justice! Download the image [here](https://challenge-files.cylabacademy.net/library/43bb511b308e00a17d1a3e2620926dc364ad802286313809599bc6bb95e178a1/output.bmp)"
>
> **Hints:**
> 1. Something doesn't quite add up with this image...
> 2. How's the image quality?

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona un archivo de imagen BMP (`output.bmp`) de 32 bits por píxel (960×540, 4 bytes por píxel).

1. **Análisis de canales y esteganografía en palabras (*WORDs*):**
   - El título del reto enfatiza la palabra **WORD** (entero de 16 bits / 2 bytes en arquitectura informática).
   - Al inspeccionar los planos de bits y canales de color, se observa que los bytes correspondientes a los canales menos significativos contienen un patrón no aleatorio.
   - En la matriz de píxeles (4 bytes por píxel), cada grupo de 4 bytes alterna 2 bytes de imagen con 2 bytes de datos arbitrarios incrustados.

2. **Extracción y reconstrucción del archivo oculto:**
   - Mediante un script en Python, se recorren los datos de la imagen tomando fragmentos de 2 bytes cada 4 bytes (`data[idx : idx + 2]`).
   - El flujo resultante contiene la firma mágica de un archivo comprimido ZIP (`PK\x03\x04`).
   - Se recorta el flujo desde la firma `PK\x03\x04` hasta el final del directorio central (`PK\x05\x06`), obteniendo un archivo `.zip` válido.
   - Al descomprimir el archivo se extrae un texto clásico de Mary Shelley (*Frankenstein*), dentro del cual se encuentra la bandera incrustada.

```python
#!/usr/bin/env python3

with open("output.bmp", "rb") as f:
    data = f.read()

# Extraer 2 bytes por cada bloque de 4 bytes
out = bytearray()
for idx in range(0, len(data), 4):
    out.extend(data[idx : idx + 2])

# Localizar inicio y fin del archivo ZIP
pk_start = out.find(b"PK\x03\x04")
eocd = out.find(b"PK\x05\x06")

with open("extracted.zip", "wb") as f:
    f.write(out[pk_start : eocd + 22])
```

```bash
# Descomprimir y buscar la bandera en el texto clásico
unzip extracted.zip
grep -riE "academy\{|picoCTF\{" .
```

## Notas adicionales
- Las imágenes de 32 BPP a menudo reservan un canal alfa o padding que puede utilizarse para canalizar flujos de datos sin degradar de manera apreciable los canales visuales principales.

## Referencias
- Reto: https://learn.cylabacademy.org/library/354
- BMP File Format Specification: https://en.wikipedia.org/wiki/BMP_file_format
- ZIP File Format Specification (APPNOTE): https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
