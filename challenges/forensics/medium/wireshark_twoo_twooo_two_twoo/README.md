# Forensics — Wireshark twoo twooo two twoo...

## Descripción
> **Prompt oficial del reto:** "Can you find the flag?
> [shark2.pcapng](https://challenge-files.cylabacademy.net/library/0c33dc2894da51c1bbfd7a6f50ac1be2322172fa3a0c5cf37d78cac6915e8b0b/shark2.pcapng)"
>
> **Hints:**
> - "Did you really find _the_ flag?"
> - "Look for traffic that seems suspicious."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Dylan

## Solución
El reto proporciona una captura de red en formato `.pcapng` (`shark2.pcapng`). La inspección inicial de flujos HTTP/TCP revela varias cadenas que aparentan ser flags pero resultan ser señuelos (*red herrings*), en línea con la pista oficial: *"Did you really find the flag?"*.

### Paso 1: Análisis de tráfico sospechoso
Al examinar el desglose de protocolos con Wireshark o `tshark`, se detecta un volumen anómalo de consultas DNS dirigidas hacia un dominio externo específico (`redd.is`):

```bash
tshark -r shark2.pcapng -Y "dns.flags.response == 0 and dns.qry.name contains \"redd.is\"" -T fields -e dns.qry.name | head -n 15
```

Las consultas muestran subdominios codificados que corresponden a fragmentos de texto en Base64:
```text
<base64_chunk_1>.redd.is
<base64_chunk_2>.redd.is
...
```

Esta técnica corresponde a **exfiltración de datos a través de DNS** (*DNS tunneling / exfiltration*), donde un atacante transmite información confidencial simulando solicitudes normales de resolución de nombres a un servidor autoritativo bajo su control.

### Paso 2: Reconstrucción y decodificación de la carga útil
Filtramos las consultas DNS únicas dirigidas a la dirección IP del servidor destino, eliminamos la extensión del dominio y concatenamos las cadenas Base64 en orden cronológico:

```python
import pyshark
import base64
import subprocess

# Extracción de consultas DNS con tshark
cmd = [
    "tshark", "-r", "shark2.pcapng",
    "-Y", "dns and dns.qry.name contains \"redd.is\" and ip.dst == 192.168.38.104",
    "-T", "fields", "-e", "dns.qry.name"
]
queries = subprocess.check_output(cmd).decode().splitlines()

# Limpiar subdominios y concatenar Base64
chunks = []
for q in queries:
    prefix = q.split(".redd.is")[0]
    if prefix not in chunks:
        chunks.append(prefix)

payload = "".join(chunks)
decoded = base64.b64decode(payload).decode("latin-1", errors="ignore")
print("Flag exfiltrada:", decoded)
```

Al decodificar la carga útil completa en Base64, se obtiene la flag auténtica.

## Notas adicionales
- La exfiltración por canal encubierto DNS es uno de los métodos más comunes utilizados por malware y amenazas persistentes (APTs) para eludir inspecciones de cortafuegos perimetrales, dado que el puerto UDP/53 suele estar abierto de forma irrestricta en la mayoría de las redes corporativas.

## Referencias
- MITRE ATT&CK T1071.004: Application Layer Protocol - DNS
- SANS Institute: Detecting DNS Tunneling and Exfiltration
