# General Skills — repetitions

## Descripción
> **Prompt oficial:** "Can you make the sense of this file? Download the file here." (tag: `base64`)

- **Categoría:** General Skills
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2023
- **Autor:** Theoneste Byagutangaza

## Solución
El archivo (`enc_flag`, adjunto) es Base64 **anidado varias veces** (decodificar el resultado vuelve a dar Base64, repetidamente).

```python
import base64
data = open("enc_flag", "rb").read()
while b"picoCTF{" not in data:
    data = base64.b64decode(data)
print(data)
```

Hicieron falta **6 decodificaciones** sucesivas.

Flag: `picoCTF{base64_n3st3d_dic0d!n8_d0wnl04d3d_3f81f7be}`

## Notas adicionales
- Truco simple pero típico: en vez de adivinar cuántas capas hay, basta con decodificar en bucle hasta que el resultado deje de "parecer" Base64 (o, más simple, hasta que aparezca el patrón `picoCTF{`).

## Referencias
- Reto: https://learn.cylabacademy.org/library/371
- Archivo: `enc_flag` (copia en esta carpeta)
