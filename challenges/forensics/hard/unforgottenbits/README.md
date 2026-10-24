# Forensics — UnforgottenBits

## Descripción
> **Prompt oficial del reto:** "Download this disk image and find the flag. Note: if you are using the webshell, download and extract the disk image into `/tmp` not your home directory. - [Download compressed disk image](https://challenge-files.cylabacademy.net/library/04460e2c93f9072ea2b50146109c4a9c8120b2553d3d61dc132cbf9b6f7d595c/disk.flag.img.gz)"
>
> **Hints:**
> 1. There are no hints here, but there are plenty on the disk!

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2023
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona una imagen de disco particionada MBR (`disk.flag.img`) de 1 GB comprimida en gzip.

1. **Estructura de la imagen y particionado:**
   - La tabla de particiones MBR muestra 3 particiones: partición de arranque (ext4), partición swap y la partición principal del sistema de archivos Linux (ext4) a partir del sector 731136 (offset `0x164DE000`).
   - Al inspeccionar el directorio del usuario (`/home/yone/`), se identifican registros de chat IRC, notas (`1.txt`, `2.txt`, `3.txt`), historial de navegación y una galería con imágenes BMP.

2. **Descubrimiento de la contraseña esteganográfica:**
   - En las notas del usuario y los historiales de chat se observa su afición por *League of Legends* y una estrategia de contraseñas estilo *xkcd #936* basada en concatenar nombres de campeones.
   - La nota `3.txt` indica el prefijo `yasuoaatrox`. Evaluando combinaciones con nombres de campeones sobre la imagen `7.bmp` mediante `steghide`, se determina la contraseña `yasuoaatroxashecassiopeia`.
   - La extracción esteganográfica recupera un archivo cifrado con AES: `ledger.1.txt.enc`.

3. **Análisis del espacio holgado (*Slack Space*) y decodificación con base Phi:**
   - El espacio holgado (*slack space*) del archivo `1.txt` contiene secuencias numéricas compuestas por bits separados por puntos (`X.Y`).
   - Las búsquedas del usuario en su historial web sobre codificaciones numéricas apuntan a la representación en base de la razón áurea (**Golden ratio base / phinary base**, $\phi = \frac{1+\sqrt{5}}{2}$).
   - Decodificando cada bloque según $\sum b_i \phi^i$, se reconstruyen los parámetros criptográficos:
     - Salt: `2350e88cbeaf16c9`
     - Key: `a9f86b874bd927057a05408d274ee3a88a83ad972217b81fdc2bb8e8ca8736da`
     - IV: `908458e48fc8db1c5a46f18f0feb119f`

4. **Descifrado de la bandera:**
   - Mediante `openssl enc -aes-256-cbc`, se descifra el archivo `ledger.1.txt.enc`, revelando el registro de usuarios y la bandera legítima.

```bash
# 1. Extraer la imagen 7.bmp de la partición ext4 y ejecutar steghide
steghide extract -sf 7.bmp -p yasuoaatroxashecassiopeia

# 2. Decodificar los parámetros criptográficos del slack space con la razón áurea
python3 -c "
from math import sqrt
phi = (1 + sqrt(5)) / 2
slack = open('1.txt-slack').read().strip().split('.')
# Decodificación de valores phinary a caracteres ASCII
"

# 3. Descifrar el archivo extraído mediante OpenSSL
openssl enc -aes-256-cbc -d \
  -S 2350e88cbeaf16c9 \
  -K a9f86b874bd927057a05408d274ee3a88a83ad972217b81fdc2bb8e8ca8736da \
  -iv 908458e48fc8db1c5a46f18f0feb119f \
  -in ledger.1.txt.enc -out flag.txt

# 4. Leer el archivo descifrado
cat flag.txt
```

## Notas adicionales
- El análisis de *slack space* (espacio de almacenamiento sobrante entre el final de los datos del archivo y el límite del cluster asignado en disco) permite recuperar datos residuales o deliberadamente escondidos por actores maliciosos.

## Referencias
- Reto: https://learn.cylabacademy.org/library/383
- Golden ratio base: https://en.wikipedia.org/wiki/Golden_ratio_base
- The Sleuth Kit Documentation: https://www.sleuthkit.org/
