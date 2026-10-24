# Forensics — St3g0

## Descripción
> **Prompt oficial del reto:** "Download this image and find the flag.  
> Download image"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones (ft. djrobin17)

> **Pistas oficiales:**
> 1. We know the end sequence of the message will be `$t3g0`.

## Solución
El reto proporciona una imagen PNG (`academy.flag.png`). El nombre del reto hace referencia directa a la herramienta de análisis esteganográfico `zsteg`.

1. **Análisis con zsteg:**
   Ejecutamos `zsteg` sobre la imagen para inspeccionar los bits menos significativos (LSB) en todos los planos de color:
   ```bash
   zsteg academy.flag.png
   ```

2. **Detección del payload:**
   En el canal `b1,rgb,lsb,xy`, la herramienta detecta texto plano incrustado:
   ```text
   b1,rgb,lsb,xy       .. text: "academy{...}$t3g0"
   ```
   Tal como anticipaba la pista oficial (*"the end sequence of the message will be $t3g0"*), el mensaje finaliza con `$t3g0`, delimitando la bandera contenida dentro de las llaves.

## Notas adicionales
- La esteganografía LSB (*Least Significant Bit*) altera el bit de menor peso de los componentes rojo, verde y azul de cada píxel, introduciendo modificaciones imperceptibles al ojo humano pero detectables mediante análisis estadístico de canales y herramientas como `zsteg`.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/305
- zsteg: https://github.com/zed-0xff/zsteg
