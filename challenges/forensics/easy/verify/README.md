# Forensics — Verify

## Descripción
> **Prompt oficial del reto:** "People keep trying to trick my players with imitation flags. I want to make sure they get the real thing! I'm going to provide the SHA-256 hash and a decrypt script to help you know that my flags are legitimate."
>
> **Hints:**
> 1. Checksums let you tell if a file is complete and from the original distributor. If the hash doesn't match, it's a different file.
> 2. You can create a SHA checksum of a file with `sha256sum <file>` or all files in a directory with `sha256sum <directory>/*`.
> 3. Remember you can pipe the output of one command to another with `|`. Try practicing with the 'First Grep' challenge if you're stuck!

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** Jeffery John

## Solución
El reto despliega una instancia SSH interactiva donde se entrega un directorio con cientos de archivos cifrados (`files/`), un archivo con el hash SHA-256 esperado (`checksum.txt`) y un script de descifrado (`decrypt.sh`).

1. **Cálculo y filtrado de sumas de verificación:**
   - Para identificar cuál de todos los archivos es el legítimo, se calcula el hash SHA-256 de cada archivo en `files/` y se filtra con `grep` por el hash indicado en `checksum.txt`:
     `deb0a6ad170cd3033d30cae15146719dd4abf37d39136bcb10d88d9c33413374`

2. **Descifrado del archivo correcto:**
   - Una vez aislado el nombre del archivo correspondiente, se le pasa como argumento al script `./decrypt.sh`.
   - El script descifra el archivo empleando OpenSSL y revela la flag en formato `academy{...}`.

```bash
# Conectar por SSH a la instancia
ssh -p <PORT> ctf-player@<HOST>

# Entrar al directorio drop-in y buscar el archivo con el hash correcto
cd drop-in
sha256sum files/* | grep $(cat checksum.txt)

# Descifrar el archivo coincidente
./decrypt.sh $(sha256sum files/* | grep $(cat checksum.txt) | awk '{print $2}')
```

## Notas adicionales
- Los algoritmos de hashing criptográfico (como SHA-256) garantizan la integridad de los datos. En análisis forense y cadena de custodia, el cálculo de hashes es la técnica fundamental para asegurar que las evidencias no han sido alteradas o manipuladas.

## Referencias
- Reto: https://learn.cylabacademy.org/library/450
- NIST Secure Hash Standard: https://csrc.nist.gov/publications/detail/fips/180/4/final
