# Forensics — WebNet1

## Descripción
> **Prompt oficial del reto:** "We found this [packet capture](https://challenge-files.cylabacademy.net/library/afb7599dd63cad30a04eb98d0e4057608120371eb3e8943b632505e32c8b622c/webnet1-capture.pcap) and [key](https://challenge-files.cylabacademy.net/library/afb7599dd63cad30a04eb98d0e4057608120371eb3e8943b632505e32c8b622c/picopico.key). Recover the flag."
>
> **Hints:**
> 1. Try using a tool like Wireshark.
> 2. How can you decrypt the TLS stream?

- **Categoría:** Forensics
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2019
- **Autor:** Jason

## Solución
El reto suministra una captura de tráfico de red en formato PCAP (`capture.pcap`) y una clave privada RSA (`picopico.key`).

1. **Descifrado de tráfico TLS:**
   - La captura contiene una sesión HTTPS (TLSv1.2) negociada mediante RSA como algoritmo de intercambio de claves.
   - Suministrando la clave RSA privada a `tshark` o `Wireshark` (`uat:rsa_keys`), se descifran automáticamente los flujos cifrados de la sesión HTTP.

2. **Inspección de las transferencias HTTP:**
   - Al descifrar el tráfico, se observan varias peticiones HTTP (`GET /second.html`, `GET /starter-template.css`, `GET /vulture.jpg`).
   - Las cabeceras HTTP de respuesta incluyen un encabezado `Pico-Flag` que indica una falsa bandera de distracción (`academy{this.is.not.your.flag.anymore}`).
   - Exportando los objetos HTTP de la sesión (`--export-objects http,...`) se extrae el archivo de imagen `vulture.jpg`.
   - Al ejecutar `strings` sobre `vulture.jpg` o inspeccionar sus metadatos/comentarios se encuentra la bandera legítima embebida en la imagen.

```bash
# 1. Descifrar el tráfico y exportar los archivos transferidos por HTTP
tshark -r capture.pcap \
  -o "uat:rsa_keys:\"picopico.key\",\"\"" \
  --export-objects "http,extracted"

# 2. Buscar la cadena de la bandera dentro de los objetos extraídos
strings extracted/vulture.jpg | grep -E "academy\{|picoCTF\{"
```

## Notas adicionales
- Cuando una captura TLS utiliza conjuntos de cifrado (*cipher suites*) RSA sin Diffie-Hellman efímero (Forward Secrecy), disponer de la clave privada del servidor permite reconstruir todo el tráfico en texto claro de forma retroactiva.

## Referencias
- Reto: https://learn.cylabacademy.org/library/42
- Wireshark TLS Decryption: https://wiki.wireshark.org/TLS#tls-decryption
