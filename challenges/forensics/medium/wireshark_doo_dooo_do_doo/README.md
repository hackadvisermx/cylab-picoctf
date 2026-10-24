# Forensics — Wireshark doo dooo do doo...

## Descripción
> **Prompt oficial del reto:** "Can you find the flag?
> [shark1.pcapng](https://challenge-files.cylabacademy.net/library/bcc244e5738c2a9af3a7fd84a79e1bf8436dc32716855581a60e27e526133fd7/shark1.pcapng)"
>
> **Hints:** Ninguna

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2021
- **Autor:** Dylan

## Solución
El reto proporciona una captura de tráfico de red en formato `.pcapng` (`shark1.pcapng`). El análisis se centra en reconstruir las sesiones de comunicación (flujos TCP) intercambiadas entre los hosts.

### Paso 1: Inspección de flujos TCP
Al abrir la captura en Wireshark o inspeccionarla mediante `tshark`, examinamos los distintos flujos de conversación TCP (*Follow TCP Stream*).

En el flujo TCP número 5 (`tcp.stream eq 5`), se observa un payload de texto plano transmitido a través del protocolo HTTP:

```text
Gur synt vf npnqrzl{c33xno00_1_f33_h_qrnqorrs}
```

### Paso 2: Identificación del cifrado y decodificación
La estructura de la cadena `Gur synt vf npnqrzl{...}` corresponde claramente a un texto ofuscado mediante el cifrado de sustitución monoalfabética **ROT13** (donde cada letra es desplazada 13 posiciones: `G` $\rightarrow$ `T`, `u` $\rightarrow$ `h`, `r` $\rightarrow$ `e`):

```bash
# Extracción directa del flujo 5 y decodificación con tr
tshark -r shark1.pcapng -q -z follow,tcp,ascii,5 | tr 'A-Za-z' 'N-ZA-Mn-za-m'

# O mediante Python
python3 -c "
import codecs
s = 'Gur synt vf npnqrzl{c33xno00_1_f33_h_qrnqorrs}'
print(codecs.decode(s, 'rot_13'))
"
```

El resultado revela el mensaje en texto plano:
`The flag is academy{...}`.

## Notas adicionales
- Al analizar capturas `.pcapng` con múltiples flujos, filtrar por protocolos de aplicación (`http`, `ftp`, `smtp`) o seguir flujos TCP individuales permite aislar rápidamente el tráfico interactivo del ruido de red (solicitudes ARP, multidifusión, etc.).

## Referencias
- Reto: https://learn.cylabacademy.org/library/115
- Análisis de flujos TCP en Wireshark: https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html
