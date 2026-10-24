# Forensics — shark on wire 2

## Descripción
> **Prompt oficial del reto:** "We found this [packet capture](https://challenge-files.cylabacademy.net/library/f76620763560ca0683be36e0ed4648743f969ab4d852fda0d8fb4d3ae21a173d/shark-on-wire-2-capture.pcap). Recover the flag that was pilfered from the network."
>
> **Hints:**
> *(Sin pistas oficiales)*

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny

## Solución
El reto provee un archivo PCAP (`shark-on-wire-2-capture.pcap`) que contiene tráfico de red donde los datos de la flag no están en el payload habitual, sino exfiltrados a través de un canal encubierto (*covert channel* / esteganografía de red).

1. **Identificación del flujo de exfiltración:**
   - Buscando cadenas indicadoras como `"start"` o `"end"`, se identifica una conversación UDP generada desde la dirección IP `10.0.0.66` hacia `10.0.0.1` en el puerto de destino 22.
   - El payload de cada paquete es irrelevante, pero los puertos de origen UDP (`udp.srcport`) siguen un patrón claro: todos tienen valores en el rango `5000 + c`, donde `c` es el código ASCII decimal de cada carácter de la flag (por ejemplo, puerto `5097` $\rightarrow 5097 - 5000 = 97 \rightarrow \text{'a'}$).

2. **Extracción y decodificación del canal encubierto:**
   - Usando `tshark`, se filtran los paquetes enviados por `10.0.0.66` y se extraen los puertos de origen.
   - Restando 5000 a cada valor de puerto y convirtiéndolo a carácter ASCII, se reconstruye la flag completa.

```bash
# Extracción de puertos de origen y decodificación en una sola línea
tshark -r shark-on-wire-2-capture.pcap -Y "ip.src == 10.0.0.66 && ip.dst == 10.0.0.1 && udp.port == 22" -T fields -e udp.srcport | \
awk '{if ($1 > 5000 && $1 < 5255) printf "%c", $1 - 5000} END {print ""}'
```

```python
#!/usr/bin/env python3
"""Decodificación de canal encubierto UDP en shark on wire 2"""
import subprocess

cmd = [
    "tshark", "-r", "shark-on-wire-2-capture.pcap",
    "-Y", "ip.src == 10.0.0.66 && ip.dst == 10.0.0.1 && udp.port == 22",
    "-T", "fields", "-e", "udp.srcport"
]
ports = subprocess.check_output(cmd, text=True).split()
flag = "".join(chr(int(p) - 5000) for p in ports if 5000 < int(p) < 5255)
print("Flag:", flag)
```

## Notas adicionales
- La esteganografía en cabeceras de red (*Network Protocol Steganography*) aprovecha campos como números de secuencia TCP, identificadores IP o puertos efímeros para transferir información evadiendo sistemas de detección de intrusos (NIDS) basados únicamente en inspección de carga útil (*deep packet inspection*).

## Referencias
- Reto: https://learn.cylabacademy.org/library/84
- Network Covert Channels: https://en.wikipedia.org/wiki/Covert_channel
