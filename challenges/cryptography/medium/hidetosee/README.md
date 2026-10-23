# HideToSee

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2023  
**Plataforma:** CyLab Security Academy  

## Descripción

How about some hide and seek heh?
Look at this [image](https://challenge-files.cylabacademy.net/library/8033762450472ffeea8ef74c4098556d749abc1f4e836b849798e18e9554e5e5/atbash.jpg).

## Hints

1. Download the image and try to extract it.

## Solución

El nombre del archivo (`atbash.jpg`) revela la pista del cifrado a usar después de extraer.

**Paso 1 — Extraer datos con steghide (sin passphrase):**

```bash
curl -O https://challenge-files.cylabacademy.net/library/8033762450472ffeea8ef74c4098556d749abc1f4e836b849798e18e9554e5e5/atbash.jpg
steghide extract -sf atbash.jpg -p "" -xf output.txt
cat output.txt
# zxzwvnb{zgyzhs_xizxp_zz003u7z}
```

> Con Docker en macOS: `docker run --rm -v "$PWD:/data" dominicbreuker/stego-toolkit steghide extract -sf /data/atbash.jpg -p "" -xf /data/output.txt`

**Paso 2 — Aplicar cifrado Atbash al texto extraído:**

El Atbash es un cifrado por sustitución donde cada letra se reemplaza por su espejo en el alfabeto (a↔z, b↔y, c↔x, ...).

```python
def atbash(s):
    result = []
    for c in s:
        if c.islower():
            result.append(chr(ord('z') - (ord(c) - ord('a'))))
        elif c.isupper():
            result.append(chr(ord('Z') - (ord(c) - ord('A'))))
        else:
            result.append(c)
    return ''.join(result)

text = 'zxzwvnb{zgyzhs_xizxp_zz003u7z}'
print(atbash(text))
# academy{atbash_crack_aa003f7a}
```

**Verificación:**
- `zxzwvnb` → `academy`
- `zgyzhs` → `atbash`
- `xizxp` → `crack`

Flag: `academy{atbash_crack_aa003f7a}`

## Referencias

- [Steghide - JPEG Steganography Tool](http://steghide.sourceforge.net/)
- [Atbash Cipher - Wikipedia](https://en.wikipedia.org/wiki/Atbash)
- [dcode.fr - Atbash Cipher](https://www.dcode.fr/atbash-cipher)
