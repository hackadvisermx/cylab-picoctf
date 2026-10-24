# Forensics — Investigative Reversing 3

## Descripción
> **Prompt oficial del reto:** "We have recovered a binary and an image See what you can make of it. There should be a flag somewhere."

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Santiago C/Danny T

## Solución
El reto proporciona un ejecutable ELF x86-64 (`investigative-reversing-3-mystery`) y una imagen de mapa de bits (`investigative-reversing-3-encoded.bmp`).

Al desensamblar el binario (función `main` y función auxiliar `codedChar`), observamos el siguiente flujo de procesamiento:
1. Omite los primeros `0x2d3` (723) bytes de la cabecera del archivo BMP original.
2. Ejecuta un bucle principal con un contador `i` de `0` a `99` (inclusive, 100 iteraciones):
   - Si `i` es par (`i % 2 == 0`): toma el carácter `flag[i / 2]` y lee 8 bytes consecutivos de la imagen BMP. En cada byte, sustituye el bit menos significativo (LSB) por el bit $b$ correspondiente de `flag[i / 2]` mediante la operación:
     $$\text{bmp\_byte} = (\text{bmp\_byte} \ \& \ \text{0xfe}) \ | \ ((\text{caracter} \gg b) \ \& \ 1)$$
   - Si `i` es impar (`i % 2 == 1`): lee y escribe 1 byte de la imagen BMP sin alterar.
3. El resto del archivo BMP se copia tal cual hasta el final.

Dado que hay 50 iteraciones pares en total ($i = 0, 2, 4, \dots, 98$), la bandera oculta tiene exactamente 50 caracteres.

Para recuperar la bandera, escribimos un script en Python que lea el archivo BMP comenzando en el desplazamiento `0x2d3`, extrayendo los LSBs de los grupos de 8 bytes en las iteraciones pares y saltando 1 byte en las iteraciones impares.

```bash
# Decodificación de la esteganografía LSB en el archivo BMP
python3 -c "
with open('investigative-reversing-3-encoded.bmp', 'rb') as f:
    data = f.read()

offset = 0x2d3
idx = offset
flag_chars = []

for i in range(100):
    if i % 2 == 0:
        c = 0
        for b in range(8):
            bit = data[idx] & 1
            c |= (bit << b)
            idx += 1
        flag_chars.append(chr(c))
    else:
        idx += 1

print('Flag:', ''.join(flag_chars))
"
```

El script imprime la bandera con formato `academy{...}`.

## Notas adicionales
- La técnica utilizada es una variación de esteganografía LSB (*Least Significant Bit*) intercalada, donde un byte de relleno inalterado separa los bloques de 8 bytes codificados para evadir análisis estadísticos simples basados en bloques contiguos homogéneos.
- El desplazamiento inicial de 723 bytes protege la cabecera estándar BMP (BITMAPFILEHEADER y BITMAPINFOHEADER) para evitar que la imagen se corrompa al ser visualizada.

## Referencias
- Reto: https://learn.cylabacademy.org/library/83
- Apoyo: https://en.wikipedia.org/wiki/Steganography#Least_significant_bit
