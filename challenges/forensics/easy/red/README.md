# Forensics — RED

## Descripción
> **Prompt oficial del reto:** "RED, RED, RED, RED
> Download the image: [red.png](https://challenge-files.cylabacademy.net/library/fefcf06050d98347e1585e5cb9f2940967f82e0b89c591966473c752de9f3aba/red.png)"
>
> **Hints:**
> 1. The picture seems pure, but is it though?
> 2. Red?Ged?Bed?Aed?
> 3. Check whatever Facebook is called now.

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2025
- **Autor:** Shuailin Pan (LeConjuror)

## Solución
El reto presenta una imagen PNG roja de 128x128 píxeles llamada `red.png`. Las pistas hacen alusión a los canales de color (Red, Green, Blue, Alpha) y a "Meta" (metadatos / esteganografía LSB en los canales de la imagen).

1. **Análisis de planos de bits (LSB):**
   - Empleando la herramienta de esteganografía para imágenes PNG `zsteg`, se analizan los bits menos significativos (LSB) de todos los canales.
   - En el canal `b1,rgba,lsb,xy`, se detecta una cadena repetida codificada en Base64:
     `YWNhZGVteXtyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==`

2. **Decodificación de la flag:**
   - Decodificando dicha cadena Base64 se obtiene directamente la flag en formato `academy{...}`.

```bash
# 1. Analizar imagen con zsteg
zsteg red.png | grep -i "YWNh"
# b1,rgba,lsb,xy      .. text: "YWNhZGVteXtyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==..."

# 2. Decodificar la cadena Base64
echo "YWNhZGVteXtyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==" | base64 -d
```

## Notas adicionales
- La esteganografía LSB (*Least Significant Bit*) en imágenes RGBA modifica los bits de menor peso visual para insertar datos ocultos sin producir cambios perceptibles al ojo humano.

## Referencias
- Reto: https://learn.cylabacademy.org/library/460
- zsteg: https://github.com/zed-0xff/zsteg
