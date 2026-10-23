# New Caesar — CyLab #158

**Categoría:** Cryptography — Medium  
**Plataforma:** CyLab Academy  
**Origen:** picoCTF 2021  
**Referencia:** https://learn.cylabacademy.org/library/158

---

## Descripción

> We found a brand new type of encryption, can you break the secret code? (Wrap with academy{})

Se proporciona un script de cifrado `new_caesar.py` y el texto cifrado directamente en la página del challenge.

**Texto cifrado:**
```
cbdabldadbplblcnpfpnpapapecpcn
```

---

## Hints oficiales

1. *"How does the cipher work if the alphabet isn't 26 letters?"*
2. *"Even though the letters are split up, the same paradigms still apply"*

---

## Solución

### Análisis del algoritmo

El script `new_caesar.py` aplica dos transformaciones en cadena:

**Paso 1 — Codificación base-16 propia (`b16_encode`)**

Alfabeto reducido: `ALPHABET = 'abcdefghijklmnop'` (16 letras).

Para cada carácter del texto plano:
1. Se obtiene su valor ASCII → 8 bits.
2. Se divide en dos nibbles de 4 bits.
3. Cada nibble se mapea a la letra del alfabeto de 16 (0→'a', 1→'b', ..., 15→'p').
4. El texto cifrado tiene el doble de longitud que el original.

**Paso 2 — Cifrado César de 16 letras (`shift`)**

La clave es un único carácter del alfabeto de 16. Se aplica desplazamiento circular mod 16:
```
enc_char = ALPHABET[(nibble_value + key_index) % 16]
```

### Ataque: fuerza bruta sobre 16 claves

El espacio de claves tiene solo 16 posibilidades. Para cada clave se invierte el César y la codificación:

```python
ALPHABET = 'abcdefghijklmnop'
ciphertext = 'cbdabldadbplblcnpfpnpapapecpcn'

def decode_nibble(enc, key):
    key_idx = ALPHABET.index(key)
    shifted = [(ALPHABET.index(c) - key_idx) % 16 for c in enc]
    result = []
    for i in range(0, len(shifted), 2):
        byte = shifted[i] * 16 + shifted[i+1]
        result.append(chr(byte))
    return ''.join(result)

for key in ALPHABET:
    try:
        result = decode_nibble(ciphertext, key)
        if all(32 <= ord(c) < 127 for c in result):
            print(f'key={key}: academy{{{result}}}')
    except:
        pass
```

### Resultado

```
key=m: academy{et_tu?_a91448ca}
```

La referencia "et tu?" es a la frase célebre de Julio César ("Et tu, Brute?"), apropiada para un reto de cifrado César.

---

## Notas adicionales

- El texto cifrado de CyLab (`cbdabldadbplblcnpfpnpapapecpcn`) es diferente al de picoCTF.org (`kjlijdliljhdjdhfkfkhhjkkhhkihlhnhghekfhmhjhkhfhekfkkkjkghghjhlhghmhhhfkikfkfhm`); la plataforma tiene su propia instancia.
- La longitud del ciphertext (30 chars) corresponde a 15 bytes de texto plano = flag content de 15 caracteres.
- La "nueva" en "New Caesar" es la codificación en nibbles que precede al desplazamiento, no el desplazamiento en sí.

---

## Referencias

- CyLab #158: https://learn.cylabacademy.org/library/158
- picoCTF original: https://play.picoctf.org/practice/challenge/56
