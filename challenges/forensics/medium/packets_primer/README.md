# Forensics — Packets Primer

## Descripción
> **Prompt oficial del reto:** "Download the packet capture file and use packet analysis software to find the flag.  
> Download packet capture"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

> **Pistas oficiales:**
> 1. Wireshark, if you can install and use it, is probably the most beginner friendly packet analysis software product.

## Solución
El reto suministra un archivo PCAP (`network-dump.flag.pcap`).

1. **Inspección de paquetes:**
   Al abrir la captura en Wireshark o filtrar texto con `strings`:
   ```bash
   strings network-dump.flag.pcap | grep -E "a c a d e m y|p i c o"
   ```
   En uno de los paquetes TCP se transmite la bandera con los caracteres separados por espacios:
   `a c a d e m y { p 4 c k 3 7 _ 5 h 4 r k _ 5 b 0 c 3 5 8 2 }`

2. **Reconstrucción:**
   Eliminando los espacios entre caracteres se ensambla la bandera en el formato estándar.

## Notas adicionales
- Los analizadores de paquetes como Wireshark permiten seguir flujos TCP completos (*Follow TCP Stream*) para inspeccionar cargas útiles (*payloads*) transmitidas en protocolos no cifrados.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/286
- Wireshark Follow TCP Stream: https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html
