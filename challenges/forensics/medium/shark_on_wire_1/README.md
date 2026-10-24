# Forensics — shark on wire 1

## Descripción
> **Prompt oficial del reto:** "We found this [packet capture](https://challenge-files.cylabacademy.net/library/e64f2c2aaf9bf531af7be1787c1407c47a4cc7b57f251d5108a1151e9721a2d6/shark-on-wire-1-capture.pcap). Recover the flag."
>
> **Hints:**
> 1. Try using a tool like Wireshark
> 2. What are streams?

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2019
- **Autor:** Danny

## Solución
El reto provee una captura de tráfico de red en formato PCAP (`shark-on-wire-1-capture.pcap`) que contiene múltiples conversaciones señuelo (decoy) en varios protocolos.

1. **Reconstrucción de flujos UDP (UDP Streams):**
   - La pista sugiere centrarse en el concepto de *flujos* (*streams*). En Wireshark, "Follow UDP Stream" o "Follow TCP Stream" permite reensamblar y visualizar los datos intercambiados entre dos sockets específicos.
   - Analizando secuencialmente los flujos UDP con `tshark` o la interfaz gráfica de Wireshark, la mayoría corresponden a ráfagas de prueba sin sentido.
   - Al llegar al flujo UDP 6 (`udp.stream eq 6`), establecido entre `10.0.0.2:5000` y `10.0.0.12:8888`, se observa una transmisión paquete a paquete que envía alternadamente un número de secuencia y un carácter:
     `a`, `c`, `a`, `d`, `e`, `m`, `y`, `{`, ...

2. **Extracción de la flag:**
   - Volcando el contenido del flujo 6 con `tshark -qz follow,udp,ascii,6` y filtrando los caracteres útiles línea por medio, se reconstruye la flag completa.

```bash
# Volcar la conversación completa del flujo UDP 6
tshark -r shark-on-wire-1-capture.pcap -qz follow,udp,ascii,6

# O extraer directamente la flag filtrando las líneas con payload
tshark -r shark-on-wire-1-capture.pcap -qz follow,udp,ascii,6 | sed -n '7,60p' | sed -n 'n;p' | tr -d '\n'; echo
```

## Notas adicionales
- A diferencia de TCP, el protocolo UDP no tiene estado ni garantiza orden de entrega a nivel de transporte. Para simular un canal de datos ordenado en un reto forense, los paquetes suelen incluir identificadores o transmitirse secuencialmente en un único flujo de datagramas.

## Referencias
- Reto: https://learn.cylabacademy.org/library/30
- Wireshark Follow Stream: https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html
