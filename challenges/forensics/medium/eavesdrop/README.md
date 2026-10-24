# Forensics — Eavesdrop

## Descripción
> **Prompt oficial del reto:** "Download this packet capture and find the flag.  
> Download packet capture"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** LT 'syreal' Jones

> **Pistas oficiales:**
> 1. All we know is that this packet capture includes a chat conversation and a file transfer.

## Solución
El reto provee una captura de paquetes de red (`capture.flag.pcap`).

1. **Análisis de la conversación TCP (Stream 0):**
   Al seguir el primer flujo TCP (`tcp.stream eq 0`) en Wireshark:
   ```text
   - Hey, how do you decrypt this file again?
   - You're so dumb, use this:
     openssl des3 -d -salt -in file.des3 -out file.txt -k supersecretpassword123
   - OK great! Where is it?
   - Just tell your friend to run the file transfer script with 'nc 10.0.2.4 9002'
   ```

2. **Extracción del archivo cifrado (Stream en puerto 9002):**
   Filtramos los paquetes transmitidos por el puerto 9002:
   ```bash
   tshark -r capture.flag.pcap -Y "tcp.port == 9002" -T fields -e data
   ```
   La carga útil comienza con la cabecera `Salted__` (`53616c7465645f5f`). Guardamos estos bytes binarios como `file.des3`.

3. **Descifrado con OpenSSL:**
   Ejecutamos el comando indicado en el chat:
   ```bash
   openssl des3 -d -salt -in file.des3 -out file.txt -k supersecretpassword123
   cat file.txt
   ```
   El archivo descifrado contiene la bandera de la academia.

## Notas adicionales
- Las suites criptográficas heredadas como 3DES (*Triple DES*) están obsoletas para entornos seguros modernos, pero siguen apareciendo en análisis forense y protocolos legacy.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/264
- OpenSSL enc manual: https://www.openssl.org/docs/manmaster/man1/openssl-enc.html
