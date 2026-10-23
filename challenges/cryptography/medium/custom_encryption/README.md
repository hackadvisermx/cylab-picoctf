# Custom Encryption

- **Categoría:** Cryptography / Medium
- **Plataforma:** CyLab Academy (picoCTF 2024)
- **CyLab ID:** 412
- **Referencia:** https://learn.cylabacademy.org/library/412

---

## Descripción

> "Can you get sense of this code file and write the function that will decode the given encrypted file content."

El reto proporciona dos archivos:
- `custom_encryption.py` — el script de cifrado
- `enc_flag` — el resultado cifrado que contiene la flag

---

## Hints oficiales

1. *"Understanding encryption algorithm to come up with decryption algorithm."*

---

## Análisis del algoritmo

El script `custom_encryption.py` implementa un cifrado en dos capas:

### Capa 1: XOR dinámico con clave de texto (`dynamic_xor_encrypt`)

```python
def dynamic_xor_encrypt(plaintext, text_key):
    cipher_text = ""
    key_length = len(text_key)
    for i, char in enumerate(plaintext[::-1]):   # Itera el texto INVERTIDO
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char
    return cipher_text
```

- El texto plano se **invierte** antes de procesar
- Cada carácter del texto invertido se XOR con caracteres de la clave `"trudeau"` (cíclica)
- El resultado es `semi_cipher`

### Capa 2: Multiplicación aritmética (`encrypt`)

```python
def encrypt(plaintext, key):
    cipher = []
    for char in plaintext:
        cipher.append(((ord(char) * key*311)))
    return cipher
```

- Cada carácter de `semi_cipher` se convierte en un entero multiplicando `ord(char) * shared_key * 311`
- El resultado es una lista de enteros

### Generación de la clave compartida (Diffie-Hellman simplificado)

```python
p = 97    # primo
g = 31    # generador
u = pow(g, a, p)
v = pow(g, b, p)
shared_key = pow(v, a, p)  # = pow(u, b, p) por propiedad DH
```

Los valores `a` y `b` se leen del archivo `enc_flag`:
```
a = 94
b = 25
```

Con estos valores: `shared_key = 43`

---

## Solución

El proceso de descifrado invierte las dos capas en orden contrario:

### Paso 1: Revertir la multiplicación aritmética

```python
# cipher[i] = ord(char) * shared_key * 311
# Por tanto: ord(char) = cipher[i] / (shared_key * 311)
char_ord = valor // (shared_key * 311)
```

### Paso 2: Revertir el XOR dinámico

El XOR es su propio inverso. Se aplica la misma operación sobre `semi_cipher` y luego se **invierte** el resultado para recuperar el texto original:

```python
def dynamic_xor_decrypt(semi_cipher, text_key):
    key_length = len(text_key)
    reversed_plaintext = ""
    for i, char in enumerate(semi_cipher):
        key_char = text_key[i % key_length]
        decrypted_char = chr(ord(char) ^ ord(key_char))
        reversed_plaintext += decrypted_char
    return reversed_plaintext[::-1]   # invertir para recuperar el original
```

### Script completo de descifrado

```python
#!/usr/bin/env python3

def generator(g, x, p):
    return pow(g, x) % p

def decrypt(cipher, key):
    divisor = key * 311
    semi_cipher = ""
    for val in cipher:
        char_ord = val // divisor
        semi_cipher += chr(char_ord)
    return semi_cipher

def dynamic_xor_decrypt(semi_cipher, text_key):
    key_length = len(text_key)
    reversed_plaintext = ""
    for i, char in enumerate(semi_cipher):
        key_char = text_key[i % key_length]
        decrypted_char = chr(ord(char) ^ ord(key_char))
        reversed_plaintext += decrypted_char
    return reversed_plaintext[::-1]

# Parámetros del archivo enc_flag
a = 94
b = 25
p = 97
g = 31

# Calcular la clave compartida DH
u = generator(g, a, p)
v = generator(g, b, p)
shared_key = generator(v, a, p)

cipher = [120357, 869245, 213968, 1243689, 1243689, 1123332, 949483, 294206,
          855872, 561666, 0, 1109959, 280833, 66865, 909364, 0, 294206,
          1150078, 13373, 829126, 320952, 361071, 80238, 80238, 227341,
          80238, 347698, 160476, 334325, 307579, 227341, 66865, 80238, 0]

text_key = "trudeau"

semi_cipher = decrypt(cipher, shared_key)
plaintext = dynamic_xor_decrypt(semi_cipher, text_key)
print(f"Flag: {plaintext}")
```

---

## Notas adicionales

- El intercambio de claves Diffie-Hellman con `p=97` y `g=31` es completamente inseguro por los primos tan pequeños; es solo un ejercicio didáctico.
- Los valores `0` en el cifrado corresponden al carácter nulo `chr(0)`, que aparece cuando el carácter del `semi_cipher` coincide con el carácter de la clave XOR.
- La clave `"trudeau"` (7 caracteres) y la clave aritmética `shared_key` son deterministas dado `a` y `b`, por lo que el cifrado es completamente reversible sin conocer el mensaje original.
- El cifrado no es seguro porque: (1) `a` y `b` se imprimen junto al cifrado; (2) los primos son muy pequeños; (3) la multiplicación aritmética no es una función hash ni de dispersión.

---

## Referencias

- https://learn.cylabacademy.org/library/412
- picoCTF 2024 — Custom Encryption
