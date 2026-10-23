# morse-code

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2022  
**Plataforma:** CyLab Security Academy  

## Descripción

Morse code is well known. Can you decrypt this?
Download the file [here](https://challenge-files.cylabacademy.net/library/3728bfa4e8314fddd6b7e9f3fae9cb453b459a0bd4b3a29a9224701152f0cd89/morse_chal.wav).

Wrap your answer with academy{}, put underscores in place of pauses, and use all uppercase.

## Hints

1. Audacity is a really good program to analyze morse code audio.

## Solución

El archivo es un WAV mono de ~29 segundos a 44100 Hz que contiene señales de código Morse.

**Paso 1: Analizar la señal de audio**

Se utiliza la librería `wave` de Python y NumPy para detectar las energías del audio en ventanas de 10 ms:

```python
import wave, numpy as np

w = wave.open('morse_chal.wav')
frames = w.readframes(w.getnframes())
w.close()

data = np.frombuffer(frames, dtype=np.int16).astype(float)
sr = 44100
window = int(sr * 0.01)  # 10ms por ventana

energy = np.array([np.sum(data[i:i+window]**2)
                   for i in range(0, len(data)-window, window)])
threshold = np.max(energy) * 0.05
binary = (energy > threshold).astype(int)
```

**Paso 2: Detectar las duraciones de los pulsos**

Las duraciones encontradas (en ventanas de 10 ms) son:
- Señal encendida: 10 (punto) o 30 (raya)
- Señal apagada: 10 (separador intra-letra), 40 (separador de letra), 80 (separador de palabra)

**Paso 3: Decodificar el Morse**

```python
MORSE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6',
    '--...': '7', '---..': '8', '----.': '9'
}

result = ''
current_letter = ''
for val, count in runs:
    if val == 1:
        current_letter += '.' if count <= 15 else '-'
    else:
        if count <= 20:
            pass  # intra-letra
        elif count <= 60:
            result += MORSE.get(current_letter, '?')
            current_letter = ''
        else:
            result += MORSE.get(current_letter, '?')
            current_letter = ''
            result += '_'
```

**Paso 4: Resultado**

El mensaje Morse decodificado es:

```
WH47_H47H_90D_W20U9H7
```

Corresponde a la frase histórica "WHAT HATH GOD WROUGHT" en leet speak — el primer mensaje enviado por telégrafo usando código Morse por Samuel Morse en 1844.

**Flag:** `academy{WH47_H47H_90D_W20U9H7}`

## Referencias

- [Código Morse — Wikipedia](https://es.wikipedia.org/wiki/C%C3%B3digo_Morse)
- [WHAT HATH GOD WROUGHT — Primer telegrama Morse (1844)](https://en.wikipedia.org/wiki/What_hath_God_wrought)
- [Audacity](https://www.audacityteam.org/)
- [picoCTF 2022](https://picoctf.org)
