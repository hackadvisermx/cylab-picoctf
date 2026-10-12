# Cryptography — interencdec

## Descripción
> **Prompt oficial del reto:** "Can you get the real meaning from this file. Download the file here."
>
> **Hints:**
> 1. Engaging in various decoding processes is of utmost importance

- **Categoría:** Cryptography
- **Dificultad:** Easy
- **Evento/origen:** picoCTF 2024
- **Autor:** NGIRIMANA Schadrack

## Solución
El archivo `enc_flag` es una cadena con **varias capas de codificación** encadenadas (tags del reto: base64, caesar):

1. **Base64** (capa externa) → devuelve un bytes-literal de Python que contiene otra cadena Base64.
2. **Base64** (capa interna) → `hjhkltf{jhlzhy_k3jy9wa3k_81lk9m02}`.
3. **César**: el prefijo `hjhkltf` debe ser `academy`, lo que da un desplazamiento de **-7**.

```bash
# capa 1 y 2
cat enc_flag | base64 -d        # -> b'aGpoa2x0ZntqaGx6aHlfazNqeTl3YTNrXzgxbGs5bTAyfQ=='
echo "aGpoa2x0ZntqaGx6aHlfazNqeTl3YTNrXzgxbGs5bTAyfQ==" | base64 -d
# -> hjhkltf{jhlzhy_k3jy9wa3k_81lk9m02}
```

```python
# capa 3: César -7
s='hjhkltf{jhlzhy_k3jy9wa3k_81lk9m02}'
print(''.join(chr((ord(c)-ord('a')-7)%26+ord('a')) if c.isalpha() else c for c in s))
# academy{caesar_d3cr9pt3d_81ed9f02}
```

## Notas adicionales
- Clave para resolverlo: probar decodificaciones en cadena (Base64 → Base64 → César) hasta que el prefijo tenga sentido. El desplazamiento del César se deduce alineando `hjhkltf` con el prefijo conocido `academy`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/418
