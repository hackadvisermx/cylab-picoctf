# Forensics — Surfing the Waves

## Descripción
> **Prompt oficial del reto:** "While you're going through the FBI's servers, you stumble across their incredible taste in music. One you found is particularly interesting, see if you can find the flag!"

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** William Batista

## Solución
El reto proporciona un archivo de audio WAV mono de 16 bits PCM (`main.wav`). Al inspeccionar las muestras de audio o graficarlas, no se aprecia música ordinaria ni voz, sino un patrón de amplitudes discretas que oscilan entre 1000 y 8500 con una pequeña cantidad de ruido aleatorio.

La diferencia de amplitudes corresponde a 16 niveles cuantizados con un paso de 500 unidades:
$$\text{valor} = \left\lfloor \frac{s - 1000}{500} \right\rfloor$$

Cada muestra mapea exactamente a un dígito hexadecimal entre $0$ y $15$ ($0\text{x}0$ a $0\text{x}F$).
Concatenando cada uno de estos nibbles hexadecimales en orden cronológico y decodificando la secuencia de bytes resultante, obtenemos el script original en Python (`generate_wav.py`) que fue utilizado para generar el archivo de audio.

Al final del script recuperado se encuentra un comentario con la bandera de la plataforma:
`# Your ears have been blessed# academy{...}`

```bash
# Script de extracción y decodificación de las muestras del audio WAV
python3 -c "
import wave, struct

with wave.open('main.wav', 'rb') as w:
    nframes = w.getnframes()
    samples = struct.unpack(f'<{nframes}h', w.readframes(nframes))

# Normalizar y convertir las muestras a dígitos hexadecimales
vals = [(s - 1000) // 500 for s in samples]
hex_str = ''.join(hex(v)[2:] for v in vals)

# Convertir hex a texto ASCII y extraer la flag
decoded = bytes.fromhex(hex_str).decode('utf-8', errors='ignore')
for line in decoded.splitlines():
    if 'academy{' in line or 'picoCTF{' in line:
        print(line)
"
```

## Notas adicionales
- El archivo contiene 2736 muestras correspondientes exactamente a los 2736 caracteres hexadecimales del código fuente de `generate_wav.py`.
- Cada carácter hexadecimal fue modulado en frecuencias base de 1000 Hz sumando 500 Hz por cada incremento de nivel, junto a una ligera variación artificial para simular ruido analógico.

## Referencias
- Reto: https://learn.cylabacademy.org/library/117
- Apoyo: https://docs.python.org/3/library/wave.html
