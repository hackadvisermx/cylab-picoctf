# Forensics — Rogue Tower

## Descripción
> **Prompt oficial del reto:** "A suspicious cell tower has been detected in the network. Analyze the captured network traffic to identify the rogue tower, find the compromised device, and recover the exfiltrated flag.  
> Download the network capture file: here"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Samuel Dinesh

> **Pistas oficiales:**
> 1. Look for unauthorized test network broadcasts on UDP port 55000
> 2. Find the device that connected to the rogue tower by checking HTTP User-Agent headers
> 3. The encryption key is derived from the victim device's IMSI
> 4. The exfiltrated data is split across multiple HTTP POST requests

## Solución
El reto proporciona un archivo de captura de tráfico de red (`rogue_tower.pcap`).

1. **Identificación de la torre celular no autorizada (Rogue Tower):**
   Siguiendo la pista 1, filtramos los paquetes de broadcast UDP enviados al puerto 55000:
   ```bash
   tshark -r rogue_tower.pcap -Y "udp.port == 55000" -T fields -e frame.number -e ip.src -e data.text
   ```
   Se observan tres emisiones:
   - Paquete 1: IP `192.168.1.1` emitiendo `CARRIER: Verizon PLMN=310410 CELLID=25042`
   - Paquete 2: IP `192.168.1.1` emitiendo `CARRIER: AT&T PLMN=310410 CELLID=25043`
   - Paquete 14: IP `192.168.99.1` emitiendo `UNAUTHORIZED-TEST-NETWORK PLMN=00101 CELLID=98355`

   La torre no autorizada tiene `CELLID=98355`.

2. **Identificación del dispositivo comprometido e IMSI:**
   Revisando las peticiones HTTP y el `User-Agent`:
   ```bash
   tshark -r rogue_tower.pcap -Y "http.request" -T fields -e frame.number -e ip.src -e http.user_agent
   ```
   En el paquete 16, un dispositivo solicita `/api/register` hacia la IP `198.51.100.137` reportando en su cabecera:
   `User-Agent: MobileDevice/1.0 (IMSI:310410670085147; CELL:98355)`
   El IMSI de la víctima es `310410670085147`.

3. **Reconstrucción de la exfiltración:**
   Inmediatamente después del registro, el dispositivo realiza múltiples peticiones HTTP POST a `/upload` (paquetes 17 a 22), transmitiendo fragmentos en Base64 en el cuerpo de cada petición:
   ```bash
   tshark -r rogue_tower.pcap -Y "http.request.method == POST" -T fields -e http.file_data
   ```
   Los fragmentos concatenados forman la cadena:
   `VlNRXFBcTUxFAFdNBm5XBFtcb0wFRgdFaABWDgcHDAVTTQ==`

4. **Descifrado de la bandera:**
   Al decodificar la cadena Base64 obtenemos 34 bytes cifrados. Aplicando una operación XOR repetitiva usando como clave los últimos 8 dígitos del IMSI (`70085147`), se descifra el texto en texto claro con el formato de la academia.

```python
import base64

b64_payload = "VlNRXFBcTUxFAFdNBm5XBFtcb0wFRgdFaABWDgcHDAVTTQ=="
ciphertext = base64.b64decode(b64_payload)
key = b"70085147"

flag = bytes([c ^ key[i % len(key)] for i, c in enumerate(ciphertext)]).decode()
print("Flag:", flag)
```

## Notas adicionales
- El IMSI estándar consta de MCC + MNC + MSIN. En este escenario, la clave de derivación corresponde al sufijo del identificador de suscripción móvil (`MSIN`).
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/714
- Wireshark Display Filters: https://wiki.wireshark.org/DisplayFilters
