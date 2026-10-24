# Forensics — FindAndOpen

## Descripción
> **Prompt oficial del reto:** "Someone might have hidden the password in the trace file.  
> Find the key to unlock this file. This tracefile might be good to analyze."

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2023
- **Autor:** Mubarak Mikail

> **Pistas oficiales:**
> 1. Download the pcap and look for the password or flag.
> 2. Don't try to use a password cracking tool, there are easier ways here.

## Solución
El reto proporciona un archivo ZIP cifrado (`flag.zip`) y una captura de tráfico de red (`dump.pcap`).

1. **Inspección de la captura de red:**
   Examinando las cadenas de texto dentro del archivo PCAP:
   ```bash
   strings dump.pcap | grep -E "secret|flag"
   ```
   Se detectan varias cadenas y un bloque codificado en Base64 en una de las tramas:
   `AABBHHPJGTFRLKVGhpcyBpcyB0aGUgc2VjcmV0OiBhY2FkZW15e1IzNERJTkdfTE9LZF8=`

2. **Decodificación de la contraseña:**
   Al aislar y decodificar la porción Base64:
   ```bash
   echo "VGhpcyBpcyB0aGUgc2VjcmV0OiBhY2FkZW15e1IzNERJTkdfTE9LZF8=" | base64 -d
   # This is the secret: academy{R34DING_LOKd_
   ```
   La contraseña para desbloquear el archivo ZIP es `academy{R34DING_LOKd_`.

3. **Extracción del archivo ZIP:**
   Utilizando `unzip` o `7zz` con la contraseña recuperada:
   ```bash
   unzip -P "academy{R34DING_LOKd_" flag.zip
   cat flag
   ```
   El contenido del archivo revela la bandera completa.

## Notas adicionales
- Este reto ilustra cómo el análisis de tráfico en texto plano permite recuperar credenciales y material de descifrado (*exfiltrated keys*) sin necesidad de realizar ataques de fuerza bruta sobre contenedores cifrados.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/348
- Wireshark Display Filters: https://wiki.wireshark.org/DisplayFilters
