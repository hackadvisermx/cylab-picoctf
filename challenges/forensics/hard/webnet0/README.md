# Forensics — WebNet0

## Descripción
> **Prompt oficial del reto:** "We found this [packet capture](https://challenge-files.cylabacademy.net/library/2d15538465c5948f0f0626d0cdd271f74363c00aa99d694730fe98331946ab88/webnet0-capture.pcap) and [key](https://challenge-files.cylabacademy.net/library/2d15538465c5948f0f0626d0cdd271f74363c00aa99d694730fe98331946ab88/picopico.key). Recover the flag."
>
> **Hints:**
> 1. Try using a tool like Wireshark.
> 2. How can you decrypt the TLS stream?

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Jason

## Solución
El reto proporciona un archivo de captura de red PCAP (`capture.pcap`) y una clave RSA privada (`picopico.key`).

1. **Configuración de la clave privada en Wireshark/tshark:**
   - La captura contiene una conversación HTTPS protegida mediante TLS 1.2.
   - En Wireshark o tshark, se suministra la clave privada RSA asociada al servidor mediante la preferencia `uat:rsa_keys` para que el analizador derive la clave de sesión y descifre el flujo TLS.

2. **Extracción de la información en texto plano:**
   - Una vez descifrado el flujo TLS, se observa una respuesta HTTP `200 OK` para la petición `GET /`.
   - Entre las cabeceras HTTP de respuesta se encuentra una cabecera personalizada denominada `Pico-Flag`, cuyo valor contiene la bandera.

```bash
# Descifrar la captura con tshark y buscar cabeceras HTTP que contengan la bandera
tshark -r capture.pcap \
  -o "uat:rsa_keys:\"picopico.key\",\"\"" \
  -Y "http" \
  -T fields \
  -e http.response.line | grep -i "pico-flag"
```

## Notas adicionales
- En Wireshark interactivo, el descifrado puede configurarse en `Edit` -> `Preferences` -> `Protocols` -> `TLS` -> `RSA keys list`, añadiendo la IP del servidor y la ruta de `picopico.key`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/32
- Wireshark TLS Dissection Guide: https://wiki.wireshark.org/TLS
