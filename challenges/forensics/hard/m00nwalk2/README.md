# Forensics — m00nwalk2

## Descripción
> **Prompt oficial del reto:** "Revisit the last transmission. We think this [transmission](https://challenge-files.cylabacademy.net/library/56d435f22572b90779f8dfb64b63981437fd3eeaf53fdf0bb58227bd4adc541a/message.wav) contains a hidden message. There are also some clues [clue 1](https://challenge-files.cylabacademy.net/library/56d435f22572b90779f8dfb64b63981437fd3eeaf53fdf0bb58227bd4adc541a/clue1.wav), [clue 2](https://challenge-files.cylabacademy.net/library/56d435f22572b90779f8dfb64b63981437fd3eeaf53fdf0bb58227bd4adc541a/clue2.wav), [clue 3](https://challenge-files.cylabacademy.net/library/56d435f22572b90779f8dfb64b63981437fd3eeaf53fdf0bb58227bd4adc541a/clue3.wav)."
>
> **Hints:**
> 1. Use the clues to extract the another flag from the .wav file

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Joon

## Solución
El reto proporciona cuatro archivos de audio WAV: `message.wav` (la transmisión principal) y tres pistas: `clue1.wav`, `clue2.wav` y `clue3.wav`.

1. **Decodificación de las pistas SSTV:**
   - Al igual que en el reto precedente (`m00nwalk`), las pistas son transmisiones de televisión de barrido lento (**SSTV**).
   - Al decodificar los archivos `clue1.wav`, `clue2.wav` y `clue3.wav` con un receptor SSTV (como QSSTV o el módulo Python `sstv`), se obtienen imágenes que hacen referencia a la herramienta de esteganografía de audio **steghide** y proporcionan una contraseña oculta (`hidden_stegosaurus`).

2. **Extracción esteganográfica con Steghide:**
   - La transmisión principal `message.wav` contiene una carga útil oculta incrustada en las muestras de audio mediante el algoritmo de incrustación de Steghide.
   - Utilizando la clave recuperada de las imágenes SSTV, se extrae el archivo de texto oculto (`steganopayload.txt`), el cual contiene la bandera.

```bash
# 1. Decodificar las pistas SSTV con Python para revelar las pistas y la contraseña
python3 -m sstv -d clue1.wav -o clue1.png
python3 -m sstv -d clue2.wav -o clue2.png
python3 -m sstv -d clue3.wav -o clue3.png

# 2. Extraer el archivo oculto en el audio con steghide
steghide extract -sf message.wav -p hidden_stegosaurus

# 3. Leer la bandera del archivo extraído
cat steganopayload*.txt
```

## Notas adicionales
- Steghide utiliza un algoritmo gráfico de correspondencia ponderada que altera de manera imperceptible los coeficientes de frecuencia y las muestras de audio/imagen.

## Referencias
- Reto: https://learn.cylabacademy.org/library/28
- Steghide Documentation: https://steghide.sourceforge.net/documentation.php
