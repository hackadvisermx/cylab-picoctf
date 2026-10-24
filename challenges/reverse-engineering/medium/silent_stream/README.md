# Reverse Engineering — Silent Stream

## Descripción
> **Prompt oficial del reto:** "We recovered a suspicious packet capture file that seems to contain a transferred file. The sender was kind enough to also share the script they used to encode and send it. Can you reconstruct the original file?
> Download the PCAP file: [here](https://challenge-files.cylabacademy.net/library/84922e0d3e8e6ea6e0bbb78bc51bf9aa23878a636062a77489eda4923ee4058e/packets.pcap). And the sender's encoding [script](https://challenge-files.cylabacademy.net/library/84922e0d3e8e6ea6e0bbb78bc51bf9aa23878a636062a77489eda4923ee4058e/encrypt.py)"
>
> **Pistas oficiales:**
> 1. The encoding script is a clue, focus on what it's doing to each byte before it's sent.
> 2. The flag is hidden inside the file, try reconstructing and opening it.
> 3. Don't rely on everything you see including flag format

- **Categoría:** Reverse Engineering
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
El reto proporciona un archivo de captura de tráfico de red (`packets.pcap`) y un script en Python (`encrypt.py`) que describe el mecanismo de ofuscación aplicado a los bytes del archivo transmitido.

### 1. Análisis del script de cifrado
El script `encrypt.py` contiene la siguiente función de codificación:
```python
def encode_byte(b, key):
    return (b + key) % 256

def simulate_flag_transfer(filename, key=42):
    ...
```
Cada byte $b$ del archivo original fue desplazado sumándole una clave fija $K = 42$ módulo 256. La operación inversa para recuperar el byte original es:
$$b = (c - 42) \pmod{256}$$

### 2. Extracción y reensamblado del flujo TCP
Inspeccionando `packets.pcap` con Wireshark o `tshark`:
- Se identifica un único flujo TCP entre `10.10.10.10:12345` y `10.10.10.11:9000`.
- Se extraen y ordenan los paquetes por número de secuencia TCP para concatenar la totalidad de la carga útil (*payload*).

### 3. Decodificación y reconstrucción del archivo
Se implementa un script en Python para parsear el archivo PCAP, extraer la carga útil TCP en orden secuencial, aplicar la resta modular de 42 y guardar el archivo resultante:

```python
import struct

with open('packets.pcap', 'rb') as f:
    f.read(24) # Salta cabecera global PCAP
    payloads = []
    while True:
        pkt_hdr = f.read(16)
        if not pkt_hdr or len(pkt_hdr) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_hdr)
        pkt_data = f.read(incl_len)
        
        # Parsear Ethernet (14 bytes) -> IPv4 -> TCP
        if struct.unpack('>H', pkt_data[12:14])[0] == 0x0800:
            ihl = (pkt_data[14] & 0x0f) * 4
            if pkt_data[23] == 6: # TCP
                tcp_offset = 14 + ihl
                data_offset = (pkt_data[tcp_offset + 12] >> 4) * 4
                payload = pkt_data[tcp_offset + data_offset :]
                if payload:
                    seq = struct.unpack('>I', pkt_data[tcp_offset + 4 : tcp_offset + 8])[0]
                    payloads.append((seq, payload))

payloads.sort(key=lambda x: x[0])
stream = bytearray()
for _, p in payloads:
    stream.extend(p)

decoded = bytes([(b - 42) % 256 for b in stream])
with open('recovered.jpg', 'wb') as out:
    out.write(decoded)
```

Al verificar el tipo de archivo resultante:
```bash
file recovered.jpg
# recovered.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, 800x500
```

### 4. Lectura de la bandera
Abriendo la imagen recuperada `recovered.jpg`, se observa el texto de la bandera dibujado en el centro con estilo *leetspeak*:
```text
academy{...}
```

## Notas adicionales
- El nombre del archivo y la pista ("Don't rely on everything you see including flag format") advierten sobre variantes en la tipografía de mapa de bits (leetspeak: `tr4ck`, `th3`, `tr4ff1c`) y la necesidad de prestar atención a las sustituciones numéricas en vez de caracteres alfabéticos estándar.

## Referencias
- Reto: https://learn.cylabacademy.org/library/717
- Wireshark User's Guide (TCP Stream Reassembly): https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html
