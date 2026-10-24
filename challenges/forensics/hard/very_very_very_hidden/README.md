# Forensics — Very very very Hidden

## Descripción
> **Prompt oficial del reto:** "Finding a flag may take many steps, but if you look diligently it won't be long until you find the light at the end of the tunnel. Just remember, sometimes you find the hidden treasure, but sometimes you find only a hidden map to the treasure."

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2021
- **Autor:** Sara

## Solución
El reto proporciona una captura de tráfico de red (`try_me.pcap`). La gran mayoría del tráfico está cifrado con TLS/HTTPS, pero al filtrar peticiones HTTP o exportar objetos HTTP descubrimos la descarga de dos imágenes desde una instancia de AWS:
1. `duck.png`
2. `evil_duck.png`

Al comparar ambas imágenes, `evil_duck.png` es considerablemente más pesada que `duck.png` a pesar de tener una calidad visual comprimida o con artefactos, lo que señala la presencia de datos esteganografiados.

Analizando el tráfico DNS y TLS del usuario, se observa que navegó por GitHub y `powershell.org`, apuntando al uso de la herramienta de esteganografía `Invoke-PSImage` (de `peewpw`), la cual incrusta scripts de PowerShell dentro de los 4 bits menos significativos de los canales verde y azul de los píxeles de una imagen PNG (`((b & 0x0F) << 4) | (g & 0x0F)`).

Escribimos un script en Python con `Pillow` para extraer los bytes del script incrustado en `evil_duck.png`:

```python
from PIL import Image

img = Image.open('evil_duck.png').convert('RGB')
width, height = img.size

payload = bytearray()
pixels = img.load()

for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]
        decoded_byte = ((b & 0x0F) << 4) | (g & 0x0F)
        payload.append(decoded_byte)

with open('payload.ps1', 'wb') as f:
    f.write(payload)
```

El script extraído contiene la rutina de descifrado:
```powershell
$out = "flag.txt"
$enc = [system.Text.Encoding]::UTF8
$string1 = "YO[\N\ME(IS_tNE)50uP?^DId_YOu(]E@t*mY_3RD()B2g3l?"
$string2 = "8,:8+14>Fx0l+$*KjVD>[o*.;+1|*[n&2G^201l&,Mv+_'T_B"

$data1 = $enc.GetBytes($string1)
$bytes = $enc.GetBytes($string2)

for($i=0; $i -lt $bytes.count ; $i++)
{
    $bytes[$i] = $bytes[$i] -bxor $data1[$i]
}
[System.IO.File]::WriteAllBytes("$out", $bytes)
```

En PowerShell, las comillas dobles expanden variables internas como `$*` y `$_tNE`. Al evaluar el script en un entorno PowerShell o reconstruir la expansión de variables y la operación XOR correspondiente, se obtiene la bandera con formato `academy{...}`.

```bash
# 1. Extraer objetos HTTP del PCAP
tshark -r try_me.pcap --export-objects http,.

# 2. Decodificar la carga útil esteganográfica de evil_duck.png
python3 -c "
from PIL import Image

img = Image.open('evil_duck.png').convert('RGB')
pixels = img.load()
payload = bytearray()
for y in range(img.height):
    for x in range(img.width):
        r, g, b = pixels[x, y]
        payload.append(((b & 0x0F) << 4) | (g & 0x0F))

with open('payload.ps1', 'wb') as f:
    f.write(payload)
"

# 3. Ejecutar el script en PowerShell para obtener flag.txt
pwsh -File payload.ps1
cat flag.txt
```

## Notas adicionales
- La herramienta `Invoke-PSImage` es comúnmente utilizada en operaciones de red team para eludir detección y evadir inspecciones de contenido en descargas de archivos de imagen aparentemente inofensivos.
- En la adaptación del reto en la plataforma, la cadena base fue adaptada para reflejar el formato `academy{...}` manteniendo el mismo esquema criptográfico y de esteganografía.

## Referencias
- Reto: https://learn.cylabacademy.org/library/141
- Apoyo: https://github.com/peewpw/Invoke-PSImage
