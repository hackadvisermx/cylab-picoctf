# credstuff

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2022  
**Plataforma:** CyLab Security Academy  

## Descripción

We found a leak of a blackmarket website's login credentials. Can you find the
password of the user `cultiris` and successfully decrypt it?
Download the leak [here](https://challenge-files.cylabacademy.net/library/7f760cee144ac7237469fd6bfab7c748d6f1d101ca47c101187ca7d8f5c721f0/leak.tar).

The first user in `usernames.txt` corresponds to the first password in
`passwords.txt`. The second user corresponds to the second password, and so on.

## Hints

1. Maybe other passwords will have hints about the leak?

## Solución

El archivo `leak.tar` contiene dos ficheros de texto: `usernames.txt` y `passwords.txt`. Cada línea de usernames corresponde a la misma línea de passwords.

**Paso 1: Extraer y localizar al usuario `cultiris`**

```bash
tar -xf leak.tar
grep -n "cultiris" leak/usernames.txt
```

El usuario `cultiris` está en la línea 378 (índice 377), con la contraseña:

```
npnqrzl{P7e1S_54I35_71Z3}
```

**Paso 2: Identificar el cifrado**

La contraseña parece texto cifrado. Inspeccionando otras contraseñas en el leak se puede notar que muchas tienen estructura legible tras aplicar ROT13. Además, `npnqrzl` decodificado con ROT13 da `academy`, lo que confirma que el cifrado es ROT13.

**Paso 3: Aplicar ROT13**

```python
import codecs
enc = 'npnqrzl{P7e1S_54I35_71Z3}'
dec = codecs.decode(enc, 'rot13')
print(dec)  # academy{C7r1F_54V35_71M3}
```

O con la herramienta de línea de comandos:

```bash
echo "npnqrzl{P7e1S_54I35_71Z3}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

**Resultado:** `academy{C7r1F_54V35_71M3}`

La frase descifrada es "C7r1F_54V35_71M3" (leet speak de "CRIES SAVES TIME" o similar).

## Referencias

- [ROT13 — Wikipedia](https://es.wikipedia.org/wiki/ROT13)
- [picoCTF 2022](https://picoctf.org)
