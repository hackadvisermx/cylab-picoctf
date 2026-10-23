# Forensics — WPA-ing Out

## Descripción
> **Prompt oficial del reto:** "I thought that my password was super-secret, but it turns out that passwords passed over the AIR can be CRACKED, especially if I used the same wireless network password as one in the rockyou.txt credential dump.
> Use this '[pcap file](https://challenge-files.cylabacademy.net/library/14d2e2f2da78ce901cceaff734ed2bca4555097ceb52f486e7836a799b411adc/wpa-ing_out.pcap)' and the rockyou wordlist. The flag should be entered in the academy{XXXXXX} format."
>
> **Hints:**
> 1. Finding the IEEE 802.11 wireless protocol used in the wireless traffic packet capture is easier with wireshark, the JAWS of the network.
> 2. Aircrack-ng can make a pcap file catch big air...and crack a password.

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2021
- **Autor:** MistressVampy

## Solución
El reto proporciona una captura de tráfico inalámbrico IEEE 802.11 (`wpa-ing_out.pcap`). El objetivo es recuperar la clave precompartida (WPA-PSK) mediante un ataque de diccionario offline contra el saludo de cuatro vías (*4-way handshake*) capturado.

1. **Identificación de la red y el handshake:**
   - Al filtrar por `wlan.fc.type_subtype == 8` (Beacon frames) y `eapol` en Wireshark/tshark, se identifica el SSID `Gone_Surfing` (BSSID `00:5f:67:4f:6a:1a`) y un intercambio completo de 4 mensajes EAPOL.

2. **Ataque de diccionario (Aircrack-ng / Hashcat):**
   - Se puede utilizar `aircrack-ng` directamente:
     ```bash
     aircrack-ng -w rockyou.txt -b 00:5f:67:4f:6a:1a wpa-ing_out.pcap
     ```
   - O convertir el archivo a formato Hashcat 22000 con `hcxpcapngtool` y utilizar GPU:
     ```bash
     hcxpcapngtool -o wpa.22000 wpa-ing_out.pcap
     hashcat -m 22000 -a 0 wpa.22000 rockyou.txt
     ```
   - El ataque recupera con éxito la clave compartida de la red WiFi: `mickeymouse`.
   - Envolviendo la contraseña en el formato requerido `academy{...}` se obtiene la flag.

```bash
# 1. Convertir captura pcap a formato 22000
hcxpcapngtool -o wpa.22000 wpa-ing_out.pcap

# 2. Ejecutar hashcat contra el diccionario rockyou.txt
hashcat -m 22000 -a 0 wpa.22000 rockyou.txt
# Status: Cracked
# 652f6c0e75f049276aaa6a06a724b9a9:005f674f6a1a:1cbfce17b0be:Gone_Surfing:mickeymouse
```

## Notas adicionales
- El protocolo WPA/WPA2-PSK deriva la Pairwise Master Key (PMK) aplicando PBKDF2-HMAC-SHA1 a la contraseña y al SSID con 4096 iteraciones. La debilidad reside en que contraseñas humanas cortas o presentes en listas de credenciales filtradas son susceptibles a ataques de fuerza bruta offline sin interactuar con el punto de acceso.

## Referencias
- Reto: https://learn.cylabacademy.org/library/237
- IEEE 802.11i-2004 Wireless Security Specification: https://standards.ieee.org/
- Hashcat WPA-PBKDF2-PMKID+EAPOL (Mode 22000): https://hashcat.net/wiki/doku.php?id=cracking_wpawpa2
