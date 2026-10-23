# caesar

**Categoría:** Cryptography  
**Dificultad:** Medium  
**Evento:** picoCTF 2019  
**Plataforma:** CyLab Security Academy  

## Descripción

Decrypt this message.  
Message: [message](https://challenge-files.cylabacademy.net/library/297f472a962ab45ee79af5ff4d616ba5206c85d5f4f5cfd41109602354d4121a/data.enc)

## Hints

1. Caesar cipher [tutorial](https://learncryptography.com/classical-encryption/caesar-cipher)

## Solución

El archivo `data.enc` contiene el texto cifrado en formato `academy{<ciphertext>}`. El cifrado César desplaza cada letra del alfabeto un número fijo de posiciones. Para descifrar se prueba cada uno de los 26 desplazamientos posibles hasta encontrar texto legible en inglés.

**Texto cifrado (interior):** `xmjnndiboczmpwdxjizaukqzbt`

Se prueban todos los desplazamientos de 0 a 25:

```python
ciphertext = 'xmjnndiboczmpwdxjizaukqzbt'

def caesar_decrypt(text, shift):
    result = []
    for c in text:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result.append(chr((ord(c) - base - shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

for shift in range(26):
    print(f'Shift {shift:2d}: {caesar_decrypt(ciphertext, shift)}')
```

Con desplazamiento **21** se obtiene `crossingtherubiconefzpvegy`, que contiene la frase reconocible "crossing the rubicon" (expresión que significa tomar una decisión irreversible, referente al cruce del río Rubicón por Julio César).

La flag completa es: `academy{crossingtherubiconefzpvegy}`

## Referencias

- [Cifrado César - Learn Cryptography](https://learncryptography.com/classical-encryption/caesar-cipher)
- [Caesar Cipher - Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
