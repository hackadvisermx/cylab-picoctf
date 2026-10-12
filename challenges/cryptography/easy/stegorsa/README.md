# Cryptography — StegoRSA

## Descripción
> **Prompt oficial del reto:** "A message has been encrypted using RSA. The public key is gone... but someone might have been careless with the private key. Can you recover it and decrypt the message? Download the flag and image."

- **Categoría:** Cryptography
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2026
- **Autor:** Yahaya Meddy

## Solución
Se entregan dos archivos: `flag.enc` (256 bytes = ciphertext RSA-2048) y `image.jpg`. El reto dice que alguien fue "descuidado con la clave privada" → la clave privada está **escondida en la imagen** (stego, de ahí "StegoRSA").

Inspeccionando la imagen, el **comentario JPEG** (marcador `0xFFFE`) contiene una cadena hexadecimal larga que, al decodificar, es la clave privada RSA en formato PEM:

```bash
file image.jpg
# ... comment: "2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a..."
# hex -> "-----BEGIN PRIVATE KEY-----\n..."
```

Extracción del comentario y reconstrucción del PEM:

```python
data=open('image.jpg','rb').read()
# localizar el marcador COM (0xFFFE) y leer su payload
# ... -> comment (hex)
pem=bytes.fromhex(comment.decode())
open('priv.pem','wb').write(pem)   # -----BEGIN PRIVATE KEY----- ...
```

Con la clave privada, se descifra `flag.enc` (RSA con padding PKCS#1 v1.5):

```bash
openssl pkeyutl -decrypt -inkey priv.pem -in flag.enc
# academy{rs4_k3y_1n_1mg_d97b7bfb}
```

## Notas adicionales
- El nombre "StegoRSA" junta **esteganografía** (clave oculta en la imagen) con **RSA**. No hay que romper RSA: la clave privada se filtró entera, solo hay que encontrarla dentro del JPEG.
- El comentario JPEG (segmento `COM`, marcador `0xFFFE`) es un lugar clásico para esconder datos; herramientas como `exiftool`, `strings` o parsear los segmentos a mano lo revelan.
- La flag privada se guarda aquí como `priv.pem` (extraída de la imagen); no es secreto del usuario, es parte del reto.

## Referencias
- Reto: https://learn.cylabacademy.org/library/719
