# Forensics — Riddle Registry

## Descripción
> **Prompt oficial del reto:** "Hi, intrepid investigator! 📄🔍 You've stumbled upon a peculiar PDF filled with what seems like nothing more than garbled nonsense. But beware! Not everything is as it appears. Amidst the chaos lies a hidden treasure—an elusive flag waiting to be uncovered.
> Find the PDF file here [Hidden Confidential Document](https://challenge-files.cylabacademy.net/library/1d073b2830cd8e8e6fb24a8bab184a91b61a25bea90c1d93530e92fe8a368e61/confidential.pdf) and uncover the flag within the metadata."
>
> **Hints:**
> 1. Don't be fooled by the visible text; it’s just a decoy!
> 2. Look beyond the surface for hidden clues

- **Categoría:** Forensics
- **Dificultad:** Easy
- **Evento/origen:** picoMini by CMU-Africa
- **Autor:** Prince Niyonshuti N.

## Solución
El reto proporciona un archivo PDF titulado `confidential.pdf`. Al visualizar el documento se observa texto aparentemente incoherente o de relleno diseñado como distractor. Siguiendo las indicaciones de las pistas y la descripción, el secreto se encuentra en los metadatos del documento.

1. Se inspeccionan los metadatos del PDF utilizando herramientas estándar como `exiftool` o `pdfinfo`.
2. En el campo `Author` de los metadatos aparece una cadena codificada en Base64:
   `YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV82MDZhMGJhOX0=`
3. Al decodificar dicha cadena en Base64 se obtiene directamente la flag en formato `academy{...}`.

```bash
# Inspección de metadatos con exiftool
exiftool confidential.pdf | grep -i author
# Author                          : YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV82MDZhMGJhOX0=

# Decodificación de la cadena Base64
echo "YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV82MDZhMGJhOX0=" | base64 -d
```

En Python se puede realizar de forma directa:
```python
import base64
import subprocess

author = subprocess.getoutput("exiftool -s3 -Author confidential.pdf")
flag = base64.b64decode(author).decode()
print("Flag encontrada:", flag)
```

## Notas adicionales
- Los metadatos de documentos ofimáticos (PDF, DOCX) a menudo conservan información sensible del creador, historial de revisiones o datos ocultos que no se muestran en el renderizado visual.

## Referencias
- Reto: https://learn.cylabacademy.org/library/530
- ExifTool Documentation: https://exiftool.org/
