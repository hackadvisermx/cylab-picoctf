# Forensics — Investigative Reversing 0

## Descripción
> **Prompt oficial del reto:** "We have recovered a binary and an image. See what you can make of it. There should be a flag somewhere."

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny Tunitis

## Solución
El reto provee un ejecutable ELF x86-64 (`investigative-reversing-0-mystery`) y una imagen PNG (`investigative-reversing-0-mystery.png`).

Al desensamblar el binario en la función `main`, se analiza la lógica de procesamiento:
1. Abre un archivo con la bandera y lee los primeros 26 bytes (`0x1a`).
2. Abre la imagen PNG en modo de adición (`append`) y concatena los 26 bytes transformados después del final del archivo (justo tras el chunk de fin `IEND` del formato PNG):
   - Bytes 0 al 5: se escriben directamente sin modificación (`flag[0..5]`).
   - Bytes 6 al 14: se les suma 5 antes de escribirse (`flag[i] + 5`).
   - Byte 15: se le resta 3 antes de escribirse (`flag[15] - 3`).
   - Bytes 16 al 25: se escriben directamente sin modificación (`flag[16..25]`).

Para recuperar la bandera original, extraemos los 26 bytes posteriores al marcador `IEND` (4 bytes del identificador `IEND` más 4 bytes del CRC correspondiente) e invertimos las operaciones aritméticas:
- `flag[0..5] = data[0..5]`
- `flag[6..14] = data[6..14] - 5`
- `flag[15] = data[15] + 3`
- `flag[16..25] = data[16..25]`

```bash
# Extracción y decodificación de los bytes anexados al PNG
python3 -c "
with open('investigative-reversing-0-mystery.png', 'rb') as f:
    data = f.read()

# Ubicar el final del chunk IEND
iend_pos = data.find(b'IEND')
trailing = data[iend_pos + 8:]

flag = bytearray(26)
for i in range(6):
    flag[i] = trailing[i]
for i in range(6, 15):
    flag[i] = trailing[i] - 5
flag[15] = trailing[15] + 3
for i in range(16, 26):
    flag[i] = trailing[i]

print('Flag:', flag.decode('latin1'))
"
```

El script reconstruye con éxito la bandera en formato `academy{...}`.

## Notas adicionales
- Los archivos de formato PNG estructuran sus datos en bloques (chunks) delimitados, finalizando obligatoriamente con el chunk `IEND` (`49 45 4E 44 AE 42 60 82`). Los visores estándar de imágenes ignoran cualquier byte colocado con posterioridad a dicho delimitador, convirtiéndolo en un método simple y eficaz de ocultación de datos en análisis forense digital.

## Referencias
- Reto: https://learn.cylabacademy.org/library/70
- Apoyo: http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html
