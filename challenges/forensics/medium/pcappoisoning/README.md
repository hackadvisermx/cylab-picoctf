# Forensics — PcapPoisoning

## Descripción
> **Prompt oficial del reto:** "How about some packet analysis?
> Download the packet capture [here](https://challenge-files.cylabacademy.net/library/2335607ab0153f2881e9e17bb2d589d825646b3aac811bcff90ca3f7a749f9d3/trace.pcap)."
>
> **Hints:**
> 1. Wireshark and strings are both useful tools here.

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** Mubarak Mikail

## Solución
El reto provee un archivo de captura de tráfico de red en formato PCAP llamado `trace.pcap` de aproximadamente 104 KB.

1. **Análisis de cadenas y triage rápido:**
   - Dado que muchas capturas contienen texto en claro transportado en capas de aplicación o campos de datos no cifrados, el primer paso de triage forense es buscar patrones de cadenas conocidos (`academy{` o `picoCTF{`).
   - El comando `strings` localiza de forma directa la cadena de la flag en el volcado de paquetes.

2. **Inspección de paquetes con Tshark / Wireshark:**
   - Al filtrar el paquete exacto mediante `tshark`:
     - Frame 507: Tráfico TCP entre `10.200.0.2` y `10.253.0.6`, puerto origen 20 hacia puerto destino 21.
     - En el payload de datos del paquete de retransmisión TCP se encuentra almacenada la flag en texto claro.

```bash
# Método 1: Búsqueda rápida con strings y grep
strings trace.pcap | grep -E "academy\{|picoCTF\{"

# Método 2: Inspección estructurada con tshark
tshark -r trace.pcap -Y 'frame contains "academy"' -T fields -e frame.number -e ip.src -e ip.dst -e _ws.col.Info

# Método 3: Volcado del payload con Wireshark/tshark
tshark -r trace.pcap -Y 'frame.number == 507' -x
```

## Notas adicionales
- `trace.pcap` contiene múltiples conversaciones señuelo (decoy) con paquetes normales para desviar la atención, pero el contenido sin cifrar en los paquetes TCP permite una extracción inmediata.
- En investigaciones de incidentes de red (Network Forensics), filtrar por palabras clave y patrones regex conocidos en el contenido de tramas permite una rápida identificación de Indicadores de Compromiso (IoC) y filtraciones de datos.

## Referencias
- Reto: https://learn.cylabacademy.org/library/362
- Wireshark Display Filters: https://www.wireshark.org/docs/dfref/
