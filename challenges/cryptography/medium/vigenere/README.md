# Vigenere — picoCTF 2022 / CyLab #316

**Categoría:** Cryptography — Medium  
**Plataforma:** CyLab Academy  
**Referencia:** https://learn.cylabacademy.org/library/316

---

## Descripción

> Can you decrypt this message? Decrypt this message using this key 'CYLAB'.

Se nos proporciona un archivo `cipher.txt` con un texto cifrado mediante el cifrado de Vigenere y se nos da la clave: **CYLAB**.

---

## Hints oficiales

- https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher

---

## Solución

### Análisis del texto cifrado

El contenido de `cipher.txt` es:

```
caldfow{O0NU_WQ3_G1G3O3T3_A1AH3S_4c372077}
```

El formato tiene la estructura típica de una flag (`{...}`), pero con el prefijo cifrado. La clave es **CYLAB** (5 caracteres), que se repite cíclicamente.

### Cifrado de Vigenere — repaso

El cifrado de Vigenere es un cifrado polialfabético por sustitución. Cada letra del texto plano se desplaza en el alfabeto según el índice de la letra correspondiente de la clave:

- **Cifrado:** `C_i = (P_i + K_i) mod 26`
- **Descifrado:** `P_i = (C_i - K_i + 26) mod 26`

Donde `P_i` es la letra del texto plano, `C_i` la del texto cifrado y `K_i` la de la clave (índice 0 = 'A', 1 = 'B', ..., 25 = 'Z'). Los caracteres no alfabéticos (números, guiones bajos, llaves) se mantienen sin cambios.

### Script de descifrado

```python
def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    result = []
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            # Preservar mayúsculas/minúsculas
            base = ord('A') if char.isupper() else ord('a')
            key_shift = ord(key[key_index % len(key)]) - ord('A')
            # Descifrar: restar el desplazamiento de la clave (mod 26)
            decrypted = chr((ord(char) - base - key_shift + 26) % 26 + base)
            result.append(decrypted)
            key_index += 1
        else:
            result.append(char)

    return ''.join(result)


ciphertext = "caldfow{O0NU_WQ3_G1G3O3T3_A1AH3S_4c372077}"
key = "CYLAB"

plaintext = vigenere_decrypt(ciphertext, key)
print(f"Texto cifrado : {ciphertext}")
print(f"Clave         : {key}")
print(f"Texto plano   : {plaintext}")
```

### Ejecución

```
Texto cifrado : caldfow{O0NU_WQ3_G1G3O3T3_A1AH3S_4c372077}
Clave         : CYLAB
Texto plano   : academy{D0NT_US3_V1G3N3R3_C1PH3R_4a372077}
```

### Verificación manual (primeros 7 caracteres)

| Pos | Cifrado | Clave | Índices        | Plano |
|-----|---------|-------|----------------|-------|
| 0   | c (2)   | C (2) | (2-2+26)%26=0  | a     |
| 1   | a (0)   | Y(24) | (0-24+26)%26=2 | c     |
| 2   | l (11)  | L(11) | (11-11+26)%26=0| a     |
| 3   | d (3)   | A (0) | (3-0+26)%26=3  | d     |
| 4   | f (5)   | B (1) | (5-1+26)%26=4  | e     |
| 5   | o (14)  | C (2) | (14-2+26)%26=12| m     |
| 6   | w (22)  | Y(24) | (22-24+26)%26=24| y    |

El prefijo descifrado es `academy`, que corresponde al formato de flag de CyLab Academy.

---

## Notas adicionales

- El cifrado de Vigenere fue considerado "le chiffre indéchiffrable" durante siglos, pero hoy es trivialmente rompible incluso sin conocer la clave (análisis de índice de coincidencia, test de Kasiski).
- Con la clave conocida, como en este reto, basta aplicar la operación inversa letra por letra.
- El mensaje descifrado reza `D0NT_US3_V1G3N3R3_C1PH3R` ("Don't use Vigenere cipher"), ironizando sobre la debilidad del propio cifrado usado en el reto.
- El índice de la clave solo avanza para caracteres alfabéticos; los demás se copian sin modificación.

---

## Referencias

- Wikipedia — Cifrado de Vigenere: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
- CyLab Academy #316: https://learn.cylabacademy.org/library/316
