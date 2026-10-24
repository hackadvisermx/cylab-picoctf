# Forensics — m00nwalk

## Descripción
> **Prompt oficial del reto:** "Decode this [message](https://challenge-files.cylabacademy.net/library/d825fde6581b1311eafdd403da1cc96f1f98fe3fe84cd71d850310ebb3908088/message.wav) from the moon."
>
> **Hints:**
> 1. How did pictures from the moon landing get sent back to Earth?
> 2. What is the CMU mascot?, that might help select a RX option

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Joon

## Solución
El reto proporciona un archivo de audio WAV llamado `message.wav` (11 MB) compuesto por tonos y pitidos de modulación en frecuencia.

1. **Identificación de la tecnología de transmisión (SSTV):**
   - La primera pista hace alusión a cómo las misiones Apolo transmitían imágenes desde la Luna a la Tierra: mediante **SSTV** (*Slow-Scan Television*, televisión de barrido lento). SSTV transmite imágenes fijas codificando la luminancia y crominancia de cada línea de píxeles en tonos audibles de frecuencia modulada.
   - La segunda pista señala la mascota de Carnegie Mellon University (CMU): *Scotty the Scottie Dog*, lo que apunta al modo de decodificación SSTV **Scottie 1**.

2. **Decodificación del audio a imagen:**
   - Usando herramientas de radioaficionado y decodificación SSTV (como `sstv` en Python o `qsstv` en Linux), se procesa el archivo de audio con el modo `Scottie 1`.
   - La imagen reconstruida línea por línea revela una imagen de temática lunar con la flag superpuesta en texto.

```bash
# 1. Instalar el decodificador de SSTV en Python (si no está disponible)
pip3 install sstv

# 2. Decodificar el archivo de audio usando el modo Scottie 1
python3 -m sstv -d message.wav -o decoded_flag.png

# 3. Visualizar la imagen decodificada
open decoded_flag.png
```

## Notas adicionales
- SSTV es ampliamente utilizado en radioafición (HF/VHF) y por la Estación Espacial Internacional (ISS) para emitir imágenes conmemorativas.
- Entre los modos más populares se encuentran Martin (Martin 1, Martin 2) y Scottie (Scottie 1, Scottie 2, Scottie DX).

## Referencias
- Reto: https://learn.cylabacademy.org/library/26
- Slow-scan television: https://en.wikipedia.org/wiki/Slow-scan_television
- Python SSTV decoder library: https://github.com/colaclanth/sstv
