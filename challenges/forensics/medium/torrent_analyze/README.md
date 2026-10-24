# Forensics — Torrent Analyze

## Descripción
> **Prompt oficial del reto:** "SOS, someone is torrenting on our network.  
> One of your colleagues has been using torrent to download some files on the company’s network. Can you identify the file(s) that were downloaded? The file name will be the flag, like `academy{filename}`.  
> Captured traffic."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** Mubarak Mikail

> **Pistas oficiales:**
> 1. Download and open the file with a packet analyzer like Wireshark.
> 2. You may want to enable BitTorrent protocol (BT-DHT, etc.) on Wireshark. Analyze -> Enabled Protocols
> 3. Try to understand peers, leechers and seeds.
> 4. The file name ends with `.iso`

## Solución
El reto suministra una captura de paquetes de red (`torrent.pcap`) que contiene tráfico generado por clientes BitTorrent mediante la red DHT (*Distributed Hash Table*).

1. **Análisis de tráfico BitTorrent / DHT:**
   Al abrir la captura en Wireshark o inspeccionarla con `tshark`, se observan mensajes codificados en formato Bencode (`bencoded dictionary`) asociados a consultas y respuestas DHT (`get_peers`, `announce_peer`).

2. **Extracción del Info Hash:**
   Filtramos los paquetes que contienen consultas de torrent o buscamos la cadena `info_hash`:
   ```bash
   tshark -r torrent.pcap -Y "bt-dht" -T fields -e bt-dht.bencoded.string | grep "info_hash"
   ```
   O mediante búsqueda directa en Python de los 20 bytes del `info_hash` de BitTorrent:
   El hash SHA-1 identificado en las peticiones salientes es:
   `e2467cbf021192c241367b892230dc1e05c0580e`

3. **Resolución del nombre del archivo descargado:**
   Consultando bases de datos públicas de torrents o trackers por el SHA-1 del info hash, este hash corresponde a la imagen de instalación oficial de Ubuntu Desktop 19.10:
   `ubuntu-19.10-desktop-amd64.iso`

   Siguiendo el formato indicado en el enunciado (`academy{filename}`), se ensambla la bandera.

## Notas adicionales
- En las redes BitTorrent distribuidas (Kademlia DHT), los clientes anuncian y buscan enjambres utilizando el hash SHA-1 de 20 bytes del diccionario `info` del archivo `.torrent`, lo que permite identificar el contenido exacto transmitido aun si el tráfico de datos esté cifrado.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/311
- BitTorrent Protocol Specification (BEP 0005: DHT Protocol): http://www.bittorrent.org/beps/bep_0005.html
