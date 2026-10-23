# ReadMyCert

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2023  
**Plataforma:** CyLab Security Academy  

## Descripción

How about we take you on an adventure on exploring certificate signing requests.
Take a look at this [CSR file](https://challenge-files.cylabacademy.net/library/adc86ad64fdfdb57ccdc30281c4c93aa2a8a913259426681737dc7e69d257275/readmycert.csr).

## Hints

1. Download the certificate signing request and try to read it.

## Solución

Se descarga el archivo `.csr` (Certificate Signing Request) y se lee con `openssl`:

```bash
curl -O https://challenge-files.cylabacademy.net/library/adc86ad64fdfdb57ccdc30281c4c93aa2a8a913259426681737dc7e69d257275/readmycert.csr

openssl req -in readmycert.csr -text -noout
```

La flag está embebida directamente en el campo **Common Name (CN)** del Subject:

```
Subject: CN=academy{read_mycert_1767ceb4}, name=ctfPlayer
```

Flag: `academy{read_mycert_1767ceb4}`

## Referencias

- [OpenSSL - Certificate Signing Request](https://www.openssl.org/docs/man1.1.1/man1/req.html)
- [¿Qué es un CSR? - DigiCert](https://www.digicert.com/kb/csr-overview.htm)
