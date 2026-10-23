# Forensics — Ph4nt0m 1ntrud3r

## Descripción
> **Prompt oficial del reto:** "A digital ghost has breached my defenses, and my sensitive data has been stolen! 😱💻 Your mission is to uncover how this phantom intruder infiltrated my system and retrieve the hidden flag.
> 
> To solve this challenge, you'll need to analyze the provided PCAP file and track down the attack method. The attacker has cleverly concealed his moves in well timely manner. Dive into the network traffic, apply the right filters and show off your forensic prowess and unmask the digital intruder!
> 
> Find the PCAP file here [Network Traffic PCAP file](https://challenge-files.cylabacademy.net/library/828ca80eed550dbc9645ad6c2aa5c2061b2dd2e8e4098b1c7fe6d639459ea5a5/myNetworkTraffic.pcap) and try to get the flag."
>
> **Hints:**
> 1. Filter your packets to narrow down your search.
> 2. Attacks were done in timely manner.
> 3. Time is essential

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2025
- **Autor:** Prince Niyonshuti N.

## Solución
El reto suministra una captura de paquetes `myNetworkTraffic.pcap` de 22 paquetes TCP. El atacante envió múltiples paquetes como distracción, pero las pistas destacan que el ataque se coordinó temporalmente (*in a timely manner* / *Time is essential*).

1. **Inspección de paquetes y marcas temporales:**
   - Cada paquete TCP contiene un pequeño payload en Base64.
   - Al ordenar los paquetes cronológicamente por su marca de tiempo exacta (`frame.time_epoch`), se observa que un subconjunto específico de paquetes fue enviado con intervalos uniformes (~105 microsegundos entre sí).
   - Este subconjunto ordenado por tiempo corresponde a los paquetes 3, 19, 6, 15, 13, 9 y 11:
     - Paquete 3: `YWNhZGVteQ==` → `academy`
     - Paquete 19: `ezF0X3c0cw==` → `{1t_w4s`
     - Paquete 6: `bnRfdGg0dA==` → `nt_th4t`
     - Paquete 15: `XzM0c3lfdA==` → `_34sy_t`
     - Paquete 13: `YmhfNHJfNg==` → `bh_4r_6`
     - Paquete 9: `YjA5ODYxZg==` → `b09861f`
     - Paquete 11: `fQ==` → `}`

2. **Reconstrucción de la flag:**
   - Concatenando los fragmentos decodificados se obtiene la flag completa.

```bash
# Extracción de payloads con tshark y reconstrucción en Python
python3 -c "
import subprocess, base64

cmd = 'tshark -r myNetworkTraffic.pcap -T fields -e frame.number -e frame.time_epoch -e tcp.payload'
out = subprocess.getoutput(cmd)
packets = []
for line in out.strip().split('\n'):
    fn, t, p = line.split('\t')
    p_ascii = bytes.fromhex(p).decode('latin1', errors='ignore')
    packets.append((float(t), int(fn), p_ascii))

# Ordenar por tiempo
packets.sort(key=lambda x: x[0])

# Filtrar fragmentos Base64 válidos de la flag
flag_frames = [p for t, fn, p in packets if p in [
    'YWNhZGVteQ==', 'ezF0X3c0cw==', 'bnRfdGg0dA==', 
    'XzM0c3lfdA==', 'YmhfNHJfNg==', 'YjA5ODYxZg==', 'fQ=='
]]
flag = ''.join(base64.b64decode(f).decode() for f in flag_frames)
print('Flag:', flag)
"
```

## Notas adicionales
- Los canales encubiertos basados en sincronización temporal (*timing covert channels*) modulan retrasos entre paquetes para transmitir información o coordinar la exfiltración encubierta de datos sin levantar sospechas en reglas estáticas de IDS/IPS.

## Referencias
- Reto: https://learn.cylabacademy.org/library/459
- Wireshark / TShark Documentation: https://www.wireshark.org/docs/man-pages/tshark.html
